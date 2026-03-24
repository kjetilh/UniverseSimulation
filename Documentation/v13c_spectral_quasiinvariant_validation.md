# Relasjonell universgraf v0.13c: målrettet validering av spektral quasi-invariant

## Formål

Denne runden skalerer bare opp ett spor: `mean_abs_delta_spectral_radius_rel`. `dim_proxy` holdes som sekundær kontroll, og de gamle null-driftene holdes bare som sanity check.

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
| 1 | initial_avg_degree | 0.034 | 0.043 |
| 2 | initial_spectral_per_sqrtN | 0.082 | 0.099 |
| 3 | initial_dim_proxy | 0.090 | 0.111 |

## Regimeutfall per størrelse

| regime | axis | target | radius | overlap | fit_speed |
| --- | --- | --- | --- | --- | --- |
| band_death_0005 | death | 48 | 4.640 | 0.664 | 0.218 |
| band_death_0005 | death | 96 | 6.160 | 0.566 | 0.217 |
| band_death_0005 | death | 192 | 8.320 | 0.611 | 0.247 |
| band_death_0005 | death | 256 | 8.120 | 0.661 | 0.240 |
| band_pdel_0005 | delete | 48 | 4.840 | 0.679 | 0.191 |
| band_pdel_0005 | delete | 96 | 7.760 | 0.560 | 0.270 |
| band_pdel_0005 | delete | 192 | 7.400 | 0.729 | 0.241 |
| band_pdel_0005 | delete | 256 | 7.400 | 0.678 | 0.226 |
| band_pdel_0010 | delete | 48 | 5.440 | 0.697 | 0.234 |
| band_pdel_0010 | delete | 96 | 6.200 | 0.640 | 0.227 |
| band_pdel_0010 | delete | 192 | 8.200 | 0.657 | 0.229 |
| band_pdel_0010 | delete | 256 | 7.600 | 0.685 | 0.226 |
| band_zero_del | anchor | 48 | 4.840 | 0.592 | 0.223 |
| band_zero_del | anchor | 96 | 6.480 | 0.652 | 0.229 |
| band_zero_del | anchor | 192 | 7.520 | 0.680 | 0.238 |
| band_zero_del | anchor | 256 | 7.400 | 0.685 | 0.236 |
| bridge_0005_0000 | triad | 48 | 4.560 | 0.598 | 0.179 |
| bridge_0005_0000 | triad | 96 | 5.280 | 0.658 | 0.183 |
| bridge_0005_0000 | triad | 192 | 6.600 | 0.710 | 0.199 |
| bridge_0005_0000 | triad | 256 | 7.480 | 0.711 | 0.248 |
| bridge_00075_0000 | triad | 48 | 4.080 | 0.649 | 0.193 |
| bridge_00075_0000 | triad | 96 | 6.040 | 0.680 | 0.222 |
| bridge_00075_0000 | triad | 192 | 6.360 | 0.701 | 0.179 |
| bridge_00075_0000 | triad | 256 | 7.880 | 0.669 | 0.242 |
| bridge_0010_0000 | triad | 48 | 4.640 | 0.650 | 0.194 |
| bridge_0010_0000 | triad | 96 | 6.240 | 0.586 | 0.216 |
| bridge_0010_0000 | triad | 192 | 7.560 | 0.712 | 0.229 |
| bridge_0010_0000 | triad | 256 | 6.760 | 0.701 | 0.228 |

## Fokusdrift per regime

| regime | axis | metric | mean_rel_drift | q10 | q90 | top2_prob |
| --- | --- | --- | --- | --- | --- | --- |
| band_death_0005 | death | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_death_0005 | death | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_death_0005 | death | mean_abs_delta_spectral_radius_rel | 0.0179 | 0.0155 | 0.0204 | 0.000 |
| band_death_0005 | death | mean_abs_delta_dim_proxy_rel | 0.0286 | 0.0243 | 0.0331 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_nodes_rel | 0.0031 | 0.0025 | 0.0039 | 1.000 |
| band_pdel_0005 | delete | mean_abs_delta_spectral_radius_rel | 0.0167 | 0.0138 | 0.0196 | 1.000 |
| band_pdel_0005 | delete | mean_abs_delta_beta1_rel | 0.0318 | 0.0241 | 0.0393 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_dim_proxy_rel | 0.0551 | 0.0485 | 0.0606 | 0.000 |
| band_pdel_0010 | delete | mean_abs_delta_nodes_rel | 0.0028 | 0.0022 | 0.0033 | 1.000 |
| band_pdel_0010 | delete | mean_abs_delta_spectral_radius_rel | 0.0222 | 0.0192 | 0.0255 | 1.000 |
| band_pdel_0010 | delete | mean_abs_delta_beta1_rel | 0.0370 | 0.0309 | 0.0437 | 0.000 |
| band_pdel_0010 | delete | mean_abs_delta_dim_proxy_rel | 0.0667 | 0.0582 | 0.0765 | 0.000 |
| band_zero_del | anchor | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | anchor | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | anchor | mean_abs_delta_spectral_radius_rel | 0.0150 | 0.0131 | 0.0172 | 0.000 |
| band_zero_del | anchor | mean_abs_delta_dim_proxy_rel | 0.0264 | 0.0215 | 0.0311 | 0.000 |
| bridge_0005_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0005_0000 | triad | mean_abs_delta_beta1_rel | 0.0076 | 0.0053 | 0.0098 | 1.000 |
| bridge_0005_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0163 | 0.0139 | 0.0188 | 0.000 |
| bridge_0005_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0280 | 0.0224 | 0.0336 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00075_0000 | triad | mean_abs_delta_beta1_rel | 0.0133 | 0.0097 | 0.0174 | 0.940 |
| bridge_00075_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0175 | 0.0150 | 0.0200 | 0.060 |
| bridge_00075_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0295 | 0.0265 | 0.0327 | 0.000 |
| bridge_0010_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0010_0000 | triad | mean_abs_delta_beta1_rel | 0.0101 | 0.0062 | 0.0140 | 1.000 |
| bridge_0010_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0234 | 0.0197 | 0.0271 | 0.000 |
| bridge_0010_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0288 | 0.0217 | 0.0362 | 0.000 |

