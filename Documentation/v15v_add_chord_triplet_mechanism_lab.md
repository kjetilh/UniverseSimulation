# Relasjonell universgraf v0.15v: add_chord triplet mechanism lab

## Formål

Denne runden forklarer det blandede `p0-p1-p2`-bildet med enkle tail-lock-observabler i stedet for å åpne et nytt søk.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Triplet mechanism summary

| placement | n | early stable | late stable | intermittent | coarse shell | mean first exact | mean lock frac | mean switch count | dominant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6 | 0.000 | 0.000 | 1.000 | 0.000 | 1557.3 | 0.878 | 8.167 | intermittent_cycle_lock |
| 1 | 6 | 0.167 | 0.000 | 0.833 | 0.000 | 1550.7 | 0.858 | 11.500 | intermittent_cycle_lock |
| 2 | 6 | 0.333 | 0.000 | 0.333 | 0.333 | 1557.3 | 0.764 | 11.667 | coarse_cycle_shell |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle add_chord-rundene matcher ønsket perturbasjon.
- `triplet_mechanism_status`: `triplet_mechanism_still_mixed` fordi Mekanismelesningen gjør triplet-en mer forklarbar, men ikke ren nok til å løse sentrumssporsmalet.
- `tail_lock_snapshot`: `p0_lock=0.000;p1_lock=0.167;p2_lock=0.333` fordi Mean first exact return: p0=1557.3, p1=1550.7, p2=1557.3. Mean switch count: p0=8.2, p1=11.5, p2=11.7.
- `next_step`: `stay_micro` fordi Neste steg bør være en enda mindre støtte-/mekanismetest inne i samme triplet.

## Tolkning

- Dette er en mekanistisk forklaringsrunde inne i samme triplet, ikke en ny cycle-map.
- Les dette som lokal tail-lock-struktur, ikke som generell defect-fysikk.
