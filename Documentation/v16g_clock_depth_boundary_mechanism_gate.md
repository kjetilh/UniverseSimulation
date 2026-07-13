# v16g clock-depth boundary mechanism gate

Status: `pass_to_v16h_fresh_rate_logged_mechanism_holdout`.

## Question and evidential role

v16g asks whether the stable v16f clock/depth anti-alignment is produced by the simulator's pre-event scheduler-rate profile and event-family/local descriptor hazards. It is a frozen-data analysis holdout on v16e, not a fresh dynamical holdout.

## Design discipline

Only v16c/v16d were used for mechanism design. Their parsimonious total-rate-profile null already explained approximately the full old-data gap, while family and descriptor-hazard conditioning added little. Total rate was therefore frozen as primary before the v16e mechanism values were computed; richer conditioning remained secondary. The preregistration locks source hashes, assignments, null families, seeds, statistics, directions, and thresholds.

| stage | clock_bins | primary_null_family | median_rate_explained_fraction | median_family_rate_increment_over_rate | median_family_hazard_increment_over_rate | conditionally_nonsurprising_fraction | calibration_supports_primary_mechanism |
| --- | --- | --- | --- | --- | --- | --- | --- |
| v16c | 128.000000 | total_rate_profile | 0.991206 | 0.005150 | 0.008091 | 0.833333 | 1.000000 |
| v16c | 64.000000 | total_rate_profile | 0.987140 | -0.011097 | -0.008314 | 1.000000 | 1.000000 |
| v16c | 32.000000 | total_rate_profile | 0.943649 | -0.006208 | 0.014519 | 1.000000 | 1.000000 |
| v16d | 128.000000 | total_rate_profile | 1.033047 | -0.001692 | -0.007480 | 1.000000 | 1.000000 |
| v16d | 64.000000 | total_rate_profile | 1.061199 | 0.000017 | -0.003343 | 0.833333 | 1.000000 |
| v16d | 32.000000 | total_rate_profile | 1.044360 | -0.007952 | -0.013371 | 1.000000 | 1.000000 |

Frozen specification digest: `13db516eaceb203d141f3238c6000ede5d6345e8a69946dcdee94689b42f94d0`.

## Exact reconstruction

Rates are reconstructed before each stored event. The normalized residual is `dt * total_rate`; the concrete descriptor hazard is `selected_family_rate * descriptor_probability`. Every replay must reproduce descriptor support, event kind, allocated IDs, resources, direct dependency predecessors, causal depth, event counts, final census, and total simulation time.

## Conditional nulls

- `shuffled_waiting_time` destroys the eventwise waiting-time/rate pairing and is the v16f-style baseline.
- `total_rate_profile` shuffles unit-rate residuals globally and reconstructs each waiting time using its original pre-event total rate.
- `event_family_rate_profile` shuffles residuals only within event family.
- `family_descriptor_hazard_profile` additionally restricts shuffling to within-family rank-quantiles of concrete descriptor hazard.

The preregistered primary is `total_rate_profile`; family and descriptor-hazard conditioning are secondary incremental diagnostics. An explained fraction of `1` means the conditional-null mean reaches the observed NMI from the unconditional waiting-time-null mean. It does not mean that a physical law has been derived.

## Reconstruction audit

| growth_seed | run_offset | arm | source_events | total_errors | residual_mean | reconstruction_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 3701.000000 | 71003.000000 | current_global | 3072.000000 | 0.000000 | 0.954118 | 1.000000 |
| 3701.000000 | 71003.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 0.987678 | 1.000000 |
| 3701.000000 | 71047.000000 | current_global | 3072.000000 | 0.000000 | 0.966039 | 1.000000 |
| 3701.000000 | 71047.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 1.009077 | 1.000000 |
| 3701.000000 | 71089.000000 | current_global | 3072.000000 | 0.000000 | 0.997804 | 1.000000 |
| 3701.000000 | 71089.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 0.987082 | 1.000000 |
| 3803.000000 | 71003.000000 | current_global | 3072.000000 | 0.000000 | 0.987417 | 1.000000 |
| 3803.000000 | 71003.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 0.999928 | 1.000000 |
| 3803.000000 | 71047.000000 | current_global | 3072.000000 | 0.000000 | 0.994272 | 1.000000 |
| 3803.000000 | 71047.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 1.000490 | 1.000000 |
| 3803.000000 | 71089.000000 | current_global | 3072.000000 | 0.000000 | 1.016816 | 1.000000 |
| 3803.000000 | 71089.000000 | exposure_matched_local | 3072.000000 | 0.000000 | 0.965511 | 1.000000 |

## Primary local result

