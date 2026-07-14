# UniverseSimulation Tool Runbook

Last source review: 2026-07-14.

## Choose the right entrypoint

- Current status: `PROJECT_CONTEXT_LIVE.md`
- Experiment history: `PROJECT_HISTORY_INDEX.md`
- Early toy baseline: `relational_universe_sim.py`
- Latest strict-null gate: `relational_universe_v16j_interval_strict_null_gate.py`
- Public archive builder: `Tools/build_emergentuniverse_public_site.py`
- RAG service: `rag_service/`

The early `trajectory.csv` is historical baseline data. It is not the current
research frontier.

## Verify the latest completed gates

From the repository root, using the environment that provides `networkx`:

```bash
/opt/anaconda3/bin/python relational_universe_v16i_causal_interval_abundance_gate.py --verify-only
/opt/anaconda3/bin/python relational_universe_v16j_interval_strict_null_gate.py --verify-only
```

The v16j command verifies the frozen binary gate products. Read
`Documentation/v16j_interpretation_audit.md` as the required semantic
decomposition of effect existence versus effect-size transfer.

## Run the early toy simulator

```bash
python3 relational_universe_sim.py --steps 2000 --log-every 500 --out ''
```

Use this only for the early model path. Do not infer v16 event-DAG or strict-null
behavior from it.

## Build and verify the public archive

```bash
PYTHONPYCACHEPREFIX=/private/tmp/pycache-emergent \
  python3 Tools/build_emergentuniverse_public_site.py \
  --out /tmp/emergentuniverse_public
```

Require the manifest to contain the current v16j report, interpretation audit,
gate evaluation, and live project context. Check their SHA-256 hashes against
the repository before deployment.

After deployment:

```bash
curl -fsS https://emergentuniverse.haven.digipomps.org/ | grep -E "v16j|magnitude transfer|Interpretation boundary"
curl -fsS https://emergentuniverse.haven.digipomps.org/data/manifest.json
curl -fsS https://emergentuniverse.haven.digipomps.org/data/latest_causal_structure/v16j_interpretation_audit.md
```

## Start the RAG service locally

From `rag_service/`:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e '.[pdf,html,docx]'
cp .env.example .env
docker compose -f docker/docker-compose.yml up -d db
python -m scripts.apply_migrations
python -m scripts.rebuild_index
uvicorn app.main:app --reload --port 8000
```

Do not overwrite an existing `.env` containing deployment configuration.

## Sync the current corpus

Prefer the orchestrator over one-file manual sync:

```bash
python -m scripts.sync_orchestrator \
  --config config/sync_orchestrator.example.toml \
  --plan-only
```

Inspect additions, updates, deletes, source types, and target paths. Then run
the same command without `--plan-only` only in the intended deployment.

## Verify dynamic RAG freshness

Static site freshness and dynamic RAG freshness are separate checks. On the
loopback-only deployed RAG instance:

```bash
RESEARCH_API_TOKEN='<token>' \
RESEARCH_BASE_URL='http://127.0.0.1:8000' \
RESEARCH_EXPECTED_RATE_LIMIT_BACKEND=postgres \
python -m scripts.research_hardening_smoke \
  --case-id universe_project \
  --query 'Hva viste v16j, og hvilken del av den frosne gaten feilet?'
```

The answer must include citation/freshness audit metadata and cite current v16j
material. `--skip-query` is not sufficient for freshness verification.

## Production instance boundary

The dedicated server instance uses
`ops/emergentuniverse_rag_compose.yml`, binds to loopback port `8103`, and keeps
its real deployment environment outside Git. It must remain distinct from the
Innovasjon and DiMy databases and upload roots. Updating the public static site
does not update this index; both deployments require separate verification.

## Interpretation rules

- Do not fabricate a CSV or runtime result.
- Do not treat a generator/replay pass as physics.
- Do not treat the v16j frozen composite failure as disappearance of the local
  strict-null effect.
- Do not treat the local strict-null effect as dimension, manifold, Lorentz
  symmetry, spacetime, particles, entanglement, or continuum evidence.
