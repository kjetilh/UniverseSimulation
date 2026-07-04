from __future__ import annotations

import asyncio
from typing import Any

from fastapi.encoders import jsonable_encoder

from cellprotocol.configuration import (
    CellConfiguration,
    CellConfigurationDiscovery,
    CellReference,
    SkeletonElement,
)
from cellprotocol.general_cell import GeneralCell
from cellprotocol.keypath import KeyPathError, get_keypath
from cellprotocol.value import KeyValue, TypedValue, from_json_value

from app.api.routes_chat import _run_query
from app.api.routes_cell import (
    CellCollectiveSummaryRequest,
    _build_link_graph,
    _corpus_rows,
)
from app.models.schemas import QueryRequest, QueryResponse
from app.rag.access.control import (
    ROLE_ORDER,
    case_list_for_user,
    delete_case_member,
    global_owner_user_ids,
    has_case_role,
    list_case_members,
    resolve_case_role,
    upsert_case_member,
)
from app.rag.catalog_ingestion import (
    catalog_status,
    media_status,
    publish_catalog,
    publish_media,
    reindex_catalog,
)
from app.rag.cases.loader import case_by_id, load_rag_cases
from app.rag.cases.visibility import visible_cases, visible_case_ids
from app.rag.generate.llm_provider import ModelProfileError, validate_model_profile
from app.rag.generate.prompt_config_store import (
    PromptRuntimeConfig,
    get_runtime_config,
    upsert_runtime_config,
)
from app.rag.interviews.collective import build_collective_summary, prepare_question_set
from app.settings import settings


class CellProtocolAccessError(PermissionError):
    pass


