# Relasjonell universgraf v0.12d: kryssakse radius-transfer

## Formål

Denne runden tester om radius-surrogatet holder utover ren triad-akse ved a sammenligne sma basisvalg mot triad-, delete- og death-naerregimer rundt `band_zero_del`.

## Startstorrelser

| target | mean_initial | q10 | q90 | separated_from_prev |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Regimeutfall per størrelse

| regime | axis | target | radius | fit_speed | overlap | rel_drift_triangles |
| --- | --- | --- | --- | --- | --- | --- |
| band_death_0005 | death | 48 | 4.562 | 0.204 | 0.731 | 0.054 |
| band_death_0005 | death | 96 | 6.188 | 0.223 | 0.645 | 0.068 |
| band_death_0005 | death | 192 | 8.438 | 0.247 | 0.655 | 0.054 |
| band_death_0005 | death | 256 | 7.812 | 0.244 | 0.786 | 0.027 |
| band_pdel_0005 | delete | 48 | 4.625 | 0.241 | 0.707 | 0.090 |
| band_pdel_0005 | delete | 96 | 5.562 | 0.223 | 0.616 | 0.074 |
| band_pdel_0005 | delete | 192 | 8.312 | 0.253 | 0.651 | 0.058 |
| band_pdel_0005 | delete | 256 | 8.438 | 0.268 | 0.695 | 0.033 |
| band_pdel_0010 | delete | 48 | 5.375 | 0.236 | 0.697 | 0.054 |
| band_pdel_0010 | delete | 96 | 6.750 | 0.250 | 0.544 | 0.159 |
| band_pdel_0010 | delete | 192 | 9.062 | 0.273 | 0.722 | 0.036 |
| band_pdel_0010 | delete | 256 | 7.750 | 0.220 | 0.687 | 0.037 |
| band_zero_del | anchor | 48 | 4.688 | 0.227 | 0.754 | 0.069 |
| band_zero_del | anchor | 96 | 4.812 | 0.188 | 0.773 | 0.090 |
| band_zero_del | anchor | 192 | 7.500 | 0.225 | 0.639 | 0.050 |
| band_zero_del | anchor | 256 | 8.625 | 0.282 | 0.778 | 0.054 |
| bridge_00075_0000 | triad | 48 | 3.625 | 0.169 | 0.786 | 0.115 |
| bridge_00075_0000 | triad | 96 | 5.000 | 0.187 | 0.732 | 0.091 |
| bridge_00075_0000 | triad | 192 | 5.375 | 0.166 | 0.839 | 0.040 |
| bridge_00075_0000 | triad | 256 | 6.688 | 0.201 | 0.792 | 0.043 |
| bridge_0010_0000 | triad | 48 | 4.000 | 0.183 | 0.732 | 0.090 |
| bridge_0010_0000 | triad | 96 | 6.062 | 0.223 | 0.656 | 0.105 |
| bridge_0010_0000 | triad | 192 | 8.438 | 0.275 | 0.596 | 0.087 |
| bridge_0010_0000 | triad | 256 | 7.625 | 0.225 | 0.778 | 0.034 |

## Radius-transfer per basis

| regime | axis | basis | relative_skill |
| --- | --- | --- | --- |
| band_death_0005 | death | spectral_plus_dim | 0.138 |
| band_death_0005 | death | spectral_only | 0.134 |
| band_death_0005 | death | spectral_plus_clustering | 0.150 |
| band_death_0005 | death | full_basis | 0.159 |
| band_pdel_0005 | delete | spectral_plus_dim | 0.118 |
| band_pdel_0005 | delete | spectral_only | 0.119 |
| band_pdel_0005 | delete | spectral_plus_clustering | 0.137 |
| band_pdel_0005 | delete | full_basis | 0.148 |
| band_pdel_0010 | delete | spectral_plus_dim | 0.068 |
| band_pdel_0010 | delete | spectral_only | 0.068 |
| band_pdel_0010 | delete | spectral_plus_clustering | 0.032 |
| band_pdel_0010 | delete | full_basis | 0.017 |
| band_zero_del | anchor | spectral_plus_dim | 0.125 |
| band_zero_del | anchor | spectral_only | 0.124 |
| band_zero_del | anchor | spectral_plus_clustering | 0.150 |
| band_zero_del | anchor | full_basis | 0.162 |
| bridge_00075_0000 | triad | spectral_plus_dim | 0.078 |
| bridge_00075_0000 | triad | spectral_only | 0.075 |
| bridge_00075_0000 | triad | spectral_plus_clustering | 0.066 |
| bridge_00075_0000 | triad | full_basis | 0.024 |
| bridge_0010_0000 | triad | spectral_plus_dim | 0.196 |
| bridge_0010_0000 | triad | spectral_only | 0.190 |
| bridge_0010_0000 | triad | spectral_plus_clustering | 0.169 |
| bridge_0010_0000 | triad | full_basis | 0.137 |

## Basis-ranking

| rank | basis | mean_cross_axis_skill | mean_off_anchor_skill | min_off_anchor_skill | cross_axis_positive |
| --- | --- | --- | --- | --- | --- |
| 1 | spectral_plus_dim | 0.108 | 0.120 | 0.068 | 3/3 |
| 2 | full_basis | 0.108 | 0.097 | 0.017 | 3/3 |
| 3 | spectral_only | 0.107 | 0.117 | 0.068 | 3/3 |
| 4 | spectral_plus_clustering | 0.106 | 0.111 | 0.032 | 3/3 |

## Operativ lesning

- Best kryssakse-basis er `spectral_plus_dim` med mean cross-axis skill `0.108` og total off-anchor skill `0.120`.
- Narmeste enkle kontroll er `spectral_only`. Det er den riktige sammenligningen hvis vi bryr oss om enkel surrogate-geometri heller enn bare score alene.
- `full_basis` er fortsatt nyttig som sanity check, men den taper her pa samlet off-anchor-robusthet (`0.097`) mot `spectral_plus_dim` (`0.120`).
- Dette er en strukturtest, ikke en ny frontier-runde. Negative tall her ma leses som grenser for surrogate-gyldighet, ikke som ny kandidatkonkurranse.

