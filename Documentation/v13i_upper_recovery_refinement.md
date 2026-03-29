# Relasjonell universgraf v0.13i: raffinering av gjenopprettet oversidepunkt

## Formål

Denne runden følger etter `v13h` og tester bare om det gjenopprettede oversidepunktet ved `bridge_00084375_0000` holder under finere bracketing, eller om det bare var en lokal fluktuasjon.

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
| 3 | initial_dim_proxy | 0.086 | 0.105 |

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
| bridge_000828125_0000 | triad | 48 | 4.640 | 0.564 | 0.211 |
| bridge_000828125_0000 | triad | 96 | 6.560 | 0.615 | 0.218 |
| bridge_000828125_0000 | triad | 192 | 7.440 | 0.557 | 0.246 |
| bridge_000828125_0000 | triad | 256 | 7.760 | 0.617 | 0.241 |
| bridge_00084375_0000 | triad | 48 | 4.640 | 0.642 | 0.181 |
| bridge_00084375_0000 | triad | 96 | 6.080 | 0.700 | 0.192 |
| bridge_00084375_0000 | triad | 192 | 7.480 | 0.565 | 0.226 |
| bridge_00084375_0000 | triad | 256 | 7.760 | 0.630 | 0.243 |
| bridge_000859375_0000 | triad | 48 | 4.440 | 0.627 | 0.186 |
| bridge_000859375_0000 | triad | 96 | 6.280 | 0.645 | 0.200 |
| bridge_000859375_0000 | triad | 192 | 7.760 | 0.600 | 0.247 |
| bridge_000859375_0000 | triad | 256 | 8.200 | 0.650 | 0.271 |
| bridge_000875_0000 | triad | 48 | 4.400 | 0.625 | 0.198 |
| bridge_000875_0000 | triad | 96 | 6.240 | 0.721 | 0.211 |
| bridge_000875_0000 | triad | 192 | 7.600 | 0.577 | 0.241 |
| bridge_000875_0000 | triad | 256 | 7.560 | 0.585 | 0.238 |

## Recovery-sammendrag

| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | spectral_top3_prob | local_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0008125_0000 | 0.0138 | 0.0320 | 0.850 | 0.0180 | -0.0010 | 1.000 | sharp_local |
| bridge_000828125_0000 | 0.0167 | 0.0353 | 0.850 | 0.0182 | 0.0021 | 1.000 | sharp_local |
| bridge_00084375_0000 | 0.0179 | 0.0296 | 0.750 | 0.0116 | 0.0030 | 1.000 | good_but_local |
| bridge_000859375_0000 | 0.0165 | 0.0312 | 0.750 | 0.0150 | 0.0017 | 1.000 | good_but_local |
| bridge_000875_0000 | 0.0147 | 0.0326 | 0.750 | 0.0180 | -0.0003 | 1.000 | good_but_local |

## Recovery-diagnose

| center | immediate_mean_p | p_gain_vs_immediate | margin_gain_vs_immediate | delta_improvement_vs_immediate | spectral_improvement_vs_immediate | recovery_status |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_00084375_0000 | 0.800 | -0.0500 | -0.0050 | -0.0011 | -0.0013 | recovery_not_supported |

## Fokusdrift per regime

| regime | metric | mean_rel_drift | q10 | q90 | top2_prob |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_spectral_radius_rel | 0.0148 | 0.0127 | 0.0172 | 0.000 |
| band_zero_del | mean_abs_delta_dim_proxy_rel | 0.0306 | 0.0250 | 0.0358 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0126 | 0.0085 | 0.0164 | 0.623 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | 0.0138 | 0.0114 | 0.0163 | 0.377 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | 0.0320 | 0.0266 | 0.0370 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_spectral_radius_rel | 0.0167 | 0.0145 | 0.0191 | 0.988 |
| bridge_000828125_0000 | mean_abs_delta_beta1_rel | 0.0293 | 0.0227 | 0.0359 | 0.012 |
| bridge_000828125_0000 | mean_abs_delta_dim_proxy_rel | 0.0353 | 0.0294 | 0.0410 | 0.000 |
| bridge_00084375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00084375_0000 | mean_abs_delta_beta1_rel | 0.0154 | 0.0118 | 0.0193 | 0.835 |
| bridge_00084375_0000 | mean_abs_delta_spectral_radius_rel | 0.0179 | 0.0141 | 0.0211 | 0.165 |
| bridge_00084375_0000 | mean_abs_delta_dim_proxy_rel | 0.0296 | 0.0235 | 0.0349 | 0.000 |
| bridge_000859375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000859375_0000 | mean_abs_delta_spectral_radius_rel | 0.0165 | 0.0138 | 0.0192 | 0.977 |
| bridge_000859375_0000 | mean_abs_delta_beta1_rel | 0.0289 | 0.0192 | 0.0393 | 0.023 |
| bridge_000859375_0000 | mean_abs_delta_dim_proxy_rel | 0.0312 | 0.0266 | 0.0364 | 0.000 |
| bridge_000875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_beta1_rel | 0.0101 | 0.0072 | 0.0129 | 0.981 |
| bridge_000875_0000 | mean_abs_delta_spectral_radius_rel | 0.0147 | 0.0109 | 0.0187 | 0.019 |
| bridge_000875_0000 | mean_abs_delta_dim_proxy_rel | 0.0326 | 0.0275 | 0.0381 | 0.000 |

