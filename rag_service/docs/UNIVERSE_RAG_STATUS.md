# UniverseSimulation RAG Status

Last source review: 2026-07-14.

## Source-of-truth order

For current project claims, use this order:

1. `PROJECT_CONTEXT_LIVE.md`
2. `PROJECT_HISTORY_INDEX.md`
3. the newest matching `Documentation/v*.md` and machine-readable CSVs
4. older reports and prompts

The formal report and early `trajectory.csv` remain historical inputs. They do
not outrank later executed gates.

## Current research state

- Operational growth regime: `band_zero_del` from v11e.
- Lorentz-like behavior: `not_yet`; mode, placement, and anisotropy alternatives
  remain unresolved.
- Defect interactions are nontrivial, but heuristic collision classes are not
  particles and active-set landscapes are growth-seed dependent.
- v16h validated that the clock/depth relation is explained by the scheduler's
  directly logged pre-event total-rate profile. It is not independent geometry
  evidence.
- v16i found a repeatable open causal-interval abundance contrast beyond a null
  preserving scheduler order, causal depth, and direct indegree.
- v16j retained that contrast under a stricter null preserving exact direct
  in/out-degree, exact causal depth, and the global dyadic parent-age histogram.
  All 12 holdout runs had effect ratio above 1 and `p=1/33`.
- The frozen v16j composite gate still failed because the v16h/v16d effect-size
  ratio was `0.469661`, below its preregistered lower bound `0.5`.

The correct concise reading is
`strict_null_contrast_supported_magnitude_transfer_not_stable`. See
`Documentation/v16j_interpretation_audit.md`. This is finite-event-poset
structure, not a validated dimension, manifold, Lorentz symmetry, physical
time, continuum, particle, entanglement, or spacetime result.

## Current next gate

Run one fresh-history replication of the frozen interval observable and strict
null. Preregister effect existence and effect-size stability as separate
outcomes. Do not increase target or fit a dimension before that replication.

## RAG corpus layout

- `universe_status`: live context, history, RAG status, and corpus policy
- `universe_experiments`: recent executed gate reports and interpretation audits
- `universe_tools`: simulator, gate, site, and RAG operating instructions
- `universe_argumentation`: formal report and evidence/claim map
- `universe_prompts`: model personas and answer templates

The `universe_project` case searches all five source types. Narrow cases retain
their scoped purpose.

## Public-site and dynamic-RAG boundary

`https://emergentuniverse.haven.digipomps.org` is a static, checksum-manifested
scientific archive. It publishes selected RAG corpus documents and executed
artifacts, but it does not route the dynamic RAG API.

The dynamic `/v1/research/*` API remains a separately operated, token-scoped
service. Public exposure requires bearer-token policy, Postgres-backed shared
rate limiting, signed citation downloads, citation audit, freshness audit, and
no public admin/ingestion routes. Static-site freshness does not prove dynamic
RAG freshness; both must be checked separately.

## Required answer discipline

Every answer must distinguish:

- algebraic or formal facts
- implemented generator/instrumentation behavior
- generated artifacts and scoring products
- actual executed dynamical or analysis results
- inference and proposed next work

If a source is stale or conflicts with a newer file, state the conflict and use
the newer file. Never fabricate missing runtime results.
