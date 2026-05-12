# Operativ anbefaling v0.15cq

- `artifact_control`: `clean` fordi Startstorrelse er ren og alle requested perturbations matcher faktisk perturbasjon.
- `budget_scope`: `intermediate_scaled_from_target768` fordi Target 896 bruker step_budget=2987, skalert fra 2560 ved target 768.
- `intermediate_scale_p2`: `intermediate_p2_partial_not_supported` fordi Target 896 has some p2 movement but does not pass support criteria.
- `next_step`: `replicate_or_retire_cautiously` fordi Neste steg bor enten replikere midpoint med litt mer seed-budget eller nedgradere p2 forsiktig.

- Ikke les dette som global invariant-, Lorentz- eller entanglement-evidens. Dette er en midpoint-test av p2 som skala-selector.
