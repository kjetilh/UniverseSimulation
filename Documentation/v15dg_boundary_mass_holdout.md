# Relasjonell universgraf v0.15dg: boundary/mass holdout

## Formal

Dette er en fresh dynamisk holdout av v15df-kandidaten.
Primarmetric er frosset til `w32_mean_boundary_per_mass` med retning `higher_is_established`.
Statisk supportgeometri rapporteres bare som confound/audit.
Route-entry/retention brukes ikke som candidate feature.

## Pre-registered scope

| field | value |
| --- | --- |
| target | 1024 |
| growth seed | 202 |
| perturbation | add_chord |
| placements | p0;p1;p2 |
| seed deltas | 10091;10133;10177;10223;10271;10331;10391;10453 |
| primary metric | w32_mean_boundary_per_mass |
| static audit | static_mean_support_degree |

## Group summary

| group | n | placements | labels | boundary/mass | static degree | genealogy intensity | mean horizon |
| --- | --- | --- | --- | --- | --- | --- | --- |
| non_decisive | 2 | p2:2 | mixed_far_shell_horizon:2 | 7.437 | 8.667 | 0.757 | 30.500 |
| other_no_horizon | 1 | p1:1 | no_far_shell_horizon:1 | 13.500 | 10.000 | 0.379 | 0.000 |
| p0_high_score_no_horizon | 8 | p0:8 | no_far_shell_horizon:8 | 11.125 | 9.333 | 0.740 | 0.000 |
| p1_established | 7 | p1:7 | established_far_shell_horizon:7 | 13.500 | 10.000 | 0.879 | 156.286 |
| p2_no_horizon | 6 | p2:6 | no_far_shell_horizon:6 | 8.500 | 8.667 | 0.116 | 0.000 |

## Metric scores

| metric | role | AUC est/no | AUC p1/p0 false | AUC p1/p2 no | median p1 | median p0 false | median p2 no |
| --- | --- | --- | --- | --- | --- | --- | --- |
| w32_mean_boundary_per_mass | primary_frozen_dynamic | 0.857 | 0.821 | 1.000 | 13.500 | 11.125 | 8.500 |
| w32_mean_boundary_to_volume | secondary_same_snapshot | 0.857 | 0.821 | 1.000 | 13.500 | 11.125 | 8.500 |
| w32_mean_total_boundary_edges | secondary_same_snapshot | 0.895 | 0.875 | 1.000 | 27.000 | 24.100 | 17.000 |
| w64_mean_boundary_per_mass | secondary_later_strict | 0.810 | 0.750 | 1.000 | 11.796 | 9.204 | 8.500 |
| w96_mean_boundary_per_mass | secondary_later_strict | 0.705 | 0.696 | 0.810 | 10.746 | 8.580 | 8.481 |
| static_mean_support_degree | static_support_audit | 0.967 | 1.000 | 1.000 | 10.000 | 9.333 | 8.667 |
| static_support_ball_1 | static_support_audit | 0.967 | 1.000 | 1.000 | 27.000 | 26.000 | 24.000 |
| genealogy_intensity_index | baseline_failed_selector | 0.800 | 0.679 | 0.952 | 0.879 | 0.740 | 0.116 |

## Matched seed comparison

| seed | p0 label | p1 label | p2 label | p0 group | p1 group | p2 group | p0 bm | p1 bm | p2 bm | p1-p0 | p1-p2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10091 | no_far_shell_horizon | established_far_shell_horizon | mixed_far_shell_horizon | p0_high_score_no_horizon | p1_established | non_decisive | 8.800 | 10.400 | 6.373 | 1.600 | 4.027 |
| 10133 | no_far_shell_horizon | no_far_shell_horizon | no_far_shell_horizon | p0_high_score_no_horizon | other_no_horizon | p2_no_horizon | 12.000 | 13.500 | 8.500 | 1.500 | 5.000 |
| 10177 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | p0_high_score_no_horizon | p1_established | p2_no_horizon | 12.000 | 13.500 | 8.500 | 1.500 | 5.000 |
| 10223 | no_far_shell_horizon | established_far_shell_horizon | mixed_far_shell_horizon | p0_high_score_no_horizon | p1_established | non_decisive | 8.226 | 10.267 | 8.500 | 2.040 | 1.767 |
| 10271 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | p0_high_score_no_horizon | p1_established | p2_no_horizon | 12.000 | 12.200 | 8.500 | 0.200 | 3.700 |
| 10331 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | p0_high_score_no_horizon | p1_established | p2_no_horizon | 10.850 | 13.500 | 8.500 | 2.650 | 5.000 |
| 10391 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | p0_high_score_no_horizon | p1_established | p2_no_horizon | 8.467 | 13.500 | 8.500 | 5.033 | 5.000 |
| 10453 | no_far_shell_horizon | established_far_shell_horizon | no_far_shell_horizon | p0_high_score_no_horizon | p1_established | p2_no_horizon | 11.400 | 13.500 | 5.967 | 2.100 | 7.533 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og requested add_chord-perturbations matcher faktisk perturbasjon.
- `pre_registration`: `frozen_w32_boundary_mass_no_refit` fordi Primarmetric er frosset til `w32_mean_boundary_per_mass` fra v15df; seed-deltaer er fresh og route-entry brukes ikke som feature.
- `outcome_balance`: `holdout_label_balance` fordi Labels: established_far_shell_horizon:7;mixed_far_shell_horizon:2;no_far_shell_horizon:15; p1-established=7, p0-high-score/no-horizon=8, no_horizon=15.
- `primary_result`: `boundary_mass_holdout_supported` fordi `w32_mean_boundary_per_mass` har AUC=0.821 mot p0 false positives, AUC=0.857 established-vs-no, median p1-p0false delta=2.375.
- `static_confound_audit`: `static_support_reported_not_primary` fordi `static_mean_support_degree` har AUC=1.000 mot p0 false positives og rapporteres som placement/support-audit, ikke dynamisk selector.
- `group_reading`: `p1_vs_p0_false_positive_boundary_mass` fordi p1 median boundary/mass=13.500; p0 false-positive median=11.125; p1 static support degree=10.000; p0 static support degree=9.333.
- `baseline_check`: `genealogy_intensity_control` fordi Baseline genealogy-intensity har AUC=0.679 mot p0 false positives.
- `next_step`: `scale_or_second_growth_seed_with_frozen_boundary_mass` fordi Kandidaten overlever fresh holdout; neste test bor bruke samme frosne metric paa ny growth seed eller naboskala.

## Tolkning

- Dette kan validere eller svekke en lokal pre-entry observabel; det kan ikke bevise partikler, Lorentz-likhet, entanglement eller global invariant.
- Hvis p0 false-positive-gruppen er tynn, er riktig konklusjon balansebegrensning, ikke positivt funn.
- Statisk supportgeometri maa holdes adskilt fra dynamisk boundary/mass.
