# UniverseSimulation v16c: preregistered three-scale coarse-graining pilot

## Research question

Can one frozen, node-label-free map turn fresh event-DAG histories into nondegenerate witnessed quotient DAGs at three scales, and do the resulting transition ratios transfer across fresh bases and the local/global scheduler contrast?

## Evidential separation

- Architecture definition: causal-depth windows and within-window direct-edge connected components define the quotient map.
- Design calibration: v16b histories were used only to reject degenerate scale choices before preregistration; they are not v16c holdout evidence.
- Generated artifacts: memberships, quotient edges, and ratio summaries are deterministic functions of each fresh event DAG.
- Actual dynamics: twelve new histories were generated only after the calibration artifact and preregistration were written.
- Negative boundary: continuum, Lorentz, spacetime, particle, entanglement, and universal-causality claims were not tested.

## Frozen source contract

| check | observed | required | status |
| --- | --- | --- | --- |
| v16b_overall | pass_to_v16c_coarse_graining_pilot | pass_to_v16c_coarse_graining_pilot | pass |
| v16b_target_hygiene | 1.000000 | 1.000000 | pass |
| design_calibration_present | bf0f0f2af98be9e44b1bc75a0881f2638dd25583ecb4a96407951dd97a79fbdf | nonempty calibration artifact from v16b | pass |
| local_adapter_rate_frozen | 0.000504 | 0.000504 | pass |

## Frozen map

For each scale window `w in {1,4,16}`, each event receives `floor(causal_depth / w)`. Direct dependency edges whose endpoints are in the same bin are treated as undirected for component contraction. Every remaining quotient edge stores one or more concrete fine-edge witnesses. The map does not inspect graph node labels or original scheduler positions beyond the dependency DAG.

Fresh target `1024`, growth seeds `3109/3203`, run offsets `51017/51059/51091`, `2048` events, and scheduler arms `current_global` / frozen `exposure_matched_local`.

Target hygiene:

| target_nodes | growth_replicates | mean_initial_nodes | mean_initial_tokens | mean_initial_beta1 | separated_from_prev |
| --- | --- | --- | --- | --- | --- |
| 1024.000000 | 2.000000 | 1024.000000 | 19.000000 | 126.000000 | 1.000000 |

## Fine histories

| growth_seed | run_offset | arm | n_events | fine_edges | fine_causal_depth | fine_max_layer_width | topological_replay_failures | relabel_pass | coarse_map_transport_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3109.000000 | 51017.000000 | current_global | 2048.000000 | 2291.000000 | 45.000000 | 86.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3109.000000 | 51017.000000 | exposure_matched_local | 2048.000000 | 2296.000000 | 45.000000 | 75.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3109.000000 | 51059.000000 | current_global | 2048.000000 | 2313.000000 | 53.000000 | 74.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3109.000000 | 51059.000000 | exposure_matched_local | 2048.000000 | 2339.000000 | 54.000000 | 67.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3109.000000 | 51091.000000 | current_global | 2048.000000 | 2397.000000 | 45.000000 | 90.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3109.000000 | 51091.000000 | exposure_matched_local | 2048.000000 | 2457.000000 | 50.000000 | 81.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3203.000000 | 51017.000000 | current_global | 2048.000000 | 2329.000000 | 60.000000 | 61.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3203.000000 | 51017.000000 | exposure_matched_local | 2048.000000 | 2334.000000 | 55.000000 | 80.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3203.000000 | 51059.000000 | current_global | 2048.000000 | 2359.000000 | 58.000000 | 81.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3203.000000 | 51059.000000 | exposure_matched_local | 2048.000000 | 2255.000000 | 58.000000 | 72.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3203.000000 | 51091.000000 | current_global | 2048.000000 | 2307.000000 | 46.000000 | 102.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3203.000000 | 51091.000000 | exposure_matched_local | 2048.000000 | 2310.000000 | 53.000000 | 69.000000 | 0.000000 | 1.000000 | 1.000000 |

## Three-scale quotients

