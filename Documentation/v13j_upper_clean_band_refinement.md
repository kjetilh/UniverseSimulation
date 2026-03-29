# Relasjonell universgraf v0.13j: raffinering av rent oversideband

## Formål

Denne runden følger etter `v13i` og tester om den reneste delen av oversiden faktisk er et lite sammenhengende band mellom `bridge_0008125_0000` og `bridge_000828125_0000`, eller om også dette bare var en lokal fluktuasjon.

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
| bridge_0008203125_0000 | triad | 48 | 4.800 | 0.672 | 0.230 |
| bridge_0008203125_0000 | triad | 96 | 5.480 | 0.690 | 0.187 |
| bridge_0008203125_0000 | triad | 192 | 7.160 | 0.632 | 0.241 |
| bridge_0008203125_0000 | triad | 256 | 8.920 | 0.580 | 0.298 |
| bridge_000828125_0000 | triad | 48 | 4.640 | 0.564 | 0.211 |
| bridge_000828125_0000 | triad | 96 | 6.560 | 0.615 | 0.218 |
| bridge_000828125_0000 | triad | 192 | 7.440 | 0.557 | 0.246 |
| bridge_000828125_0000 | triad | 256 | 7.760 | 0.617 | 0.241 |
| bridge_0008359375_0000 | triad | 48 | 4.480 | 0.609 | 0.199 |
| bridge_0008359375_0000 | triad | 96 | 6.320 | 0.637 | 0.211 |
| bridge_0008359375_0000 | triad | 192 | 7.280 | 0.582 | 0.232 |
| bridge_0008359375_0000 | triad | 256 | 7.480 | 0.622 | 0.241 |
| bridge_00084375_0000 | triad | 48 | 4.640 | 0.642 | 0.181 |
| bridge_00084375_0000 | triad | 96 | 6.080 | 0.700 | 0.192 |
| bridge_00084375_0000 | triad | 192 | 7.480 | 0.565 | 0.226 |
| bridge_00084375_0000 | triad | 256 | 7.760 | 0.630 | 0.243 |

## Band-sammendrag

| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | spectral_top3_prob | local_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0008125_0000 | 0.0138 | 0.0320 | 0.850 | 0.0180 | -0.0010 | 1.000 | sharp_local |
| bridge_0008203125_0000 | 0.0144 | 0.0398 | 0.900 | 0.0255 | -0.0003 | 1.000 | sharp_local |
| bridge_000828125_0000 | 0.0169 | 0.0353 | 0.850 | 0.0182 | 0.0021 | 1.000 | sharp_local |
| bridge_0008359375_0000 | 0.0155 | 0.0319 | 0.750 | 0.0166 | 0.0008 | 1.000 | good_but_local |
| bridge_00084375_0000 | 0.0178 | 0.0295 | 0.750 | 0.0116 | 0.0030 | 1.000 | good_but_local |

## Band-diagnose

| band_mean_p | control_mean_p | p_gain_vs_controls | margin_gain_vs_controls | delta_improvement_vs_controls | spectral_improvement_vs_controls | band_status |
| --- | --- | --- | --- | --- | --- | --- |
| 0.867 | 0.750 | 0.1167 | 0.0064 | 0.0016 | 0.0017 | clean_band_supported |

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
| bridge_0008203125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008203125_0000 | mean_abs_delta_beta1_rel | 0.0108 | 0.0076 | 0.0144 | 0.869 |
| bridge_0008203125_0000 | mean_abs_delta_spectral_radius_rel | 0.0144 | 0.0118 | 0.0176 | 0.131 |
| bridge_0008203125_0000 | mean_abs_delta_dim_proxy_rel | 0.0398 | 0.0332 | 0.0472 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_spectral_radius_rel | 0.0169 | 0.0149 | 0.0188 | 0.996 |
| bridge_000828125_0000 | mean_abs_delta_beta1_rel | 0.0287 | 0.0225 | 0.0350 | 0.004 |
| bridge_000828125_0000 | mean_abs_delta_dim_proxy_rel | 0.0353 | 0.0295 | 0.0410 | 0.000 |
| bridge_0008359375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008359375_0000 | mean_abs_delta_spectral_radius_rel | 0.0155 | 0.0131 | 0.0178 | 0.996 |
| bridge_0008359375_0000 | mean_abs_delta_beta1_rel | 0.0268 | 0.0206 | 0.0331 | 0.004 |
| bridge_0008359375_0000 | mean_abs_delta_dim_proxy_rel | 0.0319 | 0.0263 | 0.0376 | 0.000 |
| bridge_00084375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00084375_0000 | mean_abs_delta_beta1_rel | 0.0155 | 0.0114 | 0.0193 | 0.812 |
| bridge_00084375_0000 | mean_abs_delta_spectral_radius_rel | 0.0178 | 0.0140 | 0.0215 | 0.188 |
| bridge_00084375_0000 | mean_abs_delta_dim_proxy_rel | 0.0295 | 0.0243 | 0.0355 | 0.000 |

