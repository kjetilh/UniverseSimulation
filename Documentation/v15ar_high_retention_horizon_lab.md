# Relasjonell universgraf v0.15ar: high retention horizon lab

## Formal

Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter og `v15ap`-runsettet for a lese high-grensen gjennom hvor lenge high faktisk blir vaerende etter start.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Focus runs

| seed | launch label | start | last high | horizon | retention | last12 high | horizon label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5002161 | mixed_threshold_launch | 40 | 71 | 32 | 0.875 | 0.833 | established_hold_horizon |
| 5002205 | mixed_threshold_launch | 35 | 71 | 37 | 0.973 | 1.000 | established_hold_horizon |
| 5002220 | compact_terminal_launch | 69 | 71 | 3 | 1.000 | 0.250 | terminal_probe_horizon |
| 5002221 | premature_probe_launch | 9 | 24 | 16 | 0.875 | 0.000 | failed_probe_horizon |
| 5002240 | no_launch_plateau | 72 | -1 | 0 | 0.000 | 0.000 | no_high_presence |
| 5002241 | mixed_threshold_launch | 42 | 71 | 30 | 0.733 | 0.917 | established_hold_horizon |
| 5002272 | no_launch_plateau | 72 | -1 | 0 | 0.000 | 0.000 | no_high_presence |
| 5002273 | no_launch_plateau | 72 | -1 | 0 | 0.000 | 0.000 | no_high_presence |
| 5002307 | no_launch_plateau | 72 | -1 | 0 | 0.000 | 0.000 | no_high_presence |

## Aggregate

| horizon label | n | rate | mean start | mean last high | mean horizon | mean retention |
| --- | --- | --- | --- | --- | --- | --- |
| established_hold_horizon | 3 | 0.333 | 39.000 | 71.000 | 33.000 | 0.860 |
| failed_probe_horizon | 1 | 0.111 | 9.000 | 24.000 | 16.000 | 0.875 |
| no_high_presence | 4 | 0.444 | 72.000 | -1.000 | 0.000 | 0.000 |
| terminal_probe_horizon | 1 | 0.111 | 69.000 | 71.000 | 3.000 | 1.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er fortsatt rent separert; denne runden bruker bare ekte v15ai- og v15ap-data.
- `horizon_map_status`: `horizon_map_supported` fordi High-grensen blir na rent lest som et lite horisont-kart: ekte hold-horisont, terminal probe-horisont, failed probe-horisont og ingen high-presens.
- `next_step`: `holdout_horizon_map` fordi Neste steg bor teste dette horisont-kartet pa noen fa naerliggende seeds, ikke a scanne bredere.

## Tolkning

- Dette er fortsatt en liten horisont-runde, ikke en ny scan.
- Les horisont-labelene som lokale high-forlop, ikke som nye defect-arter.
- Hvis denne runden virker, betyr det at forskjellen mellom hold, terminal probe og failed probe er lesbar i hvor langt high faktisk rekker a leve.
