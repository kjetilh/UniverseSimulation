# Relasjonell universgraf v0.15cq: intermediate-scale p2 horizon

## Formal

Denne runden tester ett mellomtarget mellom `768` og `1024` etter at skalert target-1024-budsjett ikke gjenopplivet p2.
Maalet er aa avgjoere om p2 fortsatt kan brukes som skala-selector, eller boer nedgraderes til target-768 lokal lomme/kontrast.

## Budget

| reference target | target | reference steps | scaled steps | scale factor |
| --- | --- | --- | --- | --- |
| 768 | 896 | 2560 | 2987 | 1.167 |

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 896 | 896.0 | 896.0 | 896.0 | 1 |

## Profile summary

| profile | established | none | horizon | retention | last12 high | total high | far share | distance | spectral rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | 0.500 | 0.500 | 75.000 | 0.500 | 0.500 | 75.000 | 0.440 | 3.351 | 0.001 |
| add_chord_p2 | 0.500 | 0.500 | 49.500 | 0.414 | 0.500 | 41.000 | 0.866 | 5.805 | 0.015 |
| local_swap_p0 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.004 | 1.072 | 0.000 |
| local_swap_p2 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.650 | 5.102 | 0.007 |

## P2 versus P0

| compare | est gap | control none gap | retention gap | last12 gap | horizon gap | distance gap | support score | supported |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p2_minus_p0 | 0.000 | 0.000 | -0.086 | 0.000 | -25.500 | 2.453 | 1 | 0 |
| local_swap_p2_minus_p0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 4.029 | 1 | 0 |

## Scale ladder

| target | budget | carrier | p2 est | p2 horizon | p2 score | p2 supported |
| --- | --- | --- | --- | --- | --- | --- |
| 768 | v15cn_same_absolute_2560 | add_chord | 0.500 | 64.500 | 3 | 0 |
| 768 | v15cn_same_absolute_2560 | local_swap | 0.500 | 64.500 | 5 | 1 |
| 896 | v15cq_scaled_from_768 | add_chord | 0.500 | 49.500 | 1 | 0 |
| 896 | v15cq_scaled_from_768 | local_swap | 0.000 | 0.000 | 1 | 0 |
| 1024 | v15cp_scaled_from_768 | add_chord | 0.000 | 0.000 | 0 | 0 |
| 1024 | v15cp_scaled_from_768 | local_swap | 0.000 | 0.000 | 0 | 0 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og alle requested perturbations matcher faktisk perturbasjon.
- `budget_scope`: `intermediate_scaled_from_target768` fordi Target 896 bruker step_budget=2987, skalert fra 2560 ved target 768.
- `intermediate_scale_p2`: `intermediate_p2_partial_not_supported` fordi Target 896 has some p2 movement but does not pass support criteria.
- `next_step`: `replicate_or_retire_cautiously` fordi Neste steg bor enten replikere midpoint med litt mer seed-budget eller nedgradere p2 forsiktig.

## Tolkning

- Dette er en midpoint-test, ikke et bredt skala-sok.
- Hvis 896 stoetter p2, er p2 ikke bare target-768-lokal og fallet maa brackettes.
- Hvis 896 ikke stoetter p2, boer p2 nedgraderes som skala-selector og beholdes bare som lokal lomme/kontrast.
