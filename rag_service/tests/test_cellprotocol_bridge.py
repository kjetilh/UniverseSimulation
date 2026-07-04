from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

PYCELL_SRC = Path(__file__).resolve().parents[3] / "PyCellProtocol" / "src"
if str(PYCELL_SRC) not in sys.path:
    sys.path.insert(0, str(PYCELL_SRC))

from cellprotocol.bridge import BridgeCommand, BridgeEndpoint  # noqa: E402
from cellprotocol.identity import Identity  # noqa: E402

from app.cellprotocol_bridge import cells as bridge_cells  # noqa: E402
from app.cellprotocol_bridge.router import create_cellprotocol_router  # noqa: E402
from app.settings import settings  # noqa: E402


def _identity(uuid: str = "requester") -> Identity:
    identity = Identity(displayName="Requester", uuid=uuid)
    identity.properties["scaffold.identityDomain"] = "dimy-dev"
    return identity


def test_gateway_query_run_uses_identity_domain_and_updates_state(monkeypatch):
    seen = {}

    def fake_require_role(case_id, user_id, minimum_role):
        seen["role_check"] = (case_id, user_id, minimum_role)

    def fake_run_query(req):
        seen["query"] = req
        return SimpleNamespace(
            answer="Dere har bygget en case-aware RAG.",
            citations=[
                {
                    "doc_id": "doc-1",
                    "title": "Oversikt",
                    "chunk_id": "chunk-1",
                    "score": 0.91,
                    "excerpt": "case-aware RAG",
                }
            ],
            retrieval_debug={"query_plan": {"case_id": req.case_id}},
        )

    monkeypatch.setattr(bridge_cells, "_require_role", fake_require_role)
    monkeypatch.setattr(bridge_cells, "_run_query", fake_run_query)

    async def run():
        cell = bridge_cells.RAGGatewayServiceCell()
        requester = _identity()
        await cell.set("state.promptProfileCase", "innovasjon_intervjuer", requester)
        result = await cell.set(
            "query.run",
            {
                "case_id": "innovasjon",
                "message": "Hva har vi bygget?",
                "model_profile": "gpt-4.1",
                "top_k": 6,
                "filters": {"tag": "docs"},
            },
            requester,
        )
        state = await cell.get("state", requester)
        return result, state

    result, state = asyncio.run(run())

    assert result["answer"] == "Dere har bygget en case-aware RAG."
    assert state["currentCase"] == "innovasjon"
    assert state["queryInput"] == "Hva har vi bygget?"
    assert state["queryAnswer"] == "Dere har bygget en case-aware RAG."
    assert state["queryCitations"][0]["doc_id"] == "doc-1"
    assert seen["role_check"] == ("innovasjon", "dimy-dev", "viewer")
    assert seen["query"].prompt_profile_case_id == "innovasjon_intervjuer"
    assert seen["query"].filters == {"tag": "docs"}


def test_cases_list_filters_unassigned_cases_when_access_control_enabled(monkeypatch):
    monkeypatch.setattr(settings, "cell_access_control_enabled", True)
    monkeypatch.setattr(
        bridge_cells,
        "case_list_for_user",
        lambda user_id: [
            {"case_id": "visible", "description": "Visible", "enabled": True, "role": "viewer"},
            {"case_id": "hidden", "description": "Hidden", "enabled": True, "role": None},
        ],
    )

    async def run():
        cell = bridge_cells.RAGGatewayServiceCell()
        requester = _identity()
        result = await cell.set("cases.list", None, requester)
        state = await cell.get("state", requester)
        return result, state

    result, state = asyncio.run(run())

    assert result["cases"] == [
        {"case_id": "visible", "description": "Visible", "enabled": True, "role": "viewer"}
    ]
    assert state["currentCase"] == "visible"


