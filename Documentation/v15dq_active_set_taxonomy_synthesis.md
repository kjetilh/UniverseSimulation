# Relasjonell universgraf v0.15dq: active-set taxonomy synthesis

## Formal

Dette er en no-new-dynamics syntese etter v15dp.
Den smarte endringen er aa slutte aa refitte en to-type guard naar holdouten viser nye responsklasser.
I stedet samles eksisterende placement-landskap til en eksplisitt aktivt-sett-taksonomi.

## Seed taxonomy

| growth_seed | landscape_class | active_placements | covered_by_v15do_two_type_space | p0_established_rate | p1_established_rate | p2_established_rate | support_signatures |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 202 | single_active_p1 | p1 | 1 | 0.000 | 0.875 | 0.000 | p0:13,72,343;p1:1,58,537;p2:6,8,9 |
| 303 | multi_active_p0_p2 | p0;p2 | 1 | 0.500 | 0.000 | 0.500 | p0:3,4,827;p1:12,13,22;p2:25,177,430 |
| 404 | single_active_p1 | p1 | 1 | 0.000 | 0.500 | 0.000 | p0:3,27,434;p1:12,14,465;p2:5,159,1003 |
| 505 | multi_active_p0_p2 | p0;p2 | 1 | 0.750 | 0.250 | 0.750 | p0:5,98,599;p1:7,8,9;p2:13,14,263 |
| 606 | no_active | none | 0 | 0.000 | 0.000 | 0.000 | p0:12,14,30;p1:15,16,458;p2:7,8,707 |
| 707 | single_active_p0 | p0 | 0 | 0.750 | 0.000 | 0.000 | p0:151,795,884;p1:12,13,15;p2:13,15,186 |

## Taxonomy summary

| landscape_class | n_seeds | growth_seeds | old_v15do_type_space | median_p0_established_rate | median_p1_established_rate | median_p2_established_rate |
| --- | --- | --- | --- | --- | --- | --- |
| multi_active_p0_p2 | 2 | 303;505 | 1 | 0.625 | 0.125 | 0.625 |
| single_active_p1 | 2 | 202;404 | 1 | 0.000 | 0.688 | 0.000 |
| no_active | 1 | 606 | 0 | 0.000 | 0.000 | 0.000 |
| single_active_p0 | 1 | 707 | 0 | 0.750 | 0.000 | 0.000 |

## Pre-run contrast families

