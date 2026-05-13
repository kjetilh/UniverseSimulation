# Relasjonell universgraf v0.15cs: add_chord p0 scale-response holdout

## Formal

Denne runden tester om `add_chord_p0`-responsen fra v15cq/v15cp holder paa friske seed-deltaer.
Dette er en kontroll-avledet scale-response holdout, ikke en partikkel-, invariant- eller Lorentz-test.

## Design

| field | value |
| --- | --- |
| targets | 896;1024 |
| primary | add_chord_p0 |
| controls | add_chord_p2;local_swap_p0 |
| fresh seed deltas | 6203;6269 |
| reference steps | 2560 at target 768 |

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 896 | 896.0 | 896.0 | 896.0 | 1 |
| 1024 | 1024.0 | 1024.0 | 1024.0 | 1 |

## Profile summary

| target | profile | role | established | none | horizon | retention | last12 high | far share | distance | spectral rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 896 | add_chord_p0 | primary | 1.000 | 0.000 | 136.000 | 0.959 | 1.000 | 0.897 | 6.683 | 0.018 |
| 896 | add_chord_p2 | control | 0.500 | 0.500 | 45.500 | 0.445 | 0.500 | 0.845 | 5.873 | 0.016 |
| 896 | local_swap_p0 | control | 0.500 | 0.000 | 86.500 | 0.630 | 0.500 | 0.886 | 6.293 | 0.002 |
| 1024 | add_chord_p0 | primary | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.464 | 5.109 | 0.001 |
| 1024 | add_chord_p2 | control | 0.500 | 0.500 | 82.500 | 0.494 | 0.500 | 0.606 | 3.989 | 0.029 |
| 1024 | local_swap_p0 | control | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.621 | 5.842 | 0.028 |

## P0 versus controls

| target | compare | est gap | horizon gap | retention gap | last12 gap | distance gap | control weaker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 896 | add_chord_p0_minus_add_chord_p2 | 0.500 | 90.500 | 0.514 | 0.500 | 0.809 | 1 |
| 896 | add_chord_p0_minus_local_swap_p0 | 0.500 | 49.500 | 0.329 | 0.500 | 0.390 | 1 |
| 1024 | add_chord_p0_minus_add_chord_p2 | -0.500 | -82.500 | -0.494 | -0.500 | 1.120 | 0 |
| 1024 | add_chord_p0_minus_local_swap_p0 | 0.000 | 0.000 | 0.000 | 0.000 | -0.733 | 0 |

## Scale response summary

| target | p0 est | p0 horizon | max control est | max control horizon | horizon gap | score | supported |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 896 | 1.000 | 136.000 | 0.500 | 86.500 | 49.500 | 6 | 1 |
| 1024 | 0.000 | 0.000 | 0.500 | 82.500 | -82.500 | 0 | 0 |

## Historical comparison

| target | old p0 est | fresh p0 est | old horizon | fresh horizon | horizon delta | fresh supported |
| --- | --- | --- | --- | --- | --- | --- |
| 896 | 0.500 | 1.000 | 75.000 | 136.000 | 61.000 | 1 |
| 1024 | 0.500 | 0.000 | 86.000 | 0.000 | -86.000 | 0 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelser er rene og alle requested perturbations matcher faktisk perturbasjon.
- `fresh_seed_scope`: `fresh_seed_deltas` fordi Seed-deltaene (6203, 6269) er ikke brukt i v15cn/v15cp/v15cq p2-scale-ladderen.
- `add_chord_p0_scale_response`: `p0_scale_response_target_specific` fordi Fresh seed deltas support add_chord_p0 at target(s) 896, but not all targets.
- `next_step`: `replicate_or_bracket_p0_response` fordi Neste steg bor replikere eller bracketter p0-responsen foer ny kandidatstatus.

## Tolkning

- Positivt p0-resultat betyr bare at en scale-response-observabel fortjener ny analyse; det er ikke en lov.
- Negativt p0-resultat betyr at kontroll-inversjonen i v15cq/v15cp trolig var small-n eller seed-avhengig.
- Uansett skal Lorentz-, global invariant- og entanglement-sprak holdes nede.
