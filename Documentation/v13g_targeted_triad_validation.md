# Relasjonell universgraf v0.13g: målrettet validering av renset triad-korridor

## Formål

Denne runden følger direkte etter `v13f`. Nå som notch-fortellingen rundt `bridge_00075_0000` er svekket, tester vi om den rensede triad-korridoren faktisk holder under litt større lokalt budsjett.

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
| 2 | initial_spectral_per_sqrtN | 0.053 | 0.061 |
| 3 | initial_dim_proxy | 0.095 | 0.108 |

## Regimeutfall per størrelse

| regime | axis | target | radius | overlap | fit_speed |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | anchor | 48 | 4.444 | 0.688 | 0.203 |
| band_zero_del | anchor | 96 | 6.333 | 0.581 | 0.218 |
| band_zero_del | anchor | 192 | 8.389 | 0.642 | 0.239 |
| band_zero_del | anchor | 256 | 7.889 | 0.689 | 0.264 |
| bridge_0006875_0000 | triad | 48 | 4.389 | 0.682 | 0.208 |
| bridge_0006875_0000 | triad | 96 | 6.028 | 0.594 | 0.188 |
| bridge_0006875_0000 | triad | 192 | 8.944 | 0.551 | 0.249 |
| bridge_0006875_0000 | triad | 256 | 8.250 | 0.663 | 0.256 |
| bridge_00075_0000 | triad | 48 | 4.528 | 0.600 | 0.204 |
| bridge_00075_0000 | triad | 96 | 6.028 | 0.603 | 0.209 |
| bridge_00075_0000 | triad | 192 | 8.917 | 0.555 | 0.258 |
| bridge_00075_0000 | triad | 256 | 8.694 | 0.534 | 0.283 |
| bridge_0008125_0000 | triad | 48 | 4.139 | 0.709 | 0.191 |
| bridge_0008125_0000 | triad | 96 | 6.111 | 0.613 | 0.203 |
| bridge_0008125_0000 | triad | 192 | 9.167 | 0.541 | 0.273 |
| bridge_0008125_0000 | triad | 256 | 8.194 | 0.622 | 0.265 |
| bridge_000875_0000 | triad | 48 | 4.111 | 0.748 | 0.208 |
| bridge_000875_0000 | triad | 96 | 6.722 | 0.575 | 0.223 |
| bridge_000875_0000 | triad | 192 | 8.528 | 0.614 | 0.242 |
| bridge_000875_0000 | triad | 256 | 7.806 | 0.724 | 0.257 |

## Målrettet triad-korridor

| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | spectral_top3_prob | corridor_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0006875_0000 | 0.0181 | 0.0316 | 0.750 | 0.0135 | 0.0002 | 1.000 | good_but_local |
| bridge_00075_0000 | 0.0182 | 0.0368 | 0.792 | 0.0189 | 0.0003 | 1.000 | good_but_local |
| bridge_0008125_0000 | 0.0179 | 0.0337 | 0.667 | 0.0153 | -0.0002 | 1.000 | mixed |
| bridge_000875_0000 | 0.0195 | 0.0282 | 0.667 | 0.0089 | 0.0015 | 0.982 | mixed |

## Fokusdrift per regime

