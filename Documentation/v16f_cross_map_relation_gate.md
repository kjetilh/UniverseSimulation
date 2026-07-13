# UniverseSimulation v16f: clock/depth cross-map relation gate

## Research question

Are the independently validated simulation-clock and causal-depth partitions related beyond chronological, waiting-time, and exact-size/order controls?

## Evidential separation

- Design calibration: only old v16c/v16d histories determined the statistic, direction, controls, and thresholds.
- Frozen-data analysis holdout: v16e histories existed before v16f, but their clock/depth NMI relation was not used to choose the v16f design.
- Primary statistic: normalized mutual information between depth-window-16 components and clock bins 128/64/32.
- Controls: equal event counts, shuffled waiting times, and monotone slabs preserving the exact clock-bin size multiset.
- Secondary diagnostic: dependency-edge internalization phi; it is reported but does not gate the result.
- Negative boundary: lower relative NMI is not negative mutual information and is not proof of incompatible physical geometries.

## Execution hygiene

The first holdout invocation completed all 36 relation calculations but stopped before artifact writing because the transfer helper incorrectly expected six primary runs per growth seed instead of the preregistered three offsets. Only that coverage assertion was made dimension-aware (three per growth seed, six per scheduler arm); source data, statistics, controls, seeds, thresholds, and expected direction were unchanged. The complete frozen analysis was then rerun.

## Source contract

| check | observed | required | status |
| --- | --- | --- | --- |
| v16e_overall | pass_to_v16f_cross_map_relation_gate | pass_to_v16f_cross_map_relation_gate | pass |
| v16e_all_subgates | 0 | 0 | pass |
| v16e_preregistration_reverified | verified | verified | pass |
| v16f_design_selection | 832640b8c903d8b9e035281406d7cffe5faaa44cb7d300d68c0cf32fa197362e | verified old-data-only design | pass |
| source_hash_v16e_event_log.csv | 260bb00439d4abe8b6d61da9137df749c1cf9ef8a37c1875ea21214fc488fb20 | frozen into v16f preregistration | pass |
| source_hash_v16e_fine_dependency_edges.csv | d5f47212cd976198d9008acf2a846c5ddcf08f1f3c03dd5fa33b9509359f4550 | frozen into v16f preregistration | pass |
| source_hash_v16e_primary_control_membership.csv | 650bfc542e745deafde698c3e850ab15c69fab0a2f98a4daac1c331c2d4e1756 | frozen into v16f preregistration | pass |
| source_hash_v16e_run_summary.csv | 9f991bd118e45b121e7f93afba59cab399b30648eafb2aa31d2af305258d8821 | frozen into v16f preregistration | pass |
| source_hash_v16e_scheduler_effect_transfer.csv | 57c0f66976bded9a4a4f4ee55ad4d52e22cd00b406754e6f984a626301f0cba3 | frozen into v16f preregistration | pass |

## Run-level primary relation

