# Relasjonell universgraf v0.15ao: terminal probe boundary lab

## Formal

Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter, det fokuserte `v15an`-settet og ett naerliggende delayed-probe-kontrollop for a splitte high-grensen videre.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Focus runs

| seed | role | start idx | runway | high hold | post mid | post low | last12 high | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5002161 | overlap_case | 40 | 32 | 0.875 | 0.125 | 0.000 | 0.833 | established_high_hold |
| 5002205 | typical_late_high_rise | 35 | 37 | 0.973 | 0.027 | 0.000 | 1.000 | established_high_hold |
| 5002220 | overlap_case | 69 | 3 | 1.000 | 0.000 | 0.000 | 0.250 | terminal_high_probe |
| 5002221 | nearby_probe_control | 9 | 63 | 0.222 | 0.349 | 0.429 | 0.000 | failed_early_high_probe |
| 5002240 | overlap_case | 72 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | no_high_hold_plateau |
| 5002241 | typical_late_high_rise | 42 | 30 | 0.733 | 0.267 | 0.000 | 0.917 | established_high_hold |
| 5002272 | typical_mid_plateau | 72 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | no_high_hold_plateau |
| 5002273 | typical_mid_plateau | 72 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | no_high_hold_plateau |
| 5002307 | typical_mid_plateau | 72 | 0 | 0.000 | 0.000 | 0.000 | 0.000 | no_high_hold_plateau |

## Aggregate

| label | n | rate | mean start idx | mean runway | mean hold | mean post mid | mean post low |
| --- | --- | --- | --- | --- | --- | --- | --- |
| established_high_hold | 3 | 0.333 | 39.0 | 33.0 | 0.860 | 0.140 | 0.000 |
| failed_early_high_probe | 1 | 0.111 | 9.0 | 63.0 | 0.222 | 0.349 | 0.429 |
| no_high_hold_plateau | 4 | 0.444 | 72.0 | 0.0 | 0.000 | 0.000 | 0.000 |
| terminal_high_probe | 1 | 0.111 | 69.0 | 3.0 | 1.000 | 0.000 | 0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er fortsatt rent separert; denne runden bruker bare ekte v15ai-, v15aj- og v15an-data.
- `terminal_probe_boundary_status`: `terminal_probe_boundary_is_structured` fordi Den smale high-grensen deler seg na i fire lesbare utfall: ekte high-hold, terminal high-probe, mislykket tidlig high-probe og ingen high-hold.
- `next_step`: `probe_terminal_vs_hold_trigger` fordi Neste steg bor forklare hva som bestemmer om sen high starter tidlig nok til a bli hold, i stedet for a ende som terminal probe.

## Tolkning

- Dette er fortsatt en liten grenseanalyse, ikke en ny scan.
- Les utfallene som haleutfall, ikke som nye defect-arter.
- Hvis denne runden virker, betyr det at residual- og probe-sporene er bedre forklart som en liten high-grensefamilie enn som generell boundary-mix.
