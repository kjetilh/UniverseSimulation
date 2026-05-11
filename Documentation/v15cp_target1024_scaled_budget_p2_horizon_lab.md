# Relasjonell universgraf v0.15cp: target-1024 scaled-budget p2 horizon

## Formal

Denne runden tester den minste budsjettforklaringen etter `v15cn` og `v15co`.
Den holder target `1024`, p0/p2, carriers, growth seed og seed-deltaer fast, men skalerer step budget fra target `768`.

## Budget

| reference target | target | reference steps | scaled steps | scale factor |
| --- | --- | --- | --- | --- |
| 768 | 1024 | 2560 | 3414 | 1.333 |

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 1024 | 1024.0 | 1024.0 | 1024.0 | 1 |

## Profile summary

| profile | established | none | horizon | retention | last12 high | total high | far share | distance | spectral rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | 0.500 | 0.500 | 86.000 | 0.369 | 0.500 | 63.500 | 0.649 | 5.774 | 0.018 |
| add_chord_p2 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.580 | 4.057 | 0.003 |
| local_swap_p0 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.567 | 4.979 | 0.022 |
| local_swap_p2 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.129 | 0.965 | 0.000 |

## P2 versus P0

| compare | est gap | control none gap | retention gap | last12 gap | horizon gap | distance gap | support score | supported |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p2_minus_p0 | -0.500 | -0.500 | -0.369 | -0.500 | -86.000 | -1.717 | 0 | 0 |
| local_swap_p2_minus_p0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | -4.014 | 0 | 0 |

## Budget comparison versus v15cn

| profile | absolute established | scaled established | delta | absolute horizon | scaled horizon | horizon delta |
| --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | 0.500 | 0.500 | 0.000 | 33.500 | 86.000 | 52.500 |
| add_chord_p2 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| local_swap_p0 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| local_swap_p2 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelse er ren og alle requested perturbations matcher faktisk perturbasjon.
- `budget_scope`: `scaled_from_target768` fordi Target 1024 bruker step_budget=3414, skalert fra 2560 ved target 768.
- `budget_effect`: `p0_budget_response_without_p2` fordi Samlet horizon-span delta er p0=52.500 og p2=0.000 mot v15cn same-absolute-budget.
- `target1024_scaled_budget_p2`: `scaled_budget_p2_not_supported` fordi Budget scaling from target 768 to 1024 did not revive p2 under the existing support criteria.
- `next_step`: `intermediate_scale_or_retire_p2_as_scale_selector` fordi Neste steg bor enten teste ett mellomtarget eller nedgradere p2 som skala-selector.

## Tolkning

- Dette er en smal budsjett-normaliseringstest, ikke et nytt bredt target-search.
- Positivt signal betyr bare at target-1024-p2 var budsjettfoelsomt under v15cn, ikke at p2 er universell.
- Negativt signal betyr at p2 som scale-selector svekkes, men ett mellomtarget kan fortsatt skille gradvis overgang fra skarp target-lomme.
