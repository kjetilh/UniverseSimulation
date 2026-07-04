from __future__ import annotations

import asyncio
from typing import Any

from fastapi import APIRouter, WebSocket

from cellprotocol.bridge import BridgeEndpoint, WebSocketBridgeSession
from cellprotocol.identity import InMemoryIdentityVault
from cellprotocol.resolver import CellResolver, CellUsageScope

from app.cellprotocol_bridge.cells import (
    RAGGatewayServiceCell,
    RAGPromptAdminServiceCell,
    rag_gateway_configuration,
    rag_prompt_admin_configuration,
)
from app.settings import settings


def create_cellprotocol_router() -> APIRouter:
    router = APIRouter()
    state: dict[str, Any] = {"resolver": None, "owner": None, "lock": asyncio.Lock()}

    async def ensure() -> tuple[CellResolver, Any]:
        if state["resolver"] is None:
            async with state["lock"]:
                if state["resolver"] is None:
                    state["resolver"], state["owner"] = await _build_resolver()
        return state["resolver"], state["owner"]

    @router.get("/cellprotocol/health")
    async def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "service": "rag-service-cellprotocol",
            "allowInsecureWS": settings.cellprotocol_allow_insecure_ws,
        }

    @router.get("/cellprotocol/cells")
    async def cells() -> dict[str, Any]:
        resolver, owner = await ensure()
        named = await resolver.named_cells(owner)
        return {"cells": {name: await cell.advertise(owner) for name, cell in named.items()}}

    @router.get("/cellprotocol/configurations/RAGGateway")
    async def gateway_configuration() -> dict[str, Any]:
        return rag_gateway_configuration().to_json()

    @router.get("/cellprotocol/configurations/RAGPromptAdmin")
    async def prompt_admin_configuration() -> dict[str, Any]:
        return rag_prompt_admin_configuration().to_json()

    @router.websocket("/bridgehead/{first}/{second}")
    async def bridge_socket(websocket: WebSocket, first: str, second: str) -> None:
        if websocket.url.scheme == "ws" and not settings.cellprotocol_allow_insecure_ws:
            await websocket.close(code=1008)
            return
        resolver, owner = await ensure()
        endpoint_name = second if _looks_like_uuid(first) else first
        try:
            cell = await resolver.cell_at_endpoint(f"cell:///{endpoint_name}", owner)
        except Exception:
            await websocket.close(code=1008)
            return
        await WebSocketBridgeSession(websocket, BridgeEndpoint(cell, owner=owner)).run()

    return router


async def _build_resolver() -> tuple[CellResolver, Any]:
    vault = InMemoryIdentityVault()
    owner = await vault.identity(settings.cellprotocol_owner_context, make_new_if_not_found=True)
    resolver = CellResolver(allows_insecure_websockets=settings.cellprotocol_allow_insecure_ws)
    await resolver.register_named_emit_cell(
        "RAGGateway",
        emit_cell=RAGGatewayServiceCell(owner=owner),
        scope=CellUsageScope.scaffoldUnique,
        identity=owner,
    )
    await resolver.register_named_emit_cell(
        "RAGPromptAdmin",
        emit_cell=RAGPromptAdminServiceCell(owner=owner),
        scope=CellUsageScope.scaffoldUnique,
        identity=owner,
    )
    return resolver, owner


def _looks_like_uuid(value: str) -> bool:
    return len(value) >= 32 and value.count("-") in {0, 4}
