# Relasjonell universgraf v0.13n: test av nedre drop-kant

## Formål

Denne runden følger etter `v13m` og tester bare om `bridge_000822265625_0000` er en ekte nedre drop-kant mellom den renere lower-finen og resten av den lokale upper-zonen.

## Startstørrelser

| target | mean_initial | q10 | q90 | separated_from_prev |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Stabile kontrollakser

| rank | feature | mean_cv | q90_cv |
| --- | --- | --- | --- |
| 1 | initial_avg_degree | 0.028 | 0.033 |
| 2 | initial_spectral_per_sqrtN | 0.074 | 0.090 |
| 3 | initial_dim_proxy | 0.086 | 0.104 |

## Regimeutfall per størrelse

| regime | axis | target | radius | overlap | fit_speed |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | anchor | 48 | 4.560 | 0.605 | 0.182 |
| band_zero_del | anchor | 96 | 5.480 | 0.695 | 0.178 |
| band_zero_del | anchor | 192 | 7.560 | 0.535 | 0.235 |
| band_zero_del | anchor | 256 | 7.800 | 0.645 | 0.255 |
| bridge_0008203125_0000 | triad | 48 | 4.800 | 0.672 | 0.230 |
| bridge_0008203125_0000 | triad | 96 | 5.480 | 0.690 | 0.187 |
| bridge_0008203125_0000 | triad | 192 | 7.160 | 0.632 | 0.241 |
| bridge_0008203125_0000 | triad | 256 | 8.920 | 0.580 | 0.298 |
| bridge_0008212890625_0000 | triad | 48 | 4.520 | 0.661 | 0.205 |
| bridge_0008212890625_0000 | triad | 96 | 6.120 | 0.627 | 0.204 |
| bridge_0008212890625_0000 | triad | 192 | 7.800 | 0.544 | 0.251 |
| bridge_0008212890625_0000 | triad | 256 | 8.200 | 0.623 | 0.269 |
| bridge_000822265625_0000 | triad | 48 | 4.280 | 0.623 | 0.176 |
| bridge_000822265625_0000 | triad | 96 | 6.280 | 0.614 | 0.206 |
| bridge_000822265625_0000 | triad | 192 | 7.760 | 0.521 | 0.243 |
| bridge_000822265625_0000 | triad | 256 | 8.120 | 0.669 | 0.272 |
| bridge_0008232421875_0000 | triad | 48 | 4.960 | 0.569 | 0.193 |
| bridge_0008232421875_0000 | triad | 96 | 6.240 | 0.619 | 0.198 |
| bridge_0008232421875_0000 | triad | 192 | 7.040 | 0.591 | 0.213 |
| bridge_0008232421875_0000 | triad | 256 | 7.720 | 0.677 | 0.251 |
| bridge_00082421875_0000 | triad | 48 | 4.560 | 0.582 | 0.183 |
| bridge_00082421875_0000 | triad | 96 | 6.840 | 0.622 | 0.226 |
| bridge_00082421875_0000 | triad | 192 | 7.800 | 0.523 | 0.250 |
| bridge_00082421875_0000 | triad | 256 | 7.760 | 0.539 | 0.252 |

## Drop-kant-sammendrag

| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | spectral_top3_prob | local_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0008203125_0000 | 0.0145 | 0.0400 | 0.900 | 0.0255 | -0.0003 | 1.000 | sharp_local |
| bridge_0008212890625_0000 | 0.0154 | 0.0294 | 0.850 | 0.0147 | 0.0007 | 1.000 | good_but_local |
| bridge_000822265625_0000 | 0.0163 | 0.0315 | 0.700 | 0.0149 | 0.0015 | 0.996 | mixed |
| bridge_0008232421875_0000 | 0.0203 | 0.0331 | 0.700 | 0.0127 | 0.0056 | 1.000 | mixed |
| bridge_00082421875_0000 | 0.0189 | 0.0293 | 0.650 | 0.0104 | 0.0041 | 1.000 | mixed |

## Drop-kant-diagnose

| center | immediate_mean_p | p_drop_vs_immediate | margin_drop_vs_immediate | delta_worsening_vs_immediate | spectral_worsening_vs_immediate | break_status |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_000822265625_0000 | 0.775 | 0.0750 | -0.0012 | -0.0016 | -0.0015 | sampling_ambiguous |

## Fokusdrift per regime

