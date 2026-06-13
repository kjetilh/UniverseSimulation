# Relasjonell universgraf v0.15db: routing/phase observable synthesis

## Formal

Denne runden bruker ingen ny dynamikk. Den analyserer v15da for aa finne hvorfor p0 kan ha hoy genealogy-intensity uten far-shell-horizon.
Observabler deles i early/pre-entry, downstream routing og false-positive pressure.

## Group summary

| group | n | placements | labels | intensity | phase | tail route | entry timing | pressure |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| non_decisive | 2 | p0:1;p1:1 | failed_far_shell_horizon:1;mixed_far_shell_horizon:1 | 0.453 | 0.110 | 0.428 | 0.277 | 0.026 |
| other_established | 1 | p0:1 | established_far_shell_horizon:1 | 0.568 | 0.063 | 0.756 | 0.213 | -0.188 |
| other_no_horizon | 1 | p1:1 | no_far_shell_horizon:1 | 0.467 | 0.074 | 0.306 | 0.000 | 0.160 |
| p0_high_score_no_horizon | 5 | p0:5 | no_far_shell_horizon:5 | 0.816 | 0.148 | 0.317 | 0.000 | 0.545 |
| p0_no_horizon_other | 5 | p0:5 | no_far_shell_horizon:5 | 0.492 | 0.015 | 0.233 | 0.000 | 0.262 |
| p1_established | 10 | p1:10 | established_far_shell_horizon:10 | 0.768 | 0.386 | 0.898 | 0.849 | -0.131 |
| p2_no_horizon | 12 | p2:12 | no_far_shell_horizon:12 | 0.275 | 0.004 | 0.140 | 0.000 | 0.085 |

## Metric ranking

| metric | family | direction | AUC est/no | AUC p1/p0 false | median p1-p0 false |
| --- | --- | --- | --- | --- | --- |
| tail_route_index | downstream_routing | higher_is_established | 1.000 | 1.000 | 0.581 |
| entry_timing_index | downstream_routing | higher_is_established | 1.000 | 1.000 | 0.849 |
| horizon_efficiency_per_churn | downstream_outcome | higher_is_established | 1.000 | 1.000 | 0.164 |
| intensity_without_route_pressure | false_positive_pressure | lower_is_established | 0.996 | 1.000 | -0.676 |
| route_efficiency_per_intensity | downstream_routing | higher_is_established | 0.692 | 1.000 | 0.403 |
| phase_intensity_gap | false_positive_pressure | lower_is_established | 0.557 | 0.960 | -0.346 |
| component_tail_route_index | downstream_routing | higher_is_established | 0.921 | 0.860 | 0.247 |
| component_early_far8_mass_fraction | early_pre_entry | higher_is_established | 0.783 | 0.720 | 0.349 |
| phase_entry_index | early_pre_entry | higher_is_established | 0.763 | 0.700 | 0.237 |
| component_early_far10_mass_fraction | early_pre_entry | higher_is_established | 0.723 | 0.670 | 0.356 |
| component_early_weighted_mean_distance | early_pre_entry | higher_is_established | 0.751 | 0.640 | 2.538 |
| component_tail_far8_mass_fraction | downstream_routing | higher_is_established | 0.826 | 0.620 | 0.236 |
| genealogy_intensity_index | baseline_failed_selector | higher_is_established | 0.711 | 0.280 | -0.048 |

## High-score no-horizon cases

| placement | seed | score | phase | tail route | entry timing | pressure | first high | tail share | horizon |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p0 | 9479 | 0.999 | 0.227 | 0.317 | 0.000 | 0.682 | nan | 0.634 | 0.000 |
| p2 | 9631 | 0.871 | 0.274 | 0.436 | 0.000 | 0.435 | nan | 0.871 | 0.000 |
| p0 | 9833 | 0.853 | 0.148 | 0.280 | 0.000 | 0.573 | nan | 0.559 | 0.000 |
| p2 | 9887 | 0.817 | 0.229 | 0.418 | 0.000 | 0.399 | nan | 0.836 | 0.000 |
| p0 | 9533 | 0.816 | 0.009 | 0.270 | 0.000 | 0.545 | nan | 0.541 | 0.000 |
| p0 | 9391 | 0.790 | 0.124 | 0.328 | 0.000 | 0.462 | nan | 0.655 | 0.000 |
| p2 | 9833 | 0.781 | 0.100 | 0.382 | 0.000 | 0.398 | nan | 0.764 | 0.000 |
| p0 | 9631 | 0.777 | 0.298 | 0.325 | 0.000 | 0.453 | nan | 0.649 | 0.000 |

## Operativ lesning

- `data_scope`: `no_new_dynamics_v15da_only` fordi Analysen leser bare v15da runs og component trajectories.
- `primary_result`: `downstream_routing_separates_but_not_pre_entry` fordi Downstream routing `tail_route_index` skiller rent nok (AUC=1.000), men beste early/pre-entry `component_early_far8_mass_fraction` er svakere (AUC=0.720).
- `false_positive_reading`: `p0_intensity_without_route` fordi p0 false positives har median intensity 0.816 mot p1 established 0.768, men tail_route 0.317 mot 0.898.
- `next_step`: `instrument_pre_horizon_routing` fordi Neste steg bor instrumentere en tidligere route-entry/retention precursor, ikke bruke downstream route som selector.

## Tolkning

- Dette er en observabelsyntese, ikke en ny dynamisk validering.
- Downstream route/retention kan forklare p0 false positives, men er ikke automatisk en gyldig pre-horizon selector.
- Ikke oppgrader til partikler, Lorentz-likhet, invariant, entanglement eller universell geometri.
