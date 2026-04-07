# Relasjonell universgraf v0.15ad: add_chord boundary-shell dynamics lab

## Formål

Denne runden spør om den variable randen i det lokale add_chord-båndet skifter rolig og inkrementelt, eller i mer bursty hopp.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Boundary-shell summary

| placement | n | cyclic | calm shell | bursty shell | mixed shell | mean refresh | mean burst | mean shell cover |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6 | 1.000 | 1.000 | 0.000 | 0.000 | 0.080 | 0.052 | 0.653 |
| 1 | 6 | 1.000 | 0.667 | 0.000 | 0.333 | 0.091 | 0.061 | 0.628 |
| 2 | 6 | 1.000 | 0.667 | 0.000 | 0.333 | 0.085 | 0.057 | 0.623 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle smale boundary-shell-profiler matcher ønsket add_chord-perturbasjon.
- `boundary_shell_status`: `core_shell_variation_is_calm` fordi Randen ser ut til å flimre ganske rolig og inkrementelt, ikke i store resets eller bursts.
- `next_step`: `probe_shell_topology` fordi Neste steg bør måle randtopologien mer direkte, siden variasjonen ser reell men rolig ut.

## Tolkning

- Dette er en rand-observabel inne i det samme lokale add_chord-båndet, ikke en ny placement-scan.
- Les dette som dynamikk i den variable randen, ikke som bevis for en generell defect-lov.
