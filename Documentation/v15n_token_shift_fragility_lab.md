# Relasjonell universgraf v0.15n: token_shift fragility lab

## Formål

Denne runden tester ikke om `token_shift` har en stor egen survival-lov. Den spør mer presist om den delvise skjørheten i `v15m` følger lokal støttegeometri, med `add_chord` som levende kontroll.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Aggregate fragility

| perturbation | target | extinction | split tail | diffuse tail | quiet tail | dominant |
| --- | --- | --- | --- | --- | --- | --- |
| add_chord | 48 | 0.000 | 0.429 | 0.500 | 0.000 | persistent_diffuse_tail |
| add_chord | 96 | 0.000 | 1.000 | 0.000 | 0.000 | persistent_split_tail |
| token_shift | 48 | 0.143 | 0.429 | 0.429 | 0.000 | persistent_split_tail |
| token_shift | 96 | 0.067 | 0.867 | 0.000 | 0.067 | persistent_split_tail |

## Token_shift feature contrast

| feature | extinct mean | alive mean | delta |
| --- | --- | --- | --- |
| mean_support_degree | 5.667 | 5.173 | 0.494 |
| support_ball_2 | 22.667 | 21.000 | 1.667 |
| support_ball_3 | 34.000 | 31.462 | 2.538 |
| support_shell_2 | 12.000 | 11.038 | 0.962 |
| shell2_over_shell1 | 1.637 | 1.494 | 0.143 |
| ball3_over_ball1 | 3.500 | 3.300 | 0.200 |

## Placement contrast

- `token_extinct_add_alive_count`: `3`

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle testede perturbasjoner matcher ønsket type.
- `fragility_signal`: `placement_structured_fragility` fordi Token_shift-extinctionen ser delvis plassering-/støttestruert ut, med lokale støttefeatures som skiller extinct fra levende runs bedre enn i v15m alene.
- `next_step`: `follow_fragility_geometry` fordi Neste steg bør være en enda smalere token_shift-runde rundt de mest skjøre støtteprofilene, ikke brede survival-paastander.

## Tolkning

- Dette er en smal fragility-runde, ikke en ny collision-runde.
- Les fortsatt dette som defect-dynamikk, ikke som partikkelbevis eller ny generell geometri.
