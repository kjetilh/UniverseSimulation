# Operativ anbefaling v0.15db

- `data_scope`: `no_new_dynamics_v15da_only` fordi Analysen leser bare v15da runs og component trajectories.
- `primary_result`: `downstream_routing_separates_but_not_pre_entry` fordi Downstream routing `tail_route_index` skiller rent nok (AUC=1.000), men beste early/pre-entry `component_early_far8_mass_fraction` er svakere (AUC=0.720).
- `false_positive_reading`: `p0_intensity_without_route` fordi p0 false positives har median intensity 0.816 mot p1 established 0.768, men tail_route 0.317 mot 0.898.
- `next_step`: `instrument_pre_horizon_routing` fordi Neste steg bor instrumentere en tidligere route-entry/retention precursor, ikke bruke downstream route som selector.

- Ikke refit v15cz-score eller v15da-resultater til en selector-claim.
- Bruk funnet til aa designe en pre-horizon routing/phase observabel hvis mulig.
