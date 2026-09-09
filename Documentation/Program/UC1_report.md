# UC1 — back to persistent, local units of change

Date: 2026-09-09. Stage: **instrumentation only**.
Publication: **publication_blocked** (deployment authentication; RAG unverified).
Candidate universe-model runs: **0**. This is not a hypothesis test.

## Decision

Keep the original relational-emergence question, but do not launch another
dimension/symmetry search with an unqualified implementation of its premises.
This round supplies three executable counterexamples to ontology conformance
in the root baseline and a calibrated, history-based circulation instrument.
Neither result establishes spontaneous metastability. Neither rejects the
user's hypothesis.

The next scientific dependency is the representation of persistent units of
change. A clarification was requested before candidate-model execution:
are these intrinsic motifs of the untyped graph, or primitive units with a
position on it? No answer was available at measurement time. These are
different state spaces; implementing one silently would change the question.

## Original purpose, as clarified by the user

The universe has no external substrate: nodes are hubs for relations, not
carriers of physical values, and neither nodes nor edges have coordinates or
hidden physical attributes. Influence is relational change propagating through
node hops. Units of change persist; spontaneous internal births may increase
their number. New nodes can arise from local change, potentially with a
degree-dependent probability. Components without a causal path cannot be
reconnected by an external/global fallback. Time is counted from changes.

The first eligible signal is weak, spontaneously formed metastable circulation:
activity revisits relational loops or clusters and may pass between clusters.
Lorentz-like behavior, dimension and stronger physical interpretations are
later questions, not a prerequisite for detecting such a signal.

Implementation labels and an observer's history are permissible bookkeeping
only if relabeling does not change the dynamics or measured conclusions.
Bookkeeping is not permission to add hidden physical state. In particular, an
explicit token position is a modeling choice, not automatically equivalent to
an untyped adjacency-only state.

## Frozen protocol and executed evidence

`UC1_preregistration.json` was written before the measurement run. Its SHA-256:

`b0ba3861ee1df93aa102d2b0857945988a0e951caa11239e23cbc06f3bfa128a`

The executable is `Tools/units_of_change_conformance.py`. It does **not** modify
the root simulator or implement a candidate model. Full source hashes,
counterexample outputs and reference gates are in `UC1_measurements.json`.
Raw histories are in `UC1_reference_paths.csv`; paired summaries are in
`UC1_reference_summary.csv`. No threshold was tuned after these measurements.

### 1. Root baseline conformance: three counterexamples

All probes use seed 20260909, zero explicit token birth/death and seed rates,
certain traversed-edge deletion, and zero triadic closure/local rewiring.

| Specified input | Observed result | Contradicted premise |
| --- | --- | --- |
| One unit at node 0 on edge 0–1; default pruning | Both nodes pruned; units `[0]` → `[]` | Existing units never disappear |
| One unit at 0 on disconnected edges 0–1 and 2–3; relocation enabled | Nodes 0 and 1 pruned; units `[0]` → `[2]` | No cross-component influence without a causal path |
| Isolated host 0 plus separate edge 2–3; isolated-host fallback | Edge 0–2 created | A relation changes only through local node-hop causality |

These are actual executions of `relational_universe_sim.py`, not inferred
failure rates. The relevant branches are pruning/token cleanup in
`gillespie_step` and the isolated-host fallback in `token_event`. They establish
that this baseline cannot, over these permitted boundary states and settings,
serve as an unqualified implementation of the clarified premises. They do not
show that every historical v-series run exercised these branches. They do not
audit every rule (birth, scheduling and time interpretation remain to be
qualified separately). No claim is made about typical frequency.
The isolated-host probe calls `token_event` directly: ordinary
`gillespie_step` prunes isolated nodes after each event. It therefore does not
establish that this boundary state is reached from the default connected
initialization under the ordinary scheduler.

### 2. Circulation instrument: measured positive and null references

Endpoint: fraction of hops covered by at least three consecutive laps of a
simple cycle of length 3–6, in the direction established by its first lap.
Overlapping detections are counted by union of covered hop positions.

