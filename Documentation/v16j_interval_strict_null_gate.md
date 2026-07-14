# v16j causal-interval strict-null gate

Status: `causal_interval_abundance_not_supported_under_degree_age_null`.

## Question and freeze discipline

v16j asks whether the v16i causal-interval abundance signal survives a null that controls direct degree and coarse parent-age wiring. No new dynamics were generated. The null mechanics and unchanged v16i full-spectrum Jensen-Shannon statistic were calibrated on v16c/v16d, hash-frozen, and only then evaluated on v16h.

Specification digest: `f4bd9863ced6c5e6c8d297a25f751b4ad632e386977b3cfb34fa0ed2e62e5215`.

## Strict null

Directed double-edge swaps preserve event count, original scheduler order, every event's exact direct indegree and outdegree, every event's exact causal depth, the full depth-layer profile, and the global dyadic parent-age-bin histogram. Every replicate must accept swaps equal to at least 7.5% of the direct-edge count, change at least 10% of direct edges, and be unique within its run.

The null does not preserve exact parent age per edge, each child's age-bin multiset, event family, or read/write resource type. It therefore tests a specific mechanism alternative rather than every generator artifact.

## Holdout results

| growth_seed | run_offset | arm | observed_js_to_null_center | null_median_leave_one_out_js | js_effect_ratio | empirical_p_upper | min_changed_edge_fraction | tail_mass_ge_8_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4001.000000 | 81013.000000 | current_global | 0.005240 | 0.000333 | 15.733010 | 0.030303 | 0.101201 | -0.050567 |
| 4001.000000 | 81013.000000 | exposure_matched_local | 0.006366 | 0.000634 | 10.039759 | 0.030303 | 0.100000 | -0.060984 |
| 4001.000000 | 81047.000000 | current_global | 0.003802 | 0.000503 | 7.552210 | 0.030303 | 0.102694 | -0.031287 |
| 4001.000000 | 81047.000000 | exposure_matched_local | 0.003106 | 0.000504 | 6.157108 | 0.030303 | 0.100027 | -0.035266 |
| 4001.000000 | 81091.000000 | current_global | 0.004640 | 0.000424 | 10.936769 | 0.030303 | 0.100028 | -0.050850 |
| 4001.000000 | 81091.000000 | exposure_matched_local | 0.002832 | 0.000416 | 6.814271 | 0.030303 | 0.100444 | -0.038996 |
| 4127.000000 | 81013.000000 | current_global | 0.005554 | 0.000391 | 14.199345 | 0.030303 | 0.100221 | -0.047848 |
| 4127.000000 | 81013.000000 | exposure_matched_local | 0.006189 | 0.000804 | 7.700008 | 0.030303 | 0.100222 | -0.046151 |
| 4127.000000 | 81047.000000 | current_global | 0.002846 | 0.000220 | 12.945231 | 0.030303 | 0.100257 | -0.026435 |
| 4127.000000 | 81047.000000 | exposure_matched_local | 0.003148 | 0.000382 | 8.249993 | 0.030303 | 0.100230 | -0.044506 |
| 4127.000000 | 81091.000000 | current_global | 0.005570 | 0.000288 | 19.335860 | 0.030303 | 0.100000 | -0.034394 |
| 4127.000000 | 81091.000000 | exposure_matched_local | 0.008441 | 0.000681 | 12.388730 | 0.030303 | 0.100429 | -0.051844 |

## Gates

| n_runs | median_js_effect_ratio | positive_fraction | p_le_010_fraction | local_gate_pass |
| --- | --- | --- | --- | --- |
| 6.000000 | 7.975000 | 1.000000 | 1.000000 | 1.000000 |

| source_median_js_effect_ratio | holdout_median_js_effect_ratio | holdout_over_source_ratio | calibration_transfer_pass |
| --- | --- | --- | --- |
| 16.980351 | 7.975000 | 0.469661 | 0.000000 |

| group_field | group_value | n_runs | median_js_effect_ratio | positive_fraction | group_pass |
| --- | --- | --- | --- | --- | --- |
| growth_seed | 4001.000000 | 6.000000 | 8.795985 | 1.000000 | 1.000000 |
| growth_seed | 4127.000000 | 6.000000 | 12.666981 | 1.000000 | 1.000000 |

| group_field | group_value | n_runs | median_js_effect_ratio | positive_fraction | group_pass |
| --- | --- | --- | --- | --- | --- |
| arm | current_global | 6.000000 | 13.572288 | 1.000000 | 1.000000 |
| arm | exposure_matched_local | 6.000000 | 7.975000 | 1.000000 | 1.000000 |

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| v16h_source_contract | pass | 1.000000 | 1.000000 | continue |
| holdout_run_integrity | pass | runs=12;events=36864 | runs=12;events=36864 | continue |
| strict_null_integrity_and_mixing | pass | passes=384/384 | 384/384 | continue |
| local_strict_null_interval_abundance | pass | median_ratio=7.975000;positive=1.000000;p_le_010=1.000000 | median>=2.0;positive>=0.8333333333333334;p_le_010>=0.5 | continue |
| v16d_to_v16h_strict_null_transfer | fail | 0.469661 | in [0.5,2.0] | not_stable_across_seed_holdout |
| growth_seed_transfer | pass | passing_groups=2/2 | 2/2 | continue |
| scheduler_transfer | pass | passing_groups=2/2 | 2/2 | continue |
| v16j_overall | causal_interval_abundance_not_supported_under_degree_age_null | instrumentation=1;evidence=0 | instrumentation=1;evidence=1 | causal_interval_abundance_not_supported_under_degree_age_null |

## Interpretation boundary

A pass would support finite-poset interval structure beyond this degree/depth/coarse-age null. A fail with valid mixing would show that the earlier v16i contrast is not robust to this stricter mechanism control and is consistent with degree/age wiring. Neither outcome proves or disproves that a universe can emerge from local rules.

This gate does not establish dimension, manifoldlikeness, Lorentz invariance, physical time, particles, entanglement, continuum behavior, or universal geometry.
