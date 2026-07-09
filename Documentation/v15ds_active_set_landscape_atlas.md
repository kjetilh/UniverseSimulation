# Relasjonell universgraf v0.15ds: active-set landscape atlas

## Formal

Dette er et fresh active-set landskapsatlas etter v15dr.
Mapperen fra v15dr refittes ikke. Primarproduktet er klassefrekvens, klasse-novelty og per-seed active-set.
Pre-run morphology skrives foer dynamikk-loop, men brukes bare som auditgrunnlag.

## Pre-registered scope

| field | value |
| --- | --- |
| target | 1024 |
| growth_seeds | 1201;1301;1409;1511;1601;1709 |
| perturbation | add_chord |
| placements | p0;p1;p2 |
| seed_deltas | 18107;18161;18223;18289 |
| active_threshold | established_rate_ge_0.50 |
| atlas_source | v15ds_fresh_active_set_landscape_atlas_after_failed_v15dr_mapper |

## Seed-level atlas

| growth_seed | landscape_class | active_placements | class_seen_before_v15ds | new_class_in_v15ds | placement_rates | strongest_placement | strongest_established_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1201 | single_active_p2 | p2 | 1 | 0 | p0:0.250;p1:0.250;p2:1.000 | p2 | 1.000 |
| 1301 | single_active_p2 | p2 | 1 | 0 | p0:0.000;p1:0.000;p2:0.500 | p2 | 0.500 |
| 1409 | no_active | none | 1 | 0 | p0:0.000;p1:0.000;p2:0.000 | p0 | 0.000 |
| 1511 | multi_active_p0_p2 | p0;p2 | 1 | 0 | p0:0.500;p1:0.250;p2:1.000 | p2 | 1.000 |
| 1601 | multi_active_p0_p2 | p0;p2 | 1 | 0 | p0:0.500;p1:0.000;p2:0.500 | p0 | 0.500 |
| 1709 | single_active_p1 | p1 | 1 | 0 | p0:0.000;p1:0.500;p2:0.000 | p1 | 0.500 |

## v15ds class frequencies

| landscape_class | n_seeds | seed_fraction | growth_seeds | median_p0_established_rate | median_p1_established_rate | median_p2_established_rate |
| --- | --- | --- | --- | --- | --- | --- |
| multi_active_p0_p2 | 2 | 0.333 | 1511;1601 | 0.500 | 0.125 | 0.750 |
| single_active_p2 | 2 | 0.333 | 1201;1301 | 0.125 | 0.125 | 0.750 |
| no_active | 1 | 0.167 | 1409 | 0.000 | 0.000 | 0.000 |
| single_active_p1 | 1 | 0.167 | 1709 | 0.000 | 0.500 | 0.000 |

## Combined class frequencies

| landscape_class | n_seeds | seed_fraction | growth_seeds | active_placements_examples |
| --- | --- | --- | --- | --- |
| multi_active_p0_p2 | 4 | 0.250 | 303;505;1511;1601 | p0;p2 |
| single_active_p2 | 4 | 0.250 | 808;1001;1201;1301 | p2 |
| no_active | 3 | 0.188 | 606;909;1409 | none |
| single_active_p1 | 3 | 0.188 | 202;404;1709 | p1 |
| multi_active_p0_p1 | 1 | 0.062 | 1103 | p0;p1 |
| single_active_p0 | 1 | 0.062 | 707 | p0 |

## Placement outcomes

| growth_seed | placement | label_counts | established_rate | active_placement | median_boundary_mass | median_genealogy_intensity |
| --- | --- | --- | --- | --- | --- | --- |
| 1201 | 0 | established_far_shell_horizon:1;no_far_shell_horizon:3 | 0.250 | 0 | 1.267 | 0.229 |
| 1201 | 1 | established_far_shell_horizon:1;no_far_shell_horizon:3 | 0.250 | 0 | 8.760 | 0.907 |
| 1201 | 2 | established_far_shell_horizon:4 | 1.000 | 1 | 8.000 | 0.539 |
| 1301 | 0 | no_far_shell_horizon:4 | 0.000 | 0 | 6.000 | 0.423 |
| 1301 | 1 | no_far_shell_horizon:4 | 0.000 | 0 | 4.500 | 0.136 |
| 1301 | 2 | established_far_shell_horizon:2;no_far_shell_horizon:2 | 0.500 | 1 | 7.000 | 0.493 |
| 1409 | 0 | no_far_shell_horizon:4 | 0.000 | 0 | 8.000 | 0.601 |
| 1409 | 1 | no_far_shell_horizon:4 | 0.000 | 0 | 8.500 | 0.713 |
| 1409 | 2 | mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.000 | 0 | 3.500 | 0.430 |
| 1511 | 0 | established_far_shell_horizon:2;mixed_far_shell_horizon:1;no_far_shell_horizon:1 | 0.500 | 1 | 5.000 | 0.609 |
| 1511 | 1 | established_far_shell_horizon:1;no_far_shell_horizon:3 | 0.250 | 0 | 9.000 | 0.516 |
| 1511 | 2 | established_far_shell_horizon:4 | 1.000 | 1 | 6.000 | 0.410 |
| 1601 | 0 | established_far_shell_horizon:2;mixed_far_shell_horizon:1;no_far_shell_horizon:1 | 0.500 | 1 | 15.500 | 0.416 |
| 1601 | 1 | no_far_shell_horizon:4 | 0.000 | 0 | 9.000 | 0.480 |
| 1601 | 2 | established_far_shell_horizon:2;no_far_shell_horizon:2 | 0.500 | 1 | 6.640 | 0.266 |
| 1709 | 0 | no_far_shell_horizon:4 | 0.000 | 0 | 5.667 | 0.738 |
| 1709 | 1 | established_far_shell_horizon:2;no_far_shell_horizon:2 | 0.500 | 1 | 4.500 | 0.535 |
| 1709 | 2 | no_far_shell_horizon:4 | 0.000 | 0 | 8.000 | 0.624 |

