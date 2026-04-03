# Relasjonell universgraf v0.15e: pair family refinement

## Formål

Denne runden bruker bare de to mest informative 48-pairene fra v0.15d og bruker mer budsjett per pair for å se om de faktisk heller mot ulike interaksjonsvinduer.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Pair aggregates

| pair | n | min union j | final union j | window comp delta | final comp delta | binding | compress_then_split | mixed | dominant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2-3 | 6 | 0.202 | 0.557 | 0.833 | 2.000 | 0.000 | 0.333 | 0.500 | mixed_window |
| 3-4 | 12 | 0.203 | 0.476 | 1.917 | 0.250 | 0.083 | 0.000 | 0.667 | mixed_window |

## Run-level diagnostics

| pair | growth | offset | min union j | min step | window comp delta | final comp delta | class |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2-3 | 101 | 0 | 0.219 | 122 | 2.000 | -1.000 | split_then_bind |
| 2-3 | 101 | 5 | 0.267 | 46 | 1.000 | 1.000 | mixed_window |
| 2-3 | 101 | 11 | 0.179 | 140 | 2.000 | 3.000 | mixed_window |
| 2-3 | 101 | 17 | 0.188 | 198 | -2.000 | 4.000 | compress_then_split |
| 2-3 | 101 | 23 | 0.188 | 204 | 4.000 | 1.000 | mixed_window |
| 2-3 | 101 | 29 | 0.174 | 178 | -2.000 | 4.000 | compress_then_split |
| 3-4 | 101 | 0 | 0.231 | 122 | 4.000 | -3.000 | split_then_bind |
| 3-4 | 101 | 5 | 0.161 | 162 | -1.000 | 1.000 | mixed_window |
| 3-4 | 101 | 11 | 0.250 | 180 | 0.000 | -2.000 | mixed_window |
| 3-4 | 101 | 17 | 0.261 | 78 | 7.000 | 0.000 | mixed_window |
| 3-4 | 101 | 23 | 0.250 | 84 | 6.000 | 5.000 | persistent_fragmentation_tendency |
| 3-4 | 101 | 29 | 0.200 | 64 | 9.000 | -2.000 | split_then_bind |
| 3-4 | 202 | 0 | 0.161 | 256 | -5.000 | -4.000 | persistent_binding_tendency |
| 3-4 | 202 | 5 | 0.152 | 220 | 7.000 | 0.000 | mixed_window |
| 3-4 | 202 | 11 | 0.138 | 126 | -4.000 | 0.000 | mixed_window |
| 3-4 | 202 | 17 | 0.229 | 374 | 1.000 | 4.000 | mixed_window |
| 3-4 | 202 | 23 | 0.154 | 154 | -1.000 | 3.000 | mixed_window |
| 3-4 | 202 | 29 | 0.250 | 102 | 0.000 | 1.000 | mixed_window |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er separert og matched AB/BA-control holder seg samkjørt i den smale 48-runden.
- `pair_family_signal`: `pair_families_still_mixed` fordi `2-3` og `3-4` er fortsatt blandet (2-3 compress_then_split 0.333, 3-4 binding 0.083).
- `next_step`: `increase_per_pair_budget` fordi Neste steg bør være mer budsjett per pair eller enda færre, men mer kontrollerte run-seeds.
