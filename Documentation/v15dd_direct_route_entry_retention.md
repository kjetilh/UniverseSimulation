# Relasjonell universgraf v0.15dd: direct route-entry / retention lab

## Formal

Denne runden rerunner v15da-scope og logger route-state direkte per snapshot.
Maalet er aa skille faktisk high-route entry/retention fra outer pressure uten high-entry.
Dette er instrumentering, ikke en ny pre-horizon selector og ikke en fysikk-claim.

## Design

| field | value |
| --- | --- |
| target | 1024 |
| growth seed | 202 |
| perturbation | add_chord |
| placements | p0;p1;p2 |
| seed deltas | 9341;9391;9433;9479;9533;9587;9631;9677;9733;9781;9833;9887 |

## Group summary

| group | n | placements | horizon labels | route labels | intensity | first sustained | retention | last12 | outer pressure | dropout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| non_decisive | 2 | p0:1;p1:1 | failed_far_shell_horizon:1;mixed_far_shell_horizon:1 | entry_then_dropout:2 | 0.453 | 2520.0 | 0.429 | 0.167 | 0.765 | 1.0 |
| other_established | 1 | p0:1 | established_far_shell_horizon:1 | sustained_high_retention:1 | 0.568 | 2688.0 | 0.878 | 0.833 | 0.554 | 3.0 |
| other_no_horizon | 1 | p1:1 | no_far_shell_horizon:1 | outer_pressure_no_high_entry:1 | 0.467 | nan | 0.000 | 0.000 | 0.855 | 0.0 |
| p0_high_score_no_horizon | 5 | p0:5 | no_far_shell_horizon:5 | outer_pressure_no_high_entry:5 | 0.816 | nan | 0.000 | 0.000 | 0.937 | 0.0 |
| p0_no_horizon_other | 5 | p0:5 | no_far_shell_horizon:5 | outer_pressure_no_high_entry:5 | 0.492 | nan | 0.000 | 0.000 | 0.736 | 0.0 |
| p1_established | 10 | p1:10 | established_far_shell_horizon:10 | sustained_high_retention:10 | 0.768 | 516.0 | 0.978 | 1.000 | 0.088 | 1.0 |
| p2_no_horizon | 12 | p2:12 | no_far_shell_horizon:12 | no_route_entry:4;outer_pressure_no_high_entry:8 | 0.275 | nan | 0.000 | 0.000 | 0.522 | 0.0 |

## Route label cross-tab

| horizon label | direct route label | n | placements | intensity | outer pressure | retention |
| --- | --- | --- | --- | --- | --- | --- |
| established_far_shell_horizon | sustained_high_retention | 11 | p0;p1 | 0.751 | 0.126 | 0.968 |
| failed_far_shell_horizon | entry_then_dropout | 1 | p0 | 0.446 | 0.822 | 0.358 |
| mixed_far_shell_horizon | entry_then_dropout | 1 | p1 | 0.461 | 0.708 | 0.500 |
| no_far_shell_horizon | no_route_entry | 4 | p2 | 0.027 | 0.000 | 0.000 |
| no_far_shell_horizon | outer_pressure_no_high_entry | 19 | p0;p1;p2 | 0.566 | 0.850 | 0.000 |

## Metric ranking

| metric | family | direction | AUC est/no | AUC p1/p0 false | median p1 | median p0 false | p1-p0 false |
| --- | --- | --- | --- | --- | --- | --- | --- |
| first_sustained_high3_earliness | direct_entry | higher_is_established | 1.000 | 1.000 | 0.849 | 0.000 | 0.849 |
| direct_retention_rate_after_entry | direct_retention | higher_is_established | 1.000 | 1.000 | 0.978 | 0.000 | 0.978 |
| last12_high_rate_direct | direct_retention | higher_is_established | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 |
| sustained_high3_rate | direct_retention | higher_is_established | 1.000 | 1.000 | 0.833 | 0.000 | 0.833 |
| direct_high_rate | direct_entry | higher_is_established | 1.000 | 1.000 | 0.833 | 0.000 | 0.833 |
| longest_high_run_direct | direct_entry | higher_is_established | 1.000 | 1.000 | 330.000 | 0.000 | 330.000 |
| outer_pressure_without_high_rate | failed_route_pressure | lower_is_established | 0.838 | 1.000 | 0.088 | 0.937 | -0.849 |
| genealogy_intensity_index | baseline_failed_selector | higher_is_established | 0.711 | 0.280 | 0.768 | 0.816 | -0.048 |
| direct_dropout_count_after_entry | failed_retention | lower_is_established | 0.136 | 0.150 | 1.000 | 0.000 | 1.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og alle requested add_chord-perturbations matcher faktisk perturbasjon.
- `instrumentation_scope`: `direct_snapshot_route_logging` fordi v15dd rerunner v15da-scope og logger route_phase, sustained high3, retention, dropout og outer-pressure-without-high per snapshot.
- `primary_result`: `direct_route_entry_retention_separates_false_positives` fordi `first_sustained_high3_earliness` skiller p1 established fra p0 false positives med AUC=1.000. Dette er mekanistisk instrumentering, ikke en pre-entry selector.
- `group_reading`: `p1_vs_p0_false_positive_direct_route` fordi p1 established route labels `sustained_high_retention:10`; p0 high-score/no-horizon route labels `outer_pressure_no_high_entry:5`. Median retention p1=0.978, p0=0.000; outer-pressure-without-high p1=0.088, p0=0.937.
- `baseline_check`: `genealogy_intensity_still_not_selector` fordi Baseline genealogy-intensity AUC mot p0 false positives er 0.280.
- `next_step`: `derive_pre_entry_features_from_direct_route_log` fordi Bruk snapshot-loggen til aa lage eksplisitte pre-entry kandidater; ikke bruk direct route outcome som predictor.

## Tolkning

- Direct route logging kan forklare false positives, men maa ikke behandles som en pre-entry predictor.
- Hvis separasjonen er sterk, er neste steg aa avlede en tidligere feature fra snapshot-loggen og teste den separat.
- Ikke oppgrader til partikler, Lorentz-likhet, entanglement, invariant eller universell geometri.
