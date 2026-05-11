# Operativ anbefaling v0.15cp

- `artifact_control`: `clean` fordi Startstorrelse er ren og alle requested perturbations matcher faktisk perturbasjon.
- `budget_scope`: `scaled_from_target768` fordi Target 1024 bruker step_budget=3414, skalert fra 2560 ved target 768.
- `budget_effect`: `p0_budget_response_without_p2` fordi Samlet horizon-span delta er p0=52.500 og p2=0.000 mot v15cn same-absolute-budget.
- `target1024_scaled_budget_p2`: `scaled_budget_p2_not_supported` fordi Budget scaling from target 768 to 1024 did not revive p2 under the existing support criteria.
- `next_step`: `intermediate_scale_or_retire_p2_as_scale_selector` fordi Neste steg bor enten teste ett mellomtarget eller nedgradere p2 som skala-selector.

- Ikke les dette som global invariant-, Lorentz- eller entanglement-evidens. Dette er en skalert budsjett-test av en p2 far-shell-observabel.
