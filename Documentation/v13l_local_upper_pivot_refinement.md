# Relasjonell universgraf v0.13l: lokal raffinering av upper-pivot

## Formål

Denne runden følger etter `v13k` og tester bare om `bridge_0008203125_0000` er et ekte lokalt pivotpunkt når vi bracketter det finere på begge sider.

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
| bridge_0008125_0000 | triad | 48 | 3.760 | 0.700 | 0.154 |
| bridge_0008125_0000 | triad | 96 | 6.360 | 0.631 | 0.209 |
| bridge_0008125_0000 | triad | 192 | 7.720 | 0.581 | 0.255 |
| bridge_0008125_0000 | triad | 256 | 7.720 | 0.659 | 0.251 |
| bridge_00081640625_0000 | triad | 48 | 5.280 | 0.524 | 0.241 |
| bridge_00081640625_0000 | triad | 96 | 4.960 | 0.694 | 0.165 |
| bridge_00081640625_0000 | triad | 192 | 6.960 | 0.591 | 0.222 |
| bridge_00081640625_0000 | triad | 256 | 8.320 | 0.624 | 0.253 |
| bridge_0008203125_0000 | triad | 48 | 4.800 | 0.672 | 0.230 |
| bridge_0008203125_0000 | triad | 96 | 5.480 | 0.690 | 0.187 |
| bridge_0008203125_0000 | triad | 192 | 7.160 | 0.632 | 0.241 |
| bridge_0008203125_0000 | triad | 256 | 8.920 | 0.580 | 0.298 |
| bridge_00082421875_0000 | triad | 48 | 4.560 | 0.582 | 0.183 |
| bridge_00082421875_0000 | triad | 96 | 6.840 | 0.622 | 0.226 |
| bridge_00082421875_0000 | triad | 192 | 7.800 | 0.523 | 0.250 |
| bridge_00082421875_0000 | triad | 256 | 7.760 | 0.539 | 0.252 |
| bridge_000828125_0000 | triad | 48 | 4.640 | 0.564 | 0.211 |
| bridge_000828125_0000 | triad | 96 | 6.560 | 0.615 | 0.218 |
| bridge_000828125_0000 | triad | 192 | 7.440 | 0.557 | 0.246 |
| bridge_000828125_0000 | triad | 256 | 7.760 | 0.617 | 0.241 |

## Pivot-sammendrag

| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | spectral_top3_prob | local_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0008125_0000 | 0.0137 | 0.0318 | 0.850 | 0.0180 | -0.0010 | 1.000 | sharp_local |
| bridge_00081640625_0000 | 0.0136 | 0.0312 | 0.950 | 0.0171 | -0.0013 | 1.000 | sharp_local |
| bridge_0008203125_0000 | 0.0146 | 0.0405 | 0.900 | 0.0255 | -0.0003 | 1.000 | sharp_local |
| bridge_00082421875_0000 | 0.0187 | 0.0291 | 0.650 | 0.0104 | 0.0041 | 1.000 | mixed |
| bridge_000828125_0000 | 0.0168 | 0.0351 | 0.850 | 0.0182 | 0.0021 | 1.000 | sharp_local |

## Pivot-diagnose

| center | immediate_mean_p | p_gain_vs_immediate | margin_gain_vs_immediate | delta_improvement_vs_immediate | spectral_improvement_vs_immediate | pivot_status |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_0008203125_0000 | 0.800 | 0.1000 | 0.0117 | 0.0017 | 0.0015 | sampling_ambiguous |

## Fokusdrift per regime

