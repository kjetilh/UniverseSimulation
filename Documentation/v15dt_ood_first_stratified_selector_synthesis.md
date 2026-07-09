# Relasjonell universgraf v0.15dt: OOD-first stratified selector synthesis

## Formal

Dette er en no-new-dynamics selector-syntese etter v15ds.
Den kombinerer v15dq+v15dr+v15ds, bruker bare pre-run morphology, og evaluerer med leave-one-seed-out.
Singleton-klasser behandles som OOD/unknown, ikke som trenbare klasser.

## Scope

| field | value |
| --- | --- |
| target | 1024 |
| perturbation | add_chord |
| placements | p0;p1;p2 |
| repeated_class_min_seeds | 3 |
| max_features | 8 |
| synthesis_source | v15dt_ood_first_stratified_selector_from_v15dq_v15dr_v15ds |

## Class roles

| landscape_class | n_seeds | growth_seeds | selector_role |
| --- | --- | --- | --- |
| multi_active_p0_p2 | 4 | 303;505;1511;1601 | repeated_trainable |
| single_active_p2 | 4 | 808;1001;1201;1301 | repeated_trainable |
| no_active | 3 | 606;909;1409 | repeated_trainable |
| single_active_p1 | 3 | 202;404;1709 | repeated_trainable |
| multi_active_p0_p1 | 1 | 1103 | singleton_ood |
| single_active_p0 | 1 | 707 | singleton_ood |

## Selected features

| selector_feature_rank | feature | feature_family | macro_oriented_auc | separation_score | ood_outside_train_range_fraction |
| --- | --- | --- | --- | --- | --- |
| 1 | delta_return_t4_p0 | return_probability | 0.813 | 4.495 | 0.000 |
| 2 | support_boundary_to_volume_p1 | support_volume_topology | 0.804 | 7.789 | 0.500 |
| 3 | mean_support_degree_p1 | support_volume_topology | 0.804 | 7.789 | 0.500 |
| 4 | delta_return_t2_p0 | return_probability | 0.803 | 8.058 | 0.000 |
| 5 | post_mean_forman_incident_support_p1 | curvature_shortcut | 0.790 | 10.379 | 0.000 |
| 6 | base_mean_forman_incident_support_p1 | curvature_shortcut | 0.763 | 10.855 | 0.000 |
| 7 | local_ball3_boundary_to_volume_p1 | local_volume_topology | 0.763 | 6.516 | 0.000 |
| 8 | local_ball3_beta1_p0 | local_volume_topology | 0.749 | 7.097 | 0.000 |

## Candidate class profiles

