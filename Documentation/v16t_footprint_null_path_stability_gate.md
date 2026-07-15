# v16t footprint-null path stability gate

Status: `v16t_footprint_null_centers_stable_across_tested_paths`.

V16t is an effect-blind stability test of the v16q event-footprint null on the six frozen fresh v16s histories. It compares null ensembles across direct chain lengths and a segmented two-stage path. The source DAG interval spectrum and every observed/null effect statistic are excluded by design.

Specification digest: `18e6b581cb02677aae4469c285f45a0b2d2f93ae63ae5edbe0fed48b86b568a7`.

## Frozen design

Each source DAG has `16` independent nulls under each of four protocols: direct multipliers `0.075`, `0.100`, `0.200`, and staged `0.100 + 0.100`. The attempt ceiling is `240` per edge per stage.

A comparison passes only when its center Jensen-Shannon divergence is at most `2.0` times the pooled median leave-one-out divergence. Every source DAG must pass.

## Protocol summaries

| growth_seed | run_offset | protocol | median_leave_one_out_js | mean_tail_mass_ge_8 | min_changed_edge_fraction | min_actual_resource_conflict_edge_fraction | all_perturbation_integrity_pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9299.000000 | 123078.000000 | direct_short_0075 | 0.000338 | 0.816113 | 0.100055 | 0.899945 | 1.000000 |
| 9299.000000 | 123078.000000 | direct_reference_0100 | 0.000529 | 0.815335 | 0.100055 | 0.899945 | 1.000000 |
| 9299.000000 | 123078.000000 | direct_long_0200 | 0.000480 | 0.816983 | 0.100055 | 0.899945 | 1.000000 |
| 9299.000000 | 123078.000000 | staged_long_0100x2 | 0.000288 | 0.820732 | 0.115215 | 0.875965 | 1.000000 |
| 9299.000000 | 123403.000000 | direct_short_0075 | 0.000310 | 0.844217 | 0.100168 | 0.900112 | 1.000000 |
| 9299.000000 | 123403.000000 | direct_reference_0100 | 0.000307 | 0.841027 | 0.100168 | 0.900112 | 1.000000 |
| 9299.000000 | 123403.000000 | direct_long_0200 | 0.000597 | 0.844625 | 0.100168 | 0.900112 | 1.000000 |
| 9299.000000 | 123403.000000 | staged_long_0100x2 | 0.000321 | 0.848597 | 0.117795 | 0.872132 | 1.000000 |
| 9299.000000 | 127341.000000 | direct_short_0075 | 0.000512 | 0.838755 | 0.100199 | 0.900937 | 1.000000 |
| 9299.000000 | 127341.000000 | direct_reference_0100 | 0.000375 | 0.836974 | 0.100199 | 0.899801 | 1.000000 |
| 9299.000000 | 127341.000000 | direct_long_0200 | 0.000454 | 0.835896 | 0.100199 | 0.900653 | 1.000000 |
| 9299.000000 | 127341.000000 | staged_long_0100x2 | 0.000567 | 0.842796 | 0.128016 | 0.860914 | 1.000000 |
| 9365.000000 | 123078.000000 | direct_short_0075 | 0.000566 | 0.815816 | 0.100084 | 0.899916 | 1.000000 |
| 9365.000000 | 123078.000000 | direct_reference_0100 | 0.000541 | 0.813227 | 0.100084 | 0.900196 | 1.000000 |
| 9365.000000 | 123078.000000 | direct_long_0200 | 0.000567 | 0.816241 | 0.100084 | 0.899075 | 1.000000 |
| 9365.000000 | 123078.000000 | staged_long_0100x2 | 0.000393 | 0.822673 | 0.130362 | 0.856742 | 1.000000 |
| 9365.000000 | 123403.000000 | direct_short_0075 | 0.001055 | 0.860602 | 0.100166 | 0.900943 | 1.000000 |
| 9365.000000 | 123403.000000 | direct_reference_0100 | 0.001154 | 0.860452 | 0.100166 | 0.901498 | 1.000000 |
| 9365.000000 | 123403.000000 | direct_long_0200 | 0.001088 | 0.861922 | 0.100166 | 0.901498 | 1.000000 |
| 9365.000000 | 123403.000000 | staged_long_0100x2 | 0.000928 | 0.870142 | 0.116260 | 0.874029 | 1.000000 |
| 9365.000000 | 127341.000000 | direct_short_0075 | 0.000303 | 0.817315 | 0.100084 | 0.899916 | 1.000000 |
| 9365.000000 | 127341.000000 | direct_reference_0100 | 0.000547 | 0.816061 | 0.100084 | 0.899916 | 1.000000 |
| 9365.000000 | 127341.000000 | direct_long_0200 | 0.000280 | 0.817427 | 0.100084 | 0.895456 | 1.000000 |
| 9365.000000 | 127341.000000 | staged_long_0100x2 | 0.000360 | 0.823198 | 0.123223 | 0.870086 | 1.000000 |

