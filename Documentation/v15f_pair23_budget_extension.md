# Relasjonell universgraf v0.15f: pair 2-3 budget extension

## Formål

Denne runden bruker ekstra budsjett på bare pair 2-3 i 48-korridoren for å se om `compress_then_split` blir en stabil familielesning.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Pair availability

| growth | pair available | min support distance |
| --- | --- | --- |
| 101 | 1 | 4 |

## Aggregate

| pair | n | min union j | final union j | window comp delta | final comp delta | compress_then_split | split_then_bind | binding | mixed | dominant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2-3 | 16 | 0.195 | 0.497 | 1.125 | 0.938 | 0.125 | 0.062 | 0.000 | 0.750 | mixed_window |

## Run-level diagnostics

| offset | min union j | min step | window comp delta | final comp delta | class |
| --- | --- | --- | --- | --- | --- |
| 0 | 0.219 | 121 | 2.000 | -1.000 | split_then_bind |
| 2 | 0.222 | 98 | 0.000 | -1.000 | mixed_window |
| 5 | 0.267 | 46 | 1.000 | 1.000 | mixed_window |
| 8 | 0.182 | 259 | -3.000 | -2.000 | mixed_window |
| 11 | 0.179 | 140 | 2.000 | 3.000 | mixed_window |
| 14 | 0.182 | 256 | -1.000 | -2.000 | mixed_window |
| 17 | 0.188 | 197 | 0.000 | 4.000 | mixed_window |
| 20 | 0.235 | 116 | 2.000 | 1.000 | mixed_window |
| 23 | 0.188 | 204 | 4.000 | 1.000 | mixed_window |
| 26 | 0.185 | 107 | 0.000 | 0.000 | mixed_window |
| 29 | 0.160 | 213 | 5.000 | 4.000 | mixed_window |
| 32 | 0.121 | 298 | 5.000 | 1.000 | persistent_fragmentation_tendency |
| 35 | 0.152 | 208 | -2.000 | 2.000 | compress_then_split |
| 38 | 0.182 | 121 | -2.000 | 1.000 | compress_then_split |
| 41 | 0.208 | 49 | 4.000 | 1.000 | mixed_window |
| 44 | 0.250 | 124 | 1.000 | 2.000 | mixed_window |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er separert, pair 2-3 er faktisk tilgjengelig i denne smale runden, og matched AB/BA-control holder seg samkjørt.
- `pair23_signal`: `compress_then_split_leading_but_mixed` fordi `compress_then_split` leder for pair 2-3 (0.125), men mixed-andelen er fortsatt for høy (0.750) til en ren dom.
- `next_step`: `increase_budget_or_fix_base` fordi Neste steg bør være enda mer budsjett på samme base eller en enda strammere seed-familie rundt de run-offsettene som støttet signalet.