def test_admin_payloads_fail_closed_when_role_is_missing(monkeypatch):
    def deny(case_id, user_id, minimum_role):
        raise bridge_cells.CellProtocolAccessError("nope")

    def should_not_call(*args, **kwargs):
        raise AssertionError("catalog_status should not be called")

    monkeypatch.setattr(bridge_cells, "_require_role", deny)
    monkeypatch.setattr(bridge_cells, "catalog_status", should_not_call)

    async def run():
        cell = bridge_cells.RAGGatewayServiceCell()
        return await cell.set(
            "catalog.status",
            {
                "case_id": "haven_project",
                "source_repo": "CellScaffold",
                "source_type": "haven_service_catalog",
            },
            _identity(),
        )

    assert asyncio.run(run()) == "denied"


def test_catalog_publish_delegates_actor_from_cell_identity(monkeypatch):
    seen = {}

    monkeypatch.setattr(bridge_cells, "_require_role", lambda case_id, user_id, minimum_role: None)

    def fake_publish(payload, *, actor=None):
        seen["payload"] = payload
        seen["actor"] = actor
        return {"ok": True, "published": len(payload["chunks"]), "actor": actor}

    monkeypatch.setattr(bridge_cells, "publish_catalog", fake_publish)

    async def run():
        cell = bridge_cells.RAGGatewayServiceCell()
        return await cell.set(
            "catalog.publish",
            {
                "case_id": "haven_project",
                "source_repo": "CellScaffold",
                "source_type": "haven_service_catalog",
                "chunks": [{"chunk_id": "c1", "title": "T", "content": "Body", "metadata": {}}],
            },
            _identity(),
        )

    result = asyncio.run(run())

    assert result["ok"] is True
    assert result["actor"] == "dimy-dev"
    assert seen["payload"]["source_repo"] == "CellScaffold"


def test_prompt_admin_grant_maps_to_case_member_admin(monkeypatch):
    seen = {}

    monkeypatch.setattr(bridge_cells, "_require_role", lambda case_id, user_id, minimum_role: None)
    monkeypatch.setattr(
        bridge_cells,
        "upsert_case_member",
        lambda **kwargs: seen.update(kwargs),
    )
    monkeypatch.setattr(
        bridge_cells,
        "_admin_user_values",
        lambda case_id: [{"user_id": "delegate", "role": "admin"}],
    )

    async def run():
        cell = bridge_cells.RAGPromptAdminServiceCell()
        requester = _identity("owner")
        await cell.set("state.currentCase", "innovasjon", requester)
        return await cell.set("admins.grant", {"user_id": "delegate"}, requester)

    result = asyncio.run(run())

    assert result == [{"user_id": "delegate", "role": "admin"}]
    assert seen == {
        "case_id": "innovasjon",
        "user_id": "delegate",
        "role": "admin",
        "assigned_by": "dimy-dev",
    }


def test_bridge_description_and_configuration_are_swift_shaped():
    async def run():
        owner = Identity(displayName="Owner", uuid="owner")
        cell = bridge_cells.RAGGatewayServiceCell(owner=owner)
        endpoint = BridgeEndpoint(cell, owner=owner)
        description = await endpoint.handle(BridgeCommand("description", cid=1, identity=owner))
        configuration = await cell.get("configuration", owner)
        return description, configuration

    description, configuration = asyncio.run(run())

    payload = description[0].payload.value
    assert payload["name"] == "RAGGateway"
    assert payload["contractTemplate"]["state"] == "template"
    assert configuration.kind == "cellConfiguration"
    assert configuration.value.discovery.sourceCellEndpoint == "cell:///RAGGateway"


def test_cellprotocol_router_exposes_configuration_when_enabled(monkeypatch):
    monkeypatch.setattr(settings, "cellprotocol_allow_insecure_ws", True)
    app = FastAPI()
    app.include_router(create_cellprotocol_router())

    client = TestClient(app)
    response = client.get("/cellprotocol/configurations/RAGGateway")

    assert response.status_code == 200
    payload = response.json()
    assert payload["discovery"]["sourceCellEndpoint"] == "cell:///RAGGateway"
    assert payload["cellReferences"][0]["label"] == "rag"
