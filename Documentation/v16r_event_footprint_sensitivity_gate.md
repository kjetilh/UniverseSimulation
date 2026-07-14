# v16r event-footprint sensitivity gate

Status: `v16r_spectrum_contrast_persists_under_event_footprint_null`.

V16r is a posthoc sensitivity analysis on the six v16m primary histories. It reuses the observed event DAGs and replaces the v16m strict null with the v16q-qualified event-footprint null. It is not an independent replication.

Specification digest: `f0a96df3dab756a9c0aa6ed7409c8e03741a8fccaee08b0ae9267a0b185e31ac`.

## Per-run primary results

| growth_seed | run_offset | js_effect_ratio | empirical_p_upper | tail_mass_ge_8_delta | min_actual_resource_conflict_edge_fraction | all_perturbation_integrity_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 5764.000000 | 100399.000000 | 11.933454 | 0.030303 | -0.052756 | 0.899823 | 1.000000 |
| 5764.000000 | 106802.000000 | 3.953314 | 0.060606 | -0.003280 | 0.900538 | 1.000000 |
| 5764.000000 | 108688.000000 | 5.172965 | 0.030303 | -0.023765 | 0.900730 | 1.000000 |
| 6681.000000 | 100399.000000 | 14.392497 | 0.030303 | -0.039261 | 0.900498 | 1.000000 |
| 6681.000000 | 106802.000000 | 30.079876 | 0.030303 | -0.053874 | 0.900275 | 1.000000 |
| 6681.000000 | 108688.000000 | 14.181670 | 0.030303 | -0.041835 | 0.899972 | 1.000000 |

## Aggregate gates

| n_runs | median_js_effect_ratio | positive_fraction | p_le_010_fraction | local_gate_pass |
| --- | --- | --- | --- | --- |
| 6.000000 | 13.057562 | 1.000000 | 1.000000 | 1.000000 |

| n_runs | median_js_effect_ratio | positive_fraction | perturbation_integrity_pass | longer_perturbation_consistency_pass |
| --- | --- | --- | --- | --- |
| 6.000000 | 12.542120 | 1.000000 | 1.000000 | 1.000000 |

## Same-history null comparison

| growth_seed | run_offset | v16m_strict_null_js_effect_ratio | v16r_footprint_null_js_effect_ratio | footprint_over_strict_ratio |
| --- | --- | --- | --- | --- |
| 5764.000000 | 100399.000000 | 11.523766 | 11.933454 | 1.035552 |
| 5764.000000 | 106802.000000 | 2.502413 | 3.953314 | 1.579800 |
| 5764.000000 | 108688.000000 | 6.749754 | 5.172965 | 0.766393 |
| 6681.000000 | 100399.000000 | 13.477567 | 14.392497 | 1.067885 |
| 6681.000000 | 106802.000000 | 13.311701 | 30.079876 | 2.259657 |
| 6681.000000 | 108688.000000 | 18.687662 | 14.181670 | 0.758879 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| qualified_primary_footprint_perturbation_integrity | pass | 192/192 | 192/192 | continue |
| posthoc_footprint_effect_existence | pass | median=13.057562;positive=1.000000;p_le_010=1.000000 | median>=2;positive>=5/6;p_le_010>=1/2 | persists |
| qualified_longer_footprint_perturbation_integrity | pass | 96/96 | 96/96 | continue |
| longer_footprint_consistency | pass | median=12.542120;positive=1.000000 | median>=1;positive>=5/6 | consistent |
| independent_replication_exclusion | pass | same_v16m_histories | posthoc_sensitivity_only | do_not_count_as_new_replication |
| v16r_overall | v16r_spectrum_contrast_persists_under_event_footprint_null | integrity=1;existence=1;longer=1 | diagnostic_branch | v16r_spectrum_contrast_persists_under_event_footprint_null |

## Interpretation boundary

Persistence means the coarse event-family/write-read namespace footprint does not absorb the interval-spectrum contrast on these six reused histories, conditional on the qualified procedure. It does not establish independence from concrete resource identity, a causal mechanism, sampler uniformity, or a new replication.

Failure would show sensitivity to this null family, not prove that the original contrast was spurious.

No dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, or physical-law claim is authorized.
