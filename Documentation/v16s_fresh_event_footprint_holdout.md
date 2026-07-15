# v16s fresh event-footprint holdout

Status: `v16s_fresh_event_footprint_spectrum_contrast_replicated`.

V16s generated six new exposure-matched histories after freezing the v16q-qualified event-footprint null, assignments, null counts, thresholds, and source hashes. It is the first fresh-history confirmatory use of this null family.

Specification digest: `06527575422c91ed0c950742e3b0c74686d14c6c738342040f7605da48d30989`.

## Per-run primary results

| growth_seed | run_offset | js_effect_ratio | empirical_p_upper | tail_mass_ge_8_delta | min_actual_resource_conflict_edge_fraction | all_perturbation_integrity_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 9365.000000 | 123078.000000 | 12.833404 | 0.030303 | -0.055716 | 0.899636 | 1.000000 |
| 9365.000000 | 127341.000000 | 9.707298 | 0.030303 | -0.049864 | 0.899638 | 1.000000 |
| 9365.000000 | 123403.000000 | 9.504021 | 0.030303 | -0.048031 | 0.900943 | 1.000000 |
| 9299.000000 | 123078.000000 | 16.160199 | 0.030303 | -0.049322 | 0.899669 | 1.000000 |
| 9299.000000 | 127341.000000 | 11.165161 | 0.030303 | -0.045103 | 0.900653 | 1.000000 |
| 9299.000000 | 123403.000000 | 20.856233 | 0.030303 | -0.046850 | 0.900112 | 1.000000 |

## Confirmatory aggregates

| n_runs | median_js_effect_ratio | positive_fraction | p_le_010_fraction | local_gate_pass |
| --- | --- | --- | --- | --- |
| 6.000000 | 11.999282 | 1.000000 | 1.000000 | 1.000000 |

| n_runs | median_js_effect_ratio | positive_fraction | perturbation_integrity_pass | longer_perturbation_consistency_pass |
| --- | --- | --- | --- | --- |
| 6.000000 | 12.054418 | 1.000000 | 1.000000 | 1.000000 |

## Descriptive anchors

| anchor | median_js_effect_ratio | fresh_v16s_over_anchor | interpretation |
| --- | --- | --- | --- |
| v16m_strict_null_fresh_holdout | 12.417734 | 0.966302 | descriptive_only |
| v16r_footprint_null_posthoc | 13.057562 | 0.918953 | descriptive_only |
| v16s_footprint_null_fresh_holdout | 11.999282 | 1.000000 | descriptive_only |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| fresh_history_integrity | pass | runs=6;events=18432;replays=12 | runs=6;events=18432;replays=12 | continue |
| qualified_primary_footprint_perturbation_integrity | pass | 192/192 | 192/192 | continue |
| fresh_footprint_effect_existence | pass | median=11.999282;positive=1.000000;p_le_010=1.000000 | median>=2;positive>=5/6;p_le_010>=1/2 | replicated |
| qualified_longer_footprint_perturbation_integrity | pass | 96/96 | 96/96 | continue |
| longer_footprint_consistency | pass | median=12.054418;positive=1.000000 | median>=1;positive>=5/6 | consistent |
| v16s_overall | v16s_fresh_event_footprint_spectrum_contrast_replicated | history=1;existence=1;longer=1 | 1;1;1 | v16s_fresh_event_footprint_spectrum_contrast_replicated |

## Interpretation boundary

Replication supports a fresh finite event-DAG interval-spectrum contrast conditional on the qualified coarse footprint sampler. It does not establish sampler irreducibility, convergence, stationarity, representativeness, or uniformity, and the null does not preserve concrete resource identity.

The primary endpoint is full-spectrum contrast. Tail-mass deltas must be read by sign and are not assumed positive.

No dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, or physical-law claim is authorized.
