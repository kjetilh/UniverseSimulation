# Operativ anbefaling v0.15ds

- `artifact_control`: `clean` fordi Startstorrelse er ren og requested add_chord-perturbations matcher faktisk perturbasjon.
- `atlas_design`: `class_frequency_atlas_no_selector` fordi Denne runden skriver pre-run morphology, men bruker ikke pre-run features som prediksjon eller refit.
- `outcome_balance`: `fresh_growth_seed_taxonomy_recorded` fordi Run labels: established_far_shell_horizon:21;mixed_far_shell_horizon:3;no_far_shell_horizon:48. Seed classes: multi_active_p0_p2:2;no_active:1;single_active_p1:1;single_active_p2:2.
- `class_landscape_result`: `class_frequency_atlas_stabilizing` fordi new_class_count=0; new_seed_fraction=0.000; repeated_within_v15ds=multi_active_p0_p2;single_active_p2.
- `dynamic_boundary_mass_audit`: `reported_descriptive_not_primary_selector` fordi `w32_mean_boundary_per_mass` AUC established-vs-no=0.483.
- `next_step`: `stratify_next_selector_by_repeated_classes` fordi Atlaset viser repeterte klasser med begrenset novelty; neste selector bor vaere OOD-first og klasse-stratifisert.

- Ikke refit v15dr-mapperen etter dette atlaset.
- Bruk klassefrekvenser og novelty som beslutningsgrunnlag foer ny selector.
- Hvis taxonomy fortsatt ekspanderer, prioriter OOD/atlas fremfor selector-claim.
- Ikke oppgrader til invariant/Lorentz/partikkel/entanglement-claim.
