# v16v global edge-slot feasibility gate

Status: `v16v_independent_global_null_family_feasible_and_diverse`.

V16v is an effect-blind feasibility and diversity audit for a null construction independent of the local event-footprint switch chain. It computes no source interval spectrum and no observed/null effect statistic.

Specification digest: `c8b502bfc58f220a9813e6d8e58043831353bdb3fe9621a1f5efe051381f16fc`.

## Frozen construction

Each original parent contributes its exact out-degree as capacity. Each child contributes edge-slot demand classified by source event role, dyadic parent-age bin, and whether the parent is an exact causal-depth witness or a lower-depth parent. The child fixes the target event role. One variable exists per legal parent-child pair, so duplicate edges are impossible.

The complete assignment is solved globally as a bipartite b-matching linear program. Bipartite incidence makes the feasible polytope integral; every returned solution is nevertheless checked explicitly for integrality and equality residual. The objective first minimizes retained source edges, then uses an independently seeded random tie-break. No edge-swap trajectory is used.

All six sources receive `8` objectives. A source passes only with all reconstructions structurally valid, at least `4` distinct endpoints, unique fraction at least `0.75`, and changed-edge fraction at least `0.10`.

## Source summaries

| growth_seed | run_offset | edge_count | candidate_edge_count | minimum_slot_candidate_parent_count | successful_reconstructions | distinct_reconstruction_count | minimum_changed_edge_fraction | source_gate_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 3628 | 50740 | 1 | 8 | 8 | 0.623484 | 1 |
| 9299 | 123403 | 3574 | 47804 | 1 | 8 | 8 | 0.574426 | 1 |
| 9299 | 127341 | 3523 | 41390 | 1 | 8 | 8 | 0.604031 | 1 |
| 9365 | 123078 | 3567 | 49772 | 1 | 8 | 8 | 0.622091 | 1 |
| 9365 | 123403 | 3604 | 42350 | 1 | 8 | 8 | 0.577414 | 1 |
| 9365 | 127341 | 3587 | 53830 | 1 | 8 | 8 | 0.630611 | 1 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| frozen_source_and_slot_support | pass | sources=6/6;blocked=0 | sources=6/6;blocked=0 | continue |
| global_reconstruction_integrity | pass | 48/48 | 48/48 | continue |
| per_source_endpoint_diversity | pass | 9299:123078=u8,c0.623484;9299:123403=u8,c0.574426;9299:127341=u8,c0.604031;9365:123078=u8,c0.622091;9365:123403=u8,c0.577414;9365:127341=u8,c0.630611 | unique>=4;fraction>=0.75;change>=0.1 | diverse |
| independent_from_local_switch_path | pass | local_switch_calls=0 | 0 | independent_construction |
| observed_spectrum_and_effect_exclusion | pass | source_spectrum_calls=0;effect_metric_calls=0 | 0;0 | effect_blind |
| v16v_overall | v16v_independent_global_null_family_feasible_and_diverse | support=1;integrity=1;diversity=1;independence=1;exclusion=1 | 1;1;1;1;1 | v16v_independent_global_null_family_feasible_and_diverse |

## Evidential boundary

A pass establishes only that the six frozen finite source DAGs admit multiple exact global reconstructions under this stronger per-child slot constraint, and that the implementation is independent of the local switch path. It does not establish a probability measure, uniformity, representativeness, stationarity, or equivalence to the local-switch null.

V16v does not re-evaluate the v16s spectrum contrast. It establishes no energy, temperature, dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, invariant, or physical law.
