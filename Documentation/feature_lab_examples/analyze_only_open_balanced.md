# Feature-lab analyse

- source_csv: `Documentation/feature_lab_regimes/open_balanced_regime.csv`
- feature_basis: `reduced`
- analysis_mode: `both`
- row_count: 61
- t_start: 0
- t_end: 1574.5

## Feature-set

tokens, nodes, edges, components, wedges, triangles, star3, c4, spectral_radius, clustering, dim_proxy

## Algebraiske identiteter og konstante features

- constant_features: components
- max_abs_beta1_identity: 0
- max_abs_deg_sq_identity: 0

## Analysemerknader

- Rå analyse er sensitiv for absolutte skalaer og store variasjoner.
- Standardisert analyse tester om de samme kandidatene overlever når alle features z-skaleres.
- Redusert basis fjerner `beta1` og `deg_sq_sum` for å kvotientere ut de mest opplagte algebraiske redundansene.

## Skalaeffekter

Rå analyse vektlegger store absolutte skalaer, mens standardisert analyse bruker z-skårte features for å teste robusthet mot slike skalaeffekter.

| feature | mean | std | min | max |
| --- | --- | --- | --- | --- |
| tokens | 8.01639 | 1.50944 | 4 | 10 |
| nodes | 15.5902 | 5.7385 | 8 | 27 |
| edges | 93.7049 | 61.3953 | 10 | 225 |
| components | 1 | 0 | 1 | 1 |
| wedges | 1221.97 | 1120.87 | 10 | 3951 |
| triangles | 327.918 | 287.218 | 0 | 1028 |
| star3 | 5465.66 | 6355.88 | 0 | 22767 |
| c4 | 3178.93 | 3545.42 | 0 | 12842 |
| spectral_radius | 11.3676 | 4.14775 | 2 | 18.536 |
| clustering | 0.796832 | 0.1567 | 0 | 0.974115 |
| dim_proxy | 0.244125 | 0.188978 | 0.0194279 | 0.802158 |

## Singularverdier

| matrix | singular_values |
| --- | --- |
| Minste endring i rå inkrementer ΔF | 7503, 809.3, 228.2, 37.87, 5.344, 4.983, 4.13, 1.389, 0.7419, 0.258, 5.19e-15 |
| Minste endring i rå hastigheter ΔF/Δt | 337, 34.98, 8.896, 1.608, 0.2, 0.1796, 0.1584, 0.04883, 0.0324, 0.009408, 4.039e-16 |
| Minste endring i standardiserte inkrementer Δz(F) | 6.684, 4.125, 3.36, 2.157, 0.7653, 0.42, 0.245, 0.1079, 0.06446, 0.02955, 4.367e-17 |
| Minste endring i standardiserte hastigheter Δz(F)/Δt | 0.2563, 0.149, 0.1267, 0.09311, 0.03059, 0.01659, 0.01023, 0.004279, 0.002679, 0.001125, 3.946e-19 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i rå inkrementer ΔF | +1.0000·components | 1.3248e-29 | 3.68116e-17 |
| 2 | Minste endring i rå inkrementer ΔF | -0.2540·spectral_radius +0.9657·clustering | 0.00110808 | 0.00010242 |
| 3 | Minste endring i rå inkrementer ΔF | +0.1971·nodes +0.1199·spectral_radius -0.9700·dim_proxy | 0.00917013 | -0.000337575 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i rå hastigheter ΔF/Δt | -1.0000·components | 3.12174e-29 | 1.04007e-16 |
| 2 | Minste endring i rå hastigheter ΔF/Δt | -0.2436·spectral_radius +0.9686·clustering | 0.00112342 | 8.2191e-05 |
| 3 | Minste endring i rå hastigheter ΔF/Δt | +0.2066·nodes +0.1414·spectral_radius -0.9648·dim_proxy | 0.00926652 | -0.000259773 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i standardiserte inkrementer Δz(F) | +1.0000·z(components) | 1.94204e-33 | -9.5047e-19 |
| 2 | Minste endring i standardiserte inkrementer Δz(F) | +0.4785·z(edges) -0.8225·z(wedges) +0.1383·z(triangles) +0.2660·z(star3) | 1.45573e-05 | 7.99808e-06 |
| 3 | Minste endring i standardiserte inkrementer Δz(F) | +0.2871·z(edges) -0.4571·z(triangles) -0.4707·z(star3) +0.6961·z(c4) | 6.84943e-05 | 2.16113e-05 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i standardiserte hastigheter Δz(F)/Δt | +1.0000·z(components) | 3.78577e-34 | -5.21041e-19 |
| 2 | Minste endring i standardiserte hastigheter Δz(F)/Δt | -0.5106·z(edges) +0.8177·z(wedges) -0.1115·z(triangles) -0.2217·z(star3) | 1.52807e-05 | -2.32276e-05 |
| 3 | Minste endring i standardiserte hastigheter Δz(F)/Δt | +0.2465·z(edges) -0.4699·z(triangles) -0.4859·z(star3) +0.6938·z(c4) | 6.90323e-05 | 2.41905e-05 |

## Enkel drift per feature

| feature | slope | mean | std | rel_slope_per_mean |
| --- | --- | --- | --- | --- |
| tokens | 0.00265228 | 8.01639 | 1.50944 | 0.000330857 |
| nodes | 0.0120222 | 15.5902 | 5.7385 | 0.000771143 |
| edges | 0.128827 | 93.7049 | 61.3953 | 0.00137482 |
| components | 0 | 1 | 0 | 0 |
| wedges | 2.23888 | 1221.97 | 1120.87 | 0.00183219 |
| triangles | 0.578 | 327.918 | 287.218 | 0.00176264 |
| star3 | 11.8845 | 5465.66 | 6355.88 | 0.0021744 |
| c4 | 6.68848 | 3178.93 | 3545.42 | 0.002104 |
| spectral_radius | 0.00896933 | 11.3676 | 4.14775 | 0.000789026 |
| clustering | 9.59808e-05 | 0.796832 | 0.1567 | 0.000120453 |
| dim_proxy | 3.73515e-05 | 0.244125 | 0.188978 | 0.000153001 |

## Tolkning

Lineære kombinasjoner med liten increment_var og liten time_slope er kandidater til quasi-invarianter i det valgte feature-rommet.
De må fortsatt skilles fra rene algebraiske identiteter og fra artefakter som bare oppstår på grunn av ulik feature-skala.