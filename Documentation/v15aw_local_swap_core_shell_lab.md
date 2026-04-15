# Relasjonell universgraf v0.15aw: local_swap core-shell recurrence lab

## Formål

Denne runden spør om local_swap-recurrence best leses som en stabil skadekjerne med variabel rand, slik add_chord etter hvert gjorde, eller om add_chord var et særtilfelle på denne observabelen.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Core-shell summary

| target | n | cyclic | morphology return | core+shell | static core | diffuse shell | mean core share | mean shell share | mean support core frac |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 8 | 0.125 | 0.875 | 1.000 | 0.000 | 0.000 | 0.692 | 0.296 | 1.000 |
| 96 | 8 | 0.000 | 1.000 | 0.125 | 0.000 | 0.625 | 0.340 | 0.408 | 0.958 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle smale local_swap-profiler matcher ønsket perturbasjon.
- `local_swap_core_shell_status`: `local_swap_core_shell_mixed` fordi local_swap får en del kjerne/rand-struktur, men ikke rent nok til én enkel generaliserende lesning ennå.
- `next_step`: `stay_local_on_swap` fordi Neste steg bør være en enda smalere local_swap-observabel, ikke en ny bred defect-scan.

## Tolkning

- Dette er en ny observabel på local_swap-sporet, ikke en ny add_chord-runde.
- Les dette som mesoskopisk morfologi for recurrence, ikke som bevis for partikler eller generell geometri.
