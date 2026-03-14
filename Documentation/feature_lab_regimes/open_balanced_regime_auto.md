# Kjøringsoppsummering for feature lab

## Parametre

- steps: 12000
- seed: 41
- initial_cycle: 10
- initial_tokens: 6
- r_seed: 0.02
- r_token: 1.0
- r_birth: 0.01
- r_death: 0.01
- p_triad: 0.08
- p_del: 0.04
- p_swap: 0.06
- avoid_disconnect: False
- relocate_tokens: False
- log_every: 200

- trajectory_csv: `Documentation/feature_lab_regimes/open_balanced_regime.csv`

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
| tokens | 8.01639 | 1.50944 | 4 | 10 |
| nodes | 15.5902 | 5.7385 | 8 | 27 |
| edges | 93.7049 | 61.3953 | 10 | 225 |
| components | 1 | 0 | 1 | 1 |
| beta1 | 79.1148 | 55.7295 | 1 | 199 |
| wedges | 1221.97 | 1120.87 | 10 | 3951 |
| triangles | 327.918 | 287.218 | 0 | 1028 |
| star3 | 5465.66 | 6355.88 | 0 | 22767 |
| c4 | 3178.93 | 3545.42 | 0 | 12842 |
| deg_sq_sum | 2631.34 | 2363.4 | 40 | 8350 |
| spectral_radius | 11.3676 | 4.14775 | 2 | 18.536 |
| clustering | 0.796832 | 0.1567 | 0 | 0.974115 |
| dim_proxy | 0.244125 | 0.188978 | 0.0194279 | 0.802158 |

## Singularverdier

| matrix | singular_values |
| --- | --- |
| ΔF | 7736, 820.5, 511.7, 38.9, 8.368, 5.317, 4.716, 1.432, 0.7508, 0.258, 1.304e-13, 3.894e-14, 6.272e-15 |
| ΔF/Δt | 347.2, 35.57, 19.92, 1.644, 0.3047, 0.2007, 0.1791, 0.05009, 0.0328, 0.00941, 4.021e-15, 1.264e-15, 3.734e-16 |
| Δz(F) | 6.693, 4.135, 3.372, 2.353, 0.7835, 0.4245, 0.3029, 0.1151, 0.06662, 0.03921, 4.788e-16, 3.381e-16, 1.578e-17 |
| Δz(F)/Δt | 0.2564, 0.1504, 0.1277, 0.1005, 0.03143, 0.0168, 0.01263, 0.004539, 0.002734, 0.001513, 2.201e-17, 1.561e-17, 4.4e-18 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i rå inkrementer ΔF | -0.9982·components | 1.01878e-28 | -1.56479e-16 |
| 2 | Minste endring i rå inkrementer ΔF | -0.2229·nodes +0.7461·edges -0.2229·beta1 +0.5232·wedges -0.2616·deg_sq_sum | 2.47028e-26 | 1.10265e-15 |
| 3 | Minste endring i rå inkrementer ΔF | -0.5835·nodes +0.0855·edges -0.5835·beta1 -0.4980·wedges +0.2490·deg_sq_sum | 2.17323e-26 | 1.32498e-15 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i rå hastigheter ΔF/Δt | -0.9982·components | 6.4514e-29 | 8.83479e-17 |
| 2 | Minste endring i rå hastigheter ΔF/Δt | -0.5857·nodes +0.5562·edges -0.5857·beta1 | 1.52346e-27 | -4.432e-16 |
| 3 | Minste endring i rå hastigheter ΔF/Δt | -0.2172·nodes -0.5045·edges -0.2172·beta1 -0.7217·wedges +0.3609·deg_sq_sum | 3.78626e-26 | 6.518e-17 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i standardiserte inkrementer Δz(F) | +0.9985·z(components) | 2.12879e-33 | -1.5007e-19 |
| 2 | Minste endring i standardiserte inkrementer Δz(F) | +0.5715·z(edges) -0.4965·z(beta1) +0.4470·z(wedges) -0.4712·z(deg_sq_sum) | 1.40576e-32 | -2.45272e-20 |
| 3 | Minste endring i standardiserte inkrementer Δz(F) | -0.4680·z(edges) +0.4508·z(beta1) +0.5218·z(wedges) -0.5501·z(deg_sq_sum) | 1.92092e-32 | -6.82962e-19 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i standardiserte hastigheter Δz(F)/Δt | -0.9996·z(components) | 5.39625e-33 | -5.17138e-19 |
| 2 | Minste endring i standardiserte hastigheter Δz(F)/Δt | +0.4070·z(edges) -0.3405·z(beta1) +0.5828·z(wedges) -0.6144·z(deg_sq_sum) | 1.42578e-32 | -6.09635e-19 |
| 3 | Minste endring i standardiserte hastigheter Δz(F)/Δt | -0.6164·z(edges) +0.5777·z(beta1) +0.3655·z(wedges) -0.3853·z(deg_sq_sum) | 2.98343e-32 | 1.0517e-18 |

## Enkel drift per feature

| feature | slope | mean | std | rel_slope_per_mean |
| --- | --- | --- | --- | --- |
| tokens | 0.00265228 | 8.01639 | 1.50944 | 0.000330857 |
| nodes | 0.0120222 | 15.5902 | 5.7385 | 0.000771143 |
| edges | 0.128827 | 93.7049 | 61.3953 | 0.00137482 |
| components | 0 | 1 | 0 | 0 |
| beta1 | 0.116805 | 79.1148 | 55.7295 | 0.0014764 |
| wedges | 2.23888 | 1221.97 | 1120.87 | 0.00183219 |
| triangles | 0.578 | 327.918 | 287.218 | 0.00176264 |
| star3 | 11.8845 | 5465.66 | 6355.88 | 0.0021744 |
| c4 | 6.68848 | 3178.93 | 3545.42 | 0.002104 |
| deg_sq_sum | 4.73542 | 2631.34 | 2363.4 | 0.00179962 |
| spectral_radius | 0.00896933 | 11.3676 | 4.14775 | 0.000789026 |
| clustering | 9.59808e-05 | 0.796832 | 0.1567 | 0.000120453 |
| dim_proxy | 3.73515e-05 | 0.244125 | 0.188978 | 0.000153001 |

## Tolkning

En kandidat med liten increment_var og liten time_slope er en plausibel quasi-invariant i det aktuelle regimet.
Det er ikke et bevis på fundamental bevaring; det er en empirisk signatur av metastabilitet i valgt feature-rom.
Kandidater som er stabile både i rå og standardisert analyse er de mest interessante.
