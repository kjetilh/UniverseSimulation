# Relasjonell universgraf v0.13f: notch-test i triad-korridoren

## Formål

Denne runden holder modellen fast og gjør bare én ting: den tester om det blandede triadpunktet i `v13e` er et ekte lokalt hakk eller bare restusikkerhet etter for grov bracketing.

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
| 1 | initial_avg_degree | 0.017 | 0.021 |
| 2 | initial_spectral_per_sqrtN | 0.054 | 0.066 |
| 3 | initial_dim_proxy | 0.086 | 0.100 |

## Regimeutfall per størrelse

| regime | axis | target | radius | overlap | fit_speed |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | anchor | 48 | 4.960 | 0.556 | 0.209 |
| band_zero_del | anchor | 96 | 5.400 | 0.616 | 0.194 |
| band_zero_del | anchor | 192 | 7.880 | 0.592 | 0.232 |
| band_zero_del | anchor | 256 | 7.920 | 0.634 | 0.249 |
| bridge_000625_0000 | triad | 48 | 4.720 | 0.567 | 0.207 |
| bridge_000625_0000 | triad | 96 | 5.920 | 0.568 | 0.210 |
| bridge_000625_0000 | triad | 192 | 6.560 | 0.594 | 0.188 |
| bridge_000625_0000 | triad | 256 | 8.480 | 0.673 | 0.258 |
| bridge_0006875_0000 | triad | 48 | 4.240 | 0.614 | 0.165 |
| bridge_0006875_0000 | triad | 96 | 6.280 | 0.625 | 0.221 |
| bridge_0006875_0000 | triad | 192 | 8.000 | 0.597 | 0.229 |
| bridge_0006875_0000 | triad | 256 | 8.440 | 0.672 | 0.277 |
| bridge_00075_0000 | triad | 48 | 4.240 | 0.570 | 0.172 |
| bridge_00075_0000 | triad | 96 | 5.680 | 0.629 | 0.209 |
| bridge_00075_0000 | triad | 192 | 8.160 | 0.625 | 0.242 |
| bridge_00075_0000 | triad | 256 | 8.280 | 0.637 | 0.269 |
| bridge_0008125_0000 | triad | 48 | 4.280 | 0.540 | 0.178 |
| bridge_0008125_0000 | triad | 96 | 6.560 | 0.609 | 0.253 |
| bridge_0008125_0000 | triad | 192 | 8.400 | 0.568 | 0.247 |
| bridge_0008125_0000 | triad | 256 | 6.880 | 0.695 | 0.208 |
| bridge_000875_0000 | triad | 48 | 4.440 | 0.620 | 0.194 |
| bridge_000875_0000 | triad | 96 | 5.880 | 0.658 | 0.236 |
| bridge_000875_0000 | triad | 192 | 6.760 | 0.673 | 0.209 |
| bridge_000875_0000 | triad | 256 | 8.560 | 0.695 | 0.284 |

## Lokal triad-notch-summering

| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | local_status |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_000625_0000 | 0.0212 | 0.0311 | 0.650 | 0.0098 | 0.0046 | mixed |
| bridge_0006875_0000 | 0.0233 | 0.0346 | 0.750 | 0.0121 | 0.0064 | good_but_local |
| bridge_00075_0000 | 0.0176 | 0.0314 | 0.800 | 0.0141 | 0.0010 | sharp_local |
| bridge_0008125_0000 | 0.0183 | 0.0383 | 0.750 | 0.0201 | 0.0017 | good_but_local |
| bridge_000875_0000 | 0.0174 | 0.0319 | 0.850 | 0.0146 | 0.0011 | sharp_local |

## Notch-diagnose

| center | fine_neighbor_mean_p | edge_neighbor_mean_p | notch_depth_pairwise | notch_depth_margin | notch_depth_delta | notch_depth_spectral | notch_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_00075_0000 | 0.750 | 0.750 | -0.0500 | 0.0020 | -0.0031 | -0.0032 | notch_not_supported |

## Fokusdrift per regime

