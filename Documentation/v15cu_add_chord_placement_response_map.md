# Relasjonell universgraf v0.15cu: add_chord placement response map

## Formal

Denne runden tester om add_chord-responsen fra v15ct er et lite placement-landskap.
Den kjorer ny dynamikk, men bare for `add_chord`, target `896/1024`, placements `0..3` og friske seed-deltaer.
Dette er ikke en Lorentz-, global invariant-, entanglement- eller partikkeltest.

## Design

| field | value |
| --- | --- |
| targets | 896;1024 |
| perturbation | add_chord |
| placements | p0;p1;p2;p3 |
| fresh seed deltas | 7307;7351 |
| reference steps | 2560 at target 768 |

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 896 | 896.0 | 896.0 | 896.0 | 1 |
| 1024 | 1024.0 | 1024.0 | 1024.0 | 1 |

## Placement aggregate

| target | placement | class | score | established | none | horizon | retention | last12 | far share | distance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 896 | p0 | no_horizon | 0 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| 896 | p1 | strong_persistent_far_shell | 6 | 0.500 | 0.500 | 75.000 | 0.500 | 0.500 | 0.595 | 4.804 |
| 896 | p2 | moderate_persistent_far_shell | 6 | 0.500 | 0.500 | 57.500 | 0.500 | 0.500 | 0.770 | 5.587 |
| 896 | p3 | no_horizon | 0 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.290 | 3.056 |
| 1024 | p0 | no_horizon | 1 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.473 | 4.031 |
| 1024 | p1 | strong_persistent_far_shell | 6 | 0.500 | 0.500 | 86.000 | 0.500 | 0.500 | 0.569 | 5.772 |
| 1024 | p2 | no_horizon | 0 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.402 | 2.603 |
| 1024 | p3 | strong_persistent_far_shell | 6 | 1.000 | 0.000 | 172.000 | 1.000 | 1.000 | 0.792 | 7.308 |

## Placement ranks

| target | rank | placement | class | score | horizon | horizon gap to best |
| --- | --- | --- | --- | --- | --- | --- |
| 896 | 1 | p1 | strong_persistent_far_shell | 6 | 75.000 | 0.000 |
| 896 | 2 | p2 | moderate_persistent_far_shell | 6 | 57.500 | -17.500 |
| 896 | 3 | p3 | no_horizon | 0 | 0.000 | -75.000 |
| 896 | 4 | p0 | no_horizon | 0 | 0.000 | -75.000 |
| 1024 | 1 | p3 | strong_persistent_far_shell | 6 | 172.000 | 0.000 |
| 1024 | 2 | p1 | strong_persistent_far_shell | 6 | 86.000 | -86.000 |
| 1024 | 3 | p0 | no_horizon | 1 | 0.000 | -172.000 |
| 1024 | 4 | p2 | no_horizon | 0 | 0.000 | -172.000 |

## Target patterns

| target | best | class | score | horizon | persistent placements | landscape |
| --- | --- | --- | --- | --- | --- | --- |
| 896 | add_chord_p1 | strong_persistent_far_shell | 6 | 75.000 | 1;2 | multi_placement_response |
| 1024 | add_chord_p3 | strong_persistent_far_shell | 6 | 172.000 | 1;3 | single_placement_dominant_with_persistent_neighbors |

## Cross-target placement stability

| placement | 896 class | 1024 class | changed | horizon delta 1024-896 |
| --- | --- | --- | --- | --- |
| p0 | no_horizon | no_horizon | 0 | 0.000 |
| p1 | strong_persistent_far_shell | strong_persistent_far_shell | 0 | 11.000 |
| p2 | moderate_persistent_far_shell | no_horizon | 1 | -57.500 |
| p3 | no_horizon | strong_persistent_far_shell | 1 | 172.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelser er rene og alle requested add_chord-perturbations matcher faktisk perturbasjon.
- `seed_scope`: `fresh_seed_deltas_v15cu` fordi Seed-deltaene (7307, 7351) er ikke brukt i v15cn/v15cp/v15cq/v15cs.
- `add_chord_carrier`: `add_chord_carrier_live` fordi 4 target/placement-aggregater har persistent far-shell response.
- `placement_landscape`: `target_specific_placement_switch` fordi Beste placement skifter mellom target 896 og 1024, og minst en placement har persistent far-shell response.
- `target_stability`: `placement_classes_shift_across_targets` fordi 2/4 placements skifter response-class mellom target 896 og 1024.
- `next_step`: `mechanism_probe_for_winning_placements` fordi Neste steg bor sammenligne supportgeometri og tidlig launch for vinnerplasseringene, ikke oeke label-budget.

## Tolkning

- Hvis beste placement skifter mellom target, er p0/p2 best lest som lokale lommer, ikke som skala-labeler.
- Hvis samme placement vinner begge target, fortjener den en fresh holdout som placement-kandidat.
- Hvis flere placements er persistent, trenger vi en observabel som forklarer responslandskapet heller enn mer placement-budget.
