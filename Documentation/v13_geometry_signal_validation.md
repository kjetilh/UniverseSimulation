# Relasjonell universgraf v0.13: validering av geometri- og invariantsignaler

## Formål

Denne runden tar et steg tilbake fra workflow-policyene og spør hvor robuste de underliggende geometri- og quasi-invariantsignalene faktisk er. Målet er å avgjøre om et større valideringssett sannsynligvis vil gi ny informasjon, eller bare mer støy rundt svake effekter.

## Startstørrelser

| target | mean_initial | q10 | q90 | separated_from_prev | mean_dim_proxy |
| --- | --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 | 2.023 |
| 96 | 96.0 | 96.0 | 96.0 | 1 | 2.413 |
| 192 | 192.0 | 192.0 | 192.0 | 1 | 2.611 |
| 256 | 256.0 | 256.0 | 256.0 | 1 | 2.455 |

## 1. Geometrisk stabilitet

| rank | feature | mean_cv | q10_cv | q90_cv | slope_q10 | slope_q90 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | initial_avg_degree | 0.022 | 0.017 | 0.027 | 0.008 | 0.078 |
| 2 | initial_spectral_per_sqrtN | 0.051 | 0.033 | 0.066 | -0.143 | -0.100 |
| 3 | initial_dim_proxy | 0.080 | 0.064 | 0.097 | 0.211 | 0.378 |
| 4 | initial_beta1_per_node | 0.188 | 0.148 | 0.229 | -0.006 | 0.029 |
| 5 | initial_clustering | 0.197 | 0.156 | 0.237 | -0.015 | 0.014 |
| 6 | initial_triangles_per_node | 0.221 | 0.169 | 0.278 | 0.004 | 0.037 |

## 2. Quasi-invariant-kandidater

| rank | metric | mean_rel_drift | q10 | q90 | top1_prob | top3_prob |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 | 1.000 |
| 2 | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| 3 | mean_abs_delta_spectral_radius_rel | 0.0138 | 0.0114 | 0.0159 | 0.000 | 1.000 |
| 4 | mean_abs_delta_dim_proxy_rel | 0.0281 | 0.0246 | 0.0318 | 0.000 | 0.000 |
| 5 | mean_abs_delta_triangles_rel | 0.0593 | 0.0472 | 0.0720 | 0.000 | 0.000 |
| 6 | mean_abs_delta_clustering_rel | 0.0670 | 0.0536 | 0.0811 | 0.000 | 0.000 |
| 7 | mean_abs_delta_tokens_rel | 0.4287 | 0.3295 | 0.5359 | 0.000 | 0.000 |

## 3. Redusert basis: split-validering

| target_metric | basis | mean_skill | q10_skill | q90_skill | positive_rate | pairwise_within | spearman | top_rank_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mean_avg_local_overlap | spectral_only | -0.045 | -0.178 | 0.022 | 0.386 | 0.546 | -0.113 | 0.250 |
| mean_avg_local_overlap | avg_degree_only | -0.047 | -0.199 | 0.066 | 0.507 | 0.631 | 0.183 | 0.557 |
| mean_avg_local_overlap | spectral_plus_clustering | -0.125 | -0.316 | 0.017 | 0.214 | 0.530 | -0.094 | 0.057 |
| mean_avg_local_overlap | dim_only | -0.147 | -0.353 | -0.004 | 0.050 | 0.371 | -0.300 | 0.093 |
| mean_avg_local_overlap | spectral_plus_dim | -0.201 | -0.534 | 0.010 | 0.136 | 0.427 | -0.238 | 0.043 |
| mean_avg_local_overlap | full_basis | -0.570 | -1.177 | -0.130 | 0.007 | 0.448 | -0.173 | 0.000 |
| mean_final_radius_control | spectral_only | 0.149 | -0.131 | 0.317 | 0.829 | 0.507 | 0.543 | 0.379 |
| mean_final_radius_control | spectral_plus_clustering | 0.097 | -0.154 | 0.306 | 0.807 | 0.585 | 0.470 | 0.407 |
| mean_final_radius_control | spectral_plus_dim | 0.055 | -0.203 | 0.250 | 0.693 | 0.460 | 0.397 | 0.043 |
| mean_final_radius_control | dim_only | -0.046 | -0.192 | 0.069 | 0.493 | 0.488 | 0.164 | 0.071 |
| mean_final_radius_control | avg_degree_only | -0.093 | -0.231 | -0.000 | 0.100 | 0.480 | -0.285 | 0.100 |
| mean_final_radius_control | full_basis | -0.290 | -0.687 | 0.055 | 0.157 | 0.445 | 0.078 | 0.000 |

## 4. Pairwise basis-sammenligning

