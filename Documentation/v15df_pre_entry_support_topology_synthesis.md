# Relasjonell universgraf v0.15df: strict pre-entry support/topology synthesis

## Formal

Denne runden bruker ingen ny dynamikk.
Den leser `v15da` component trajectories og `v15dd` run-summary, men bruker downstream horizon/route-labels bare som evalueringsfasit.
Kandidatfeatures er ikke-route: statisk supportgeometri og komponent/topologi/support-distance i strict vinduer `<=32`, `<=64`, `<=96`.
Primarresultatet bruker strict dynamisk komponent/topologi; statisk supportgeometri rapporteres som confound-/heuristikk-audit.

## Family summary

| family | window | n metrics | best metric | direction | AUC p1/p0 false | AUC est/no | median p1 | median p0 false |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| static_support_geometry | 0 | 9 | static_mean_support_degree | higher_is_established | 1.000 | 0.957 | 10.000 | 9.333 |
| strict_pre_entry_component_topology | 32 | 34 | w32_mean_boundary_per_mass | higher_is_established | 0.960 | 0.864 | 13.500 | 11.200 |
| strict_pre_entry_component_topology | 64 | 34 | w64_mean_boundary_per_mass | higher_is_established | 0.880 | 0.800 | 13.500 | 8.711 |
| strict_pre_entry_component_topology | 96 | 34 | w96_mean_boundary_per_mass | higher_is_established | 0.800 | 0.702 | 13.122 | 8.487 |

## Group summary

| group | n | placements | labels | intensity | static b3/b1 | static b/v | w96 mass | w96 beta1 | w96 boundary/mass | w96 bridge | w96 tension | w96 trapped |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| non_decisive | 2 | p0:1;p1:1 | failed_far_shell_horizon:1;mixed_far_shell_horizon:1 | 0.453 | 5.083 | 8.333 | 2.000 | 0.000 | 12.654 | 0.000 | 0.213 | 1.000 |
| other_established | 1 | p0:1 | established_far_shell_horizon:1 | 0.568 | 6.462 | 8.000 | 4.615 | 0.000 | 6.946 | 0.000 | 0.125 | 0.459 |
| other_no_horizon | 1 | p1:1 | no_far_shell_horizon:1 | 0.467 | 3.704 | 8.667 | 2.000 | 0.000 | 13.500 | 0.000 | 0.213 | 1.000 |
| p0_high_score_no_horizon | 5 | p0:5 | no_far_shell_horizon:5 | 0.816 | 6.462 | 8.000 | 2.846 | 0.000 | 8.487 | 0.000 | 0.156 | 0.694 |
| p0_no_horizon_other | 5 | p0:5 | no_far_shell_horizon:5 | 0.492 | 6.462 | 8.000 | 2.000 | 0.000 | 12.000 | 0.000 | 0.213 | 1.000 |
| p1_established | 10 | p1:10 | established_far_shell_horizon:10 | 0.768 | 3.704 | 8.667 | 2.115 | 0.000 | 13.122 | 0.000 | 0.205 | 0.968 |
| p2_no_horizon | 12 | p2:12 | no_far_shell_horizon:12 | 0.275 | 6.750 | 7.333 | 2.000 | 0.000 | 8.500 | 0.000 | 0.154 | 0.708 |

## Top metrics

