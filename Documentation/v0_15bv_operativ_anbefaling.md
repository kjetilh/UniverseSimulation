# v0.15bv operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `family_structure`: `family_structure_without_symmetry_supported` fordi 1 ikke-trivielle family-labels gjentas, men ingen profilpar er naere pa bade support og carrier.
- `symmetry_scope`: `feature_level_only` fordi Symmetri her betyr bare lav normalisert avstand i valgte support/carrier-features, ikke automorfier eller fysisk symmetri.
- `next_step`: `holdout_repeated_families` fordi Neste steg bor teste om de repeterte family-labelene holder under flere seeds for samme placements.

- Bruk family-/near-symmetry-kandidater bare som holdout-kandidater. Ikke les dem som partikler eller eksakte symmetrier.
