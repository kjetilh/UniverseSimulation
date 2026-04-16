# Relasjonell universgraf v0.15bh: local_swap rare-load trigger lab

## Formål

Denne runden tester om `p2` kan leses som en egen rare-load-retning ut fra en liten støtte-/last-akse.

## Placement snapshot

| placement | rare share | shell share | coarse return | mean degree | ball1 | ball2 | ball3 | shell2/shell1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.274 | 0.384 | 0.846 | 6.667 | 18.000 | 37.000 | 49.000 | 1.267 |
| 2 | 0.429 | 0.442 | 0.446 | 7.667 | 21.000 | 42.000 | 54.000 | 1.167 |
| 3 | 0.333 | 0.444 | 0.631 | 5.333 | 14.000 | 26.000 | 39.000 | 1.091 |

## Candidate trigger axes

| axis | p1 | p2 | p3 | p2 top | full rare order | margin |
| --- | --- | --- | --- | --- | --- | --- |
| ball2_load | 37.000 | 42.000 | 26.000 | 1 | 0 | 5.000 |
| ball3_load | 49.000 | 54.000 | 39.000 | 1 | 0 | 5.000 |
| ball1_load | 18.000 | 21.000 | 14.000 | 1 | 0 | 3.000 |
| compact_dense_load | 5.744 | 7.195 | 3.948 | 1 | 0 | 1.451 |
| dense_local_load | 7.200 | 8.600 | 5.642 | 1 | 0 | 1.400 |
| degree_minus_shell2 | 5.400 | 6.500 | 4.242 | 1 | 0 | 1.100 |
| support_degree | 6.667 | 7.667 | 5.333 | 1 | 0 | 1.000 |

## Operativ lesning

- `rare_load_trigger_status`: `p2_rare_load_trigger_supported` fordi Flere små støtte-/last-akser setter p2 tydelig øverst, men ingen av dem løser samtidig p3 > p1. Det støtter en lokal p2-trigger uten å late som hele rare-rangeringen er løst.
- `best_axis`: `ball2_load` fordi Beste kandidatakse gir p2-margin 5.000.
- `next_step`: `explain_p2_trigger_without_overclaim` fordi Neste steg bør forklare p2-triggeren lokalt, ikke åpne en bredere scan.

## Tolkning

- Dette er fortsatt en ren akse-/triggerlab på eksisterende data, ikke en ny simulering.
- Les dette som en smal test av p2-retningen, ikke som en full forklaring av hele p1/p2/p3-kartet.
