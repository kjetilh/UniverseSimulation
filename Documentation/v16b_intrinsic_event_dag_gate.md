# UniverseSimulation v16b: history-intrinsic event-DAG gate

## Research question

Can executed local events be represented by a nontrivial dependency DAG whose independent linearizations, concrete relabel replay, and adjacent disjoint swaps preserve the same dynamics, and are coarse DAG fingerprints stable across fresh bases and the local/global scheduler contrast?

## Evidential separation

- Architecture definition: a directed edge records a declared RAW, WAR, or WAW conflict on a concrete node, token, edge, or adjacency resource.
- Generated artifact: the DAG, causal depths, antichain layers, and comparability counts are computed from each executed event history.
- Actual dynamics: twelve fresh runs were executed after a separate preregistration step, six per scheduler arm.
- Negative boundary: no Lorentz, spacetime, particle, entanglement, or universal-causality claim is tested.

## Frozen source contract

| check | observed | required | status |
| --- | --- | --- | --- |
| v16ac_overall | pass_adapter_to_v16b | pass_adapter_to_v16b | pass |
| v16ac_target_status | pass_adapter_to_v16b | pass_adapter_to_v16b | pass |
| v16ac_frozen_rate | 0.000504 | 0.000504 | pass |
| core_anchor_not_promoted | 0.000000 | 0.000000 | pass |
| v16ac_all_subgates | 0.000000 | 0.000000 | pass |

## Design

Target `1024`, fresh growth seeds `2801/2903`, three run offsets, `2048` events, and two independent arms: `current_global` and frozen `exposure_matched_local`. Each trace receives `4` random topological replays.

The DAG frontier connects a read to the most recent writer, and a write to the most recent writer plus readers since that write. Read/read pairs remain unordered. This is a conflict-dependency DAG for the declared support schema, not a claim that the schema is fundamental physics.

Target hygiene:

| target_nodes | growth_replicates | mean_initial_nodes | mean_initial_tokens | mean_initial_beta1 | separated_from_prev |
| --- | --- | --- | --- | --- | --- |
| 1024.000000 | 2.000000 | 1024.000000 | 21.500000 | 134.000000 | 1.000000 |

## Run-level DAG results

| growth_seed | run_offset | arm | n_events | edge_count | causal_depth | causal_depth_fraction | max_layer_width_fraction | comparable_pair_fraction | topological_replay_failures | relabel_pass | commutation_tests | commutation_failures |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2801.000000 | 41011.000000 | current_global | 2048.000000 | 2489.000000 | 51.000000 | 0.024902 | 0.038086 | 0.035058 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |
| 2801.000000 | 41011.000000 | exposure_matched_local | 2048.000000 | 2326.000000 | 50.000000 | 0.024414 | 0.043945 | 0.027834 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |
| 2801.000000 | 41047.000000 | current_global | 2048.000000 | 2340.000000 | 60.000000 | 0.029297 | 0.033691 | 0.035194 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |
| 2801.000000 | 41047.000000 | exposure_matched_local | 2048.000000 | 2234.000000 | 64.000000 | 0.031250 | 0.031250 | 0.033247 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |
| 2801.000000 | 41081.000000 | current_global | 2048.000000 | 2352.000000 | 49.000000 | 0.023926 | 0.040039 | 0.027911 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |
| 2801.000000 | 41081.000000 | exposure_matched_local | 2048.000000 | 2358.000000 | 50.000000 | 0.024414 | 0.043945 | 0.027417 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |
| 2903.000000 | 41011.000000 | current_global | 2048.000000 | 2356.000000 | 45.000000 | 0.021973 | 0.040039 | 0.033241 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |
| 2903.000000 | 41011.000000 | exposure_matched_local | 2048.000000 | 2261.000000 | 52.000000 | 0.025391 | 0.037598 | 0.023342 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |
| 2903.000000 | 41047.000000 | current_global | 2048.000000 | 2234.000000 | 41.000000 | 0.020020 | 0.040039 | 0.019975 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |
| 2903.000000 | 41047.000000 | exposure_matched_local | 2048.000000 | 2400.000000 | 41.000000 | 0.020020 | 0.042969 | 0.028772 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |
| 2903.000000 | 41081.000000 | current_global | 2048.000000 | 2286.000000 | 41.000000 | 0.020020 | 0.044434 | 0.020722 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |
| 2903.000000 | 41081.000000 | exposure_matched_local | 2048.000000 | 2295.000000 | 42.000000 | 0.020508 | 0.048828 | 0.023432 | 0.000000 | 1.000000 | 128.000000 | 0.000000 |

