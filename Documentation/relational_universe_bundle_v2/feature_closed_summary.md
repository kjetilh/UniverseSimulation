# Kjøringsoppsummering for feature lab

## Parametre

- steps: 50000
- seed: 11
- initial_cycle: 6
- initial_tokens: 4
- r_seed: 0.05
- r_token: 1.0
- r_birth: 0.0
- r_death: 0.0
- p_triad: 0.0
- p_del: 0.0
- p_swap: 0.12
- avoid_disconnect: True
- relocate_tokens: True
- log_every: 500

- trajectory_csv: `/mnt/data/feature_closed.csv`

# Empirisk quasi-invariantanalyse

Dette dokumentet identifiserer lineære kombinasjoner av features som endrer seg minst over de loggede intervallene.
Matematisk er dette de høyre-singularvektorene til inkrementmatrisen med minst singularverdi.

## Feature-set

tokens, nodes, edges, beta1, wedges, triangles, star3, c4, deg_sq_sum, spectral_radius

## Singularverdier

| matrix | singular_values |
| --- | --- |
| ΔF | 3811, 462.1, 28.48, 2.297, 1.521, 0.7824, 8.795e-14, 1.444e-14, 1.732e-15, 0 |
| ΔF/Δt | 30.89, 3.761, 0.2316, 0.01823, 0.01254, 0.006333, 3.719e-16, 1.219e-16, 6.206e-18, 0 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i rå inkrementer ΔF | +1.0000·tokens | 0 | 9.25654e-20 |
| 2 | Minste endring i rå inkrementer ΔF | +0.9995·beta1 | 3.15689e-30 | 8.42841e-18 |
| 3 | Minste endring i rå inkrementer ΔF | +0.6503·nodes -0.7506·edges -0.1003·wedges | 4.78534e-27 | -3.43312e-16 |

| rank | type | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- | --- |
| 1 | Minste endring i hastigheter ΔF/Δt | +1.0000·tokens | 0 | 9.25654e-20 |
| 2 | Minste endring i hastigheter ΔF/Δt | +0.9989·beta1 | 5.71172e-30 | -1.05995e-17 |
| 3 | Minste endring i hastigheter ΔF/Δt | +0.6771·nodes -0.7318·edges | 1.5007e-27 | -4.14814e-18 |

## Enkel drift per feature

| feature | slope | mean | std | rel_slope_per_mean |
| --- | --- | --- | --- | --- |
| tokens | 9.25654e-20 | 4 | 0 | 2.31414e-20 |
| nodes | 0.0490322 | 300.545 | 175.401 | 0.000163145 |
| edges | 0.0490322 | 300.545 | 175.401 | 0.000163145 |
| beta1 | 2.31414e-20 | 1 | 0 | 2.31414e-20 |
| wedges | 0.261262 | 1362.58 | 940.135 | 0.00019174 |
| triangles | -2.63383e-05 | 0.0594059 | 0.236383 | -0.000443361 |
| star3 | 1.54823 | 6757.35 | 5716.82 | 0.000229118 |
| c4 | -3.88778e-06 | 0.00990099 | 0.0990099 | -0.000392666 |
| deg_sq_sum | 0.620588 | 3326.26 | 2229.48 | 0.000186572 |
| spectral_radius | 0.000238926 | 4.68948 | 0.931042 | 5.09494e-05 |

## Tolkning

En kandidat med liten increment_var og liten time_slope er en plausibel quasi-invariant i det aktuelle regimet.
Det er ikke et bevis på fundamental bevaring; det er en empirisk signatur av metastabilitet i valgt feature-rom.
