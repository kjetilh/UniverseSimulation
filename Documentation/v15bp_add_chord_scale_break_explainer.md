# Relasjonell universgraf v0.15bp: add_chord scale-break explainer

## Formal

Denne runden forklarer hvorfor 48/p2 ikke holder som en ren liten skalafamilie ved 96 etter v15bo.

## Bruddtyper mot ankeret

| profile | role | break label | exact gap | coarse gap | core gap | shell gap | rare gap | spectral rank | best metric |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| control_96_p1 | control | geometry_without_spectral_hold | -0.774 | -0.041 | -0.268 | 0.225 | 0.043 | 2 | abs_delta_dim_proxy_rel |
| candidate_96_p3 | candidate | spectral_without_geometry_hold | -0.704 | -0.112 | -0.342 | 0.238 | 0.105 | 1 | abs_delta_spectral_radius_rel |

## Operativ lesning

- `scale_break`: `split_scale_break_supported` fordi 96/p3 holder spectral rang, men glipper geometrisk; 96/p1 holder bedre coarse-geometri, men glipper spectralt. Skalabruddet ser derfor ut som en delt breaking av samme familiekrav.
- `next_step`: `pause_scale_transfer_claim` fordi Neste steg bor ikke presse mer pa samme scale-transfer-claim uten en ny coarse observabel eller et annet carrier-spor.

## Tolkning

- Dette er en forklaringsrunde, ikke en ny simulering.
- Poenget er a lokalisere om 48->96-bruddet sitter i spectral rang, coarse geometri eller begge.