| growth_seed | run_offset | arm | clock_bins | depth_components | observed_nmi | nmi_minus_waiting_null | nmi_minus_size_order_null | nmi_minus_event_count | waiting_null_z | size_order_null_z |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3701 | 71003 | current_global | 128 | 183 | 0.368529 | -0.016542 | -0.008739 | -0.017503 | -12.870685 | -4.767614 |
| 3701 | 71003 | current_global | 64 | 183 | 0.318860 | -0.013313 | -0.010100 | -0.013275 | -9.611759 | -4.519036 |
| 3701 | 71003 | current_global | 32 | 183 | 0.284891 | -0.010433 | -0.010229 | -0.008765 | -8.686717 | -3.152642 |
| 3701 | 71003 | exposure_matched_local | 128 | 154 | 0.362790 | -0.016958 | -0.010940 | -0.018273 | -13.714120 | -5.453726 |
| 3701 | 71003 | exposure_matched_local | 64 | 154 | 0.310045 | -0.015912 | -0.013670 | -0.016633 | -13.628975 | -5.767452 |
| 3701 | 71003 | exposure_matched_local | 32 | 154 | 0.276884 | -0.013086 | -0.013292 | -0.014740 | -8.856663 | -4.626901 |
| 3701 | 71047 | current_global | 128 | 172 | 0.376823 | -0.022174 | -0.015063 | -0.022754 | -15.141738 | -7.894856 |
| 3701 | 71047 | current_global | 64 | 172 | 0.324026 | -0.018938 | -0.016007 | -0.017986 | -12.830764 | -6.570291 |
| 3701 | 71047 | current_global | 32 | 172 | 0.288869 | -0.014939 | -0.014127 | -0.014840 | -8.646354 | -5.149414 |
| 3701 | 71047 | exposure_matched_local | 128 | 149 | 0.362381 | -0.015839 | -0.009379 | -0.018267 | -12.496519 | -5.934198 |
| 3701 | 71047 | exposure_matched_local | 64 | 149 | 0.308260 | -0.016777 | -0.013172 | -0.017908 | -12.140313 | -5.683908 |
| 3701 | 71047 | exposure_matched_local | 32 | 149 | 0.276118 | -0.009997 | -0.011602 | -0.009720 | -6.071336 | -3.892065 |
| 3701 | 71089 | current_global | 128 | 160 | 0.364293 | -0.017131 | -0.011484 | -0.019508 | -12.160286 | -6.838378 |
| 3701 | 71089 | current_global | 64 | 160 | 0.317810 | -0.015831 | -0.012972 | -0.016168 | -11.998158 | -6.356269 |
| 3701 | 71089 | current_global | 32 | 160 | 0.287034 | -0.014130 | -0.014766 | -0.012991 | -10.358456 | -5.556118 |
| 3701 | 71089 | exposure_matched_local | 128 | 160 | 0.362784 | -0.020120 | -0.012316 | -0.021963 | -16.023760 | -5.912122 |
| 3701 | 71089 | exposure_matched_local | 64 | 160 | 0.308592 | -0.016087 | -0.012736 | -0.015776 | -12.889460 | -5.689116 |
| 3701 | 71089 | exposure_matched_local | 32 | 160 | 0.270911 | -0.014211 | -0.015026 | -0.013325 | -10.225274 | -4.468279 |
| 3803 | 71003 | current_global | 128 | 182 | 0.382891 | -0.018694 | -0.009155 | -0.020191 | -15.428269 | -5.745915 |
| 3803 | 71003 | current_global | 64 | 182 | 0.323279 | -0.017652 | -0.013043 | -0.018146 | -13.099777 | -5.686686 |
| 3803 | 71003 | current_global | 32 | 182 | 0.284376 | -0.012769 | -0.012313 | -0.013412 | -9.153268 | -3.646402 |
| 3803 | 71003 | exposure_matched_local | 128 | 179 | 0.377968 | -0.024822 | -0.014375 | -0.028586 | -20.033486 | -7.933443 |
| 3803 | 71003 | exposure_matched_local | 64 | 179 | 0.322266 | -0.023395 | -0.018576 | -0.025741 | -16.595525 | -6.041071 |
| 3803 | 71003 | exposure_matched_local | 32 | 179 | 0.286154 | -0.018214 | -0.017982 | -0.018491 | -11.992166 | -4.877569 |
| 3803 | 71047 | current_global | 128 | 177 | 0.375305 | -0.022076 | -0.011636 | -0.025962 | -15.697705 | -5.052014 |
| 3803 | 71047 | current_global | 64 | 177 | 0.319491 | -0.021729 | -0.017374 | -0.022896 | -16.304175 | -6.666494 |
| 3803 | 71047 | current_global | 32 | 177 | 0.284330 | -0.016772 | -0.017631 | -0.018394 | -13.696702 | -4.299832 |
| 3803 | 71047 | exposure_matched_local | 128 | 178 | 0.378909 | -0.017775 | -0.011875 | -0.021081 | -12.635323 | -6.321713 |
| 3803 | 71047 | exposure_matched_local | 64 | 178 | 0.322016 | -0.018471 | -0.014983 | -0.017504 | -14.522758 | -7.220881 |
| 3803 | 71047 | exposure_matched_local | 32 | 178 | 0.284199 | -0.016461 | -0.015851 | -0.016486 | -11.322443 | -6.714322 |
| 3803 | 71089 | current_global | 128 | 188 | 0.365453 | -0.022956 | -0.013405 | -0.025480 | -16.079714 | -6.642171 |
| 3803 | 71089 | current_global | 64 | 188 | 0.309760 | -0.023493 | -0.017112 | -0.024477 | -15.648288 | -5.281462 |
| 3803 | 71089 | current_global | 32 | 188 | 0.272162 | -0.020904 | -0.019724 | -0.020924 | -15.953974 | -5.435023 |
| 3803 | 71089 | exposure_matched_local | 128 | 155 | 0.357880 | -0.019120 | -0.011119 | -0.019805 | -15.038203 | -5.396918 |
| 3803 | 71089 | exposure_matched_local | 64 | 155 | 0.308802 | -0.016299 | -0.011885 | -0.015651 | -10.841739 | -4.760607 |
| 3803 | 71089 | exposure_matched_local | 32 | 155 | 0.276683 | -0.011692 | -0.010653 | -0.011608 | -8.922842 | -3.528764 |

