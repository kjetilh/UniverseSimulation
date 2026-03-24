# Relasjonell universgraf v0.13e: skjerping av spektral triad-korridor

## Formål

Denne runden tar bare triad-korridoren videre. Delete-punktet er allerede lokalt sterkt, så her bruker vi budsjettet på å se om triadpunktene kan bli skarpe nok til å løfte hele spektralsporet.

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
| 1 | initial_avg_degree | 0.023 | 0.030 |
| 2 | initial_dim_proxy | 0.052 | 0.067 |
| 3 | initial_spectral_per_sqrtN | 0.058 | 0.083 |

## Regimeutfall per størrelse

| regime | axis | target | radius | overlap | fit_speed |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | anchor | 48 | 3.875 | 0.685 | 0.166 |
| band_zero_del | anchor | 96 | 6.125 | 0.686 | 0.231 |
| band_zero_del | anchor | 192 | 8.125 | 0.625 | 0.264 |
| band_zero_del | anchor | 256 | 8.375 | 0.627 | 0.265 |
| bridge_000625_0000 | triad | 48 | 4.125 | 0.698 | 0.233 |
| bridge_000625_0000 | triad | 96 | 5.875 | 0.618 | 0.218 |
| bridge_000625_0000 | triad | 192 | 7.625 | 0.641 | 0.231 |
| bridge_000625_0000 | triad | 256 | 8.062 | 0.680 | 0.252 |
| bridge_00075_0000 | triad | 48 | 4.562 | 0.637 | 0.241 |
| bridge_00075_0000 | triad | 96 | 6.750 | 0.663 | 0.244 |
| bridge_00075_0000 | triad | 192 | 7.062 | 0.601 | 0.213 |
| bridge_00075_0000 | triad | 256 | 7.188 | 0.699 | 0.218 |
| bridge_000875_0000 | triad | 48 | 4.625 | 0.703 | 0.213 |
| bridge_000875_0000 | triad | 96 | 6.438 | 0.639 | 0.226 |
| bridge_000875_0000 | triad | 192 | 8.250 | 0.611 | 0.273 |
| bridge_000875_0000 | triad | 256 | 7.188 | 0.717 | 0.233 |
| bridge_0010_0000 | triad | 48 | 4.312 | 0.625 | 0.185 |
| bridge_0010_0000 | triad | 96 | 6.062 | 0.705 | 0.243 |
| bridge_0010_0000 | triad | 192 | 7.188 | 0.658 | 0.216 |
| bridge_0010_0000 | triad | 256 | 8.312 | 0.677 | 0.256 |

## Triad-korridor-summering

| regime | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | corridor_status |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_000625_0000 | 0.0151 | 0.0305 | 0.875 | 0.0147 | 0.0035 | sharp_local |
| bridge_00075_0000 | 0.0164 | 0.0331 | 0.625 | 0.0173 | 0.0045 | mixed |
| bridge_000875_0000 | 0.0151 | 0.0341 | 0.875 | 0.0188 | 0.0035 | sharp_local |
| bridge_0010_0000 | 0.0147 | 0.0305 | 0.750 | 0.0159 | 0.0029 | good_but_local |

## Fokusdrift per regime

| regime | metric | mean_rel_drift | q10 | q90 | top2_prob |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | mean_abs_delta_spectral_radius_rel | 0.0116 | 0.0096 | 0.0138 | 0.000 |
| band_zero_del | mean_abs_delta_dim_proxy_rel | 0.0350 | 0.0294 | 0.0400 | 0.000 |
| bridge_000625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000625_0000 | mean_abs_delta_beta1_rel | 0.0102 | 0.0072 | 0.0131 | 0.900 |
| bridge_000625_0000 | mean_abs_delta_spectral_radius_rel | 0.0151 | 0.0118 | 0.0188 | 0.100 |
| bridge_000625_0000 | mean_abs_delta_dim_proxy_rel | 0.0305 | 0.0256 | 0.0354 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00075_0000 | mean_abs_delta_beta1_rel | 0.0098 | 0.0060 | 0.0138 | 0.994 |
| bridge_00075_0000 | mean_abs_delta_spectral_radius_rel | 0.0164 | 0.0131 | 0.0197 | 0.006 |
| bridge_00075_0000 | mean_abs_delta_dim_proxy_rel | 0.0331 | 0.0270 | 0.0400 | 0.000 |
| bridge_000875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_spectral_radius_rel | 0.0151 | 0.0116 | 0.0186 | 0.831 |
| bridge_000875_0000 | mean_abs_delta_beta1_rel | 0.0197 | 0.0128 | 0.0268 | 0.169 |
| bridge_000875_0000 | mean_abs_delta_dim_proxy_rel | 0.0341 | 0.0276 | 0.0395 | 0.000 |
| bridge_0010_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0010_0000 | mean_abs_delta_spectral_radius_rel | 0.0147 | 0.0115 | 0.0175 | 0.706 |
| bridge_0010_0000 | mean_abs_delta_beta1_rel | 0.0186 | 0.0087 | 0.0287 | 0.294 |
| bridge_0010_0000 | mean_abs_delta_dim_proxy_rel | 0.0305 | 0.0223 | 0.0381 | 0.000 |

