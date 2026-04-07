# Relasjonell universgraf v0.15ae: add_chord shell topology lab

## Formal

Denne runden spør om den rolige variable randen rundt add_chord-kjernen vanligvis holder seg sammenhengende, blir fragmentert, eller bærer lokal cycle-rank.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Shell-topology summary

| placement | n | cyclic | connected shell | looped shell | fragmented shell | mixed shell | mean comp | mean connected | mean loop |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 | 3.352 | 0.090 | 0.000 |
| 1 | 6 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 | 3.551 | 0.108 | 0.000 |
| 2 | 6 | 1.000 | 0.000 | 0.000 | 0.833 | 0.167 | 4.184 | 0.177 | 0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle shell-topologiprofilene matcher onsket add_chord-perturbasjon.
- `shell_topology_status`: `cycle_band_has_fragmented_shell_zone` fordi Minst ett av de lokale punktene ser ofte ut til a bryte randen opp i flere separate biter.
- `next_step`: `localize_fragment_events` fordi Neste steg bør finne hvor i halen disse fragmenteringene oppstar, ikke scanne bredere.

## Tolkning

- Dette er fortsatt samme smale `t48_g202`-band, ikke en ny bred scan.
- Les topologi her som en lokal randobservabel, ikke som bevis for en generell defect-lov.
