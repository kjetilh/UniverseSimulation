# Relasjonell universgraf v0.15r: add_chord long-horizon recurrence

## Formål

Denne runden følger bare noen få representative `add_chord`-traces lenger for å se om senfase-retur overlever på lang horisont.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Profile transitions

| profile | role | expected prefix | prefix | full | transition | prefix exact | full exact | full coarse |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| t48_g202_p2 | cyclic_candidate_primary | cyclic_return | cyclic_return | cyclic_return | sustained_cyclic_return | 0.723 | 0.969 | 0.961 |
| t96_g202_p3 | cyclic_candidate_secondary | cyclic_return | cyclic_return | morphology_return | cyclic_softens_to_morphology_return | 0.200 | 0.132 | 0.450 |
| t48_g101_p3 | morphology_control_primary | morphology_return | morphology_return | cyclic_return | mixed_transition | 0.015 | 0.977 | 1.000 |
| t48_g202_p1 | morphology_control_secondary | morphology_return | morphology_return | cyclic_return | mixed_transition | 0.154 | 1.000 | 0.961 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og de valgte add_chord-profilene matcher ønsket perturbasjonstype.
- `long_horizon_recurrence`: `cyclic_return_survives` fordi Minst én add_chord-profil holder ekte cyclic_return også på lengre horisont.
- `next_step`: `map_cycle_family` fordi Neste steg bør være en enda smalere kartlegging rundt den overlevende add_chord-cycle-familien.

## Tolkning

- Dette er en lang-horisont-runde for representative add_chord-profiler, ikke en bred ny scan.
- Les dette som recurrence i local defects, ikke som partikkelbevis eller generell geometri.
