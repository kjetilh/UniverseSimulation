# Relasjonell universgraf v0.12c: radius-transfer-raffinement

## Formål

Denne runden holder `band_zero_del` fast og tester bare hvor robust radius-transferen er til nærliggende triad-varianter, og hvilken liten basis som bærer mest av signalet.

## Startstorrelser

| target | mean_initial | q10 | q90 | separated_from_prev |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Regimeutfall per størrelse

| regime | target | radius | fit_speed | overlap | rel_drift_triangles |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | 48 | 4.188 | 0.189 | 0.736 | 0.216 |
| band_zero_del | 96 | 5.750 | 0.186 | 0.614 | 0.095 |
| band_zero_del | 192 | 8.500 | 0.229 | 0.589 | 0.054 |
| band_zero_del | 256 | 8.375 | 0.258 | 0.594 | 0.042 |
| bridge_0005_0000 | 48 | 4.500 | 0.168 | 0.697 | 0.087 |
| bridge_0005_0000 | 96 | 6.688 | 0.198 | 0.554 | 0.171 |
| bridge_0005_0000 | 192 | 7.750 | 0.226 | 0.725 | 0.054 |
| bridge_0005_0000 | 256 | 7.625 | 0.235 | 0.731 | 0.038 |
| bridge_00075_0000 | 48 | 3.688 | 0.156 | 0.754 | 0.106 |
| bridge_00075_0000 | 96 | 6.312 | 0.182 | 0.570 | 0.159 |
| bridge_00075_0000 | 192 | 8.562 | 0.235 | 0.515 | 0.109 |
| bridge_00075_0000 | 256 | 7.875 | 0.249 | 0.708 | 0.052 |
| bridge_0010_0000 | 48 | 4.500 | 0.189 | 0.693 | 0.212 |
| bridge_0010_0000 | 96 | 5.938 | 0.203 | 0.598 | 0.147 |
| bridge_0010_0000 | 192 | 8.250 | 0.255 | 0.625 | 0.098 |
| bridge_0010_0000 | 256 | 8.375 | 0.272 | 0.632 | 0.044 |
| bridge_00125_0000 | 48 | 4.688 | 0.202 | 0.707 | 0.184 |
| bridge_00125_0000 | 96 | 6.375 | 0.225 | 0.617 | 0.128 |
| bridge_00125_0000 | 192 | 8.250 | 0.230 | 0.563 | 0.073 |
| bridge_00125_0000 | 256 | 7.812 | 0.256 | 0.712 | 0.047 |
| bridge_0015_0000 | 48 | 5.188 | 0.190 | 0.734 | 0.178 |
| bridge_0015_0000 | 96 | 6.375 | 0.199 | 0.626 | 0.112 |
| bridge_0015_0000 | 192 | 7.438 | 0.206 | 0.609 | 0.087 |
| bridge_0015_0000 | 256 | 7.188 | 0.226 | 0.723 | 0.051 |

## Radius-transfer per basis

