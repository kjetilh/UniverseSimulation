# Relasjonell universgraf v0.10f: frontier-runde rundt band_zero_del og band_small_triad

## Formål

Denne runden gjør det neste naturlige metodiske steget etter v0.10e: vi holder generatoren fast på `fast_balanced / deep`, øker growth-seed-variasjonen i en smal lokal scan, og bruker deretter ekstra run-seed-replikasjon på den ankerbaserte fronten. Målet er å avgjøre om fronten fortsatt er todelt, om den smelter sammen til én kandidat, eller om en tredje lokal nabo begynner å dominere.

## Realiserte startstørrelser

| target | mean_initial | q10 | q90 | separated_from_prev | mean_tokens | mean_beta1 |
| --- | --- | --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 | 6.0 | 7.2 |
| 96 | 96.0 | 96.0 | 96.0 | 1 | 7.8 | 11.8 |
| 192 | 192.0 | 192.0 | 192.0 | 1 | 9.5 | 26.0 |
| 256 | 256.0 | 256.0 | 256.0 | 1 | 9.5 | 39.8 |

## Bred frontier-scan

| candidate | family | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontier_diag_mid | diagonal_bridge | 0.672 | 0.578 | 0.517 | 0.017 | 0.055 | -0.057 | 0.091 | -0.094 |
| frontier_zero_del_swap025 | zero_del_family | 0.621 | 0.658 | 0.589 | 0.211 | 0.161 | -0.081 | 0.120 | -0.143 |
| frontier_triad_only | triad_axis | 0.598 | 0.582 | 0.522 | 0.011 | 0.162 | -0.060 | 0.008 | 0.088 |
| band_zero_del | zero_del_family | 0.480 | 0.686 | 0.628 | 0.566 | 0.345 | 0.026 | -0.059 | -0.178 |
| band_best | reference_axis | 0.426 | 0.382 | 0.381 | 0.000 | 0.095 | -0.084 | 0.074 | -0.151 |
| band_small_triad | small_triad_family | 0.400 | 0.421 | 0.390 | 0.000 | -0.031 | -0.064 | 0.021 | -0.358 |
| frontier_small_triad_swap015 | small_triad_family | 0.267 | 0.648 | 0.583 | 0.194 | 0.316 | 0.103 | 0.008 | -0.328 |

## Finalister med ekstra run-seeds

| candidate | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontier_diag_mid | 0.714 | 0.585 | 0.515 | 0.209 | 0.087 | -0.064 | 0.058 | -0.157 |
| band_zero_del | 0.666 | 0.637 | 0.575 | 0.791 | 0.251 | -0.021 | 0.049 | -0.132 |
| band_small_triad | 0.382 | 0.386 | 0.353 | 0.000 | 0.102 | 0.011 | 0.039 | -0.283 |

## Pairwise sannsynligheter i finalefeltet

| a | b | P(a > b) |
| --- | --- | --- |
| band_small_triad | band_zero_del | 0.000 |
| band_small_triad | frontier_diag_mid | 0.009 |
| band_zero_del | band_small_triad | 1.000 |
| band_zero_del | frontier_diag_mid | 0.791 |
| frontier_diag_mid | band_small_triad | 0.991 |
| frontier_diag_mid | band_zero_del | 0.209 |

## Tolkning

Hvis `band_zero_del` og `band_small_triad` fortsatt begge ligger i toppen etter ekstra run-seeds, bør prosjektet foreløpig holde to kandidater åpne. Hvis én av dem begynner å dominere også i det utvidede finalefeltet, er det grunnlag for å gjøre den til operativ standard i neste runde. Hvis en tredje lokal nabo tar over, er det et tegn på at fronten fortsatt må kartlegges litt finere før vi låser oss til én etikett.

