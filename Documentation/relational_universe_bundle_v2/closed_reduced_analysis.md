# Redusert quasi-invariantanalyse

## Feature-set

tokens, nodes, beta1, wedges, triangles, star3, c4, spectral_radius

## Singularverdier

- ΔF: 3713, 177, 20.39, 2.297, 1.521, 0.7823, 3.17e-15, 0
- ΔF/Δt: 30.1, 1.44, 0.1659, 0.01823, 0.01254, 0.006333, 1.226e-17, 0

## Minste endring i rå inkrementer ΔF

| rank | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- |
| 1 | +1.0000·tokens | 0 | 9.25654e-20 |
| 2 | -1.0000·beta1 | 1.9738e-27 | 2.0985e-16 |
| 3 | +0.5349·triangles +0.5519·c4 -0.6397·spectral_radius | 0.00610991 | 4.84998e-05 |
| 4 | -0.1302·triangles +0.8019·c4 +0.5831·spectral_radius | 0.023135 | -6.97965e-05 |

## Minste endring i hastigheter ΔF/Δt

| rank | combinasjon | increment_var | time_slope |
| --- | --- | --- | --- |
| 1 | +1.0000·tokens | 0 | 9.25654e-20 |
| 2 | -1.0000·beta1 | 6.00753e-29 | 3.49474e-17 |
| 3 | +0.5315·triangles +0.5499·c4 -0.6442·spectral_radius | 0.00611015 | 5.35581e-05 |
| 4 | -0.1496·triangles +0.8095·c4 +0.5677·spectral_radius | 0.0231589 | -5.9237e-05 |