| target_metric | basis_a | basis_b | p_a_beats_b_by_skill | p_a_beats_b_by_pairwise | mean_skill_margin |
| --- | --- | --- | --- | --- | --- |
| mean_final_radius_control | avg_degree_only | spectral_only | 0.129 | 0.454 | -0.242 |
| mean_final_radius_control | avg_degree_only | dim_only | 0.264 | 0.511 | -0.047 |
| mean_final_radius_control | avg_degree_only | spectral_plus_dim | 0.243 | 0.518 | -0.148 |
| mean_final_radius_control | avg_degree_only | spectral_plus_clustering | 0.143 | 0.375 | -0.190 |
| mean_final_radius_control | avg_degree_only | full_basis | 0.721 | 0.554 | 0.197 |
| mean_final_radius_control | spectral_only | dim_only | 0.893 | 0.521 | 0.195 |
| mean_final_radius_control | spectral_only | spectral_plus_dim | 0.921 | 0.571 | 0.094 |
| mean_final_radius_control | spectral_only | spectral_plus_clustering | 0.536 | 0.396 | 0.053 |
| mean_final_radius_control | spectral_only | full_basis | 0.993 | 0.596 | 0.440 |
| mean_final_radius_control | dim_only | spectral_plus_dim | 0.264 | 0.525 | -0.101 |
| mean_final_radius_control | dim_only | spectral_plus_clustering | 0.150 | 0.371 | -0.142 |
| mean_final_radius_control | dim_only | full_basis | 0.771 | 0.543 | 0.245 |
| mean_final_radius_control | spectral_plus_dim | spectral_plus_clustering | 0.364 | 0.343 | -0.042 |
| mean_final_radius_control | spectral_plus_dim | full_basis | 0.929 | 0.496 | 0.346 |
| mean_final_radius_control | spectral_plus_clustering | full_basis | 0.979 | 0.671 | 0.387 |
| mean_avg_local_overlap | avg_degree_only | spectral_only | 0.607 | 0.639 | -0.001 |
| mean_avg_local_overlap | avg_degree_only | dim_only | 0.771 | 0.793 | 0.100 |
| mean_avg_local_overlap | avg_degree_only | spectral_plus_dim | 0.807 | 0.746 | 0.155 |
| mean_avg_local_overlap | avg_degree_only | spectral_plus_clustering | 0.807 | 0.646 | 0.078 |
| mean_avg_local_overlap | avg_degree_only | full_basis | 1.000 | 0.757 | 0.523 |
| mean_avg_local_overlap | spectral_only | dim_only | 0.793 | 0.704 | 0.102 |
| mean_avg_local_overlap | spectral_only | spectral_plus_dim | 0.836 | 0.693 | 0.156 |
| mean_avg_local_overlap | spectral_only | spectral_plus_clustering | 0.693 | 0.500 | 0.079 |
| mean_avg_local_overlap | spectral_only | full_basis | 0.950 | 0.618 | 0.525 |
| mean_avg_local_overlap | dim_only | spectral_plus_dim | 0.607 | 0.421 | 0.054 |
| mean_avg_local_overlap | dim_only | spectral_plus_clustering | 0.414 | 0.300 | -0.022 |
| mean_avg_local_overlap | dim_only | full_basis | 0.950 | 0.429 | 0.423 |
| mean_avg_local_overlap | spectral_plus_dim | spectral_plus_clustering | 0.364 | 0.329 | -0.077 |
| mean_avg_local_overlap | spectral_plus_dim | full_basis | 0.879 | 0.464 | 0.369 |
| mean_avg_local_overlap | spectral_plus_clustering | full_basis | 0.914 | 0.604 | 0.445 |

## 5. Repo-lojal tolkning

- Algebraiske identiteter er fortsatt ikke hovedpoenget her. Denne runden handler om normalisert geometri, langsom drift og prediktiv kompresjon.
- Generatorsporet holdes separat via target summary. Dersom startstørrelsene ikke hadde vært rent separert, ville tolkningen under vært mye svakere.
- `mean_abs_delta_nodes_rel` og `mean_abs_delta_beta1_rel` kan se svært sterke ut, men bør fortsatt behandles som mulige regime-/koblingsartefakter til de er testet bedre på tvers av nærliggende regimer.
- Den viktige beslutningen i denne runden er ikke om én liten basis 'vinner alt', men om radius-/geometrisignalet er ekte nok til å fortjene et større valideringssett.

## 6. Anbefaling om større valideringssett

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| radius_basis | not_yet | spectral_only | Radius-signalet er for svakt eller for ustabilt til at større validering er førsteprioritet. |
| overlap_basis | not_yet | spectral_only | Overlap-signalet er fortsatt for svakt til å forsvare større validering. |
| stable_geometry_features | yes_targeted | initial_avg_degree+initial_spectral_per_sqrtN | De mest stabile normaliserte geometriaksene er sterke nok til å brukes som faste kontroller i større validering. |
| quasi_invariants | cross_regime_first | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel+mean_abs_delta_spectral_radius_rel | Null- eller nesten-null-drift ser interessant ut, men bør testes på tvers av nærliggende regimer før større validering. |