## Local primary gate

| clock_bins | median_nmi_minus_waiting_null | median_nmi_minus_size_order_null | median_nmi_minus_event_count | median_waiting_null_z | median_size_order_null_z | negative_run_fraction | local_relation_pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 128 | -0.018448 | -0.011497 | -0.020443 | -14.376161 | -5.923160 | 1.000000 | 1 |
| 64 | -0.016538 | -0.013421 | -0.017068 | -13.259218 | -5.728284 | 1.000000 | 1 |
| 32 | -0.013648 | -0.014159 | -0.014033 | -9.574058 | -4.547590 | 1.000000 | 1 |

## Growth transfer

| clock_bins | first_value | second_value | waiting_magnitude_ratio | size_magnitude_ratio | count_magnitude_ratio | transfer_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | 3701 | 3803 | 1.127541 | 1.085418 | 1.153687 | 1 |
| 64 | 3701 | 3803 | 1.148192 | 1.137512 | 1.052330 | 1 |
| 32 | 3701 | 3803 | 1.257933 | 1.192519 | 1.237178 | 1 |

## Scheduler diagnostic

| clock_bins | first_value | second_value | waiting_magnitude_ratio | size_magnitude_ratio | count_magnitude_ratio | transfer_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 128 | current_global | exposure_matched_local | 0.904964 | 0.994545 | 0.952077 | 1 |
| 64 | current_global | exposure_matched_local | 0.903951 | 0.923972 | 0.944796 | 1 |
| 32 | current_global | exposure_matched_local | 0.939054 | 0.980094 | 0.993368 | 1 |

## Edge internalization diagnostic

