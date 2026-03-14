# Kjøringsoppsummering for feature lab

## Parametre

- steps: 12000
- seed: 31
- initial_cycle: 10
- initial_tokens: 6
- r_seed: 0.0
- r_token: 1.0
- r_birth: 0.0
- r_death: 0.0
- p_triad: 0.0
- p_del: 0.0
- p_swap: 0.18
- avoid_disconnect: True
- relocate_tokens: False
- log_every: 200

- trajectory_csv: `Documentation/feature_lab_regimes/closed_topological_sector.csv`

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
| tokens | 6 | 0 | 6 | 6 |
| nodes | 10 | 0 | 10 | 10 |
| edges | 10 | 0 | 10 | 10 |
| components | 1 | 0 | 1 | 1 |
| beta1 | 1 | 0 | 1 | 1 |
| wedges | 16.3607 | 2.63664 | 10 | 26 |
| triangles | 0.442623 | 0.496697 | 0 | 1 |
| star3 | 9.16393 | 5.65738 | 0 | 36 |
| c4 | 0.344262 | 0.475127 | 0 | 1 |
| deg_sq_sum | 52.7213 | 5.27329 | 40 | 72 |
| spectral_radius | 2.49877 | 0.146162 | 2 | 2.91268 |
| clustering | 0.0657611 | 0.0791677 | 0 | 0.216667 |
| dim_proxy | 0.889378 | 0.0818281 | 0.66797 | 1.07564 |

## Singularverdier

| matrix | singular_values |
| --- | --- |
| ΔF | 78.84, 9.781, 6.159, 2.879, 0.6281, 0.4796, 0.2495, 4.158e-15, 9.435e-16, 4.539e-16, 2.949e-16, 1.119e-16, 0 |
| ΔF/Δt | 2.306, 0.2861, 0.1807, 0.08654, 0.01853, 0.0142, 0.007303, 6.211e-17, 3.941e-17, 1.125e-17, 8.206e-18, 5.329e-18, 0 |
| Δz(F) | 20.82, 14.51, 8.394, 6.345, 4.637, 1.789, 1.461, 2.469e-15, 1.213e-15, 6.552e-16, 4.44e-16, 3.048e-16, 0 |
| Δz(F)/Δt | 0.6207, 0.4241, 0.252, 0.1868, 0.1367, 0.05206, 0.04267, 4.306e-17, 1.638e-17, 1.431e-17, 1.303e-17, 4.749e-18, 0 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i rå inkrementer ΔF | +1.0000·tokens | 0 | 7.75369e-19 |
| 2 | Minste endring i rå inkrementer ΔF | -0.0945·nodes +0.6277·edges +0.7723·beta1 | 5.91427e-31 | 2.32611e-18 |
| 3 | Minste endring i rå inkrementer ΔF | +0.5046·edges +0.7470·components -0.4253·beta1 | 3.54768e-31 | 1.55074e-18 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i rå hastigheter ΔF/Δt | +1.0000·tokens | 0 | 7.75369e-19 |
| 2 | Minste endring i rå hastigheter ΔF/Δt | +0.7276·edges -0.6669·components +0.1456·beta1 | 4.19849e-31 | 0 |
| 3 | Minste endring i rå hastigheter ΔF/Δt | +0.2685·components +0.9617·beta1 | 4.10865e-32 | 5.81527e-19 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i standardiserte inkrementer Δz(F) | +1.0000·z(tokens) | 0 | 0 |
| 2 | Minste endring i standardiserte inkrementer Δz(F) | -0.2506·z(nodes) +0.1678·z(edges) -0.8563·z(components) -0.4183·z(beta1) | 6.59024e-32 | 9.5995e-22 |
| 3 | Minste endring i standardiserte inkrementer Δz(F) | +0.3443·z(nodes) -0.4819·z(components) +0.8035·z(beta1) | 1.11168e-31 | -6.63039e-20 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i standardiserte hastigheter Δz(F)/Δt | +1.0000·z(tokens) | 0 | 0 |
| 2 | Minste endring i standardiserte hastigheter Δz(F)/Δt | -0.4365·z(nodes) +0.4171·z(edges) -0.1047·z(components) -0.7844·z(beta1) | 1.31306e-31 | 4.41926e-20 |
| 3 | Minste endring i standardiserte hastigheter Δz(F)/Δt | +0.3956·z(nodes) +0.1317·z(edges) +0.8127·z(components) -0.2166·z(beta1) +0.2436·z(wedges) -0.2436·z(deg_sq_sum) | 1.66993e-32 | -9.39268e-21 |

## Enkel drift per feature

| feature | slope | mean | std | rel_slope_per_mean |
| --- | --- | --- | --- | --- |
| tokens | 7.75369e-19 | 6 | 0 | 1.29228e-19 |
| nodes | 1.55074e-18 | 10 | 0 | 1.55074e-19 |
| edges | 1.55074e-18 | 10 | 0 | 1.55074e-19 |
| components | 9.69211e-20 | 1 | 0 | 9.69211e-20 |
| beta1 | 9.69211e-20 | 1 | 0 | 9.69211e-20 |
| wedges | 0.000624272 | 16.3607 | 2.63664 | 3.81569e-05 |
| triangles | 0.000108466 | 0.442623 | 0.496697 | 0.000245053 |
| star3 | 0.00109296 | 9.16393 | 5.65738 | 0.000119268 |
| c4 | -3.37641e-05 | 0.344262 | 0.475127 | -9.80766e-05 |
| deg_sq_sum | 0.00124854 | 52.7213 | 5.27329 | 2.3682e-05 |
| spectral_radius | 1.8179e-05 | 2.49877 | 0.146162 | 7.27519e-06 |
| clustering | 1.36846e-05 | 0.0657611 | 0.0791677 | 0.000208095 |
| dim_proxy | -8.7252e-06 | 0.889378 | 0.0818281 | -9.81044e-06 |

## Tolkning

En kandidat med liten increment_var og liten time_slope er en plausibel quasi-invariant i det aktuelle regimet.
Det er ikke et bevis på fundamental bevaring; det er en empirisk signatur av metastabilitet i valgt feature-rom.
Kandidater som er stabile både i rå og standardisert analyse er de mest interessante.
