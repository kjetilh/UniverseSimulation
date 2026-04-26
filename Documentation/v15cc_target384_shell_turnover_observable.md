# Relasjonell universgraf v0.15cc: target-384 shell-turnover observable

## Formal

Denne runden bruker en ny observabel: tidsopplost shell-turnover rundt support ved target `384`.
Sporsmalet er om dette skiller quartetet fra p2-paret tydeligere enn de tidligere statiske family-labelene.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 384 | 384.0 | 384.0 | 384.0 | 1 |

## Aggregert turnover

| profile | family | inner share | outer share | shell4+ | inner refresh | outer refresh | gradient | burst | distance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | mixed_turnover | 0.288 | 0.497 | 0.300 | 0.024 | 0.051 | 0.027 | 0.000 | 2.479 |
| add_chord_p1 | mixed_turnover | 0.319 | 0.456 | 0.280 | 0.016 | 0.068 | 0.051 | 0.000 | 2.385 |
| add_chord_p2 | mixed_turnover | 0.313 | 0.427 | 0.248 | 0.026 | 0.063 | 0.037 | 0.000 | 2.322 |
| add_chord_p3 | outer_weighted_diffuse | 0.373 | 0.526 | 0.439 | 0.030 | 0.056 | 0.026 | 0.013 | 2.409 |
| local_swap_p0 | outer_diffuse_persistent | 0.232 | 0.602 | 0.452 | 0.020 | 0.058 | 0.037 | 0.000 | 2.799 |
| local_swap_p1 | mixed_turnover | 0.275 | 0.511 | 0.313 | 0.019 | 0.056 | 0.037 | 0.000 | 2.520 |
| local_swap_p2 | outer_weighted_diffuse | 0.236 | 0.532 | 0.377 | 0.018 | 0.057 | 0.039 | 0.000 | 2.644 |
| local_swap_p3 | outer_diffuse_persistent | 0.201 | 0.690 | 0.550 | 0.012 | 0.075 | 0.063 | 0.003 | 2.909 |

## Quartet / P2 summary

| quartet majority | quartet count | p2 same | p2 label | quartet mean dist | quartet->p2 mean dist | p2 pair dist |
| --- | --- | --- | --- | --- | --- | --- |
| mixed_turnover | 2 | 0 | split | 0.459 | 0.339 | 0.328 |

## Naermeste turnover-par

| rank | profile A | profile B | same family | turnover dist |
| --- | --- | --- | --- | --- |
| 1 | add_chord_p0 | local_swap_p1 | 1 | 0.114 |
| 2 | local_swap_p0 | local_swap_p2 | 0 | 0.119 |
| 3 | local_swap_p1 | local_swap_p2 | 0 | 0.125 |
| 4 | add_chord_p1 | add_chord_p2 | 1 | 0.189 |
| 5 | add_chord_p1 | local_swap_p1 | 1 | 0.197 |
| 6 | add_chord_p0 | add_chord_p2 | 1 | 0.199 |
| 7 | local_swap_p0 | local_swap_p1 | 0 | 0.213 |
| 8 | add_chord_p2 | local_swap_p1 | 1 | 0.215 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `turnover_structure`: `turnover_structure_not_yet` fordi Turnover-observabelen splitter ikke target-384-profiler rent: quartet-majoritet 2/4, p2-pair-same 0.
- `observed_turnover_groups`: `observed` fordi mixed_turnover:add_chord_p0,add_chord_p1,add_chord_p2,local_swap_p1 | outer_diffuse_persistent:local_swap_p0,local_swap_p3 | outer_weighted_diffuse:add_chord_p3,local_swap_p2
- `next_step`: `new_scale_decision` fordi Neste steg bor vaere ny skalaavgjorelse.

## Tolkning

- Dette er en ny observabelklasse, ikke mer terskelarbeid pa gamle family-labels.
- Positivt signal her betyr at target-384 struktur ligger i tidsopplost turnover, ikke bare i statiske tail-snitter.
