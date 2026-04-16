# Relasjonell universgraf v0.15bi: local_swap load-stabilizer flip

## Formål

Denne runden tester om `p2` og `p1` skilles best av en last-vs-stabilisering-flip: `p2` som tyngst lokal last, `p1` som sterkest stabilisering.

## Placement snapshot

| placement | coarse return | core share | rare share | mean degree | ball1 | ball2 | shell2/shell1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.846 | 0.342 | 0.274 | 6.667 | 18.000 | 37.000 | 1.267 |
| 2 | 0.446 | 0.130 | 0.429 | 7.667 | 21.000 | 42.000 | 1.167 |
| 3 | 0.631 | 0.222 | 0.333 | 5.333 | 14.000 | 26.000 | 1.091 |

## Load and stabilizer axes

| axis | family | p1 | p2 | p3 | supported | margin |
| --- | --- | --- | --- | --- | --- | --- |
| ball2_load | load | 37.000 | 42.000 | 26.000 | 1 | 5.000 |
| ball3_load | load | 49.000 | 54.000 | 39.000 | 1 | 5.000 |
| ball1_load | load | 18.000 | 21.000 | 14.000 | 1 | 3.000 |
| degree_ball1_load | load | 8.467 | 9.767 | 6.733 | 1 | 1.300 |
| degree_ball2_load | load | 8.517 | 9.767 | 6.633 | 1 | 1.250 |
| full_stabilizer | stabilizer | 2.455 | 1.743 | 1.944 | 1 | 0.511 |
| retention_shell_stabilizer | stabilizer | 2.113 | 1.613 | 1.722 | 1 | 0.391 |
| retention_core_stabilizer | stabilizer | 1.189 | 0.576 | 0.853 | 1 | 0.336 |

## Operativ lesning

- `load_stabilizer_status`: `load_without_stabilization_supported` fordi p2 topper alle små last-akser, mens p1 topper alle små stabiliseringsakser. Det støtter at rare-load-flippen ligger i høy last uten tilsvarende stabilisering.
- `best_load_axis`: `ball2_load` fordi Beste lastakse gir margin 5.000.
- `best_stabilizer_axis`: `full_stabilizer` fordi Beste stabiliseringsakse gir margin 0.511.
- `next_step`: `explain_missing_stabilizer` fordi Neste steg bør forklare hva p2 mangler av stabilisering relativt til p1.

## Tolkning

- Dette er fortsatt en ren forklaringsrunde på eksisterende data, ikke en ny simulering.
- Les dette som en lokal p2-vs-p1-grenseforklaring, ikke som en global law for `local_swap`.
