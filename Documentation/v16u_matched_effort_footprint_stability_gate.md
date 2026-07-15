# v16u matched-effort footprint-null stability gate

Status: `v16u_footprint_null_centers_stable_under_exact_matched_effort`.

V16u repairs the known v16t realized-effort confound. It is effect-blind: only rewired null DAG spectra are computed; source spectra and observed/null effect metrics are excluded.

Specification digest: `e0a1c001b7879ff5794f2ed7e8a5916cd4603fd8d3aa39369b241be72ed940f6`.

## Frozen design

Each of the six frozen v16s DAGs has `16` shared burn-in replicates. Burn-in uses the qualified footprint sampler until at least `0.100` of source edges differ. From each frozen burn-in state, `K = ceil(0.100 * source edge count)` accepted swaps are used as the exact effort unit.

The direct path records exact `+K` and `+2K` checkpoints from one RNG stream. The staged path branches from the exact same `+K` checkpoint, resets the RNG stream, and advances exactly another `+K`. Direct and staged endpoints therefore both contain exactly `+2K` accepted swaps after an identical prefix.

A center comparison passes when Jensen-Shannon center shift is at most `2.0` times pooled median leave-one-out dispersion. Every source DAG must pass.

## Protocol summaries

| growth_seed | run_offset | protocol | mean_k_accepted_swaps | mean_burnin_accepted_swaps | mean_incremental_accepted_swaps | median_leave_one_out_js | min_burnin_changed_edge_fraction | all_perturbation_integrity_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299.000000 | 123078.000000 | burnin | 363.000000 | 962.312500 | 0.000000 | 0.000300 | 0.100055 | 1.000000 |
| 9299.000000 | 123078.000000 | direct_plus_k | 363.000000 | 962.312500 | 363.000000 | 0.000304 | 0.100055 | 1.000000 |
| 9299.000000 | 123078.000000 | direct_plus_2k | 363.000000 | 962.312500 | 726.000000 | 0.000275 | 0.100055 | 1.000000 |
| 9299.000000 | 123078.000000 | staged_plus_k_plus_k | 363.000000 | 962.312500 | 726.000000 | 0.000451 | 0.100055 | 1.000000 |
| 9299.000000 | 123403.000000 | burnin | 358.000000 | 1128.187500 | 0.000000 | 0.000335 | 0.100168 | 1.000000 |
| 9299.000000 | 123403.000000 | direct_plus_k | 358.000000 | 1128.187500 | 358.000000 | 0.000395 | 0.100168 | 1.000000 |
| 9299.000000 | 123403.000000 | direct_plus_2k | 358.000000 | 1128.187500 | 716.000000 | 0.000382 | 0.100168 | 1.000000 |
| 9299.000000 | 123403.000000 | staged_plus_k_plus_k | 358.000000 | 1128.187500 | 716.000000 | 0.000301 | 0.100168 | 1.000000 |
| 9299.000000 | 127341.000000 | burnin | 353.000000 | 1119.625000 | 0.000000 | 0.000397 | 0.100199 | 1.000000 |
| 9299.000000 | 127341.000000 | direct_plus_k | 353.000000 | 1119.625000 | 353.000000 | 0.000354 | 0.100199 | 1.000000 |
| 9299.000000 | 127341.000000 | direct_plus_2k | 353.000000 | 1119.625000 | 706.000000 | 0.000605 | 0.100199 | 1.000000 |
| 9299.000000 | 127341.000000 | staged_plus_k_plus_k | 353.000000 | 1119.625000 | 706.000000 | 0.000391 | 0.100199 | 1.000000 |
| 9365.000000 | 123078.000000 | burnin | 357.000000 | 811.812500 | 0.000000 | 0.000342 | 0.100084 | 1.000000 |
| 9365.000000 | 123078.000000 | direct_plus_k | 357.000000 | 811.812500 | 357.000000 | 0.000674 | 0.100084 | 1.000000 |
| 9365.000000 | 123078.000000 | direct_plus_2k | 357.000000 | 811.812500 | 714.000000 | 0.000938 | 0.100084 | 1.000000 |
| 9365.000000 | 123078.000000 | staged_plus_k_plus_k | 357.000000 | 811.812500 | 714.000000 | 0.000767 | 0.100084 | 1.000000 |
| 9365.000000 | 123403.000000 | burnin | 361.000000 | 1158.437500 | 0.000000 | 0.000690 | 0.100166 | 1.000000 |
| 9365.000000 | 123403.000000 | direct_plus_k | 361.000000 | 1158.437500 | 361.000000 | 0.001085 | 0.100166 | 1.000000 |
| 9365.000000 | 123403.000000 | direct_plus_2k | 361.000000 | 1158.437500 | 722.000000 | 0.000810 | 0.100166 | 1.000000 |
| 9365.000000 | 123403.000000 | staged_plus_k_plus_k | 361.000000 | 1158.437500 | 722.000000 | 0.001175 | 0.100166 | 1.000000 |
| 9365.000000 | 127341.000000 | burnin | 359.000000 | 878.312500 | 0.000000 | 0.000311 | 0.100084 | 1.000000 |
| 9365.000000 | 127341.000000 | direct_plus_k | 359.000000 | 878.312500 | 359.000000 | 0.000414 | 0.100084 | 1.000000 |
| 9365.000000 | 127341.000000 | direct_plus_2k | 359.000000 | 878.312500 | 718.000000 | 0.000490 | 0.100084 | 1.000000 |
| 9365.000000 | 127341.000000 | staged_plus_k_plus_k | 359.000000 | 878.312500 | 718.000000 | 0.000367 | 0.100084 | 1.000000 |

