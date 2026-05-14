# Relasjonell universgraf v0.15cv: add_chord winning-placement mechanism probe

## Formal

Denne runden rerunner bare v15cu sine p1/p3-cases med rikere mekanismeobservabler.
Maalet er aa se om target-switchen kan knyttes til supportgeometri og tidlig launch, ikke aa score flere labels.

## Design

| field | value |
| --- | --- |
| targets | 896;1024 |
| placements | p1;p3 |
| seed deltas | 7307;7351 |
| early step limit | 640 |

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 896 | 896.0 | 896.0 | 896.0 | 1 |
| 1024 | 1024.0 | 1024.0 | 1024.0 | 1 |

## Aggregate mechanism

| target | placement | class | est | horizon | early high | first high | early outer | early distance | support ball3 | ball3/ball1 | trigger labels |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 896 | p1 | strong_persistent_far_shell | 0.500 | 75.000 | 0.000 | 1632.0 | 0.027 | 0.674 | 120.0 | 4.138 | inner_gate_load_without_outer_horizon;quiet_or_delayed_launch |
| 896 | p3 | no_horizon | 0.000 | 0.000 | 0.000 | nan | 0.071 | 0.991 | 240.0 | 6.154 | inner_gate_load_without_outer_horizon;quiet_or_delayed_launch |
| 1024 | p1 | strong_persistent_far_shell | 0.500 | 86.000 | 0.000 | 1360.0 | 0.000 | 0.100 | 100.0 | 3.704 | quiet_or_delayed_launch |
| 1024 | p3 | strong_persistent_far_shell | 1.000 | 172.000 | 0.000 | 1076.0 | 0.079 | 1.136 | 111.0 | 3.364 | early_outer_mass_without_high;quiet_or_delayed_launch |

## Contrasts

| compare | horizon gap | early high gap | first high gap | early outer gap | distance gap | ball3 gap | ball3/ball1 gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| target896_p3_minus_p1 | -75.000 | 0.000 | nan | 0.044 | 0.317 | 120.0 | 2.016 |
| target1024_p3_minus_p1 | 86.000 | 0.000 | -284.0 | 0.079 | 1.036 | 11.0 | -0.340 |
| p1_1024_minus_896 | 11.000 | 0.000 | -272.0 | -0.027 | -0.574 | -20.0 | -0.434 |
| p3_1024_minus_896 | 172.000 | 0.000 | nan | 0.008 | 0.145 | -129.0 | -2.790 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelser er rene og alle requested add_chord-perturbations matcher faktisk perturbasjon.
- `p1_bridge`: `p1_stable_persistent_bridge` fordi p1 er persistent ved baade 896 og 1024 under samme fresh-seed scope.
- `p3_switch`: `p3_target_switch_confirmed` fordi p3 er ikke persistent ved 896, men er persistent ved 1024.
- `early_launch_axis`: `early_launch_not_sufficient` fordi Tidlig launch forklarer ikke p3-switchen rent (score 0/6).
- `support_geometry_axis`: `support_geometry_not_sufficient` fordi Static support geometry forklarer ikke p3-switchen rent (score 0/5).
- `p1_target_shift`: `p1_launch_relatively_stable` fordi p1 1024-minus-896 early-launch shift score er 0/3.
- `next_step`: `add_genealogy_to_p1_p3_seed_splits` fordi P1/p3-landskapet holder, men mekanismen er ikke forklart; neste steg bor legge til per-run genealogi.

## Tolkning

- P1/p3 er fortsatt heuristiske placement-profiler, ikke partikler.
- En mekanismeakse her betyr bare at support/launch-observabler kan forklare noe av placement-landskapet.
- Hvis mekanismen holder, neste steg er holdout. Hvis ikke, maa vi til genealogi/per-run seed-splits.
