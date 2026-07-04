# Relasjonell universgraf v0.15dr: active-set taxonomy mapper holdout

## Formal

Dette er en fresh dynamic holdout av en liten taxonomy-mapper etter v15dq.
Mapperen trenes bare paa repeated-class contrasts fra v15dq og kan eksplisitt svare `unknown`.
Pre-run mapper CSV skrives foer dynamikk-loop; dynamiske observabler brukes bare til evaluering og audit.

## Pre-registered scope

| field | value |
| --- | --- |
| target | 1024 |
| growth_seeds | 808;909;1001;1103 |
| perturbation | add_chord |
| placements | p0;p1;p2 |
| seed_deltas | 17011;17053;17107;17167 |
| known_classes | multi_active_p0_p2;single_active_p1 |
| mapper_source | v15dq_repeated_class_contrasts_family_diverse_fixed_before_v15dr |

## Mapper feature spec

| feature | feature_family | high_class | threshold_high_class_if_value_ge | clean_training_separation |
| --- | --- | --- | --- | --- |
| new_edge_mean_forman_p2_minus_p1 | curvature_shortcut | multi_active_p0_p2 | -0.500 | 1 |
| local_ball3_beta1_p2 | local_volume_topology | single_active_p1 | 28.000 | 1 |
| base_return_t2_p1 | return_probability | multi_active_p0_p2 | 0.340 | 1 |
| base_return_t2_p0_minus_p1 | return_probability | single_active_p1 | -0.052 | 1 |
| support_ball_3_p2 | support_volume_topology | single_active_p1 | 109.000 | 1 |
| local_ball3_boundary_to_volume_p0_minus_p1 | local_volume_topology | multi_active_p0_p2 | 0.165 | 1 |

## Pre-run mapper

| growth_seed | predicted_type | predicted_active_placements | mapper_reason | multi_active_p0_p2_votes | single_active_p1_votes | known_envelope_hits | outside_envelope_count | p0_support_signature | p1_support_signature | p2_support_signature |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 808 | multi_active_p0_p2 | p0;p2 | known_class_decisive | 4 | 2 | 5 | 1 | 15,24,264 | 11,475,575 | 23,318,546 |
| 909 | single_active_p1 | p1 | known_class_decisive | 1 | 5 | 6 | 0 | 13,14,139 | 0,2,129 | 12,13,209 |
| 1001 | multi_active_p0_p2 | p0;p2 | known_class_decisive | 4 | 2 | 4 | 2 | 16,36,42 | 9,10,11 | 436,438,836 |
| 1103 | multi_active_p0_p2 | p0;p2 | known_class_decisive | 4 | 2 | 6 | 0 | 0,20,27 | 93,167,541 | 59,260,930 |

## Placement outcomes

| growth_seed | placement | mapper_predicted_type | mapper_placement_predicted_active | label_counts | established_rate | active_placement | median_boundary_mass | median_genealogy_intensity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 808 | 0 | multi_active_p0_p2 | 1 | established_far_shell_horizon:1;no_far_shell_horizon:3 | 0.250 | 0 | 10.000 | 0.633 |
| 808 | 1 | multi_active_p0_p2 | 0 | no_far_shell_horizon:4 | 0.000 | 0 | 12.500 | 0.674 |
| 808 | 2 | multi_active_p0_p2 | 1 | established_far_shell_horizon:2;no_far_shell_horizon:2 | 0.500 | 1 | 8.000 | 0.779 |
| 909 | 0 | single_active_p1 | 0 | mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.000 | 0 | 12.000 | 0.431 |
| 909 | 1 | single_active_p1 | 1 | mixed_far_shell_horizon:2;no_far_shell_horizon:2 | 0.000 | 0 | 7.500 | 0.647 |
| 909 | 2 | single_active_p1 | 0 | mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.000 | 0 | 7.500 | 0.166 |
| 1001 | 0 | multi_active_p0_p2 | 1 | failed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.000 | 0 | 5.500 | 0.244 |
| 1001 | 1 | multi_active_p0_p2 | 0 | no_far_shell_horizon:4 | 0.000 | 0 | 12.000 | 0.463 |
| 1001 | 2 | multi_active_p0_p2 | 1 | established_far_shell_horizon:3;no_far_shell_horizon:1 | 0.750 | 1 | 3.000 | 0.476 |
| 1103 | 0 | multi_active_p0_p2 | 1 | established_far_shell_horizon:2;no_far_shell_horizon:2 | 0.500 | 1 | 8.500 | 0.432 |
| 1103 | 1 | multi_active_p0_p2 | 0 | established_far_shell_horizon:3;no_far_shell_horizon:1 | 0.750 | 1 | 8.000 | 0.828 |
| 1103 | 2 | multi_active_p0_p2 | 1 | no_far_shell_horizon:4 | 0.000 | 0 | 5.500 | 0.229 |

