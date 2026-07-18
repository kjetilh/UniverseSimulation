# v17d effect-blind finite stability

Status: `v17d_endpoint_centers_not_stable`.

## Purpose and frozen design

V17d asks whether the qualified v17c bounded-cycle chain gives compatible finite endpoint distributions across the two frozen starts, two fresh deterministic seed families, and separated early/late windows. It uses 2048 steps per chain and computes no source spectrum or observed-effect statistic.

## Source qualification

| growth_seed | run_offset | chain_passes | endpoint_center_passes | endpoint_agreement_passes | component_center_passes | proposal_overlap_passes | source_qualification_pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 4 | 14 | 2 | 15 | 3 | 0 |
| 9299 | 123403 | 4 | 14 | 2 | 15 | 3 | 0 |
| 9299 | 127341 | 4 | 14 | 2 | 15 | 3 | 0 |
| 9365 | 123078 | 4 | 14 | 2 | 15 | 3 | 0 |
| 9365 | 123403 | 4 | 15 | 2 | 15 | 3 | 0 |
| 9365 | 127341 | 4 | 14 | 2 | 15 | 3 | 0 |

## Endpoint agreement

| growth_seed | run_offset | agreement_kind | median_within_changed_edge_fraction | median_cross_changed_edge_fraction | cross_to_within_distance_ratio | endpoint_agreement_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | start_family | 0.155458 | 0.441014 | 2.836879 | 0 |
| 9299 | 123078 | independent_chain_seed_family | 0.430954 | 0.346058 | 0.803006 | 1 |
| 9299 | 123078 | early_vs_late_sample_window | 0.431367 | 0.331036 | 0.767412 | 1 |
| 9299 | 123403 | start_family | 0.144656 | 0.395076 | 2.731141 | 0 |
| 9299 | 123403 | independent_chain_seed_family | 0.388220 | 0.322188 | 0.829910 | 1 |
| 9299 | 123403 | early_vs_late_sample_window | 0.385562 | 0.305960 | 0.793541 | 1 |
| 9299 | 127341 | start_family | 0.149730 | 0.412433 | 2.754502 | 0 |
| 9299 | 127341 | independent_chain_seed_family | 0.403917 | 0.343032 | 0.849262 | 1 |
| 9299 | 127341 | early_vs_late_sample_window | 0.405478 | 0.327562 | 0.807840 | 1 |
| 9365 | 123078 | start_family | 0.169891 | 0.451360 | 2.656766 | 0 |
| 9365 | 123078 | independent_chain_seed_family | 0.446594 | 0.359966 | 0.806026 | 1 |
| 9365 | 123078 | early_vs_late_sample_window | 0.444351 | 0.347771 | 0.782650 | 1 |
| 9365 | 123403 | start_family | 0.145117 | 0.394284 | 2.717017 | 0 |
| 9365 | 123403 | independent_chain_seed_family | 0.389290 | 0.322697 | 0.828938 | 1 |
| 9365 | 123403 | early_vs_late_sample_window | 0.386792 | 0.309795 | 0.800933 | 1 |
| 9365 | 127341 | start_family | 0.155283 | 0.451352 | 2.906643 | 0 |
| 9365 | 127341 | independent_chain_seed_family | 0.441873 | 0.362141 | 0.819558 | 1 |
| 9365 | 127341 | early_vs_late_sample_window | 0.442152 | 0.347505 | 0.785939 | 1 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_integrity | pass | spectrum=0;effect=0 | 0;0 | continue |
| frozen_start_replay | pass | 12/12 | 12/12 | continue |
| endpoint_integrity | pass | 384/384 | 384/384 | continue |
| pathwise_detailed_balance | pass | 36/36 | 36/36 | continue |
| representation_covariance | pass | 12/12 | 12/12 | continue |
| finite_traversal | pass | 24/24 | 24/24 | continue |
| resource_bound | pass | 24/24;max=67.228174s | 24/24;each<=75s | continue |
| endpoint_center_stability | fail | 85/108 | 108/108 | effects_closed |
| endpoint_distance_agreement | fail | 12/18 | 18/18 | effects_closed |
| residual_component_profile_stability | pass | 90/90 | 90/90 | continue |
| proposal_footprint_overlap | pass | 18/18 | 18/18 | continue |
| v17d_overall | v17d_endpoint_centers_not_stable | exclusion=1;starts=12/12;integrity=384/384;reverse=36/36;representation=12/12;traversal=24/24;resource=24/24;centers=85/108;distance=12/18;components=90/90;footprints=18/18 | 1;12/12;384/384;36/36;12/12;24/24;24/24;108/108;18/18;90/90;18/18 | v17d_endpoint_centers_not_stable |

## Runtime and traversal

Across 24 chains, maximum runtime was `67.228174` seconds, minimum final displacement was `0.148169`, and minimum accepted-cycle counts in the early/late windows were `55`.

## Interpretation boundary

Endpoint center and distance agreement are finite diagnostics, not convergence or mixing proofs. Residual SCCs describe alternating-cycle flexibility at sampled assignments. Empirical proposal-incidence footprints describe only accepted moves observed in these runs. Neither establishes global connectivity of the Markov state graph.

No source effect, Bell correlation, entanglement, Lorentz symmetry, spacetime geometry, particle or universe model was tested.

## Postrun start-memory diagnosis

The formal failure is not diffuse. Seed-family endpoint agreement passed `6/6`, early/late endpoint-distance agreement passed `6/6`, residual-component center stability passed `90/90`, and proposal-footprint overlap passed `18/18`. Start-family endpoint-distance agreement failed `0/6`, with cross/within ratios `2.656766-2.906643`.

Source-edge and concrete-conflict start gaps contracted from early to late in `12/12` source-feature cells, but direct cross-start endpoint distance was effectively flat: late/early ratios were `0.987676-1.005646`. Candidate-rank gaps contracted in only `3/6` sources. The chains therefore move in some coarse coordinates without erasing state-level start memory at 2048 steps.

All eight representative endpoints within each source, spanning both starts, both seeds and both windows, had the same exact residual-SCC profile digest and flexible-edge Jaccard `1.0`. This is an exact finite residual-algebra artifact. It does not establish connectivity of the length-2-to-4 proposal state graph.

The next gate is one bounded effect-blind scale response. If direct cross-start distance remains flat at substantially longer checkpoints, stop scaling this kernel and change the move class. Source-spectrum effects remain closed.