class RAGGatewayServiceCell(GeneralCell):
    """CellProtocol facade over the existing RAG service contracts."""

    def __init__(self, owner: Any | None = None) -> None:
        super().__init__(owner=owner, name="RAGGateway")
        self._lock = asyncio.Lock()
        self._state: dict[str, Any] = {
            "cases": [],
            "currentCase": "",
            "promptProfileCase": "",
            "queryInput": "",
            "queryAnswer": "",
            "queryCitations": [],
            "corpusItems": [],
            "linkItems": [],
            "memberItems": [],
            "interviewItems": [],
            "queryResult": None,
            "corpusResult": None,
            "linksResult": None,
            "membersResult": None,
            "interviewResult": None,
            "catalogPublishResult": None,
            "catalogReindexResult": None,
            "catalogStatus": None,
            "mediaPublishResult": None,
            "mediaStatus": None,
            "lastError": "",
        }
        self._configure_agreement_template()
        self._register_handlers()

    def _configure_agreement_template(self) -> None:
        for keypath in [
            "state",
            "cases",
            "query",
            "corpus",
            "links",
            "interviews",
            "members",
            "catalog",
            "media",
        ]:
            self.agreement_template.add_grant("rw--", keypath)
        for keypath in ["contracts", "configuration", "feed"]:
            self.agreement_template.add_grant("r---", keypath)

    def _register_handlers(self) -> None:
        self._get_handlers["state"] = self._get_state
        self._get_handlers["contracts"] = self._get_contracts
        self._get_handlers["configuration"] = self._get_configuration
        self._set_handlers["state"] = self._set_state
        self._set_handlers["cases.list"] = self._cases_list
        self._set_handlers["query.run"] = self._query_run
        self._set_handlers["corpus.list"] = self._corpus_list
        self._set_handlers["links.case"] = self._links_case
        self._set_handlers["links.document"] = self._links_document
        self._set_handlers["interviews.collectiveSummary"] = self._collective_summary
        self._set_handlers["members.list"] = self._members_list
        self._set_handlers["members.setRole"] = self._members_set_role
        self._set_handlers["members.removeRole"] = self._members_remove_role
        self._set_handlers["catalog.publish"] = self._catalog_publish
        self._set_handlers["catalog.reindex"] = self._catalog_reindex
        self._set_handlers["catalog.status"] = self._catalog_status
        self._set_handlers["media.publish"] = self._media_publish
        self._set_handlers["media.status"] = self._media_status

    async def _get_state(self, keypath: str, requester: Any | None) -> Any:
        _ = requester
        async with self._lock:
            state = _jsonable(self._state)
        if keypath == "state":
            return state
        return _value_at_prefixed_keypath(state, keypath, "state")

    async def _get_contracts(self, keypath: str, requester: Any | None) -> Any:
        _ = keypath, requester
        return _gateway_contracts()

    async def _get_configuration(self, keypath: str, requester: Any | None) -> Any:
        _ = keypath, requester
        return TypedValue("cellConfiguration", rag_gateway_configuration())

    async def _set_state(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = requester
        field = keypath.removeprefix("state.")
        if field == "currentCase":
            normalized = _string_value(value) or ""
        elif field == "queryInput":
            normalized = _string_value(value) or ""
        elif field == "promptProfileCase":
            normalized = _string_value(value) or ""
        else:
            return await self._record_error(f"Unsupported state field: {field}")
        async with self._lock:
            self._state[field] = normalized
        return normalized

    async def _cases_list(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath, value
        user_id = _user_id_for(requester)
        rows = case_list_for_user(user_id)
        if settings.cell_access_control_enabled:
            rows = [row for row in rows if row.get("role")]
        cases = _jsonable({"cases": rows})
        default_case = _first_case_id(cases.get("cases", []))
        async with self._lock:
            self._state["cases"] = cases["cases"]
            if not self._state["currentCase"]:
                self._state["currentCase"] = default_case
            self._state["lastError"] = ""
        return cases

    async def _query_run(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = _object_or_string_payload(value, string_key="message")
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("query.run requires current case.")
            _require_role(case_id, _user_id_for(requester), "viewer")
            message = _string_value(payload.get("message")) or await self._state_string("queryInput")
            if not message:
                return await self._record_error("query.run requires message.")
            prompt_profile_case_id = _string_value(payload.get("prompt_profile_case_id")) or await self._state_string(
                "promptProfileCase"
            )
            query_request = QueryRequest(
                query=message,
                conversation_id=_string_value(payload.get("conversation_id")),
                case_id=case_id,
                filters=payload.get("filters") if isinstance(payload.get("filters"), dict) else {},
                top_k=_int_value(payload.get("top_k")),
                model_profile=_string_value(payload.get("model_profile")),
                prompt_profile_case_id=prompt_profile_case_id or None,
            )
            response = _run_query(query_request)
            trace = None
            if response.retrieval_debug and isinstance(response.retrieval_debug, dict):
                trace = response.retrieval_debug.get("query_plan")
            value_out = QueryResponse(
                answer=response.answer,
                citations=response.citations,
                retrieval_debug=response.retrieval_debug,
                trace=trace,
            )
            result = _jsonable(value_out)
            async with self._lock:
                self._state["currentCase"] = case_id
                self._state["queryInput"] = message
                self._state["queryAnswer"] = result.get("answer", "")
                self._state["queryCitations"] = result.get("citations", [])
                self._state["queryResult"] = result
                self._state["lastError"] = ""
            return result
        except CellProtocolAccessError:
            return "denied"
        except ModelProfileError as error:
            return await self._record_error(str(error))
        except Exception as error:
            return await self._record_error(str(error))

    async def _corpus_list(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("corpus.list requires current case.")
            _require_role(case_id, _user_id_for(requester), "viewer")
            limit = _int_value(payload.get("limit")) or 100
            offset = _int_value(payload.get("offset")) or 0
            q = _string_value(payload.get("q"))
            include_tombstones = bool(_bool_value(payload.get("include_tombstones")) or False)
            total, rows = _corpus_rows(case_id, q, include_tombstones, limit, offset)
            result = _jsonable(
                {
                    "case_id": case_id,
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "items": rows,
                }
            )
            async with self._lock:
                self._state["currentCase"] = case_id
                self._state["corpusItems"] = result["items"]
                self._state["corpusResult"] = result
                self._state["lastError"] = ""
            return result
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _links_case(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("links.case requires current case.")
            _require_role(case_id, _user_id_for(requester), "viewer")
            result = _jsonable(_build_link_graph(case_id, only_doc_id=None, limit_docs=_int_value(payload.get("limit_docs")) or 300))
            await self._store_links_result(case_id, result)
            return result
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _links_document(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            doc_id = _string_value(payload.get("doc_id"))
            if not doc_id:
                return await self._record_error("links.document expects payload {doc_id, case_id?}.")
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("links.document requires current case.")
            _require_role(case_id, _user_id_for(requester), "viewer")
            result = _jsonable(_build_link_graph(case_id, only_doc_id=doc_id, limit_docs=1))
            await self._store_links_result(case_id, result)
            return result
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _collective_summary(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("interviews.collectiveSummary requires current case.")
            _require_role(case_id, _user_id_for(requester), "viewer")
            request_payload = dict(payload)
            request_payload.pop("case_id", None)
            if not request_payload.get("prompt_profile_case_id"):
                prompt_profile_case_id = await self._state_string("promptProfileCase")
                if prompt_profile_case_id:
                    request_payload["prompt_profile_case_id"] = prompt_profile_case_id
            request = CellCollectiveSummaryRequest.model_validate(request_payload)
            validate_model_profile(request.model_profile)
            question_set = prepare_question_set(
                inline_questions=request.questions,
                question_set_path=request.question_set_path,
                question_set_id=request.question_set_id,
            )
            result = _jsonable(
                build_collective_summary(
                    case_id=case_id,
                    prompt_profile_case_id=request.prompt_profile_case_id,
                    question_set=question_set,
                    filters=request.filters,
                    top_k=request.top_k,
                    model_profile=request.model_profile,
                    run_query_fn=_run_query,
                )
            )
            async with self._lock:
                self._state["currentCase"] = case_id
                self._state["interviewItems"] = result.get("items", [])
                self._state["interviewResult"] = result
                self._state["lastError"] = ""
            return result
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _members_list(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath, value
        try:
            case_id = await self._state_string("currentCase")
            if not case_id:
                return await self._record_error("members.list requires current case.")
            _require_role(case_id, _user_id_for(requester), "admin")
            result = {"case_id": case_id, "members": _member_values(case_id)}
            async with self._lock:
                self._state["memberItems"] = result["members"]
                self._state["membersResult"] = result
                self._state["lastError"] = ""
            return result
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _members_set_role(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            target_user_id = _string_value(payload.get("user_id"))
            role = _string_value(payload.get("role"))
            if not target_user_id or not role:
                return await self._record_error("members.setRole expects payload {user_id, role, case_id?}.")
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("members.setRole requires current case.")
            actor = _user_id_for(requester)
            _require_role(case_id, actor, "owner")
            if role == "owner":
                return await self._record_error("Only admin API key can grant owner role.")
            if role not in {"admin", "viewer"}:
                return await self._record_error("role must be owner|admin|viewer.")
            upsert_case_member(case_id=case_id, user_id=target_user_id, role=role, assigned_by=actor)
            result = {"case_id": case_id, "members": _member_values(case_id)}
            async with self._lock:
                self._state["currentCase"] = case_id
                self._state["memberItems"] = result["members"]
                self._state["membersResult"] = result
                self._state["lastError"] = ""
            return result
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _members_remove_role(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            target_user_id = _string_value(payload.get("user_id"))
            if not target_user_id:
                return await self._record_error("members.removeRole expects payload {user_id, case_id?}.")
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("members.removeRole requires current case.")
            actor = _user_id_for(requester)
            _require_role(case_id, actor, "owner")
            if target_user_id in global_owner_user_ids():
                return await self._record_error("Cannot remove env-defined owner.")
            if resolve_case_role(case_id, target_user_id) == "owner":
                return await self._record_error("Only admin API key can remove owner role.")
            delete_case_member(case_id=case_id, user_id=target_user_id)
            result = {"case_id": case_id, "members": _member_values(case_id)}
            async with self._lock:
                self._state["currentCase"] = case_id
                self._state["memberItems"] = result["members"]
                self._state["membersResult"] = result
                self._state["lastError"] = ""
            return result
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _catalog_publish(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        return await self._admin_payload_call(
            value,
            requester,
            state_key="catalogPublishResult",
            operation=lambda payload, actor: publish_catalog(payload, actor=actor),
            required_fields=("case_id",),
            error_prefix="catalog.publish",
        )

    async def _catalog_reindex(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        return await self._admin_payload_call(
            value if isinstance(value, dict) else {},
            requester,
            state_key="catalogReindexResult",
            operation=lambda payload, actor: reindex_catalog(
                case_id=str(payload["case_id"]),
                source_repo=str(payload["source_repo"]),
                source_type=str(payload["source_type"]),
            ),
            required_fields=("case_id", "source_repo", "source_type"),
            error_prefix="catalog.reindex",
        )

    async def _catalog_status(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        return await self._admin_payload_call(
            value if isinstance(value, dict) else {},
            requester,
            state_key="catalogStatus",
            operation=lambda payload, actor: catalog_status(
                case_id=str(payload["case_id"]),
                source_repo=str(payload["source_repo"]),
                source_type=str(payload["source_type"]),
            ),
            required_fields=("case_id", "source_repo", "source_type"),
            error_prefix="catalog.status",
        )

    async def _media_publish(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        return await self._admin_payload_call(
            value,
            requester,
            state_key="mediaPublishResult",
            operation=lambda payload, actor: publish_media(payload, actor=actor),
            required_fields=("case_id",),
            error_prefix="media.publish",
        )

    async def _media_status(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        return await self._admin_payload_call(
            value if isinstance(value, dict) else {},
            requester,
            state_key="mediaStatus",
            operation=lambda payload, actor: media_status(
                case_id=str(payload["case_id"]),
                source_repo=_string_value(payload.get("source_repo")),
                source_type=str(payload["source_type"]),
            ),
            required_fields=("case_id", "source_type"),
            error_prefix="media.status",
        )

    async def _admin_payload_call(
        self,
        value: Any,
        requester: Any | None,
        *,
        state_key: str,
        operation: Any,
        required_fields: tuple[str, ...],
        error_prefix: str,
    ) -> Any:
        try:
            if not isinstance(value, dict):
                return await self._record_error(f"{error_prefix} expects object payload.")
            payload = dict(value)
            case_id = await self._resolved_case_id(payload)
            if case_id and not payload.get("case_id"):
                payload["case_id"] = case_id
            if not case_id:
                return await self._record_error(f"{error_prefix} requires case_id or current case.")
            for field in required_fields:
                if not _string_value(payload.get(field)):
                    return await self._record_error(f"{error_prefix} requires {field}.")
            actor = _user_id_for(requester)
            _require_role(case_id, actor, "admin")
            result = _jsonable(operation(payload, actor))
            async with self._lock:
                self._state["currentCase"] = case_id
                self._state[state_key] = result
                self._state["lastError"] = ""
            return result
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _resolved_case_id(self, payload: dict[str, Any]) -> str:
        payload_case_id = _string_value(payload.get("case_id"))
        async with self._lock:
            if payload_case_id:
                self._state["currentCase"] = payload_case_id
                return payload_case_id
            if self._state["currentCase"]:
                return str(self._state["currentCase"])
            default_case = _first_case_id(self._state["cases"])
            if default_case:
                self._state["currentCase"] = default_case
                return default_case
        return ""

    async def _state_string(self, field: str) -> str:
        async with self._lock:
            return str(self._state.get(field) or "")

    async def _store_links_result(self, case_id: str, result: dict[str, Any]) -> None:
        async with self._lock:
            self._state["currentCase"] = case_id
            self._state["linkItems"] = result.get("items", [])
            self._state["linksResult"] = result
            self._state["lastError"] = ""

    async def _record_error(self, message: str) -> str:
        async with self._lock:
            self._state["lastError"] = message
        return f"error: {message}"


class RAGPromptAdminServiceCell(GeneralCell):
    def __init__(self, owner: Any | None = None) -> None:
        super().__init__(owner=owner, name="RAGPromptAdmin")
        self._lock = asyncio.Lock()
        self._state: dict[str, Any] = {
            "currentCase": "",
            "applyProfileCase": "",
            "adminUserDraft": "",
            "runtimeConfig": None,
            "caseProfiles": [],
            "adminUsers": [],
            "lastError": "",
        }
        self._configure_agreement_template()
        self._register_handlers()

    def _configure_agreement_template(self) -> None:
        self.agreement_template.add_grant("r---", "state")
        for keypath in ["profiles", "runtime", "admins"]:
            self.agreement_template.add_grant("rw--", keypath)
        for keypath in ["contracts", "configuration", "feed"]:
            self.agreement_template.add_grant("r---", keypath)

    def _register_handlers(self) -> None:
        self._get_handlers["state"] = self._get_state
        self._get_handlers["contracts"] = self._get_contracts
        self._get_handlers["configuration"] = self._get_configuration
        self._set_handlers["state"] = self._set_state
        self._set_handlers["profiles.load"] = self._profiles_load
        self._set_handlers["runtime.refresh"] = self._runtime_refresh
        self._set_handlers["runtime.applyCaseProfile"] = self._runtime_apply_case_profile
        self._set_handlers["runtime.clear"] = self._runtime_clear
        self._set_handlers["admins.grant"] = self._admins_grant
        self._set_handlers["admins.revoke"] = self._admins_revoke

    async def _get_state(self, keypath: str, requester: Any | None) -> Any:
        _ = requester
        async with self._lock:
            state = _jsonable(self._state)
        if keypath == "state":
            return state
        return _value_at_prefixed_keypath(state, keypath, "state")

    async def _get_contracts(self, keypath: str, requester: Any | None) -> Any:
        _ = keypath, requester
        return _prompt_admin_contracts()

    async def _get_configuration(self, keypath: str, requester: Any | None) -> Any:
        _ = keypath, requester
        return TypedValue("cellConfiguration", rag_prompt_admin_configuration())

    async def _set_state(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = requester
        field = keypath.removeprefix("state.")
        mapping = {
            "currentCase": "currentCase",
            "applyProfileCase": "applyProfileCase",
            "adminUserDraft": "adminUserDraft",
        }
        if field not in mapping:
            return await self._record_error(f"Unsupported state field: {field}")
        normalized = _string_value(value) or ""
        async with self._lock:
            self._state[mapping[field]] = normalized
        return normalized

    async def _profiles_load(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("profiles.load requires current case.")
            _require_role(case_id, _user_id_for(requester), "admin")
            runtime = _runtime_config_value()
            profiles = _case_prompt_profiles()
            admin_users = _admin_user_values(case_id)
            result = {"cases": profiles, "runtime": runtime}
            async with self._lock:
                self._state["currentCase"] = case_id
                self._state["caseProfiles"] = profiles
                self._state["runtimeConfig"] = runtime
                self._state["adminUsers"] = admin_users
                self._state["lastError"] = ""
            return result
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _runtime_refresh(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("runtime.refresh requires current case.")
            _require_role(case_id, _user_id_for(requester), "admin")
            runtime = _runtime_config_value()
            async with self._lock:
                self._state["currentCase"] = case_id
                self._state["runtimeConfig"] = runtime
                self._state["lastError"] = ""
            return runtime
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _runtime_apply_case_profile(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("runtime.applyCaseProfile requires current case.")
            actor = _user_id_for(requester)
            _require_role(case_id, actor, "admin")
            profile_case_id = _string_value(payload.get("profile_case_id")) or await self._state_string("applyProfileCase")
            if not profile_case_id:
                return await self._record_error("runtime.applyCaseProfile requires profile_case_id.")
            runtime = _apply_case_prompt_profile(profile_case_id, actor)
            async with self._lock:
                self._state["currentCase"] = case_id
                self._state["applyProfileCase"] = profile_case_id
                self._state["runtimeConfig"] = runtime
                self._state["lastError"] = ""
            return runtime
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _runtime_clear(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("runtime.clear requires current case.")
            actor = _user_id_for(requester)
            _require_role(case_id, actor, "admin")
            updated = upsert_runtime_config(
                system_persona_path=None,
                answer_template_path=None,
                updated_by=actor,
                change_note="Cleared from RAGPromptAdminCell",
            )
            runtime = _runtime_config_value(updated)
            async with self._lock:
                self._state["currentCase"] = case_id
                self._state["runtimeConfig"] = runtime
                self._state["lastError"] = ""
            return runtime
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _admins_grant(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("admins.grant requires current case.")
            actor = _user_id_for(requester)
            _require_role(case_id, actor, "owner")
            target = _string_value(payload.get("user_id")) or await self._state_string("adminUserDraft")
            if not target:
                return await self._record_error("admins.grant expects payload {user_id}.")
            upsert_case_member(case_id=case_id, user_id=target, role="admin", assigned_by=actor)
            return await self._store_admin_users(case_id, target)
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _admins_revoke(self, keypath: str, value: Any, requester: Any | None) -> Any:
        _ = keypath
        try:
            payload = value if isinstance(value, dict) else {}
            case_id = await self._resolved_case_id(payload)
            if not case_id:
                return await self._record_error("admins.revoke requires current case.")
            actor = _user_id_for(requester)
            _require_role(case_id, actor, "owner")
            target = _string_value(payload.get("user_id")) or await self._state_string("adminUserDraft")
            if not target:
                return await self._record_error("admins.revoke expects payload {user_id}.")
            if target in global_owner_user_ids():
                return await self._record_error("Cannot revoke env-defined owner.")
            if resolve_case_role(case_id, target) == "owner":
                return await self._record_error("Only admin API key can remove owner role.")
            delete_case_member(case_id=case_id, user_id=target)
            return await self._store_admin_users(case_id, "")
        except CellProtocolAccessError:
            return "denied"
        except Exception as error:
            return await self._record_error(str(error))

    async def _resolved_case_id(self, payload: dict[str, Any]) -> str:
        payload_case_id = _string_value(payload.get("case_id"))
        async with self._lock:
            if payload_case_id:
                self._state["currentCase"] = payload_case_id
                return payload_case_id
            return str(self._state.get("currentCase") or "")

    async def _state_string(self, field: str) -> str:
        async with self._lock:
            return str(self._state.get(field) or "")

    async def _store_admin_users(self, case_id: str, draft: str) -> list[dict[str, str]]:
        admin_users = _admin_user_values(case_id)
        async with self._lock:
            self._state["currentCase"] = case_id
            self._state["adminUserDraft"] = draft
            self._state["adminUsers"] = admin_users
            self._state["lastError"] = ""
        return admin_users

    async def _record_error(self, message: str) -> str:
        async with self._lock:
            self._state["lastError"] = message
        return f"error: {message}"


def rag_gateway_configuration() -> CellConfiguration:
    configuration = CellConfiguration(name="RAG Gateway Workspace")
    configuration.description = "Case-aware workspace for domain RAG query, corpus exploration and link navigation."
    configuration.discovery = CellConfigurationDiscovery(
        sourceCellEndpoint="cell:///RAGGateway",
        sourceCellName="RAGGatewayCell",
        purpose="Domenespesifikk RAG-utforskning",
        purposeDescription="Case-aware RAG for sporsmal, sitater, corpus-utforskning og dokumentlenker.",
        interests=["rag", "documentation", "prompts", "knowledge", "citations", "search"],
        menuSlots=["upperLeft", "upperMid"],
    )
    configuration.cellReferences = [
        CellReference(
            endpoint="cell:///RAGGateway",
            label="rag",
            setKeysAndValues=[KeyValue("cases.list", {}).to_json()],
        )
    ]
    configuration.skeleton = SkeletonElement(
        "VStack",
        {
            "elements": [
                {"Text": {"text": "RAG Gateway Workspace"}},
                {"Button": {"keypath": "rag.cases.list", "label": "Load Cases", "payload": {}}},
                {
                    "TextField": {
                        "sourceKeypath": "rag.state.currentCase",
                        "targetKeypath": "rag.state.currentCase",
                        "placeholder": "Current case_id",
                    }
                },
                {
                    "TextArea": {
                        "sourceKeypath": "rag.state.queryInput",
                        "targetKeypath": "rag.state.queryInput",
                        "placeholder": "Ask a domain question",
                        "minLines": 4,
                        "maxLines": 8,
                        "submitOnEnter": False,
                    }
                },
                {
                    "HStack": {
                        "elements": [
                            {"Button": {"keypath": "rag.query.run", "label": "Run Query", "payload": {}}},
                            {"Button": {"keypath": "rag.corpus.list", "label": "Load Corpus", "payload": {}}},
                            {"Button": {"keypath": "rag.links.case", "label": "Load Links", "payload": {}}},
                        ]
                    }
                },
                {"Divider": {}},
                {"Text": {"text": "Cases"}},
                {"List": {"keypath": "rag.state.cases", "flowElementSkeleton": {"Text": {"keypath": "case_id"}}}},
                {"Divider": {}},
                {"Text": {"text": "Answer"}},
                {"Text": {"keypath": "rag.state.queryAnswer"}},
                {"Text": {"text": "Citations"}},
                {
                    "List": {
                        "keypath": "rag.state.queryCitations",
                        "flowElementSkeleton": {"Text": {"keypath": "title"}},
                    }
                },
                {"Divider": {}},
                {"Text": {"text": "Corpus Items"}},
                {"List": {"keypath": "rag.state.corpusItems", "flowElementSkeleton": {"Text": {"keypath": "title"}}}},
                {"Divider": {}},
                {"Text": {"text": "Link Items"}},
                {"List": {"keypath": "rag.state.linkItems", "flowElementSkeleton": {"Text": {"keypath": "target_href"}}}},
                {"Divider": {}},
                {"Text": {"keypath": "rag.state.lastError"}},
            ]
        },
    )
    return configuration


def rag_prompt_admin_configuration() -> CellConfiguration:
    configuration = CellConfiguration(name="RAG Prompt Admin")
    configuration.description = "Admin workspace for prompt profiles, runtime overrides and delegated prompt admins."
    configuration.discovery = CellConfigurationDiscovery(
        sourceCellEndpoint="cell:///RAGPromptAdmin",
        sourceCellName="RAGPromptAdminCell",
        purpose="RAG promptadministrasjon",
        purposeDescription="Se aktive promptprofiler, sett runtime override og deleger admin-tilgang for RAG promptstyring.",
        interests=["rag", "prompts", "admin", "configuration", "operations"],
        menuSlots=["upperMid", "lowerLeft"],
    )
    configuration.cellReferences = [CellReference(endpoint="cell:///RAGPromptAdmin", label="ragPromptAdmin")]
    configuration.skeleton = SkeletonElement(
        "VStack",
        {
            "elements": [
                {"Text": {"text": "RAG Prompt Admin"}},
                {
                    "TextField": {
                        "sourceKeypath": "ragPromptAdmin.state.currentCase",
                        "targetKeypath": "ragPromptAdmin.state.currentCase",
                        "placeholder": "Upstream case_id",
                    }
                },
                {
                    "TextField": {
                        "sourceKeypath": "ragPromptAdmin.state.applyProfileCase",
                        "targetKeypath": "ragPromptAdmin.state.applyProfileCase",
                        "placeholder": "prompt_profile case_id",
                    }
                },
                {
                    "HStack": {
                        "elements": [
                            {"Button": {"keypath": "ragPromptAdmin.profiles.load", "label": "Load Profiles", "payload": {}}},
                            {"Button": {"keypath": "ragPromptAdmin.runtime.refresh", "label": "Refresh Runtime", "payload": {}}},
                            {
                                "Button": {
                                    "keypath": "ragPromptAdmin.runtime.applyCaseProfile",
                                    "label": "Apply Profile",
                                    "payload": {},
                                }
                            },
                            {"Button": {"keypath": "ragPromptAdmin.runtime.clear", "label": "Clear Override", "payload": {}}},
                        ]
                    }
                },
                {"Divider": {}},
                {"Text": {"keypath": "ragPromptAdmin.state.runtimeConfig.effective_system_persona_path"}},
                {"List": {"keypath": "ragPromptAdmin.state.caseProfiles", "flowElementSkeleton": {"Text": {"keypath": "case_id"}}}},
                {"TextField": {"sourceKeypath": "ragPromptAdmin.state.adminUserDraft", "targetKeypath": "ragPromptAdmin.state.adminUserDraft", "placeholder": "requester uuid or identityDomain"}},
                {
                    "HStack": {
                        "elements": [
                            {"Button": {"keypath": "ragPromptAdmin.admins.grant", "label": "Grant Admin", "payload": {}}},
                            {"Button": {"keypath": "ragPromptAdmin.admins.revoke", "label": "Revoke Admin", "payload": {}}},
                        ]
                    }
                },
                {"List": {"keypath": "ragPromptAdmin.state.adminUsers", "flowElementSkeleton": {"Text": {"keypath": "user_id"}}}},
                {"Text": {"keypath": "ragPromptAdmin.state.lastError"}},
            ]
        },
    )
    return configuration


def _gateway_contracts() -> dict[str, Any]:
    return {
        "state.currentCase": {"expects": "String case_id"},
        "state.promptProfileCase": {"expects": "Optional String prompt_profile_case_id"},
        "state.queryInput": {"expects": "String question or instruction"},
        "cases.list": {"expects": "Empty payload"},
        "query.run": {
            "expects": {
                "case_id": "optional String",
                "prompt_profile_case_id": "optional String",
                "message": "optional String",
                "model_profile": "optional String",
                "top_k": "optional Int",
                "filters": "optional Object",
            }
        },
        "corpus.list": {
            "expects": {
                "case_id": "optional String",
                "q": "optional String",
                "limit": "optional Int",
                "offset": "optional Int",
                "include_tombstones": "optional Bool",
            }
        },
        "links.case": {"expects": {"case_id": "optional String"}},
        "links.document": {"expects": {"case_id": "optional String", "doc_id": "required String"}},
        "interviews.collectiveSummary": {"expects": "Cell collective summary payload"},
        "members.list": {"expects": "Empty payload"},
        "members.setRole": {"expects": {"case_id": "optional String", "user_id": "required String", "role": "required owner|admin|viewer"}},
        "members.removeRole": {"expects": {"case_id": "optional String", "user_id": "required String"}},
        "catalog.publish": {"expects": "Object matching /v1/admin/catalog/publish"},
        "catalog.reindex": {"expects": "Object with case_id, source_repo, source_type"},
        "catalog.status": {"expects": "Object with case_id, source_repo, source_type"},
        "media.publish": {"expects": "Object matching /v1/admin/media/publish"},
        "media.status": {"expects": "Object with case_id, source_repo?, source_type"},
        "configuration": {"returns": "CellConfiguration"},
    }


def _prompt_admin_contracts() -> dict[str, Any]:
    return {
        "state.currentCase": {"expects": "String case_id that selects the upstream instance"},
        "state.applyProfileCase": {"expects": "String case_id whose prompt_profile should be applied"},
        "state.adminUserDraft": {"expects": "String requester UUID or identityDomain to delegate"},
        "profiles.load": {"expects": {"case_id": "optional String upstream case_id"}},
        "runtime.refresh": {"expects": {"case_id": "optional String upstream case_id"}},
        "runtime.applyCaseProfile": {
            "expects": {
                "case_id": "optional String upstream case_id",
                "profile_case_id": "optional String prompt profile case_id",
            }
        },
        "runtime.clear": {"expects": {"case_id": "optional String upstream case_id"}},
        "admins.grant": {"expects": {"user_id": "required String requester UUID or identityDomain"}},
        "admins.revoke": {"expects": {"user_id": "required String requester UUID or identityDomain"}},
        "configuration": {"returns": "CellConfiguration"},
    }


def _require_role(case_id: str, user_id: str, minimum_role: str) -> None:
    cfg = load_rag_cases(settings.rag_cases_path)
    if case_id not in visible_case_ids(cfg):
        raise CellProtocolAccessError(f"Unknown case: {case_id}")
    case_by_id(cfg, case_id)
    if not settings.cell_access_control_enabled:
        return
    if not has_case_role(case_id, user_id, minimum_role):
        raise CellProtocolAccessError(f"User does not have required role '{minimum_role}' for case '{case_id}'.")


def _member_values(case_id: str) -> list[dict[str, str | None]]:
    return [
        {"user_id": member.user_id, "role": member.role, "assigned_by": member.assigned_by}
        for member in list_case_members(case_id)
    ]


def _admin_user_values(case_id: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for member in list_case_members(case_id):
        if ROLE_ORDER.get(member.role, 0) >= ROLE_ORDER["admin"]:
            out.append({"user_id": member.user_id, "role": member.role})
    return out


def _runtime_config_value(runtime_cfg: PromptRuntimeConfig | None = None) -> dict[str, Any]:
    if runtime_cfg is None:
        runtime_cfg = get_runtime_config()
    return _jsonable(_build_prompt_config_response(runtime_cfg))


def _case_prompt_profiles() -> list[dict[str, Any]]:
    runtime_cfg = get_runtime_config()
    cfg = load_rag_cases(settings.rag_cases_path)
    return [_jsonable(_case_prompt_summary(case.case_id, runtime_cfg)) for case in visible_cases(cfg)]


def _apply_case_prompt_profile(profile_case_id: str, actor: str) -> dict[str, Any]:
    cfg = load_rag_cases(settings.rag_cases_path)
    if profile_case_id not in visible_case_ids(cfg):
        raise ValueError(f"Unknown case: {profile_case_id}")
    selected = case_by_id(cfg, profile_case_id)
    system_override = _normalize_optional_text(selected.prompt_profile.system_persona_path)
    answer_override = _normalize_optional_text(selected.prompt_profile.answer_template_path)
    if system_override is None and answer_override is None:
        raise ValueError(f"Case '{selected.case_id}' does not define a prompt_profile.")
    proposed = PromptRuntimeConfig(
        system_persona_path=system_override,
        answer_template_path=answer_override,
        version=0,
        updated_by=actor,
        change_note=f"Apply prompt_profile from case '{selected.case_id}'",
        updated_at=None,
    )
    _runtime_config_value(proposed)
    updated = upsert_runtime_config(
        system_persona_path=system_override,
        answer_template_path=answer_override,
        updated_by=actor,
        change_note=f"Apply prompt_profile from case '{selected.case_id}'",
    )
    return _runtime_config_value(updated)


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _build_prompt_config_response(runtime_cfg: PromptRuntimeConfig) -> Any:
    from app.api.routes_admin import _build_prompt_config_response as build_response

    return build_response(runtime_cfg)


def _case_prompt_summary(case_id: str, runtime_cfg: PromptRuntimeConfig) -> Any:
    from app.api.routes_admin import _case_prompt_summary as case_summary

    return case_summary(case_id, runtime_cfg)


def _value_at_prefixed_keypath(state: dict[str, Any], keypath: str, prefix: str) -> Any:
    relative = keypath.removeprefix(f"{prefix}.")
    try:
        return get_keypath(state, relative)
    except KeyPathError:
        return None


def _object_or_string_payload(value: Any, *, string_key: str) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    raw = _string_value(value)
    return {string_key: raw} if raw else {}


def _user_id_for(identity: Any | None) -> str:
    properties = getattr(identity, "properties", None)
    if isinstance(properties, dict):
        identity_domain = properties.get("scaffold.identityDomain")
        if isinstance(identity_domain, str) and identity_domain.strip():
            return identity_domain.strip()
    uuid = getattr(identity, "uuid", None)
    if isinstance(uuid, str) and uuid.strip():
        return uuid.strip()
    return "anonymous"


def _first_case_id(items: Any) -> str:
    if not isinstance(items, list):
        return ""
    for item in items:
        if isinstance(item, dict):
            case_id = _string_value(item.get("case_id"))
            if case_id:
                return case_id
    return ""


def _string_value(value: Any) -> str | None:
    if isinstance(value, TypedValue):
        value = value.value
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        return str(value)
    return None


def _int_value(value: Any) -> int | None:
    if isinstance(value, TypedValue):
        value = value.value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return None
    return None


def _bool_value(value: Any) -> bool | None:
    if isinstance(value, TypedValue):
        value = value.value
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
    return None


def _jsonable(value: Any) -> Any:
    return from_json_value(jsonable_encoder(value))
