# Relasjonell universgraf v0.15cx: p1/1024 genealogy holdout

## Formal

Denne runden holder ut den konkrete v15cw-hypotesen for `add_chord_p1` ved target `1024`.
Den utvider ikke placement-rommet. Primaerdata er component trajectories og event logs; far-shell horizon er downstream outcome.

## Design

| field | value |
| --- | --- |
| target | 1024 |
| placement | p1 |
| growth seed | 202 |
| holdout seed deltas | 7411;7477;7541;7603 |
| v15cw calibration | `birth_death_churn -> no_far_shell_horizon`; `split_fragment -> established_far_shell_horizon` |

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 1024 | 1024.0 | 1024.0 | 1024.0 | 1 |

## Per-run holdout

| seed | horizon | genealogy pattern | expected from v15cw | match | split | birth | death | churn | max comps | max mass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7411 | established_far_shell_horizon | split_persistent_dual | ambiguous_from_v15cw_calibration | ambiguous | 198 | 584 | 521 | 1515 | 48 | 267 |
| 7477 | mixed_far_shell_horizon | split_persistent_dual | ambiguous_from_v15cw_calibration | ambiguous | 92 | 367 | 305 | 883 | 36 | 183 |
| 7541 | established_far_shell_horizon | split_persistent_dual | ambiguous_from_v15cw_calibration | ambiguous | 151 | 572 | 519 | 1398 | 40 | 215 |
| 7603 | established_far_shell_horizon | split_persistent_dual | ambiguous_from_v15cw_calibration | ambiguous | 218 | 677 | 599 | 1728 | 47 | 276 |

## Aggregate

| n | est rate | horizon | patterns | known mapping n | match rate | separates outcome | mean churn | mean max comps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 0.750 | 126.000 | split_persistent_dual:4 | 0 | nan | 0 | 1381.000 | 42.750 |

## Chain summary

| pattern | n | seeds | expected | est rate | mean horizon | mean churn | mean max mass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| split_persistent_dual | 4 | 7411;7477;7541;7603 | ambiguous_from_v15cw_calibration | 0.750 | 126.000 | 1381.000 | 235.250 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og alle requested add_chord-perturbations matcher faktisk perturbasjon.
- `holdout_scope`: `narrow_p1_1024_only` fordi Target 1024, placement p1, growth_seed 202, seeds (7411, 7477, 7541, 7603).
- `genealogy_holdout`: `p1_1024_specific_genealogy_axis_not_reproduced` fordi Ingen holdout-runs traff de to kalibrerte v15cw-patterns; patterns=split_persistent_dual:4. Dette svekker den konkrete birth_death_churn/split_fragment-mappingen, selv om genealogy-intensitet fortsatt kan vaere informativ.
- `next_step`: `build_continuous_genealogy_intensity_observable` fordi Neste steg bor score churn, split-timing, dual-duration og max-mass som kontinuerlige observabler mot horizon, ikke legge mer vekt paa grove event-chain labels.

## Tolkning

- Dette er en holdout av en konkret genealogy-mapping, ikke en ny partikkel-, Lorentz- eller invariantpaastand.
- Positivt resultat betyr bare at p1/1024-genealogien kan brukes som lokal selector under denne growth seeden.
- Negativt eller ambivalent resultat betyr at genealogy fortsatt er nyttig diagnostikk, men ikke en stabil selector alene.
