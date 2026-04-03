# Relasjonell universgraf v0.15l: holdout failure explainer

## Formål

Denne runden forklarer hvorfor v15j sine lokale tail-mekanismer ikke generaliserte på v15k-holdoutene.

## Per-trace sammenlikning

| trace | anchor mech | holdout mech | primary driver | d events | d quiet | d birth/death |
| --- | --- | --- | --- | --- | --- | --- |
| pair23_compress_split_rebind_holdout | fragmenting_repair_cycle | mixed_mechanism | quiet_suffix_collapse | 15.000 | -68.000 | 0.000 |
| pair23_merge_hold_split_holdout | balanced_rebound_cycle | mixed_mechanism | birth_death_intrusion | -10.000 | 16.000 | 1.000 |
| pair23_split_persistent_dual_holdout | quiet_relaxation_lock | mixed_mechanism | birth_death_intrusion | 6.000 | -152.000 | 1.000 |
| pair34_split_persistent_dual_holdout | fragmenting_repair_cycle | mixed_mechanism | quiet_suffix_collapse | -9.000 | -146.000 | 0.000 |

## Aggregate bruddmodi

| break driver | n | rate | mean d events | mean d quiet |
| --- | --- | --- | --- | --- |
| birth_death_intrusion | 2 | 0.500 | -2.000 | -68.000 |
| quiet_suffix_collapse | 2 | 0.500 | 3.000 | -107.000 |

## Operativ lesning

- `failure_explanation`: `holdout_failure_explained_locally` fordi Holdout-bruddet kan leses som noen fa lokale bruddmodi (birth_death_intrusion, quiet_suffix_collapse), ikke bare ren uforklarlig stoy.
- `next_step`: `pivot_question` fordi Neste steg bør være et nytt defect-spørsmål, ikke mer av samme collision-generalisering.

## Tolkning

- Dette er fortsatt en lokal forklaringsanalyse, ikke en ny mekanismelov.
- Verdien her er å vise at holdout-bruddet ikke var helt vilkårlig, men heller ikke sterkt nok til å redde collision-generaliseringen.