## Null-center comparisons

| growth_seed | run_offset | comparison | center_jensen_shannon | pooled_median_leave_one_out_js | center_shift_ratio | stability_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 9299.000000 | 123078.000000 | burnin_vs_plus_k | 0.000030 | 0.000301 | 0.100894 | 1.000000 |
| 9299.000000 | 123078.000000 | plus_k_vs_plus_2k | 0.000039 | 0.000288 | 0.136195 | 1.000000 |
| 9299.000000 | 123078.000000 | burnin_vs_plus_2k | 0.000130 | 0.000286 | 0.453210 | 1.000000 |
| 9299.000000 | 123078.000000 | direct_plus_2k_vs_staged_plus_k_plus_k | 0.000002 | 0.000359 | 0.005939 | 1.000000 |
| 9299.000000 | 123403.000000 | burnin_vs_plus_k | 0.000066 | 0.000372 | 0.177037 | 1.000000 |
| 9299.000000 | 123403.000000 | plus_k_vs_plus_2k | 0.000009 | 0.000395 | 0.022947 | 1.000000 |
| 9299.000000 | 123403.000000 | burnin_vs_plus_2k | 0.000070 | 0.000337 | 0.207752 | 1.000000 |
| 9299.000000 | 123403.000000 | direct_plus_2k_vs_staged_plus_k_plus_k | 0.000030 | 0.000358 | 0.084544 | 1.000000 |
| 9299.000000 | 127341.000000 | burnin_vs_plus_k | 0.000086 | 0.000385 | 0.224546 | 1.000000 |
| 9299.000000 | 127341.000000 | plus_k_vs_plus_2k | 0.000012 | 0.000521 | 0.022662 | 1.000000 |
| 9299.000000 | 127341.000000 | burnin_vs_plus_2k | 0.000058 | 0.000521 | 0.111055 | 1.000000 |
| 9299.000000 | 127341.000000 | direct_plus_2k_vs_staged_plus_k_plus_k | 0.000098 | 0.000542 | 0.180595 | 1.000000 |
| 9365.000000 | 123078.000000 | burnin_vs_plus_k | 0.000136 | 0.000543 | 0.250972 | 1.000000 |
| 9365.000000 | 123078.000000 | plus_k_vs_plus_2k | 0.000083 | 0.000835 | 0.099896 | 1.000000 |
| 9365.000000 | 123078.000000 | burnin_vs_plus_2k | 0.000348 | 0.000522 | 0.666516 | 1.000000 |
| 9365.000000 | 123078.000000 | direct_plus_2k_vs_staged_plus_k_plus_k | 0.000034 | 0.000900 | 0.037563 | 1.000000 |
| 9365.000000 | 123403.000000 | burnin_vs_plus_k | 0.000038 | 0.000953 | 0.040213 | 1.000000 |
| 9365.000000 | 123403.000000 | plus_k_vs_plus_2k | 0.000168 | 0.001017 | 0.164789 | 1.000000 |
| 9365.000000 | 123403.000000 | burnin_vs_plus_2k | 0.000280 | 0.000793 | 0.353621 | 1.000000 |
| 9365.000000 | 123403.000000 | direct_plus_2k_vs_staged_plus_k_plus_k | 0.000026 | 0.001065 | 0.024506 | 1.000000 |
| 9365.000000 | 127341.000000 | burnin_vs_plus_k | 0.000083 | 0.000357 | 0.234028 | 1.000000 |
| 9365.000000 | 127341.000000 | plus_k_vs_plus_2k | 0.000038 | 0.000465 | 0.081534 | 1.000000 |
| 9365.000000 | 127341.000000 | burnin_vs_plus_2k | 0.000228 | 0.000399 | 0.571164 | 1.000000 |
| 9365.000000 | 127341.000000 | direct_plus_2k_vs_staged_plus_k_plus_k | 0.000013 | 0.000462 | 0.028985 | 1.000000 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| frozen_source_integrity | pass | source_dags=6 | source_dags=6 | continue |
| all_protocol_perturbation_integrity | pass | 384/384 | 384/384 | continue |
| exact_increment_realization | pass | 96/96 | 96/96 | continue |
| direct_staged_matched_effort | pass | 96/96;max_abs_difference=0 | 96/96;difference=0 | continue |
| shared_k_prefix | pass | 96/96 | 96/96 | continue |
| exact_realized_length_null_center_stability | pass | 18/18;max_ratio=0.666516 | 18/18;ratio<=2.0 | stable |
| matched_effort_path_segmentation_stability | pass | 6/6;max_ratio=0.180595 | 6/6;ratio<=2.0 | stable |
| observed_spectrum_and_effect_exclusion | pass | source_spectra=0;observed_effect_metrics=0 | 0;0 | effect_blind |
| v16u_overall | v16u_footprint_null_centers_stable_under_exact_matched_effort | integrity=1;effort=1;length=1;path=1 | 1;1;1;1 | v16u_footprint_null_centers_stable_under_exact_matched_effort |

## Evidential boundary

A pass supports null-center stability under the tested exact realized lengths and prefix-matched segmentation. It does not prove irreducibility, mixing time, convergence, stationarity, independence, representativeness, uniform sampling, or independence from every alternative null construction.

V16u does not re-evaluate the v16s observed spectrum contrast. It establishes no dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, invariant, or physical law.
