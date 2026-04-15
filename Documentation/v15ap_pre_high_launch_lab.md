# Relasjonell universgraf v0.15ap: pre-high launch lab

## Formal

Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter og `v15ao`-runsettet for a lese high-grensen gjennom launch-vinduet rett for high enten holder, feiler eller uteblir.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Focus runs

| seed | high boundary | pre bands | pre high | pre mid | pre low | pre largest | pre active-comp | launch label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5002161 | established_high_hold | mmmmmmhm | 1 | 7 | 0 | 0.172 | 0.000 | mixed_threshold_launch |
| 5002205 | established_high_hold | mlmmmmhm | 1 | 6 | 1 | 0.226 | 0.000 | mixed_threshold_launch |
| 5002220 | terminal_high_probe | mmmmmmmm | 0 | 8 | 0 | 0.321 | 1.000 | compact_terminal_launch |
| 5002221 | failed_early_high_probe | mmmmmmmm | 0 | 8 | 0 | 0.196 | 0.000 | premature_probe_launch |
| 5002240 | no_high_hold_plateau | mmmmmmmm | 0 | 8 | 0 | 0.200 | 0.000 | no_launch_plateau |
| 5002241 | established_high_hold | lmlmmmhm | 1 | 5 | 2 | 0.237 | 0.000 | mixed_threshold_launch |
| 5002272 | no_high_hold_plateau | mmmmmllm | 0 | 6 | 2 | 0.265 | 0.000 | no_launch_plateau |
| 5002273 | no_high_hold_plateau | mmmmmmmm | 0 | 8 | 0 | 0.215 | 0.000 | no_launch_plateau |
| 5002307 | no_high_hold_plateau | mmmmmmmm | 0 | 8 | 0 | 0.167 | 1.000 | no_launch_plateau |

## Aggregate

| launch label | n | rate | mean pre high | mean pre mid | mean pre low | mean pre largest |
| --- | --- | --- | --- | --- | --- | --- |
| compact_terminal_launch | 1 | 0.111 | 0.000 | 8.000 | 0.000 | 0.321 |
| mixed_threshold_launch | 3 | 0.333 | 1.000 | 6.000 | 1.000 | 0.212 |
| no_launch_plateau | 4 | 0.444 | 0.000 | 7.500 | 0.500 | 0.211 |
| premature_probe_launch | 1 | 0.111 | 0.000 | 8.000 | 0.000 | 0.196 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er fortsatt rent separert; denne runden bruker bare ekte v15ai- og v15ao-data.
- `launch_map_status`: `pre_high_launch_map_supported` fordi Pre-high-vinduet deler de fire haleutfallene i et lite launch-kart: blandet threshold-launch, kompakt terminal launch, prematur probe-launch og ingen launch.
- `next_step`: `holdout_launch_map` fordi Neste steg bor teste om dette launch-kartet holder pa noen fa naerliggende seeds, ikke a scanne bredere.

## Tolkning

- Dette er fortsatt en liten launch-runde, ikke en ny scan.
- Les launch-labelene som lokale pre-high forklaringer, ikke som nye defect-arter.
- Hvis denne runden virker, betyr det at forskjellen mellom hold, terminal probe og failed probe faktisk er synlig allerede rett for high-forsoket.
