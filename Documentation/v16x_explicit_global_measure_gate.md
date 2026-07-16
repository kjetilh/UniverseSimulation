# v16x explicit global measure gate

Status: `v16x_integer_measure_endpoint_diversity_not_qualified`.

## Evidential status

This is an effect-blind deterministic state-space audit followed by a preregistered finite sampler qualification. The forced-edge counts were inspected during design and are not a fresh holdout. Sampler endpoints, representation checks, and seed-family checks were generated only after the specification and script hash were frozen.

No source spectrum or observed-effect statistic was computed.

## State-space audit

| growth_seed | run_offset | state_space_arm | candidate_edge_count | globally_forced_source_edge_fraction | flexible_non_source_edge_count | maximum_possible_changed_edge_fraction | nontrivial_change_possible_pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | coarse_v16v_slot_space | 50740 | 0.369625 | 27627 | 0.630375 | 1 |
| 9299 | 123078 | actual_concrete_conflict_only | 3899 | 0.999173 | 3 | 0.000827 | 0 |
| 9299 | 123403 | coarse_v16v_slot_space | 47804 | 0.417180 | 22697 | 0.582820 | 1 |
| 9299 | 123403 | actual_concrete_conflict_only | 4029 | 0.997482 | 10 | 0.002518 | 0 |
| 9299 | 127341 | coarse_v16v_slot_space | 41390 | 0.387170 | 20963 | 0.612830 | 1 |
| 9299 | 127341 | actual_concrete_conflict_only | 3785 | 0.994607 | 19 | 0.005393 | 0 |
| 9365 | 123078 | coarse_v16v_slot_space | 49772 | 0.371741 | 29056 | 0.628259 | 1 |
| 9365 | 123078 | actual_concrete_conflict_only | 3827 | 0.999159 | 3 | 0.000841 | 0 |
| 9365 | 123403 | coarse_v16v_slot_space | 42350 | 0.411487 | 20642 | 0.588513 | 1 |
| 9365 | 123403 | actual_concrete_conflict_only | 3873 | 0.994173 | 21 | 0.005827 | 0 |
| 9365 | 127341 | coarse_v16v_slot_space | 53830 | 0.361305 | 31303 | 0.638695 | 1 |
| 9365 | 127341 | actual_concrete_conflict_only | 3869 | 0.999164 | 3 | 0.000836 | 0 |

A source edge is globally forced exactly when it is not part of an alternating cycle in the source assignment residual graph. Strongly connected components classify this property; explicit alternating-cycle flips validate sampled flexible-source witnesses. The exact-conflict arm is judged against the already frozen v16v 10% nontrivial-change floor, not a new v16x-tuned threshold.

## Explicit measure

The surviving coarse state space receives independent seeded pseudo-random integer costs in `[1, 2^63-1]` on canonically ordered candidate edges. An integer-capacity `network_simplex` solve selects the minimum-cost feasible b-matching. No source-retention term is present. Under ideal independent uniform weights, the isolation-lemma collision bound is at most `candidate_count/(2^63-1)` per endpoint. The implementation is deterministic pseudorandom, so that nominal bound is not promoted to a physical or cryptographic guarantee.

This defines an explicit edge-exchangeable random-cost measure. It is not uniform over feasible matchings, maximum entropy, canonical, or proven representative.

## Source qualification

| growth_seed | run_offset | primary_unique_fraction | primary_median_pairwise_change | primary_variable_union_coverage | primary_effective_variable_support_ratio | representation_pass | batch_center_pass | seed_family_pass | source_qualification_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 1.000000 | 0.444322 | 0.378786 | 0.281646 | 1 | 1 | 1 | 0 |
| 9299 | 123403 | 1.000000 | 0.398993 | 0.385593 | 0.288915 | 1 | 0 | 1 | 0 |
| 9299 | 127341 | 1.000000 | 0.418393 | 0.423147 | 0.319294 | 1 | 1 | 1 | 0 |
| 9365 | 123078 | 1.000000 | 0.451079 | 0.372048 | 0.276751 | 1 | 1 | 1 | 1 |
| 9365 | 123403 | 1.000000 | 0.395117 | 0.414532 | 0.309368 | 1 | 1 | 1 | 0 |
| 9365 | 127341 | 1.000000 | 0.450516 | 0.344466 | 0.253525 | 1 | 1 | 1 | 0 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_endpoint_integrity | pass | endpoints=192/192;switch=0;spectrum=0;effect=0 | 192/192;0;0;0 | continue |
| global_forced_edge_witness_integrity | pass | arms=12/12;witnesses=45 | arms=12/12 | continue |
| effect_blind_state_space_choice | pass | coarse_nontrivial=6/6;conflict_nontrivial=0/6 | coarse_nontrivial=6/6;conflict_nontrivial=0/6 | coarse_measure_with_conflict_stratification |
| representation_covariance | pass | 24/24 | 24/24 | continue |
| finite_endpoint_diversity | fail | sources=2/6 | sources=6/6 | measure_concentrated |
| finite_batch_center_stability | fail | features=35/36 | 36/36 | increase_or_repair_sampling |
| independent_seed_family_stability | pass | features=36/36 | 36/36 | finitely_qualified |
| v16x_overall | v16x_integer_measure_endpoint_diversity_not_qualified | integrity=1;witness=1;state=1;representation=1;diversity=0;batch=0;seed=1;exclusion=1 | 1;1;1;1;1;1;1;1 | v16x_integer_measure_endpoint_diversity_not_qualified |

## Interpretation boundary

A pass would establish only finite implementation qualification for this declared random-cost measure on six frozen DAGs. It would not validate the old LP procedure, prove uniform sampling, establish a canonical null, or reproduce the v16s effect.

A failure still narrows the method: it identifies whether representation covariance, finite diversity, seed-family stability, or the state-space choice remains unresolved before effect inspection.

V16x establishes no energy, temperature, invariant, dimension, manifold, Lorentz symmetry, spacetime, particle, entanglement, continuum, or physical law.

## Algorithm references

- Mulmuley, Vazirani, and Vazirani, *Matching is as Easy as Matrix Inversion* (1987), DOI: https://doi.org/10.1145/28395.383347
- NetworkX `network_simplex` documentation: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.network_simplex.html
