# Relasjonell universgraf v0.15bt: same-locus carrier timing lab

## Formal

Denne runden tester om add_chord og local_swap skiller lag tydeligere i timingtekstur enn i de statiske carrier-maalingene fra v15bs.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 96 | 96.0 | 96.0 | 96.0 | 1 |

## Timing summary

| perturbation | anchored early lock | looser early lock | delayed lock | churn | first fragment step | first fragment attach | switches |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord | 0.500 | 0.500 | 0.000 | 0.000 | 1536.000 | 0.810 | 0.000 |
| local_swap | 0.333 | 0.667 | 0.000 | 0.000 | 1536.000 | 0.793 | 0.000 |

## Timing deltas

| anchored gap add-swap | churn gap swap-add | fragment step gap swap-add | attach gap add-swap | switch gap swap-add |
| --- | --- | --- | --- | --- |
| 0.167 | 0.000 | 0.000 | 0.017 | 0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle timing-runs matcher onsket perturbasjon.
- `carrier_timing_compare`: `carrier_timing_still_mixed` fordi Timing-observabelen gjor ikke carrier-duellen ren nok ved samme locus.
- `next_step`: `new_cross_carrier_observable` fordi Neste steg bor bruke en helt ny carrier-observabel, ikke flere timing-varianter av samme duell.

## Tolkning

- Dette er en timingobservabel pa samme locus, ikke en ny bred carrier-scan.
- Positivt signal her betyr bare at carrierne skiller lag i hvordan de laaser seg inn i halen, ikke at vi allerede har en full geometri-lov.
