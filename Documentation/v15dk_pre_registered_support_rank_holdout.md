# Relasjonell universgraf v0.15dk: pre-registered support-rank holdout

## Formal

Dette er en fresh growth-seed holdout av v15dj sin support-conditioned scout.
Support-rangering beregnes foer dynamikk, skrives til CSV, og brukes deretter som frossen placement-prior.
Dynamiske observabler rapporteres etterpaa som audit, ikke som refit.

## Pre-registered scope

| field | value |
| --- | --- |
| target | 1024 |
| growth_seed | 404 |
| perturbation | add_chord |
| placements | p0;p1;p2 |
| seed_deltas | 12011;12071;12143;12203;12281;12347;12413;12491 |
| rank_metric | support_ball2_minus_ball1 |
| rank_tiebreak | support_ball_3 |

## Pre-run support ranking

| pre_run_primary_rank | placement | support_signature | support_ball2_minus_ball1 | support_ball_3 | mean_support_degree | support_boundary_to_volume |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3,27,434 | 35.000 | 107.000 | 5.333 | 4.000 |
| 2 | 2 | 5,159,1003 | 40.000 | 112.000 | 6.333 | 5.000 |
| 3 | 1 | 12,14,465 | 56.000 | 175.000 | 9.000 | 7.667 |

## Placement outcomes

| pre_run_primary_rank | placement | label_counts | established_rate | mean_horizon_span | median_boundary_mass | median_genealogy_intensity |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | no_far_shell_horizon:8 | 0.000 | 0.000 | 4.500 | 0.476 |
| 2 | 2 | no_far_shell_horizon:8 | 0.000 | 0.000 | 7.500 | 0.449 |
| 3 | 1 | established_far_shell_horizon:4;mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.500 | 103.250 | 6.000 | 0.711 |

## Support-rank evaluation

| key | value | evidence |
| --- | --- | --- |
| primary_rank_metric | support_ball2_minus_ball1 | direction=lower_is_better; tiebreak=support_ball_3 |
| active_threshold | established_rate_ge_0.50 | active placement is evaluated after dynamics, not used in support ranking |
| top1_placements | p0 | p0:est=0.000 |
| top2_placements | p0;p2 | p0:est=0.000;p2:est=0.000 |
| contrast_placements | p1 | p1:est=0.500 |
| active_placements | p1 | active_total=1 |
| top1_capture_fraction | 0.000 | captured=0; active_total=1 |
| top2_capture_fraction | 0.000 | captured=0; active_total=1 |
| support_rank_status | support_rank_not_supported | fresh growth-seed evaluation of the pre-run ranking |

## Dynamic metric audit

| metric | role | auc_established_vs_no | median_established_raw | median_no_horizon_raw |
| --- | --- | --- | --- | --- |
| w32_mean_boundary_per_mass | primary_frozen_dynamic | 0.526 | 6.083 | 6.000 |
| w32_mean_boundary_to_volume | secondary_same_snapshot | 0.526 | 6.083 | 6.000 |
| w32_mean_total_boundary_edges | secondary_same_snapshot | 0.711 | 16.000 | 12.000 |
| w64_mean_boundary_per_mass | secondary_later_strict | 0.507 | 5.486 | 5.704 |
| w96_mean_boundary_per_mass | secondary_later_strict | 0.526 | 5.341 | 5.385 |
| static_mean_support_degree | static_support_audit | 0.921 | 9.000 | 6.333 |
| static_support_ball_1 | static_support_audit | 0.921 | 24.000 | 17.000 |
| genealogy_intensity_index | baseline_failed_selector | 0.947 | 0.833 | 0.461 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og requested add_chord-perturbations matcher faktisk perturbasjon.
- `pre_registration`: `support_rank_written_before_dynamics` fordi Pre-run ranking er frosset til `support_ball2_minus_ball1` lower-is-better med `support_ball_3` som tiebreak foer dynamikk-loop.
- `outcome_balance`: `fresh_growth_seed_label_balance_recorded` fordi Labels: established_far_shell_horizon:4;mixed_far_shell_horizon:1;no_far_shell_horizon:19.
- `support_rank_result`: `support_rank_not_supported` fordi Top1 capture=0.000; top2 capture=0.000. fresh growth-seed evaluation of the pre-run ranking
- `dynamic_boundary_mass_audit`: `reported_descriptive_not_primary_selector` fordi `w32_mean_boundary_per_mass` AUC established-vs-no=0.526; dette er audit etter support-rankingen, ikke en refittet selector.
- `next_step`: `retire_support_rank_as_selector_candidate` fordi Pre-run support-rankingen traff ikke; gaa tilbake til observabeldesign eller skala/placement-landskap.

## Tolkning

- Dette er fortsatt en lokal defect/response-test, ikke Lorentz-, invariant-, entanglement- eller partikkel-evidens.
- Hvis support-rankingen treffer, er det en placement-prior som maa replikeres, ikke en fysikklov.
- Hvis support-rankingen feiler, skal v15dj-scouten pensjoneres eller nedgraderes til deskriptiv audit.
