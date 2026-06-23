# Relasjonell universgraf v0.15dn: multi-active landscape synthesis

## Formal

Dette er en no-new-dynamics syntese etter v15dm.
Den kombinerer eksisterende `1024/add_chord/p0,p1,p2`-resultater fra growth seeds `202`, `303`, `404` og `505`.
Formaalet er aa teste om pre-run morfologi kan foreslaa et lite aktivt plasseringssett per base,
i stedet for aa fortsette med en single-winner selector som v15dm allerede svekket.
Alle set-regler her er post-hoc screens; de er observabeldesign, ikke validerte selectors.

## Seed landscapes

| growth_seed | source | landscape_class | active_placements | placement_rates |
| --- | --- | --- | --- | --- |
| 202 | v15dl | single_active_p1 | p1 | p0:0.000;p1:0.875;p2:0.000 |
| 303 | v15dl | multi_active_p0_p2 | p0;p2 | p0:0.500;p1:0.000;p2:0.500 |
| 404 | v15dl | single_active_p1 | p1 | p0:0.000;p1:0.500;p2:0.000 |
| 505 | v15dm | multi_active_p0_p2 | p0;p2 | p0:0.750;p1:0.250;p2:0.750 |

## Placement rows

| growth_seed | placement | source | label_counts | established_rate | active_placement | support_signature | delta_return_t2 | delta_return_t4 | base_return_spectral_dim_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 202 | 0 | v15dl | no_far_shell_horizon:8 | 0.000 | 0 | 13,72,343 | -0.0334410959410959 | -0.018340512214362892 | 1.6533443646008974 |
| 202 | 1 | v15dl | established_far_shell_horizon:7;no_far_shell_horizon:1 | 0.875 | 1 | 1,58,537 | -0.02157738095238093 | -0.013610869346666998 | 1.5920363014324512 |
| 202 | 2 | v15dl | mixed_far_shell_horizon:2;no_far_shell_horizon:6 | 0.000 | 0 | 6,8,9 | -0.024934301614973897 | -0.020969629441292603 | 1.7411678272264506 |
| 303 | 0 | v15dl | established_far_shell_horizon:4;no_far_shell_horizon:4 | 0.500 | 1 | 3,4,827 | -0.013853469762560688 | -0.018099240931717664 | 1.3896874093294376 |
| 303 | 1 | v15dl | no_far_shell_horizon:8 | 0.000 | 0 | 12,13,22 | -0.022319223985890646 | -0.014622078165971442 | 1.8279603950526455 |
| 303 | 2 | v15dl | established_far_shell_horizon:4;mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.500 | 1 | 25,177,430 | -0.026873897707230976 | -0.01575895002572847 | 1.5826960346544348 |
| 404 | 0 | v15dl | no_far_shell_horizon:8 | 0.000 | 0 | 3,27,434 | -0.032407766525413606 | -0.029506342081421888 | 1.3427049561886841 |
| 404 | 1 | v15dl | established_far_shell_horizon:4;mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.500 | 1 | 12,14,465 | -0.011507751507751518 | -0.008013472108073655 | 1.5814729653128132 |
| 404 | 2 | v15dl | no_far_shell_horizon:8 | 0.000 | 0 | 5,159,1003 | -0.06902116402116404 | -0.035529223341758315 | 1.8867711065117236 |
| 505 | 0 | v15dm | established_far_shell_horizon:3;no_far_shell_horizon:1 | 0.750 | 1 | 5,98,599 | -0.020 | -0.011 | 2.149 |
| 505 | 1 | v15dm | established_far_shell_horizon:1;no_far_shell_horizon:3 | 0.250 | 0 | 7,8,9 | -0.025 | -0.027 | 1.061 |
| 505 | 2 | v15dm | established_far_shell_horizon:3;no_far_shell_horizon:1 | 0.750 | 1 | 13,14,263 | -0.033 | -0.025 | 1.464 |

## Best placement-level morphology audits

| metric | feature_family | best_direction_posthoc | best_auc_posthoc | spearman_vs_established_rate_raw | median_active_raw | median_inactive_raw |
| --- | --- | --- | --- | --- | --- | --- |
| delta_return_t4 | return_probability | high | 0.861 | 0.538 | -0.015 | -0.024 |
| delta_return_t6 | return_probability | high | 0.833 | 0.421 | -0.009 | -0.018 |
| local_ball3_beta1 | local_volume_topology | low | 0.819 | -0.724 | 19.000 | 33.500 |
| delta_return_t2 | return_probability | high | 0.806 | 0.465 | -0.021 | -0.029 |
| base_return_t2 | return_probability | low | 0.778 | -0.311 | 0.309 | 0.378 |
| new_edge_mean_forman | curvature_shortcut | high | 0.764 | 0.527 | -9.500 | -11.500 |
| new_edge_min_forman | curvature_shortcut | high | 0.764 | 0.527 | -9.500 | -11.500 |
| delta_ball3_mean_pair_distance | shortcut_reach | high | 0.750 | 0.201 | -0.012 | -0.043 |
| support_ball_1 | support_volume_topology | low | 0.736 | -0.376 | 14.500 | 20.500 |
| base_return_t4 | return_probability | low | 0.722 | -0.245 | 0.176 | 0.207 |
| delta_ball3_efficiency | shortcut_reach | low | 0.722 | -0.168 | 0.001 | 0.002 |
| local_ball3_boundary_to_volume | local_volume_topology | high | 0.722 | 0.337 | 0.749 | 0.594 |

## Best active-set screens

