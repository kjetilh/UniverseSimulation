# UniverseSimulation v16ab: fresh seed-clock scheduler holdout

Dato: 2026-07-12

## Konklusjon

Status: `promote_local_seed_clock_to_v16a_rerun`.

Den frosne lokale seed-raten `rho_seed=0.000503953814774212` ble testet uten refit mot `current_global` og `preparation_only` paa fresh growth seeds `1801/1901`.

Dette er en scheduler-/vekstgate. Den tester ikke geometri, Lorentz-likhet eller causal cones.

## Target hygiene

| target_nodes | growth_replicates | mean_initial_nodes | mean_initial_tokens | separated_from_prev |
| --- | --- | --- | --- | --- |
| 1024.000000 | 2.000000 | 1024.000000 | 14.500000 | 1.000000 |

## Armer

| arm | n_runs | mean_initial_tokens | mean_final_tokens | mean_node_growth | max_node_growth | total_seed_events | total_integrated_seed_hazard | mean_total_time | max_seed_formula_error | max_abs_beta1_drift |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| current_global | 16.000000 | 14.500000 | 208.000000 | 2.062500 | 5.000000 | 33.000000 | 28.768776 | 44.951213 | 0.000000 | 0.000000 |
| preparation_only | 16.000000 | 14.500000 | 203.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 45.078964 | 0.000000 | 0.000000 |
| exposure_matched_local | 16.000000 | 14.500000 | 201.750000 | 1.625000 | 3.000000 | 26.000000 | 26.029969 | 46.469647 | 0.000000 | 0.000000 |

## Frozen gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| run_integrity | pass | 48.000000 | 48.000000 | continue |
| local_seed_formula | pass | 0.000000 | <=1e-12 | continue |
| aggregate_hazard_ratio | pass | 0.904799 | [0.75,1.25] | continue |
| per_growth_hazard_ratio | pass | 0.873599;0.938264 | each in [0.5,2.0] | continue |
| median_total_time_ratio | pass | 1.056431 | [0.75,1.25] | continue |
| median_final_token_ratio | pass | 1.002439 | [0.75,1.25] | continue |
| nonseed_family_tv | pass | 0.001839 | <=0.05 | continue |
| local_runaway_control | pass | 3.000000 | <=51 | continue |
| preparation_only_hygiene | pass | seeds=0;max_node_growth=0 | seeds=0;max_node_growth=0 | continue |
| invalid_event_control | pass | 0.000000 | 0.000000 | continue |
| beta1_anchor_control | pass | 0.000000 | 0.000000 | continue |
| v16ab_overall | promote_local_seed_clock_to_v16a_rerun | rho_seed=0.000503953814774212 | all frozen gates pass | rerun_v16a_locality |

## Evidensstatus

- Growth seeds og terskler ble skrevet til `v16ab_pre_registration.csv` foer fresh dynamikk.
- Armene bruker separate RNG-stroemmer og ID-allokatorer; sammenligningene er matched paa base og run-offset, ikke coupled trajectories.
- Integrert hazard er primaer fordi faktiske seed-events er sjeldne. Seed-tellingene er deskriptive.
- Et pass kvalifiserer kandidaten bare for en ny v16a-locality-rerun. Det gjoer den ikke automatisk til anchor.

## Beslutning

Den lokale kandidaten passerte alle frosne scheduler-/vekstgater. Neste steg er aa implementere clock-varianten eksplisitt i en isolert regeladapter og rerun v16a support/locality med seed aktiv. `v16b` event-DAG forblir blokkert til dette er gjort.
