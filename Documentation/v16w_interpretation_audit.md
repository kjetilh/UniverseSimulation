# v16w interpretation audit

Date: 2026-07-15

Frozen overall status:
`v16w_global_null_qualification_instrumentation_failed`.

This audit does not replace or repair the preregistered gate. It decomposes the
failure so the next experiment does not discard valid negative information.

## What passed

- All `288/288` primary and objective-sensitivity endpoints passed the frozen
  structural and edge-slot integrity checks.
- The implementation made `0` local-switch, `0` source-spectrum, and `0`
  observed-effect calls.
- Semantic event-family/resource relabel covariance passed `24/24`.
- Every source produced `32/32` distinct primary endpoints.
- Median pairwise changed-edge fraction ranged from `0.236959` to `0.320437`.
- Effective edge-support ratio ranged from `0.120935` to `0.140574`, above the
  frozen `0.10` floor for all six sources.
- First-half versus second-half center stability passed `36/36` null-only
  feature comparisons.

These facts establish finite structural feasibility and some finite ensemble
diversity. They do not qualify a probability distribution.

## Representation failure

Exact replay passed `23/24`, while candidate-column permutation covariance
passed only `8/24`. All reruns remained structurally valid. The solver is thus
selecting among numerically or combinatorially near-degenerate optima in a way
that is not reliably independent of LP representation. This is a procedure
failure, not a physical asymmetry.

The semantic role-relabel pass does not cancel this result. It shows that
renaming event families and resource namespaces preserves the modeled feasible
set; it does not show that the LP chooses a representation-independent sample
from that set.

## Diversity-gate nuance

The composite diversity gate failed even though uniqueness, pairwise distance,
source change, and effective-support floors mostly passed. One source narrowly
missed candidate-union coverage (`0.199607` versus `0.20`). More importantly,
the maximum inclusion rate among edges classified as locally non-forced was
`1.000` for every source, above the `0.95` ceiling.

The current non-forced classifier uses local child-slot surplus. An edge can
have local alternatives yet still be forced by the complete parent-capacity
matching problem. Therefore this row cannot yet distinguish true sampler
concentration from globally forced edges. The frozen failure stands, but the
next instrumentation must compute global edge necessity rather than relabel
this result as ensemble collapse.

## Objective dependence

Only `15/36` objective-sensitivity comparisons passed. The failures are
systematic across all six sources:

- source-edge fraction: primary median `0.369389–0.425574`, random-priority
  median `0.547672–0.605300`;
- concrete-conflict fraction: primary median `0.370086–0.426973`,
  random-priority median `0.548230–0.608213`;
- mean pairwise changed fraction: primary median `0.236775–0.320464`,
  random-priority median `0.393757–0.451343`.

Exact parent-lag and depth-gap centers did not move because those properties
are strongly constrained. Source retention and actual concrete resource
conflicts did move. The current global edge-slot constraints preserve coarse
event roles but permit edges without a concrete dependency conflict. The solver
objective therefore controls both how far the endpoint moves and how much of
the original concrete causal support remains.

This objective result is descriptive because the overall gate already failed
at the representation layer. Its six-source consistency nevertheless makes it
a required design constraint for the next effect-blind gate.

## Decision

Do not evaluate the v16s spectrum contrast under the current global family.
The next gate should:

1. replace floating LP endpoint selection with an exact, auditable
   representation-independent integer-cost or combinatorial procedure;
2. compute whether each apparently concentrated edge is globally forced;
3. define an explicit stochastic measure over feasible global matchings rather
   than treating optimization endpoints as samples;
4. decide effect-blind whether concrete resource conflict must be preserved or
   explicitly stratified;
5. repeat replay, representation, diversity, and objective checks before any
   source spectrum is computed.

The units-of-change/action-density hypothesis remains a separate promising
mechanism track. V16w supplies no energy, temperature, geometry, Lorentz,
particle, entanglement, or spacetime evidence.
