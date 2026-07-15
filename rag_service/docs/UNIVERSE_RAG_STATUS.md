# UniverseSimulation RAG Status

Last source review: 2026-07-15.

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
- v16m independently replicated the strict-null contrast on new histories with
  a qualified attempt ceiling.
- v16o showed that the proposed concrete-resource-conflict edge-color null was
  structurally immobile. v16p found broad static support for a weaker event-
  footprint null, and v16q qualified that procedure effect-blind at `60`
  attempts per edge with `288/288` perturbations passing.
- v16r retained the spectrum contrast under that footprint null on the reused
  v16m histories. v16s then replicated it on six new histories with the null
  selected before generation: median JS effect ratio `11.999282`, positive
  direction and empirical `p=1/33` in `6/6`, with longer median `12.054418`.
- All v16s tail-mass deltas were negative. The result is a full-spectrum
  contrast, not excess large intervals.
- v16t tested the footprint-null center effect-blind across direct swap
  multipliers `0.075/0.100/0.200` and staged `0.100+0.100`. All `384/384`
  perturbations passed. Direct chain-length stability passed `12/12` with
  maximum ratio `0.237211`; path-segmentation stability passed `6/6` with
  maximum ratio `1.463604` against the frozen limit `2.0`.
- The newer v16t realized-effort audit limits that frozen pass: direct
  short/reference/long averaged `993/1005/998` accepted swaps, while staged
  averaged `2023`. Direct length was not separated, and path segmentation was
  confounded with extra effort.
- v16u repaired that confound effect-blind. All `384/384` outputs and `96/96`
  exact-effort branches passed; direct `+2K` and staged `+K+K` differed by zero
  accepted swaps after the same prefix in every branch. Realized-length center
  stability passed `18/18` with maximum ratio `0.666516`; matched-path stability
  passed `6/6` with maximum ratio `0.180595` against the frozen limit `2.0`.
- v16v then constructed an independent global edge-slot null without local
  switch steps or effect inspection. All `48/48` complete reconstructions
  passed exact integrity. Every source produced `8/8` distinct endpoints; the
  minimum changed-edge fraction per source ranged from `0.574426` to
  `0.630611`.

The correct concise current reading is
`fresh_event_footprint_spectrum_contrast_with_independent_global_null_construction_feasible_but_not_yet_qualified`. See
`Documentation/v16s_fresh_event_footprint_holdout.md` and
`Documentation/v16v_global_edge_slot_feasibility_gate.md`. This remains finite
event-DAG structure: the global family is constructible and diverse, but has
not been qualified as a representative probability distribution and has not
been used for an effect test. It is not a validated energy, temperature,
dimension, manifold, Lorentz symmetry, physical time, continuum, particle,
entanglement, or spacetime result.

## Current next gate

Run v16w as an effect-blind qualification of the frozen global edge-slot null.
Increase endpoint count and test replay, relabel invariance, endpoint diversity,
and within-family center stability while still excluding every source spectrum
and observed-effect metric. Only after qualification may one preregister a
single independent-null effect test.

The separate units-of-action hypothesis is an open proposal, not a result. The
repo supports a future test of local edit work, action-carrier density and
boundary flux as possible microscopic inputs to emergent energy. Uniform
scaling of all Gillespie rates changes clock speed rather than the embedded
event sequence and is not a valid cooling intervention.

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