| metric | direction | rule_type | rule_param | coverage_fraction | precision_fraction | burden_fraction | mean_predicted_count | exact_set_match_rate | total_false_positive | rule_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| local_ball3_beta1 | low | top_k | 2 | 1.000 | 0.750 | 0.667 | 2.000 | 0.500 | 2 | posthoc_full_coverage_nontrivial_set_candidate |
| local_ball3_boundary_to_volume | high | above_or_equal_median | within_seed | 1.000 | 0.750 | 0.667 | 2.000 | 0.500 | 2 | posthoc_full_coverage_nontrivial_set_candidate |
| local_ball3_boundary_to_volume | high | top_k | 2 | 1.000 | 0.750 | 0.667 | 2.000 | 0.500 | 2 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t4 | high | epsilon_from_best | eps_0p015 | 1.000 | 0.667 | 0.750 | 2.250 | 0.500 | 3 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_ball3_efficiency | high | epsilon_from_best | eps_0p010 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t2 | high | epsilon_from_best | eps_0p015 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t2 | high | epsilon_from_best | eps_0p020 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t4 | high | epsilon_from_best | eps_0p020 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t6 | high | epsilon_from_best | eps_0p015 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t6 | high | epsilon_from_best | eps_0p020 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| local_ball3_beta1 | low | above_or_equal_median | within_seed | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t2 | high | epsilon_from_best | eps_0p030 | 1.000 | 0.545 | 0.917 | 2.750 | 0.000 | 5 | posthoc_full_coverage_nontrivial_set_candidate |
| ball3_over_ball1 | high | top_k | 3 | 1.000 | 0.500 | 1.000 | 3.000 | 0.000 | 6 | trivial_full_coverage_selects_all |
| ball3_over_ball1 | low | top_k | 3 | 1.000 | 0.500 | 1.000 | 3.000 | 0.000 | 6 | trivial_full_coverage_selects_all |
| base_ball3_efficiency | high | top_k | 3 | 1.000 | 0.500 | 1.000 | 3.000 | 0.000 | 6 | trivial_full_coverage_selects_all |
| base_ball3_efficiency | low | top_k | 3 | 1.000 | 0.500 | 1.000 | 3.000 | 0.000 | 6 | trivial_full_coverage_selects_all |

## Best nontrivial active-set screens

| metric | direction | rule_type | rule_param | coverage_fraction | precision_fraction | burden_fraction | mean_predicted_count | exact_set_match_rate | total_false_positive | rule_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| local_ball3_beta1 | low | top_k | 2 | 1.000 | 0.750 | 0.667 | 2.000 | 0.500 | 2 | posthoc_full_coverage_nontrivial_set_candidate |
| local_ball3_boundary_to_volume | high | above_or_equal_median | within_seed | 1.000 | 0.750 | 0.667 | 2.000 | 0.500 | 2 | posthoc_full_coverage_nontrivial_set_candidate |
| local_ball3_boundary_to_volume | high | top_k | 2 | 1.000 | 0.750 | 0.667 | 2.000 | 0.500 | 2 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t4 | high | epsilon_from_best | eps_0p015 | 1.000 | 0.667 | 0.750 | 2.250 | 0.500 | 3 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_ball3_efficiency | high | epsilon_from_best | eps_0p010 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t2 | high | epsilon_from_best | eps_0p015 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t2 | high | epsilon_from_best | eps_0p020 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t4 | high | epsilon_from_best | eps_0p020 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t6 | high | epsilon_from_best | eps_0p015 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t6 | high | epsilon_from_best | eps_0p020 | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| local_ball3_beta1 | low | above_or_equal_median | within_seed | 1.000 | 0.600 | 0.833 | 2.500 | 0.250 | 4 | posthoc_full_coverage_nontrivial_set_candidate |
| delta_return_t2 | high | epsilon_from_best | eps_0p030 | 1.000 | 0.545 | 0.917 | 2.750 | 0.000 | 5 | posthoc_full_coverage_nontrivial_set_candidate |

## Operativ lesning

- `input_scope`: `no_new_dynamics_synthesis` fordi Combined v15dl seeds 202/303/404 and v15dm seed 505; old dynamic outputs are reused only as response labels.
- `landscape_state`: `multi_active_base_conditioned_landscape` fordi Active sets by seed: 202:p1; 303:p0;p2; 404:p1; 505:p0;p2. Unique active patterns=2; active count range=1-2.
- `placement_selector_language`: `single_winner_selector_deprioritized` fordi v15dm showed active p0;p2 while frozen top1/top2 return ranking captured only one active placement.
- `metric_screen`: `posthoc_metric_audit_only` fordi Best placement-level metric is delta_return_t4/high with AUC=0.861; this is descriptive because it is screened after outcomes.
- `set_rule_screen`: `posthoc_full_coverage_nontrivial_but_false_positive_set_rule` fordi Best nontrivial full-coverage rule still has false positives: 202:pred=p0;p1/active=p1/miss=none/fp=p0 | 303:pred=p0;p2/active=p0;p2/miss=none/fp=none | 404:pred=p0;p1/active=p1/miss=none/fp=p0 | 505:pred=p0;p2/active=p0;p2/miss=none/fp=none.
- `next_step`: `treat_as_observable_design_not_selector; require_fresh_holdout_if_used` fordi Do not promote any set rule without a fresh pre-registered holdout over at least two new growth seeds.

## Tolkning

- Resultatet skal ikke brukes som Lorentz-, invariant-, entanglement-, partikkel- eller universell-geometri-evidens.
- Hvis en set-regel ser lovende ut, er den en kandidat til frossen holdout, ikke en oppdaget lov.
- Hvis full coverage krever aa velge alle placements, har regelen ikke redusert usikkerhet.
- Det interessante spoersmaalet etter v15dn er om vi kan lage en pre-run observabel som predikerer aktivt sett med lavere burden enn `p0;p1;p2`.
