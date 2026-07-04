# Relasjonell universgraf v0.15dp: active-set type-guard holdout

## Formal

Dette er en fresh two-growth-seed holdout av en enkelt frossen v15do type-guard.
Guarden beregnes fra basegraf/add_chord-probe foer dynamikk og skrives til CSV foer run-loop.
Dynamiske observabler brukes til evaluering/audit, ikke til refit av guarden.

## Pre-registered scope

| field | value |
| --- | --- |
| target | 1024 |
| growth_seeds | 606;707 |
| perturbation | add_chord |
| placements | p0;p1;p2 |
| seed_deltas | 15007;15061;15121;15187 |
| guard | delta_return_t2/p0_ge_p1 -> p0_p2 else p1_only |

## Pre-run guard

| growth_seed | left_value | right_value | margin_left_minus_right | predicted_type | predicted_active_placements | p0_support_signature | p1_support_signature | p2_support_signature |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 606 | -0.011 | -0.010 | -0.001 | p1_only | p1 | 12,14,30 | 15,16,458 | 7,8,707 |
| 707 | -0.092 | -0.021 | -0.071 | p1_only | p1 | 151,795,884 | 12,13,15 | 13,15,186 |

## Placement outcomes

| growth_seed | placement | guard_metric_value | guard_placement_predicted_active | label_counts | established_rate | active_placement | median_boundary_mass | median_genealogy_intensity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 606 | 0 | -0.011 | 0 | no_far_shell_horizon:4 | 0.000 | 0 | 21.000 | 0.646 |
| 606 | 1 | -0.010 | 1 | no_far_shell_horizon:4 | 0.000 | 0 | 3.500 | 0.220 |
| 606 | 2 | -0.031 | 0 | no_far_shell_horizon:4 | 0.000 | 0 | 6.500 | 0.564 |
| 707 | 0 | -0.092 | 0 | established_far_shell_horizon:3;mixed_far_shell_horizon:1 | 0.750 | 1 | 3.500 | 0.329 |
| 707 | 1 | -0.021 | 1 | no_far_shell_horizon:4 | 0.000 | 0 | 15.500 | 0.629 |
| 707 | 2 | -0.017 | 0 | no_far_shell_horizon:4 | 0.000 | 0 | 8.000 | 0.623 |

## Seed-level guard evaluation

| growth_seed | actual_type | actual_active_placements | predicted_type | predicted_active_placements | type_hit | exact_set_match | placement_rates |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 606 | other | none | p1_only | p1 | 0 | 0 | p0:0.000;p1:0.000;p2:0.000 |
| 707 | other | p0 | p1_only | p1 | 0 | 0 | p0:0.750;p1:0.000;p2:0.000 |

## Aggregate guard evaluation

| key | value | evidence |
| --- | --- | --- |
| guard_rule | delta_return_t2/p0_ge_p1->true=p0_p2;false=p1_only | v15do_best_sorted_posthoc_rule_pre_registered_for_v15dp |
| seed_count | 2 | 606;707 |
| type_accuracy | 0.000 | type_hits=0; seed_count=2 |
| exact_set_match_rate | 0.000 | exact_matches=0; seed_count=2 |
| coverage_fraction | 0.000 | captured=0; active=1; missed=1 |
| precision_fraction | 0.000 | captured=0; predicted=2; false_positive=2 |
| burden_fraction | 0.333 | predicted=2; possible=6 |
| guard_status | guard_inconclusive_unobserved_active_set_type | fresh two-growth-seed active-set type holdout; no refit after dynamics |

## Dynamic metric audit

| metric | role | auc_established_vs_no | median_established_raw | median_no_horizon_raw |
| --- | --- | --- | --- | --- |
| w32_mean_boundary_per_mass | primary_frozen_dynamic | 0.067 | 3.500 | 8.000 |
| w32_mean_boundary_to_volume | secondary_same_snapshot | 0.067 | 3.500 | 8.000 |
| w32_mean_total_boundary_edges | secondary_same_snapshot | 0.067 | 7.000 | 16.000 |
| w64_mean_boundary_per_mass | secondary_later_strict | 0.067 | 3.500 | 8.000 |
| w96_mean_boundary_per_mass | secondary_later_strict | 0.033 | 3.179 | 7.795 |
| static_mean_support_degree | static_support_audit | 0.000 | 3.333 | 13.000 |
| static_support_ball_1 | static_support_audit | 0.000 | 9.000 | 33.000 |
| genealogy_intensity_index | baseline_failed_selector | 0.283 | 0.414 | 0.592 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og requested add_chord-perturbations matcher faktisk perturbasjon.
- `pre_registration`: `type_guard_written_before_dynamics` fordi Guard er frosset til `delta_return_t2/p0_ge_p1` -> `p0_p2` ellers `p1_only`, og pre-run CSV skrives foer dynamikk-loop.
- `outcome_balance`: `fresh_growth_seed_label_balance_recorded` fordi Run labels: established_far_shell_horizon:3;mixed_far_shell_horizon:1;no_far_shell_horizon:20. Actual seed types: other:2.
- `type_guard_result`: `guard_inconclusive_unobserved_active_set_type` fordi type_accuracy=0.000; exact_set_match=0.000; coverage=0.000; precision=0.000.
- `dynamic_boundary_mass_audit`: `reported_descriptive_not_primary_selector` fordi `w32_mean_boundary_per_mass` AUC established-vs-no=0.067.
- `next_step`: `retire_this_type_guard_as_selector_candidate` fordi Den frosne v15do-guarden traff ikke godt nok; ikke refit samme regel etter outcome.

## Tolkning

- Dette er en lokal defect/response holdout av en type-guard, ikke evidens for partikler, Lorentz-likhet, entanglement eller global invariant.
- Treffer guarden, er det en selector-kandidat som maa replikeres paa flere seeds; den er ikke en fysikklov.
- Feiler guarden, skal akkurat denne v15do-regelen pensjoneres eller nedgraderes til deskriptiv kandidatgenerator.
