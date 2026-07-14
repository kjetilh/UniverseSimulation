# v16k fresh strict-null replication

Status: `v16k_instrumentation_failed`.

## Frozen question

Does the v16j finite event-DAG interval-spectrum contrast replicate on twelve fresh arm-specific runs when the observable, primary strict perturbation family, and existence thresholds are unchanged? Magnitude compatibility is reported separately and cannot change the existence result.

Specification digest: `3cba919f951c580ce3851c4294294d723bafb63053c1a67fe25112b9b6d61f14`.

The formal growth seeds were deterministically derived as 8036, 6132. Adviser-transient seeds 5203 and 5389 were quarantined and were not used.

## Primary results

| growth_seed | run_offset | arm | observed_js_to_null_center | null_median_leave_one_out_js | js_effect_ratio | empirical_p_upper | tail_mass_ge_8_delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 8036.000000 | 96729.000000 | current_global | 0.002883 | 0.000256 | 11.274753 | 0.030303 | -0.045757 |
| 8036.000000 | 96729.000000 | exposure_matched_local | 0.006056 | 0.000361 | 16.792664 | 0.030303 | -0.062941 |
| 8036.000000 | 92980.000000 | current_global | 0.004573 | 0.000529 | 8.650976 | 0.030303 | -0.052988 |
| 8036.000000 | 92980.000000 | exposure_matched_local | 0.002916 | 0.000336 | 8.667017 | 0.030303 | -0.041671 |
| 8036.000000 | 91663.000000 | current_global | 0.005150 | 0.000334 | 15.417067 | 0.030303 | -0.050534 |
| 8036.000000 | 91663.000000 | exposure_matched_local | 0.007745 | 0.000671 | 11.541961 | 0.030303 | -0.058600 |
| 6132.000000 | 96729.000000 | current_global | 0.001504 | 0.000350 | 4.300979 | 0.060606 | -0.021195 |
| 6132.000000 | 96729.000000 | exposure_matched_local | 0.001244 | 0.000213 | 5.832132 | 0.030303 | -0.022182 |
| 6132.000000 | 92980.000000 | current_global | 0.009130 | 0.000466 | 19.586443 | 0.030303 | -0.061580 |
| 6132.000000 | 92980.000000 | exposure_matched_local | 0.001540 | 0.000470 | 3.275483 | 0.030303 | -0.026623 |
| 6132.000000 | 91663.000000 | current_global | 0.005651 | 0.000400 | 14.112097 | 0.030303 | -0.035340 |
| 6132.000000 | 91663.000000 | exposure_matched_local | 0.004236 | 0.000497 | 8.518326 | 0.030303 | -0.046423 |

## Separate outcomes

| n_runs | median_js_effect_ratio | positive_fraction | p_le_010_fraction | local_gate_pass |
| --- | --- | --- | --- | --- |
| 6.000000 | 8.592671 | 1.000000 | 1.000000 | 1.000000 |

| n_runs | target_swap_multiplier | median_js_effect_ratio | positive_fraction | perturbation_integrity_pass | longer_perturbation_consistency_pass |
| --- | --- | --- | --- | --- | --- |
| 6.000000 | 0.100000 | 8.768244 | 1.000000 | 0.000000 | 0.000000 |

| fresh_median_js_effect_ratio | bootstrap_median_ci_low | bootstrap_median_ci_high | fresh_over_v16d | fresh_over_v16h | magnitude_compatibility_class |
| --- | --- | --- | --- | --- | --- |
| 8.592671 | 4.553808 | 14.167312 | 0.506036 | 1.077451 | compatible_with_both_prior_anchors |

Growth and scheduler rows are diagnostics, not additional primary endpoints.

| group_field | group_value | n_runs | median_js_effect_ratio | positive_fraction | group_pass |
| --- | --- | --- | --- | --- | --- |
| growth_seed | 6132.000000 | 6.000000 | 7.175229 | 1.000000 | 1.000000 |
| growth_seed | 8036.000000 | 6.000000 | 11.408357 | 1.000000 | 1.000000 |

| group_field | group_value | n_runs | median_js_effect_ratio | positive_fraction | group_pass |
| --- | --- | --- | --- | --- | --- |
| arm | current_global | 6.000000 | 12.693425 | 1.000000 | 1.000000 |
| arm | exposure_matched_local | 6.000000 | 8.592671 | 1.000000 | 1.000000 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| target_hygiene | pass | 1536.000000 | 1536.000000 | continue |
| fresh_history_integrity | pass | runs=12;events=36864 | runs=12;events=36864 | continue |
| replay_relabel_rate_parity | pass | replay=1;relabel=1;rate=1 | 1;1;1 | continue |
| primary_perturbation_integrity | fail | passes=383/384 | 384/384 | inconclusive |
| fresh_effect_existence | pass | median=8.592671;positive=1.000000;p_le_010=1.000000 | median>=2;positive>=5/6;p_le_010>=1/2 | replicated_primary |
| longer_perturbation_integrity | fail | passes=160/192 | 192/192 | inconclusive |
| longer_perturbation_consistency | fail | median=8.768244;positive=1.000000 | median>=1;positive>=5/6 | inconclusive |
| magnitude_compatibility | descriptive | compatible_with_both_prior_anchors | not_a_confirmatory_gate | compatible_with_both_prior_anchors |
| v16k_overall | v16k_instrumentation_failed | instrumentation=0;existence=1;longer=0 | 1;1;1 | v16k_instrumentation_failed |

## Interpretation boundary

The primary null preserves scheduler order, exact direct in/out-degree, exact causal-depth sequence/profile, and the global dyadic parent-age-bin histogram. Its independently seeded short swap perturbations are audited for preservation, minimum perturbation, and uniqueness. These checks do not establish convergence, stationarity, independence, representativeness, or approximate uniform sampling over the constrained DAG space.

All v16j strict-null tail-mass deltas, and the v16k values reported above, must be read by sign. The primary finding is a full-spectrum contrast; it is not automatically an increase in large intervals.

Causal-set interval-abundance work derives dimension relevance by comparison with analytic expectations for Poisson-sprinkled Alexandrov intervals. v16k performs no such comparison. It therefore does not establish dimension, manifoldlikeness, Lorentz invariance, spacetime, continuum behavior, particles, entanglement, or a physical causal law.
