# Relasjonell universgraf v0.15p: token_shift profile refinement

## Formål

Denne runden tester bare den sterkeste skjøre `token_shift`-profilen fra v15o (`p3` på target 48 / growth seed 101) mot to bedre matchede levende kontroller på samme base.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Aggregate by role

| role | perturbation | extinction | split tail | diffuse tail | quiet tail | dominant |
| --- | --- | --- | --- | --- | --- | --- |
| control_adjacent_p4 | add_chord | 0.000 | 0.438 | 0.438 | 0.000 | persistent_split_tail |
| control_adjacent_p4 | token_shift | 0.250 | 0.375 | 0.125 | 0.000 | persistent_split_tail |
| control_ball3_p1 | add_chord | 0.000 | 0.562 | 0.375 | 0.000 | persistent_split_tail |
| control_ball3_p1 | token_shift | 0.312 | 0.500 | 0.188 | 0.000 | persistent_split_tail |
| fragile_p3 | add_chord | 0.000 | 0.188 | 0.500 | 0.000 | persistent_diffuse_tail |
| fragile_p3 | token_shift | 0.188 | 0.312 | 0.438 | 0.000 | persistent_diffuse_tail |

## Role diagnosis

| control | token fragile ext | token control ext | token gap | add fragile ext | add control ext | status |
| --- | --- | --- | --- | --- | --- | --- |
| control_ball3_p1 | 0.188 | 0.312 | -0.125 | 0.000 | 0.000 | no_clean_gap |
| control_adjacent_p4 | 0.188 | 0.250 | -0.062 | 0.000 | 0.000 | no_clean_gap |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsen holder fortsatt rent og alle replikerte perturbasjoner matcher ønsket type.
- `profile_refinement`: `not_supported` fordi Den skjøre `p3`-profilen holder ikke et rent extinction-gap mot de bedre matchede kontrollene.
- `next_step`: `pivot_again` fordi Neste steg bør være et annet smalt defect-spørsmål heller enn mer token_shift-fragility langs denne profilen.

## Tolkning

- Dette er en mikro-runde rundt én lokal profil, ikke en ny bred defect-scan.
- Les fortsatt dette som local fragility, ikke som partikkelbevis eller generell geometri.
