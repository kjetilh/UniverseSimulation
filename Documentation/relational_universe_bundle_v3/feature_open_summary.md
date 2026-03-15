# Kjøringsoppsummering for feature lab

## Parametre

- steps: 80000
- seed: 13
- initial_cycle: 6
- initial_tokens: 4
- r_seed: 0.03
- r_token: 1.0
- r_birth: 0.0
- r_death: 0.0
- p_triad: 0.07
- p_del: 0.07
- p_swap: 0.06
- avoid_disconnect: True
- relocate_tokens: True
- log_every: 800

- trajectory_csv: `/mnt/data/feature_open.csv`

# Empirisk quasi-invariantanalyse

Dette dokumentet identifiserer lineære kombinasjoner av features som endrer seg minst over de loggede intervallene.
Matematisk er dette de høyre-singularvektorene til inkrementmatrisen med minst singularverdi.

## Feature-set

tokens, nodes, edges, beta1, wedges, triangles, star3, c4, deg_sq_sum, spectral_radius

## Singularverdier

| matrix | singular_values |
| --- | --- |
| ΔF | 6502, 1341, 219.9, 74.42, 60.54, 33.78, 3.22, 1.547e-13, 2.119e-14, 0 |
| ΔF/Δt | 32.72, 6.735, 1.091, 0.3717, 0.305, 0.1698, 0.01606, 8.799e-16, 1.504e-16, 0 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i rå inkrementer ΔF | +1.0000·tokens | 0 | -4.53633e-20 |
| 2 | Minste endring i rå inkrementer ΔF | -0.5769·nodes +0.5783·edges -0.5769·beta1 | 3.67355e-27 | -1.14984e-17 |
| 3 | Minste endring i rå inkrementer ΔF | +0.2419·nodes +0.4804·edges +0.2419·beta1 +0.7223·wedges -0.3612·deg_sq_sum | 6.02982e-26 | -6.40832e-17 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i hastigheter ΔF/Δt | +1.0000·tokens | 0 | -4.53633e-20 |
| 2 | Minste endring i hastigheter ΔF/Δt | -0.5700·nodes +0.5913·edges -0.5700·beta1 | 8.17869e-27 | -2.23559e-16 |
| 3 | Minste endring i hastigheter ΔF/Δt | -0.2577·nodes -0.4643·edges -0.2577·beta1 -0.7220·wedges +0.3610·deg_sq_sum | 7.30768e-26 | 1.29752e-16 |

## Enkel drift per feature

| feature | slope | mean | std | rel_slope_per_mean |
| --- | --- | --- | --- | --- |
| tokens | -4.53633e-20 | 4 | 0 | -1.13408e-20 |
| nodes | 0.0319466 | 316.406 | 185.356 | 0.000100967 |
| edges | 0.0496747 | 502.861 | 288.526 | 9.87841e-05 |
| beta1 | 0.0177282 | 187.455 | 104.107 | 9.45727e-05 |
| wedges | 0.22109 | 2341.55 | 1302.48 | 9.44202e-05 |
| triangles | 0.0129037 | 136.545 | 77.211 | 9.45017e-05 |
| star3 | 0.513286 | 5908.94 | 3309.39 | 8.6866e-05 |
| c4 | 0.0225348 | 245.584 | 140.075 | 9.17598e-05 |
| deg_sq_sum | 0.54153 | 5688.83 | 3177.65 | 9.51917e-05 |
| spectral_radius | 6.93907e-05 | 6.33724 | 0.947507 | 1.09497e-05 |

## Tolkning

En kandidat med liten increment_var og liten time_slope er en plausibel quasi-invariant i det aktuelle regimet.
Det er ikke et bevis på fundamental bevaring; det er en empirisk signatur av metastabilitet i valgt feature-rom.
