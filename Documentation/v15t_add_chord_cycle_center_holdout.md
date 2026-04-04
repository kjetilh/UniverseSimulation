# Relasjonell universgraf v0.15t: add_chord cycle-center holdout

## Formål

Denne runden holder seg inne i `v15s`-båndet og tester bare om `p1` faktisk er et sterkere lokalt cycle-sentrum enn `p2` under noen få nye dynamikk-seeds.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Holdout summary

| placement | n | cyclic rate | mean full exact | q10 full exact | mean full coarse |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | 1.000 | 0.897 | 0.806 | 0.968 |
| 2 | 6 | 0.833 | 0.744 | 0.419 | 0.961 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle smale holdout-profiler matcher ønsket add_chord-perturbasjon.
- `cycle_center_status`: `shifted_center_p1` fordi Plassering 1 holder høyere cycle-rate og høyere exact-return over de smale holdout-seedene enn plassering 2.
- `pairwise_seed_duels`: `p1_wins=4;p2_wins=2;ties=0` fordi Dette teller bare smale head-to-head-dueller på samme seed_delta, med 0.01 som liten likevektsterskel.
- `next_step`: `probe_p1_microcenter` fordi Neste steg bør være en enda smalere mikrotest rundt p1 som lokalt cycle-sentrum.

## Tolkning

- Dette er en smal holdout-test inne i samme lokale cycle-band, ikke en ny placement-scan.
- Les resultatet som lokal robusthet for cycle-bandet, ikke som bevis for en universell defect-lov.
