# UniverseSimulation v16d: preregistered target-scale holdout

## Research question

Does the exact frozen v16c quotient map retain its transition-ratio family when target size increases from 1024 to 1536 at the same two-events-per-initial-target-node exposure?

## Evidential separation

- Frozen architecture: the v16c script hash, map, scales, metrics, and thresholds were locked before fresh target-1536 dynamics.
- Frozen reference: six target-1024 local medians were copied from v16c into a separate baseline artifact before preregistration.
- Actual dynamics: twelve new target-1536 histories were generated after preregistration.
- Primary holdout: target-1536 local medians divided by the frozen target-1024 local medians.
- Diagnostic control: current-global remains a scheduler contrast, not the primary architecture candidate.
- Negative boundary: continuum, Lorentz, spacetime, particle, entanglement, and universal-causality claims were not tested.

## Source contract

| check | observed | required | status |
| --- | --- | --- | --- |
| v16c_overall | pass_to_v16d_scale_holdout | pass_to_v16d_scale_holdout | pass |
| v16c_all_subgates | 0.000000 | 0.000000 | pass |
| v16c_preregistration_reverified | verified | verified | pass |
| frozen_map_and_threshold_contract | 1.000000 | 1.000000 | pass |
| v16c_source_script_sha256 | c143b58862e3fa82c0ba012e3a14224b7c5135226f92b6f15c4bca14cbaca7ef | frozen into v16d preregistration | pass |
| frozen_v16c_baseline | 3c8b9de8c44ace77925b9552503fcd57f7945a8f9b7ee062295012eec9315264 | six exact local transition medians | pass |

## Frozen holdout design

Target `1536`, source target `1024`, fresh growth seeds `3407/3511`, offsets `61001/61043/61091`, `3072` events (`2` per target node), and the unchanged scheduler arms.

The quotient map is imported from the hash-locked v16c script. No target-1536 calibration was performed before preregistration.

Target hygiene:

| target_nodes | growth_replicates | mean_initial_nodes | q10_initial_nodes | source_q90_initial_nodes | separated_from_source | event_budget |
| --- | --- | --- | --- | --- | --- | --- |
| 1536.000000 | 2.000000 | 1536.000000 | 1536.000000 | 1024.000000 | 1.000000 | 3072.000000 |

## Fine histories

| growth_seed | run_offset | arm | n_events | fine_edges | fine_causal_depth | fine_max_layer_width | topological_replay_failures | relabel_pass | coarse_map_transport_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3407.000000 | 61001.000000 | current_global | 3072.000000 | 3673.000000 | 60.000000 | 98.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3407.000000 | 61001.000000 | exposure_matched_local | 3072.000000 | 3521.000000 | 54.000000 | 120.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3407.000000 | 61043.000000 | current_global | 3072.000000 | 3685.000000 | 70.000000 | 91.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3407.000000 | 61043.000000 | exposure_matched_local | 3072.000000 | 3629.000000 | 72.000000 | 103.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3407.000000 | 61091.000000 | current_global | 3072.000000 | 3457.000000 | 63.000000 | 99.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3407.000000 | 61091.000000 | exposure_matched_local | 3072.000000 | 3633.000000 | 62.000000 | 104.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3511.000000 | 61001.000000 | current_global | 3072.000000 | 3493.000000 | 58.000000 | 105.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3511.000000 | 61001.000000 | exposure_matched_local | 3072.000000 | 3432.000000 | 60.000000 | 105.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3511.000000 | 61043.000000 | current_global | 3072.000000 | 3615.000000 | 57.000000 | 115.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3511.000000 | 61043.000000 | exposure_matched_local | 3072.000000 | 3436.000000 | 64.000000 | 90.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3511.000000 | 61091.000000 | current_global | 3072.000000 | 3611.000000 | 61.000000 | 94.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3511.000000 | 61091.000000 | exposure_matched_local | 3072.000000 | 3673.000000 | 64.000000 | 96.000000 | 0.000000 | 1.000000 | 1.000000 |

## Three-scale quotients

