# Operativ anbefaling v0.15cv

- `artifact_control`: `clean` fordi Startstorrelser er rene og alle requested add_chord-perturbations matcher faktisk perturbasjon.
- `p1_bridge`: `p1_stable_persistent_bridge` fordi p1 er persistent ved baade 896 og 1024 under samme fresh-seed scope.
- `p3_switch`: `p3_target_switch_confirmed` fordi p3 er ikke persistent ved 896, men er persistent ved 1024.
- `early_launch_axis`: `early_launch_not_sufficient` fordi Tidlig launch forklarer ikke p3-switchen rent (score 0/6).
- `support_geometry_axis`: `support_geometry_not_sufficient` fordi Static support geometry forklarer ikke p3-switchen rent (score 0/5).
- `p1_target_shift`: `p1_launch_relatively_stable` fordi p1 1024-minus-896 early-launch shift score er 0/3.
- `next_step`: `add_genealogy_to_p1_p3_seed_splits` fordi P1/p3-landskapet holder, men mekanismen er ikke forklart; neste steg bor legge til per-run genealogi.

- Dette er en mekanismeprobe for add_chord-placement-landskapet, ikke en global invariant- eller Lorentz-test.
