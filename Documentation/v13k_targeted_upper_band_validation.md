# Relasjonell universgraf v0.13k: målrettet validering av rent oversideband

## Formål

Denne runden følger etter `v13j` og gjør ikke et nytt søk. Den bruker bare et litt større lokalt budsjett for å teste om upper-bandet mellom `bridge_0008125_0000` og `bridge_000828125_0000` fortsatt holder når vi måler det hardere.

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
| 1 | initial_avg_degree | 0.026 | 0.031 |
| 2 | initial_spectral_per_sqrtN | 0.078 | 0.091 |
| 3 | initial_dim_proxy | 0.090 | 0.107 |

## Regimeutfall per størrelse

| regime | axis | target | radius | overlap | fit_speed |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | anchor | 48 | 4.806 | 0.595 | 0.192 |
| band_zero_del | anchor | 96 | 6.083 | 0.653 | 0.200 |
| band_zero_del | anchor | 192 | 7.611 | 0.500 | 0.230 |
| band_zero_del | anchor | 256 | 7.806 | 0.623 | 0.258 |
| bridge_0008125_0000 | triad | 48 | 4.083 | 0.675 | 0.167 |
| bridge_0008125_0000 | triad | 96 | 5.944 | 0.644 | 0.199 |
| bridge_0008125_0000 | triad | 192 | 7.417 | 0.593 | 0.239 |
| bridge_0008125_0000 | triad | 256 | 7.611 | 0.671 | 0.245 |
| bridge_0008203125_0000 | triad | 48 | 4.917 | 0.628 | 0.223 |
| bridge_0008203125_0000 | triad | 96 | 5.750 | 0.679 | 0.188 |
| bridge_0008203125_0000 | triad | 192 | 6.944 | 0.640 | 0.224 |
| bridge_0008203125_0000 | triad | 256 | 8.861 | 0.586 | 0.291 |
| bridge_000828125_0000 | triad | 48 | 4.583 | 0.582 | 0.205 |
| bridge_000828125_0000 | triad | 96 | 6.444 | 0.634 | 0.222 |
| bridge_000828125_0000 | triad | 192 | 7.194 | 0.576 | 0.228 |
| bridge_000828125_0000 | triad | 256 | 7.639 | 0.675 | 0.241 |
| bridge_0008359375_0000 | triad | 48 | 4.472 | 0.645 | 0.192 |
| bridge_0008359375_0000 | triad | 96 | 6.028 | 0.654 | 0.201 |
| bridge_0008359375_0000 | triad | 192 | 6.889 | 0.629 | 0.217 |
| bridge_0008359375_0000 | triad | 256 | 7.361 | 0.652 | 0.234 |
| bridge_00084375_0000 | triad | 48 | 4.972 | 0.605 | 0.198 |
| bridge_00084375_0000 | triad | 96 | 6.306 | 0.663 | 0.198 |
| bridge_00084375_0000 | triad | 192 | 7.250 | 0.562 | 0.219 |
| bridge_00084375_0000 | triad | 256 | 8.111 | 0.594 | 0.258 |

## Band-sammendrag

| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | spectral_top3_prob | local_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0008125_0000 | 0.0148 | 0.0288 | 0.792 | 0.0143 | -0.0017 | 1.000 | good_but_local |
| bridge_0008203125_0000 | 0.0153 | 0.0405 | 0.917 | 0.0251 | -0.0011 | 1.000 | sharp_local |
| bridge_000828125_0000 | 0.0165 | 0.0308 | 0.750 | 0.0142 | 0.0000 | 1.000 | good_but_local |
| bridge_0008359375_0000 | 0.0155 | 0.0302 | 0.750 | 0.0147 | -0.0010 | 1.000 | good_but_local |
| bridge_00084375_0000 | 0.0185 | 0.0324 | 0.792 | 0.0139 | 0.0020 | 1.000 | good_but_local |

## Band-diagnose

| band_mean_p | control_mean_p | p_gain_vs_controls | margin_gain_vs_controls | delta_improvement_vs_controls | spectral_improvement_vs_controls | band_status |
| --- | --- | --- | --- | --- | --- | --- |
| 0.819 | 0.771 | 0.0486 | 0.0036 | 0.0014 | 0.0014 | sampling_ambiguous |

## Fokusdrift per regime

