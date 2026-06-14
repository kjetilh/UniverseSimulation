# Relasjonell universgraf v0.15de: pre-entry feature synthesis

## Formal

Denne runden bruker ingen ny dynamikk. Den leser v15dd snapshot-loggen og tester faste tidlige vinduer.
Vinduer `<=96` er strict pre-entry fordi tidligste p1 established sustained high3-entry er step `104`.
Senere vinduer rapporteres, men regnes som entry-risk og skal ikke brukes som selector-claim alene.

## Window summary

| window | class | best metric | AUC p1/p0 false | AUC est/no | direction |
| --- | --- | --- | --- | --- | --- |
| 64 | strict_pre_entry | w64_component_count_slope_per_100 | 0.550 | 0.545 | higher_is_established |
| 96 | strict_pre_entry | w96_mean_outer_share | 0.560 | 0.617 | higher_is_established |
| 128 | entry_risk_window | w128_largest_component_slope_per_100 | 0.620 | 0.466 | higher_is_established |
| 256 | entry_risk_window | w256_positive_distance_margin_rate | 0.750 | 0.727 | higher_is_established |
| 512 | entry_risk_window | w512_positive_distance_margin_rate | 0.800 | 0.773 | higher_is_established |
| 640 | entry_risk_window | w640_ready_both_rate | 0.800 | 0.834 | higher_is_established |

## Top strict pre-entry metrics

| metric | direction | AUC est/no | AUC p1/p0 false | median p1 | median p0 false | p1-p0 false |
| --- | --- | --- | --- | --- | --- | --- |
| w96_mean_outer_share | higher_is_established | 0.617 | 0.560 | 0.000 | 0.000 | 0.000 |
| w96_max_outer_share | higher_is_established | 0.617 | 0.560 | 0.000 | 0.000 | 0.000 |
| w96_mean_high_share_margin | higher_is_established | 0.617 | 0.560 | -0.680 | -0.680 | 0.000 |
| w96_max_high_share_margin | higher_is_established | 0.617 | 0.560 | -0.680 | -0.680 | 0.000 |
| w96_outer_present_rate | higher_is_established | 0.617 | 0.560 | 0.000 | 0.000 | 0.000 |
| w64_component_count_slope_per_100 | higher_is_established | 0.545 | 0.550 | 0.000 | 0.000 | 0.000 |
| w96_ready_both_rate | higher_is_established | 0.545 | 0.550 | 0.000 | 0.000 | 0.000 |
| w96_outer_share_slope_per_100 | higher_is_established | 0.613 | 0.540 | 0.000 | 0.000 | 0.000 |
| w64_mean_outer_share | higher_is_established | 0.573 | 0.520 | 0.000 | 0.000 | 0.000 |
| w64_max_outer_share | higher_is_established | 0.573 | 0.520 | 0.000 | 0.000 | 0.000 |
| w64_mean_high_share_margin | higher_is_established | 0.573 | 0.520 | -0.680 | -0.680 | 0.000 |
| w64_max_high_share_margin | higher_is_established | 0.573 | 0.520 | -0.680 | -0.680 | 0.000 |
| w64_outer_present_rate | higher_is_established | 0.573 | 0.520 | 0.000 | 0.000 | 0.000 |
| w64_outer_share_slope_per_100 | higher_is_established | 0.573 | 0.520 | 0.000 | 0.000 | 0.000 |
| w64_mean_weighted_distance | higher_is_established | 0.613 | 0.500 | 0.000 | 0.000 | 0.000 |
| w64_mean_high_distance_margin | higher_is_established | 0.613 | 0.500 | -6.000 | -6.000 | 0.000 |
| w64_distance_slope_per_100 | higher_is_established | 0.605 | 0.500 | 0.000 | 0.000 | 0.000 |
| w64_max_weighted_distance | higher_is_established | 0.603 | 0.500 | 0.000 | 0.000 | 0.000 |
| w64_max_high_distance_margin | higher_is_established | 0.603 | 0.500 | -6.000 | -6.000 | 0.000 |
| w64_route_readiness_index | higher_is_established | 0.601 | 0.500 | 0.000 | 0.000 | 0.000 |

## Top entry-risk metrics

| metric | window | direction | AUC est/no | AUC p1/p0 false | median p1 | median p0 false |
| --- | --- | --- | --- | --- | --- | --- |
| w640_ready_both_rate | 640 | higher_is_established | 0.834 | 0.800 | 0.377 | 0.000 |
| w512_positive_distance_margin_rate | 512 | higher_is_established | 0.773 | 0.800 | 0.315 | 0.000 |
| w640_positive_distance_margin_rate | 640 | higher_is_established | 0.773 | 0.800 | 0.383 | 0.000 |
| w512_ready_both_rate | 512 | higher_is_established | 0.794 | 0.780 | 0.323 | 0.000 |
| w640_mid_or_high_rate | 640 | higher_is_established | 0.794 | 0.780 | 0.321 | 0.000 |
| w640_outer_pressure_without_high_rate | 640 | lower_is_established | 0.427 | 0.770 | 0.173 | 0.667 |
| w256_positive_distance_margin_rate | 256 | higher_is_established | 0.727 | 0.750 | 0.076 | 0.000 |
| w256_ready_both_rate | 256 | higher_is_established | 0.727 | 0.750 | 0.061 | 0.000 |
| w256_mid_or_high_rate | 256 | higher_is_established | 0.727 | 0.750 | 0.015 | 0.000 |
| w512_high_rate | 512 | higher_is_established | 0.727 | 0.750 | 0.062 | 0.000 |
| w640_high_rate | 640 | higher_is_established | 0.727 | 0.750 | 0.148 | 0.000 |
| w512_outer_pressure_without_high_rate | 512 | lower_is_established | 0.393 | 0.750 | 0.169 | 0.585 |
| w640_max_outer_share | 640 | higher_is_established | 0.773 | 0.740 | 0.725 | 0.429 |
| w640_max_high_share_margin | 640 | higher_is_established | 0.773 | 0.740 | 0.045 | -0.251 |
| w512_mid_or_high_rate | 512 | higher_is_established | 0.749 | 0.740 | 0.262 | 0.000 |

## Operativ lesning

- `data_scope`: `no_new_dynamics_v15dd_only` fordi Analysen leser bare v15dd snapshot-log og run-summary.
- `leakage_guard`: `strict_windows_le_96` fordi Tidligste p1 established sustained high3 entry i v15dd er step 104; vinduer <=96 er strict pre-entry.
- `primary_result`: `pre_entry_feature_not_found` fordi Beste strict pre-entry feature `w96_mean_outer_share` har AUC=0.560.
- `entry_risk_best`: `w640_ready_both_rate` fordi Beste senere vindu har AUC=0.800 mot p0 false positives og skal behandles som entry-risk, ikke claim.
- `baseline_check`: `genealogy_intensity_still_not_selector` fordi Baseline genealogy-intensity har AUC=0.280 mot p0 false positives.
- `next_step`: `seek_non_route_pre_entry_observable` fordi Route-loggen forklarer outcome, men gir ikke tidlig selector under strict-vindu.

## Tolkning

- Strict pre-entry-vinduer kan bli selector-kandidater hvis de er sterke nok.
- Entry-risk-vinduer kan forklare mekanismen, men maa ikke behandles som pre-entry predictors.
- Ikke oppgrader til partikler, Lorentz-likhet, entanglement, invariant eller universell geometri.
