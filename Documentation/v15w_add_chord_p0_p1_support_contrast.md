# Relasjonell universgraf v0.15w: add_chord p0-vs-p1 support contrast

## Formål

Denne runden prøver å forklare den gjenværende p0-vs-p1-usikkerheten med støttegeometri og smale seed-dueller, uten å åpne ny mapping.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Support contrast

| placement | support | unique node | mean degree | ball1 | ball2 | ball3 | shell2/shell1 | ball3/ball1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p0 | 5,6,8 | 5 | 5.667 | 15.0 | 28.0 | 36.0 | 1.083 | 2.400 |
| p1 | 6,8,10 | 10 | 6.333 | 17.0 | 30.0 | 39.0 | 0.929 | 2.294 |

## Duel aggregate

| duel label | n | rate | mean exact gap | mean first-exact gap | mean lock gap | mean switch gap |
| --- | --- | --- | --- | --- | --- | --- |
| mixed_duel | 1 | 0.167 | -0.008 | 0.0 | -0.008 | 2.000 |
| p0_clean_advantage | 1 | 0.167 | -0.240 | 24.0 | -0.223 | 17.000 |
| p1_calm_advantage | 1 | 0.167 | 0.093 | 0.0 | 0.093 | -2.000 |
| p1_clean_advantage | 2 | 0.333 | 0.112 | -24.0 | 0.092 | -4.500 |
| speed_stability_tradeoff | 1 | 0.167 | -0.147 | -16.0 | -0.169 | 12.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert i denne støttekontrasten.
- `support_snapshot`: `degree_gap=0.667;ball1_gap=2.000;expansion_gap=-0.106` fordi Positiv degree/ball1-gap betyr tettere lokal støtte for p1. Negativ expansion-gap betyr at p0 har litt større relativ videre ekspansjon.
- `duel_snapshot`: `tradeoff_rate=0.167;p0_calm_rate=0.000;p1_clean_rate=0.333` fordi Dette oppsummerer hvordan p0 og p1 skiller lag på samme seed_delta i de smale holdout-duellene.
- `p0_p1_contrast`: `contrast_still_mixed` fordi Støttekontrasten gjør p0-vs-p1 mer konkret, men ikke ren nok til å gi én enkel forklaring ennå.
- `next_step`: `stay_local` fordi Neste steg bør være en enda mindre forklaringsrunde på unike noder eller første tail-segment.

## Tolkning

- Dette er en støttekontrast på samme lokale band, ikke en ny dynamikk-scan.
- Les dette som en liten forklaringsrunde for p0-vs-p1, ikke som generell defect-teori.