## Spektral mot dim

| regime | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- |
| band_zero_del | 0.850 | 0.0157 | -0.0025 | 0.0455 |
| bridge_0008125_0000 | 0.850 | 0.0180 | -0.0049 | 0.0374 |
| bridge_0008203125_0000 | 0.900 | 0.0255 | 0.0019 | 0.0657 |
| bridge_000828125_0000 | 0.850 | 0.0182 | -0.0030 | 0.0528 |
| bridge_0008359375_0000 | 0.750 | 0.0166 | -0.0024 | 0.0483 |
| bridge_00084375_0000 | 0.750 | 0.0116 | -0.0126 | 0.0348 |

## Off-anchor mot anker

| regime | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_0008203125_0000 | mean_abs_delta_beta1_rel | 0.0110 | 0.0000 | 0.0197 | 0.600 | 0.400 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0125 | 0.0000 | 0.0297 | 0.550 | 0.450 |
| bridge_00084375_0000 | mean_abs_delta_beta1_rel | 0.0153 | 0.0000 | 0.0340 | 0.750 | 0.250 |
| bridge_0008359375_0000 | mean_abs_delta_beta1_rel | 0.0273 | 0.0000 | 0.0680 | 0.800 | 0.200 |
| bridge_000828125_0000 | mean_abs_delta_beta1_rel | 0.0292 | 0.0049 | 0.0680 | 0.900 | 0.100 |
| bridge_00084375_0000 | mean_abs_delta_dim_proxy_rel | -0.0011 | -0.0342 | 0.0202 | 0.450 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | 0.0013 | -0.0243 | 0.0230 | 0.400 | 0.000 |
| bridge_0008359375_0000 | mean_abs_delta_dim_proxy_rel | 0.0017 | -0.0234 | 0.0323 | 0.350 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_dim_proxy_rel | 0.0046 | -0.0292 | 0.0358 | 0.600 | 0.000 |
| bridge_0008203125_0000 | mean_abs_delta_dim_proxy_rel | 0.0095 | -0.0189 | 0.0499 | 0.600 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008203125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008359375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00084375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008203125_0000 | mean_abs_delta_spectral_radius_rel | -0.0003 | -0.0111 | 0.0125 | 0.400 | 0.000 |
| bridge_0008359375_0000 | mean_abs_delta_spectral_radius_rel | 0.0008 | -0.0072 | 0.0104 | 0.550 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | -0.0010 | -0.0154 | 0.0143 | 0.450 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_spectral_radius_rel | 0.0021 | -0.0079 | 0.0136 | 0.550 | 0.000 |
| bridge_00084375_0000 | mean_abs_delta_spectral_radius_rel | 0.0030 | -0.0111 | 0.0151 | 0.600 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Den smale upper-band-runden bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov. |
| spectral_quasi_invariant | good_but_local | mean_abs_delta_spectral_radius_rel | Det smale bandet mellom `bridge_0008125_0000` og `bridge_000828125_0000` holder som den reneste lokale triad-sonen, men sporet er fortsatt lokalt. |
| larger_validation_set | yes_targeted | spectral_vs_dim_upper_clean_band | Et lite målrettet valideringssett rundt dette bandet er nå rimelig. |

## Tolkning

- Denne runden spør bare om de reneste oversidepunktene faktisk danner et lite sammenhengende band.
- Hvis de gjør det, vet vi at upper-bandet er en ekte lokal struktur og ikke bare ett enkelt godt punkt.
- Hvis de ikke gjør det, skal også dette bandet leses som midlertidig lokal variasjon.

