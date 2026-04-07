# Relasjonell universgraf v0.15ac: add_chord core-shell recurrence lab

## Formål

Denne runden spør om det lokale add_chord-recurrence-båndet ser ut som en stabil skadekjerne med flimrende rand, eller som bred diffus turnover uten en tydelig vedvarende kjerne.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Core-shell summary

| placement | n | cyclic | core+shell | static core | diffuse shell | mean core share | mean shell share | mean support core frac |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6 | 1.000 | 0.500 | 0.500 | 0.000 | 0.879 | 0.108 | 1.000 |
| 1 | 6 | 1.000 | 0.500 | 0.500 | 0.000 | 0.892 | 0.108 | 1.000 |
| 2 | 6 | 1.000 | 0.667 | 0.333 | 0.000 | 0.855 | 0.145 | 1.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle smale core-shell-profiler matcher ønsket add_chord-perturbasjon.
- `core_shell_status`: `cycle_band_is_core_shell` fordi Det lokale add_chord-båndet ser ut til å være drevet av en stabil kjerne med variabel rand, ikke av en skarp periode.
- `next_step`: `probe_boundary_shell` fordi Neste steg bør måle randdynamikken mer direkte, siden det nå ser ut til å være der variasjonen sitter.

## Tolkning

- Dette er en ny observabel inne i samme lokale add_chord-band, ikke en ny placement-scan.
- Les dette som kjerne/rand-diagnostikk for recurrence, ikke som bevis for en generell defect-lov.
