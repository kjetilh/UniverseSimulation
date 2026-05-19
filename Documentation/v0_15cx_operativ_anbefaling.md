# Operativ anbefaling v0.15cx

- `artifact_control`: `clean` fordi Startstorrelse er ren og alle requested add_chord-perturbations matcher faktisk perturbasjon.
- `holdout_scope`: `narrow_p1_1024_only` fordi Target 1024, placement p1, growth_seed 202, seeds (7411, 7477, 7541, 7603).
- `genealogy_holdout`: `p1_1024_specific_genealogy_axis_not_reproduced` fordi Ingen holdout-runs traff de to kalibrerte v15cw-patterns; patterns=split_persistent_dual:4. Dette svekker den konkrete birth_death_churn/split_fragment-mappingen, selv om genealogy-intensitet fortsatt kan vaere informativ.
- `next_step`: `build_continuous_genealogy_intensity_observable` fordi Neste steg bor score churn, split-timing, dual-duration og max-mass som kontinuerlige observabler mot horizon, ikke legge mer vekt paa grove event-chain labels.

- Dette er en smal holdout av `1024/p1`, ikke en bred placement-search.
- Ikke oppgrader resultatet til partikler, global invariant, Lorentz-likhet eller entanglement-sprak.