| metric | family | window | direction | AUC est/no | AUC p1/p0 false | median p1 | median p0 false | p1-p0 false |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| static_mean_support_degree | static_support_geometry | 0 | higher_is_established | 0.957 | 1.000 | 10.000 | 9.333 | 0.667 |
| static_support_ball_1 | static_support_geometry | 0 | higher_is_established | 0.957 | 1.000 | 27.000 | 26.000 | 1.000 |
| w32_mean_boundary_per_mass | strict_pre_entry_component_topology | 32 | higher_is_established | 0.864 | 0.960 | 13.500 | 11.200 | 2.300 |
| w32_mean_boundary_to_volume | strict_pre_entry_component_topology | 32 | higher_is_established | 0.864 | 0.960 | 13.500 | 11.200 | 2.300 |
| w32_mean_total_boundary_edges | strict_pre_entry_component_topology | 32 | higher_is_established | 0.964 | 0.930 | 27.000 | 24.000 | 3.000 |
| w64_mean_boundary_per_mass | strict_pre_entry_component_topology | 64 | higher_is_established | 0.800 | 0.880 | 13.500 | 8.711 | 4.789 |
| w64_mean_boundary_to_volume | strict_pre_entry_component_topology | 64 | higher_is_established | 0.800 | 0.880 | 13.500 | 8.711 | 4.789 |
| w96_mean_boundary_per_mass | strict_pre_entry_component_topology | 96 | higher_is_established | 0.702 | 0.800 | 13.122 | 8.487 | 4.635 |
| w96_mean_boundary_to_volume | strict_pre_entry_component_topology | 96 | higher_is_established | 0.702 | 0.800 | 13.122 | 8.487 | 4.635 |
| w96_mean_gate_tension_index | strict_pre_entry_component_topology | 96 | higher_is_established | 0.632 | 0.800 | 0.205 | 0.156 | 0.049 |
| w64_mean_gate_tension_index | strict_pre_entry_component_topology | 64 | higher_is_established | 0.644 | 0.780 | 0.213 | 0.164 | 0.049 |
| w64_mean_total_boundary_edges | strict_pre_entry_component_topology | 64 | higher_is_established | 0.941 | 0.770 | 27.000 | 24.000 | 3.000 |
| w64_gate_tension_index_slope_per_100 | strict_pre_entry_component_topology | 64 | higher_is_established | 0.439 | 0.760 | 0.000 | -0.148 | 0.148 |
| w32_mean_gate_tension_index | strict_pre_entry_component_topology | 32 | higher_is_established | 0.715 | 0.720 | 0.213 | 0.198 | 0.014 |
| w96_mean_total_boundary_edges | strict_pre_entry_component_topology | 96 | higher_is_established | 0.919 | 0.700 | 27.000 | 24.000 | 3.000 |
| w32_gate_tension_index_slope_per_100 | strict_pre_entry_component_topology | 32 | higher_is_established | 0.443 | 0.700 | 0.000 | -0.161 | 0.161 |
| w96_gate_tension_index_slope_per_100 | strict_pre_entry_component_topology | 96 | higher_is_established | 0.360 | 0.700 | -0.036 | -0.092 | 0.056 |
| w32_boundary_to_volume_slope_per_100 | strict_pre_entry_component_topology | 32 | higher_is_established | 0.472 | 0.680 | 0.000 | -8.750 | 8.750 |
| w32_component_count_slope_per_100 | strict_pre_entry_component_topology | 32 | higher_is_established | 0.626 | 0.640 | 0.000 | 0.000 | 0.000 |
| w32_mean_component_count | strict_pre_entry_component_topology | 32 | higher_is_established | 0.542 | 0.640 | 2.000 | 2.000 | 0.000 |
| w64_boundary_to_volume_slope_per_100 | strict_pre_entry_component_topology | 64 | higher_is_established | 0.449 | 0.630 | 0.000 | -7.500 | 7.500 |
| w32_mean_near_support_fraction | strict_pre_entry_component_topology | 32 | lower_is_established | 0.636 | 0.600 | 1.000 | 1.000 | 0.000 |
| w32_mean_support_touch_fraction | strict_pre_entry_component_topology | 32 | lower_is_established | 0.636 | 0.600 | 1.000 | 1.000 | 0.000 |
| w96_mean_spanning_fraction | strict_pre_entry_component_topology | 96 | higher_is_established | 0.565 | 0.600 | 0.000 | 0.000 | 0.000 |

## Operativ lesning

- `data_scope`: `no_new_dynamics_v15da_components_v15dd_labels` fordi Analysen leser v15da component trajectories og v15dd run-summary; ingen ny dynamikk.
- `leakage_guard`: `strict_windows_le_96_no_route_fields` fordi Kandidatfeatures bruker bare statisk supportgeometri og komponent/topologi ved steps <=96; route-entry/retention brukes ikke som feature.
- `primary_result`: `pre_entry_support_topology_promising` fordi Beste strict dynamiske ikke-route metric `w32_mean_boundary_per_mass` har AUC=0.960 mot p0 false positives og AUC=0.864 established-vs-no.
- `static_confound_check`: `static_support_geometry_separates_but_is_placement_level` fordi Beste statiske metric `static_mean_support_degree` har AUC=1.000 mot p0 false positives, men dette er statisk support/placement-informasjon og maa ikke alene tolkes som dynamisk selector.
- `dynamic_check`: `best_strict_component_topology` fordi Beste strict dynamiske metric `w32_mean_boundary_per_mass` har AUC=0.960 mot p0 false positives.
- `group_reading`: `p1_vs_p0_false_positive_support_topology` fordi p1 median w96 gate_tension=0.205, trapped_core=0.968; p0 false-positive median gate_tension=0.156, trapped_core=0.694.
- `baseline_check`: `genealogy_intensity_not_primary_selector` fordi Baseline genealogy-intensity har AUC=0.280 mot p0 false positives.
- `next_step`: `pre_register_boundary_mass_holdout_with_static_audit` fordi Frys beste strict dynamiske observabel og test paa friske seeds; statisk supportgeometri maa rapporteres som placement-confound/audit.

## Tolkning

- Dette er en observabelsyntese paa eksisterende data, ikke en ny dynamisk validering.
- Route-entry/retention-felt er eksplisitt utelatt fra kandidatfeatures.
- Et positivt funn her er bare en kandidat for pre-registrert holdout, ikke en invariant eller en universell geometri.
- Et negativt funn betyr at strict pre-entry support/topologi ikke forklarer p1-vs-p0 false-positive-skillet i dagens data.
