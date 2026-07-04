#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import importlib.util
import os
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from types import SimpleNamespace
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HAVEN_ROOT = ROOT.parents[1]
PYCELL_ROOT = Path(os.environ.get("PYCELLPROTOCOL_ROOT", HAVEN_ROOT / "PyCellProtocol"))
CELLPROTOCOL_SWIFT = Path(os.environ.get("CELLPROTOCOL_SWIFT_PATH", HAVEN_ROOT / "CellProtocol"))

sys.path.insert(0, str(PYCELL_ROOT / "src"))
sys.path.insert(0, str(ROOT))

from cellprotocol.bridge import BridgeEndpoint  # noqa: E402
from cellprotocol.identity import Identity  # noqa: E402

from app.cellprotocol_bridge import cells as rag_cells  # noqa: E402


async def main() -> int:
    endpoint = BridgeEndpoint(_make_smoke_cell(), owner=Identity(displayName="python-rag", uuid="python-rag"))
    websocket = _load_pycell_websocket_smoke()
    server = await asyncio.start_server(lambda r, w: websocket.websocket_client(r, w, endpoint), "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]
    print(f"PY_RAG_PARITY_SERVER ws://127.0.0.1:{port}/bridgehead/RAGGateway/<bridge-uuid>")
    try:
        package_dir = Path(os.environ.get("RAG_CELL_SWIFT_SMOKE_DIR", tempfile.gettempdir())) / "rag-cell-swift-smoke"
        package_dir.mkdir(parents=True, exist_ok=True)
        _write_swift_package(package_dir, port)
        process = await asyncio.create_subprocess_exec(
            "arch",
            "-arm64",
            "swift",
            "run",
            "RAGCellProtocolSwiftSmoke",
            cwd=package_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        stdout, _stderr = await asyncio.wait_for(process.communicate(), timeout=180)
        print(stdout.decode("utf-8", errors="replace"))
        return process.returncode or 0
    finally:
        server.close()
        await server.wait_closed()


def _make_smoke_cell() -> rag_cells.RAGGatewayServiceCell:
    rag_cells._require_role = lambda case_id, user_id, minimum_role: None
    rag_cells.case_list_for_user = lambda user_id: [
        {"case_id": "swift_smoke", "description": "Swift smoke case", "enabled": True, "role": "admin"}
    ]
    rag_cells._corpus_rows = lambda case_id, q, include_tombstones, limit, offset: (
        1,
        [
            {
                "doc_id": "doc-smoke",
                "title": "Smoke corpus",
                "source_type": "smoke",
                "doc_state": "active",
                "doc_version": 1,
                "chunk_count": 1,
            }
        ],
    )
    rag_cells.catalog_status = lambda case_id, source_repo, source_type: {
        "ok": True,
        "case_id": case_id,
        "source_repo": source_repo,
        "source_type": source_type,
        "active_docs": 1,
        "errors": [],
    }

    def fake_run_query(req: Any) -> SimpleNamespace:
        return SimpleNamespace(
            answer=f"answer:{req.query}",
            citations=[
                {
                    "doc_id": "doc-smoke",
                    "title": "Smoke corpus",
                    "chunk_id": "chunk-smoke",
                    "score": 1.0,
                    "excerpt": "smoke citation",
                }
            ],
            retrieval_debug={"query_plan": {"case_id": req.case_id}},
        )

    rag_cells._run_query = fake_run_query
    return rag_cells.RAGGatewayServiceCell(owner=Identity(displayName="python-rag", uuid="python-rag"))


def _load_pycell_websocket_smoke() -> Any:
    script = PYCELL_ROOT / "scripts" / "swift_parity_smoke.py"
    spec = importlib.util.spec_from_file_location("pycell_swift_parity_smoke", script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load PyCellProtocol websocket smoke helper: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_swift_package(package_dir: Path, port: int) -> None:
    source_dir = package_dir / "Sources" / "RAGCellProtocolSwiftSmoke"
    source_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "Package.swift").write_text(
        textwrap.dedent(
            f"""
            // swift-tools-version:5.8
            import PackageDescription

            let package = Package(
                name: "RAGCellProtocolSwiftSmoke",
                platforms: [.macOS(.v13)],
                dependencies: [
                    .package(path: "{CELLPROTOCOL_SWIFT}")
                ],
                targets: [
                    .executableTarget(
                        name: "RAGCellProtocolSwiftSmoke",
                        dependencies: [
                            .product(name: "CellBase", package: "CellProtocol")
                        ]
                    )
                ]
            )
            """
        ).strip()
        + "\n"
    )
    (source_dir / "main.swift").write_text(_swift_main(port))


def _swift_main(port: int) -> str:
    return (
        textwrap.dedent(
            f"""
            import Foundation
            import CellBase

            @main
            struct RAGCellProtocolSwiftSmoke {{
                static func main() async throws {{
                    CellBase.webSocketSecurityPolicy = .developmentOnlyInsecureAllowed
                    CellBase.sendDataAsText = true

                    let resolver = CellResolver.sharedInstance
                    CellBase.defaultCellResolver = resolver
                    try await resolver.registerDefaultWebSocketBridgeTransports()
                    resolver.registerRemoteCellHost(
                        "127.0.0.1",
                        route: RemoteCellHostRoute(
                            websocketEndpoint: "bridgehead",
                            schemePreference: .ws,
                            pathLayout: .endpointThenPublisherUUID
                        )
                    )

                    let requester = Identity(
                        "00000000-0000-0000-0000-00000000CAFE",
                        displayName: "swift-rag-smoke",
                        identityVault: nil
                    )
                    requester.properties?["scaffold.identityDomain"] = .string("swift-smoke-user")

                    let emit = try await resolver.cellAtEndpoint(
                        endpoint: "cell://127.0.0.1:{port}/RAGGateway",
                        requester: requester
                    )
                    guard let meddle = emit as? Meddle else {{
                        throw SmokeError.notMeddle
                    }}

                    let cases = try await meddle.set(keypath: "cases.list", value: .object([:]), requester: requester)
                    guard case let .object(casesObject)? = cases,
                          case let .list(caseItems)? = casesObject["cases"],
                          caseItems.count == 1 else {{
                        throw SmokeError.unexpected("cases.list", String(describing: cases))
                    }}
                    print("SWIFT_RAG_CASES_OK")

                    let query = try await meddle.set(
                        keypath: "query.run",
                        value: .object([
                            "case_id": .string("swift_smoke"),
                            "message": .string("hello")
                        ]),
                        requester: requester
                    )
                    guard case let .object(queryObject)? = query,
                          case let .string(answer)? = queryObject["answer"],
                          answer == "answer:hello" else {{
                        throw SmokeError.unexpected("query.run", String(describing: query))
                    }}
                    print("SWIFT_RAG_QUERY_OK")

                    let corpus = try await meddle.set(
                        keypath: "corpus.list",
                        value: .object(["case_id": .string("swift_smoke")]),
                        requester: requester
                    )
                    guard case let .object(corpusObject)? = corpus,
                          case let .list(corpusItems)? = corpusObject["items"],
                          corpusItems.count == 1 else {{
                        throw SmokeError.unexpected("corpus.list", String(describing: corpus))
                    }}
                    print("SWIFT_RAG_CORPUS_OK")

                    let status = try await meddle.set(
                        keypath: "catalog.status",
                        value: .object([
                            "case_id": .string("swift_smoke"),
                            "source_repo": .string("CellScaffold"),
                            "source_type": .string("smoke")
                        ]),
                        requester: requester
                    )
                    guard case let .object(statusObject)? = status,
                          case let .bool(ok)? = statusObject["ok"],
                          ok else {{
                        throw SmokeError.unexpected("catalog.status", String(describing: status))
                    }}
                    print("SWIFT_RAG_CATALOG_STATUS_OK")
                    print("SWIFT_RAG_PARITY_SMOKE_OK")
                }}
            }}

            enum SmokeError: Error {{
                case notMeddle
                case unexpected(String, String)
            }}
            """
        ).strip()
        + "\n"
    )


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