| test_regime | basis | rmse | baseline_rmse | relative_skill |
| --- | --- | --- | --- | --- |
| band_zero_del | spectral_only | 2.2303 | 2.8976 | 0.230 |
| band_zero_del | clustering_only | 2.8038 | 2.8976 | 0.032 |
| band_zero_del | dim_only | 2.5874 | 2.8976 | 0.107 |
| band_zero_del | spectral_plus_clustering | 2.2243 | 2.8976 | 0.232 |
| band_zero_del | spectral_plus_dim | 2.2295 | 2.8976 | 0.231 |
| band_zero_del | clustering_plus_dim | 2.5584 | 2.8976 | 0.117 |
| band_zero_del | full_basis | 2.2218 | 2.8976 | 0.233 |
| bridge_0005_0000 | spectral_only | 2.2577 | 2.5769 | 0.124 |
| bridge_0005_0000 | clustering_only | 2.4510 | 2.5769 | 0.049 |
| bridge_0005_0000 | dim_only | 2.4987 | 2.5769 | 0.030 |
| bridge_0005_0000 | spectral_plus_clustering | 2.2771 | 2.5769 | 0.116 |
| bridge_0005_0000 | spectral_plus_dim | 2.2518 | 2.5769 | 0.126 |
| bridge_0005_0000 | clustering_plus_dim | 2.4351 | 2.5769 | 0.055 |
| bridge_0005_0000 | full_basis | 2.2671 | 2.5769 | 0.120 |
| bridge_00075_0000 | spectral_only | 2.1964 | 2.8772 | 0.237 |
| bridge_00075_0000 | clustering_only | 2.7353 | 2.8772 | 0.049 |
| bridge_00075_0000 | dim_only | 2.5555 | 2.8772 | 0.112 |
| bridge_00075_0000 | spectral_plus_clustering | 2.2050 | 2.8772 | 0.234 |
| bridge_00075_0000 | spectral_plus_dim | 2.1960 | 2.8772 | 0.237 |
| bridge_00075_0000 | clustering_plus_dim | 2.4983 | 2.8772 | 0.132 |
| bridge_00075_0000 | full_basis | 2.1914 | 2.8772 | 0.238 |
| bridge_0010_0000 | spectral_only | 2.4368 | 2.9731 | 0.180 |
| bridge_0010_0000 | clustering_only | 2.8611 | 2.9731 | 0.038 |
| bridge_0010_0000 | dim_only | 2.6868 | 2.9731 | 0.096 |
| bridge_0010_0000 | spectral_plus_clustering | 2.4426 | 2.9731 | 0.178 |
| bridge_0010_0000 | spectral_plus_dim | 2.4386 | 2.9731 | 0.180 |
| bridge_0010_0000 | clustering_plus_dim | 2.6453 | 2.9731 | 0.110 |
| bridge_0010_0000 | full_basis | 2.4410 | 2.9731 | 0.179 |
| bridge_00125_0000 | spectral_only | 2.2836 | 2.6497 | 0.138 |
| bridge_00125_0000 | clustering_only | 2.5400 | 2.6497 | 0.041 |
| bridge_00125_0000 | dim_only | 2.5171 | 2.6497 | 0.050 |
| bridge_00125_0000 | spectral_plus_clustering | 2.2965 | 2.6497 | 0.133 |
| bridge_00125_0000 | spectral_plus_dim | 2.2801 | 2.6497 | 0.139 |
| bridge_00125_0000 | clustering_plus_dim | 2.4660 | 2.6497 | 0.069 |
| bridge_00125_0000 | full_basis | 2.2936 | 2.6497 | 0.134 |
| bridge_0015_0000 | spectral_only | 2.9311 | 2.8653 | -0.023 |
| bridge_0015_0000 | clustering_only | 2.9044 | 2.8653 | -0.014 |
| bridge_0015_0000 | dim_only | 2.8779 | 2.8653 | -0.004 |
| bridge_0015_0000 | spectral_plus_clustering | 2.9244 | 2.8653 | -0.021 |
| bridge_0015_0000 | spectral_plus_dim | 2.9325 | 2.8653 | -0.023 |
| bridge_0015_0000 | clustering_plus_dim | 2.8983 | 2.8653 | -0.012 |
| bridge_0015_0000 | full_basis | 2.9192 | 2.8653 | -0.019 |

## Off-anchor basis-ranking

| rank | basis | mean_off_anchor_skill | min_off_anchor_skill | positive_regimes | best_test | worst_test |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | spectral_plus_dim | 0.132 | -0.023 | 4/5 | bridge_00075_0000 (0.237) | bridge_0015_0000 (-0.023) |
| 2 | spectral_only | 0.131 | -0.023 | 4/5 | bridge_00075_0000 (0.237) | bridge_0015_0000 (-0.023) |
| 3 | full_basis | 0.131 | -0.019 | 4/5 | bridge_00075_0000 (0.238) | bridge_0015_0000 (-0.019) |
| 4 | spectral_plus_clustering | 0.128 | -0.021 | 4/5 | bridge_00075_0000 (0.234) | bridge_0015_0000 (-0.021) |
| 5 | clustering_plus_dim | 0.071 | -0.012 | 4/5 | bridge_00075_0000 (0.132) | bridge_0015_0000 (-0.012) |
| 6 | dim_only | 0.057 | -0.004 | 4/5 | bridge_00075_0000 (0.112) | bridge_0015_0000 (-0.004) |
| 7 | clustering_only | 0.033 | -0.014 | 4/5 | bridge_00075_0000 (0.049) | bridge_0015_0000 (-0.014) |

## Operativ lesning

- Den sterkeste off-anchor radius-basen i denne runden er `spectral_plus_dim` med mean off-anchor skill `0.132` og worst-case `-0.023`.
- Alle de testede basisene blir svakt negative ved `bridge_0015_0000`. Det tyder mer pa en lokal gyldighetsgrense for radius-surrogatet enn pa en ren rangeringsstoy.
- Hvis en liten basis topper både mean og worst-case off-anchor, er det et bedre tegn på ekte struktur enn om bare anchor-fitten ser god ut.
- Hvis signalet holder for radius men ikke for overlap, peker det mot en smal geometrisk surrogate heller enn en bred dynamisk erstatning.

