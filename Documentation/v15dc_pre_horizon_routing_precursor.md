# Relasjonell universgraf v0.15dc: censored pre-horizon routing precursor

## Formal

Denne runden bruker ingen ny dynamikk. Den leser v15da-komponentbaner og sensurerer pre-horizon observabler foer `first_high_step` der high-entry finnes.
Maalet er aa teste om routing-forskjellen som v15db fant downstream allerede finnes i strengere pre-high komponentdata.

## Group summary

| group | n | placements | labels | intensity | coherence | mean far8 | peak far8 | active | distance | snapshots |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| non_decisive | 2 | p0:1;p1:1 | failed_far_shell_horizon:1;mixed_far_shell_horizon:1 | 0.453 | 0.133 | 0.065 | 0.143 | 0.228 | 0.974 | 81.0 |
| other_established | 1 | p0:1 | established_far_shell_horizon:1 | 0.568 | 0.014 | 0.000 | 0.000 | 0.000 | 1.144 | 81.0 |
| other_no_horizon | 1 | p1:1 | no_far_shell_horizon:1 | 0.467 | 0.113 | 0.039 | 0.250 | 0.111 | 0.589 | 81.0 |
| p0_high_score_no_horizon | 5 | p0:5 | no_far_shell_horizon:5 | 0.816 | 0.125 | 0.066 | 0.222 | 0.062 | 2.300 | 81.0 |
| p0_no_horizon_other | 5 | p0:5 | no_far_shell_horizon:5 | 0.492 | 0.005 | 0.000 | 0.000 | 0.000 | 0.425 | 81.0 |
| p1_established | 10 | p1:10 | established_far_shell_horizon:10 | 0.768 | 0.339 | 0.166 | 0.541 | 0.377 | 2.102 | 62.0 |
| p2_no_horizon | 12 | p2:12 | no_far_shell_horizon:12 | 0.275 | 0.002 | 0.000 | 0.000 | 0.000 | 0.194 | 81.0 |

## Metric ranking

| metric | AUC est/no | AUC p1/p0 false | median p1 | median p0 false | p1-p0 false |
| --- | --- | --- | --- | --- | --- |
| pre_far8_slope_per_100 | 0.794 | 0.780 | 0.100 | 0.017 | 0.083 |
| pre_distance_slope_per_100 | 0.767 | 0.760 | 1.310 | 0.388 | 0.922 |
| pre_last_mean_distance | 0.783 | 0.740 | 5.617 | 3.486 | 2.131 |
| pre_late_route_gain | 0.775 | 0.720 | 0.234 | 0.007 | 0.227 |
| pre_peak_far10_fraction | 0.727 | 0.700 | 0.453 | 0.136 | 0.317 |
| pre_peak_far8_fraction | 0.769 | 0.660 | 0.541 | 0.222 | 0.318 |
| pre_mean_far10_fraction | 0.723 | 0.650 | 0.100 | 0.027 | 0.073 |
| pre_mean_far8_fraction | 0.759 | 0.620 | 0.166 | 0.066 | 0.100 |
| pre_route_coherence_index | 0.755 | 0.620 | 0.339 | 0.125 | 0.215 |
| pre_route_active_rate | 0.727 | 0.620 | 0.377 | 0.062 | 0.315 |
| pre_longest_route_active_run | 0.686 | 0.580 | 10.000 | 4.000 | 6.000 |
| pre_mean_distance | 0.680 | 0.400 | 2.102 | 2.300 | -0.198 |
| pre_mass_distance_flux | 0.640 | 0.300 | 17.460 | 54.975 | -37.516 |
| genealogy_intensity_index | 0.711 | 0.280 | 0.768 | 0.816 | -0.048 |

## High-score no-horizon cases

| placement | seed | intensity | coherence | mean far8 | peak far8 | active | distance | cutoff | first high | horizon |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p0 | 9479 | 0.999 | 0.635 | 0.314 | 0.766 | 0.938 | 4.142 | 640.0 | nan | 0.000 |
| p2 | 9631 | 0.871 | 0.316 | 0.054 | 0.333 | 0.593 | 2.915 | 640.0 | nan | 0.000 |
| p0 | 9833 | 0.853 | 0.125 | 0.066 | 0.222 | 0.062 | 2.300 | 640.0 | nan | 0.000 |
| p2 | 9887 | 0.817 | 0.178 | 0.073 | 0.170 | 0.247 | 2.822 | 640.0 | nan | 0.000 |
| p0 | 9533 | 0.816 | 0.006 | 0.000 | 0.000 | 0.000 | 0.482 | 640.0 | nan | 0.000 |
| p0 | 9391 | 0.790 | 0.055 | 0.003 | 0.136 | 0.000 | 1.610 | 640.0 | nan | 0.000 |
| p2 | 9833 | 0.781 | 0.078 | 0.012 | 0.222 | 0.025 | 0.841 | 640.0 | nan | 0.000 |
| p0 | 9631 | 0.777 | 0.311 | 0.139 | 0.438 | 0.407 | 2.580 | 640.0 | nan | 0.000 |

## Operativ lesning

- `data_scope`: `no_new_dynamics_v15da_only` fordi Analysen leser bare v15da runs og component trajectories.
- `censoring_rule`: `pre_first_high_or_early_limit` fordi Established-runs sensureres foer first_high_step; no-high-runs bruker early_step_limit.
- `primary_result`: `pre_horizon_route_precursor_weak` fordi Beste censored pre-horizon observabel `pre_far8_slope_per_100` er bare delvis separerende (p1-vs-p0-false AUC=0.780, established-vs-no AUC=0.794).
- `group_reading`: `p1_vs_p0_false_positive_pre_horizon` fordi p1 established median coherence=0.339 og pre_far8=0.166; p0 false positives median coherence=0.125 og pre_far8=0.066.
- `baseline_check`: `genealogy_intensity_still_not_selector` fordi Baseline genealogy-intensity har p1-vs-p0-false AUC=0.280; pre_route_coherence har AUC=0.620.
- `next_step`: `instrument_snapshot_route_entry_directly` fordi Treng mer direkte per-snapshot route-entry/retention logging; eksisterende sensurerte komponentfelt er ikke nok.

## Tolkning

- Dette er fortsatt en observabelsyntese paa eksisterende v15da-data, ikke en ny dynamisk validering.
- Sensureringen gjor testen strengere enn v15db: downstream tail/retention er bare evaluering, ikke feature.
- Et svakt eller negativt resultat betyr at eksisterende komponentproxyer ikke er nok som pre-horizon selector.
- Ikke oppgrader til partikler, Lorentz-likhet, invariant, entanglement eller universell geometri.
