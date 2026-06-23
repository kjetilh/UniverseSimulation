# Relasjonell universgraf v0.15do: active-set type discriminator synthesis

## Formal

Dette er en no-new-dynamics syntese etter v15dn.
Den bruker v15dn sine placement-rader og lager seed-level pre-run kontraster for aa se om
det finnes et lite signal som skiller `p1`-only seeds fra `p0;p2` seeds.
Alle regler er post-hoc screens; ingen dynamikk er kjort her.

## Seed features

| growth_seed | actual_type | active_placements | local_ball3_beta1_p0 | local_ball3_beta1_p1 | local_ball3_beta1_p2 | local_ball3_beta1_p2_minus_p1 | placement_rates |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 202 | p1_only | p1 | 23.000 | 18.000 | 49.000 | 31.000 | p0:0.000;p1:0.875;p2:0.000 |
| 303 | p0_p2 | p0;p2 | 31.000 | 31.000 | 20.000 | -11.000 | p0:0.500;p1:0.000;p2:0.500 |
| 404 | p1_only | p1 | 36.000 | 36.000 | 36.000 | 0.000 | p0:0.000;p1:0.500;p2:0.000 |
| 505 | p0_p2 | p0;p2 | 16.000 | 28.000 | 12.000 | -16.000 | p0:0.750;p1:0.250;p2:0.750 |

## Best comparison rules

| metric | comparison | true_type | false_type | type_accuracy | exact_set_match_rate | coverage_fraction | precision_fraction | burden_fraction | rule_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| delta_return_t2 | p0_ge_p1 | p0_p2 | p1_only | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| delta_return_t2 | p0_gt_p1 | p0_p2 | p1_only | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| delta_return_t2 | p0_le_p1 | p1_only | p0_p2 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| delta_return_t2 | p0_lt_p1 | p1_only | p0_p2 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| delta_return_t2 | p1_ge_p0 | p1_only | p0_p2 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| delta_return_t2 | p1_gt_p0 | p1_only | p0_p2 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| delta_return_t2 | p1_le_p0 | p0_p2 | p1_only | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| delta_return_t2 | p1_lt_p0 | p0_p2 | p1_only | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| delta_return_t6 | p1_ge_p2 | p1_only | p0_p2 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| delta_return_t6 | p1_gt_p2 | p1_only | p0_p2 | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| delta_return_t6 | p1_le_p2 | p0_p2 | p1_only | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| delta_return_t6 | p1_lt_p2 | p0_p2 | p1_only | 1.000 | 1.000 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |

## Best threshold rules

| metric | feature | operator | threshold | true_type | false_type | exact_set_match_rate | precision_fraction | burden_fraction | rule_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ball3_over_ball1 | ball3_over_ball1_p2_minus_p0 | le | -2.046 | p0_p2 | p1_only | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| ball3_over_ball1 | ball3_over_ball1_p2_minus_p0 | gt | -2.046 | p1_only | p0_p2 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| base_return_t2 | base_return_t2_p0_minus_p1 | le | -0.052 | p0_p2 | p1_only | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| base_return_t2 | base_return_t2_p0_minus_p1 | gt | -0.052 | p1_only | p0_p2 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| base_return_t2 | base_return_t2_p2_minus_p0 | le | 0.093 | p1_only | p0_p2 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| base_return_t2 | base_return_t2_p2_minus_p0 | gt | 0.093 | p0_p2 | p1_only | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| base_return_t2 | base_return_t2_p2_minus_p1 | le | 0.025 | p0_p2 | p1_only | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| base_return_t2 | base_return_t2_p2_minus_p1 | gt | 0.025 | p1_only | p0_p2 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| base_return_t4 | base_return_t4_p0_minus_p1 | le | -0.017 | p0_p2 | p1_only | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| base_return_t4 | base_return_t4_p0_minus_p1 | gt | -0.017 | p1_only | p0_p2 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| base_return_t6 | base_return_t6_p2_minus_p0 | le | 0.028 | p1_only | p0_p2 | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |
| base_return_t6 | base_return_t6_p2_minus_p0 | gt | 0.028 | p0_p2 | p1_only | 1.000 | 1.000 | 0.500 | posthoc_exact_compact_type_discriminator_not_validated |

## Operativ lesning

- `input_scope`: `no_new_dynamics_synthesis` fordi Reads v15dn placement rows and derives seed-level pre-run contrasts only.
- `type_scope`: `observed_two_type_landscape_only` fordi Only observed classes are p1_only and p0_p2 across four seeds; this is too small for validation.
- `multiplicity_guard`: `underdetermined` fordi Exact compact rules=110; exact metrics=ball3_over_ball1;base_return_t2;base_return_t4;base_return_t6;delta_ball3_efficiency;delta_return_t2;delta_return_t4;delta_return_t6;local_ball3_beta1;local_ball3_boundary_to_volume;new_edge_mean_forman;new_edge_min_forman;post_return_spectral_dim_proxy;post_return_t2;post_return_t4;post_return_t6;support_ball_2.
- `type_discriminator_screen`: `many_posthoc_exact_type_discriminators_found_underdetermined` fordi Found 110 exact compact rules across 17 metrics (ball3_over_ball1;base_return_t2;base_return_t4;base_return_t6;delta_ball3_efficiency;delta_return_t2;delta_return_t4;delta_return_t6;local_ball3_beta1;local_ball3_boundary_to_volume;new_edge_mean_forman;new_edge_min_forman;post_return_spectral_dim_proxy;post_return_t2;post_return_t4;post_return_t6;support_ball_2). Best sorted rule is delta_return_t2/p0_ge_p1, but the screen is underdetermined.
- `next_step`: `choose_one_pre_registered_guard_then_v15dp_two_seed_holdout` fordi Do not claim a selector before a fresh pre-registered holdout over at least two new growth seeds.

## Tolkning

- v15do er en forklarings-/observabelrunde, ikke en selector-validering.
- Hvis regelen brukes videre, maa den fryses noyaktig foer fresh growth-seed holdout.
- Den interessante muligheten er at aktivt-sett-typen kan vaere mer stabil enn enkeltplacement-rankingen.
- Dette er ikke evidens for Lorentz-likhet, global invariant, entanglement, partikler eller universell geometri.
