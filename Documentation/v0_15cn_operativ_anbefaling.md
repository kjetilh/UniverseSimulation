# Operativ anbefaling v0.15cn

- `artifact_control`: `clean` fordi Startstorrelser er separerte og alle requested perturbations matcher faktisk perturbasjon.
- `p2_horizon_scale_holdout`: `target768_specific_under_current_budget` fordi Fresh target-768 anchor reproduces at least partly, but target-1024 does not support p2 under the same absolute step budget. Dette kan bety target-768-spesifisitet eller at 1024 trenger lengre dynamisk budsjett.
- `budget_scope`: `same_absolute_budget` fordi Alle targets bruker step_budget=2560; fravaer ved 1024 er derfor ikke alene bevis for skala-fravaer.
- `next_step`: `target1024_budget_extension_or_intermediate_scale` fordi Neste steg bor teste om 1024 trenger lengre budsjett, eller om et mellomtarget bryter overgangen.

- Ikke les dette som global invariant-evidens. Dette er en smal holdout av en p2 far-shell-observabel.