## Seed-level mapper evaluation

| growth_seed | actual_type | actual_active_placements | predicted_type | predicted_active_placements | mapper_reason | known_class_type_hit | ood_correct_abstain | exact_set_match | placement_rates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 808 | single_active_p2 | p2 | multi_active_p0_p2 | p0;p2 | known_class_decisive | 0 | 0 | 0 | p0:0.250;p1:0.000;p2:0.500 |
| 909 | no_active | none | single_active_p1 | p1 | known_class_decisive | 0 | 0 | 0 | p0:0.000;p1:0.000;p2:0.000 |
| 1001 | single_active_p2 | p2 | multi_active_p0_p2 | p0;p2 | known_class_decisive | 0 | 0 | 0 | p0:0.000;p1:0.000;p2:0.750 |
| 1103 | multi_active_p0_p1 | p0;p1 | multi_active_p0_p2 | p0;p2 | known_class_decisive | 0 | 0 | 0 | p0:0.500;p1:0.750;p2:0.000 |

## Aggregate mapper evaluation

| key | value | evidence |
| --- | --- | --- |
| mapper_source | v15dq_repeated_class_contrasts_family_diverse_fixed_before_v15dr | new_edge_mean_forman_p2_minus_p1;local_ball3_beta1_p2;base_return_t2_p1;base_return_t2_p0_minus_p1;support_ball_3_p2;local_ball3_boundary_to_volume_p0_minus_p1 |
| seed_count | 4 | 808;909;1001;1103 |
| known_class_seed_count | 0 | none |
| ood_seed_count | 4 | 808;909;1001;1103 |
| known_class_type_accuracy | nan | known_hits=0; known_rows=0; known_false_ood=0 |
| ood_abstain_accuracy | 0.000 | ood_correct_abstain=0; ood_rows=4; ood_false_known=4 |
| overall_exact_set_match_rate | 0.000 | exact_matches=0; seed_count=4 |
| coverage_fraction | 0.750 | captured=3; active=4; missed=1 |
| precision_fraction | 0.429 | captured=3; predicted=7; false_positive=4 |
| burden_fraction | 0.583 | predicted=7; possible=12 |
| mapper_status | taxonomy_mapper_not_supported | fresh active-set taxonomy mapper holdout; no refit after dynamics |

## Dynamic metric audit

| metric | role | auc_established_vs_no | median_established_raw | median_no_horizon_raw |
| --- | --- | --- | --- | --- |
| w32_mean_boundary_per_mass | primary_frozen_dynamic | 0.354 | 8.000 | 8.250 |
| w32_mean_boundary_to_volume | secondary_same_snapshot | 0.354 | 8.000 | 8.250 |
| w32_mean_total_boundary_edges | secondary_same_snapshot | 0.354 | 16.000 | 17.000 |
| w64_mean_boundary_per_mass | secondary_later_strict | 0.325 | 8.000 | 8.250 |
| w96_mean_boundary_per_mass | secondary_later_strict | 0.321 | 6.833 | 8.250 |
| static_mean_support_degree | static_support_audit | 0.241 | 6.667 | 9.333 |
| static_support_ball_1 | static_support_audit | 0.229 | 18.000 | 25.000 |
| genealogy_intensity_index | baseline_failed_selector | 0.878 | 0.836 | 0.270 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og requested add_chord-perturbations matcher faktisk perturbasjon.
- `pre_registration`: `taxonomy_mapper_written_before_dynamics` fordi Mapperen bruker bare v15dq repeated-class contrasts, skriver pre-run mapper CSV foer run-loop, og refittes ikke etter outcome.
- `outcome_balance`: `fresh_growth_seed_taxonomy_recorded` fordi Run labels: established_far_shell_horizon:11;failed_far_shell_horizon:1;mixed_far_shell_horizon:4;no_far_shell_horizon:32. Actual seed types: multi_active_p0_p1:1;no_active:1;single_active_p2:2. Predicted types: multi_active_p0_p2:3;single_active_p1:1.
- `mapper_result`: `taxonomy_mapper_not_supported` fordi known_class_type_accuracy=nan; ood_abstain_accuracy=0.000; exact_set_match=0.000; coverage=0.750; precision=0.429.
- `dynamic_boundary_mass_audit`: `reported_descriptive_not_primary_selector` fordi `w32_mean_boundary_per_mass` AUC established-vs-no=0.354.
- `next_step`: `retire_this_mapper_or_expand_taxonomy_atlas` fordi Mapperen traff ikke; neste gevinst er trolig mer klassefrekvens/atlas, ikke refit av samme features.

## Tolkning

- Dette tester om active-set-landskapet kan kartlegges bedre enn single-feature guards.
- `unknown` er et legitimt svar hvis fresh seed faller utenfor repeated-class-rommet.
- Ikke oppgrader dette til invariant/Lorentz/partikkel/entanglement-claim.
