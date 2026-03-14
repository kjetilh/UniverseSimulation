# Kjøringsoppsummering for feature lab

## Parametre

- steps: 10000
- seed: 51
- initial_cycle: 10
- initial_tokens: 6
- r_seed: 0.03
- r_token: 1.0
- r_birth: 0.01
- r_death: 0.01
- p_triad: 0.18
- p_del: 0.14
- p_swap: 0.1
- avoid_disconnect: False
- relocate_tokens: False
- log_every: 200

- trajectory_csv: `Documentation/feature_lab_regimes/aggressive_triad_delete_regime.csv`

# Empirisk quasi-invariantanalyse

Dette dokumentet identifiserer lineære kombinasjoner av features som endrer seg minst over de loggede intervallene.
Matematisk er dette de høyre-singularvektorene til inkrementmatrisen med minst singularverdi.

## Feature-set

tokens, nodes, edges, components, beta1, wedges, triangles, star3, c4, deg_sq_sum, spectral_radius, clustering, dim_proxy

## Skalaeffekter

Rå SVD vektlegger features med store absolutte skalaer og store variasjoner.
Standardisert SVD kjører samme analyse på z-skårte features og tester derfor om konklusjonen er robust når alle features gis sammenlignbar skala.
Hvis en kandidat bare ser god ut i rå analyse, men forsvinner i standardisert analyse, er det et tydelig tegn på skala-dominans heller enn en robust quasi-invariant.

| feature | mean | std | min | max |
| --- | --- | --- | --- | --- |
| tokens | 1.5098 | 0.997498 | 0 | 6 |
| nodes | 171.667 | 84.1103 | 2 | 289 |
| edges | 357.078 | 199.016 | 1 | 645 |
| components | 8.68627 | 4.23566 | 1 | 17 |
| beta1 | 194.098 | 119.68 | 0 | 373 |
| wedges | 3135.39 | 2263.13 | 0 | 6928 |
| triangles | 174.294 | 115.139 | 0 | 374 |
| star3 | 14525.7 | 12914.7 | 0 | 39489 |
| c4 | 901.824 | 773.225 | 0 | 2459 |
| deg_sq_sum | 6984.94 | 4918.49 | 2 | 15128 |
| spectral_radius | 9.30592 | 2.75888 | 1 | 13.0174 |
| clustering | 0.177718 | 0.0460604 | 0 | 0.28436 |
| dim_proxy | 1.91167 | 0.47978 | 0 | 2.78864 |

## Singularverdier

