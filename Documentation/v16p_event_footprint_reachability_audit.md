# v16p event-footprint reachability audit

Status: `v16p_event_footprint_static_support_promising`.

V16p exactly enumerates all direct-edge pairs that share a source-write/target-read event footprint in the six saved v16n calibration DAGs. The footprint retains event family and resource namespace sets, but it does not require a concrete shared resource ID on proposed null edges.

The round performs no rewiring and computes no interval spectrum. It is an effect-blind support diagnostic, not an effect test.

Specification digest: `6acf5c65e86f0d493a949474b25a65f9529b1798f04b8ebea79b7d16f01ce656`.

## Per-run support

| growth_seed | run_offset | edge_count | eligible_edge_fraction | within_footprint_candidate_pairs | legal_pairs | legal_edge_fraction | promising_support |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 7252.000000 | 110360.000000 | 3498.000000 | 0.999714 | 3551536.000000 | 6294.000000 | 0.681246 | 1.000000 |
| 7252.000000 | 114756.000000 | 3623.000000 | 0.999724 | 3487272.000000 | 8212.000000 | 0.675959 | 1.000000 |
| 7252.000000 | 117562.000000 | 3463.000000 | 0.999711 | 3610543.000000 | 3918.000000 | 0.633843 | 1.000000 |
| 8018.000000 | 110360.000000 | 3566.000000 | 0.999159 | 3562347.000000 | 6233.000000 | 0.646102 | 1.000000 |
| 8018.000000 | 114756.000000 | 3557.000000 | 1.000000 | 3634426.000000 | 5047.000000 | 0.616812 | 1.000000 |
| 8018.000000 | 117562.000000 | 3513.000000 | 0.999715 | 3486843.000000 | 5831.000000 | 0.663535 | 1.000000 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| exact_within_footprint_enumeration | pass | runs=6;candidate_pairs=21332967 | runs=6;all_within_bucket_pairs_exact | continue |
| all_run_reachability | pass | legal_pairs=35535;runs_with_moves=6/6 | runs_with_moves=6/6 | continue |
| all_run_static_support | pass | 0.616812 | >=0.1 | qualify_sampler_next |
| spectrum_and_rewiring_exclusion | pass | spectrum=0;rewires=0 | 0;0 | diagnostic_only |
| v16p_overall | v16p_event_footprint_static_support_promising | reachable=1;promising=1;min_legal_edge_fraction=0.616811920157 | diagnostic_branch | v16p_event_footprint_static_support_promising |

## Interpretation boundary

Static reachability is necessary but not sufficient for a useful null sampler. It does not establish chain connectivity, mixing, convergence, stationarity, independence, representativeness, or uniformity.

The footprint is a coarse event-side conditioning rule. It does not preserve concrete resource identity and does not test a physical mechanism. No v16m spectrum effect is evaluated here.
