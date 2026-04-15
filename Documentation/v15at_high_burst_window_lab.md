# Relasjonell universgraf v0.15at: high burst window lab

## Formal

Denne runden tester om den skjore high-grensen leses bedre som et lite burst-kart enn som bare horisont- eller impulse-etiketter.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Focus runs

| role | run seed | expected horizon | first high | last high | total high | peak start | peak rate | burst label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| anchor_focus | 5002220 | terminal_probe_horizon | 69 | 71 | 3 | 64 | 0.375 | terminal_compact_burst |
| anchor_focus | 5002221 | failed_probe_horizon | 9 | 24 | 14 | 9 | 0.875 | early_failed_burst |
| anchor_focus | 5002240 | no_high_presence | 72 | -1 | 4 | 28 | 0.375 | no_high_burst |
| anchor_focus | 5002241 | established_hold_horizon | 42 | 71 | 23 | 61 | 1.000 | sustained_hold_burst |
| holdout_focus | 5002212 | terminal_probe_horizon | 72 | -1 | 0 | 0 | 0.000 | no_high_burst |
| holdout_focus | 5002213 | failed_probe_horizon | 72 | -1 | 0 | 0 | 0.000 | no_high_burst |
| holdout_focus | 5002228 | terminal_probe_horizon | 72 | -1 | 0 | 0 | 0.000 | no_high_burst |
| holdout_focus | 5002229 | failed_probe_horizon | 72 | -1 | 0 | 0 | 0.000 | no_high_burst |
| holdout_focus | 5002232 | no_high_presence | 72 | -1 | 0 | 0 | 0.000 | no_high_burst |
| holdout_focus | 5002233 | established_hold_horizon | 40 | 60 | 17 | 51 | 1.000 | fading_late_burst |
| holdout_focus | 5002248 | no_high_presence | 72 | -1 | 0 | 0 | 0.000 | no_high_burst |
| holdout_focus | 5002249 | established_hold_horizon | 72 | -1 | 0 | 0 | 0.000 | no_high_burst |

## Aggregate by role

| role | n | sustained | terminal | failed | no-high | fading late | mixed | burst mode |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| anchor_focus | 4 | 0.250 | 0.250 | 0.250 | 0.250 | 0.000 | 0.000 | terminal_compact_burst |
| holdout_focus | 8 | 0.000 | 0.000 | 0.000 | 0.875 | 0.125 | 0.000 | no_high_burst |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle run i denne runden matcher onsket add_chord-perturbasjon.
- `burst_map_status`: `burst_map_sharpens_holdout_collapse` fordi Burst-observabelen holder ankerkartet rent og viser samtidig at naerliggende holdouts hovedsakelig kollapser til `no_high_burst`, med et lite restspor av `fading_late_burst` i stedet for ekte hold.
- `next_step`: `explain_fading_late_burst` fordi Neste steg bor forklare det lille `fading_late_burst`-sporet i stedet for a presse horisontkartet hardere.

## Tolkning

- Dette er en liten burst-runde rundt samme boundary-run, ikke en ny bred seed-scan.
- Les burst-labelene som lokale high-forlop, ikke som nye defect-arter.
