# Relasjonell universgraf v0.13d: lokal skjerping av spektral quasi-invariant

## Formål

Denne runden gjør ikke familien bredere. Den bruker mer budsjett på et stramt lokalt regime-sett for å se om spektraldriften blir skarpere enn `dim_proxy` akkurat der `v13c` fortsatt var blandet.

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
| 1 | initial_avg_degree | 0.012 | 0.016 |
| 2 | initial_spectral_per_sqrtN | 0.035 | 0.045 |
| 3 | initial_dim_proxy | 0.071 | 0.088 |

## Regimeutfall per størrelse

| regime | axis | target | radius | overlap | fit_speed |
| --- | --- | --- | --- | --- | --- |
| band_pdel_0005 | delete | 48 | 4.750 | 0.648 | 0.217 |
| band_pdel_0005 | delete | 96 | 6.062 | 0.717 | 0.204 |
| band_pdel_0005 | delete | 192 | 8.562 | 0.671 | 0.265 |
| band_pdel_0005 | delete | 256 | 8.125 | 0.689 | 0.279 |
| band_zero_del | anchor | 48 | 4.688 | 0.570 | 0.209 |
| band_zero_del | anchor | 96 | 5.875 | 0.741 | 0.223 |
| band_zero_del | anchor | 192 | 9.062 | 0.612 | 0.280 |
| band_zero_del | anchor | 256 | 6.688 | 0.780 | 0.214 |
| bridge_00075_0000 | triad | 48 | 4.812 | 0.581 | 0.231 |
| bridge_00075_0000 | triad | 96 | 5.938 | 0.747 | 0.212 |
| bridge_00075_0000 | triad | 192 | 8.500 | 0.580 | 0.256 |
| bridge_00075_0000 | triad | 256 | 8.250 | 0.743 | 0.283 |
| bridge_0010_0000 | triad | 48 | 4.438 | 0.585 | 0.190 |
| bridge_0010_0000 | triad | 96 | 5.938 | 0.719 | 0.181 |
| bridge_0010_0000 | triad | 192 | 8.875 | 0.593 | 0.270 |
| bridge_0010_0000 | triad | 256 | 9.375 | 0.686 | 0.308 |

## Lokal spektral-vs-dim-summering

| regime | axis | spectral_mean | dim_mean | p_spectral_lt_dim | mean_dim_minus_spectral | spectral_delta_vs_anchor | local_status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| band_pdel_0005 | delete | 0.0156 | 0.0428 | 0.812 | 0.0272 | 0.0035 | strong_local |
| bridge_00075_0000 | triad | 0.0156 | 0.0264 | 0.688 | 0.0105 | 0.0033 | good_but_local |
| bridge_0010_0000 | triad | 0.0140 | 0.0260 | 0.750 | 0.0113 | 0.0020 | good_but_local |

## Fokusdrift per regime

| regime | axis | metric | mean_rel_drift | q10 | q90 | top2_prob |
| --- | --- | --- | --- | --- | --- | --- |
| band_pdel_0005 | delete | mean_abs_delta_nodes_rel | 0.0027 | 0.0020 | 0.0034 | 1.000 |
| band_pdel_0005 | delete | mean_abs_delta_spectral_radius_rel | 0.0156 | 0.0127 | 0.0184 | 1.000 |
| band_pdel_0005 | delete | mean_abs_delta_beta1_rel | 0.0280 | 0.0237 | 0.0324 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_dim_proxy_rel | 0.0428 | 0.0345 | 0.0522 | 0.000 |
| band_zero_del | anchor | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | anchor | mean_abs_delta_beta1_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| band_zero_del | anchor | mean_abs_delta_spectral_radius_rel | 0.0121 | 0.0095 | 0.0147 | 0.000 |
| band_zero_del | anchor | mean_abs_delta_dim_proxy_rel | 0.0228 | 0.0203 | 0.0253 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_00075_0000 | triad | mean_abs_delta_beta1_rel | 0.0074 | 0.0032 | 0.0121 | 0.925 |
| bridge_00075_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0156 | 0.0114 | 0.0209 | 0.075 |
| bridge_00075_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0264 | 0.0216 | 0.0318 | 0.000 |
| bridge_0010_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| bridge_0010_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0140 | 0.0108 | 0.0172 | 0.725 |
| bridge_0010_0000 | triad | mean_abs_delta_beta1_rel | 0.0165 | 0.0114 | 0.0226 | 0.275 |
| bridge_0010_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0260 | 0.0222 | 0.0294 | 0.000 |

