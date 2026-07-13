# v16h fresh directly rate-logged mechanism holdout

Status: `total_rate_mechanism_validated_retire_clock_depth_common_geometry`.

## Evidential role

v16h is a fresh dynamical holdout of the v16g total-rate explanation. New growth seeds and run offsets were frozen before execution. Target, event density, scheduler arms, depth/clock maps, null families, statistics, directions, and thresholds were unchanged.

Specification digest: `0971020c6986a8419a07358620e121a0b2497b25815d078a188472b6444ed9fd`. Script and v16g source hashes are locked in `v16h_pre_registration.csv`.

## Direct-rate instrumentation

Each event logs all four pre-event family rates, selected family rate, descriptor probability, concrete descriptor hazard, and unit-rate residual before the state mutation. An independent replay reconstructs the same quantities from the event history and must match within the frozen tolerance.

| growth_seed | run_offset | arm | direct_rows | reconstruction_total_errors | max_abs_numeric_error | residual_mean | residual_sd | direct_log_parity_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4001.000000 | 81013.000000 | current_global | 3072.000000 | 0.000000 | 0.000000 | 1.032539 | 1.036675 | 1.000000 |
| 4001.000000 | 81013.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 0.000000 | 0.996494 | 1.000556 | 1.000000 |
| 4001.000000 | 81047.000000 | current_global | 3072.000000 | 0.000000 | 0.000000 | 0.999584 | 0.987079 | 1.000000 |
| 4001.000000 | 81047.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 0.000000 | 0.964935 | 0.943323 | 1.000000 |
| 4001.000000 | 81091.000000 | current_global | 3072.000000 | 0.000000 | 0.000000 | 0.993819 | 1.001951 | 1.000000 |
| 4001.000000 | 81091.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 0.000000 | 1.024779 | 1.030367 | 1.000000 |
| 4127.000000 | 81013.000000 | current_global | 3072.000000 | 0.000000 | 0.000000 | 1.010027 | 1.016534 | 1.000000 |
| 4127.000000 | 81013.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 0.000000 | 0.997317 | 0.984206 | 1.000000 |
| 4127.000000 | 81047.000000 | current_global | 3072.000000 | 0.000000 | 0.000000 | 1.021918 | 1.023006 | 1.000000 |
| 4127.000000 | 81047.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 0.000000 | 1.011632 | 1.028601 | 1.000000 |
| 4127.000000 | 81091.000000 | current_global | 3072.000000 | 0.000000 | 0.000000 | 1.013235 | 1.002597 | 1.000000 |
| 4127.000000 | 81091.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 0.000000 | 1.019594 | 1.013253 | 1.000000 |

## Fresh primary result

| clock_bins | n_runs | median_waiting_minus_observed_nmi | median_rate_explained_fraction | median_family_rate_increment_over_rate | median_family_hazard_increment_over_rate | conditionally_nonsurprising_fraction | local_mechanism_pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 128.000000 | 6.000000 | 0.023856 | 1.022118 | -0.007782 | -0.006216 | 1.000000 | 1.000000 |
| 64.000000 | 6.000000 | 0.022504 | 0.981567 | -0.000034 | -0.005787 | 1.000000 | 1.000000 |
| 32.000000 | 6.000000 | 0.016575 | 0.967823 | 0.003549 | 0.012267 | 0.833333 | 1.000000 |

## Frozen-baseline transfer

| clock_bins | v16g_median_waiting_minus_observed_nmi | v16h_median_waiting_minus_observed_nmi | v16h_over_v16g_gap_ratio | ratio_low | ratio_high | baseline_transfer_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 128.000000 | 0.018554 | 0.023856 | 1.285763 | 0.500000 | 2.000000 | 1.000000 |
| 64.000000 | 0.016668 | 0.022504 | 1.350161 | 0.500000 | 2.000000 | 1.000000 |
| 32.000000 | 0.013752 | 0.016575 | 1.205295 | 0.500000 | 2.000000 | 1.000000 |

## Growth and scheduler diagnostics

| group_field | group_value | clock_bins | median_rate_explained_fraction | conditionally_nonsurprising_fraction | group_mechanism_pass |
| --- | --- | --- | --- | --- | --- |
| growth_seed | 4001.000000 | 128.000000 | 0.960650 | 1.000000 | 1.000000 |
| growth_seed | 4127.000000 | 128.000000 | 0.983678 | 0.833333 | 1.000000 |
| growth_seed | 4001.000000 | 64.000000 | 0.946115 | 1.000000 | 1.000000 |
| growth_seed | 4127.000000 | 64.000000 | 0.958481 | 1.000000 | 1.000000 |
| growth_seed | 4001.000000 | 32.000000 | 0.934626 | 0.666667 | 1.000000 |
| growth_seed | 4127.000000 | 32.000000 | 0.945435 | 0.833333 | 1.000000 |

| group_field | group_value | clock_bins | median_rate_explained_fraction | conditionally_nonsurprising_fraction | group_mechanism_pass |
| --- | --- | --- | --- | --- | --- |
| arm | current_global | 128.000000 | 0.934036 | 0.833333 | 1.000000 |
| arm | exposure_matched_local | 128.000000 | 1.022118 | 1.000000 | 1.000000 |
| arm | current_global | 64.000000 | 0.927225 | 1.000000 | 1.000000 |
| arm | exposure_matched_local | 64.000000 | 0.981567 | 1.000000 | 1.000000 |
| arm | current_global | 32.000000 | 0.908610 | 0.666667 | 1.000000 |
| arm | exposure_matched_local | 32.000000 | 0.967823 | 0.833333 | 1.000000 |

## Gate evaluation

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| v16g_source_contract | pass | 1.000000 | 1.000000 | continue |
| fresh_target_hygiene | pass | 1536.000000 | 1536.000000 | continue |
| fresh_run_and_dag_integrity | pass | runs=12;invalid=0 | runs=12;invalid=0 | continue |
| topological_replay | pass | replays=24;failures=0 | replays=24;failures=0 | continue |
| relabel_and_depth_map | pass | relabel=12/12;maps=12/12 | 12/12;12/12 | continue |
| direct_rate_log_parity | pass | passes=12/12;max_error=0.000e+00 | 12/12;max_error<=1e-12 | continue |
| v16f_relation_fresh_reproduction | pass | positive_gap=36/36 | 36/36 | continue |
| fresh_total_rate_mechanism | pass | passing_bins=3/3 | 3/3 | retire_common_geometry |
| v16g_to_v16h_gap_transfer | pass | 128:1.285763;64:1.350161;32:1.205295 | each in [0.5,2.0] | continue |
| fresh_growth_transfer | pass | passing_groups=6/6 | 6/6 | continue |
| fresh_scheduler_transfer | pass | passing_groups=6/6 | 6/6 | continue |
| v16h_overall | total_rate_mechanism_validated_retire_clock_depth_common_geometry | instrumentation=1;mechanism=1 | instrumentation=1;mechanism=1 | total_rate_mechanism_validated_retire_clock_depth_common_geometry |

## Interpretation

A full pass validates a finite simulator mechanism: the varying pre-event total rate accounts for the previously stable clock/depth partition relation on fresh histories. It therefore closes the simple common-geometry synthesis rather than strengthening it. The depth map remains a valid architecture artifact and the clock map remains a scheduler-sensitive diagnostic, but their relation is not independent geometry evidence.

This does not establish physical time, Lorentz symmetry, metric spacetime, a continuum limit, particles, entanglement, or universal causal laws.
