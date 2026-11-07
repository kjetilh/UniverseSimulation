from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import routes_admin
from app.settings import settings


def test_admin_revalidation_rejects_unauthorized_dry_run_and_traversal(monkeypatch, tmp_path):
    monkeypatch.setattr(settings, "admin_api_key", "test-key")
    monkeypatch.setattr(settings, "ingest_root", str(tmp_path))
    calls = []

    def verify(files, revision):
        calls.append((files, revision))
        return {"verified_docs": 1, "verified_files": 1, "source_revision": revision}

    monkeypatch.setattr(routes_admin, "revalidate_sources", verify)
    app = FastAPI()
    app.include_router(routes_admin.router)
    client = TestClient(app)
    route = "/v1/admin/revalidate"
    item = {"source_type": "experiments", "path": "live/one.md",
            "source_path": "docs/one.md", "raw_sha256": "1"*64}
    payload = {"files": [item], "source_revision": "2"*40}
    headers = {"X-API-Key": "test-key"}
    assert client.post(route, json=payload).status_code == 401
    assert client.post(route, headers=headers, json={**payload, "dry_run": True}).status_code == 422
    unsafe = {**payload, "files": [{**item, "path": "../one.md"}]}
    assert client.post(route, headers=headers, json=unsafe).status_code == 400
    assert not calls
    assert client.post(route, headers=headers, json=payload).status_code == 200
    assert calls == [([{**item, "path": str(tmp_path / "live/one.md")}], "2"*40)]
