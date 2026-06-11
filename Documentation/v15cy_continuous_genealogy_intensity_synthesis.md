# Relasjonell universgraf v0.15cy: continuous genealogy intensity synthesis

## Formal

Dette er en synteserunde uten ny dynamikk. Den leser v15cw/v15cx-run-tabeller og tester om kontinuerlig genealogy-intensitet forklarer far-shell horizon bedre enn grove event-chain labels.
Intensity-scoren bruker bare genealogy/event/mass-felter; horizon-label og horizon-span brukes bare som downstream evaluering.

## Inputs

| lab | scope | path |
| --- | --- | --- |
| v15cw | calibration_seed_split | `Documentation/v15cw_add_chord_p1_p3_genealogy_runs.csv` |
| v15cx | p1_1024_fresh_holdout | `Documentation/v15cx_p1_1024_genealogy_holdout_runs.csv` |

## Per-run score

| lab | target | placement | seed | horizon | pattern | intensity | churn/step | max mass frac | dual frac |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v15cw | 896 | p1 | 7307 | established_far_shell_horizon | split_persistent_dual | 0.635 | 0.201 | 0.183 | 0.954 |
| v15cw | 896 | p1 | 7351 | no_far_shell_horizon | split_persistent_dual | 0.110 | 0.011 | 0.020 | 0.384 |
| v15cw | 896 | p3 | 7307 | no_far_shell_horizon | split_persistent_dual | 0.384 | 0.144 | 0.104 | 0.638 |
| v15cw | 896 | p3 | 7351 | no_far_shell_horizon | split_persistent_dual | 0.723 | 0.388 | 0.253 | 0.011 |
| v15cw | 1024 | p1 | 7307 | no_far_shell_horizon | birth_death_churn | 0.007 | 0.015 | 0.023 | 0.000 |
| v15cw | 1024 | p1 | 7351 | established_far_shell_horizon | split_fragment | 0.377 | 0.128 | 0.140 | 0.000 |
| v15cw | 1024 | p3 | 7307 | established_far_shell_horizon | split_persistent_dual | 0.725 | 0.371 | 0.228 | 0.063 |
| v15cw | 1024 | p3 | 7351 | established_far_shell_horizon | split_persistent_dual | 0.643 | 0.205 | 0.202 | 0.904 |
| v15cx | 1024 | p1 | 7411 | established_far_shell_horizon | split_persistent_dual | 0.935 | 0.444 | 0.261 | 0.974 |
| v15cx | 1024 | p1 | 7477 | mixed_far_shell_horizon | split_persistent_dual | 0.650 | 0.259 | 0.179 | 0.937 |
| v15cx | 1024 | p1 | 7541 | established_far_shell_horizon | split_persistent_dual | 0.797 | 0.409 | 0.210 | 0.904 |
| v15cx | 1024 | p1 | 7603 | established_far_shell_horizon | split_persistent_dual | 0.987 | 0.506 | 0.270 | 0.979 |

## Scope summary

| scope | n | est rate | intensity AUC | span rho | mean int est | mean int non | patterns |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all_runs | 12 | 0.583 | 0.800 | 0.521 | 0.728 | 0.375 | birth_death_churn:1;split_fragment:1;split_persistent_dual:10 |
| v15cw_all | 8 | 0.500 | 0.750 | 0.443 | 0.595 | 0.306 | birth_death_churn:1;split_fragment:1;split_persistent_dual:6 |
| p1_1024_all | 6 | 0.667 | 0.875 | 0.638 | 0.774 | 0.329 | birth_death_churn:1;split_fragment:1;split_persistent_dual:4 |
| p1_1024_holdout_only | 4 | 0.750 | 1.000 | 0.949 | 0.906 | 0.650 | split_persistent_dual:4 |

## Top metrics

| scope | rank | metric | AUC | span rho | delta |
| --- | --- | --- | --- | --- | --- |
| all_runs | 1 | max_component_count_per_target | 0.943 | 0.783 | 0.019 |
| all_runs | 2 | first_split_earliness | 0.886 | 0.766 | 0.375 |
| all_runs | 3 | max_total_defect_mass_fraction | 0.829 | 0.577 | 0.097 |
| p1_1024_all | 1 | compress_per_step | 1.000 | 0.893 | 0.002 |
| p1_1024_all | 2 | first_split_earliness | 0.875 | 0.880 | 0.492 |
| p1_1024_all | 3 | genealogy_intensity_index | 0.875 | 0.638 | 0.445 |
| p1_1024_holdout_only | 1 | genealogy_intensity_index | 1.000 | 0.949 | 0.256 |
| p1_1024_holdout_only | 2 | churn_per_step | 1.000 | 0.949 | 0.194 |
| p1_1024_holdout_only | 3 | birth_death_per_step | 1.000 | 0.949 | 0.142 |
| v15cw_all | 1 | first_split_earliness | 0.938 | 0.743 | 0.466 |
| v15cw_all | 2 | max_component_count_per_target | 0.938 | 0.743 | 0.021 |
| v15cw_all | 3 | first_birth_earliness | 0.812 | 0.456 | 0.220 |

## Operativ lesning

- `input_control`: `clean` fordi Leste labs ['v15cw', 'v15cx'] fra eksisterende CSV-er; ingen ny dynamikk er kjoert.
- `coarse_label_result`: `coarse_event_labels_not_enough` fordi v15cx svekket birth_death_churn/split_fragment som kategorisk selector; v15cy tester derfor kontinuerlige genealogy-features.
- `continuous_intensity_axis`: `continuous_genealogy_intensity_promising_small_n` fordi Intensity AUC er 0.800 globalt, 0.875 for p1/1024 og 1.000 i holdout-only. Dette er lovende, men post-hoc og liten n.
- `best_p1_1024_metric`: `compress_per_step` fordi Beste p1/1024-metrikk etter AUC er compress_per_step med AUC 1.000 og Spearman mot horizon-span 0.893.
- `next_step`: `pre_register_continuous_intensity_holdout` fordi Frys intensity-score/top-metrikker og test paa nye runs foer scorevekter eller observabler justeres videre.

## Tolkning

- Dette er ikke en partikkel-, Lorentz-, invariant- eller entanglement-paastand.
- En positiv intensity-score betyr bare at noen genealogy-intensitetsmaal predikerer horizon bedre enn grove labels i dette lokale datasettet.
- Hvis neste holdout feiler, maa genealogy nedgraderes fra selector til diagnostikk og vi bor teste timing/phase-coupling mot band-entry.
