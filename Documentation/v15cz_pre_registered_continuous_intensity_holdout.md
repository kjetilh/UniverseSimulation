# Relasjonell universgraf v0.15cz: pre-registered continuous intensity holdout

## Formal

Denne runden fryser v15cy genealogy-intensity-scoren foer nye `1024/p1/add_chord` holdout-runs evalueres.
Score-input er genealogy/event/mass-felter. Horizon-felter brukes bare som downstream fasit.

## Pre-registered scope

| field | value |
| --- | --- |
| target | 1024 |
| placement | p1 |
| perturbation | add_chord |
| growth seed | 202 |
| scheduled seed deltas | 8101;8117;8171;8219;8273;8317;8363;8419;8461;8521;8573;8627;8681;8731;8791;8849;8893;8951;9001;9059;9113;9167;9221;9281 |
| primary score | genealogy_intensity_index |
| primary outcome | established vs no_far_shell only; mixed excluded from primary AUC |

## Calibration manifest

| lab | scope | n | targets | placements | labels |
| --- | --- | --- | --- | --- | --- |
| v15cw | calibration_seed_split | 8 | 1024;896 | p1;p3 | established_far_shell_horizon:4;no_far_shell_horizon:4 |
| v15cx | p1_1024_fresh_holdout | 4 | 1024 | p1 | established_far_shell_horizon:3;mixed_far_shell_horizon:1 |

## Frozen score inputs

| feature | min | max | weight |
| --- | --- | --- | --- |
| churn_per_step | 0.011 | 0.506 | 0.125 |
| split_per_step | 0.000 | 0.064 | 0.125 |
| birth_death_per_step | 0.009 | 0.374 | 0.125 |
| max_component_count_per_target | 0.009 | 0.050 | 0.125 |
| max_total_defect_mass_fraction | 0.020 | 0.270 | 0.125 |
| mean_total_defect_mass_fraction | 0.005 | 0.147 | 0.125 |
| post_split_dual_fraction | 0.000 | 0.979 | 0.125 |
| first_split_earliness | 0.000 | 0.988 | 0.125 |

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 1024 | 1024.0 | 1024.0 | 1024.0 | 1 |

## Per-run holdout

| seed | horizon | primary score | pattern | churn | max comps | max mass |
| --- | --- | --- | --- | --- | --- | --- |
| 8101 | established_far_shell_horizon | 0.949 | split_persistent_dual | 1557 | 57 | 311 |
| 8117 | no_far_shell_horizon | 0.293 | split_persistent_dual | 203 | 21 | 47 |
| 8171 | established_far_shell_horizon | 0.773 | split_persistent_dual | 1190 | 35 | 234 |
| 8219 | established_far_shell_horizon | 0.548 | split_persistent_dual | 898 | 44 | 168 |
| 8273 | established_far_shell_horizon | 0.774 | split_persistent_dual | 1078 | 48 | 237 |
| 8317 | established_far_shell_horizon | 0.955 | split_persistent_dual | 1620 | 56 | 264 |
| 8363 | established_far_shell_horizon | 0.789 | split_persistent_dual | 1164 | 38 | 233 |
| 8419 | established_far_shell_horizon | 0.607 | split_persistent_dual | 715 | 47 | 159 |
| 8461 | established_far_shell_horizon | 0.651 | split_persistent_dual | 828 | 39 | 172 |
| 8521 | established_far_shell_horizon | 0.856 | split_persistent_dual | 1166 | 46 | 292 |
| 8573 | established_far_shell_horizon | 0.570 | split_persistent_dual | 707 | 34 | 183 |
| 8627 | established_far_shell_horizon | 0.799 | split_persistent_dual | 1202 | 61 | 236 |
| 8681 | established_far_shell_horizon | 0.640 | split_persistent_dual | 857 | 34 | 176 |
| 8731 | established_far_shell_horizon | 0.359 | split_persistent_dual | 471 | 34 | 74 |
| 8791 | established_far_shell_horizon | 0.621 | split_persistent_dual | 864 | 55 | 183 |
| 8849 | established_far_shell_horizon | 0.872 | split_persistent_dual | 1364 | 44 | 250 |
| 8893 | established_far_shell_horizon | 0.930 | split_persistent_dual | 1568 | 51 | 250 |
| 8951 | mixed_far_shell_horizon | 0.401 | split_fragment | 579 | 29 | 146 |
| 9001 | established_far_shell_horizon | 0.516 | split_persistent_dual | 603 | 48 | 167 |
| 9059 | established_far_shell_horizon | 0.400 | split_persistent_dual | 463 | 27 | 89 |
| 9113 | established_far_shell_horizon | 0.555 | split_fragment | 918 | 44 | 171 |
| 9167 | established_far_shell_horizon | 0.760 | split_persistent_dual | 963 | 40 | 248 |
| 9221 | established_far_shell_horizon | 0.688 | split_persistent_dual | 885 | 46 | 193 |
| 9281 | established_far_shell_horizon | 0.897 | split_persistent_dual | 1491 | 57 | 270 |

## Primary and secondary metrics

| metric | role | decisive | est | no | mixed | AUC | p | delta | span rho |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| genealogy_intensity_index | primary | 23 | 22 | 1 | 1 | 1.000 | 0.043 | 0.412 | 0.126 |
| compress_per_step | secondary | 23 | 22 | 1 | 1 | 0.114 | 0.913 | -0.001 | 0.059 |
| first_split_earliness | secondary | 23 | 22 | 1 | 1 | 0.818 | 0.217 | 0.098 | -0.150 |
| max_component_count_per_target | secondary | 23 | 22 | 1 | 1 | 1.000 | 0.043 | 0.023 | 0.295 |
| churn_per_step | secondary | 23 | 22 | 1 | 1 | 1.000 | 0.043 | 0.241 | 0.178 |
| birth_death_per_step | secondary | 23 | 22 | 1 | 1 | 1.000 | 0.043 | 0.174 | 0.141 |

## Scope summary

- labels: `established_far_shell_horizon:22;mixed_far_shell_horizon:1;no_far_shell_horizon:1`
- patterns: `split_fragment:2;split_persistent_dual:22`
- primary AUC: `1.000`
- primary exact p: `0.043`

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og alle requested add_chord-perturbations matcher faktisk perturbasjon.
- `pre_registration_control`: `frozen_score_applied` fordi Score-spec er fit paa v15cw/v15cx calibration rows og brukt uten refit paa v15cz holdout.
- `primary_test`: `pre_registered_intensity_inconclusive_balance` fordi Ikke nok balansert decisive data for confirmatory test: decisive=23, established=22, no_horizon=1, mixed=1; AUC=1.000, p=0.043.
- `next_step`: `run_pre_registered_extension_or_report_inconclusive` fordi Forleng bare etter den pre-registrerte balanse-regelen; ikke endre score eller metric.

## Tolkning

- Dette er en pre-registrert lokal selector-test, ikke en partikkel-, invariant-, Lorentz- eller entanglement-paastand.
- Sekundaermetrikker kan bare generere nye hypoteser hvis primaerscoren feiler.
- Mixed outcomes er ikke halvpositive i primaertesten.