| growth_seed | run_offset | arm | scale_window | coarse_nodes | coarse_edges | node_retention | causal_depth | max_layer_width | comparable_pair_fraction | dependency_density |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3407.000000 | 61001.000000 | current_global | 1.000000 | 3072.000000 | 3673.000000 | 1.000000 | 60.000000 | 98.000000 | 0.040810 | 1.195638 |
| 3407.000000 | 61001.000000 | current_global | 4.000000 | 755.000000 | 1009.000000 | 0.245768 | 15.000000 | 96.000000 | 0.074664 | 1.336424 |
| 3407.000000 | 61001.000000 | current_global | 16.000000 | 158.000000 | 207.000000 | 0.051432 | 4.000000 | 56.000000 | 0.130533 | 1.310127 |
| 3407.000000 | 61001.000000 | exposure_matched_local | 1.000000 | 3072.000000 | 3521.000000 | 1.000000 | 54.000000 | 120.000000 | 0.024399 | 1.146159 |
| 3407.000000 | 61001.000000 | exposure_matched_local | 4.000000 | 772.000000 | 939.000000 | 0.251302 | 14.000000 | 116.000000 | 0.032590 | 1.216321 |
| 3407.000000 | 61001.000000 | exposure_matched_local | 16.000000 | 169.000000 | 220.000000 | 0.055013 | 4.000000 | 103.000000 | 0.041420 | 1.301775 |
| 3407.000000 | 61043.000000 | current_global | 1.000000 | 3072.000000 | 3685.000000 | 1.000000 | 70.000000 | 91.000000 | 0.039986 | 1.199544 |
| 3407.000000 | 61043.000000 | current_global | 4.000000 | 766.000000 | 1030.000000 | 0.249349 | 18.000000 | 85.000000 | 0.054509 | 1.344648 |
| 3407.000000 | 61043.000000 | current_global | 16.000000 | 167.000000 | 251.000000 | 0.054362 | 5.000000 | 70.000000 | 0.068465 | 1.502994 |
| 3407.000000 | 61043.000000 | exposure_matched_local | 1.000000 | 3072.000000 | 3629.000000 | 1.000000 | 72.000000 | 103.000000 | 0.038343 | 1.181315 |
| 3407.000000 | 61043.000000 | exposure_matched_local | 4.000000 | 768.000000 | 1017.000000 | 0.250000 | 18.000000 | 103.000000 | 0.052345 | 1.324219 |
| 3407.000000 | 61043.000000 | exposure_matched_local | 16.000000 | 187.000000 | 237.000000 | 0.060872 | 5.000000 | 99.000000 | 0.071531 | 1.267380 |
| 3407.000000 | 61091.000000 | current_global | 1.000000 | 3072.000000 | 3457.000000 | 1.000000 | 63.000000 | 99.000000 | 0.031447 | 1.125326 |
| 3407.000000 | 61091.000000 | current_global | 4.000000 | 763.000000 | 895.000000 | 0.248372 | 16.000000 | 95.000000 | 0.037561 | 1.173001 |
| 3407.000000 | 61091.000000 | current_global | 16.000000 | 173.000000 | 223.000000 | 0.056315 | 4.000000 | 66.000000 | 0.047117 | 1.289017 |
| 3407.000000 | 61091.000000 | exposure_matched_local | 1.000000 | 3072.000000 | 3633.000000 | 1.000000 | 62.000000 | 104.000000 | 0.039844 | 1.182617 |
| 3407.000000 | 61091.000000 | exposure_matched_local | 4.000000 | 755.000000 | 1023.000000 | 0.245768 | 16.000000 | 103.000000 | 0.059339 | 1.354967 |
| 3407.000000 | 61091.000000 | exposure_matched_local | 16.000000 | 144.000000 | 193.000000 | 0.046875 | 4.000000 | 69.000000 | 0.101010 | 1.340278 |
| 3511.000000 | 61001.000000 | current_global | 1.000000 | 3072.000000 | 3493.000000 | 1.000000 | 58.000000 | 105.000000 | 0.030749 | 1.137044 |
| 3511.000000 | 61001.000000 | current_global | 4.000000 | 756.000000 | 927.000000 | 0.246094 | 15.000000 | 98.000000 | 0.038726 | 1.226190 |
| 3511.000000 | 61001.000000 | current_global | 16.000000 | 150.000000 | 169.000000 | 0.048828 | 4.000000 | 64.000000 | 0.047427 | 1.126667 |
| 3511.000000 | 61001.000000 | exposure_matched_local | 1.000000 | 3072.000000 | 3432.000000 | 1.000000 | 60.000000 | 105.000000 | 0.020709 | 1.117188 |
| 3511.000000 | 61001.000000 | exposure_matched_local | 4.000000 | 769.000000 | 866.000000 | 0.250326 | 15.000000 | 103.000000 | 0.022222 | 1.126138 |
| 3511.000000 | 61001.000000 | exposure_matched_local | 16.000000 | 189.000000 | 212.000000 | 0.061523 | 4.000000 | 97.000000 | 0.025386 | 1.121693 |
| 3511.000000 | 61043.000000 | current_global | 1.000000 | 3072.000000 | 3615.000000 | 1.000000 | 57.000000 | 115.000000 | 0.024026 | 1.176758 |
| 3511.000000 | 61043.000000 | current_global | 4.000000 | 754.000000 | 942.000000 | 0.245443 | 15.000000 | 107.000000 | 0.028096 | 1.249337 |
| 3511.000000 | 61043.000000 | current_global | 16.000000 | 145.000000 | 163.000000 | 0.047201 | 4.000000 | 80.000000 | 0.032184 | 1.124138 |
| 3511.000000 | 61043.000000 | exposure_matched_local | 1.000000 | 3072.000000 | 3436.000000 | 1.000000 | 64.000000 | 90.000000 | 0.022869 | 1.118490 |
| 3511.000000 | 61043.000000 | exposure_matched_local | 4.000000 | 775.000000 | 874.000000 | 0.252279 | 16.000000 | 88.000000 | 0.024586 | 1.127742 |
| 3511.000000 | 61043.000000 | exposure_matched_local | 16.000000 | 178.000000 | 193.000000 | 0.057943 | 4.000000 | 78.000000 | 0.027741 | 1.084270 |
| 3511.000000 | 61091.000000 | current_global | 1.000000 | 3072.000000 | 3611.000000 | 1.000000 | 61.000000 | 94.000000 | 0.029107 | 1.175456 |
| 3511.000000 | 61091.000000 | current_global | 4.000000 | 751.000000 | 956.000000 | 0.244466 | 16.000000 | 87.000000 | 0.034464 | 1.272969 |
| 3511.000000 | 61091.000000 | current_global | 16.000000 | 153.000000 | 175.000000 | 0.049805 | 4.000000 | 69.000000 | 0.042312 | 1.143791 |
| 3511.000000 | 61091.000000 | exposure_matched_local | 1.000000 | 3072.000000 | 3673.000000 | 1.000000 | 64.000000 | 96.000000 | 0.031012 | 1.195638 |
| 3511.000000 | 61091.000000 | exposure_matched_local | 4.000000 | 763.000000 | 1002.000000 | 0.248372 | 16.000000 | 93.000000 | 0.034626 | 1.313237 |
| 3511.000000 | 61091.000000 | exposure_matched_local | 16.000000 | 161.000000 | 205.000000 | 0.052409 | 4.000000 | 60.000000 | 0.041227 | 1.273292 |