| regime | metric | mean_rel_drift | q10 | q90 | top2_prob |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_spectral_radius_rel | 0.0148 | 0.0127 | 0.0171 | 0.000 |
| band_zero_del | mean_abs_delta_dim_proxy_rel | 0.0305 | 0.0251 | 0.0357 | 0.000 |
| bridge_0008203125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008203125_0000 | mean_abs_delta_beta1_rel | 0.0110 | 0.0081 | 0.0148 | 0.864 |
| bridge_0008203125_0000 | mean_abs_delta_spectral_radius_rel | 0.0145 | 0.0118 | 0.0172 | 0.136 |
| bridge_0008203125_0000 | mean_abs_delta_dim_proxy_rel | 0.0400 | 0.0329 | 0.0476 | 0.000 |
| bridge_0008212890625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008212890625_0000 | mean_abs_delta_beta1_rel | 0.0148 | 0.0104 | 0.0200 | 0.561 |
| bridge_0008212890625_0000 | mean_abs_delta_spectral_radius_rel | 0.0154 | 0.0129 | 0.0181 | 0.439 |
| bridge_0008212890625_0000 | mean_abs_delta_dim_proxy_rel | 0.0294 | 0.0236 | 0.0346 | 0.000 |
| bridge_000822265625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000822265625_0000 | mean_abs_delta_spectral_radius_rel | 0.0163 | 0.0139 | 0.0188 | 0.786 |
| bridge_000822265625_0000 | mean_abs_delta_beta1_rel | 0.0204 | 0.0132 | 0.0281 | 0.211 |
| bridge_000822265625_0000 | mean_abs_delta_dim_proxy_rel | 0.0315 | 0.0248 | 0.0384 | 0.004 |
| bridge_0008232421875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008232421875_0000 | mean_abs_delta_spectral_radius_rel | 0.0203 | 0.0163 | 0.0245 | 0.589 |
| bridge_0008232421875_0000 | mean_abs_delta_beta1_rel | 0.0208 | 0.0153 | 0.0268 | 0.411 |
| bridge_0008232421875_0000 | mean_abs_delta_dim_proxy_rel | 0.0331 | 0.0283 | 0.0377 | 0.000 |
| bridge_00082421875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00082421875_0000 | mean_abs_delta_spectral_radius_rel | 0.0189 | 0.0153 | 0.0231 | 0.857 |
| bridge_00082421875_0000 | mean_abs_delta_beta1_rel | 0.0264 | 0.0177 | 0.0359 | 0.143 |
| bridge_00082421875_0000 | mean_abs_delta_dim_proxy_rel | 0.0293 | 0.0244 | 0.0346 | 0.000 |

## Spektral mot dim

| regime | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- |
| band_zero_del | 0.850 | 0.0157 | -0.0025 | 0.0455 |
| bridge_0008203125_0000 | 0.900 | 0.0255 | 0.0019 | 0.0657 |
| bridge_0008212890625_0000 | 0.850 | 0.0147 | -0.0028 | 0.0515 |
| bridge_000822265625_0000 | 0.700 | 0.0149 | -0.0054 | 0.0616 |
| bridge_0008232421875_0000 | 0.700 | 0.0127 | -0.0049 | 0.0331 |
| bridge_00082421875_0000 | 0.650 | 0.0104 | -0.0047 | 0.0477 |

## Off-anchor mot anker

| regime | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_0008203125_0000 | mean_abs_delta_beta1_rel | 0.0110 | 0.0000 | 0.0197 | 0.600 | 0.400 |
| bridge_0008212890625_0000 | mean_abs_delta_beta1_rel | 0.0148 | 0.0000 | 0.0410 | 0.650 | 0.350 |
| bridge_000822265625_0000 | mean_abs_delta_beta1_rel | 0.0204 | 0.0000 | 0.0680 | 0.700 | 0.300 |
| bridge_0008232421875_0000 | mean_abs_delta_beta1_rel | 0.0208 | 0.0000 | 0.0456 | 0.700 | 0.300 |
| bridge_00082421875_0000 | mean_abs_delta_beta1_rel | 0.0259 | 0.0000 | 0.0671 | 0.700 | 0.300 |
| bridge_0008212890625_0000 | mean_abs_delta_dim_proxy_rel | -0.0003 | -0.0258 | 0.0266 | 0.400 | 0.000 |
| bridge_000822265625_0000 | mean_abs_delta_dim_proxy_rel | 0.0007 | -0.0259 | 0.0341 | 0.450 | 0.000 |
| bridge_00082421875_0000 | mean_abs_delta_dim_proxy_rel | -0.0012 | -0.0298 | 0.0289 | 0.550 | 0.000 |
| bridge_0008232421875_0000 | mean_abs_delta_dim_proxy_rel | 0.0027 | -0.0132 | 0.0198 | 0.450 | 0.000 |
| bridge_0008203125_0000 | mean_abs_delta_dim_proxy_rel | 0.0095 | -0.0189 | 0.0499 | 0.600 | 0.000 |
| bridge_0008203125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008212890625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000822265625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008232421875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00082421875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008203125_0000 | mean_abs_delta_spectral_radius_rel | -0.0003 | -0.0111 | 0.0125 | 0.400 | 0.000 |
| bridge_0008212890625_0000 | mean_abs_delta_spectral_radius_rel | 0.0007 | -0.0070 | 0.0082 | 0.400 | 0.000 |
| bridge_000822265625_0000 | mean_abs_delta_spectral_radius_rel | 0.0015 | -0.0090 | 0.0097 | 0.650 | 0.000 |
| bridge_00082421875_0000 | mean_abs_delta_spectral_radius_rel | 0.0041 | -0.0084 | 0.0167 | 0.550 | 0.000 |
| bridge_0008232421875_0000 | mean_abs_delta_spectral_radius_rel | 0.0056 | -0.0084 | 0.0214 | 0.650 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Den smale lower-drop-runden bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov. |
| spectral_quasi_invariant | mixed | mean_abs_delta_spectral_radius_rel | Drop-kanten er fortsatt ikke ren nok til å kalle spektralsporet målrettet validert. |
| larger_validation_set | not_yet | spectral_vs_dim_lower_drop_edge | Vent med bredere validering til den nedre drop-kanten er bedre avklart. |

## Tolkning

- Dette er ikke en ny scan. Det er en smal test av den nedre drop-kanten rundt `bridge_000822265625_0000`.
- Hvis drop-kanten holder, vet vi at usikkerheten i `v13m` faktisk sitter i den nedre delen av drop-sonen og ikke i hele området.
- Hvis den ikke holder, ser området mer ut som et smalt lokalt plateau enn som en reell knekk.
