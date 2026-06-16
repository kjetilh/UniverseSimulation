# Relasjonell universgraf v0.15di: growth-seed signature synthesis

## Formal

Dette er en no-new-dynamics syntese av v15dg og v15dh.
Den sammenligner placement-respons, support-signaturer og metric-retning mellom growth seed 202 og 303.
Ingen metric er refittet, og ingen nye dynamiske runs er laget.

## Placement summary

| seed | p | labels | established | support | bm | static degree | genealogy | horizon |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 202 | p0 | no_far_shell_horizon:8 | 0.000 | `13,72,343` | 11.125 | 9.333 | 0.740 | 0.000 |
| 202 | p1 | established_far_shell_horizon:7;no_far_shell_horizon:1 | 0.875 | `1,58,537` | 13.500 | 10.000 | 0.874 | 172.000 |
| 202 | p2 | mixed_far_shell_horizon:2;no_far_shell_horizon:6 | 0.000 | `6,8,9` | 8.500 | 8.667 | 0.310 | 0.000 |
| 303 | p0 | established_far_shell_horizon:4;no_far_shell_horizon:4 | 0.500 | `3,4,827` | 7.000 | 6.667 | 0.378 | 86.000 |
| 303 | p1 | no_far_shell_horizon:8 | 0.000 | `12,13,22` | 6.500 | 9.333 | 0.506 | 0.000 |
| 303 | p2 | established_far_shell_horizon:4;mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.500 | `25,177,430` | 4.990 | 6.000 | 0.515 | 97.000 |

## Growth-seed deltas

| p | shift | support 202 | support 303 | est 202 | est 303 | bm delta | static degree delta | genealogy delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p0 | gained_positive_anchor | `13,72,343` | `3,4,827` | 0.000 | 0.500 | -4.125 | -2.667 | -0.362 |
| p1 | lost_positive_anchor | `1,58,537` | `12,13,22` | 0.875 | 0.000 | -7.000 | -0.667 | -0.369 |
| p2 | gained_positive_anchor | `6,8,9` | `25,177,430` | 0.000 | 0.500 | -3.510 | -2.667 | 0.204 |

## Metric audit

| scope | metric | role | AUC | median established | median no-horizon | status |
| --- | --- | --- | --- | --- | --- | --- |
| all | w32_mean_boundary_per_mass | primary_frozen_dynamic | 0.563 | 8.033 | 7.000 | weak_or_mixed_direction |
| all | static_mean_support_degree | static_support_audit | 0.517 | 6.667 | 9.333 | weak_or_mixed_direction |
| all | genealogy_intensity_index | baseline_descriptive | 0.769 | 0.686 | 0.412 | weak_or_mixed_direction |
| growth_seed_202 | w32_mean_boundary_per_mass | primary_frozen_dynamic | 0.857 | 13.500 | 8.500 | strong_positive_direction |
| growth_seed_202 | static_mean_support_degree | static_support_audit | 0.967 | 10.000 | 9.333 | strong_positive_direction |
| growth_seed_202 | genealogy_intensity_index | baseline_descriptive | 0.800 | 0.879 | 0.630 | strong_positive_direction |
| growth_seed_303 | w32_mean_boundary_per_mass | primary_frozen_dynamic | 0.463 | 5.483 | 6.500 | weak_or_mixed_direction |
| growth_seed_303 | static_mean_support_degree | static_support_audit | 0.217 | 6.333 | 9.333 | inverted_or_failed_direction |
| growth_seed_303 | genealogy_intensity_index | baseline_descriptive | 0.858 | 0.632 | 0.362 | strong_positive_direction |

## Operativ lesning

- `artifact_control`: `clean` fordi Requested perturbations matcher og target-storrelsesseparasjon er clean.
- `placement_transfer`: `placement_landscape_not_growth_seed_stable` fordi p1 established-rate endres 0.875->0.000; p0 endres 0.000->0.500; p2 endres 0.000->0.500.
- `support_signature`: `support_signatures_change_by_growth_seed` fordi p1-support endres `1,58,537` -> `12,13,22`; p0 `13,72,343` -> `3,4,827`; p2 `6,8,9` -> `25,177,430`.
- `boundary_mass_transfer`: `boundary_mass_seed_conditioned_not_general` fordi AUC for `w32_mean_boundary_per_mass` er 0.857 paa seed 202 men 0.463 paa seed 303.
- `static_support_audit`: `static_support_direction_not_general` fordi `static_mean_support_degree` AUC endres fra 0.967 til 0.217; supportgeometri er viktig, men retningen er ikke universell.
- `genealogy_audit`: `genealogy_intensity_descriptive_not_selector` fordi `genealogy_intensity_index` er 0.858 paa seed 303, men dette var ikke primary metric og maa ikke refittes til claim.
- `next_step`: `condition_on_base_support_before_more_dynamics` fordi Ikke bruk mer blind label-budget paa fast p1-anchor. Bygg forst en support-/base-kondisjonert selector eller billig pre-run audit som predikerer hvilke placements som er plausible paa gitt basegraf.

## Tolkning

- v15dg sin positive boundary/mass-lesning var reell i seed-202-landskapet, men ikke growth-seed-general.
- v15dh viser at p1 ikke er et universelt anker; p0/p2 kan bli de aktive plasseringene paa en annen base.
- Neste arbeid bor kondisjonere paa base/support-signaturer foer mer dynamikk brukes.
- Dette er fortsatt defect/response-instrumentering, ikke invariant-, Lorentz-, partikkel- eller entanglement-evidens.
