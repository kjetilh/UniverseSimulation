# v16i causal-interval abundance gate

Status: `causal_interval_abundance_supported_beyond_layer_indegree_null`.

## Question and evidential role

v16i asks whether intrinsic event-DAG interval topology contains a repeatable signal beyond event count, scheduler order, the full causal-depth layer profile, and every event's indegree. It is an analysis holdout on existing v16h histories. No new dynamics were generated.

The full-spectrum Jensen-Shannon effect ratio was selected on v16c/v16d only and frozen before any v16h interval value was computed. Specification digest: `4abd9769b44ae7baee5e666f92d119435bc58e310b49d3c720ce04d4e705a184`.

## Observable and structural null

For every comparable event pair `(past, future)`, the open interval is the set of events causally after `past` and causally before `future`. Exact open-interval cardinalities are accumulated into the frozen dyadic bins `0, 1, 2-3, ..., 128+`.

The null rewires direct parents while preserving event count, original scheduler order, each event's indegree, each event's causal depth, and the complete depth-layer profile. It does not preserve outdegree, parent-age distribution, event family, or read/write resource type. A positive result is therefore narrower than a mechanism claim.

## Holdout run results

| growth_seed | run_offset | arm | comparable_pairs | observed_js_to_null_center | null_median_leave_one_out_js | js_effect_ratio | empirical_p_upper | tail_mass_ge_8_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4001.000000 | 81013.000000 | current_global | 123219.000000 | 0.003893 | 0.000938 | 4.151915 | 0.061538 | 0.052315 |
| 4001.000000 | 81013.000000 | exposure_matched_local | 159371.000000 | 0.007849 | 0.003441 | 2.280884 | 0.184615 | 0.060422 |
| 4001.000000 | 81047.000000 | current_global | 149622.000000 | 0.004933 | 0.001992 | 2.476525 | 0.076923 | 0.063052 |
| 4001.000000 | 81047.000000 | exposure_matched_local | 148803.000000 | 0.004266 | 0.001939 | 2.199930 | 0.061538 | 0.040044 |
| 4001.000000 | 81091.000000 | current_global | 103979.000000 | 0.004689 | 0.000349 | 13.424889 | 0.015385 | 0.055900 |
| 4001.000000 | 81091.000000 | exposure_matched_local | 128628.000000 | 0.010444 | 0.001313 | 7.956701 | 0.015385 | 0.081718 |
| 4127.000000 | 81013.000000 | current_global | 141900.000000 | 0.007172 | 0.001876 | 3.824199 | 0.030769 | 0.049142 |
| 4127.000000 | 81013.000000 | exposure_matched_local | 185254.000000 | 0.010794 | 0.001813 | 5.952965 | 0.030769 | 0.073280 |
| 4127.000000 | 81047.000000 | current_global | 142235.000000 | 0.004581 | 0.001802 | 2.541461 | 0.107692 | 0.025289 |
| 4127.000000 | 81047.000000 | exposure_matched_local | 131496.000000 | 0.001647 | 0.001049 | 1.570228 | 0.369231 | 0.008215 |
| 4127.000000 | 81091.000000 | current_global | 177662.000000 | 0.010525 | 0.001018 | 10.341566 | 0.015385 | 0.090708 |
| 4127.000000 | 81091.000000 | exposure_matched_local | 155670.000000 | 0.004539 | 0.002058 | 2.205564 | 0.107692 | 0.051141 |

## Primary and transfer gates

| n_runs | median_js_effect_ratio | positive_fraction | p_le_010_fraction | local_gate_pass |
| --- | --- | --- | --- | --- |
| 6.000000 | 2.243224 | 1.000000 | 0.500000 | 1.000000 |

| source_median_js_effect_ratio | holdout_median_js_effect_ratio | holdout_over_source_ratio | target_transfer_pass |
| --- | --- | --- | --- |
| 3.076413 | 2.243224 | 0.729169 | 1.000000 |

| group_field | group_value | n_runs | median_js_effect_ratio | positive_fraction | group_pass |
| --- | --- | --- | --- | --- | --- |
| growth_seed | 4001.000000 | 6.000000 | 3.314220 | 1.000000 | 1.000000 |
| growth_seed | 4127.000000 | 6.000000 | 3.182830 | 1.000000 | 1.000000 |

| group_field | group_value | n_runs | median_js_effect_ratio | positive_fraction | group_pass |
| --- | --- | --- | --- | --- | --- |
| arm | current_global | 6.000000 | 3.988057 | 1.000000 | 1.000000 |
| arm | exposure_matched_local | 6.000000 | 2.243224 | 1.000000 | 1.000000 |

## Gate evaluation

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| v16h_source_contract | pass | 1.000000 | 1.000000 | continue |
| holdout_run_integrity | pass | runs=12;events=36864 | runs=12;events=36864 | continue |
| layer_indegree_null_integrity | pass | passes=768/768 | 768/768 | continue |
| event_poset_isomorphism | pass | passes=24/24 | 24/24 | continue |
| local_interval_abundance | pass | median_ratio=2.243224;positive=1.000000;p_le_010=0.500000 | median>=2.0;positive>=0.8333333333333334;p_le_010>=0.5 | continue |
| v16d_to_v16h_target_transfer | pass | 0.729169 | in [0.5,2.0] | continue |
| growth_seed_transfer | pass | passing_groups=2/2 | 2/2 | continue |
| scheduler_transfer | pass | passing_groups=2/2 | 2/2 | continue |
| v16i_overall | causal_interval_abundance_supported_beyond_layer_indegree_null | instrumentation=1;evidence=1 | instrumentation=1;evidence=1 | causal_interval_abundance_supported_beyond_layer_indegree_null |

## Interpretation boundary

A pass supports a repeatable finite-poset interval-abundance structure not reduced to the frozen layer+indegree null. It does not establish a causal-set dimension, manifoldlikeness, Lorentz invariance, physical time, continuum behavior, particles, entanglement, or a spacetime geometry.

Before any stronger interpretation, the smallest next mechanism gate is a stricter null that also preserves direct in/out-degree and parent-age structure. Failure there would identify the present signal as a degree/age wiring artifact.