## Spektral mot dim

| regime | axis | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- | --- |
| band_death_0005 | death | 0.700 | 0.0108 | -0.0107 | 0.0334 |
| band_pdel_0005 | delete | 0.950 | 0.0390 | 0.0151 | 0.0749 |
| band_pdel_0010 | delete | 0.950 | 0.0445 | 0.0032 | 0.0990 |
| band_zero_del | anchor | 0.650 | 0.0116 | -0.0062 | 0.0302 |
| bridge_0005_0000 | triad | 0.700 | 0.0120 | -0.0079 | 0.0400 |
| bridge_00075_0000 | triad | 0.850 | 0.0117 | -0.0008 | 0.0269 |
| bridge_0010_0000 | triad | 0.600 | 0.0043 | -0.0223 | 0.0272 |

## Off-anchor mot anker

| regime | axis | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| band_death_0005 | death | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0005_0000 | triad | mean_abs_delta_beta1_rel | 0.0079 | 0.0000 | 0.0212 | 0.550 | 0.450 |
| bridge_0010_0000 | triad | mean_abs_delta_beta1_rel | 0.0103 | 0.0000 | 0.0316 | 0.500 | 0.500 |
| bridge_00075_0000 | triad | mean_abs_delta_beta1_rel | 0.0131 | 0.0000 | 0.0289 | 0.600 | 0.400 |
| band_pdel_0005 | delete | mean_abs_delta_beta1_rel | 0.0317 | 0.0111 | 0.0537 | 1.000 | 0.000 |
| band_pdel_0010 | delete | mean_abs_delta_beta1_rel | 0.0375 | 0.0100 | 0.0594 | 0.900 | 0.100 |
| bridge_0010_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0015 | -0.0249 | 0.0278 | 0.500 | 0.000 |
| bridge_0005_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0018 | -0.0229 | 0.0275 | 0.550 | 0.000 |
| band_death_0005 | death | mean_abs_delta_dim_proxy_rel | 0.0020 | -0.0221 | 0.0194 | 0.650 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0028 | -0.0130 | 0.0164 | 0.750 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_dim_proxy_rel | 0.0289 | 0.0109 | 0.0619 | 0.950 | 0.000 |
| band_pdel_0010 | delete | mean_abs_delta_dim_proxy_rel | 0.0402 | -0.0053 | 0.0868 | 0.800 | 0.000 |
| band_death_0005 | death | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0005_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00075_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0010_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| band_pdel_0010 | delete | mean_abs_delta_nodes_rel | 0.0028 | 0.0000 | 0.0064 | 0.750 | 0.250 |
| band_pdel_0005 | delete | mean_abs_delta_nodes_rel | 0.0031 | 0.0007 | 0.0044 | 0.900 | 0.100 |
| bridge_0005_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0013 | -0.0099 | 0.0137 | 0.500 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_spectral_radius_rel | 0.0015 | -0.0073 | 0.0080 | 0.500 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0026 | -0.0111 | 0.0172 | 0.600 | 0.000 |
| band_death_0005 | death | mean_abs_delta_spectral_radius_rel | 0.0028 | -0.0074 | 0.0165 | 0.550 | 0.000 |
| band_pdel_0010 | delete | mean_abs_delta_spectral_radius_rel | 0.0073 | -0.0055 | 0.0208 | 0.700 | 0.000 |
| bridge_0010_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0088 | -0.0058 | 0.0201 | 0.800 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Null-driftene bryter fortsatt off-anchor og skal behandles som artefakter, ikke lover. |
| spectral_quasi_invariant | mixed | mean_abs_delta_spectral_radius_rel | Spektraldriften er fortsatt interessant, men ikke sterk nok til å stå alene som neste store valideringsmål. |
| larger_validation_set | not_yet | spectral_vs_dim_cross_regime | Vent med større valideringssett til spektralsporet er skarpere eller bredere testet. |

## Tolkning

- Denne runden er en målrettet validering, ikke en ny bred struktur-scan.
- Hvis `spectral_radius_rel` fortsatt holder under et litt større og bredere lokalt regime-sett, er det det sterkeste ikke-trivielle sporet vi har nå.
- Hvis `dim_proxy` holder nesten like godt eller null-driftene plutselig blir eksakte igjen, må lesningen dempes igjen.