| growth_seed | run_offset | arm | scale_window | coarse_nodes | coarse_edges | node_retention | causal_depth | max_layer_width | comparable_pair_fraction | dependency_density |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3109.000000 | 51017.000000 | current_global | 1.000000 | 2048.000000 | 2291.000000 | 1.000000 | 45.000000 | 86.000000 | 0.028891 | 1.118652 |
| 3109.000000 | 51017.000000 | current_global | 4.000000 | 510.000000 | 578.000000 | 0.249023 | 12.000000 | 80.000000 | 0.037598 | 1.133333 |
| 3109.000000 | 51017.000000 | current_global | 16.000000 | 101.000000 | 101.000000 | 0.049316 | 3.000000 | 48.000000 | 0.053465 | 1.000000 |
| 3109.000000 | 51017.000000 | exposure_matched_local | 1.000000 | 2048.000000 | 2296.000000 | 1.000000 | 45.000000 | 75.000000 | 0.026181 | 1.121094 |
| 3109.000000 | 51017.000000 | exposure_matched_local | 4.000000 | 521.000000 | 598.000000 | 0.254395 | 12.000000 | 73.000000 | 0.028163 | 1.147793 |
| 3109.000000 | 51017.000000 | exposure_matched_local | 16.000000 | 122.000000 | 138.000000 | 0.059570 | 3.000000 | 58.000000 | 0.032380 | 1.131148 |
| 3109.000000 | 51059.000000 | current_global | 1.000000 | 2048.000000 | 2313.000000 | 1.000000 | 53.000000 | 74.000000 | 0.028943 | 1.129395 |
| 3109.000000 | 51059.000000 | current_global | 4.000000 | 500.000000 | 576.000000 | 0.244141 | 14.000000 | 65.000000 | 0.038044 | 1.152000 |
| 3109.000000 | 51059.000000 | current_global | 16.000000 | 116.000000 | 119.000000 | 0.056641 | 4.000000 | 60.000000 | 0.051874 | 1.025862 |
| 3109.000000 | 51059.000000 | exposure_matched_local | 1.000000 | 2048.000000 | 2339.000000 | 1.000000 | 54.000000 | 67.000000 | 0.029606 | 1.142090 |
| 3109.000000 | 51059.000000 | exposure_matched_local | 4.000000 | 512.000000 | 610.000000 | 0.250000 | 14.000000 | 67.000000 | 0.031678 | 1.191406 |
| 3109.000000 | 51059.000000 | exposure_matched_local | 16.000000 | 115.000000 | 125.000000 | 0.056152 | 4.000000 | 48.000000 | 0.035698 | 1.086957 |
| 3109.000000 | 51091.000000 | current_global | 1.000000 | 2048.000000 | 2397.000000 | 1.000000 | 45.000000 | 90.000000 | 0.033762 | 1.170410 |
| 3109.000000 | 51091.000000 | current_global | 4.000000 | 513.000000 | 640.000000 | 0.250488 | 12.000000 | 86.000000 | 0.044530 | 1.247563 |
| 3109.000000 | 51091.000000 | current_global | 16.000000 | 116.000000 | 132.000000 | 0.056641 | 3.000000 | 65.000000 | 0.060570 | 1.137931 |
| 3109.000000 | 51091.000000 | exposure_matched_local | 1.000000 | 2048.000000 | 2457.000000 | 1.000000 | 50.000000 | 81.000000 | 0.039677 | 1.199707 |
| 3109.000000 | 51091.000000 | exposure_matched_local | 4.000000 | 506.000000 | 681.000000 | 0.247070 | 13.000000 | 80.000000 | 0.054123 | 1.345850 |
| 3109.000000 | 51091.000000 | exposure_matched_local | 16.000000 | 112.000000 | 125.000000 | 0.054688 | 4.000000 | 63.000000 | 0.055341 | 1.116071 |
| 3203.000000 | 51017.000000 | current_global | 1.000000 | 2048.000000 | 2329.000000 | 1.000000 | 60.000000 | 61.000000 | 0.034403 | 1.137207 |
| 3203.000000 | 51017.000000 | current_global | 4.000000 | 511.000000 | 603.000000 | 0.249512 | 15.000000 | 57.000000 | 0.036867 | 1.180039 |
| 3203.000000 | 51017.000000 | current_global | 16.000000 | 128.000000 | 143.000000 | 0.062500 | 4.000000 | 53.000000 | 0.036048 | 1.117188 |
| 3203.000000 | 51017.000000 | exposure_matched_local | 1.000000 | 2048.000000 | 2334.000000 | 1.000000 | 55.000000 | 80.000000 | 0.031791 | 1.139648 |
| 3203.000000 | 51017.000000 | exposure_matched_local | 4.000000 | 514.000000 | 592.000000 | 0.250977 | 14.000000 | 77.000000 | 0.032645 | 1.151751 |
| 3203.000000 | 51017.000000 | exposure_matched_local | 16.000000 | 125.000000 | 125.000000 | 0.061035 | 4.000000 | 74.000000 | 0.027613 | 1.000000 |
| 3203.000000 | 51059.000000 | current_global | 1.000000 | 2048.000000 | 2359.000000 | 1.000000 | 58.000000 | 81.000000 | 0.034561 | 1.151855 |
| 3203.000000 | 51059.000000 | current_global | 4.000000 | 501.000000 | 596.000000 | 0.244629 | 15.000000 | 73.000000 | 0.036120 | 1.189621 |
| 3203.000000 | 51059.000000 | current_global | 16.000000 | 117.000000 | 123.000000 | 0.057129 | 4.000000 | 62.000000 | 0.037725 | 1.051282 |
| 3203.000000 | 51059.000000 | exposure_matched_local | 1.000000 | 2048.000000 | 2255.000000 | 1.000000 | 58.000000 | 72.000000 | 0.034962 | 1.101074 |
| 3203.000000 | 51059.000000 | exposure_matched_local | 4.000000 | 516.000000 | 579.000000 | 0.251953 | 15.000000 | 65.000000 | 0.041349 | 1.122093 |
| 3203.000000 | 51059.000000 | exposure_matched_local | 16.000000 | 116.000000 | 131.000000 | 0.056641 | 4.000000 | 53.000000 | 0.046027 | 1.129310 |
| 3203.000000 | 51091.000000 | current_global | 1.000000 | 2048.000000 | 2307.000000 | 1.000000 | 46.000000 | 102.000000 | 0.027983 | 1.126465 |
| 3203.000000 | 51091.000000 | current_global | 4.000000 | 514.000000 | 581.000000 | 0.250977 | 12.000000 | 100.000000 | 0.032403 | 1.130350 |
| 3203.000000 | 51091.000000 | current_global | 16.000000 | 123.000000 | 137.000000 | 0.060059 | 3.000000 | 65.000000 | 0.032920 | 1.113821 |
| 3203.000000 | 51091.000000 | exposure_matched_local | 1.000000 | 2048.000000 | 2310.000000 | 1.000000 | 53.000000 | 69.000000 | 0.035757 | 1.127930 |
| 3203.000000 | 51091.000000 | exposure_matched_local | 4.000000 | 500.000000 | 605.000000 | 0.244141 | 14.000000 | 67.000000 | 0.042798 | 1.210000 |
| 3203.000000 | 51091.000000 | exposure_matched_local | 16.000000 | 103.000000 | 109.000000 | 0.050293 | 4.000000 | 50.000000 | 0.047401 | 1.058252 |