| regime | metric | mean_rel_drift | q10 | q90 | top2_prob |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_spectral_radius_rel | 0.0177 | 0.0152 | 0.0202 | 0.000 |
| band_zero_del | mean_abs_delta_dim_proxy_rel | 0.0279 | 0.0230 | 0.0332 | 0.000 |
| bridge_0006875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0006875_0000 | mean_abs_delta_beta1_rel | 0.0112 | 0.0071 | 0.0157 | 0.918 |
| bridge_0006875_0000 | mean_abs_delta_spectral_radius_rel | 0.0181 | 0.0156 | 0.0205 | 0.082 |
| bridge_0006875_0000 | mean_abs_delta_dim_proxy_rel | 0.0316 | 0.0262 | 0.0375 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00075_0000 | mean_abs_delta_beta1_rel | 0.0137 | 0.0111 | 0.0165 | 0.989 |
| bridge_00075_0000 | mean_abs_delta_spectral_radius_rel | 0.0182 | 0.0156 | 0.0208 | 0.011 |
| bridge_00075_0000 | mean_abs_delta_dim_proxy_rel | 0.0368 | 0.0316 | 0.0419 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0126 | 0.0090 | 0.0166 | 0.921 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | 0.0179 | 0.0153 | 0.0206 | 0.079 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | 0.0337 | 0.0278 | 0.0393 | 0.000 |
| bridge_000875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_beta1_rel | 0.0117 | 0.0089 | 0.0149 | 0.993 |
| bridge_000875_0000 | mean_abs_delta_spectral_radius_rel | 0.0195 | 0.0171 | 0.0221 | 0.007 |
| bridge_000875_0000 | mean_abs_delta_dim_proxy_rel | 0.0282 | 0.0243 | 0.0323 | 0.000 |

## Spektral mot dim

| regime | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- |
| band_zero_del | 0.750 | 0.0100 | -0.0077 | 0.0340 |
| bridge_0006875_0000 | 0.750 | 0.0135 | -0.0044 | 0.0308 |
| bridge_00075_0000 | 0.792 | 0.0189 | -0.0097 | 0.0450 |
| bridge_0008125_0000 | 0.667 | 0.0153 | -0.0113 | 0.0476 |
| bridge_000875_0000 | 0.667 | 0.0089 | -0.0200 | 0.0317 |

## Off-anchor mot anker

| regime | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_0006875_0000 | mean_abs_delta_beta1_rel | 0.0114 | 0.0000 | 0.0269 | 0.625 | 0.375 |
| bridge_000875_0000 | mean_abs_delta_beta1_rel | 0.0117 | 0.0000 | 0.0295 | 0.625 | 0.375 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0126 | 0.0000 | 0.0269 | 0.708 | 0.292 |
| bridge_00075_0000 | mean_abs_delta_beta1_rel | 0.0136 | 0.0000 | 0.0278 | 0.708 | 0.292 |
| bridge_000875_0000 | mean_abs_delta_dim_proxy_rel | 0.0003 | -0.0186 | 0.0126 | 0.542 | 0.000 |
| bridge_0006875_0000 | mean_abs_delta_dim_proxy_rel | 0.0037 | -0.0195 | 0.0294 | 0.542 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | 0.0051 | -0.0144 | 0.0249 | 0.667 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_dim_proxy_rel | 0.0091 | -0.0134 | 0.0275 | 0.750 | 0.000 |
| bridge_0006875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00075_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | -0.0002 | -0.0162 | 0.0120 | 0.458 | 0.000 |
| bridge_0006875_0000 | mean_abs_delta_spectral_radius_rel | 0.0002 | -0.0092 | 0.0102 | 0.500 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_spectral_radius_rel | 0.0003 | -0.0135 | 0.0144 | 0.500 | 0.000 |
| bridge_000875_0000 | mean_abs_delta_spectral_radius_rel | 0.0015 | -0.0119 | 0.0164 | 0.500 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Targeted triad-valideringen bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov. |
| spectral_quasi_invariant | mixed | mean_abs_delta_spectral_radius_rel | Selv den rensede triad-korridoren er ikke ren nok til å kalle spektralsporet målrettet validert ennå. |
| larger_validation_set | not_yet | spectral_vs_dim_targeted_triad_corridor | Vent med bredere validering til triad-korridoren er skarpere. |

## Tolkning

- Denne runden bruker mer budsjett på den delen av triad-familien som faktisk overlevde `v13f`.
- Hvis spektralsporet holder her og `dim_proxy` fortsatt taper, har vi et sterkere grunnlag for en kontrollert neste utvidelse.
- Hvis korridoren fortsatt spriker her, skal signalet fortsatt leses som lokalt og ikke skaleres bredt ennå.