| feature_family | evidence_strength | n_contrasts | n_clean_current_sample | clean_rate | example_clean_features |
| --- | --- | --- | --- | --- | --- |
| curvature_shortcut | repeated_pair_tiny | 42 | 11 | 0.262 | base_mean_forman_incident_support_range;delta_mean_forman_incident_support_range;new_edge_mean_forman_p2;new_edge_mean_forman_p2_minus_p0;new_edge_mean_forman_p2_minus_p1;new_edge_mean_forman_range;new_edge_min_forman_p2;new_edge_min_forman_p2_minus_p0 |
| curvature_shortcut | singleton_descriptive_only | 210 | 155 | 0.738 | base_mean_forman_incident_support_p0;base_mean_forman_incident_support_p0_minus_p1;base_mean_forman_incident_support_p1;base_mean_forman_incident_support_p2_minus_p0;base_mean_forman_incident_support_range;delta_mean_forman_incident_support_p0;delta_mean_forman_incident_support_p0_minus_p1;delta_mean_forman_incident_support_p1 |
| local_volume_topology | repeated_pair_tiny | 21 | 8 | 0.381 | local_ball3_beta1_p2;local_ball3_beta1_p2_minus_p0;local_ball3_beta1_p2_minus_p1;local_ball3_boundary_to_volume_p0_minus_p1;local_ball3_boundary_to_volume_p1;local_ball3_boundary_to_volume_p2_minus_p0;local_ball3_boundary_to_volume_p2_minus_p1;local_ball3_node_count_p2 |
| local_volume_topology | singleton_descriptive_only | 105 | 84 | 0.800 | local_ball3_beta1_p0;local_ball3_beta1_p0_minus_p1;local_ball3_beta1_p1;local_ball3_beta1_p2_minus_p0;local_ball3_beta1_p2_minus_p1;local_ball3_beta1_range;local_ball3_boundary_to_volume_p0;local_ball3_boundary_to_volume_p0_minus_p1 |
| return_probability | repeated_pair_tiny | 84 | 33 | 0.393 | base_return_spectral_dim_proxy_p2;base_return_t2_p0;base_return_t2_p0_minus_p1;base_return_t2_p1;base_return_t2_p2_minus_p0;base_return_t2_p2_minus_p1;base_return_t4_p0;base_return_t4_p0_minus_p1 |
| return_probability | singleton_descriptive_only | 420 | 295 | 0.702 | base_return_spectral_dim_proxy_p2;base_return_spectral_dim_proxy_p2_minus_p0;base_return_spectral_dim_proxy_range;base_return_t2_p0;base_return_t2_p0_minus_p1;base_return_t2_p1;base_return_t2_p2;base_return_t2_p2_minus_p0 |
| shortcut_reach | repeated_pair_tiny | 63 | 4 | 0.063 | delta_ball3_efficiency_p0;delta_ball3_efficiency_p2_minus_p0;delta_ball3_mean_pair_distance_p0;post_ball3_mean_pair_distance_range |
| shortcut_reach | singleton_descriptive_only | 315 | 190 | 0.603 | base_ball3_efficiency_p0;base_ball3_efficiency_p0_minus_p1;base_ball3_efficiency_p2_minus_p1;base_ball3_efficiency_range;base_ball3_mean_pair_distance_p0;base_ball3_mean_pair_distance_p0_minus_p1;base_ball3_mean_pair_distance_p2_minus_p1;base_ball3_mean_pair_distance_range |
| support_volume_topology | repeated_pair_tiny | 77 | 9 | 0.117 | ball3_over_ball1_p2;ball3_over_ball1_p2_minus_p0;ball3_over_ball1_range;mean_support_degree_p1;support_ball3_minus_ball1_p2;support_ball3_minus_ball2_p2;support_ball_2_p2_minus_p1;support_ball_3_p2 |
| support_volume_topology | singleton_descriptive_only | 385 | 234 | 0.608 | ball3_over_ball1_p0;ball3_over_ball1_p0_minus_p1;ball3_over_ball1_p1;ball3_over_ball1_p2;ball3_over_ball1_p2_minus_p0;ball3_over_ball1_p2_minus_p1;ball3_over_ball1_range;mean_support_degree_p0 |

## Repeated-class descriptive contrasts

