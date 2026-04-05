# Relasjonell universgraf v0.15x: add_chord p0-vs-p1 first tail segment

## Formål

Denne runden sammenligner bare første tail-segment for `p0` og `p1`, for å se om forskjellen deres skyldes tidligere konsolidering, roligere tail-lock eller en blanding.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Duel aggregate

| duel label | n | rate | first gap | component gap | largest gap | boundary gap | jaccard gap | post-switch gap | exact gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mixed_first_segment | 6 | 1.000 | -6.7 | 0.208 | -0.004 | 0.002 | 0.017 | 3.333 | -0.013 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert i denne første-tail-segment-runden.
- `duel_family_snapshot`: `p1_early=0.000;p1_soft=0.000;tradeoff=0.000;p0_calm=0.000` fordi Dette oppsummerer hvordan p0 og p1 skiller lag i første tail-segment på de samme små holdout-seedene.
- `first_segment_status`: `first_segment_still_mixed` fordi Første tail-segment gjør forskjellen mer konkret, men ikke rent nok til én enkel mekanisme.
- `next_step`: `stay_tiny` fordi Neste steg bør være en enda mindre forklaringsrunde på én eller to seed-caser.

## Tolkning

- Dette er en første-tail-segment-runde på samme `p0`/`p1`-dueller, ikke en ny seed-scan.
- Les dette som lokal onset-mekanikk, ikke som generell defect-lov.