## Spektral mot dim

| regime | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- |
| band_zero_del | 0.850 | 0.0157 | -0.0025 | 0.0455 |
| bridge_0008125_0000 | 0.850 | 0.0180 | -0.0049 | 0.0374 |
| bridge_000828125_0000 | 0.850 | 0.0182 | -0.0030 | 0.0528 |
| bridge_00084375_0000 | 0.750 | 0.0116 | -0.0126 | 0.0348 |
| bridge_000859375_0000 | 0.750 | 0.0150 | -0.0040 | 0.0434 |
| bridge_000875_0000 | 0.750 | 0.0180 | -0.0029 | 0.0529 |

## Off-anchor mot anker

| regime | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_000875_0000 | mean_abs_delta_beta1_rel | 0.0100 | 0.0000 | 0.0254 | 0.600 | 0.400 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0125 | 0.0000 | 0.0297 | 0.550 | 0.450 |
| bridge_00084375_0000 | mean_abs_delta_beta1_rel | 0.0153 | 0.0000 | 0.0340 | 0.750 | 0.250 |
| bridge_000828125_0000 | mean_abs_delta_beta1_rel | 0.0292 | 0.0049 | 0.0680 | 0.900 | 0.100 |
| bridge_000859375_0000 | mean_abs_delta_beta1_rel | 0.0297 | 0.0000 | 0.1020 | 0.800 | 0.200 |
| bridge_000859375_0000 | mean_abs_delta_dim_proxy_rel | 0.0011 | -0.0225 | 0.0262 | 0.400 | 0.000 |
| bridge_00084375_0000 | mean_abs_delta_dim_proxy_rel | -0.0011 | -0.0342 | 0.0202 | 0.450 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | 0.0013 | -0.0243 | 0.0230 | 0.400 | 0.000 |
| bridge_000875_0000 | mean_abs_delta_dim_proxy_rel | 0.0020 | -0.0217 | 0.0270 | 0.450 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_dim_proxy_rel | 0.0046 | -0.0292 | 0.0358 | 0.600 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00084375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000859375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_spectral_radius_rel | -0.0003 | -0.0133 | 0.0115 | 0.500 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | -0.0010 | -0.0154 | 0.0143 | 0.450 | 0.000 |
| bridge_000859375_0000 | mean_abs_delta_spectral_radius_rel | 0.0017 | -0.0058 | 0.0110 | 0.550 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_spectral_radius_rel | 0.0021 | -0.0079 | 0.0136 | 0.550 | 0.000 |
| bridge_00084375_0000 | mean_abs_delta_spectral_radius_rel | 0.0030 | -0.0111 | 0.0151 | 0.600 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Upper-recovery-runden bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov. |
| spectral_quasi_invariant | mixed | mean_abs_delta_spectral_radius_rel | Det gjenopprettede oversidepunktet holder ikke under finere bracketing; spektralsporet er fortsatt blandet her. |
| larger_validation_set | not_yet | spectral_vs_dim_upper_recovery_refinement | Vent med bredere validering til recovery-området er bedre forstått. |

## Tolkning

- Denne runden spør bare om det gjenopprettede punktet holder når vi ser enda nærmere på det.
- Hvis det holder, vet vi at oversiden har ekte lokal struktur, ikke bare støy.
- Hvis det ikke holder, skal recovery-punktet leses som en midlertidig lokal fluktuasjon.

