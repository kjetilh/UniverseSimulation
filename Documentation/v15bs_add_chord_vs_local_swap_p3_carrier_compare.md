# Relasjonell universgraf v0.15bs: add_chord vs local_swap carrier compare at 96/p3

## Formal

Denne runden sammenlikner add_chord og local_swap direkte pa samme base, samme placement og samme holdout-seeds for a se om carrier-fordelen splitter mellom geometri og spectral renhet.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Carrier summary

| perturbation | exact | coarse | core | shell | rare | refresh | attach | spectral | dim | spectral rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord | 0.074 | 0.769 | 0.513 | 0.399 | 0.088 | 0.086 | 0.810 | 0.041 | 0.067 | 1 |
| local_swap | 0.034 | 0.743 | 0.484 | 0.403 | 0.113 | 0.093 | 0.793 | 0.037 | 0.070 | 1 |

## Comparison deltas

| coarse gap add-swap | core gap add-swap | rare gap add-swap | spectral gap swap-add | dim-minus-spectral gap swap-add |
| --- | --- | --- | --- | --- |
| 0.026 | 0.030 | -0.026 | 0.004 | 0.007 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle p3-runs matcher onsket perturbasjon.
- `carrier_compare`: `carrier_compare_still_mixed` fordi Carrier-sammenlikningen ved samme locus er fortsatt for blandet til en ren delt arbeidsdeling.
- `next_step`: `new_carrier_observable` fordi Neste steg bor bruke en ny carrier-observabel, ikke mer av samme p3-sammenlikning.

## Tolkning

- Dette er en ren carrier-sammenlikning ved samme lokale locus.
- Positivt signal her betyr ikke at noen perturbasjon er universelt best, men at de kan egne seg til ulike deler av videre geometri-/quasi-invariant-arbeid.
