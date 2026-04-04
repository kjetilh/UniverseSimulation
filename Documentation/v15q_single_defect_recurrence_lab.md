# Relasjonell universgraf v0.15q: single-defect recurrence lab

## Formål

Denne runden spør om single defects kommer tilbake til tidligere morfologier i senfasen, eller om de for det meste bare fortsetter å drive.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Aggregate recurrence

| perturbation | target | cyclic | morphology return | near return | extinct-after-return | drifting | dominant |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord | 48 | 0.125 | 0.875 | 0.000 | 0.000 | 0.000 | morphology_return |
| add_chord | 96 | 0.125 | 0.875 | 0.000 | 0.000 | 0.000 | morphology_return |
| local_swap | 48 | 0.125 | 0.875 | 0.000 | 0.000 | 0.000 | morphology_return |
| local_swap | 96 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | morphology_return |
| token_shift | 48 | 0.250 | 0.500 | 0.000 | 0.250 | 0.000 | morphology_return |
| token_shift | 96 | 0.125 | 0.875 | 0.000 | 0.000 | 0.000 | morphology_return |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle testede perturbasjoner matcher ønsket type.
- `recurrence_signal`: `late_return_signal_present` fordi `add_chord` viser den tydeligste senfase-returstrukturen i denne smale runden, men fortsatt bare som lokal defect-dynamikk.
- `next_step`: `follow_recurrence_family` fordi Neste steg bør være en enda smalere retur-/recurrence-runde for `add_chord`, ikke brede defect-paastander.

## Tolkning

- Dette er en single-defect-runde, ikke en collision-runde.
- Les dette som morfologisk recurrence i lokale defects, ikke som partikkelbevis eller generell geometri.