## Atlas evaluation

| key | value | evidence |
| --- | --- | --- |
| atlas_source | v15ds_fresh_active_set_landscape_atlas_after_failed_v15dr_mapper | fresh growth-seed class-frequency atlas; no selector prediction |
| seed_count | 6 | 1201;1301;1409;1511;1601;1709 |
| prior_class_count | 6 | multi_active_p0_p1;multi_active_p0_p2;no_active;single_active_p0;single_active_p1;single_active_p2 |
| v15ds_class_count | 4 | multi_active_p0_p2;no_active;single_active_p1;single_active_p2 |
| new_class_count | 0 | none |
| new_seed_fraction | 0.000 | new_seed_count=0; known_seed_count=6 |
| active_seed_fraction | 0.833 | active_seed_count=5; no_active_seed_count=1 |
| repeated_classes_within_v15ds | multi_active_p0_p2;single_active_p2 | classes with at least two v15ds growth seeds |
| combined_repeated_classes | multi_active_p0_p2;single_active_p2;no_active;single_active_p1 | classes with at least two seeds across v15dq+v15dr+v15ds |
| atlas_status | class_frequency_atlas_stabilizing | class-frequency atlas status; not a selector metric |

## Dynamic metric audit

| metric | role | auc_established_vs_no | median_established_raw | median_no_horizon_raw |
| --- | --- | --- | --- | --- |
| w32_mean_boundary_per_mass | primary_frozen_dynamic | 0.483 | 6.000 | 7.000 |
| w32_mean_boundary_to_volume | secondary_same_snapshot | 0.483 | 6.000 | 7.000 |
| w32_mean_total_boundary_edges | secondary_same_snapshot | 0.521 | 14.600 | 16.000 |
| w64_mean_boundary_per_mass | secondary_later_strict | 0.491 | 6.000 | 6.772 |
| w96_mean_boundary_per_mass | secondary_later_strict | 0.488 | 6.000 | 6.326 |
| static_mean_support_degree | static_support_audit | 0.288 | 6.333 | 9.000 |
| static_support_ball_1 | static_support_audit | 0.293 | 18.000 | 24.000 |
| genealogy_intensity_index | baseline_failed_selector | 0.595 | 0.577 | 0.480 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og requested add_chord-perturbations matcher faktisk perturbasjon.
- `atlas_design`: `class_frequency_atlas_no_selector` fordi Denne runden skriver pre-run morphology, men bruker ikke pre-run features som prediksjon eller refit.
- `outcome_balance`: `fresh_growth_seed_taxonomy_recorded` fordi Run labels: established_far_shell_horizon:21;mixed_far_shell_horizon:3;no_far_shell_horizon:48. Seed classes: multi_active_p0_p2:2;no_active:1;single_active_p1:1;single_active_p2:2.
- `class_landscape_result`: `class_frequency_atlas_stabilizing` fordi new_class_count=0; new_seed_fraction=0.000; repeated_within_v15ds=multi_active_p0_p2;single_active_p2.
- `dynamic_boundary_mass_audit`: `reported_descriptive_not_primary_selector` fordi `w32_mean_boundary_per_mass` AUC established-vs-no=0.483.
- `next_step`: `stratify_next_selector_by_repeated_classes` fordi Atlaset viser repeterte klasser med begrenset novelty; neste selector bor vaere OOD-first og klasse-stratifisert.

## Tolkning

- Dette er en klassefrekvensrunde, ikke en ny selector.
- Repeterte klasser er nyttige som atlasstruktur, men er ikke partikler eller universelle arter.
- Hvis nye klasser dukker opp i senere atlasrunder, betyr det at active-set-rommet fortsatt ekspanderer under fresh growth seeds.
- Ikke oppgrader dette til invariant/Lorentz/partikkel/entanglement-claim.
