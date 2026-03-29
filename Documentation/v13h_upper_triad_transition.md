# Relasjonell universgraf v0.13h: overside-overgang i triad-korridoren

## Formål

Denne runden følger direkte etter `v13g` og zoomer bare inn på oversiden av triad-korridoren. Målet er å finne ut om den øvre delen degraderes systematisk, eller om det finnes et lokalt gjenopprettet punkt der også.

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
| 1 | initial_avg_degree | 0.022 | 0.026 |
| 2 | initial_spectral_per_sqrtN | 0.045 | 0.054 |
| 3 | initial_dim_proxy | 0.074 | 0.090 |

## Regimeutfall per størrelse

| regime | axis | target | radius | overlap | fit_speed |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | anchor | 48 | 4.920 | 0.598 | 0.195 |
| band_zero_del | anchor | 96 | 5.800 | 0.635 | 0.205 |
| band_zero_del | anchor | 192 | 7.400 | 0.590 | 0.228 |
| band_zero_del | anchor | 256 | 7.600 | 0.672 | 0.219 |
| bridge_00075_0000 | triad | 48 | 4.640 | 0.648 | 0.184 |
| bridge_00075_0000 | triad | 96 | 6.760 | 0.603 | 0.237 |
| bridge_00075_0000 | triad | 192 | 7.600 | 0.596 | 0.244 |
| bridge_00075_0000 | triad | 256 | 9.040 | 0.627 | 0.291 |
| bridge_00078125_0000 | triad | 48 | 4.400 | 0.597 | 0.172 |
| bridge_00078125_0000 | triad | 96 | 6.040 | 0.578 | 0.194 |
| bridge_00078125_0000 | triad | 192 | 7.600 | 0.543 | 0.217 |
| bridge_00078125_0000 | triad | 256 | 8.200 | 0.661 | 0.256 |
| bridge_0008125_0000 | triad | 48 | 4.560 | 0.559 | 0.188 |
| bridge_0008125_0000 | triad | 96 | 6.040 | 0.673 | 0.215 |
| bridge_0008125_0000 | triad | 192 | 7.480 | 0.591 | 0.222 |
| bridge_0008125_0000 | triad | 256 | 9.040 | 0.698 | 0.284 |
| bridge_00084375_0000 | triad | 48 | 4.560 | 0.580 | 0.183 |
| bridge_00084375_0000 | triad | 96 | 5.160 | 0.650 | 0.205 |
| bridge_00084375_0000 | triad | 192 | 7.000 | 0.608 | 0.215 |
| bridge_00084375_0000 | triad | 256 | 7.920 | 0.665 | 0.248 |
| bridge_000875_0000 | triad | 48 | 4.480 | 0.592 | 0.185 |
| bridge_000875_0000 | triad | 96 | 6.040 | 0.599 | 0.213 |
| bridge_000875_0000 | triad | 192 | 6.920 | 0.656 | 0.209 |
| bridge_000875_0000 | triad | 256 | 8.160 | 0.690 | 0.269 |

## Overside-sammendrag

| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | spectral_top3_prob | local_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_00075_0000 | 0.0186 | 0.0390 | 0.750 | 0.0204 | 0.0028 | 1.000 | good_but_local |
| bridge_00078125_0000 | 0.0186 | 0.0358 | 0.700 | 0.0171 | 0.0026 | 1.000 | mixed |
| bridge_0008125_0000 | 0.0186 | 0.0296 | 0.650 | 0.0109 | 0.0028 | 1.000 | mixed |
| bridge_00084375_0000 | 0.0179 | 0.0355 | 0.800 | 0.0174 | 0.0018 | 1.000 | sharp_local |
| bridge_000875_0000 | 0.0164 | 0.0370 | 0.750 | 0.0209 | 0.0005 | 1.000 | good_but_local |

## Overgangsdiagnose

| center | upper_mean_p | center_gap_to_upper_mean | center_margin_gap | upper_delta_penalty | monotone_degrade | transition_status |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_00075_0000 | 0.725 | 0.0250 | 0.0038 | -0.0008 | 0 | upper_recovery_exists |

## Fokusdrift per regime