| regime | metric | mean_rel_drift | q10 | q90 | top2_prob |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_spectral_radius_rel | 0.0166 | 0.0142 | 0.0193 | 0.000 |
| band_zero_del | mean_abs_delta_dim_proxy_rel | 0.0300 | 0.0264 | 0.0338 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | 0.0148 | 0.0122 | 0.0176 | 0.653 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0165 | 0.0113 | 0.0223 | 0.347 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | 0.0288 | 0.0241 | 0.0335 | 0.000 |
| bridge_0008203125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008203125_0000 | mean_abs_delta_spectral_radius_rel | 0.0153 | 0.0130 | 0.0178 | 0.853 |
| bridge_0008203125_0000 | mean_abs_delta_beta1_rel | 0.0187 | 0.0141 | 0.0233 | 0.147 |
| bridge_0008203125_0000 | mean_abs_delta_dim_proxy_rel | 0.0405 | 0.0345 | 0.0461 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_spectral_radius_rel | 0.0165 | 0.0144 | 0.0184 | 0.956 |
| bridge_000828125_0000 | mean_abs_delta_beta1_rel | 0.0252 | 0.0187 | 0.0315 | 0.044 |
| bridge_000828125_0000 | mean_abs_delta_dim_proxy_rel | 0.0308 | 0.0260 | 0.0358 | 0.000 |
| bridge_0008359375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0008359375_0000 | mean_abs_delta_spectral_radius_rel | 0.0155 | 0.0132 | 0.0178 | 0.900 |
| bridge_0008359375_0000 | mean_abs_delta_beta1_rel | 0.0208 | 0.0159 | 0.0260 | 0.100 |
| bridge_0008359375_0000 | mean_abs_delta_dim_proxy_rel | 0.0302 | 0.0255 | 0.0349 | 0.000 |
| bridge_00084375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00084375_0000 | mean_abs_delta_beta1_rel | 0.0162 | 0.0122 | 0.0200 | 0.853 |
| bridge_00084375_0000 | mean_abs_delta_spectral_radius_rel | 0.0185 | 0.0155 | 0.0217 | 0.147 |
| bridge_00084375_0000 | mean_abs_delta_dim_proxy_rel | 0.0324 | 0.0268 | 0.0380 | 0.000 |

## Spektral mot dim

| regime | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- |
| band_zero_del | 0.875 | 0.0136 | -0.0007 | 0.0354 |
| bridge_0008125_0000 | 0.792 | 0.0143 | -0.0042 | 0.0358 |
| bridge_0008203125_0000 | 0.917 | 0.0251 | 0.0007 | 0.0580 |
| bridge_000828125_0000 | 0.750 | 0.0142 | -0.0033 | 0.0460 |
| bridge_0008359375_0000 | 0.750 | 0.0147 | -0.0057 | 0.0433 |
| bridge_00084375_0000 | 0.792 | 0.0139 | -0.0027 | 0.0349 |

## Off-anchor mot anker

| regime | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_00084375_0000 | mean_abs_delta_beta1_rel | 0.0162 | 0.0000 | 0.0317 | 0.833 | 0.167 |
| bridge_0008125_0000 | mean_abs_delta_beta1_rel | 0.0166 | 0.0000 | 0.0399 | 0.625 | 0.375 |
| bridge_0008203125_0000 | mean_abs_delta_beta1_rel | 0.0186 | 0.0000 | 0.0403 | 0.750 | 0.250 |
| bridge_0008359375_0000 | mean_abs_delta_beta1_rel | 0.0208 | 0.0000 | 0.0556 | 0.708 | 0.292 |
| bridge_000828125_0000 | mean_abs_delta_beta1_rel | 0.0250 | 0.0000 | 0.0750 | 0.792 | 0.208 |
| bridge_0008359375_0000 | mean_abs_delta_dim_proxy_rel | 0.0001 | -0.0246 | 0.0253 | 0.417 | 0.000 |
| bridge_000828125_0000 | mean_abs_delta_dim_proxy_rel | 0.0007 | -0.0256 | 0.0236 | 0.500 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_dim_proxy_rel | -0.0010 | -0.0226 | 0.0155 | 0.417 | 0.000 |
| bridge_00084375_0000 | mean_abs_delta_dim_proxy_rel | 0.0023 | -0.0193 | 0.0203 | 0.458 | 0.000 |
| bridge_0008203125_0000 | mean_abs_delta_dim_proxy_rel | 0.0105 | -0.0198 | 0.0392 | 0.625 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008203125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0008359375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00084375_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000828125_0000 | mean_abs_delta_spectral_radius_rel | 0.0000 | -0.0118 | 0.0086 | 0.583 | 0.000 |
| bridge_0008359375_0000 | mean_abs_delta_spectral_radius_rel | -0.0010 | -0.0100 | 0.0082 | 0.500 | 0.000 |
| bridge_0008203125_0000 | mean_abs_delta_spectral_radius_rel | -0.0011 | -0.0118 | 0.0138 | 0.375 | 0.000 |
| bridge_0008125_0000 | mean_abs_delta_spectral_radius_rel | -0.0017 | -0.0128 | 0.0096 | 0.417 | 0.000 |
| bridge_00084375_0000 | mean_abs_delta_spectral_radius_rel | 0.0020 | -0.0121 | 0.0100 | 0.583 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Den smale upper-band-runden bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov. |
| spectral_quasi_invariant | mixed | mean_abs_delta_spectral_radius_rel | Upper-bandet er fortsatt ikke rent nok til å kalle spektralsporet målrettet validert. |
| larger_validation_set | not_yet | spectral_vs_dim_upper_clean_band | Vent med bredere validering til det smale bandet er bedre avklart. |

## Tolkning

- Dette er ikke en ny scan. Det er en målrettet kontroll av det rene upper-bandet fra `v13j`.
- Hvis bandet holder også her, er det et bedre grunnlag for en liten neste validering enn tidligere i v13-sporet.
- Hvis det ikke holder, skal `v13j` leses som en nyttig, men lokal overtolkning.