| clock_bins | n_runs | median_waiting_minus_observed_nmi | median_rate_explained_fraction | median_family_rate_increment_over_rate | median_family_hazard_increment_over_rate | conditionally_nonsurprising_fraction | local_mechanism_pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 128.000000 | 6.000000 | 0.018554 | 1.000673 | 0.004332 | 0.009140 | 1.000000 | 1.000000 |
| 64.000000 | 6.000000 | 0.016668 | 1.014511 | 0.002099 | 0.003843 | 1.000000 | 1.000000 |
| 32.000000 | 6.000000 | 0.013752 | 0.981891 | -0.003032 | -0.010176 | 0.833333 | 1.000000 |

Across the three primary resolutions, the total-rate profile explains median fractions `0.981891` to `1.014511` of the unconditional clock/depth gap. The median event-family increment ranges from `-0.003032` to `0.004332` and the descriptor-hazard increment from `-0.010176` to `0.009140`. The parsimonious result is therefore a total scheduler-rate mechanism; no separate family or concrete-hazard mechanism is supported by these secondary medians.

## Growth and scheduler diagnostics

| group_field | group_value | clock_bins | median_primary_explained_fraction | conditionally_nonsurprising_fraction | group_mechanism_pass |
| --- | --- | --- | --- | --- | --- |
| growth_seed | 3701.000000 | 128.000000 | 0.961864 | 1.000000 | 1.000000 |
| growth_seed | 3803.000000 | 128.000000 | 1.049045 | 1.000000 | 1.000000 |
| growth_seed | 3701.000000 | 64.000000 | 0.994998 | 1.000000 | 1.000000 |
| growth_seed | 3803.000000 | 64.000000 | 1.024529 | 1.000000 | 1.000000 |
| growth_seed | 3701.000000 | 32.000000 | 0.993871 | 0.833333 | 1.000000 |
| growth_seed | 3803.000000 | 32.000000 | 0.957230 | 0.833333 | 1.000000 |

| group_field | group_value | clock_bins | median_primary_explained_fraction | conditionally_nonsurprising_fraction | group_mechanism_pass |
| --- | --- | --- | --- | --- | --- |
| arm | current_global | 128.000000 | 1.024984 | 1.000000 | 1.000000 |
| arm | exposure_matched_local | 128.000000 | 1.000673 | 1.000000 | 1.000000 |
| arm | current_global | 64.000000 | 0.994998 | 1.000000 | 1.000000 |
| arm | exposure_matched_local | 64.000000 | 1.014511 | 1.000000 | 1.000000 |
| arm | current_global | 32.000000 | 0.969210 | 0.833333 | 1.000000 |
| arm | exposure_matched_local | 32.000000 | 0.981891 | 0.833333 | 1.000000 |

## Gate evaluation

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| exact_rate_reconstruction | pass | audits=12;failures=0 | 12 audits;failures=0 | continue |
| v16f_relation_reproduction | pass | positive_waiting_minus_observed=36/36 | 36/36 | continue |
| total_rate_profile_mechanism | pass | passing_bins=3/3 | 3/3 | fresh_holdout |
| growth_transfer | pass | passing_groups=6/6 | 6/6 | continue |
| scheduler_transfer | pass | passing_groups=6/6 | 6/6 | continue |
| v16g_overall | pass_to_v16h_fresh_rate_logged_mechanism_holdout | reconstruction=1;relation=1;local=1;growth=1;scheduler=1 | all five gates pass for fresh rate-logged holdout | pass_to_v16h_fresh_rate_logged_mechanism_holdout |

## Execution audit

| event | change | primary_gate_affected | secondary_transfer_gate_affected | design_changed | source_data_changed |
| --- | --- | --- | --- | --- | --- |
| pre_holdout_group_diagnostic_threshold_serialization_omission | documented_only_no_threshold_data_statistic_seed_or_result_change | 0.000000 | 1.000000 | 0.000000 | 0.000000 |

The `0.50` conditional-nonsurprise threshold used by the growth/scheduler diagnostics was present in the frozen code before holdout execution but omitted from the serialized spec-digest payload. No threshold, data, statistic, seed, or result was changed after opening v16e. The primary local gate is digest-locked; growth/scheduler transfer therefore has weaker manifest evidence and remains supportive rather than independently decisive.

## Interpretation limits

A pass identifies a finite simulator mechanism capable of accounting for the relative partition statistic and justifies one fresh rate-logged holdout. It weakens, rather than strengthens, any claim that the two maps are independent coordinates of one geometry: the cross-map relation is currently best understood as scheduler-rate-induced. A failure means the tested scheduler/rate mechanism is insufficient; it does not turn the maps into physical spacetime.

No result here establishes Lorentz symmetry, proper time, a spacetime metric, a continuum limit, particles, entanglement, or universal causal laws.
