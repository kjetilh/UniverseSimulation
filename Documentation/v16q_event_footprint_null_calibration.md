# v16q event-footprint null calibration

Status: `v16q_event_footprint_sampler_qualified`.

V16q is an effect-blind sampler calibration on the six frozen v16n DAGs. The proposal preserves event family plus source write-namespace and target read-namespace footprints, but does not require concrete resource overlap on proposed edges. No interval spectrum is computed.

Specification digest: `f73caff88c6b944eb2e320d1723dab4cc784e41fc2ccbeb0224e884327a43ea2`.

## Attempt ceiling ladder

| attempt_ceiling | n_perturbations | integrity_passes | required_passes | max_attempts_per_edge_observed | min_changed_edge_fraction | min_acceptance_rate | min_actual_resource_conflict_edge_fraction | ceiling_qualification_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 60.000000 | 288.000000 | 288.000000 | 288.000000 | 59.573491 | 0.100057 | 0.004535 | 0.899509 | 1.000000 |
| 120.000000 | 0.000000 | 0.000000 | 288.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 240.000000 | 0.000000 | 0.000000 | 288.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 480.000000 | 0.000000 | 0.000000 | 288.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| frozen_source_and_footprint_support | pass | runs=6;v16p=promising | runs=6;v16p=promising | continue |
| effect_blind_attempt_ceiling_qualification | pass | 60.000000 | lowest_frozen_ceiling_with_all_288_perturbations_valid | qualify |
| spectrum_exclusion | pass | 0.000000 | 0.000000 | calibration_only |
| v16q_overall | v16q_event_footprint_sampler_qualified | ceiling=60 | ceiling=qualified | v16q_event_footprint_sampler_qualified |

## Interpretation boundary

Qualification means only that the frozen procedure completed, generated unique changed DAGs, and preserved its declared finite-DAG invariants on this calibration corpus. It does not prove irreducibility, convergence, stationarity, independence, representativeness, or uniformity.

Concrete resource conflict is deliberately not invariant under this coarse footprint rule. The reported retained-conflict fraction is diagnostic, not a qualification condition.

No interval-spectrum effect or physical geometry claim is evaluated here.
