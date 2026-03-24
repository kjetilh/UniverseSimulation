# Relasjonell universgraf v0.13b: kryssregime-test av quasi-invarianter

## Formål

Denne runden tester om de viktigste langsomme driftssignalene fra v0.13 holder når vi åpner små lokale triad-, delete- og death-avvik rundt `band_zero_del`.

## Startstørrelser

| target | mean_initial | q10 | q90 | separated_from_prev |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Stabile kontrollakser fra v0.13

| rank | feature | mean_cv | q90_cv | slope_q10 | slope_q90 |
| --- | --- | --- | --- | --- | --- |
| 1 | initial_avg_degree | 0.026 | 0.032 | -0.006 | 0.082 |
| 2 | initial_spectral_per_sqrtN | 0.049 | 0.063 | -0.136 | -0.107 |
| 3 | initial_dim_proxy | 0.078 | 0.096 | -0.084 | 0.181 |
| 4 | initial_beta1_per_node | 0.240 | 0.296 | -0.013 | 0.031 |

## Regimeutfall per størrelse

| regime | axis | target | radius | overlap | fit_speed |
| --- | --- | --- | --- | --- | --- |
| band_death_0005 | death | 48 | 5.438 | 0.522 | 0.224 |
| band_death_0005 | death | 96 | 6.562 | 0.523 | 0.212 |
| band_death_0005 | death | 192 | 8.625 | 0.650 | 0.266 |
| band_death_0005 | death | 256 | 8.562 | 0.574 | 0.234 |
| band_pdel_0005 | delete | 48 | 5.125 | 0.563 | 0.207 |
| band_pdel_0005 | delete | 96 | 7.125 | 0.475 | 0.221 |
| band_pdel_0005 | delete | 192 | 8.812 | 0.693 | 0.270 |
| band_pdel_0005 | delete | 256 | 8.312 | 0.548 | 0.256 |
| band_zero_del | anchor | 48 | 6.000 | 0.481 | 0.233 |
| band_zero_del | anchor | 96 | 7.188 | 0.542 | 0.221 |
| band_zero_del | anchor | 192 | 9.000 | 0.579 | 0.242 |
| band_zero_del | anchor | 256 | 8.062 | 0.525 | 0.227 |
| bridge_00075_0000 | triad | 48 | 5.125 | 0.539 | 0.201 |
| bridge_00075_0000 | triad | 96 | 6.875 | 0.571 | 0.215 |
| bridge_00075_0000 | triad | 192 | 8.125 | 0.685 | 0.246 |
| bridge_00075_0000 | triad | 256 | 8.812 | 0.598 | 0.270 |
| bridge_0010_0000 | triad | 48 | 5.125 | 0.539 | 0.206 |
| bridge_0010_0000 | triad | 96 | 6.438 | 0.639 | 0.200 |
| bridge_0010_0000 | triad | 192 | 8.750 | 0.648 | 0.253 |
| bridge_0010_0000 | triad | 256 | 8.500 | 0.572 | 0.273 |

## Drift-rangering per regime

| regime | axis | metric | mean_rel_drift | q10 | q90 | top3_prob |
| --- | --- | --- | --- | --- | --- | --- |
| band_death_0005 | death | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_death_0005 | death | mean_abs_delta_beta1_rel | 0.0013 | 0.0000 | 0.0028 | 1.000 |
| band_death_0005 | death | mean_abs_delta_spectral_radius_rel | 0.0147 | 0.0118 | 0.0177 | 1.000 |
| band_death_0005 | death | mean_abs_delta_dim_proxy_rel | 0.0296 | 0.0250 | 0.0345 | 0.000 |
| band_death_0005 | death | mean_abs_delta_triangles_rel | 0.0602 | 0.0431 | 0.0775 | 0.000 |
| band_death_0005 | death | mean_abs_delta_tokens_rel | 0.4160 | 0.3042 | 0.5258 | 0.000 |
| band_death_0005 | death | mean_abs_delta_clustering_rel | 136453.0800 | 0.0578 | 276360.6104 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_nodes_rel | 0.0027 | 0.0018 | 0.0039 | 1.000 |
| band_pdel_0005 | delete | mean_abs_delta_spectral_radius_rel | 0.0207 | 0.0157 | 0.0248 | 1.000 |
| band_pdel_0005 | delete | mean_abs_delta_beta1_rel | 0.0533 | 0.0367 | 0.0692 | 0.562 |
| band_pdel_0005 | delete | mean_abs_delta_dim_proxy_rel | 0.0558 | 0.0432 | 0.0681 | 0.331 |
| band_pdel_0005 | delete | mean_abs_delta_triangles_rel | 0.0704 | 0.0574 | 0.0834 | 0.106 |
| band_pdel_0005 | delete | mean_abs_delta_clustering_rel | 0.0982 | 0.0807 | 0.1152 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_tokens_rel | 0.4847 | 0.3048 | 0.6593 | 0.000 |
| band_zero_del | anchor | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | anchor | mean_abs_delta_beta1_rel | 0.0014 | 0.0000 | 0.0028 | 1.000 |
| band_zero_del | anchor | mean_abs_delta_spectral_radius_rel | 0.0172 | 0.0138 | 0.0208 | 1.000 |
| band_zero_del | anchor | mean_abs_delta_dim_proxy_rel | 0.0367 | 0.0296 | 0.0426 | 0.000 |
| band_zero_del | anchor | mean_abs_delta_triangles_rel | 0.0602 | 0.0440 | 0.0781 | 0.000 |
| band_zero_del | anchor | mean_abs_delta_clustering_rel | 0.0739 | 0.0553 | 0.0930 | 0.000 |
| band_zero_del | anchor | mean_abs_delta_tokens_rel | 0.4873 | 0.3627 | 0.6341 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00075_0000 | triad | mean_abs_delta_beta1_rel | 0.0088 | 0.0065 | 0.0117 | 1.000 |
| bridge_00075_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0178 | 0.0145 | 0.0207 | 1.000 |
| bridge_00075_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0332 | 0.0281 | 0.0375 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_triangles_rel | 0.0802 | 0.0639 | 0.0973 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_clustering_rel | 0.0846 | 0.0678 | 0.1022 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_tokens_rel | 0.3889 | 0.2629 | 0.5169 | 0.000 |
| bridge_0010_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0010_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0208 | 0.0159 | 0.0260 | 1.000 |
| bridge_0010_0000 | triad | mean_abs_delta_beta1_rel | 0.0293 | 0.0129 | 0.0451 | 0.675 |
| bridge_0010_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0334 | 0.0287 | 0.0376 | 0.325 |
| bridge_0010_0000 | triad | mean_abs_delta_triangles_rel | 0.0948 | 0.0636 | 0.1250 | 0.000 |
| bridge_0010_0000 | triad | mean_abs_delta_tokens_rel | 0.4434 | 0.3252 | 0.5553 | 0.000 |
| bridge_0010_0000 | triad | mean_abs_delta_clustering_rel | 306665.1230 | 0.0831 | 617187.5824 | 0.000 |