## Local stability

| transition | metric | median_retention | retention_cv | local_stability_pass |
| --- | --- | --- | --- | --- |
| 1_to_4 | causal_depth_retention | 0.250000 | 0.017751 | 1.000000 |
| 1_to_4 | antichain_width_retention | 0.979365 | 0.013015 | 1.000000 |
| 1_to_4 | dependency_density_retention | 1.079786 | 0.053957 | 1.000000 |
| 4_to_16 | causal_depth_retention | 0.258333 | 0.060133 | 1.000000 |
| 4_to_16 | antichain_width_retention | 0.887147 | 0.166531 | 1.000000 |
| 4_to_16 | dependency_density_retention | 0.979371 | 0.042331 | 1.000000 |

## Growth-seed transfer

| transition | metric | growth_3407_median | growth_3511_median | second_over_first_ratio | growth_transfer_pass |
| --- | --- | --- | --- | --- | --- |
| 1_to_4 | causal_depth_retention | 0.258065 | 0.250000 | 0.968750 | 1.000000 |
| 1_to_4 | antichain_width_retention | 0.990385 | 0.977778 | 0.987271 | 1.000000 |
| 1_to_4 | dependency_density_retention | 1.120970 | 1.008272 | 0.899464 | 1.000000 |
| 4_to_16 | causal_depth_retention | 0.277778 | 0.250000 | 0.900000 | 1.000000 |
| 4_to_16 | antichain_width_retention | 0.887931 | 0.886364 | 0.998235 | 1.000000 |
| 4_to_16 | dependency_density_retention | 0.989159 | 0.969583 | 0.980209 | 1.000000 |

## Primary target transfer

| transition | metric | source_local_median | holdout_local_median | holdout_over_source_ratio | target_transfer_pass |
| --- | --- | --- | --- | --- | --- |
| 1_to_4 | causal_depth_retention | 0.259630 | 0.250000 | 0.962910 | 1.000000 |
| 1_to_4 | antichain_width_retention | 0.972174 | 0.979365 | 1.007397 | 1.000000 |
| 1_to_4 | dependency_density_retention | 1.033498 | 1.079786 | 1.044788 | 1.000000 |
| 4_to_16 | causal_depth_retention | 0.285714 | 0.258333 | 0.904167 | 1.000000 |
| 4_to_16 | antichain_width_retention | 0.791010 | 0.887147 | 1.121537 | 1.000000 |
| 4_to_16 | dependency_density_retention | 0.893460 | 0.979371 | 1.096155 | 1.000000 |

## Scheduler diagnostic

