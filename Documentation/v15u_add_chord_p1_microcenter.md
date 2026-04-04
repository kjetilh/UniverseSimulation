# Relasjonell universgraf v0.15u: add_chord p1 microcenter

## Formål

Denne runden tester bare om `p1` faktisk er et lokalt maksimum mot begge nærmeste flanker `p0` og `p2` under friske holdout-seeds.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Microcenter summary

| placement | n | cyclic rate | mean full exact | q10 full exact | mean full coarse |
| --- | --- | --- | --- | --- | --- |
| 0 | 6 | 1.000 | 0.859 | 0.775 | 0.934 |
| 1 | 6 | 1.000 | 0.846 | 0.736 | 0.946 |
| 2 | 6 | 1.000 | 0.752 | 0.543 | 0.944 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle smale microcenter-profiler matcher ønsket add_chord-perturbasjon.
- `microcenter_status`: `microcenter_still_mixed` fordi P1 ser fortsatt lovende ut, men mikrocenteret er ikke rent nok skilt fra flankene til å kalles fullt avklart.
- `p1_vs_p0_seed_duels`: `p1_wins=3;p0_wins=2;ties=1` fordi Smale head-to-head-dueller pa samme seed_delta mellom p1 og p0.
- `p1_vs_p2_seed_duels`: `p1_wins=4;p2_wins=1;ties=1` fordi Smale head-to-head-dueller pa samme seed_delta mellom p1 og p2.
- `next_step`: `stay_micro` fordi Neste steg bør være en liten mekanistisk forklaringsrunde inne i p0-p1-p2-triplet.

## Tolkning

- Dette er en mikrotest inne i samme lokale add_chord-band, ikke en ny family-scan.
- Les resultatet som lokal robusthet eller flathet i et lite band, ikke som generell defect-lov.
