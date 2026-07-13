# UniverseSimulation v16e: independent clock-slab coarse-map gate

## Research question

Does an independently defined, relabel-invariant simulation-clock coarse map expose dependency clustering that survives fresh holdout and exceeds both equal-event-count and shuffled-waiting-time controls?

## Evidential separation

- Discovery artifact: old v16c/v16d histories selected nondegenerate resolutions and a negative edge-retention direction before fresh dynamics.
- Frozen candidate: equal intervals of normalized simulation time at 128, 64, and 32 bins; no causal depth enters the assignment.
- Controls: equal-event-count slabs and 32 deterministic shuffled-waiting-time maps per run and resolution.
- Primary observable: clock quotient edge retention minus control edge retention. Lower values mean more direct dependencies are internalized by actual clock slabs.
- Actual dynamics: twelve fresh target-1536 histories were generated after design selection and preregistration.
- Negative boundary: the simulation clock is not assumed to be proper time or a physical metric.

## Source contract

| check | observed | required | status |
| --- | --- | --- | --- |
| v16d_overall | pass_to_v16e_independent_coarse_map_gate | pass_to_v16e_independent_coarse_map_gate | pass |
| v16d_all_subgates | 0.000000 | 0.000000 | pass |
| v16d_preregistration_reverified | verified | verified | pass |
| v16d_source_script_sha256 | 3828155a391cb3dc4ac39e055a47f61cdc0da873077d5c59a0f561dbd4df6503 | frozen into v16e preregistration | pass |
| clock_design_selection | 6ba19c245110e66c132758e76c7179416257bfb4648703bd67f259e9803befa3 | verified selected bins and direction | pass |

## Fresh design

Target `1536`, growth seeds `3701/3803`, offsets `71003/71047/71089`, `3072` events, two scheduler arms, selected bins `(128, 64, 32)`, and `32` waiting-time shuffles per run and resolution.

Target hygiene:

| target_nodes | growth_replicates | mean_initial_nodes | mean_initial_tokens | mean_initial_beta1 |
| --- | --- | --- | --- | --- |
| 1536.000000 | 2.000000 | 1536.000000 | 25.000000 | 195.500000 |

## Fine-history controls

| growth_seed | run_offset | arm | n_events | fine_edges | fine_causal_depth | topological_replay_failures | relabel_pass | clock_map_transport_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3701.000000 | 71003.000000 | current_global | 3072.000000 | 3601.000000 | 68.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3701.000000 | 71003.000000 | exposure_matched_local | 3072.000000 | 3693.000000 | 56.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3701.000000 | 71047.000000 | current_global | 3072.000000 | 3614.000000 | 57.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3701.000000 | 71047.000000 | exposure_matched_local | 3072.000000 | 3611.000000 | 50.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3701.000000 | 71089.000000 | current_global | 3072.000000 | 3677.000000 | 58.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3701.000000 | 71089.000000 | exposure_matched_local | 3072.000000 | 3487.000000 | 53.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3803.000000 | 71003.000000 | current_global | 3072.000000 | 3471.000000 | 54.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3803.000000 | 71003.000000 | exposure_matched_local | 3072.000000 | 3403.000000 | 53.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3803.000000 | 71047.000000 | current_global | 3072.000000 | 3423.000000 | 52.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3803.000000 | 71047.000000 | exposure_matched_local | 3072.000000 | 3401.000000 | 58.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3803.000000 | 71089.000000 | current_global | 3072.000000 | 3604.000000 | 51.000000 | 0.000000 | 1.000000 | 1.000000 |
| 3803.000000 | 71089.000000 | exposure_matched_local | 3072.000000 | 3573.000000 | 54.000000 | 0.000000 | 1.000000 | 1.000000 |

## Fresh run-level null effects

