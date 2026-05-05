# Relasjonell universgraf v0.15cg: target-768 far-shell horizon lab

## Formal

Denne runden tester om target `768` leses bedre gjennom en vedvarende far-shell-horisont ved placement `2` enn gjennom brede family-labels.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 768 | 768.0 | 768.0 | 768.0 | 1 |

## Profile summary

| profile | established | late probe | failed | none | coarse | horizon | retention | last12 high | total high | far share | q90 far share | distance | spectral rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | 0.000 | 0.000 | 0.000 | 1.000 | 0.882 | 0.000 | 0.000 | 0.000 | 0.000 | 0.577 | 0.630 | 4.430 | 0.012 |
| add_chord_p2 | 0.500 | 0.000 | 0.000 | 0.500 | 0.841 | 64.500 | 0.500 | 0.500 | 64.500 | 0.480 | 0.546 | 4.930 | 0.004 |
| local_swap_p0 | 0.000 | 0.000 | 0.000 | 1.000 | 0.773 | 0.000 | 0.000 | 0.000 | 0.000 | 0.577 | 0.633 | 4.181 | 0.007 |
| local_swap_p2 | 0.750 | 0.000 | 0.000 | 0.250 | 0.948 | 96.750 | 0.750 | 0.750 | 96.750 | 0.782 | 0.837 | 7.502 | 0.010 |

## P2 versus P0

| compare | established gap | retention gap | last12 high gap | horizon gap | total high gap | far share gap | q90 far share gap | distance gap | spectral gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p2_minus_p0 | 0.500 | 0.500 | 0.500 | 64.500 | 64.500 | -0.097 | -0.084 | 0.500 | -0.008 |
| local_swap_p2_minus_p0 | 0.750 | 0.750 | 0.750 | 96.750 | 96.750 | 0.205 | 0.204 | 3.321 | 0.004 |

## Carrier gap

| compare | established gap | retention gap | last12 high gap | horizon gap | total high gap | far share gap | distance gap | spectral gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| carrier_gap_at_p0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.249 | 0.005 |
| carrier_gap_at_p2 | 0.250 | 0.250 | 0.250 | 32.250 | 32.250 | 0.302 | 2.571 | 0.006 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle target-768 far-shell-runs matcher onsket perturbasjon.
- `far_shell_horizon`: `far_shell_horizon_weak` fordi Far-shell-horisonten gir en svak p2->p0-splittelse (scores add=3, swap=6), men ikke rent nok ennå.
- `next_step`: `narrow_p2_horizon_holdout_or_second_observable` fordi Neste steg bor vaere en enda smalere p2-holdout eller en komplementar target-768-observabel.

## Tolkning

- Dette er en smal target-768-observabel rundt p2-lommen, ikke mer bred family-tuning.
- Positivt signal her betyr at p2 holder far-shell-overvekt over tid, ikke bare i tail-gjennomsnitt.
