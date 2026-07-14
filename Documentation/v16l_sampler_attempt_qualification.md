# v16l sampler attempt-budget qualification

Status: `sampler_attempt_budget_qualified_for_new_holdout`.

v16l keeps frozen v16k failed. It changes only the operational safety ceiling from 60 to 240 attempts per direct edge and reruns the exact same perturbation seeds, targets, stopping conditions, and null counts on the saved v16k DAGs.

Specification digest: `e730d36cef1ec18ef13ce07a24c4b25cbc3c8a016d3fd3058b56b98a586e0413`.

## Effect-blind qualification

| null_family | n_perturbations | completion_and_integrity_passes | max_observed_attempts_per_edge | min_changed_edge_fraction | all_unique_within_run | qualification_pass |
| --- | --- | --- | --- | --- | --- | --- |
| degree_depth_global_age_bin_double_edge_swap | 384.000000 | 384.000000 | 60.138480 | 0.100026 | 1.000000 | 1.000000 |
| degree_depth_global_age_bin_double_edge_swap_longer_010 | 192.000000 | 192.000000 | 75.522982 | 0.111359 | 1.000000 | 1.000000 |

## Post-hoc spectrum sensitivity

These rows are nonconfirmatory and did not enter the qualification decision.

| growth_seed | run_offset | arm | null_family | source_js_effect_ratio | qualified_js_effect_ratio | qualified_over_source_ratio | same_effect_direction | confirmatory |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6132.000000 | 91663.000000 | current_global | degree_depth_global_age_bin_double_edge_swap | 14.112097 | 14.112097 | 1.000000 | 1.000000 | 0.000000 |
| 6132.000000 | 91663.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap | 8.518326 | 8.518326 | 1.000000 | 1.000000 | 0.000000 |
| 6132.000000 | 92980.000000 | current_global | degree_depth_global_age_bin_double_edge_swap | 19.586443 | 19.586443 | 1.000000 | 1.000000 | 0.000000 |
| 6132.000000 | 92980.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap | 3.275483 | 3.275483 | 1.000000 | 1.000000 | 0.000000 |
| 6132.000000 | 96729.000000 | current_global | degree_depth_global_age_bin_double_edge_swap | 4.300979 | 4.300979 | 1.000000 | 1.000000 | 0.000000 |
| 6132.000000 | 96729.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap | 5.832132 | 5.832132 | 1.000000 | 1.000000 | 0.000000 |
| 8036.000000 | 91663.000000 | current_global | degree_depth_global_age_bin_double_edge_swap | 15.417067 | 15.417067 | 1.000000 | 1.000000 | 0.000000 |
| 8036.000000 | 91663.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap | 11.541961 | 11.541961 | 1.000000 | 1.000000 | 0.000000 |
| 8036.000000 | 92980.000000 | current_global | degree_depth_global_age_bin_double_edge_swap | 8.650976 | 8.700842 | 1.005764 | 1.000000 | 0.000000 |
| 8036.000000 | 92980.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap | 8.667017 | 8.667017 | 1.000000 | 1.000000 | 0.000000 |
| 8036.000000 | 96729.000000 | current_global | degree_depth_global_age_bin_double_edge_swap | 11.274753 | 11.274753 | 1.000000 | 1.000000 | 0.000000 |
| 8036.000000 | 96729.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap | 16.792664 | 16.792664 | 1.000000 | 1.000000 | 0.000000 |
| 6132.000000 | 91663.000000 | current_global | degree_depth_global_age_bin_double_edge_swap_longer_010 | 16.437266 | 16.437266 | 1.000000 | 1.000000 | 0.000000 |
| 6132.000000 | 91663.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap_longer_010 | 7.210570 | 7.210570 | 1.000000 | 1.000000 | 0.000000 |
| 6132.000000 | 92980.000000 | current_global | degree_depth_global_age_bin_double_edge_swap_longer_010 | 19.279691 | 19.279691 | 1.000000 | 1.000000 | 0.000000 |
| 6132.000000 | 92980.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap_longer_010 | 4.304116 | 4.304116 | 1.000000 | 1.000000 | 0.000000 |
| 6132.000000 | 96729.000000 | current_global | degree_depth_global_age_bin_double_edge_swap_longer_010 | 5.658728 | 5.658728 | 1.000000 | 1.000000 | 0.000000 |
| 6132.000000 | 96729.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap_longer_010 | 6.930345 | 6.930345 | 1.000000 | 1.000000 | 0.000000 |
| 8036.000000 | 91663.000000 | current_global | degree_depth_global_age_bin_double_edge_swap_longer_010 | 17.127206 | 17.127206 | 1.000000 | 1.000000 | 0.000000 |
| 8036.000000 | 91663.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap_longer_010 | 14.485155 | 19.422795 | 1.340876 | 1.000000 | 0.000000 |
| 8036.000000 | 92980.000000 | current_global | degree_depth_global_age_bin_double_edge_swap_longer_010 | 19.108526 | 16.253114 | 0.850569 | 1.000000 | 0.000000 |
| 8036.000000 | 92980.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap_longer_010 | 10.325918 | 10.325918 | 1.000000 | 1.000000 | 0.000000 |
| 8036.000000 | 96729.000000 | current_global | degree_depth_global_age_bin_double_edge_swap_longer_010 | 27.766754 | 27.766754 | 1.000000 | 1.000000 | 0.000000 |
| 8036.000000 | 96729.000000 | exposure_matched_local | degree_depth_global_age_bin_double_edge_swap_longer_010 | 20.405286 | 20.405286 | 1.000000 | 1.000000 | 0.000000 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| v16k_source_contract | pass | 1.000000 | 1.000000 | continue |
| primary_completion_integrity | pass | 384/384 | 384/384 | continue |
| longer_completion_integrity | pass | 192/192 | 192/192 | continue |
| effect_blind_qualification | pass | 0.000000 | effect_values_used=0 | continue |
| v16l_overall | sampler_attempt_budget_qualified_for_new_holdout | source=1;primary=1;longer=1 | 1;1;1 | sampler_attempt_budget_qualified_for_new_holdout |

## Interpretation boundary

A pass means only that the larger safety ceiling completes the declared perturbation contracts on these saved DAGs and can be frozen for a new holdout. It does not prove convergence, stationarity, independence, representativeness, or uniform sampling. It does not make v16k a completed replication.

No result here establishes dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum behavior, particles, entanglement, or a physical causal law.
