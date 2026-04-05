# Relasjonell universgraf v0.15aa: p0-vs-p1 case trigger holdout

## Formål

Denne runden tester om de tre onset-triggerne fra `v15z` har lokal bæreevne i noen få nærliggende holdout-seeds.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Holdout rows

| anchor | holdout | expected | observed | status | exact gap | first gap | first comp gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 151 | 139 | p1_compact_radius_trigger | mixed_trigger | mixed_holdout | -0.085 | 8.0 | 0.000 |
| 151 | 163 | p1_compact_radius_trigger | mixed_trigger | mixed_holdout | 0.023 | 32.0 | 0.000 |
| 239 | 227 | fragmented_fast_tradeoff_trigger | mixed_trigger | mixed_holdout | -0.085 | 32.0 | -1.000 |
| 239 | 251 | fragmented_fast_tradeoff_trigger | mixed_trigger | mixed_holdout | -0.008 | 8.0 | -1.000 |
| 271 | 259 | p0_calm_singleton_trigger | mixed_trigger | mixed_holdout | 0.023 | 0.0 | -1.000 |
| 271 | 283 | p0_calm_singleton_trigger | mixed_trigger | mixed_holdout | -0.093 | 88.0 | 2.000 |

## Family aggregate

| anchor | expected | match rate | mixed rate | shift rate | status |
| --- | --- | --- | --- | --- | --- |
| 151 | p1_compact_radius_trigger | 0.000 | 1.000 | 0.000 | not_supported |
| 239 | fragmented_fast_tradeoff_trigger | 0.000 | 1.000 | 0.000 | not_supported |
| 271 | p0_calm_singleton_trigger | 0.000 | 1.000 | 0.000 | not_supported |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle holdout-runene matcher ønsket add_chord-perturbasjon.
- `family_snapshot`: `fully_supported=0;partly_supported=0;contested=0;not_supported=3` fordi Dette oppsummerer hvor mange av de tre lokale trigger-familiene som holder i de nærliggende holdout-seedene.
- `trigger_holdout_status`: `trigger_holdout_not_yet` fordi Trigger-historien holder ikke rent nok i nærliggende seeds til å kalles stabil ennå.
- `next_step`: `stop_generalizing` fordi Neste steg bør være en ny observabel eller et annet defect-spørsmål, ikke mer trigger-generalisering.

## Tolkning

- Les denne runden som lokal trigger-holdout, ikke som bred generalisering.
- Målet her er bare å se om `v15z`-forklaringen bærer litt utover de tre opprinnelige case-seedene.
