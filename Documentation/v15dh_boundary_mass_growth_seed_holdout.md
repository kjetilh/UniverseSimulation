# Relasjonell universgraf v0.15dh: boundary/mass growth-seed holdout

## Formal

Dette er en second-growth-seed holdout av v15df/v15dg-kandidaten.
Primarmetric er fortsatt frosset til `w32_mean_boundary_per_mass` med retning `higher_is_established`.
Target, perturbation, placements og budget holdes fast fra v15dg.
Growth seed flyttes fra 202 til 303.
Statisk supportgeometri rapporteres bare som confound/audit.
Route-entry/retention brukes ikke som candidate feature.

## Pre-registered scope

| field | value |
| --- | --- |
| target | 1024 |
| growth seed | 303 |
| perturbation | add_chord |
| placements | p0;p1;p2 |
| seed deltas | 11003;11057;11113;11171;11239;11311;11383;11447 |
| primary metric | w32_mean_boundary_per_mass |
| static audit | static_mean_support_degree |

## Group summary

| group | n | placements | labels | boundary/mass | static degree | genealogy intensity | mean horizon |
| --- | --- | --- | --- | --- | --- | --- | --- |
| non_decisive | 1 | p2:1 | mixed_far_shell_horizon:1 | 5.500 | 6.000 | 0.504 | 22.000 |
| other_established | 8 | p0:4;p2:4 | established_far_shell_horizon:8 | 5.483 | 6.333 | 0.632 | 172.000 |
| other_no_horizon | 8 | p1:8 | no_far_shell_horizon:8 | 6.500 | 9.333 | 0.506 | 0.000 |
| p0_no_horizon_other | 4 | p0:4 | no_far_shell_horizon:4 | 7.000 | 6.667 | 0.057 | 0.000 |
| p2_no_horizon | 3 | p2:3 | no_far_shell_horizon:3 | 4.500 | 6.000 | 0.162 | 0.000 |

## Metric scores

| metric | role | AUC est/no | AUC p1/p0 false | AUC p1/p2 no | median p1 | median p0 false | median p2 no |
| --- | --- | --- | --- | --- | --- | --- | --- |
| w32_mean_boundary_per_mass | primary_frozen_dynamic | 0.463 | nan | nan | nan | nan | 4.500 |
| w32_mean_boundary_to_volume | secondary_same_snapshot | 0.463 | nan | nan | nan | nan | 4.500 |
| w32_mean_total_boundary_edges | secondary_same_snapshot | 0.725 | nan | nan | nan | nan | 11.400 |
| w64_mean_boundary_per_mass | secondary_later_strict | 0.438 | nan | nan | nan | nan | 3.644 |
| w96_mean_boundary_per_mass | secondary_later_strict | 0.229 | nan | nan | nan | nan | 4.115 |
| static_mean_support_degree | static_support_audit | 0.217 | nan | nan | nan | nan | 6.000 |
| static_support_ball_1 | static_support_audit | 0.217 | nan | nan | nan | nan | 14.000 |
| genealogy_intensity_index | baseline_failed_selector | 0.858 | nan | nan | nan | nan | 0.162 |

## Matched seed comparison

| seed | p0 label | p1 label | p2 label | p0 group | p1 group | p2 group | p0 bm | p1 bm | p2 bm | p1-p0 | p1-p2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11003 | established_far_shell_horizon | no_far_shell_horizon | no_far_shell_horizon | other_established | other_no_horizon | p2_no_horizon | 5.467 | 5.900 | 4.500 | 0.433 | 1.400 |
| 11057 | no_far_shell_horizon | no_far_shell_horizon | mixed_far_shell_horizon | p0_no_horizon_other | other_no_horizon | non_decisive | 7.000 | 6.500 | 5.500 | -0.500 | 1.000 |
| 11113 | established_far_shell_horizon | no_far_shell_horizon | established_far_shell_horizon | other_established | other_no_horizon | other_established | 7.200 | 6.500 | 5.013 | -0.700 | 1.487 |
| 11171 | established_far_shell_horizon | no_far_shell_horizon | established_far_shell_horizon | other_established | other_no_horizon | other_established | 7.000 | 6.500 | 4.900 | -0.500 | 1.600 |
| 11239 | no_far_shell_horizon | no_far_shell_horizon | established_far_shell_horizon | p0_no_horizon_other | other_no_horizon | other_established | 7.000 | 6.500 | 5.500 | -0.500 | 1.000 |
| 11311 | no_far_shell_horizon | no_far_shell_horizon | established_far_shell_horizon | p0_no_horizon_other | other_no_horizon | other_established | 7.000 | 6.500 | 4.967 | -0.500 | 1.533 |
| 11383 | no_far_shell_horizon | no_far_shell_horizon | no_far_shell_horizon | p0_no_horizon_other | other_no_horizon | p2_no_horizon | 7.000 | 6.500 | 5.500 | -0.500 | 1.000 |
| 11447 | established_far_shell_horizon | no_far_shell_horizon | no_far_shell_horizon | other_established | other_no_horizon | p2_no_horizon | 8.033 | 5.033 | 3.400 | -3.000 | 1.633 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og requested add_chord-perturbations matcher faktisk perturbasjon.
- `pre_registration`: `frozen_w32_boundary_mass_no_refit` fordi Primarmetric er frosset til `w32_mean_boundary_per_mass` fra v15df/v15dg; growth seed er endret til 303, og route-entry brukes ikke som feature.
- `outcome_balance`: `holdout_label_balance_anchor_changed` fordi Labels: established_far_shell_horizon:8;mixed_far_shell_horizon:1;no_far_shell_horizon:15; p1-established=0, p1-no-horizon=8, p0-established=4, p2-established=4.
- `placement_landscape`: `growth_seed_303_placement_landscape_changed` fordi p1 har 8/8 no-horizon og 0 established, mens p0 har 4 established og p2 har 4 established.
- `primary_result`: `boundary_mass_not_growth_seed_transferable_under_original_anchor` fordi `w32_mean_boundary_per_mass` har AUC=0.463 established-vs-no, og den opprinnelige p1-positive kontrasten finnes ikke paa growth seed 303.
- `static_confound_audit`: `static_support_not_transferable_as_selector` fordi `static_mean_support_degree` har AUC=0.217 established-vs-no; supportgeometrien er fortsatt viktig, men retningen fra v15dg transferer ikke som selector.
- `baseline_check`: `genealogy_intensity_correlates_overall_not_primary` fordi Baseline genealogy-intensity har AUC=0.858 established-vs-no, men er ikke den pre-registrerte primary selector her og skal ikke refittes til claim.
- `next_step`: `compare_growth_seed_support_signatures_before_more_dynamics` fordi Neste steg bor vaere en no-new-dynamics syntese av v15dg/v15dh som sammenligner base/support-signaturer og placement-respons, foer mer label-budget brukes.

## Tolkning

- Dette tester base-state-transfer for en lokal pre-entry observabel; det kan ikke bevise partikler, Lorentz-likhet, entanglement eller global invariant.
- Hvis support-audit fortsatt skiller renere enn dynamikken, er support-confound fortsatt live.
- Hvis boundary/mass faller paa ny growth seed, skal kandidaten nedgraderes til growth-seed-spesifikk observabel.