| growth_seed | run_offset | arm | requested_bins | clock_edge_retention | event_count_edge_retention | shuffle_mean_edge_retention | clock_minus_shuffle_mean | clock_null_z | clock_minus_event_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3701.000000 | 71003.000000 | current_global | 128.000000 | 0.339072 | 0.409886 | 0.401338 | -0.062266 | -15.647234 | -0.070814 |
| 3701.000000 | 71003.000000 | current_global | 64.000000 | 0.158845 | 0.191336 | 0.190260 | -0.031415 | -10.755337 | -0.032491 |
| 3701.000000 | 71003.000000 | current_global | 32.000000 | 0.068870 | 0.083866 | 0.081609 | -0.012740 | -8.622503 | -0.014996 |
| 3701.000000 | 71003.000000 | exposure_matched_local | 128.000000 | 0.350122 | 0.404820 | 0.399734 | -0.049612 | -13.115720 | -0.054698 |
| 3701.000000 | 71003.000000 | exposure_matched_local | 64.000000 | 0.163553 | 0.188735 | 0.188109 | -0.024557 | -13.033349 | -0.025183 |
| 3701.000000 | 71003.000000 | exposure_matched_local | 32.000000 | 0.074194 | 0.083130 | 0.081582 | -0.007387 | -5.342118 | -0.008936 |
| 3701.000000 | 71047.000000 | current_global | 128.000000 | 0.358329 | 0.413116 | 0.401425 | -0.043096 | -11.054272 | -0.054787 |
| 3701.000000 | 71047.000000 | current_global | 64.000000 | 0.167128 | 0.190647 | 0.190241 | -0.023113 | -8.554210 | -0.023520 |
| 3701.000000 | 71047.000000 | current_global | 32.000000 | 0.071112 | 0.081627 | 0.080252 | -0.009140 | -5.604080 | -0.010515 |
| 3701.000000 | 71047.000000 | exposure_matched_local | 128.000000 | 0.363611 | 0.425090 | 0.416626 | -0.053015 | -14.922547 | -0.061479 |
| 3701.000000 | 71047.000000 | exposure_matched_local | 64.000000 | 0.174744 | 0.197729 | 0.197314 | -0.022570 | -12.016519 | -0.022985 |
| 3701.000000 | 71047.000000 | exposure_matched_local | 32.000000 | 0.079202 | 0.084741 | 0.085485 | -0.006283 | -3.838648 | -0.005539 |
| 3701.000000 | 71089.000000 | current_global | 128.000000 | 0.365787 | 0.420995 | 0.411953 | -0.046165 | -13.883936 | -0.055208 |
| 3701.000000 | 71089.000000 | current_global | 64.000000 | 0.172695 | 0.197172 | 0.199424 | -0.026729 | -13.799410 | -0.024476 |
| 3701.000000 | 71089.000000 | current_global | 32.000000 | 0.076421 | 0.084036 | 0.085132 | -0.008711 | -7.584107 | -0.007615 |
| 3701.000000 | 71089.000000 | exposure_matched_local | 128.000000 | 0.340694 | 0.408087 | 0.398023 | -0.057329 | -14.869892 | -0.067393 |
| 3701.000000 | 71089.000000 | exposure_matched_local | 64.000000 | 0.155148 | 0.185546 | 0.182795 | -0.027647 | -11.106463 | -0.030399 |
| 3701.000000 | 71089.000000 | exposure_matched_local | 32.000000 | 0.064525 | 0.075710 | 0.075432 | -0.010907 | -6.458379 | -0.011184 |
| 3803.000000 | 71003.000000 | current_global | 128.000000 | 0.324114 | 0.405071 | 0.391818 | -0.067704 | -22.811338 | -0.080956 |
| 3803.000000 | 71003.000000 | current_global | 64.000000 | 0.143763 | 0.180351 | 0.176732 | -0.032970 | -13.291868 | -0.036589 |
| 3803.000000 | 71003.000000 | current_global | 32.000000 | 0.058773 | 0.072602 | 0.072755 | -0.013982 | -10.782844 | -0.013829 |
| 3803.000000 | 71003.000000 | exposure_matched_local | 128.000000 | 0.317073 | 0.413459 | 0.396892 | -0.079819 | -22.084487 | -0.096386 |
| 3803.000000 | 71003.000000 | exposure_matched_local | 64.000000 | 0.138701 | 0.181898 | 0.178152 | -0.039450 | -16.112911 | -0.043197 |
| 3803.000000 | 71003.000000 | exposure_matched_local | 32.000000 | 0.061123 | 0.071408 | 0.070903 | -0.009780 | -7.771900 | -0.010285 |
| 3803.000000 | 71047.000000 | current_global | 128.000000 | 0.317266 | 0.402571 | 0.387443 | -0.070178 | -17.672842 | -0.085305 |
| 3803.000000 | 71047.000000 | current_global | 64.000000 | 0.134677 | 0.173824 | 0.171231 | -0.036554 | -14.902171 | -0.039147 |
| 3803.000000 | 71047.000000 | current_global | 32.000000 | 0.055507 | 0.070406 | 0.068471 | -0.012964 | -9.785412 | -0.014899 |
| 3803.000000 | 71047.000000 | exposure_matched_local | 128.000000 | 0.332255 | 0.391944 | 0.381009 | -0.048754 | -15.625394 | -0.059688 |
| 3803.000000 | 71047.000000 | exposure_matched_local | 64.000000 | 0.139959 | 0.166716 | 0.164207 | -0.024248 | -13.071282 | -0.026757 |
| 3803.000000 | 71047.000000 | exposure_matched_local | 32.000000 | 0.058218 | 0.065863 | 0.066616 | -0.008398 | -8.013050 | -0.007645 |
| 3803.000000 | 71089.000000 | current_global | 128.000000 | 0.353219 | 0.433130 | 0.424407 | -0.071188 | -13.332311 | -0.079911 |
| 3803.000000 | 71089.000000 | current_global | 64.000000 | 0.162042 | 0.198946 | 0.197775 | -0.035733 | -18.479815 | -0.036903 |
| 3803.000000 | 71089.000000 | current_global | 32.000000 | 0.069367 | 0.081299 | 0.080865 | -0.011498 | -7.288995 | -0.011931 |
| 3803.000000 | 71089.000000 | exposure_matched_local | 128.000000 | 0.337252 | 0.414218 | 0.401457 | -0.064205 | -15.148160 | -0.076966 |
| 3803.000000 | 71089.000000 | exposure_matched_local | 64.000000 | 0.153093 | 0.190596 | 0.186249 | -0.033157 | -15.360589 | -0.037503 |
| 3803.000000 | 71089.000000 | exposure_matched_local | 32.000000 | 0.066611 | 0.079765 | 0.079363 | -0.012752 | -9.644386 | -0.013154 |