## Local transition stability

| transition | metric | mean_retention | median_retention | retention_cv | local_stability_pass |
| --- | --- | --- | --- | --- | --- |
| 1_to_4 | causal_depth_retention | 0.260541 | 0.259630 | 0.016475 | 1.000000 |
| 1_to_4 | antichain_width_retention | 0.966213 | 0.972174 | 0.034984 | 1.000000 |
| 1_to_4 | dependency_density_retention | 1.048547 | 1.033498 | 0.040240 | 1.000000 |
| 4_to_16 | causal_depth_retention | 0.280250 | 0.285714 | 0.070326 | 1.000000 |
| 4_to_16 | antichain_width_retention | 0.803522 | 0.791010 | 0.105828 | 1.000000 |
| 4_to_16 | dependency_density_retention | 0.912727 | 0.893460 | 0.076654 | 1.000000 |

## Fresh-base transfer

| transition | metric | growth_3109_median | growth_3203_median | second_over_first_ratio | growth_transfer_pass |
| --- | --- | --- | --- | --- | --- |
| 1_to_4 | causal_depth_retention | 0.260000 | 0.258621 | 0.994695 | 1.000000 |
| 1_to_4 | antichain_width_retention | 0.987654 | 0.962500 | 0.974531 | 1.000000 |
| 1_to_4 | dependency_density_retention | 1.043181 | 1.019089 | 0.976906 | 1.000000 |
| 4_to_16 | causal_depth_retention | 0.285714 | 0.285714 | 1.000000 | 1.000000 |
| 4_to_16 | antichain_width_retention | 0.787500 | 0.815385 | 1.035409 | 1.000000 |
| 4_to_16 | dependency_density_retention | 0.912331 | 0.874589 | 0.958631 | 1.000000 |

