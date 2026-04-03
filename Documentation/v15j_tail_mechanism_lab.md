# Relasjonell universgraf v0.15j: tail mechanism lab

## Formål

Denne runden forklarer v15i sine tail-overganger med eksplisitte segmentmekanismer i stedet for bare overgangsnavn.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Trace mechanisms

| trace | v15i tail | mechanism | segments | events | quiet suffix |
| --- | --- | --- | --- | --- | --- |
| pair23_compress_split_rebind | fragmenting_lock | fragmenting_repair_cycle | 2.000 | 10.000 | 92.000 |
| pair23_merge_hold_split | merge_rebound_lock | balanced_rebound_cycle | 2.000 | 18.000 | 56.000 |
| pair23_split_persistent_dual | quiet_singleton_lock | quiet_relaxation_lock | 0.000 | 0.000 | 314.000 |
| pair34_split_persistent_dual | fragmenting_lock | fragmenting_repair_cycle | 1.000 | 15.000 | 148.000 |

## Aggregate mechanisms

| mechanism | n traces | rate | mean segments | mean events |
| --- | --- | --- | --- | --- |
| balanced_rebound_cycle | 1 | 0.250 | 2.000 | 18.000 |
| fragmenting_repair_cycle | 2 | 0.500 | 1.500 | 12.500 |
| quiet_relaxation_lock | 1 | 0.250 | 0.000 | 0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Mekanismelabelene er order-stabile i denne runden.
- `mechanism_signal`: `tail_mechanisms_explained` fordi De tre v15i-tail-overgangene kan na forklares av tre enkle segmentmekanismer (balanced_rebound_cycle, fragmenting_repair_cycle, quiet_relaxation_lock).
- `next_step`: `test_mechanism_thresholds` fordi Neste steg bør teste hvilke terskler som utløser disse mekanismene, ikke nye pair-offset-sok.

## Tolkning

- Dette er fortsatt forklarende arbeidskategorier, ikke partikkelbevis.
- Poenget er at senfasen na beskrives med enklere mekanismer enn i v15i alene.
- Hvis disse mekanismene holder, er neste riktige steg terskeltesting, ikke ny bred collision-scan.
