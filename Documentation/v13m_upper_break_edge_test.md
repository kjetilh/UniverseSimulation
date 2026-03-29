# Relasjonell universgraf v0.13m: test av øvre bruddkant

## Formål

Denne runden følger etter `v13l` og tester bare om `bridge_00082421875_0000` er en ekte lokal bruddkant mellom en renere nedre del og en renere øvre del av upper-triad-familien.

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
| bridge_000822265625_0000 | triad | 48 | 4.280 | 0.623 | 0.176 |
| bridge_000822265625_0000 | triad | 96 | 6.280 | 0.614 | 0.206 |
| bridge_000822265625_0000 | triad | 192 | 7.760 | 0.521 | 0.243 |
| bridge_000822265625_0000 | triad | 256 | 8.120 | 0.669 | 0.272 |
| bridge_00082421875_0000 | triad | 48 | 4.560 | 0.582 | 0.183 |
| bridge_00082421875_0000 | triad | 96 | 6.840 | 0.622 | 0.226 |
| bridge_00082421875_0000 | triad | 192 | 7.800 | 0.523 | 0.250 |
| bridge_00082421875_0000 | triad | 256 | 7.760 | 0.539 | 0.252 |
| bridge_000826171875_0000 | triad | 48 | 4.640 | 0.679 | 0.224 |
| bridge_000826171875_0000 | triad | 96 | 5.640 | 0.650 | 0.178 |
| bridge_000826171875_0000 | triad | 192 | 8.120 | 0.532 | 0.254 |
| bridge_000826171875_0000 | triad | 256 | 7.640 | 0.691 | 0.249 |
| bridge_000828125_0000 | triad | 48 | 4.640 | 0.564 | 0.211 |
| bridge_000828125_0000 | triad | 96 | 6.560 | 0.615 | 0.218 |
| bridge_000828125_0000 | triad | 192 | 7.440 | 0.557 | 0.246 |
| bridge_000828125_0000 | triad | 256 | 7.760 | 0.617 | 0.241 |

## Bruddkant-sammendrag

| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | spectral_top3_prob | local_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0008203125_0000 | 0.0145 | 0.0400 | 0.900 | 0.0255 | -0.0003 | 1.000 | sharp_local |
| bridge_000822265625_0000 | 0.0163 | 0.0306 | 0.700 | 0.0149 | 0.0015 | 1.000 | mixed |
| bridge_00082421875_0000 | 0.0189 | 0.0291 | 0.650 | 0.0104 | 0.0041 | 1.000 | mixed |
| bridge_000826171875_0000 | 0.0150 | 0.0297 | 0.850 | 0.0151 | 0.0004 | 1.000 | sharp_local |
| bridge_000828125_0000 | 0.0168 | 0.0351 | 0.850 | 0.0182 | 0.0021 | 1.000 | sharp_local |

## Bruddkant-diagnose

| center | immediate_mean_p | p_drop_vs_immediate | margin_drop_vs_immediate | delta_worsening_vs_immediate | spectral_worsening_vs_immediate | break_status |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_00082421875_0000 | 0.775 | 0.1250 | 0.0046 | 0.0032 | 0.0033 | sampling_ambiguous |

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
| bridge_000822265625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000822265625_0000 | mean_abs_delta_spectral_radius_rel | 0.0163 | 0.0139 | 0.0188 | 0.846 |
| bridge_000822265625_0000 | mean_abs_delta_beta1_rel | 0.0209 | 0.0143 | 0.0282 | 0.154 |
| bridge_000822265625_0000 | mean_abs_delta_dim_proxy_rel | 0.0306 | 0.0242 | 0.0380 | 0.000 |
| bridge_00082421875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00082421875_0000 | mean_abs_delta_spectral_radius_rel | 0.0189 | 0.0151 | 0.0229 | 0.861 |
| bridge_00082421875_0000 | mean_abs_delta_beta1_rel | 0.0258 | 0.0171 | 0.0353 | 0.139 |
| bridge_00082421875_0000 | mean_abs_delta_dim_proxy_rel | 0.0291 | 0.0237 | 0.0342 | 0.000 |
| bridge_000826171875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000826171875_0000 | mean_abs_delta_beta1_rel | 0.0094 | 0.0052 | 0.0136 | 0.957 |
| bridge_000826171875_0000 | mean_abs_delta_spectral_radius_rel | 0.0150 | 0.0119 | 0.0180 | 0.043 |
| bridge_000826171875_0000 | mean_abs_delta_dim_proxy_rel | 0.0297 | 0.0241 | 0.0355 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_spectral_radius_rel | 0.0168 | 0.0145 | 0.0192 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_beta1_rel | 0.0297 | 0.0236 | 0.0358 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_dim_proxy_rel | 0.0351 | 0.0289 | 0.0410 | 0.000 |

