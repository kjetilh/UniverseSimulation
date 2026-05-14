# Relasjonell universgraf v0.15cw: add_chord p1/p3 genealogy seed split

## Formal

Denne runden holder v15cv-scope fast og legger til komponentgenealogi per run.
Far-shell horizon er downstream outcome; primaerdata er component trajectories og event logs.

## Design

| field | value |
| --- | --- |
| targets | 896;1024 |
| placements | p1;p3 |
| seed deltas | 7307;7351 |

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 896 | 896.0 | 896.0 | 896.0 | 1 |
| 1024 | 1024.0 | 1024.0 | 1024.0 | 1 |

## Per-run genealogy

| target | placement | seed | horizon | genealogy pattern | split | birth | death | max comps | max mass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 896 | p1 | 7307 | established_far_shell_horizon | split_persistent_dual | 89 | 225 | 186 | 38 | 164 |
| 896 | p1 | 7351 | no_far_shell_horizon | split_persistent_dual | 3 | 16 | 11 | 11 | 18 |
| 896 | p3 | 7307 | no_far_shell_horizon | split_persistent_dual | 40 | 187 | 159 | 24 | 93 |
| 896 | p3 | 7351 | no_far_shell_horizon | split_persistent_dual | 137 | 469 | 402 | 34 | 227 |
| 1024 | p1 | 7307 | no_far_shell_horizon | birth_death_churn | 0 | 29 | 21 | 9 | 24 |
| 1024 | p1 | 7351 | established_far_shell_horizon | split_fragment | 47 | 187 | 144 | 34 | 143 |
| 1024 | p3 | 7307 | established_far_shell_horizon | split_persistent_dual | 153 | 503 | 441 | 51 | 233 |
| 1024 | p3 | 7351 | established_far_shell_horizon | split_persistent_dual | 95 | 276 | 223 | 45 | 207 |

## Aggregate

| target | placement | est | horizon | patterns | separates outcome | mean churn | mean max comps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 896 | p1 | 0.500 | 75.000 | split_persistent_dual:2 | 0 | 316.000 | 24.500 |
| 896 | p3 | 0.000 | 0.000 | split_persistent_dual:2 | 0 | 794.000 | 29.000 |
| 1024 | p1 | 0.500 | 86.000 | birth_death_churn:1;split_fragment:1 | 1 | 243.500 | 21.500 |
| 1024 | p3 | 1.000 | 172.000 | split_persistent_dual:2 | 0 | 983.500 | 48.000 |

## Chain summary

| pattern | n | est rate | targets | placements | mean horizon | mean churn |
| --- | --- | --- | --- | --- | --- | --- |
| birth_death_churn | 1 | 0.000 | 1024 | p1 | 0.000 | 51.000 |
| split_fragment | 1 | 1.000 | 1024 | p1 | 172.000 | 436.000 |
| split_persistent_dual | 6 | 0.500 | 1024;896 | p1;p3 | 82.333 | 697.833 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelser er rene og alle requested add_chord-perturbations matcher faktisk perturbasjon.
- `landscape_reproduction`: `p1_bridge_p3_switch_reproduced` fordi p1_bridge=1, p3_switch=1 under genealogy rerun.
- `genealogy_axis`: `genealogy_separates_limited_seed_splits` fordi 1 target/placement-grupper (1024:p1) har disjunkte genealogy patterns for horizon vs no-horizon.
- `next_step`: `holdout_p1_1024_genealogy_split_axis` fordi Neste steg bor holde ut den konkrete p1/1024 genealogy-splitten paa nye seeds foer generalisering.

## Tolkning

- Genealogy patterns er mekanismeobservabler, ikke partikkelklasser.
- En positiv separation betyr bare at komponenthistorikk forklarer seed-splits bedre enn statisk supportgeometri.
- En negativ separation betyr at p1/p3-landskapet fortsatt er ekte, men mekanismen krever annen observabel eller mer n.