## Scheduler transfer

| transition | metric | current_global_median | local_median | local_over_global_ratio | scheduler_transfer_pass | nonseed_event_tv | nonseed_tv_pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1_to_4 | causal_depth_retention | 0.262510 | 0.259630 | 0.989027 | 1.000000 | 0.007593 | 1.000000 |
| 1_to_4 | antichain_width_retention | 0.932329 | 0.972174 | 1.042737 | 1.000000 | 0.007593 | 1.000000 |
| 1_to_4 | dependency_density_retention | 1.026401 | 1.033498 | 1.006914 | 1.000000 | 0.007593 | 1.000000 |
| 4_to_16 | causal_depth_retention | 0.258333 | 0.285714 | 1.105991 | 1.000000 | 0.007593 | 1.000000 |
| 4_to_16 | antichain_width_retention | 0.802565 | 0.791010 | 0.985603 | 1.000000 | 0.007593 | 1.000000 |
| 4_to_16 | dependency_density_retention | 0.901314 | 0.893460 | 0.991286 | 1.000000 | 0.007593 | 1.000000 |

## Gate evaluation

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| v16b_source_contract | pass | 1.000000 | 1.000000 | continue |
| target_hygiene | pass | 1.000000 | 1.000000 | continue |
| fresh_run_integrity | pass | runs=12;invalid=0 | runs=12;invalid=0 | continue |
| fine_dag_integrity | pass | acyclic=12;witness_errors=0 | acyclic=12;witness_errors=0 | continue |
| fresh_topological_replay | pass | replays=24;min_reorder=0.996094;failures=0 | replays=24;failures=0 | continue |
| relabel_and_map_transport | pass | 12.000000 | 12.000000 | continue |
| quotient_map_integrity | pass | passes=36/36 | 36.000000 | continue |
| scale1_identity | pass | 1.000000 | 1.000000 | continue |
| strict_three_scale_compression | pass | 1.000000 | 1.000000 | continue |
| scale16_nondegenerate | pass | nodes=101-128;retention=0.049316-0.062500 | nodes>=16;retention in [0.01,0.9] | continue |
| local_transition_cv | pass | 1_to_4:causal_depth_retention=0.016475;1_to_4:antichain_width_retention=0.034984;1_to_4:dependency_density_retention=0.040240;4_to_16:causal_depth_retention=0.070326;4_to_16:antichain_width_retention=0.105828;4_to_16:dependency_density_retention=0.076654 | each<=0.4 | continue |
| growth_seed_transfer | pass | 1_to_4:causal_depth_retention=0.994695;1_to_4:antichain_width_retention=0.974531;1_to_4:dependency_density_retention=0.976906;4_to_16:causal_depth_retention=1.000000;4_to_16:antichain_width_retention=1.035409;4_to_16:dependency_density_retention=0.958631 | each in [0.6,1.67] | continue |
| scheduler_transfer | pass | 1_to_4:causal_depth_retention=0.989027;1_to_4:antichain_width_retention=1.042737;1_to_4:dependency_density_retention=1.006914;4_to_16:causal_depth_retention=1.105991;4_to_16:antichain_width_retention=0.985603;4_to_16:dependency_density_retention=0.991286;tv=0.007593 | ratios in [0.6,1.67];tv<=0.05 | continue |
| v16c_overall | pass_to_v16d_scale_holdout | 1.000000 | 1.000000 | design_fresh_scale_holdout |

Overall status: `pass_to_v16d_scale_holdout`.

## Interpretation

The frozen map is exact at scale 1, yields strictly smaller witnessed DAGs at scales 4 and 16, and its three preregistered transition ratios remain inside broad pilot bounds across fresh bases and scheduler arms. This supports one independent scale holdout, not a continuum or spacetime claim.

Causal-depth retention is partly construction-adjacent: depth windows mechanically constrain that ratio toward the inverse window factor. Antichain-width and dependency-density retention are therefore the less direct transfer checks. Passing all three is a consistency result for this map, not three independent physical signals.

## Evidential boundary

A stable finite three-scale quotient would show that the event-history representation supports a repeatable hierarchy under one explicit map. It would not show an observer-independent continuum, metric geometry, Lorentz covariance, quantum entanglement, particles, or laws of our universe.

## Next decision

Run one preregistered v16d holdout with a fresh target or event budget. Freeze the same map and ratios unchanged; use the local adapter as primary and current-global only as a diagnostic control.
