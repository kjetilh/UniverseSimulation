# Relasjonell universgraf v0.10f: frontier-runde rundt band_zero_del og band_small_triad

## Formål

Denne runden gjør det neste naturlige metodiske steget etter v0.10e: vi holder generatoren fast på `fast_balanced / deep`, øker growth-seed-variasjonen i en smal lokal scan, og bruker deretter ekstra run-seed-replikasjon på den ankerbaserte fronten. Målet er å avgjøre om fronten fortsatt er todelt, om den smelter sammen til én kandidat, eller om en tredje lokal nabo begynner å dominere.

## Realiserte startstørrelser

| target | mean_initial | q10 | q90 | separated_from_prev | mean_tokens | mean_beta1 |
| --- | --- | --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 | 6.0 | 7.2 |
| 96 | 96.0 | 96.0 | 96.0 | 1 | 7.8 | 11.8 |
| 192 | 192.0 | 192.0 | 192.0 | 1 | 9.0 | 27.0 |
| 256 | 256.0 | 256.0 | 256.0 | 1 | 9.5 | 39.8 |

## Bred frontier-scan

| candidate | family | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontier_triad_only | triad_axis | 0.792 | 0.553 | 0.502 | 0.023 | 0.166 | -0.061 | 0.197 | 0.088 |
| frontier_zero_del_swap025 | zero_del_family | 0.756 | 0.653 | 0.578 | 0.480 | 0.117 | -0.084 | 0.187 | -0.130 |
| frontier_diag_mid | diagonal_bridge | 0.588 | 0.530 | 0.482 | 0.006 | 0.116 | 0.007 | 0.051 | -0.215 |
| band_zero_del | zero_del_family | 0.544 | 0.633 | 0.591 | 0.317 | 0.375 | 0.027 | 0.108 | -0.290 |
| band_small_triad | small_triad_family | 0.446 | 0.431 | 0.400 | 0.000 | 0.071 | 0.040 | 0.007 | -0.229 |
| band_best | reference_axis | 0.396 | 0.385 | 0.374 | 0.000 | 0.202 | 0.004 | 0.045 | -0.313 |
| frontier_small_triad_swap015 | small_triad_family | 0.155 | 0.602 | 0.543 | 0.174 | 0.426 | 0.162 | 0.004 | -0.378 |

## Finalister med ekstra run-seeds

| candidate | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frontier_triad_only | 0.877 | 0.645 | 0.509 | 0.380 | 0.203 | -0.061 | 0.235 | 0.044 |
| band_zero_del | 0.546 | 0.654 | 0.558 | 0.620 | 0.315 | 0.012 | 0.139 | -0.258 |
| band_small_triad | 0.120 | 0.443 | 0.357 | 0.000 | 0.248 | 0.145 | 0.000 | -0.307 |

## Pairwise sannsynligheter i finalefeltet

| a | b | P(a > b) |
| --- | --- | --- |
| band_small_triad | band_zero_del | 0.000 |
| band_small_triad | frontier_triad_only | 0.023 |
| band_zero_del | band_small_triad | 1.000 |
| band_zero_del | frontier_triad_only | 0.620 |
| frontier_triad_only | band_small_triad | 0.977 |
| frontier_triad_only | band_zero_del | 0.380 |

## Tolkning

Hvis `band_zero_del` og `band_small_triad` fortsatt begge ligger i toppen etter ekstra run-seeds, bør prosjektet foreløpig holde to kandidater åpne. Hvis én av dem begynner å dominere også i det utvidede finalefeltet, er det grunnlag for å gjøre den til operativ standard i neste runde. Hvis en tredje lokal nabo tar over, er det et tegn på at fronten fortsatt må kartlegges litt finere før vi låser oss til én etikett.