| transition | metric | current_global_median | local_median | local_over_global_ratio | scheduler_transfer_pass | nonseed_event_tv | nonseed_tv_pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1_to_4 | causal_depth_retention | 0.257882 | 0.250000 | 0.969436 | 1.000000 | 0.000814 | 1.000000 |
| 1_to_4 | antichain_width_retention | 0.933700 | 0.979365 | 1.048908 | 1.000000 | 0.000814 | 1.000000 |
| 1_to_4 | dependency_density_retention | 1.080680 | 1.079786 | 0.999173 | 1.000000 | 0.000814 | 1.000000 |
| 4_to_16 | causal_depth_retention | 0.266667 | 0.258333 | 0.968750 | 1.000000 | 0.000814 | 1.000000 |
| 4_to_16 | antichain_width_retention | 0.721200 | 0.887147 | 1.230099 | 1.000000 | 0.000814 | 1.000000 |
| 4_to_16 | dependency_density_retention | 0.949579 | 0.979371 | 1.031374 | 1.000000 | 0.000814 | 1.000000 |

## Gate evaluation

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| v16c_source_contract | pass | 1.000000 | 1.000000 | continue |
| target_1536_hygiene | pass | mean=1536.0;separated=1 | mean=1536;separated=1 | continue |
| fresh_run_integrity | pass | runs=12;invalid=0 | runs=12;invalid=0 | continue |
| fine_dag_integrity | pass | acyclic=12;witness_errors=0 | acyclic=12;witness_errors=0 | continue |
| fresh_topological_replay | pass | replays=24;min_reorder=0.996419;failures=0 | replays=24;failures=0 | continue |
| relabel_and_map_transport | pass | 12.000000 | 12.000000 | continue |
| quotient_map_integrity | pass | passes=36/36 | 36.000000 | continue |
| scale1_identity | pass | 1.000000 | 1.000000 | continue |
| strict_three_scale_compression | pass | 1.000000 | 1.000000 | continue |
| scale16_nondegenerate | pass | nodes=144-189;retention=0.046875-0.061523 | nodes>=16;retention in [0.01,0.9] | continue |
| local_transition_cv | pass | 1_to_4:causal_depth_retention=0.017751;1_to_4:antichain_width_retention=0.013015;1_to_4:dependency_density_retention=0.053957;4_to_16:causal_depth_retention=0.060133;4_to_16:antichain_width_retention=0.166531;4_to_16:dependency_density_retention=0.042331 | each<=0.4 | continue |
| growth_seed_transfer | pass | 1_to_4:causal_depth_retention=0.968750;1_to_4:antichain_width_retention=0.987271;1_to_4:dependency_density_retention=0.899464;4_to_16:causal_depth_retention=0.900000;4_to_16:antichain_width_retention=0.998235;4_to_16:dependency_density_retention=0.980209 | each in [0.6,1.67] | continue |
| target_1024_to_1536_transfer | pass | 1_to_4:causal_depth_retention=0.962910;1_to_4:antichain_width_retention=1.007397;1_to_4:dependency_density_retention=1.044788;4_to_16:causal_depth_retention=0.904167;4_to_16:antichain_width_retention=1.121537;4_to_16:dependency_density_retention=1.096155 | each in [0.6,1.67] | continue |
| scheduler_diagnostic_transfer | pass | 1_to_4:causal_depth_retention=0.969436;1_to_4:antichain_width_retention=1.048908;1_to_4:dependency_density_retention=0.999173;4_to_16:causal_depth_retention=0.968750;4_to_16:antichain_width_retention=1.230099;4_to_16:dependency_density_retention=1.031374;tv=0.000814 | ratios in [0.6,1.67];tv<=0.05 | continue |
| v16d_overall | pass_to_v16e_independent_coarse_map_gate | 1.000000 | 1.000000 | design_independent_map_gate |

Overall status: `pass_to_v16e_independent_coarse_map_gate`.

## Interpretation

The unchanged finite quotient construction survives a fresh target increase from 1024 to 1536 under equal event density, including exact structural controls and broad transition-ratio transfer bounds. This justifies testing an independent coarse map; it does not justify another same-map scale extension by default.

Causal-depth retention remains construction-adjacent because the map itself bins by depth. Antichain-width and dependency-density retention are less direct, but all three still come from one chosen map. Target transfer is therefore stronger than v16c repetition, yet it is not map-independent evidence.

## Evidential boundary

A pass supports one reproducible finite hierarchy across two target sizes. It does not establish convergence as target grows, a metric, a continuum, Lorentz covariance, quantum structure, or laws matching our universe.

## Next decision

Design one preregistered v16e contrast whose primary map is not defined by causal-depth bins. It must be relabel-invariant, witnessed, and evaluated against null/coarsening controls before more target scaling.
