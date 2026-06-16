# Operativ anbefaling v0.15dh

- `artifact_control`: `clean` fordi Startstorrelse er ren og requested add_chord-perturbations matcher faktisk perturbasjon.
- `pre_registration`: `frozen_w32_boundary_mass_no_refit` fordi Primarmetric er frosset til `w32_mean_boundary_per_mass` fra v15df/v15dg; growth seed er endret til 303, og route-entry brukes ikke som feature.
- `outcome_balance`: `holdout_label_balance_anchor_changed` fordi Labels: established_far_shell_horizon:8;mixed_far_shell_horizon:1;no_far_shell_horizon:15; p1-established=0, p1-no-horizon=8, p0-established=4, p2-established=4.
- `placement_landscape`: `growth_seed_303_placement_landscape_changed` fordi p1 har 8/8 no-horizon og 0 established, mens p0 har 4 established og p2 har 4 established.
- `primary_result`: `boundary_mass_not_growth_seed_transferable_under_original_anchor` fordi `w32_mean_boundary_per_mass` har AUC=0.463 established-vs-no, og den opprinnelige p1-positive kontrasten finnes ikke paa growth seed 303.
- `static_confound_audit`: `static_support_not_transferable_as_selector` fordi `static_mean_support_degree` har AUC=0.217 established-vs-no; supportgeometrien er fortsatt viktig, men retningen fra v15dg transferer ikke som selector.
- `baseline_check`: `genealogy_intensity_correlates_overall_not_primary` fordi Baseline genealogy-intensity har AUC=0.858 established-vs-no, men er ikke den pre-registrerte primary selector her og skal ikke refittes til claim.
- `next_step`: `compare_growth_seed_support_signatures_before_more_dynamics` fordi Neste steg bor vaere en no-new-dynamics syntese av v15dg/v15dh som sammenligner base/support-signaturer og placement-respons, foer mer label-budget brukes.

- Ikke refit `w32_mean_boundary_per_mass` etter denne holdouten.
- Ikke bruk statisk supportgeometri som dynamisk selector.
- Ikke oppgrader til invariant/Lorentz/partikkel/entanglement-claim.