| left_type | right_type | feature | feature_family | direction | left_median | right_median |
| --- | --- | --- | --- | --- | --- | --- |
| multi_active_p0_p2 | single_active_p1 | base_mean_forman_incident_support_range | curvature_shortcut | single_active_p1_gt_multi_active_p0_p2 | 5.518 | 8.200 |
| multi_active_p0_p2 | single_active_p1 | delta_mean_forman_incident_support_range | curvature_shortcut | single_active_p1_gt_multi_active_p0_p2 | 0.435 | 0.553 |
| multi_active_p0_p2 | single_active_p1 | new_edge_mean_forman_p2 | curvature_shortcut | multi_active_p0_p2_gt_single_active_p1 | -7.500 | -14.500 |
| multi_active_p0_p2 | single_active_p1 | new_edge_mean_forman_p2_minus_p0 | curvature_shortcut | multi_active_p0_p2_gt_single_active_p1 | 1.500 | -5.000 |
| multi_active_p0_p2 | single_active_p1 | new_edge_mean_forman_p2_minus_p1 | curvature_shortcut | multi_active_p0_p2_gt_single_active_p1 | 3.000 | -4.000 |
| multi_active_p0_p2 | single_active_p1 | new_edge_mean_forman_range | curvature_shortcut | single_active_p1_gt_multi_active_p0_p2 | 3.500 | 5.500 |
| multi_active_p0_p2 | single_active_p1 | new_edge_min_forman_p2 | curvature_shortcut | multi_active_p0_p2_gt_single_active_p1 | -7.500 | -14.500 |
| multi_active_p0_p2 | single_active_p1 | new_edge_min_forman_p2_minus_p0 | curvature_shortcut | multi_active_p0_p2_gt_single_active_p1 | 1.500 | -5.000 |
| multi_active_p0_p2 | single_active_p1 | new_edge_min_forman_p2_minus_p1 | curvature_shortcut | multi_active_p0_p2_gt_single_active_p1 | 3.000 | -4.000 |
| multi_active_p0_p2 | single_active_p1 | new_edge_min_forman_range | curvature_shortcut | single_active_p1_gt_multi_active_p0_p2 | 3.500 | 5.500 |
| multi_active_p0_p2 | single_active_p1 | post_mean_forman_incident_support_range | curvature_shortcut | single_active_p1_gt_multi_active_p0_p2 | 5.129 | 7.760 |
| multi_active_p0_p2 | single_active_p1 | local_ball3_beta1_p2 | local_volume_topology | single_active_p1_gt_multi_active_p0_p2 | 16.000 | 42.500 |
| multi_active_p0_p2 | single_active_p1 | local_ball3_beta1_p2_minus_p0 | local_volume_topology | single_active_p1_gt_multi_active_p0_p2 | -7.500 | 13.000 |
| multi_active_p0_p2 | single_active_p1 | local_ball3_beta1_p2_minus_p1 | local_volume_topology | single_active_p1_gt_multi_active_p0_p2 | -13.500 | 15.500 |
| multi_active_p0_p2 | single_active_p1 | local_ball3_boundary_to_volume_p0_minus_p1 | local_volume_topology | multi_active_p0_p2_gt_single_active_p1 | 0.329 | -0.114 |
| multi_active_p0_p2 | single_active_p1 | local_ball3_boundary_to_volume_p1 | local_volume_topology | single_active_p1_gt_multi_active_p0_p2 | 0.504 | 0.985 |
| multi_active_p0_p2 | single_active_p1 | local_ball3_boundary_to_volume_p2_minus_p0 | local_volume_topology | multi_active_p0_p2_gt_single_active_p1 | -0.166 | -0.277 |
| multi_active_p0_p2 | single_active_p1 | local_ball3_boundary_to_volume_p2_minus_p1 | local_volume_topology | multi_active_p0_p2_gt_single_active_p1 | 0.162 | -0.391 |
| multi_active_p0_p2 | single_active_p1 | local_ball3_node_count_p2 | local_volume_topology | single_active_p1_gt_multi_active_p0_p2 | 77.000 | 160.500 |
| multi_active_p0_p2 | single_active_p1 | base_return_spectral_dim_proxy_p2 | return_probability | single_active_p1_gt_multi_active_p0_p2 | 1.523 | 1.814 |
| multi_active_p0_p2 | single_active_p1 | base_return_t2_p0 | return_probability | single_active_p1_gt_multi_active_p0_p2 | 0.286 | 0.375 |
| multi_active_p0_p2 | single_active_p1 | base_return_t2_p0_minus_p1 | return_probability | single_active_p1_gt_multi_active_p0_p2 | -0.098 | 0.078 |
| multi_active_p0_p2 | single_active_p1 | base_return_t2_p1 | return_probability | multi_active_p0_p2_gt_single_active_p1 | 0.384 | 0.297 |
| multi_active_p0_p2 | single_active_p1 | base_return_t2_p2_minus_p0 | return_probability | multi_active_p0_p2_gt_single_active_p1 | 0.100 | -0.017 |

## Operativ lesning

- `input_scope`: `no_new_dynamics` fordi v15dq leser v15dn og v15dp placement/morphology CSV-er; ingen nye defect-runs er kjoert.
- `taxonomy_scope`: `expanded_beyond_v15do_two_type_space` fordi Observed classes: multi_active_p0_p2:2;no_active:1;single_active_p0:1;single_active_p1:2. Old v15do type-space covers 4/6 seeds; new classes cover 2/6.
- `repetition_balance`: `mixed_repeated_and_singleton_classes` fordi Repeated classes: multi_active_p0_p2;single_active_p1. Singleton classes: no_active;single_active_p0.
- `v15dp_guard_reading`: `guard_inconclusive_unobserved_active_set_type` fordi Frozen delta_return_t2 guard is retained only as a failed candidate, not refit.
- `pre_run_contrasts`: `descriptive_leads_only` fordi Repeated-pair clean contrasts in current sample: 65. Because n is tiny and two classes are singletons, these are leads, not selector validation.
- `next_step`: `build_taxonomy_mapper_before_new_selector` fordi Neste dynamiske budsjett bor brukes til aa kartlegge flere fresh seeds eller teste en taxonomy-mapper; ikke til aa refitte den gamle two-type-guarden.

## Tolkning

- `none` og `single_active_p0` maa inn i type-rommet foer nye selector-claims.
- Repeated classes (`single_active_p1`, `multi_active_p0_p2`) kan brukes til deskriptive contrasts, men ikke som validert lov.
- Singleton classes er viktige som taxonomisk varsellampe, men kan ikke laere en robust mapper alene.
- Ikke oppgrader dette til Lorentz-, invariant-, entanglement-, partikkel- eller universell geometri-evidens.
