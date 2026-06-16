# Operativ anbefaling v0.15di

- `artifact_control`: `clean` fordi Requested perturbations matcher og target-storrelsesseparasjon er clean.
- `placement_transfer`: `placement_landscape_not_growth_seed_stable` fordi p1 established-rate endres 0.875->0.000; p0 endres 0.000->0.500; p2 endres 0.000->0.500.
- `support_signature`: `support_signatures_change_by_growth_seed` fordi p1-support endres `1,58,537` -> `12,13,22`; p0 `13,72,343` -> `3,4,827`; p2 `6,8,9` -> `25,177,430`.
- `boundary_mass_transfer`: `boundary_mass_seed_conditioned_not_general` fordi AUC for `w32_mean_boundary_per_mass` er 0.857 paa seed 202 men 0.463 paa seed 303.
- `static_support_audit`: `static_support_direction_not_general` fordi `static_mean_support_degree` AUC endres fra 0.967 til 0.217; supportgeometri er viktig, men retningen er ikke universell.
- `genealogy_audit`: `genealogy_intensity_descriptive_not_selector` fordi `genealogy_intensity_index` er 0.858 paa seed 303, men dette var ikke primary metric og maa ikke refittes til claim.
- `next_step`: `condition_on_base_support_before_more_dynamics` fordi Ikke bruk mer blind label-budget paa fast p1-anchor. Bygg forst en support-/base-kondisjonert selector eller billig pre-run audit som predikerer hvilke placements som er plausible paa gitt basegraf.

- Ikke bruk `p1/1024` som generell anchor uten base/support-kondisjonering.
- Ikke refit boundary/mass eller genealogy-intensity til et positivt claim.
- Neste steg bor vaere en billig pre-run support/base-audit eller selector, ikke mer blind label-budget.
