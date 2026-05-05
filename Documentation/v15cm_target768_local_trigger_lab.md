# Relasjonell universgraf v0.15cm: target-768 local trigger lab

## Formal

Denne runden tester om p2-horisonten ved target 768 kan forklares av tidlig supportnaer launch-dynamikk.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 768 | 768.0 | 768.0 | 768.0 | 1 |

## Aggregate local trigger

| profile | horizon | fast launch | first outer | first shell3 | early slope | early damage | shell3 peak | support degree | ball3/ball1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | 0.000 | 0.750 | 162.7 | 213.3 | 0.0160 | 19.2 | 0.251 | 4.000 | 6.818 |
| add_chord_p2 | 0.250 | 0.250 | 674.7 | 245.3 | 0.0059 | 6.8 | 0.275 | 5.000 | 3.308 |
| local_swap_p0 | 0.000 | 1.000 | 232.0 | 220.0 | 0.0172 | 27.0 | 0.319 | 4.000 | 6.818 |
| local_swap_p2 | 0.750 | 0.750 | 466.0 | 422.0 | 0.0129 | 17.8 | 0.207 | 5.000 | 3.308 |

## P2 versus P0

| compare | horizon gap | fast launch gap | first outer gap | early slope gap | early damage gap | shell3 peak gap | support degree gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p2_minus_p0 | 0.250 | -0.500 | 512.0 | -0.0102 | -12.5 | 0.024 | 1.000 |
| local_swap_p2_minus_p0 | 0.750 | -0.250 | 234.0 | -0.0043 | -9.2 | -0.112 | 1.000 |

## Cross-carrier P2 contrast

| compare | horizon gap | fast launch gap | first outer gap | early slope gap | early damage gap | shell3 peak gap | support degree gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| local_swap_p2_minus_add_chord_p2 | 0.500 | 0.500 | -208.7 | 0.0070 | 11.0 | -0.068 | 0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `shared_p2_local_trigger`: `local_trigger_not_yet` fordi Tidlig supportnaer trigger skiller ikke p2 rent fra p0 (scores add=1/6, swap=1/6).
- `support_geometry_alignment`: `support_geometry_not_explanatory` fordi Static support geometry forklarer ikke p2-trigger rent (scores add=1/4, swap=1/4).
- `next_step`: `p2_horizon_scale_holdout` fordi Neste steg bor teste om p2-horisonten er target-768-spesifikk eller holder paa ny skala.

## Tolkning

- Dette er en lokal tidligfase-observabel, ikke en ny global invariant-test.
- Positivt signal betyr bare at p2-horisonten kan ha en supportnaer launch-forklaring.
- Negativt signal betyr at neste steg bor teste skala/holdout heller enn enda mer trigger-tuning.
