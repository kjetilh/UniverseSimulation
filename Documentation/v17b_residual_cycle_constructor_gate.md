# v17b residual cycle constructor gate

Status: `v17b_resource_not_qualified`.

## Method

The proposal is target-independent and effect-blind. It samples an exact cycle length from 2, 3 or 4 and one selected start edge, enumerates every simple residual alternating cycle of that length from the start, then samples one uniformly. The selected cycle is a distinguished auxiliary; the reverse uses the same exact length and reversed ordered added edges with an exact lazy Metropolis ratio.

## Source qualification

| growth_seed | run_offset | representation_passes | reversibility_passes | movement_passes | minimum_valid_proposals | minimum_accepted_cycles | minimum_final_start_changed_edge_fraction | maximum_chain_seconds | source_qualification_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 2 | 6 | 4 | 144 | 85 | 0.060639 | 93.196351 | 0 |
| 9299 | 123403 | 2 | 6 | 4 | 119 | 77 | 0.056799 | 244.258264 | 0 |
| 9299 | 127341 | 2 | 6 | 4 | 129 | 76 | 0.051944 | 98.854279 | 0 |
| 9365 | 123078 | 2 | 6 | 4 | 138 | 79 | 0.057471 | 270.449001 | 0 |
| 9365 | 123403 | 2 | 6 | 4 | 129 | 84 | 0.056326 | 50.684319 | 1 |
| 9365 | 127341 | 2 | 6 | 4 | 132 | 72 | 0.052969 | 124.891733 | 0 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_integrity | pass | spectrum=0;effect=0 | 0;0 | continue |
| frozen_start_replay | pass | 12/12 | 12/12 | continue |
| representation_covariance | pass | 12/12 | 12/12 | continue |
| exact_reverse_support | pass | 36/36 | 36/36 | continue |
| pathwise_detailed_balance | pass | 36/36 | 36/36 | continue |
| paired_v17a_valid_yield | pass | improved=24/24;median_ratio=2.898276 | 24/24;>=2.0 | continue |
| finite_movement | pass | 24/24 | 24/24 | continue |
| resource_bound | fail | 12/24 | 24/24 | optimize_before_stability |
| v17b_overall | v17b_resource_not_qualified | exclusion=1;starts=12/12;representation=12/12;reverse=36/36;balance=36/36;improvement=1;movement=24/24;resource=12/24 | 1;12/12;12/12;36/36;36/36;1;24/24;24/24 | v17b_resource_not_qualified |

## Finite movement and baseline comparison

Across 24 chains, minimum valid proposals were `119`, minimum accepted cycles `72`, minimum accepted length>=3 cycles `34`, minimum final displacement `0.051944`, and maximum runtime `270.449001` seconds.

Matched against v17a, `24/24` cells increased valid-proposal count and the median ratio was `2.898276`. This comparison diagnoses constructor efficiency; it does not establish convergence or mixing.

## Interpretation boundary

A passing residual constructor would qualify only finite representation, reverse-support, pathwise-balance and movement checks on six reused spaces. It would not prove global irreducibility, stationarity from arbitrary starts, mixing time, a canonical probability law, the v16s source effect, Bell correlations, entanglement, Lorentz symmetry, spacetime or a universe model.