## Local primary gate

| requested_bins | median_clock_minus_shuffle | median_clock_minus_event_count | median_clock_null_z | negative_run_fraction | holdout_over_discovery_magnitude_ratio | local_effect_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 128.000000 | -0.055172 | -0.064436 | -15.035353 | 1.000000 | 1.017265 | 1.000000 |
| 64.000000 | -0.026102 | -0.028578 | -13.052315 | 1.000000 | 0.930480 | 1.000000 |
| 32.000000 | -0.009089 | -0.009610 | -7.115139 | 1.000000 | 0.744350 | 1.000000 |

## Growth-seed transfer

| requested_bins | growth_3701_median_abs_effect | growth_3803_median_abs_effect | second_over_first_magnitude_ratio | growth_effect_pass |
| --- | --- | --- | --- | --- |
| 128.000000 | 0.053015 | 0.064205 | 1.211080 | 1.000000 |
| 64.000000 | 0.024557 | 0.033157 | 1.350214 | 1.000000 |
| 32.000000 | 0.007387 | 0.009780 | 1.323893 | 1.000000 |

## Scheduler diagnostic

| requested_bins | current_global_median_abs_effect | local_median_abs_effect | local_over_global_magnitude_ratio | scheduler_effect_pass | nonseed_event_tv | nonseed_tv_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 128.000000 | 0.064985 | 0.055172 | 0.849000 | 1.000000 | 0.000976 | 1.000000 |
| 64.000000 | 0.032192 | 0.026102 | 0.810815 | 1.000000 | 0.000976 | 1.000000 |
| 32.000000 | 0.012119 | 0.009089 | 0.750015 | 1.000000 | 0.000976 | 1.000000 |

## Gate evaluation

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| v16d_source_contract | pass | 1.000000 | 1.000000 | continue |
| fresh_target_hygiene | pass | 1536.000000 | 1536.000000 | continue |
| fresh_run_integrity | pass | runs=12;invalid=0 | runs=12;invalid=0 | continue |
| fine_dag_integrity | pass | acyclic=12;witness_errors=0 | acyclic=12;witness_errors=0 | continue |
| fresh_topological_replay | pass | replays=24;min_reorder=0.996745;failures=0 | replays=24;failures=0 | continue |
| relabel_and_clock_map_transport | pass | 12.000000 | 12.000000 | continue |
| all_map_integrity | pass | passes=1224/1224 | 1224.000000 | continue |
| primary_control_bin_coverage | pass | 1.000000 | 1.000000 | continue |
| effect_row_integrity | pass | 36.000000 | 36.000000 | continue |
| local_clock_null_effect | pass | 128:-0.055172:z=-15.035:neg=1.000:ratio=1.017;64:-0.026102:z=-13.052:neg=1.000:ratio=0.930;32:-0.009089:z=-7.115:neg=1.000:ratio=0.744 | delta<=-0.005;count_delta<=-0.005;z<=-2.0;negative>=0.833;discovery_ratio in (0.5, 2.0) | continue |
| growth_effect_transfer | pass | 128=1.211080;64=1.350214;32=1.323893 | each in (0.6, 1.67) | continue |
| scheduler_effect_diagnostic | pass | 128=0.849000;64=0.810815;32=0.750015;tv=0.000976 | ratios in (0.6, 1.67);tv<=0.05 | continue |
| v16e_overall | pass_to_v16f_cross_map_relation_gate | 1.000000 | 1.000000 | design_cross_map_relation |

Overall status: `pass_to_v16f_cross_map_relation_gate`.

## Interpretation

The actual simulation clock groups direct dependencies more strongly than both chronological equal-count slabs and shuffled waiting-time clocks at all three frozen resolutions. The effect survives fresh seeds, discovery-to-holdout magnitude checks, and the scheduler diagnostic. This is a non-null independent coarse-map signal, but it is not yet evidence that the clock and causal-depth maps represent one common geometry.

The edge-retention statistic is not a Lorentz diagnostic. A waiting-time-aligned dependency cluster can arise from the stochastic scheduler and local rate structure without defining a metric, light cone, observer transformation, or continuum.

## Next decision

Preregister one v16f cross-map relation test: quantify whether clock slabs and causal-depth quotients align more than matched size/order nulls on the same fresh histories. Do not add a third map or increase target size first.
