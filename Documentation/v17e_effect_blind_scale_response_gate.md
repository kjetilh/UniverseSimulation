# v17e effect-blind scale-response gate

Status: `v17e_cross_start_distance_flat_retire_length_2_4_kernel`.

## Frozen design

V17e reuses the six v17d state spaces, both frozen starts, both v17d random streams, and the exact v17c length-2-to-4 proposal law. The 1536-1984 checkpoint window must replay v17d exactly; each chain then continues without restart to a 3584-4032 window under a 4096-step total budget. No source spectrum or observed-effect statistic is computed.

## Primary scale response

| growth_seed | run_offset | baseline_median_cross_start_distance | scale_median_cross_start_distance | scale_over_baseline_cross_start_distance_ratio | primary_material_contraction_pass | baseline_cross_to_within_ratio | scale_cross_to_within_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 0.439912 | 0.437293 | 0.994048 | 0 | 1.918269 | 1.323738 |
| 9299 | 123403 | 0.392417 | 0.394516 | 1.005348 | 0 | 1.731481 | 1.256125 |
| 9299 | 127341 | 0.410729 | 0.410020 | 0.998272 | 0 | 1.650884 | 1.163043 |
| 9365 | 123078 | 0.449397 | 0.448276 | 0.997505 | 0 | 1.818491 | 1.272076 |
| 9365 | 123403 | 0.395394 | 0.391509 | 0.990175 | 0 | 1.921780 | 1.293902 |
| 9365 | 127341 | 0.450795 | 0.441316 | 0.978973 | 0 | 1.909091 | 1.303417 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_integrity | pass | spectrum=0;effect=0 | 0;0 | continue |
| frozen_start_replay | pass | 12/12 | 12/12 | continue |
| matched_v17d_prefix_replay | pass | 192/192 | 192/192 | continue |
| endpoint_integrity | pass | 384/384 | 384/384 | continue |
| pathwise_detailed_balance | pass | 36/36 | 36/36 | continue |
| representation_covariance | pass | 12/12 | 12/12 | continue |
| finite_traversal | pass | 24/24 | 24/24 | continue |
| resource_bound | pass | 24/24;max=107.676262s | 24/24;each<=160s | continue |
| primary_cross_start_distance_contraction | fail | 0/6;ratio=0.978973-1.005348 | 6/6;each<=0.90 | retire_length_2_4_kernel_scale_growth |
| endpoint_center_diagnostic | reported | 83/108 | diagnostic_only | no_primary_decision |
| endpoint_agreement_diagnostic | reported | 12/18 | diagnostic_only | no_primary_decision |
| residual_profile_diagnostic | reported | centers=90/90;identity=6/6 | diagnostic_only | not_connectivity |
| proposal_footprint_diagnostic | reported | 18/18 | diagnostic_only | not_connectivity |
| v17e_overall | v17e_cross_start_distance_flat_retire_length_2_4_kernel | exclusion=1;starts=12/12;prefix=192/192;integrity=384/384;reverse=36/36;representation=12/12;traversal=24/24;resource=24/24;primary=0/6 | 1;12/12;192/192;384/384;36/36;12/12;24/24;24/24;6/6 | v17e_cross_start_distance_flat_retire_length_2_4_kernel |

## Diagnostics

Direct cross-start distance contracted directionally in `5/6` sources and met the preregistered material threshold in `0/6`. The source-ratio range was `0.978973-1.005348`. Start-sensitive feature gaps contracted directionally in `15/18` diagnostic cells. Exact residual-profile identity held in `6/6` sources.

All 24 chains had a maximum runtime of `107.676262` seconds. These finite rows do not prove convergence, irreducibility, mixing, global uniformity, or state-graph connectivity.

## Decision

The preregistered six-source contraction requirement failed. Further scale growth of this length-2-to-4 kernel is retired. The next gate must change the move class while preserving an explicit target law and effect blindness.

## Claim boundary

No source effect, Bell correlation, entanglement, Lorentz symmetry, spacetime geometry, particle, energy, temperature, or universe model was tested.
