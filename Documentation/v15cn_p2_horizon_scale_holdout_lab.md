# Relasjonell universgraf v0.15cn: p2 horizon scale holdout

## Formal

Denne runden tester om p2 far-shell-horisonten er target-768-spesifikk eller overlever ett moderat skalahopp til target `1024`.
Den inkluderer en fresh target-768 anchor og holder oppsettet smalt: `p0` mot `p2`, `add_chord` og `local_swap`, samme absolute step budget.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 768 | 768.0 | 768.0 | 768.0 | 1 |
| 1024 | 1024.0 | 1024.0 | 1024.0 | 1 |

## Profile summary

| target | profile | established | none | horizon | retention | last12 high | total high | far share | distance | spectral rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 768 | add_chord_p0 | 0.000 | 0.500 | 2.000 | 0.500 | 0.000 | 2.000 | 0.738 | 4.961 | 0.001 |
| 768 | add_chord_p2 | 0.500 | 0.500 | 64.500 | 0.500 | 0.500 | 64.500 | 0.468 | 4.503 | 0.023 |
| 768 | local_swap_p0 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.500 | 0.711 | 5.227 | 0.003 |
| 768 | local_swap_p2 | 0.500 | 0.500 | 64.500 | 0.465 | 0.500 | 60.000 | 0.374 | 3.890 | 0.002 |
| 1024 | add_chord_p0 | 0.500 | 0.500 | 33.500 | 0.321 | 0.500 | 22.500 | 0.623 | 5.601 | 0.008 |
| 1024 | add_chord_p2 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.495 | 3.181 | 0.002 |
| 1024 | local_swap_p0 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.566 | 4.849 | 0.005 |
| 1024 | local_swap_p2 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.069 | 0.588 | 0.000 |

## P2 versus P0

| target | compare | est gap | control none gap | retention gap | last12 gap | horizon gap | distance gap | support score | supported |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 768 | add_chord_p2_minus_p0 | 0.500 | 0.000 | 0.000 | 0.500 | 62.500 | -0.459 | 3 | 0 |
| 768 | local_swap_p2_minus_p0 | 0.500 | 0.500 | 0.465 | 0.500 | 64.500 | -1.337 | 5 | 1 |
| 1024 | add_chord_p2_minus_p0 | -0.500 | -0.500 | -0.321 | -0.500 | -33.500 | -2.420 | 0 | 0 |
| 1024 | local_swap_p2_minus_p0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | -4.260 | 0 | 0 |

## Scale summary

| target | supported carriers | shared | add p2 est | swap p2 est | add score | swap score | p0 none |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 768 | local_swap | 0 | 0.500 | 0.500 | 3 | 5 | 0.750 |
| 1024 | none | 0 | 0.000 | 0.000 | 0 | 0 | 0.750 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelser er separerte og alle requested perturbations matcher faktisk perturbasjon.
- `p2_horizon_scale_holdout`: `target768_specific_under_current_budget` fordi Fresh target-768 anchor reproduces at least partly, but target-1024 does not support p2 under the same absolute step budget. Dette kan bety target-768-spesifisitet eller at 1024 trenger lengre dynamisk budsjett.
- `budget_scope`: `same_absolute_budget` fordi Alle targets bruker step_budget=2560; fravaer ved 1024 er derfor ikke alene bevis for skala-fravaer.
- `next_step`: `target1024_budget_extension_or_intermediate_scale` fordi Neste steg bor teste om 1024 trenger lengre budsjett, eller om et mellomtarget bryter overgangen.

## Tolkning

- Dette er en smal skala-holdout av p2-horisonten, ikke et bredt nytt target-search.
- Positivt signal betyr bare at samme observabel overlever ett skalahopp under samme absolute budsjett.
- Negativt signal ved target 1024 er ikke alene bevis mot skalaeffekt, fordi tidsbudsjettet ikke er skalanormalisert.