| landscape_class | feature | class_n_train | class_median | buffered_min | buffered_max |
| --- | --- | --- | --- | --- | --- |
| multi_active_p0_p2 | delta_return_t4_p0 | 4 | -0.015 | -0.020 | -0.009 |
| multi_active_p0_p2 | support_boundary_to_volume_p1 | 4 | 8.167 | 5.933 | 8.733 |
| multi_active_p0_p2 | mean_support_degree_p1 | 4 | 9.500 | 7.267 | 10.067 |
| multi_active_p0_p2 | delta_return_t2_p0 | 4 | -0.017 | -0.035 | -0.010 |
| multi_active_p0_p2 | post_mean_forman_incident_support_p1 | 4 | -12.853 | -16.755 | -11.791 |
| multi_active_p0_p2 | base_mean_forman_incident_support_p1 | 4 | -12.469 | -15.888 | -11.006 |
| multi_active_p0_p2 | local_ball3_boundary_to_volume_p1 | 4 | 0.508 | 0.414 | 0.762 |
| multi_active_p0_p2 | local_ball3_beta1_p0 | 4 | 27.500 | 13.000 | 34.000 |
| no_active | delta_return_t4_p0 | 3 | -0.014 | -0.015 | -0.009 |
| no_active | support_boundary_to_volume_p1 | 3 | 5.667 | 2.133 | 8.200 |
| no_active | mean_support_degree_p1 | 3 | 7.000 | 3.467 | 9.533 |
| no_active | delta_return_t2_p0 | 3 | -0.015 | -0.019 | -0.009 |
| no_active | post_mean_forman_incident_support_p1 | 3 | -11.640 | -13.120 | -5.980 |
| no_active | base_mean_forman_incident_support_p1 | 3 | -10.792 | -12.207 | -5.602 |
| no_active | local_ball3_boundary_to_volume_p1 | 3 | 0.641 | 0.550 | 0.847 |
| no_active | local_ball3_beta1_p0 | 3 | 51.000 | 25.000 | 60.000 |
| single_active_p1 | delta_return_t4_p0 | 3 | -0.030 | -0.036 | -0.015 |
| single_active_p1 | support_boundary_to_volume_p1 | 3 | 4.333 | 2.467 | 8.533 |
| single_active_p1 | mean_support_degree_p1 | 3 | 5.667 | 3.800 | 9.867 |
| single_active_p1 | delta_return_t2_p0 | 3 | -0.033 | -0.034 | -0.032 |
| single_active_p1 | post_mean_forman_incident_support_p1 | 3 | -7.000 | -15.508 | -5.223 |
| single_active_p1 | base_mean_forman_incident_support_p1 | 3 | -5.917 | -15.291 | -4.296 |
| single_active_p1 | local_ball3_boundary_to_volume_p1 | 3 | 1.052 | 0.622 | 1.349 |
| single_active_p1 | local_ball3_beta1_p0 | 3 | 36.000 | 19.600 | 43.400 |
| single_active_p2 | delta_return_t4_p0 | 4 | -0.026 | -0.168 | 0.010 |
| single_active_p2 | support_boundary_to_volume_p1 | 4 | 10.500 | 8.200 | 11.467 |
| single_active_p2 | mean_support_degree_p1 | 4 | 11.833 | 9.533 | 12.800 |
| single_active_p2 | delta_return_t2_p0 | 4 | -0.026 | -0.166 | 0.002 |
| single_active_p2 | post_mean_forman_incident_support_p1 | 4 | -17.111 | -23.456 | -12.664 |
| single_active_p2 | base_mean_forman_incident_support_p1 | 4 | -16.303 | -23.843 | -11.559 |
| single_active_p2 | local_ball3_boundary_to_volume_p1 | 4 | 0.571 | 0.412 | 0.865 |
| single_active_p2 | local_ball3_beta1_p0 | 4 | 23.500 | -3.400 | 34.400 |

## Leave-one-seed-out evaluation

| growth_seed | source | actual_class | actual_repeated_train_class | predicted_class | prediction_reason | nearest_class | nearest_mean_distance | distance_margin | nearest_envelope_hits | repeated_class_hit | singleton_ood_correct_abstain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 202 | v15dq | single_active_p1 | 1 | unknown | mean_distance_too_high | single_active_p1 | 1.805 | 0.846 | 5 | 0 | 0 |
| 303 | v15dq | multi_active_p0_p2 | 1 | multi_active_p0_p2 | accepted_repeated_class | multi_active_p0_p2 | 0.452 | 0.755 | 7 | 1 | 0 |
| 404 | v15dq | single_active_p1 | 1 | unknown | mean_distance_too_high | single_active_p2 | 1.442 | 0.119 | 5 | 0 | 0 |
| 505 | v15dq | multi_active_p0_p2 | 1 | multi_active_p0_p2 | accepted_repeated_class | multi_active_p0_p2 | 0.678 | 0.891 | 6 | 1 | 0 |
| 606 | v15dq | no_active | 1 | unknown | mean_distance_too_high | single_active_p1 | 1.809 | 0.196 | 5 | 0 | 0 |
| 707 | v15dq | single_active_p0 | 0 | unknown | mean_distance_too_high | single_active_p2 | 4.043 | 1.591 | 6 | 0 | 1 |
| 808 | v15dr | single_active_p2 | 1 | unknown | mean_distance_too_high | multi_active_p0_p2 | 1.724 | 0.191 | 5 | 0 | 0 |
| 909 | v15dr | no_active | 1 | multi_active_p0_p2 | accepted_repeated_class | multi_active_p0_p2 | 0.663 | 0.504 | 6 | 0 | 0 |
| 1001 | v15dr | single_active_p2 | 1 | unknown | mean_distance_too_high | single_active_p2 | 1.790 | 0.038 | 8 | 0 | 0 |
| 1103 | v15dr | multi_active_p0_p1 | 0 | unknown | mean_distance_too_high | no_active | 1.298 | 0.174 | 5 | 0 | 1 |
| 1201 | v15ds | single_active_p2 | 1 | unknown | mean_distance_too_high | multi_active_p0_p2 | 9.136 | 0.087 | 3 | 0 | 0 |
| 1301 | v15ds | single_active_p2 | 1 | unknown | mean_distance_too_high | single_active_p2 | 2.394 | 0.084 | 5 | 0 | 0 |
| 1409 | v15ds | no_active | 1 | unknown | ambiguous_nearest_class | no_active | 1.118 | 0.051 | 6 | 0 | 0 |
| 1511 | v15ds | multi_active_p0_p2 | 1 | unknown | ambiguous_nearest_class | single_active_p2 | 1.248 | 0.128 | 6 | 0 | 0 |
| 1601 | v15ds | multi_active_p0_p2 | 1 | multi_active_p0_p2 | accepted_repeated_class | multi_active_p0_p2 | 0.424 | 0.753 | 7 | 1 | 0 |
| 1709 | v15ds | single_active_p1 | 1 | unknown | mean_distance_too_high | single_active_p1 | 1.866 | 1.298 | 3 | 0 | 0 |