| matrix | singular_values |
| --- | --- |
| ΔF | 9861, 1182, 329.6, 63.58, 47.64, 24.58, 8.86, 6.448, 3.175, 2.034, 0.173, 1.745e-13, 4.054e-14 |
| ΔF/Δt | 56.54, 6.101, 2.357, 0.2979, 0.2066, 0.1294, 0.04254, 0.03135, 0.01209, 0.008184, 0.0006992, 9.786e-16, 3.334e-16 |
| Δz(F) | 9.51, 5.91, 4.521, 1.945, 1.283, 0.886, 0.7251, 0.4123, 0.3049, 0.2058, 0.07664, 5.107e-16, 3.682e-16 |
| Δz(F)/Δt | 0.05367, 0.03171, 0.02332, 0.01045, 0.006452, 0.003295, 0.002954, 0.002127, 0.001439, 0.001005, 0.0003298, 2.492e-18, 1.835e-18 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i rå inkrementer ΔF | -0.4952·nodes +0.5138·edges +0.4952·components -0.4952·beta1 | 5.22761e-27 | -3.9152e-17 |
| 2 | Minste endring i rå inkrementer ΔF | -0.1899·nodes -0.5170·edges +0.1899·components -0.1899·beta1 -0.7069·wedges +0.3534·deg_sq_sum | 9.99333e-26 | -1.18078e-17 |
| 3 | Minste endring i rå inkrementer ΔF | +0.9991·clustering | 0.000595907 | -8.48264e-06 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i rå hastigheter ΔF/Δt | +0.4699·nodes -0.5701·edges -0.4699·components +0.4699·beta1 -0.1002·wedges | 1.43591e-26 | -7.23675e-17 |
| 2 | Minste endring i rå hastigheter ΔF/Δt | +0.2458·nodes +0.4541·edges -0.2458·components +0.2458·beta1 +0.7000·wedges -0.3500·deg_sq_sum | 1.32132e-25 | -5.8433e-17 |
| 3 | Minste endring i rå hastigheter ΔF/Δt | -0.9998·clustering | 0.000878799 | -1.38129e-05 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i standardiserte inkrementer Δz(F) | -0.2435·z(nodes) +0.6158·z(edges) -0.3465·z(beta1) +0.4498·z(wedges) -0.4888·z(deg_sq_sum) | 1.38818e-32 | -6.50489e-20 |
| 2 | Minste endring i standardiserte inkrementer Δz(F) | -0.2385·z(nodes) +0.5199·z(edges) -0.3394·z(beta1) -0.5056·z(wedges) +0.5494·z(deg_sq_sum) | 2.57073e-32 | -2.51946e-21 |
| 3 | Minste endring i standardiserte inkrementer Δz(F) | +0.2112·z(edges) +0.3600·z(beta1) -0.5677·z(wedges) +0.4947·z(star3) -0.5053·z(deg_sq_sum) | 0.000117475 | -1.48183e-06 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i standardiserte hastigheter Δz(F)/Δt | -0.0995·z(nodes) +0.1777·z(edges) -0.1416·z(beta1) -0.6560·z(wedges) +0.7128·z(deg_sq_sum) | 2.06009e-32 | -3.78211e-20 |
| 2 | Minste endring i standardiserte hastigheter Δz(F)/Δt | +0.3260·z(nodes) -0.7861·z(edges) +0.4639·z(beta1) -0.1663·z(wedges) +0.1807·z(deg_sq_sum) | 2.77612e-32 | 1.11505e-19 |
| 3 | Minste endring i standardiserte hastigheter Δz(F)/Δt | +0.2322·z(edges) +0.4062·z(beta1) -0.5783·z(wedges) +0.4227·z(star3) -0.5134·z(deg_sq_sum) | 0.000141874 | -7.40506e-06 |

## Enkel drift per feature

| feature | slope | mean | std | rel_slope_per_mean |
| --- | --- | --- | --- | --- |
| tokens | -5.57272e-08 | 1.5098 | 0.997498 | -3.69102e-08 |
| nodes | 0.0174446 | 171.667 | 84.1103 | 0.000101619 |
| edges | 0.0414633 | 357.078 | 199.016 | 0.000116118 |
| components | 0.000833423 | 8.68627 | 4.23566 | 9.59471e-05 |
| beta1 | 0.0248521 | 194.098 | 119.68 | 0.000128039 |
| wedges | 0.464214 | 3135.39 | 2263.13 | 0.000148056 |
| triangles | 0.0235511 | 174.294 | 115.139 | 0.000135123 |
| star3 | 2.56129 | 14525.7 | 12914.7 | 0.000176328 |
| c4 | 0.151561 | 901.824 | 773.225 | 0.00016806 |
| deg_sq_sum | 1.01136 | 6984.94 | 4918.49 | 0.000144791 |
| spectral_radius | 0.000554995 | 9.30592 | 2.75888 | 5.96389e-05 |
| clustering | -2.63222e-07 | 0.177718 | 0.0460604 | -1.48112e-06 |
| dim_proxy | 7.16176e-05 | 1.91167 | 0.47978 | 3.74633e-05 |

## Tolkning

En kandidat med liten increment_var og liten time_slope er en plausibel quasi-invariant i det aktuelle regimet.
Det er ikke et bevis på fundamental bevaring; det er en empirisk signatur av metastabilitet i valgt feature-rom.
Kandidater som er stabile både i rå og standardisert analyse er de mest interessante.