## Spektral mot dim

| regime | axis | p_spectral_lt_dim | mean_dim_minus_spectral | q10 | q90 |
| --- | --- | --- | --- | --- | --- |
| band_pdel_0005 | delete | 0.812 | 0.0272 | -0.0004 | 0.0598 |
| band_zero_del | anchor | 0.875 | 0.0106 | -0.0003 | 0.0254 |
| bridge_00075_0000 | triad | 0.688 | 0.0105 | -0.0098 | 0.0286 |
| bridge_0010_0000 | triad | 0.750 | 0.0113 | -0.0059 | 0.0307 |

## Off-anchor mot anker

| regime | axis | metric | mean_delta_vs_anchor | q10 | q90 | p_off_gt_anchor | same_value_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_00075_0000 | triad | mean_abs_delta_beta1_rel | 0.0076 | 0.0000 | 0.0124 | 0.438 | 0.562 |
| bridge_0010_0000 | triad | mean_abs_delta_beta1_rel | 0.0172 | 0.0000 | 0.0290 | 0.750 | 0.250 |
| band_pdel_0005 | delete | mean_abs_delta_beta1_rel | 0.0283 | 0.0079 | 0.0521 | 0.938 | 0.062 |
| bridge_0010_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0027 | -0.0135 | 0.0207 | 0.562 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_dim_proxy_rel | 0.0031 | -0.0128 | 0.0169 | 0.562 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_dim_proxy_rel | 0.0200 | -0.0174 | 0.0505 | 0.625 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| bridge_0010_0000 | triad | mean_abs_delta_nodes_rel | 0.0000 | 0.0000 | 0.0000 | 0.000 | 1.000 |
| band_pdel_0005 | delete | mean_abs_delta_nodes_rel | 0.0028 | 0.0000 | 0.0052 | 0.812 | 0.188 |
| bridge_0010_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0020 | -0.0097 | 0.0159 | 0.562 | 0.000 |
| bridge_00075_0000 | triad | mean_abs_delta_spectral_radius_rel | 0.0033 | -0.0063 | 0.0116 | 0.625 | 0.000 |
| band_pdel_0005 | delete | mean_abs_delta_spectral_radius_rel | 0.0035 | -0.0062 | 0.0172 | 0.625 | 0.000 |

## Operativ lesning

| signal_family | status | best_candidate | note |
| --- | --- | --- | --- |
| zero_drift_sanity | breaks_off_anchor | mean_abs_delta_nodes_rel+mean_abs_delta_beta1_rel | Null-driftene bryter fortsatt off-anchor og skal behandles som artefakter, ikke lover. |
| spectral_quasi_invariant | mixed | mean_abs_delta_spectral_radius_rel | Spektraldriften er fortsatt interessant, men ikke skarp nok lokalt til å rettferdiggjøre større valideringssett. |
| larger_validation_set | not_yet | spectral_vs_dim_local_sharpening | Vent med større valideringssett til det lokale spektralsporet er skarpere. |

## Tolkning

- Denne runden bruker mer diskrimineringsbudsjett per regime i stedet for å gjøre familien bredere.
- Hvis spektraldriften fortsatt ikke skiller seg tydelig fra `dim_proxy` her, bør vi være forsiktige med større valideringssett.
- Hvis den derimot skjerpes i knife-edge-regimene, er det et bedre grunnlag for målrettet oppskalering enn `v13c` ga alene.