## Spektral mot dim

| regime | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- |
| band_zero_del | 0.938 | 0.0231 | 0.0062 | 0.0444 |
| bridge_000625_0000 | 0.875 | 0.0147 | -0.0008 | 0.0317 |
| bridge_00075_0000 | 0.625 | 0.0173 | -0.0051 | 0.0437 |
| bridge_000875_0000 | 0.875 | 0.0188 | -0.0017 | 0.0387 |
| bridge_0010_0000 | 0.750 | 0.0159 | -0.0068 | 0.0484 |

## Off-anchor mot anker

| regime | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_00075_0000 | mean_abs_delta_beta1_rel | 0.0096 | 0.0000 | 0.0317 | 0.375 | 0.625 |
| bridge_000625_0000 | mean_abs_delta_beta1_rel | 0.0104 | 0.0000 | 0.0264 | 0.562 | 0.438 |
| bridge_0010_0000 | mean_abs_delta_beta1_rel | 0.0175 | 0.0000 | 0.0371 | 0.438 | 0.562 |
| bridge_000875_0000 | mean_abs_delta_beta1_rel | 0.0193 | 0.0000 | 0.0268 | 0.688 | 0.312 |
| bridge_000875_0000 | mean_abs_delta_dim_proxy_rel | -0.0008 | -0.0299 | 0.0312 | 0.438 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_dim_proxy_rel | -0.0013 | -0.0244 | 0.0311 | 0.375 | 0.000 |
| bridge_0010_0000 | mean_abs_delta_dim_proxy_rel | -0.0042 | -0.0352 | 0.0167 | 0.438 | 0.000 |
| bridge_000625_0000 | mean_abs_delta_dim_proxy_rel | -0.0049 | -0.0256 | 0.0137 | 0.438 | 0.000 |
| bridge_000625_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_00075_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_000875_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0010_0000 | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0010_0000 | mean_abs_delta_spectral_radius_rel | 0.0029 | -0.0130 | 0.0136 | 0.688 | 0.000 |
| bridge_000625_0000 | mean_abs_delta_spectral_radius_rel | 0.0035 | -0.0100 | 0.0197 | 0.562 | 0.000 |
| bridge_000875_0000 | mean_abs_delta_spectral_radius_rel | 0.0035 | -0.0057 | 0.0099 | 0.688 | 0.000 |
| bridge_00075_0000 | mean_abs_delta_spectral_radius_rel | 0.0045 | -0.0103 | 0.0201 | 0.562 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Triad-korridoren bryter fortsatt `beta1` off-anchor; null-drift skal fortsatt ikke leses som lov. |
| spectral_quasi_invariant | mixed | mean_abs_delta_spectral_radius_rel | Triad-korridoren er fortsatt interessant, men ikke skarp nok lokalt til å rettferdiggjøre større valideringssett. |
| larger_validation_set | not_yet | spectral_vs_dim_triad_corridor | Vent med større valideringssett til triad-korridoren er skarpere. |

## Tolkning

- Denne runden prøver ikke å gjøre signalet bredere, bare å gjøre triad-korridoren skarpere.
- Hvis triadpunktene fortsatt ikke blir skarpe her, bør vi være forsiktige med å tro at mer budsjett alene vil løse spektralsporet.
- Hvis de derimot begynner å konvergere mot et lokalt plateau eller et tydelig optimum, har vi et bedre grunnlag for neste smale steg.

