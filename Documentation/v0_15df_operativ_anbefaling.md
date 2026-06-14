# Operativ anbefaling v0.15df

- `data_scope`: `no_new_dynamics_v15da_components_v15dd_labels` fordi Analysen leser v15da component trajectories og v15dd run-summary; ingen ny dynamikk.
- `leakage_guard`: `strict_windows_le_96_no_route_fields` fordi Kandidatfeatures bruker bare statisk supportgeometri og komponent/topologi ved steps <=96; route-entry/retention brukes ikke som feature.
- `primary_result`: `pre_entry_support_topology_promising` fordi Beste strict dynamiske ikke-route metric `w32_mean_boundary_per_mass` har AUC=0.960 mot p0 false positives og AUC=0.864 established-vs-no.
- `static_confound_check`: `static_support_geometry_separates_but_is_placement_level` fordi Beste statiske metric `static_mean_support_degree` har AUC=1.000 mot p0 false positives, men dette er statisk support/placement-informasjon og maa ikke alene tolkes som dynamisk selector.
- `dynamic_check`: `best_strict_component_topology` fordi Beste strict dynamiske metric `w32_mean_boundary_per_mass` har AUC=0.960 mot p0 false positives.
- `group_reading`: `p1_vs_p0_false_positive_support_topology` fordi p1 median w96 gate_tension=0.205, trapped_core=0.968; p0 false-positive median gate_tension=0.156, trapped_core=0.694.
- `baseline_check`: `genealogy_intensity_not_primary_selector` fordi Baseline genealogy-intensity har AUC=0.280 mot p0 false positives.
- `next_step`: `pre_register_boundary_mass_holdout_with_static_audit` fordi Frys beste strict dynamiske observabel og test paa friske seeds; statisk supportgeometri maa rapporteres som placement-confound/audit.

- Ikke bruk route-entry/retention som pre-entry selector.
- Ikke refit genealogy-intensity til denne kontrasten.
- Hvis beste ikke-route feature er sterk nok, frys den foer eventuell frisk holdout.
