# v16x interpretation audit

Date: 2026-07-16

Frozen overall status:
`v16x_integer_measure_endpoint_diversity_not_qualified`.

This audit does not replace or repair the preregistered v16x gate. It combines
the frozen gate products with two effect-blind post-run audits so the next
experiment targets the actual remaining uncertainty.

## What v16x resolved

- All `192/192` declared endpoints passed structural, slot-signature, and
  globally-forced-edge integrity checks.
- The implementation made `0` local-switch, `0` source-spectrum, and `0`
  observed-effect calls.
- Exact replay, candidate insertion-order covariance, and semantic role
  relabel covariance passed together on `24/24` checks.
- Independent seed-family center stability passed `36/36` feature checks.
- Every source produced `16/16` distinct primary endpoints.
- Primary median pairwise changed-edge fraction ranged from `0.395117` to
  `0.451079`.
- Variable-edge union coverage ranged from `0.344466` to `0.423147`.
- Effective variable-edge support ratio ranged from `0.253525` to `0.319294`.

This is a real method improvement over v16w: integer min-cost flow with
canonical candidate ordering removed the observed dependence on the solver's
candidate-column representation. It does not qualify the resulting
probability measure by itself.

## Exact forced-edge result

The residual-SCC audit passed all `45` explicit alternating-cycle witnesses.
Under the coarse v16v state space, globally forced source-edge fraction ranged
from `0.361305` to `0.417180`; the exact upper bound on possible source change
ranged from `0.582820` to `0.638695`, above the already frozen v16v `0.10`
nontriviality floor for all six sources.

Requiring every candidate edge to retain an actual concrete resource conflict
collapsed the state space. Globally forced source-edge fraction became
`0.994607–0.999173`, and the maximum possible changed-edge fraction became
only `0.000827–0.005827`. All six exact-conflict spaces therefore fail the old
`0.10` floor algebraically. This is not a sampler or budget failure.

The correct surviving state space is consequently the coarse slot space with
concrete-conflict fraction measured and stratified, not exact concrete-conflict
preservation. This does not mean concrete conflict is irrelevant; it means the
present source histories do not provide enough alternative concrete conflicts
for a nontrivial exact-preservation null.

## Why the frozen gate still failed

Four of six sources failed only the frozen
`maximum_variable_edge_inclusion_rate <= 0.95` criterion. All other finite
diversity criteria passed on every source. One additional half-batch feature
failed: `mean_candidate_rank_fraction` at source `9299/123403` shifted by
`0.004639`, but the shift occupied `0.504021` of that small observed range.
The independent 16-vs-16 seed-family comparison passed all `36/36` features.

The post-run audit replayed all `192/192` endpoint digests exactly and combined
the two declared seed families. The maximum globally variable edge-inclusion
rate passed the old `0.95` ceiling on only `2/6` sources:

| growth_seed | run_offset | combined maximum | count |
| --- | --- | --- | --- |
| 9299 | 123078 | 0.937500 | 30/32 |
| 9299 | 123403 | 0.968750 | 31/32 |
| 9299 | 127341 | 1.000000 | 32/32 |
| 9365 | 123078 | 0.906250 | 29/32 |
| 9365 | 123403 | 1.000000 | 32/32 |
| 9365 | 127341 | 0.968750 | 31/32 |

This rules out treating the four primary 16-endpoint failures as merely a
single-seed extreme value. The frozen diversity failure stands.

## Structural interpretation of the concentrated edges

Every highest-inclusion edge is an original source edge with an actual concrete
resource conflict. All are nevertheless globally variable and have explicit
valid alternating-cycle witnesses that remove them.

Five top edges lie in large residual SCCs with `2,529–3,099` nodes and
`19,690–29,255` internal candidate edges. The sixth lies in an SCC with `146`
nodes and `857` candidates. The shortest alternating return paths require
`2–10` changed source edges. The concentration is therefore not explained by a
mistaken forced-edge label or universally tiny SCCs.

The remaining possibilities include:

- strong structural asymmetry in the number or cost geometry of matchings that
  exclude these edges;
- concentration induced specifically by choosing the minimum of independent
  edge costs;
- a diversity criterion that is too sensitive to one legitimate high-marginal
  edge now that globally forced edges are classified exactly.

The current data do not distinguish these explanations. In particular, a
large SCC proves existence of alternating cycles, not uniform or high-probability
access to every edge state under the declared measure.

## Decision

Do not compute the v16s spectrum contrast under v16x and do not merely add more
draws to the same random-cost law. The 32-draw post-run audit already shows
persistent high marginals on four sources.

The next effect-blind gate should compare probability laws on the same exact
coarse state space:

1. retain v16x integer random-cost sampling as a reference measure;
2. define a symmetric lazy alternating-cycle or heat-bath chain with an
   explicitly stated stationary target, preferably uniform/maximum-entropy on
   the reachable matching component if this can be implemented honestly;
3. test connectivity/reachability, replay, seed-family stability, marginal
   entropy, component coverage, pairwise distance, and effective support;
4. replace the single maximum-inclusion veto only in a new preregistration,
   with a concentration profile that separates exact forced mass from empirical
   marginal entropy;
5. keep concrete-conflict fraction as a declared diagnostic or stratum;
6. open an effect statistic only after one probability law passes on fresh
   histories.

This next gate must not assume that a swap chain mixes merely because it is
symmetric. Connectivity and finite mixing diagnostics remain empirical and
limited.

V16x establishes no uniform sampling, maximum entropy, canonical null,
spectrum effect, energy, temperature, invariant, dimension, manifold, Lorentz
symmetry, spacetime, particle, entanglement, continuum, or physical law.

## Evidence

- `v16x_state_space_forced_edge_audit.csv`
- `v16x_sampler_endpoint_audit.csv`
- `v16x_representation_audit.csv`
- `v16x_source_qualification_summary.csv`
- `v16x_postrun_combined_seed_concentration.csv`
- `v16x_postrun_top_edge_component_audit.csv`
- `v16x_postrun_concentration_audit.md`

## Algorithm references

- Mulmuley, Vazirani, and Vazirani, *Matching is as Easy as Matrix Inversion*
  (1987): https://doi.org/10.1145/28395.383347
- NetworkX integer `network_simplex` documentation:
  https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.network_simplex.html
