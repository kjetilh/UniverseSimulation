# Relasjonell universgraf v0.12: geometri- og invariantlab rundt band_zero_del

## Formål

Denne runden fryser frontier midlertidig ved `band_zero_del` og tester om regimet eksponerer en liten geometrisk eller invariant-lignende basis som kan beskrive dynamikken enklere enn en bred frontier-scan.

## Startstorrelser

| target | mean_initial | q10 | q90 | separated_from_prev | mean_beta1 | mean_triangles | mean_dim_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 | 9.5 | 8.2 | 2.120 |
| 96 | 96.0 | 96.0 | 96.0 | 1 | 10.5 | 8.8 | 2.359 |
| 192 | 192.0 | 192.0 | 192.0 | 1 | 22.2 | 21.0 | 2.316 |
| 256 | 256.0 | 256.0 | 256.0 | 1 | 37.8 | 34.8 | 2.402 |

## Geometrisk stabilitet

| feature | mean_cv | max_cv | range | slope_vs_logN |
| --- | --- | --- | --- | --- |
| initial_beta1_per_node | 0.184 | 0.319 | 0.089 | -0.031 |
| initial_triangles_per_node | 0.194 | 0.357 | 0.081 | -0.021 |
| initial_spectral_per_sqrtN | 0.070 | 0.111 | 0.273 | -0.162 |
| initial_dim_proxy | 0.105 | 0.144 | 0.282 | 0.141 |
| initial_clustering | 0.255 | 0.357 | 0.073 | -0.025 |
| initial_avg_degree | 0.024 | 0.052 | 0.156 | -0.042 |

## Dynamiske utfall per størrelse

| target | overlap | radius | fit_speed | rel_drift_beta1 | rel_drift_triangles | rel_drift_dim |
| --- | --- | --- | --- | --- | --- | --- |
| 48 | 0.653 | 4.100 | 0.199 | 0.000 | 0.140 | 0.033 |
| 96 | 0.656 | 6.350 | 0.204 | 0.000 | 0.071 | 0.025 |
| 192 | 0.637 | 8.900 | 0.248 | 0.000 | 0.036 | 0.014 |
| 256 | 0.605 | 8.550 | 0.273 | 0.000 | 0.053 | 0.026 |

## Kandidater til quasi-invarianter

| rank | metric | mean_rel_drift | median_rel_drift | q10 | q90 |
| --- | --- | --- | --- | --- | --- |
| 1 | abs_delta_nodes_rel | 0.000 | 0.000 | 0.000 | 0.000 |
| 2 | abs_delta_beta1_rel | 0.000 | 0.000 | 0.000 | 0.000 |
| 3 | abs_delta_spectral_radius_rel | 0.012 | 0.007 | 0.000 | 0.030 |
| 4 | abs_delta_dim_proxy_rel | 0.025 | 0.018 | 0.002 | 0.062 |
| 5 | abs_delta_triangles_rel | 0.075 | 0.050 | 0.000 | 0.200 |
| 6 | abs_delta_clustering_rel | 0.076 | 0.054 | 0.002 | 0.185 |
| 7 | abs_delta_tokens_rel | 0.223 | 0.111 | 0.000 | 0.574 |

## Redusert basis som prediksjonsoppgave

| target_metric | subset_size | subset | cv_rmse | baseline_rmse | relative_skill |
| --- | --- | --- | --- | --- | --- |
| avg_local_overlap | 1 | initial_beta1_per_node | 0.2050 | 0.2052 | 0.001 |
| avg_local_overlap | 2 | initial_spectral_per_sqrtN+initial_clustering | 0.2056 | 0.2052 | -0.002 |
| avg_local_overlap | 5 | initial_beta1_per_node+initial_triangles_per_node+initial_spectral_per_sqrtN+initial_dim_proxy+initial_clustering | 0.2448 | 0.2052 | -0.193 |
| final_radius_control | 1 | initial_spectral_per_sqrtN | 2.9249 | 3.6269 | 0.194 |
| final_radius_control | 2 | initial_spectral_per_sqrtN+initial_clustering | 2.7542 | 3.6269 | 0.241 |
| final_radius_control | 5 | initial_beta1_per_node+initial_triangles_per_node+initial_spectral_per_sqrtN+initial_dim_proxy+initial_clustering | 4.1016 | 3.6269 | -0.131 |
| abs_delta_beta1_rel | 1 | initial_beta1_per_node | 0.0000 | 0.0000 | nan |
| abs_delta_beta1_rel | 2 | initial_beta1_per_node+initial_triangles_per_node | 0.0000 | 0.0000 | nan |
| abs_delta_beta1_rel | 5 | initial_beta1_per_node+initial_triangles_per_node+initial_spectral_per_sqrtN+initial_dim_proxy+initial_clustering | 0.0000 | 0.0000 | nan |

## Tolkning

- Algebraiske identiteter er ikke hovedpoenget i denne runden; vi ser etter langsom drift og prediktiv kompresjon.
- Generatorartefakter holdes separat via target summary; hvis størrelsene ikke separerer, kan ikke geometrilesningen tas seriøst.
- Hvis en liten basis av normaliserte geometrifeatures gir god skill på dynamiske mål, er det et første tegn på at regimet bærer en effektiv grov beskrivelse.
- Hvis quasi-invariant-kandidatene også er de samme størrelsene som er lettest å predikere, er det spesielt interessant for videre matematisk arbeid.

