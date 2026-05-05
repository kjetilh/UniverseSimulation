from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import routes_admin
from app.settings import settings


def _client(monkeypatch):
    monkeypatch.setattr(settings, "admin_api_key", "test-admin-key")
    app = FastAPI()
    app.include_router(routes_admin.router)
    return TestClient(app)


def test_catalog_publish_rejects_missing_admin_key(monkeypatch):
    client = _client(monkeypatch)

    response = client.post(
        "/v1/admin/catalog/publish",
        json={
            "case_id": "haven_project",
            "source_repo": "CellScaffold",
            "source_type": "haven_service_catalog",
            "chunks": [
                {
                    "chunk_id": "cellscaffold.rag-gateway.overview",
                    "title": "RAGGatewayCell overview",
                    "content": "RAGGatewayCell supports query.run.",
                    "metadata": {
                        "repo": "CellScaffold",
                        "serviceID": "cellscaffold.rag-gateway",
                        "cell": "RAGGatewayCell",
                        "contract": "query.run",
                        "status": "supported now",
                    },
                }
            ],
        },
    )

    assert response.status_code == 401


def test_catalog_publish_delegates_payload_and_actor(monkeypatch):
    seen = {}

    def fake_publish(payload, *, actor=None):
        seen["payload"] = payload
        seen["actor"] = actor
        return {"ok": True, "published": len(payload["chunks"])}

    monkeypatch.setattr(routes_admin, "publish_catalog", fake_publish)
    client = _client(monkeypatch)

    response = client.post(
        "/v1/admin/catalog/publish",
        headers={"X-API-Key": "test-admin-key", "X-Cell-User-Id": "user:signe"},
        json={
            "case_id": "haven_project",
            "source_repo": "CellScaffold",
            "source_commit": "working-tree",
            "source_type": "haven_service_catalog",
            "replace_source": True,
            "dry_run": False,
            "chunks": [
                {
                    "chunk_id": "cellscaffold.rag-gateway.overview",
                    "title": "RAGGatewayCell overview",
                    "content": "RAGGatewayCell supports query.run.",
                    "metadata": {
                        "repo": "CellScaffold",
                        "serviceID": "cellscaffold.rag-gateway",
                        "cell": "RAGGatewayCell",
                        "contract": "query.run",
                        "status": "supported now",
                    },
                }
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True, "published": 1}
    assert seen["actor"] == "user:signe"
    assert seen["payload"]["source_type"] == "haven_service_catalog"
    assert seen["payload"]["chunks"][0]["metadata"]["contract"] == "query.run"


def test_catalog_status_delegates_query(monkeypatch):
    seen = {}

    def fake_status(*, case_id, source_repo, source_type):
        seen.update(
            {"case_id": case_id, "source_repo": source_repo, "source_type": source_type}
        )
        return {"ok": True, "active_docs": 12}

    monkeypatch.setattr(routes_admin, "catalog_status", fake_status)
    client = _client(monkeypatch)

    response = client.get(
        "/v1/admin/catalog/status",
        headers={"X-API-Key": "test-admin-key"},
        params={
            "case_id": "haven_project",
            "source_repo": "CellScaffold",
            "source_type": "haven_service_catalog",
        },
    )

    assert response.status_code == 200
    assert response.json()["active_docs"] == 12
    assert seen == {
        "case_id": "haven_project",
        "source_repo": "CellScaffold",
        "source_type": "haven_service_catalog",
    }


def test_media_publish_accepts_inline_base64_payload(monkeypatch):
    seen = {}

    def fake_publish(payload, *, actor=None):
        seen["payload"] = payload
        seen["actor"] = actor
        return {"ok": True, "media_id": payload["media"]["media_id"]}

    monkeypatch.setattr(routes_admin, "publish_media", fake_publish)
    client = _client(monkeypatch)

    response = client.post(
        "/v1/admin/media/publish",
        headers={"X-API-Key": "test-admin-key", "X-Cell-User-Id": "user:signe"},
        json={
            "case_id": "haven_project",
            "source_type": "haven_media",
            "media": {
                "media_id": "sha256:2cf24d",
                "filename": "spec.md",
                "mime_type": "text/markdown",
                "size_bytes": 5,
                "sha256": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
                "delivery": {
                    "mode": "inlineBase64",
                    "bytes_base64": "aGVsbG8=",
                },
            },
            "metadata": {
                "source_repo": "CellScaffold",
                "subject_kind": "project.doc",
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["media_id"] == "sha256:2cf24d"
    assert seen["actor"] == "user:signe"
    assert seen["payload"]["media"]["delivery"]["mode"] == "inlineBase64"