## Null-center comparisons

| growth_seed | run_offset | comparison | center_jensen_shannon | pooled_median_leave_one_out_js | center_shift_ratio | stability_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 9299.000000 | 123078.000000 | short_vs_reference | 0.000029 | 0.000409 | 0.069807 | 1.000000 |
| 9299.000000 | 123078.000000 | reference_vs_long | 0.000082 | 0.000511 | 0.160088 | 1.000000 |
| 9299.000000 | 123078.000000 | direct_long_vs_staged_long | 0.000060 | 0.000366 | 0.164763 | 1.000000 |
| 9299.000000 | 123403.000000 | short_vs_reference | 0.000046 | 0.000307 | 0.149293 | 1.000000 |
| 9299.000000 | 123403.000000 | reference_vs_long | 0.000063 | 0.000447 | 0.141707 | 1.000000 |
| 9299.000000 | 123403.000000 | direct_long_vs_staged_long | 0.000092 | 0.000446 | 0.205402 | 1.000000 |
| 9299.000000 | 127341.000000 | short_vs_reference | 0.000062 | 0.000430 | 0.142977 | 1.000000 |
| 9299.000000 | 127341.000000 | reference_vs_long | 0.000092 | 0.000387 | 0.237211 | 1.000000 |
| 9299.000000 | 127341.000000 | direct_long_vs_staged_long | 0.000242 | 0.000503 | 0.481278 | 1.000000 |
| 9365.000000 | 123078.000000 | short_vs_reference | 0.000017 | 0.000541 | 0.030688 | 1.000000 |
| 9365.000000 | 123078.000000 | reference_vs_long | 0.000014 | 0.000551 | 0.026188 | 1.000000 |
| 9365.000000 | 123078.000000 | direct_long_vs_staged_long | 0.000701 | 0.000479 | 1.463604 | 1.000000 |
| 9365.000000 | 123403.000000 | short_vs_reference | 0.000119 | 0.001128 | 0.105640 | 1.000000 |
| 9365.000000 | 123403.000000 | reference_vs_long | 0.000141 | 0.001154 | 0.121926 | 1.000000 |
| 9365.000000 | 123403.000000 | direct_long_vs_staged_long | 0.000641 | 0.000967 | 0.662739 | 1.000000 |
| 9365.000000 | 127341.000000 | short_vs_reference | 0.000062 | 0.000332 | 0.188010 | 1.000000 |
| 9365.000000 | 127341.000000 | reference_vs_long | 0.000078 | 0.000393 | 0.198833 | 1.000000 |
| 9365.000000 | 127341.000000 | direct_long_vs_staged_long | 0.000184 | 0.000308 | 0.597571 | 1.000000 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| frozen_source_integrity | pass | source_dags=6 | source_dags=6 | continue |
| all_protocol_perturbation_integrity | pass | 384/384 | 384/384 | continue |
| chain_length_null_center_stability | pass | 12/12;max_ratio=0.237211 | 12/12;ratio<=2.0 | stable |
| path_segmentation_null_center_stability | pass | 6/6;max_ratio=1.463604 | 6/6;ratio<=2.0 | stable |
| observed_spectrum_and_effect_exclusion | pass | source_spectra=0;observed_effect_metrics=0 | 0;0 | effect_blind |
| v16t_overall | v16t_footprint_null_centers_stable_across_tested_paths | integrity=1;chain=1;path=1 | 1;1;1 | v16t_footprint_null_centers_stable_across_tested_paths |

## Evidential boundary

A pass supports only procedure-level stability of null centers across these tested finite paths, lengths, seeds, and six source DAGs. It does not establish Markov-chain irreducibility, mixing time, convergence, stationarity, independence, representativeness, or uniform sampling.

Because no source spectrum is computed, v16t neither confirms nor weakens the observed v16s spectrum contrast. It only tests whether that contrast was referenced to a visibly path-sensitive null center.

No dimension, manifoldlikeness, Lorentz symmetry, spacetime, continuum, particle, entanglement, invariant, or physical-law claim is evaluated.