## Spektral mot dim

| regime | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- |
| band_zero_del | 0.850 | 0.0157 | -0.0025 | 0.0455 |
| bridge_0008203125_0000 | 0.900 | 0.0255 | 0.0019 | 0.0657 |
| bridge_000822265625_0000 | 0.700 | 0.0149 | -0.0054 | 0.0616 |
| bridge_00082421875_0000 | 0.650 | 0.0104 | -0.0047 | 0.0477 |
| bridge_000826171875_0000 | 0.850 | 0.0151 | -0.0025 | 0.0337 |
| bridge_000828125_0000 | 0.850 | 0.0182 | -0.0030 | 0.0528 |

## Off-anchor mot anker

| regime | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_000826171875_0000 | mean_abs_delta_beta1_rel | 0.0096 | 0.0000 | 0.0235 | 0.450 | 0.550 |
| bridge_0008203125_0000 | mean_abs_delta_beta1_rel | 0.0110 | 0.0000 | 0.0197 | 0.600 | 0.400 |
| bridge_000822265625_0000 | mean_abs_delta_beta1_rel | 0.0204 | 0.0000 | 0.0680 | 0.700 | 0.300 |
| bridge_00082421875_0000 | mean_abs_delta_beta1_rel | 0.0259 | 0.0000 | 0.0671 | 0.700 | 0.300 |
| bridge_000828125_0000 | mean_abs_delta_beta1_rel | 0.0292 | 0.0049 | 0.0680 | 0.900 | 0.100 |
| bridge_000826171875_0000 | mean_abs_delta_dim_proxy_rel | -0.0003 | -0.0284 | 0.0219 | 0.350 | 0.000 |
| bridge_000822265625_0000 | mean_abs_delta_dim_proxy_rel | 0.0007 | -0.0259 | 0.0341 | 0.450 | 0.000 |
| bridge_00082421875_0000 | mean_abs_delta_dim_proxy_rel | -0.0012 | -0.0298 | 0.0289 | 0.550 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_dim_proxy_rel | 0.0046 | -0.0292 | 0.0358 | 0.600 | 0.000 |
| bridge_0008203125_0000 | mean_abs_delta_dim_proxy_rel | 0.0095 | -0.0189 | 0.0499 | 0.600 | 0.000 |
| bridge_0008203125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000822265625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00082421875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000826171875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008203125_0000 | mean_abs_delta_spectral_radius_rel | -0.0003 | -0.0111 | 0.0125 | 0.400 | 0.000 |
| bridge_000826171875_0000 | mean_abs_delta_spectral_radius_rel | 0.0004 | -0.0174 | 0.0108 | 0.600 | 0.000 |
| bridge_000822265625_0000 | mean_abs_delta_spectral_radius_rel | 0.0015 | -0.0090 | 0.0097 | 0.650 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_spectral_radius_rel | 0.0021 | -0.0079 | 0.0136 | 0.550 | 0.000 |
| bridge_00082421875_0000 | mean_abs_delta_spectral_radius_rel | 0.0041 | -0.0084 | 0.0167 | 0.550 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Den smale upper-break-runden bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov. |
| spectral_quasi_invariant | mixed | mean_abs_delta_spectral_radius_rel | Bruddkanten er fortsatt ikke ren nok til å kalle spektralsporet målrettet validert. |
| larger_validation_set | not_yet | spectral_vs_dim_upper_break_edge | Vent med bredere validering til den øvre bruddkanten er bedre avklart. |

## Tolkning

- Dette er ikke en ny scan. Det er en smal test av den øvre bruddkanten rundt `bridge_00082421875_0000`.
- Hvis bruddkanten holder, vet vi at usikkerheten i `v13l` faktisk sitter i en lokal overgang og ikke i hele området.
- Hvis den ikke holder, er den øvre delen renere enn `v13l` alene tilsa.

