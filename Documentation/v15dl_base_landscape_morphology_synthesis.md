# Relasjonell universgraf v0.15dl: base-landscape morphology synthesis

## Formal

Dette er en no-new-dynamics syntese etter v15dk.
Den samler eksisterende `1024/add_chord/p0,p1,p2`-resultater fra growth seeds `202`, `303` og `404`,
og legger til billige pre-run morfologiobservabler paa basegrafen og add_chord-proben.
Gamle dynamiske labels brukes bare som responskolonner, ikke som nye runtime-resultater.

## Landscape by growth seed

| growth_seed | landscape_class | active_placements | placement_rates |
| --- | --- | --- | --- |
| 202 | single_active_p1 | p1 | p0:0.000;p1:0.875;p2:0.000 |
| 303 | multi_active_p0_p2 | p0;p2 | p0:0.500;p1:0.000;p2:0.500 |
| 404 | single_active_p1 | p1 | p0:0.000;p1:0.500;p2:0.000 |

## Placement summary

| growth_seed | placement | label_counts | established_rate | mean_high_horizon_span | support_signature_mode | support_ball_1 | support_ball_2 | support_ball_3 | delta_ball3_efficiency | base_return_spectral_dim_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 202 | 0 | no_far_shell_horizon:8 | 0.000 | 0.000 | 13,72,343 | 15.000 | 50.000 | 90.000 | 0.002 | 1.653 |
| 202 | 1 | established_far_shell_horizon:7;no_far_shell_horizon:1 | 0.875 | 136.750 | 1,58,537 | 14.000 | 27.000 | 49.000 | 0.012 | 1.592 |
| 202 | 2 | mixed_far_shell_horizon:2;no_far_shell_horizon:6 | 0.000 | 7.625 | 6,8,9 | 32.000 | 100.000 | 209.000 | 0.001 | 1.741 |
| 303 | 0 | established_far_shell_horizon:4;no_far_shell_horizon:4 | 0.500 | 86.000 | 3,4,827 | 15.000 | 57.000 | 146.000 | 0.000 | 1.390 |
| 303 | 1 | no_far_shell_horizon:8 | 0.000 | 0.000 | 12,13,22 | 24.000 | 51.000 | 82.000 | 0.007 | 1.828 |
| 303 | 2 | established_far_shell_horizon:4;mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.500 | 88.750 | 25,177,430 | 14.000 | 25.000 | 48.000 | 0.003 | 1.583 |
| 404 | 0 | no_far_shell_horizon:8 | 0.000 | 0.000 | 3,27,434 | 14.000 | 49.000 | 107.000 | 0.003 | 1.343 |
| 404 | 1 | established_far_shell_horizon:4;mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.500 | 103.250 | 12,14,465 | 24.000 | 80.000 | 175.000 | 0.000 | 1.581 |
| 404 | 2 | no_far_shell_horizon:8 | 0.000 | 0.000 | 5,159,1003 | 17.000 | 57.000 | 112.000 | 0.001 | 1.887 |

## Best morphology screens

| metric | feature_family | best_direction_posthoc | best_auc_posthoc | spearman_vs_established_rate_raw | median_active_raw | median_inactive_raw |
| --- | --- | --- | --- | --- | --- | --- |
| delta_return_t2 | return_probability | high | 0.900 | 0.671 | -0.018 | -0.032 |
| delta_return_t4 | return_probability | high | 0.900 | 0.708 | -0.015 | -0.021 |
| delta_return_t6 | return_probability | high | 0.850 | 0.559 | -0.009 | -0.017 |
| base_return_spectral_dim_proxy | return_probability | low | 0.800 | -0.447 | 1.582 | 1.741 |
| base_return_t2 | return_probability | low | 0.800 | -0.484 | 0.297 | 0.363 |
| post_return_spectral_dim_proxy | return_probability | low | 0.800 | -0.447 | 1.578 | 1.792 |
| local_ball3_beta1 | local_volume_topology | low | 0.775 | -0.571 | 25.500 | 36.000 |
| local_ball3_boundary_to_volume | local_volume_topology | high | 0.750 | 0.522 | 0.813 | 0.608 |
| base_mean_forman_incident_support | curvature_shortcut | high | 0.700 | 0.447 | -8.712 | -12.308 |
| base_return_t4 | return_probability | low | 0.700 | -0.298 | 0.176 | 0.193 |
| new_edge_mean_forman | curvature_shortcut | high | 0.700 | 0.319 | -10.500 | -12.000 |
| new_edge_min_forman | curvature_shortcut | high | 0.700 | 0.319 | -10.500 | -12.000 |

## Best rule screens

| metric | direction | top1_capture_fraction | top2_capture_fraction | top1_inactive_selected | top2_inactive_selected | rule_status |
| --- | --- | --- | --- | --- | --- | --- |
| delta_return_t2 | high | 0.750 | 0.750 | 0 | 3 | weak_posthoc_top2_scout |
| delta_return_t6 | high | 0.750 | 0.750 | 0 | 3 | weak_posthoc_top2_scout |
| base_return_spectral_dim_proxy | low | 0.500 | 1.000 | 1 | 2 | posthoc_top2_candidate_not_validated |
| local_ball3_beta1 | low | 0.500 | 1.000 | 1 | 2 | posthoc_top2_candidate_not_validated |
| local_ball3_boundary_to_volume | high | 0.500 | 1.000 | 1 | 2 | posthoc_top2_candidate_not_validated |
| post_return_spectral_dim_proxy | low | 0.500 | 1.000 | 1 | 2 | posthoc_top2_candidate_not_validated |
| base_ball3_mean_pair_distance | low | 0.500 | 0.750 | 1 | 3 | not_selector_ready |
| base_mean_forman_incident_support | high | 0.500 | 0.750 | 1 | 3 | not_selector_ready |
| base_return_t2 | low | 0.500 | 0.750 | 1 | 3 | weak_posthoc_top2_scout |
| base_return_t4 | low | 0.500 | 0.750 | 1 | 3 | weak_posthoc_top2_scout |
| delta_ball3_efficiency | low | 0.500 | 0.750 | 1 | 3 | not_selector_ready |
| delta_ball3_mean_pair_distance | high | 0.500 | 0.750 | 1 | 3 | not_selector_ready |

## Operativ lesning

- `artifact_control`: `clean` fordi Target summaries are separated and add_chord requested-match is clean.
- `landscape_state`: `base_conditioned_placement_landscape` fordi Active placements vary by growth seed: {202: [1], 303: [0, 2], 404: [1]}; unique patterns=2.
- `retired_selector`: `low_support_rank_retired` fordi v15dk top1/top2 support-rank capture was zero; low local support volume/gap should not be reused as selector.
- `morphology_screen`: `weak_posthoc_top2_scout` fordi Best placement-level AUC metric is `delta_return_t2` with posthoc AUC=0.900; best rule status=weak_posthoc_top2_scout.
- `next_step`: `freeze_best_morphology_rule_for_small_v15dm_holdout` fordi Beste post-hoc regel er `delta_return_t2`/high; den maa fryses foer ny dynamikk og kan ikke rapporteres som validert.

## Evidensgrenser

- Dette er ikke ny dynamikk; alle outcome-kolonner kommer fra eksisterende v15dg/v15dh/v15dk-run.
- Morfologireglene er post-hoc screens. De kan foreslaa en frossen v15dm-test, men er ikke validert her.
- Ikke bruk dette som Lorentz-, global invariant-, entanglement-, partikkel- eller universell geometri-claim.
