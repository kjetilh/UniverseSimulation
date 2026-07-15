# UniverseSimulation Corpus Plan

Last source review: 2026-07-15.

## Source types

### `universe_status`

Current state and source-priority documents:

- `PROJECT_CONTEXT_LIVE.md`
- `PROJECT_HISTORY_INDEX.md`
- `rag_service/docs/UNIVERSE_RAG_STATUS.md`
- `rag_service/docs/UNIVERSE_CORPUS_PLAN.md`

### `universe_experiments`

Recent executed evidence, not general theory:

- v16h direct total-rate mechanism validation
- v16i/v16j causal-interval abundance and strict-null interpretation
- v16m fresh strict-null replication
- v16q sampler qualification and v16r/v16s footprint-null evidence
- v16t frozen null-center gate, realized-effort interpretation audit, and corrected next direction
- operational recommendations and selected gate CSVs

Do not ingest the large per-null distributions into the default RAG corpus.
They remain downloadable evidence on the public site.

### `universe_tools`

- `rag_service/docs/UNIVERSE_TOOL_RUNBOOK.md`
- `rag_service/docs/RAG_SERVICE_API.md`
- `Documentation/EmergentUniverse_Public_Site_Runbook.md`

### `universe_argumentation`

- `Documentation/grundig-research-rapport-16.md`
- `rag_service/docs/UNIVERSE_ARGUMENTATION_MAP.md`

### `universe_prompts`

- `rag_service/prompts/**/*.md`
- `rag_service/docs/UNIVERSE_DEEP_RESEARCH_PROMPT.md`

## Cases

- `universe_project`: all source types
- `universe_tools`: status + tools + recent experiments
- `universe_argumentation`: argumentation + status + recent experiments
- `universe_prompts`: prompts + status + argumentation + tools

## Sync policy

Use `scripts.sync_orchestrator` with the tracked TOML template on the deployed
checkout. It stages a deterministic live tree, tombstones removed documents,
and calls the admin sync/rebuild surface. Verify the plan before applying.

From `rag_service/`:

```bash
python -m scripts.sync_orchestrator \
  --config config/sync_orchestrator.example.toml \
  --plan-only
```

Then run without `--plan-only` only against the intended deployment. After
sync, run a token-scoped research query for `v16t` and require citations to the
path-stability report or next-direction assessment plus freshness metadata.

## Quality rules

- Newer repo files outrank older summaries.
- Current status docs must carry a source-review date.
- Keep effect existence separate from effect-size stability.
- Keep formal facts, instrumentation, generated artifacts, executed results,
  and inference separate.
- Do not index secrets, `.env`, admin keys, private uploads, `.git`, `.venv`,
  build products, or raw caches.
- Never claim dynamic RAG freshness from a static-site deployment alone.
