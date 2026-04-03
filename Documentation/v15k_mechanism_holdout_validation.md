# Relasjonell universgraf v0.15k: mechanism holdout validation

## Formål

Denne runden tester om mekanismelesningen fra v15j holder på nye, nærliggende holdout-traces fra de samme v15g-familiene.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Holdout mechanism check

| trace | pair | offset | prefix | expected mechanism | observed mechanism | match |
| --- | --- | --- | --- | --- | --- | --- |
| pair23_compress_split_rebind_holdout | 2-3 | 23 | compress_split_rebind | fragmenting_repair_cycle | mixed_mechanism | 0 |
| pair23_merge_hold_split_holdout | 2-3 | 17 | merge_hold_split | balanced_rebound_cycle | mixed_mechanism | 0 |
| pair23_split_persistent_dual_holdout | 2-3 | 29 | split_persistent_dual | quiet_relaxation_lock | mixed_mechanism | 0 |
| pair34_split_persistent_dual_holdout | 3-4 | 11 | split_persistent_dual | fragmenting_repair_cycle | mixed_mechanism | 0 |

## Operativ lesning

- `artifact_control`: `clean` fordi Holdout-tracene reproduserer forventet prefix-chain og holder seg order-stabile i tail og mekanikk.
- `generalization_signal`: `mechanism_generalization_weak` fordi Holdout-tracene bekrefter ikke mekanismelesningen godt nok (match-rate 0.000).
- `next_step`: `pause_threshold_claims` fordi Neste steg bør være en mindre påstand: forklarende spor, men ikke stabil generalisering.

## Tolkning

- Dette er fortsatt en smal generaliseringstest, ikke ny fysikk.
- Et positivt utfall betyr bare at de samme mekanismene ser ut til å komme igjen på nærliggende holdout-traces.
- Et negativt utfall ville ha betydd at v15j var for lokalt overfit. Det er derfor nyttig uansett vei.
