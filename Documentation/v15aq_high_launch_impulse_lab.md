# Relasjonell universgraf v0.15aq: high launch impulse lab

## Formal

Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter og `v15ap`-runsettet for a lese high-grensen gjennom det aller forste post-launch-vinduet.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Focus runs

| seed | launch label | post bands | high8 | mid8 | longest high | active gain | impulse label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5002161 | mixed_threshold_launch | hhhhhhhh | 1.000 | 0.000 | 8 | 1.500 | sustained_hold_impulse |
| 5002205 | mixed_threshold_launch | hhhhhmhh | 0.875 | 0.125 | 5 | 2.625 | sustained_hold_impulse |
| 5002220 | compact_terminal_launch | hhh | 1.000 | 0.000 | 3 | 1.417 | compact_late_spike |
| 5002221 | premature_probe_launch | hhhhhhmh | 0.875 | 0.125 | 6 | 1.750 | soft_failed_impulse |
| 5002240 | no_launch_plateau |  | 0.000 | 0.000 | 0 | -5.125 | inactive_mid_plateau |
| 5002241 | mixed_threshold_launch | hhhmmhhh | 0.750 | 0.250 | 3 | 2.500 | rebounding_hold_impulse |
| 5002272 | no_launch_plateau |  | 0.000 | 0.000 | 0 | -3.875 | inactive_mid_plateau |
| 5002273 | no_launch_plateau |  | 0.000 | 0.000 | 0 | -4.750 | inactive_mid_plateau |
| 5002307 | no_launch_plateau |  | 0.000 | 0.000 | 0 | -6.000 | inactive_mid_plateau |

## Aggregate

| impulse label | n | rate | mean high8 | mean mid8 | mean longest high | mean active gain |
| --- | --- | --- | --- | --- | --- | --- |
| compact_late_spike | 1 | 0.111 | 1.000 | 0.000 | 3.000 | 1.417 |
| inactive_mid_plateau | 4 | 0.444 | 0.000 | 0.000 | 0.000 | -4.938 |
| rebounding_hold_impulse | 1 | 0.111 | 0.750 | 0.250 | 3.000 | 2.500 |
| soft_failed_impulse | 1 | 0.111 | 0.875 | 0.125 | 6.000 | 1.750 |
| sustained_hold_impulse | 2 | 0.222 | 0.938 | 0.062 | 6.500 | 2.062 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er fortsatt rent separert; denne runden bruker bare ekte v15ai- og v15ap-data.
- `impulse_map_status`: `launch_impulse_map_still_mixed` fordi Impulsvinduet gir litt mer struktur, men ikke et rent nok kart ennå.
- `next_step`: `change_impulse_observable` fordi Neste steg bor bytte impulsobservabel i stedet for a presse dette kartet hardere.

## Tolkning

- Dette er fortsatt en liten impulse-runde, ikke en ny scan.
- Les impulslabelene som lokale onset-forklaringer, ikke som nye defect-arter.
- Hvis denne runden virker, betyr det at forskjellen mellom hold og probe er lesbar allerede i det aller forste launch-stoetet.