## Off-anchor mot anker

| regime | axis | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| band_death_0005 | death | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| band_death_0005 | death | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| band_death_0005 | death | mean_abs_delta_triangles_rel | 0.0011 | -0.0792 | 0.0641 | 0.312 | 0.250 |
| band_death_0005 | death | mean_abs_delta_spectral_radius_rel | -0.0025 | -0.0195 | 0.0103 | 0.562 | 0.000 |
| band_death_0005 | death | mean_abs_delta_dim_proxy_rel | -0.0066 | -0.0435 | 0.0122 | 0.500 | 0.000 |
| band_death_0005 | death | mean_abs_delta_tokens_rel | -0.0765 | -0.4187 | 0.1288 | 0.375 | 0.000 |
| band_death_0005 | death | mean_abs_delta_clustering_rel | 138180.2589 | -0.0627 | 0.0900 | 0.250 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_tokens_rel | -0.0005 | -0.3601 | 0.2656 | 0.438 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_nodes_rel | 0.0026 | 0.0000 | 0.0065 | 0.750 | 0.250 |
| band_pdel_0005 | delete | mean_abs_delta_spectral_radius_rel | 0.0038 | -0.0128 | 0.0249 | 0.688 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_triangles_rel | 0.0126 | -0.0663 | 0.0966 | 0.500 | 0.188 |
| band_pdel_0005 | delete | mean_abs_delta_dim_proxy_rel | 0.0194 | -0.0398 | 0.0795 | 0.688 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_clustering_rel | 0.0247 | -0.0622 | 0.0999 | 0.688 | 0.062 |
| band_pdel_0005 | delete | mean_abs_delta_beta1_rel | 0.0510 | 0.0000 | 0.1250 | 0.750 | 0.250 |
| bridge_00075_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00075_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0006 | -0.0097 | 0.0076 | 0.688 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_dim_proxy_rel | -0.0030 | -0.0441 | 0.0270 | 0.625 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_beta1_rel | 0.0074 | 0.0000 | 0.0159 | 0.438 | 0.562 |
| bridge_00075_0000 | triad | mean_abs_delta_clustering_rel | 0.0119 | -0.0675 | 0.0903 | 0.625 | 0.062 |
| bridge_00075_0000 | triad | mean_abs_delta_triangles_rel | 0.0213 | -0.0326 | 0.0859 | 0.562 | 0.125 |
| bridge_00075_0000 | triad | mean_abs_delta_tokens_rel | -0.0978 | -0.3014 | 0.0833 | 0.188 | 0.062 |
| bridge_0010_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0010_0000 | triad | mean_abs_delta_dim_proxy_rel | -0.0033 | -0.0306 | 0.0133 | 0.438 | 0.000 |
| bridge_0010_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0039 | -0.0114 | 0.0153 | 0.562 | 0.000 |
| bridge_0010_0000 | triad | mean_abs_delta_beta1_rel | 0.0278 | 0.0000 | 0.0326 | 0.562 | 0.438 |
| bridge_0010_0000 | triad | mean_abs_delta_triangles_rel | 0.0356 | -0.0793 | 0.1151 | 0.500 | 0.188 |
| bridge_0010_0000 | triad | mean_abs_delta_tokens_rel | -0.0557 | -0.3542 | 0.2569 | 0.312 | 0.062 |
| bridge_0010_0000 | triad | mean_abs_delta_clustering_rel | 308593.7592 | -0.0503 | 0.1147 | 0.562 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| exact_zero_drifts | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | De eksakte null-driftene bryter når vi forlater ankerregimet, og bør derfor leses som regime-/koblingsartefakter. |
| spectral_quasi_invariant | promote | mean_abs_delta_spectral_radius_rel | Den relative spektraldriften holder seg lav og top-3 gjennom hele den lokale regimefamilien. |
| larger_validation_set | yes_targeted | spectral_quasi_invariant_cross_regime | Et større valideringssett er mest naturlig for spektral quasi-invariant-testing, ikke for nye basis/workflow-runder. |

## Tolkning

- Dette er en dynamikk-/robusthetrunde, ikke en ny frontier-konkurranse.
- Hvis null-driftene holder også off-anchor, blir de mer interessante, men fortsatt ikke automatisk til ny matematikk uten forklaring.
- Hvis den relative spektraldriften holder seg lav og top-3 off-anchor, er det vår sterkeste ikke-trivielle quasi-invariant-kandidat så langt.

