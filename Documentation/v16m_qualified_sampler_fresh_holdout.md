# v16m qualified-sampler fresh holdout

Status: `fresh_strict_null_spectrum_contrast_replicated_with_qualified_sampler`.

v16m is a new 12-run holdout. It uses new histories and the v16l-qualified 240-attempt safety ceiling while retaining the v16j/v16k observable, null targets, null counts, stopping conditions, and scientific thresholds.

Specification digest: `569ac97666bbb75c0c8a1335a1b3b96d8c27bbfa4c8236a6184a24c9064e5677`.

## Per-run primary results

| growth_seed | run_offset | arm | observed_js_to_null_center | null_median_leave_one_out_js | js_effect_ratio | empirical_p_upper | tail_mass_ge_8_delta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5764.000000 | 106802.000000 | current_global | 0.003849 | 0.000395 | 9.753477 | 0.030303 | -0.047676 |
| 5764.000000 | 106802.000000 | exposure_matched_local | 0.000594 | 0.000237 | 2.502413 | 0.151515 | -0.011181 |
| 5764.000000 | 108688.000000 | current_global | 0.003290 | 0.000355 | 9.259514 | 0.030303 | -0.044278 |
| 5764.000000 | 108688.000000 | exposure_matched_local | 0.002447 | 0.000363 | 6.749754 | 0.030303 | -0.034732 |
| 5764.000000 | 100399.000000 | current_global | 0.002794 | 0.000464 | 6.021682 | 0.030303 | -0.029996 |
| 5764.000000 | 100399.000000 | exposure_matched_local | 0.005888 | 0.000511 | 11.523766 | 0.030303 | -0.057807 |
| 6681.000000 | 106802.000000 | current_global | 0.006155 | 0.000508 | 12.115116 | 0.030303 | -0.051731 |
| 6681.000000 | 106802.000000 | exposure_matched_local | 0.007649 | 0.000575 | 13.311701 | 0.030303 | -0.052754 |
| 6681.000000 | 108688.000000 | current_global | 0.005175 | 0.000339 | 15.242416 | 0.030303 | -0.037043 |
| 6681.000000 | 108688.000000 | exposure_matched_local | 0.007797 | 0.000417 | 18.687662 | 0.030303 | -0.051371 |
| 6681.000000 | 100399.000000 | current_global | 0.004190 | 0.000514 | 8.156391 | 0.030303 | -0.048800 |
| 6681.000000 | 100399.000000 | exposure_matched_local | 0.006639 | 0.000493 | 13.477567 | 0.030303 | -0.044545 |

## Separate outcomes

| n_runs | median_js_effect_ratio | positive_fraction | p_le_010_fraction | local_gate_pass |
| --- | --- | --- | --- | --- |
| 6.000000 | 12.417734 | 1.000000 | 0.833333 | 1.000000 |

| n_runs | target_swap_multiplier | median_js_effect_ratio | positive_fraction | perturbation_integrity_pass | longer_perturbation_consistency_pass |
| --- | --- | --- | --- | --- | --- |
| 6.000000 | 0.100000 | 14.222428 | 1.000000 | 1.000000 | 1.000000 |

| fresh_median_js_effect_ratio | bootstrap_median_ci_low | bootstrap_median_ci_high | fresh_over_v16d | fresh_over_v16h | magnitude_compatibility_class |
| --- | --- | --- | --- | --- | --- |
| 12.417734 | 4.626084 | 16.082615 | 0.731300 | 1.557083 | compatible_with_both_prior_anchors |

Growth and scheduler rows remain diagnostics.

| group_field | group_value | n_runs | median_js_effect_ratio | positive_fraction | group_pass |
| --- | --- | --- | --- | --- | --- |
| growth_seed | 5764.000000 | 6.000000 | 8.004634 | 1.000000 | 1.000000 |
| growth_seed | 6681.000000 | 6.000000 | 13.394634 | 1.000000 | 1.000000 |

| group_field | group_value | n_runs | median_js_effect_ratio | positive_fraction | group_pass |
| --- | --- | --- | --- | --- | --- |
| arm | current_global | 6.000000 | 9.506496 | 1.000000 | 1.000000 |
| arm | exposure_matched_local | 6.000000 | 12.417734 | 1.000000 | 1.000000 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| fresh_history_integrity | pass | runs=12;events=36864;replays=24 | runs=12;events=36864;replays=24 | continue |
| qualified_primary_perturbation_integrity | pass | 384/384 | 384/384 | continue |
| fresh_effect_existence | pass | median=12.417734;positive=1.000000;p_le_010=0.833333 | median>=2;positive>=5/6;p_le_010>=1/2 | replicated |
| qualified_longer_perturbation_integrity | pass | 192/192 | 192/192 | continue |
| longer_perturbation_consistency | pass | median=14.222428;positive=1.000000 | median>=1;positive>=5/6 | consistent |
| magnitude_compatibility | descriptive | compatible_with_both_prior_anchors | not_a_confirmatory_gate | compatible_with_both_prior_anchors |
| v16m_overall | fresh_strict_null_spectrum_contrast_replicated_with_qualified_sampler | instrumentation=1;existence=1;longer=1 | 1;1;1 | fresh_strict_null_spectrum_contrast_replicated_with_qualified_sampler |

## Interpretation boundary

A replication supports a repeatable finite event-DAG interval-spectrum contrast conditional on this perturbation sampler. The null preserves scheduler order, exact direct in/out-degree, exact causal depth/profile, and the global dyadic parent-age-bin histogram. The higher attempt ceiling establishes completion, not convergence or uniform sampling.

Tail-mass deltas must be read by sign; the primary endpoint is the full-spectrum contrast, not an assumed increase in large intervals.

This result does not establish dimension, manifoldlikeness, Lorentz invariance, spacetime, continuum behavior, particles, entanglement, or a physical causal law.
