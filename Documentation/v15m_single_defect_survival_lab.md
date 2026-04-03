# Relasjonell universgraf v0.15m: single-defect survival lab

## Formål

Denne runden skifter bort fra kollisjoner og tester et nytt defect-spørsmål: om `token_shift` viser en ekte survival/extinction-splitt, med `add_chord` som levende kontroll.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Aggregate survival / tail

| perturbation | target | alive | extinction | late extinction | split tail | quiet tail | mixed | dominant |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord | 48 | 1.000 | 0.000 | 0.000 | 0.333 | 0.083 | 0.000 | persistent_diffuse_tail |
| add_chord | 96 | 1.000 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | persistent_split_tail |
| token_shift | 48 | 0.833 | 0.167 | 0.000 | 0.333 | 0.000 | 0.000 | persistent_diffuse_tail |
| token_shift | 96 | 0.917 | 0.083 | 0.000 | 0.833 | 0.083 | 0.000 | persistent_split_tail |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er fortsatt rent separert i denne runden.
- `survival_signal`: `token_shift_extinction_not_clean` fordi Token_shift skiller seg ikke klart nok fra add_chord til å kalle dette et rent survival/extinction-spor ennå.
- `next_step`: `pause_survival_claims` fordi Neste steg bør være mer forsiktig eller bytte defect-spørsmål igjen.

## Tolkning

- Dette er et nytt defect-spørsmål, ikke en utvidelse av collision-generaliseringen.
- Poenget er å se om én perturbasjonstype faktisk har en egen survival-/extinction-dynamikk.