## Scheduler summaries

| arm | n_runs | total_events | total_dependency_edges | median_causal_depth_fraction | cv_causal_depth_fraction | median_max_layer_width_fraction | cv_max_layer_width_fraction | median_comparable_pair_fraction | cv_comparable_pair_fraction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| current_global | 6.000000 | 12288.000000 | 14057.000000 | 0.022949 | 0.150996 | 0.040039 | 0.088588 | 0.030576 | 0.243352 |
| exposure_matched_local | 6.000000 | 12288.000000 | 13874.000000 | 0.024414 | 0.166648 | 0.043457 | 0.148061 | 0.027626 | 0.135330 |

## Fresh-base stability

| metric | growth_2801_median | growth_2903_median | second_over_first_ratio | growth_stability_pass |
| --- | --- | --- | --- | --- |
| causal_depth_fraction | 0.024414 | 0.020508 | 0.840000 | 1.000000 |
| max_layer_width_fraction | 0.043945 | 0.042969 | 0.977778 | 1.000000 |
| comparable_pair_fraction | 0.027834 | 0.023432 | 0.841835 | 1.000000 |

## Scheduler coarse fingerprint

| metric | current_global_median | local_median | local_over_global_ratio | scheduler_metric_pass | nonseed_event_tv | nonseed_tv_pass |
| --- | --- | --- | --- | --- | --- | --- |
| causal_depth_fraction | 0.022949 | 0.024414 | 1.063830 | 1.000000 | 0.001572 | 1.000000 |
| max_layer_width_fraction | 0.040039 | 0.043457 | 1.085366 | 1.000000 | 0.001572 | 1.000000 |
| comparable_pair_fraction | 0.030576 | 0.027626 | 0.903512 | 1.000000 | 0.001572 | 1.000000 |

## Gate evaluation

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| v16ac_source_contract | pass | 1.000000 | 1.000000 | continue |
| target_hygiene | pass | 1.000000 | 1.000000 | continue |
| run_integrity | pass | runs=12;invalid=0 | runs=12;invalid=0 | continue |
| dag_acyclic_witnessed | pass | runs=12;witness_errors=0 | runs=12;witness_errors=0 | continue |
| topological_replay_invariance | pass | replays=48;failures=0;min_reorder=0.995605 | replays=48;failures=0;min_reorder>=0.1 | continue |
| concrete_relabel_replay | pass | 12.000000 | 12.000000 | continue |
| adjacent_disjoint_commutation | pass | min_tests=128;failures=0 | min_tests>=64;failures=0 | continue |
| nontrivial_partial_order | pass | depth=41-64;width_fraction=0.031250-0.048828 | 1<depth<steps;nonzero antichain and comparability | continue |
| local_dag_metric_cv | pass | causal_depth_fraction=0.166648;max_layer_width_fraction=0.148061;comparable_pair_fraction=0.135330 | each<=0.35 | continue |
| growth_seed_transfer | pass | causal_depth_fraction=0.840000;max_layer_width_fraction=0.977778;comparable_pair_fraction=0.841835 | each in [0.6,1.67] | continue |
| scheduler_coarse_fingerprint | pass | causal_depth_fraction=1.063830;max_layer_width_fraction=1.085366;comparable_pair_fraction=0.903512;tv=0.001572 | ratios in [0.6,1.67];tv<=0.05 | continue |
| v16b_overall | pass_to_v16c_coarse_graining_pilot | 1.000000 | 1.000000 | design_v16c_three_scale_pilot |

Overall status: `pass_to_v16c_coarse_graining_pilot`.

## Interpretation

A topological replay pass would show that the declared dependency structure is operationally sufficient for the sampled histories: many sequential orders are representational choices rather than different outcomes. Relabel replay would show that this structure does not depend on node names.

Even a full pass remains modest. The DAG is history-intrinsic under the current event vocabulary and support declaration. It is not yet an observer-independent continuum causal order, and stable normalized DAG summaries are not Lorentz symmetry.

## Next decision

Proceed to one small three-scale v16c pilot. Freeze a coarse-graining map before dynamics and test whether causal-depth, antichain-width, and dependency-density ratios transfer across scales. Keep the local adapter isolated and retain current-global as a diagnostic control.
