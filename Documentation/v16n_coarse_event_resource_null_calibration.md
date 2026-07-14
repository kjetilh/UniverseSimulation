# v16n coarse event/resource null calibration

Status: `v16n_coarse_event_resource_sampler_not_qualified`.

v16n is an effect-blind sampler calibration. It generated six new calibration histories after freezing the event/resource color, proposal rule, ceiling ladder, integrity criteria, assignments, and source hashes. No interval spectrum was computed in this round.

Specification digest: `dd548e8ba4df92d2367154023266395c80d87f6769e5139860d7f5050a11b5fc`.

## Coarse edge color

Each edge color contains parent family, child family, and the sorted set of actual shared-resource conflict channels. Channels retain access direction and the namespace before the first colon, but not the concrete resource identity. Proposed swaps must preserve the global color histogram and every resulting edge must still have an actual concrete read/write conflict.

This is stronger than the v16j degree/depth/age null but weaker than exact resource-identity or per-child conditioning.

## Metadata audit

| growth_seed | run_offset | event_rows | event_id_mapping_total_pass | other_namespace_count | metadata_sha256 |
| --- | --- | --- | --- | --- | --- |
| 8018.000000 | 114756.000000 | 3072.000000 | 1.000000 | 0.000000 | 4eda1e7fca4e13c562885389576a67cb638588949238a37cce9aee5af3a1b20b |
| 8018.000000 | 117562.000000 | 3072.000000 | 1.000000 | 0.000000 | 2ae21c45a792e87e87f1bc5614bd3cd65971892e967441616c3d92dacc1ff5d1 |
| 8018.000000 | 110360.000000 | 3072.000000 | 1.000000 | 0.000000 | a153022394e1d87c6944afe46b4780f6a587e4a55c000374e5b247250fe3f6e5 |
| 7252.000000 | 114756.000000 | 3072.000000 | 1.000000 | 0.000000 | a6e5a1f4e05fa2467fd31224e368e47c0d924dda90a66c2cf7296df1fac255c3 |
| 7252.000000 | 117562.000000 | 3072.000000 | 1.000000 | 0.000000 | 524ca007f842aa981926f4f1fd47229da7b0d46b8731d2cbea1cfeab9a4b02c9 |
| 7252.000000 | 110360.000000 | 3072.000000 | 1.000000 | 0.000000 | 4ce480b63648cea71789ca7ad2d9103c50ee13f5ebffc755471c718dc4470325 |

## Attempt ceiling ladder

| attempt_ceiling | n_perturbations | integrity_passes | required_passes | max_attempts_per_edge_observed | min_changed_edge_fraction | min_eligible_edge_fraction | ceiling_qualification_pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 240.000000 | 288.000000 | 0.000000 | 288.000000 | 240.000000 | 0.000000 | 0.997141 | 0.000000 |
| 480.000000 | 288.000000 | 0.000000 | 288.000000 | 480.000000 | 0.000000 | 0.997141 | 0.000000 |
| 960.000000 | 288.000000 | 0.000000 | 288.000000 | 960.000000 | 0.000000 | 0.997141 | 0.000000 |
| 1920.000000 | 288.000000 | 0.000000 | 288.000000 | 1920.000000 | 0.000000 | 0.997141 | 0.000000 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| fresh_calibration_history_and_metadata_integrity | pass | runs=6;events=18432;metadata=6/6 | runs=6;events=18432;metadata=6/6 | continue |
| effect_blind_attempt_ceiling_qualification | fail | none | lowest_frozen_ceiling_with_all_288_perturbations_valid | stop_without_spectrum |
| spectrum_exclusion | pass | 0.000000 | 0.000000 | calibration_only |
| v16n_overall | v16n_coarse_event_resource_sampler_not_qualified | history=1;ceiling=None | history=1;ceiling=qualified | v16n_coarse_event_resource_sampler_not_qualified |

## Interpretation boundary

A qualified result means only that this frozen constrained perturbation procedure completed and preserved its declared finite-DAG invariants on the calibration corpus. It does not prove irreducibility, convergence, stationarity, independence, representativeness, or uniform sampling.

No effect, dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, or physical-law claim is evaluated here.
