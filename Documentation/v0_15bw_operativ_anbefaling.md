# v0.15bw operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `family_holdout`: `family_structure_not_replicated` fordi Family-map replikerer ikke rent i holdout (0.375).
- `geometry_core_members`: `observed` fordi add_chord_p1;add_chord_p2;local_swap_p1;local_swap_p2;local_swap_p3
- `symmetry_holdout`: `full_near_symmetry_candidate` fordi 2 profilpar er full feature-level near-symmetry-kandidater i holdouten.
- `next_step`: `new_scale_jump` fordi Neste steg bor vaere nytt skalahopp heller enn mer family-threshold-tuning ved target 96.

- Bruk denne runden som holdout av v15bv family-map. Hvis den peker mot skalahopp, ikke press flere target-96 terskler.
