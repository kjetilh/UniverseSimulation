# Relasjonell universgraf v0.15dm: frozen return-probability morphology holdout

## Formal

Dette er en liten fresh growth-seed holdout av v15dl sin beste morfologi-scout.
Ranking beregnes fra basegraf/add_chord-probe foer dynamikk og skrives til CSV foer run-loop.
Dynamiske observabler rapporteres etterpaa som evaluering/audit, ikke som refit.

## Pre-registered scope

| field | value |
| --- | --- |
| target | 1024 |
| growth_seed | 505 |
| perturbation | add_chord |
| placements | p0;p1;p2 |
| seed_deltas | 13007;13063;13127;13187 |
| rank_metric | delta_return_t2 |
| rank_direction | higher_is_better |
| rank_tiebreak | delta_return_t4 |

## Pre-run morphology ranking

| pre_run_primary_rank | placement | support_signature | delta_return_t2 | delta_return_t4 | delta_return_t6 | base_return_spectral_dim_proxy |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 5,98,599 | -0.020 | -0.011 | -0.006 | 2.149 |
| 2 | 1 | 7,8,9 | -0.025 | -0.027 | -0.027 | 1.061 |
| 3 | 2 | 13,14,263 | -0.033 | -0.025 | -0.019 | 1.464 |

## Placement outcomes

| pre_run_primary_rank | placement | label_counts | established_rate | mean_horizon_span | median_boundary_mass | median_genealogy_intensity |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | established_far_shell_horizon:3;no_far_shell_horizon:1 | 0.750 | 129.000 | 4.000 | 0.700 |
| 2 | 1 | established_far_shell_horizon:1;no_far_shell_horizon:3 | 0.250 | 43.000 | 6.000 | 0.238 |
| 3 | 2 | established_far_shell_horizon:3;no_far_shell_horizon:1 | 0.750 | 129.000 | 4.117 | 0.585 |

## Morphology-scout evaluation

| key | value | evidence |
| --- | --- | --- |
| primary_rank_metric | delta_return_t2 | direction=higher_is_better; tiebreak=delta_return_t4 |
| pre_registration | morphology_rank_written_before_dynamics | pre-run ranking CSV is written before defect run loop |
| active_threshold | established_rate_ge_0.50 | active placement is evaluated after dynamics, not used in morphology ranking |
| top1_placements | p0 | p0:est=0.750 |
| top2_placements | p0;p1 | p0:est=0.750;p1:est=0.250 |
| contrast_placements | p2 | p2:est=0.750 |
| active_placements | p0;p2 | active_total=2 |
| top1_capture_fraction | 0.500 | captured=1; active_total=2 |
| top2_capture_fraction | 0.500 | captured=1; active_total=2 |
| return_scout_status | return_scout_weak_partial_capture | fresh growth-seed evaluation of the frozen v15dl morphology scout |

## Dynamic metric audit

| metric | role | auc_established_vs_no | median_established_raw | median_no_horizon_raw |
| --- | --- | --- | --- | --- |
| w32_mean_boundary_per_mass | primary_frozen_dynamic | 0.300 | 4.000 | 6.000 |
| w32_mean_boundary_to_volume | secondary_same_snapshot | 0.300 | 4.000 | 6.000 |
| w32_mean_total_boundary_edges | secondary_same_snapshot | 0.357 | 9.200 | 12.000 |
| w64_mean_boundary_per_mass | secondary_later_strict | 0.300 | 4.000 | 6.000 |
| w96_mean_boundary_per_mass | secondary_later_strict | 0.300 | 4.000 | 6.000 |
| static_mean_support_degree | static_support_audit | 0.271 | 8.667 | 9.667 |
| static_support_ball_1 | static_support_audit | 0.271 | 24.000 | 28.000 |
| genealogy_intensity_index | baseline_failed_selector | 1.000 | 0.685 | 0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og requested add_chord-perturbations matcher faktisk perturbasjon.
- `pre_registration`: `return_probability_rank_written_before_dynamics` fordi Pre-run ranking er frosset til `delta_return_t2` high-is-better foer dynamikk-loop.
- `outcome_balance`: `fresh_growth_seed_label_balance_recorded` fordi Labels: established_far_shell_horizon:7;no_far_shell_horizon:5.
- `return_scout_result`: `return_scout_weak_partial_capture` fordi Top1 capture=0.500; top2 capture=0.500. fresh growth-seed evaluation of the frozen v15dl morphology scout
- `dynamic_boundary_mass_audit`: `reported_descriptive_not_primary_selector` fordi `w32_mean_boundary_per_mass` AUC established-vs-no=0.300.
- `next_step`: `return_probability_scout_needs_repeat_or_downgrade` fordi Scout partially captured active placements; too weak for selector language without another fresh seed.

## Tolkning

- Dette er fortsatt en lokal defect/response-test, ikke Lorentz-, invariant-, entanglement- eller partikkel-evidens.
- Hvis return-probability-rankingen treffer, er det en placement-prior som maa replikeres, ikke en fysikklov.
- Hvis den feiler, skal `delta_return_t2` pensjoneres eller nedgraderes til deskriptiv audit.
