# Relasjonell universgraf v0.15as: horizon map holdout

## Formal

Denne runden tester om det lille high-horisont-kartet fra `v15ar` holder pa noen fa naerliggende seeds rundt de representative anker-runene.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Holdout summary

| placement | anchor run | anchor delta | expected | match | mixed | different | observed mode | mean horizon | mean retention |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 5002241 | 239 | established_hold_horizon | 0.000 | 0.500 | 0.500 | no_high_presence | 10.500 | 0.405 |
| 1 | 5002220 | 219 | terminal_probe_horizon | 0.000 | 0.000 | 1.000 | no_high_presence | 0.000 | 0.000 |
| 2 | 5002221 | 219 | failed_probe_horizon | 0.000 | 0.000 | 1.000 | no_high_presence | 0.000 | 0.000 |
| 1 | 5002240 | 239 | no_high_presence | 1.000 | 0.000 | 0.000 | no_high_presence | 0.000 | 0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle holdout-runene matcher onsket add_chord-perturbasjon.
- `horizon_holdout_status`: `horizon_map_holdout_mixed` fordi Horisont-kartet gir fortsatt nyttig struktur pa holdouts, men holder ikke rent nok som lokalt lovmessig kart ennå.
- `next_step`: `tighten_failed_probe_horizon` fordi Neste steg bor vaere en enda smalere observabel eller holdout rundt failed-probe og terminal-probe-grensen.

## Tolkning

- Dette er en liten holdout-runde rundt horisontankrene, ikke en ny bred seed-scan.
- Les horisont-labelene som lokale high-forlop, ikke som nye defect-arter.