## Aggregate evaluation

| key | value | evidence |
| --- | --- | --- |
| synthesis_source | v15dt_ood_first_stratified_selector_from_v15dq_v15dr_v15ds | no-new-dynamics OOD-first class-stratified selector synthesis |
| train_classes | multi_active_p0_p2;no_active;single_active_p1;single_active_p2 | min_seed_count=3 |
| selected_features | delta_return_t4_p0;support_boundary_to_volume_p1;mean_support_degree_p1;delta_return_t2_p0;post_mean_forman_incident_support_p1;base_mean_forman_incident_support_p1;local_ball3_boundary_to_volume_p1;local_ball3_beta1_p0 | max_features=8; max_per_family=2 |
| repeated_leave_one_out_accuracy | 0.214 | hits=3; repeated=14; abstain=10; miss=1 |
| singleton_ood_abstain_accuracy | 1.000 | abstain=2; singleton=2; false_known=0 |
| repeated_abstain_fraction | 0.714 | abstention on trainable repeated classes |
| selector_candidate_status | ood_guard_ok_but_class_prediction_weak | leave-one-seed-out repeated classes plus singleton OOD abstention |

## Operativ lesning

- `input_scope`: `combined_v15dq_v15dr_v15ds_no_new_dynamics` fordi Seed count=16; class counts=multi_active_p0_p2:4;single_active_p2:4;no_active:3;single_active_p1:3;multi_active_p0_p1:1;single_active_p0:1.
- `class_stratification`: `repeated_classes_trainable_singletons_ood` fordi Train classes=multi_active_p0_p2;no_active;single_active_p1;single_active_p2; singletons behandles som OOD/unknown.
- `feature_selection`: `posthoc_family_diverse_candidate` fordi Selected 8 pre-run morphology features. Dette er kandidatdesign, ikke validert selector.
- `leave_one_out_result`: `ood_guard_ok_but_class_prediction_weak` fordi Repeated LOO accuracy=0.214; singleton OOD abstain accuracy=1.000.
- `next_step`: `improve_class_profiles_or_add_one_atlas_round` fordi OOD-abstention fungerer, men repeated-class prediksjon er for svak; mer atlas eller bedre profiler trengs.

## Tolkning

- Dette er post-hoc kandidatdesign, ikke en validated selector.
- En fresh holdout er bare berettiget hvis OOD-vakten og repeated-class treffsikkerheten begge er sterke nok.
- Ikke oppgrader dette til invariant/Lorentz/partikkel/entanglement-claim.