| growth_seed | run_offset | clock_bins | depth_internal_edge_fraction | clock_internal_edge_fraction | observed_edge_phi | edge_phi_minus_waiting_null | edge_phi_minus_size_order_null | diagnostic_only |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3701 | 71003 | 128 | 0.873003 | 0.114541 | 0.050356 | -0.004583 | -0.013620 | 1 |
| 3701 | 71003 | 64 | 0.873003 | 0.206066 | 0.081719 | -0.001296 | -0.014995 | 1 |
| 3701 | 71003 | 32 | 0.873003 | 0.359599 | 0.136677 | 0.008253 | -0.001580 | 1 |
| 3701 | 71047 | 128 | 0.882304 | 0.119358 | 0.076146 | -0.003111 | -0.010864 | 1 |
| 3701 | 71047 | 64 | 0.882304 | 0.205483 | 0.094285 | -0.016346 | -0.024827 | 1 |
| 3701 | 71047 | 32 | 0.882304 | 0.360011 | 0.155769 | 0.008624 | -0.001682 | 1 |
| 3701 | 71089 | 128 | 0.896473 | 0.127043 | 0.047666 | -0.003355 | -0.012487 | 1 |
| 3701 | 71089 | 64 | 0.896473 | 0.224548 | 0.065561 | -0.007048 | -0.018333 | 1 |
| 3701 | 71089 | 32 | 0.896473 | 0.379983 | 0.103125 | -0.006957 | -0.015940 | 1 |
| 3803 | 71003 | 128 | 0.912430 | 0.119600 | 0.037294 | -0.015324 | -0.020362 | 1 |
| 3803 | 71003 | 64 | 0.912430 | 0.225977 | 0.062991 | -0.004374 | -0.014986 | 1 |
| 3803 | 71003 | 32 | 0.912430 | 0.392595 | 0.076625 | -0.019609 | -0.026821 | 1 |
| 3803 | 71047 | 128 | 0.910320 | 0.123199 | 0.029982 | -0.014368 | -0.021687 | 1 |
| 3803 | 71047 | 64 | 0.910320 | 0.231991 | 0.067671 | 0.006286 | -0.001201 | 1 |
| 3803 | 71047 | 32 | 0.910320 | 0.395766 | 0.066728 | -0.021678 | -0.018747 | 1 |
| 3803 | 71089 | 128 | 0.885530 | 0.119228 | 0.061752 | -0.023740 | -0.030760 | 1 |
| 3803 | 71089 | 64 | 0.885530 | 0.225581 | 0.101506 | -0.004738 | -0.009198 | 1 |
| 3803 | 71089 | 32 | 0.885530 | 0.382872 | 0.147559 | 0.015945 | 0.004954 | 1 |

## Gate evaluation

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| v16e_source_contract | pass | 1 | 1 | continue |
| v16f_preregistration | pass | 1 | 1 | continue |
| depth16_map_integrity | pass | passes=12/12 | 12 | continue |
| relation_row_integrity | pass | 36 | 36 | continue |
| null_row_integrity | pass | 4608 | 4608 | continue |
| local_relative_anti_alignment | pass | 128:-0.018448/-0.011497/-0.020443;64:-0.016538/-0.013421/-0.017068;32:-0.013648/-0.014159/-0.014033 | all medians<=-0.005;null_z<=-2.0;negative>=0.833 | continue |
| growth_relation_transfer | pass | 128:1.128/1.085/1.154;64:1.148/1.138/1.052;32:1.258/1.193/1.237 | each in (0.6, 1.67) | continue |
| scheduler_relation_diagnostic | pass | 128:0.905/0.995/0.952;64:0.904/0.924/0.945;32:0.939/0.980/0.993 | each in (0.6, 1.67) | continue |
| v16f_overall | pass_to_v16g_clock_depth_boundary_mechanism_gate | 1 | 1 | test_boundary_mechanism |

Overall status: `pass_to_v16g_clock_depth_boundary_mechanism_gate`.

## Interpretation

The actual simulation-clock partition is systematically less similar to the depth-window-16 partition than all three chronological controls. The direction survives the frozen v16c-to-v16d calibration transfer, the v16e analysis holdout, both v16e growth seeds, and the scheduler diagnostic.

This is evidence for a repeatable relative cross-map relation, but it is evidence against immediately treating the two maps as interchangeable views of one common geometry. A scheduler/rate mechanism can produce the same pattern.

The NMI delta is not a Lorentz diagnostic and does not define a metric, observer transformation, light cone, proper time, or continuum.

## Next decision

If the frozen anti-alignment passes, preregister one v16g mechanism test asking whether event-family and local-rate conditioning explains where clock boundaries cut depth components. Do not add a third map or increase target size first.