| regime | metric | mean_rel_drift | q10 | q90 | top2_prob |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_spectral_radius_rel | 0.0164 | 0.0123 | 0.0208 | 0.000 |
| band_zero_del | mean_abs_delta_dim_proxy_rel | 0.0302 | 0.0266 | 0.0334 | 0.000 |
| bridge_000625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000625_0000 | mean_abs_delta_beta1_rel | 0.0078 | 0.0050 | 0.0106 | 1.000 |
| bridge_000625_0000 | mean_abs_delta_spectral_radius_rel | 0.0212 | 0.0177 | 0.0245 | 0.000 |
| bridge_000625_0000 | mean_abs_delta_dim_proxy_rel | 0.0311 | 0.0261 | 0.0362 | 0.000 |
| bridge_0006875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0006875_0000 | mean_abs_delta_beta1_rel | 0.0164 | 0.0125 | 0.0207 | 0.977 |
| bridge_0006875_0000 | mean_abs_delta_spectral_radius_rel | 0.0233 | 0.0182 | 0.0279 | 0.023 |
| bridge_0006875_0000 | mean_abs_delta_dim_proxy_rel | 0.0346 | 0.0283 | 0.0411 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00075_0000 | mean_abs_delta_beta1_rel | 0.0122 | 0.0089 | 0.0160 | 1.000 |
| bridge_00075_0000 | mean_abs_delta_spectral_radius_rel | 0.0176 | 0.0158 | 0.0194 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_dim_proxy_rel | 0.0314 | 0.0253 | 0.0377 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0129 | 0.0089 | 0.0169 | 0.905 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | 0.0183 | 0.0153 | 0.0212 | 0.095 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | 0.0383 | 0.0338 | 0.0429 | 0.000 |
| bridge_000875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_beta1_rel | 0.0117 | 0.0088 | 0.0144 | 0.900 |
| bridge_000875_0000 | mean_abs_delta_spectral_radius_rel | 0.0174 | 0.0137 | 0.0216 | 0.100 |
| bridge_000875_0000 | mean_abs_delta_dim_proxy_rel | 0.0319 | 0.0255 | 0.0388 | 0.000 |

## Spektral mot dim

| regime | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- |
| band_zero_del | 0.850 | 0.0138 | -0.0016 | 0.0380 |
| bridge_000625_0000 | 0.650 | 0.0098 | -0.0062 | 0.0278 |
| bridge_0006875_0000 | 0.750 | 0.0121 | -0.0099 | 0.0460 |
| bridge_00075_0000 | 0.800 | 0.0141 | -0.0033 | 0.0382 |
| bridge_0008125_0000 | 0.750 | 0.0201 | -0.0120 | 0.0477 |
| bridge_000875_0000 | 0.850 | 0.0146 | -0.0026 | 0.0369 |

## Off-anchor mot anker

| regime | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_000625_0000 | mean_abs_delta_beta1_rel | 0.0081 | 0.0000 | 0.0233 | 0.550 | 0.450 |
| bridge_000875_0000 | mean_abs_delta_beta1_rel | 0.0116 | 0.0000 | 0.0251 | 0.750 | 0.250 |
| bridge_00075_0000 | mean_abs_delta_beta1_rel | 0.0120 | 0.0000 | 0.0273 | 0.600 | 0.400 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0133 | 0.0000 | 0.0250 | 0.650 | 0.350 |
| bridge_0006875_0000 | mean_abs_delta_beta1_rel | 0.0163 | 0.0000 | 0.0377 | 0.650 | 0.350 |
| bridge_000625_0000 | mean_abs_delta_dim_proxy_rel | 0.0006 | -0.0276 | 0.0208 | 0.500 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_dim_proxy_rel | 0.0013 | -0.0324 | 0.0349 | 0.550 | 0.000 |
| bridge_000875_0000 | mean_abs_delta_dim_proxy_rel | 0.0019 | -0.0243 | 0.0273 | 0.500 | 0.000 |
| bridge_0006875_0000 | mean_abs_delta_dim_proxy_rel | 0.0047 | -0.0240 | 0.0326 | 0.550 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | 0.0080 | -0.0232 | 0.0378 | 0.600 | 0.000 |
| bridge_000625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0006875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00075_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00075_0000 | mean_abs_delta_spectral_radius_rel | 0.0010 | -0.0175 | 0.0137 | 0.750 | 0.000 |
| bridge_000875_0000 | mean_abs_delta_spectral_radius_rel | 0.0011 | -0.0137 | 0.0189 | 0.500 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | 0.0017 | -0.0125 | 0.0188 | 0.650 | 0.000 |
| bridge_000625_0000 | mean_abs_delta_spectral_radius_rel | 0.0046 | -0.0080 | 0.0179 | 0.800 | 0.000 |
| bridge_0006875_0000 | mean_abs_delta_spectral_radius_rel | 0.0064 | 0.0007 | 0.0145 | 0.900 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Triad-notch-runden bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov. |
| spectral_quasi_invariant | good_but_local | mean_abs_delta_spectral_radius_rel | Det tidligere blandede punktet ser ikke lenger ut som et eget hakk; den smale triad-korridoren er lokalt renere. |
| larger_validation_set | yes_targeted | spectral_vs_dim_triad_notch | Den smale triad-korridoren er ren nok til en målrettet neste valideringsrunde. |

## Tolkning

- Denne runden prøver ikke å gjøre spektralsporet bredere, bare å avgjøre om hakket rundt `bridge_00075_0000` er reelt.
- Hvis hakket er reelt, betyr det at spektralsporet har mer lokal struktur enn `v13e` alene kunne vise.
- Hvis hakket flater ut, er triad-korridoren renere enn før og et bedre grunnlag for neste målrettede validering.