| regime | metric | mean_rel_drift | q10 | q90 | top2_prob |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_spectral_radius_rel | 0.0159 | 0.0131 | 0.0183 | 0.000 |
| band_zero_del | mean_abs_delta_dim_proxy_rel | 0.0375 | 0.0317 | 0.0441 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00075_0000 | mean_abs_delta_beta1_rel | 0.0144 | 0.0094 | 0.0200 | 0.804 |
| bridge_00075_0000 | mean_abs_delta_spectral_radius_rel | 0.0186 | 0.0154 | 0.0214 | 0.196 |
| bridge_00075_0000 | mean_abs_delta_dim_proxy_rel | 0.0390 | 0.0322 | 0.0453 | 0.000 |
| bridge_00078125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00078125_0000 | mean_abs_delta_spectral_radius_rel | 0.0186 | 0.0149 | 0.0219 | 0.554 |
| bridge_00078125_0000 | mean_abs_delta_beta1_rel | 0.0195 | 0.0121 | 0.0276 | 0.446 |
| bridge_00078125_0000 | mean_abs_delta_dim_proxy_rel | 0.0358 | 0.0284 | 0.0430 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0126 | 0.0091 | 0.0160 | 0.954 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | 0.0186 | 0.0156 | 0.0214 | 0.046 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | 0.0296 | 0.0262 | 0.0336 | 0.000 |
| bridge_00084375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00084375_0000 | mean_abs_delta_beta1_rel | 0.0125 | 0.0090 | 0.0163 | 0.925 |
| bridge_00084375_0000 | mean_abs_delta_spectral_radius_rel | 0.0179 | 0.0155 | 0.0202 | 0.075 |
| bridge_00084375_0000 | mean_abs_delta_dim_proxy_rel | 0.0355 | 0.0300 | 0.0404 | 0.000 |
| bridge_000875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_beta1_rel | 0.0158 | 0.0109 | 0.0211 | 0.562 |
| bridge_000875_0000 | mean_abs_delta_spectral_radius_rel | 0.0164 | 0.0132 | 0.0198 | 0.438 |
| bridge_000875_0000 | mean_abs_delta_dim_proxy_rel | 0.0370 | 0.0322 | 0.0421 | 0.000 |

## Spektral mot dim

| regime | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- |
| band_zero_del | 0.800 | 0.0214 | -0.0109 | 0.0459 |
| bridge_00075_0000 | 0.750 | 0.0204 | -0.0062 | 0.0486 |
| bridge_00078125_0000 | 0.700 | 0.0171 | -0.0113 | 0.0514 |
| bridge_0008125_0000 | 0.650 | 0.0109 | -0.0074 | 0.0395 |
| bridge_00084375_0000 | 0.800 | 0.0174 | -0.0059 | 0.0475 |
| bridge_000875_0000 | 0.750 | 0.0209 | -0.0067 | 0.0434 |

## Off-anchor mot anker

| regime | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0125 | 0.0000 | 0.0294 | 0.700 | 0.300 |
| bridge_00084375_0000 | mean_abs_delta_beta1_rel | 0.0127 | 0.0000 | 0.0307 | 0.650 | 0.350 |
| bridge_00075_0000 | mean_abs_delta_beta1_rel | 0.0144 | 0.0000 | 0.0344 | 0.700 | 0.300 |
| bridge_000875_0000 | mean_abs_delta_beta1_rel | 0.0158 | 0.0000 | 0.0302 | 0.750 | 0.250 |
| bridge_00078125_0000 | mean_abs_delta_beta1_rel | 0.0191 | 0.0000 | 0.0417 | 0.650 | 0.350 |
| bridge_000875_0000 | mean_abs_delta_dim_proxy_rel | 0.0001 | -0.0225 | 0.0284 | 0.550 | 0.000 |
| bridge_00078125_0000 | mean_abs_delta_dim_proxy_rel | -0.0017 | -0.0262 | 0.0249 | 0.500 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_dim_proxy_rel | 0.0018 | -0.0194 | 0.0450 | 0.550 | 0.000 |
| bridge_00084375_0000 | mean_abs_delta_dim_proxy_rel | -0.0021 | -0.0336 | 0.0331 | 0.550 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | -0.0077 | -0.0345 | 0.0262 | 0.300 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00078125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00084375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_spectral_radius_rel | 0.0005 | -0.0132 | 0.0097 | 0.500 | 0.000 |
| bridge_00084375_0000 | mean_abs_delta_spectral_radius_rel | 0.0018 | -0.0087 | 0.0166 | 0.550 | 0.000 |
| bridge_00078125_0000 | mean_abs_delta_spectral_radius_rel | 0.0026 | -0.0070 | 0.0164 | 0.600 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_spectral_radius_rel | 0.0028 | -0.0045 | 0.0101 | 0.700 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | 0.0028 | -0.0076 | 0.0127 | 0.550 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Upper-triad-runden bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov. |
| spectral_quasi_invariant | mixed | mean_abs_delta_spectral_radius_rel | Oversiden av triad-korridoren er fortsatt ikke ren nok til å kalle spektralsporet målrettet validert. |
| larger_validation_set | not_yet | spectral_vs_dim_upper_triad_transition | Vent med bredere validering til oversiden er bedre avklart. |

## Tolkning

- Denne runden spør ikke om hele korridoren er validert. Den spør bare hva slags overgang oversiden faktisk har.
- Hvis oversiden degraderes systematisk, har vi lært hvor spektralsporet faktisk slutter å være rent.
- Hvis et oversidepunkt gjenoppretter signalet, bør neste steg gå enda smalere akkurat der.

