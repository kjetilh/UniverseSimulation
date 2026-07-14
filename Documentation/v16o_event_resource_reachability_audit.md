# v16o event/resource reachability audit

Status: `v16o_actual_conflict_color_null_structurally_immobile`.

V16o exactly enumerates every unordered direct-edge pair in the six saved v16n calibration DAGs. It compares the frozen same-color proposal with the more general global two-color multiset rule. It performs no rewiring and computes no interval spectrum.

Specification digest: `d5dfa4d7b0fbe3f92bd47a827d252416c4c353d9a9ec22e5343492192dae4c4a`.

## Per-run support

| growth_seed | run_offset | edge_count | all_unordered_edge_pairs | same_color_legal_pairs | same_color_legal_edge_fraction | general_multiset_legal_pairs | general_multiset_legal_edge_fraction | general_multiset_promising_support |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7252.000000 | 110360.000000 | 3498.000000 | 6116253.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 7252.000000 | 114756.000000 | 3623.000000 | 6561253.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 7252.000000 | 117562.000000 | 3463.000000 | 5994453.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 8018.000000 | 110360.000000 | 3566.000000 | 6356395.000000 | 0.000000 | 0.000000 | 1.000000 | 0.000561 | 0.000000 |
| 8018.000000 | 114756.000000 | 3557.000000 | 6324346.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 8018.000000 | 117562.000000 | 3513.000000 | 6168828.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| exact_pair_enumeration | pass | runs=6;pairs=37521528 | runs=6;all_pairs_exact | continue |
| v16n_same_color_zero_move_reproduction | pass | 0.000000 | 0.000000 | diagnosed |
| general_color_multiset_reachability | fail | legal_pairs=1;runs_with_moves=1/6 | runs_with_moves=6/6 | retire_actual_conflict_color_null |
| general_color_multiset_support | fail | 0.000000 | >=0.1 | do_not_run_effect_gate |
| spectrum_and_rewiring_exclusion | pass | spectrum=0;rewires=0 | 0;0 | diagnostic_only |
| v16o_overall | v16o_actual_conflict_color_null_structurally_immobile | same_zero=1;general_reachable=0;general_promising=0 | diagnostic_branch | v16o_actual_conflict_color_null_structurally_immobile |

## Interpretation boundary

Reachability is necessary but not sufficient for a useful sampler. Legal static swaps do not establish chain connectivity, mixing, convergence, stationarity, independence, representativeness, or uniformity.

No event/resource-conditioned spectrum effect or physical claim is evaluated here.
