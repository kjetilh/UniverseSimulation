from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent


def test_docker_compose_threads_research_hardening_env_to_api_container():
    compose = yaml.safe_load((ROOT / "docker" / "docker-compose.yml").read_text(encoding="utf-8"))
    env = compose["services"]["api"]["environment"]

    for key in (
        "RESEARCH_API_TOKENS_JSON",
        "RESEARCH_DOWNLOAD_SIGNING_KEY",
        "RESEARCH_ALLOW_QUERY_ACCESS_TOKEN",
        "RESEARCH_RATE_LIMIT_BACKEND",
        "RESEARCH_RATE_LIMIT_PER_MINUTE",
        "RESEARCH_RATE_LIMIT_BURST",
        "RESEARCH_MIN_CITATIONS",
        "RESEARCH_MIN_UNIQUE_DOCS",
        "RESEARCH_FRESHNESS_MAX_AGE_SECONDS",
        "RESEARCH_ENFORCE_RESPONSE_AUDIT",
        "RESEARCH_ENFORCE_FRESHNESS",
    ):
        assert key in env


def test_research_smoke_runbook_names_postgres_backend_and_smoke_script():
    api_doc = (ROOT / "docs" / "RAG_SERVICE_API.md").read_text(encoding="utf-8")
    public_runbook = (REPO_ROOT / "Documentation" / "EmergentUniverse_Public_Site_Runbook.md").read_text(
        encoding="utf-8"
    )

    assert "scripts.research_hardening_smoke" in api_doc
    assert "RESEARCH_RATE_LIMIT_BACKEND=postgres" in api_doc
    assert "scripts.research_hardening_smoke" in public_runbook
    assert "RESEARCH_EXPECTED_RATE_LIMIT_BACKEND=postgres" in public_runbook