The positive histories are deliberately oriented laps; the null histories are
unbiased neighbor walks on **the same cycle**, with the same 2,048-hop budget.
There are eight null seeds on C3 and eight on C4: 16 paired comparisons,
32 histories and 65,568 recorded positions. The positive history within each
graph size is a repeated deterministic control, not an independent discovery.

| Quantity | Measured value |
| --- | --- |
| Positive median coverage | 1.0 |
| Null median coverage (pooled C3/C4) | 0.007568359375 |
| Positive / negative / tied paired signs | 16 / 0 / 0 |
| Frozen one-sided sign score | 0.0000152587890625 |
| Signs preserved after squaring coverage | 16 / 16 |
| Frozen reference-separation gate | PASS |

The sign score is the prespecified binomial tail for these calibration pairs,
not a probability for the universe hypothesis or a generalization across
network families. Squaring is an instrument sanity check, not evidence for a
physical invariant. Null coverage is not universally zero: chance circulation
already occurs on these tiny graphs. C3 and C4 calibrate only two graph sizes;
the length-5/6 detection range is not thereby dynamically calibrated.

## What has and has not become more promising

The useful direction is to test **persistent local dynamics first, then
history-based circulation under continuing change**. This is closer to the
stated hypothesis than treating a fitted dimension as the first success gate.
UC1 has made that direction more executable, not more physically probable.

A return walk on a frozen graph is not evidence that graph structure survives
rewriting. A future metastability endpoint must register formation without
hindsight, record actual edits as well as update opportunities, and distinguish
an actively maintained structure from an unvisited or frozen one. Its own
measured positive and null references are required; UC1 circulation calibration
does not qualify such an endpoint automatically.
The present detector is deliberately narrow: it will miss noisy circulation
that does not repeat an exact three-lap word. On dynamic graphs, recorded hops
must be checked against contemporaneous edges; a repeated node word alone does
not prove that all edges of the cycle existed simultaneously.

The null must preserve the opportunities relevant to the proposed effect:
locality, component structure, exposure and the selection procedure. A global
random rewiring may be useful as an explicitly nonphysical diagnostic but is
not automatically a lawful alternative universe. Comparing against a null
that changes connectivity can measure that confound instead of the target.

Encoding a unit as a pendant leaf is **not adopted**: moving that leaf can
create/remove other degree-one markers, and guards that preserve its identity
can freeze its host. Such freezing could manufacture apparent metastability.
This is a design objection, not a simulated result. The representation choice
must be settled before a candidate's rules and references are frozen.

## Verification and next gate

The six focused analytic tests passed before the measurement run. They check
the three-lap threshold, rejection of backtracking/acyclic histories,
overlap counting, node renaming, full-history reversal and exact sign arithmetic.
Every reference hop was checked against its declared cycle during generation.
Independent review and byte-exact replay are recorded in `UC1_verification.md`.
No verification scan of all `Documentation/` was run.

Next: resolve the unit representation; specify a small local transition system
with persistent units and no disconnected-component fallback; qualify those
invariants and a dynamic positive/null pair before spending on spontaneous
pattern searches. Do not count this round as evidence for emergent particles,
physical invariants, Lorentz symmetry, dimension, spacetime or an impossibility
theorem. No candidate model has been run in UC1.

## Publication boundary

The deployment host resolved to 89.167.90.101. A batch, strict-host-key,
read-only SSH preflight using the documented root access path failed with
`Permission denied (publickey,password)`, exit 255. No remote change was made.
Static deployment/live revision and the separate dedicated RAG sync and
token-scoped authentication, PostgreSQL rate-limit, citation and freshness
checks are therefore **not passed**. No credentials were printed or changed.

The repository evidence and a revision-locked local archive can still be
preserved. They do not imply publication. Exact local verification, repository
state and remaining dependencies are recorded in `UC1_verification.md` and
reported to the user; deployment may resume only after access is restored.