| regime | metric | mean_rel_drift | q10 | q90 | top2_prob |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_spectral_radius_rel | 0.0148 | 0.0127 | 0.0171 | 0.000 |
| band_zero_del | mean_abs_delta_dim_proxy_rel | 0.0305 | 0.0251 | 0.0357 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0126 | 0.0086 | 0.0164 | 0.632 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | 0.0137 | 0.0114 | 0.0163 | 0.368 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | 0.0318 | 0.0265 | 0.0368 | 0.000 |
| bridge_00081640625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00081640625_0000 | mean_abs_delta_spectral_radius_rel | 0.0136 | 0.0113 | 0.0161 | 0.589 |
| bridge_00081640625_0000 | mean_abs_delta_beta1_rel | 0.0145 | 0.0101 | 0.0191 | 0.411 |
| bridge_00081640625_0000 | mean_abs_delta_dim_proxy_rel | 0.0312 | 0.0264 | 0.0359 | 0.000 |
| bridge_0008203125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008203125_0000 | mean_abs_delta_beta1_rel | 0.0110 | 0.0080 | 0.0146 | 0.829 |
| bridge_0008203125_0000 | mean_abs_delta_spectral_radius_rel | 0.0146 | 0.0122 | 0.0169 | 0.171 |
| bridge_0008203125_0000 | mean_abs_delta_dim_proxy_rel | 0.0405 | 0.0343 | 0.0470 | 0.000 |
| bridge_00082421875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00082421875_0000 | mean_abs_delta_spectral_radius_rel | 0.0187 | 0.0152 | 0.0225 | 0.864 |
| bridge_00082421875_0000 | mean_abs_delta_beta1_rel | 0.0261 | 0.0177 | 0.0347 | 0.136 |
| bridge_00082421875_0000 | mean_abs_delta_dim_proxy_rel | 0.0291 | 0.0234 | 0.0344 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_spectral_radius_rel | 0.0168 | 0.0145 | 0.0192 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_beta1_rel | 0.0297 | 0.0236 | 0.0358 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_dim_proxy_rel | 0.0351 | 0.0289 | 0.0410 | 0.000 |

## Spektral mot dim

| regime | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- |
| band_zero_del | 0.850 | 0.0157 | -0.0025 | 0.0455 |
| bridge_0008125_0000 | 0.850 | 0.0180 | -0.0049 | 0.0374 |
| bridge_00081640625_0000 | 0.950 | 0.0171 | 0.0027 | 0.0346 |
| bridge_0008203125_0000 | 0.900 | 0.0255 | 0.0019 | 0.0657 |
| bridge_00082421875_0000 | 0.650 | 0.0104 | -0.0047 | 0.0477 |
| bridge_000828125_0000 | 0.850 | 0.0182 | -0.0030 | 0.0528 |

## Off-anchor mot anker

| regime | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_0008203125_0000 | mean_abs_delta_beta1_rel | 0.0110 | 0.0000 | 0.0197 | 0.600 | 0.400 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0125 | 0.0000 | 0.0297 | 0.550 | 0.450 |
| bridge_00081640625_0000 | mean_abs_delta_beta1_rel | 0.0146 | 0.0000 | 0.0340 | 0.650 | 0.350 |
| bridge_00082421875_0000 | mean_abs_delta_beta1_rel | 0.0259 | 0.0000 | 0.0671 | 0.700 | 0.300 |
| bridge_000828125_0000 | mean_abs_delta_beta1_rel | 0.0292 | 0.0049 | 0.0680 | 0.900 | 0.100 |
| bridge_00081640625_0000 | mean_abs_delta_dim_proxy_rel | 0.0001 | -0.0298 | 0.0345 | 0.550 | 0.000 |
| bridge_00082421875_0000 | mean_abs_delta_dim_proxy_rel | -0.0012 | -0.0298 | 0.0289 | 0.550 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | 0.0013 | -0.0243 | 0.0230 | 0.400 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_dim_proxy_rel | 0.0046 | -0.0292 | 0.0358 | 0.600 | 0.000 |
| bridge_0008203125_0000 | mean_abs_delta_dim_proxy_rel | 0.0095 | -0.0189 | 0.0499 | 0.600 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00081640625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008203125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00082421875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008203125_0000 | mean_abs_delta_spectral_radius_rel | -0.0003 | -0.0111 | 0.0125 | 0.400 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | -0.0010 | -0.0154 | 0.0143 | 0.450 | 0.000 |
| bridge_00081640625_0000 | mean_abs_delta_spectral_radius_rel | -0.0013 | -0.0125 | 0.0115 | 0.400 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_spectral_radius_rel | 0.0021 | -0.0079 | 0.0136 | 0.550 | 0.000 |
| bridge_00082421875_0000 | mean_abs_delta_spectral_radius_rel | 0.0041 | -0.0084 | 0.0167 | 0.550 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Den smale upper-pivot-runden bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov. |
| spectral_quasi_invariant | mixed | mean_abs_delta_spectral_radius_rel | Pivot-området er fortsatt ikke rent nok til å kalle spektralsporet målrettet validert. |
| larger_validation_set | not_yet | spectral_vs_dim_upper_pivot_refinement | Vent med bredere validering til pivot-området er bedre avklart. |

## Tolkning

- Dette er ikke en ny scan. Det er en lokal pivot-test rundt `bridge_0008203125_0000`.
- Hvis pivoten holder, vet vi at upper-bandet fra `v13j` og `v13k` egentlig samler seg rundt ett tydelig punkt.
- Hvis den ikke holder, er området fortsatt lovende, men blandet.

