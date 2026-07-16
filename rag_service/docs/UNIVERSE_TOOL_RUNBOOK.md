# UniverseSimulation Tool Runbook

Last source review: 2026-07-16.

Every completed research round follows the mandatory closure contract in
`Documentation/Research_Round_Closure_Policy.md`: verify, commit, push, deploy
the revision-locked static bundle, sync RAG separately, and prove both surfaces
live. Any missing gate is `publication_blocked`, not an implicit success.

## Choose the right entrypoint

- Current status: `PROJECT_CONTEXT_LIVE.md`
- Experiment history: `PROJECT_HISTORY_INDEX.md`
- Early toy baseline: `relational_universe_sim.py`
- Latest effect-blind global-measure gate: `relational_universe_v16x_explicit_global_measure_gate.py`
- Frozen post-run concentration audit: `relational_universe_v16x_postrun_concentration_audit.py`
- Top-edge alternating-cycle audit: `relational_universe_v16x_top_edge_component_audit.py`
- Public archive builder: `Tools/build_emergentuniverse_public_site.py`
- RAG service: `rag_service/`

The early `trajectory.csv` is historical baseline data. It is not the current
research frontier.

## Verify the latest completed gates

From the repository root, using the environment that provides `networkx`:

```bash
/opt/anaconda3/bin/python relational_universe_v16i_causal_interval_abundance_gate.py --verify-only
/opt/anaconda3/bin/python relational_universe_v16j_interval_strict_null_gate.py --verify-only
/opt/anaconda3/bin/python relational_universe_v16q_event_footprint_null_calibration.py --verify-only
/opt/anaconda3/bin/python relational_universe_v16s_fresh_event_footprint_holdout.py --verify-only
/opt/anaconda3/bin/python relational_universe_v16t_footprint_null_path_stability_gate.py --verify-only
/opt/anaconda3/bin/python relational_universe_v16u_matched_effort_footprint_stability_gate.py --verify-only
/opt/anaconda3/bin/python relational_universe_v16v_global_edge_slot_feasibility_gate.py --verify-only
/opt/anaconda3/bin/python relational_universe_v16w_global_null_qualification_gate.py --verify-only
/opt/anaconda3/bin/python relational_universe_v16x_explicit_global_measure_gate.py --verify-only
```

The v16q command verifies effect-blind footprint-sampler qualification. The
v16s command verifies the fresh histories, null integrity and spectrum gates.
The v16t command verifies the frozen effect-blind center-comparison products
and source-spectrum exclusion. Read
`Documentation/v16t_realized_effort_interpretation_audit.md` before assigning
chain-length or path meaning, then
`Documentation/v16t_next_direction_assessment.md`. The v16u command verifies
the exact-effort repair, shared prefix, matched direct/staged work and current
center gates. The v16v command verifies the independent global reconstruction,
48 endpoint audits, per-source diversity and effect exclusions. Read
`Documentation/v16v_next_direction_assessment.md` for that recommendation. The
v16w command verifies the frozen 288-endpoint qualification output and effect
exclusions. Read `Documentation/v16w_interpretation_audit.md` because the
frozen overall failure must be decomposed before choosing the next gate.
The v16x command verifies the frozen 192-endpoint integer-measure output,
preregistration/source hashes and effect exclusions. Read both
`Documentation/v16x_interpretation_audit.md` and
`Documentation/v16x_postrun_concentration_audit.md`; the latter replays all
declared endpoint digests while combining seed families without changing the
frozen gate.

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

Require the manifest to contain the v16s effect report, v16t interpretation
audit, v16u matched-effort products, v16v feasibility products, the v16w
qualification failure, and the v16x report, interpretation audit, forced-edge
audit, representation audit, source summary, gate evaluation, claim ledger,
post-run concentration products, next-direction assessment, and live project
context. Check SHA-256 hashes.

After deployment:

```bash
curl -fsS https://emergentuniverse.haven.digipomps.org/ | grep -E "v16x|192/192|24/24|2/6|32/32|Interpretation boundary"
curl -fsS https://emergentuniverse.haven.digipomps.org/data/manifest.json
curl -fsS https://emergentuniverse.haven.digipomps.org/data/latest_causal_structure/v16x_interpretation_audit.md
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
  --query 'Hvorfor feilet v16x selv om representasjonskontrollene besto, hva viste forced-edge-auditen, og hva er neste gate?'
```

The answer must include citation/freshness audit metadata and cite current
v16x material plus v16s when the underlying effect is discussed. `--skip-query` is not sufficient for freshness
verification.

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
- Do not treat the v16s footprint-null replication as sampler uniformity,
  concrete-resource independence, dimension, manifold, Lorentz symmetry,
  spacetime, particles, entanglement, or continuum evidence.
- Do not treat the frozen v16t path/chain-length pass as validated separation:
  the realized-effort audit found near-equal direct lengths and unmatched staged
  effort. It also proves no irreducibility, mixing, convergence, stationarity,
  representativeness, or uniformity.
- Do not treat the v16u exact matched-effort pass as mixing, uniformity,
  independence from other null constructions, or a replication of the v16s
  observed effect.
- Do not treat v16v feasibility/diversity as a qualified, uniform or
  representative global null, or as evidence that v16s survives it.
- Do not use v16w endpoint uniqueness or batch-center stability to rehabilitate
  the current global procedure. Replay/column covariance and objective
  sensitivity failed, and no source effect was computed.
- Do not use v16x representation covariance, endpoint uniqueness, or
  alternating-cycle witnesses as proof of a uniform, maximum-entropy, mixed or
  representative global measure. The frozen diversity gate passed only `2/6`,
  the combined 32-endpoint concentration audit failed `4/6`, and no source
  effect was computed.
- Do not call token count, action density or edit work physical energy or
  temperature before a local balance law and intensive fluctuation observable
  pass fresh tests. Uniformly scaling all rates is only clock rescaling.
