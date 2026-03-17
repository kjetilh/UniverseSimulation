# Relasjonell universgraf v0.10e: fokusert band-validering under anbefalt ensemble-regime

## Formål

Denne runden bruker bare anbefalt generatorregime `fast_balanced` på deep-ensembler, med et smalt lokalt kandidatbånd rundt `band_best`. Målet er ikke å lage et nytt bredt atlas, men å sjekke om `band_best` fortsatt står seg når vi (i) øker replikasjonen moderat, (ii) holder startregimet fast, og (iii) undersøker noen få nærliggende parameterperturbasjoner.

## Realiserte startstørrelser

| target | mean_initial | q10 | q90 | separated_from_prev | mean_tokens | mean_beta1 | mean_triangles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 | 5.7 | 4.7 | 3.0 |
| 96 | 96.0 | 96.0 | 96.0 | 1 | 6.7 | 12.0 | 11.3 |
| 192 | 192.0 | 192.0 | 192.0 | 1 | 8.3 | 27.3 | 24.3 |
| 256 | 256.0 | 256.0 | 256.0 | 1 | 9.3 | 34.0 | 31.3 |

## Kandidatsammendrag

| candidate | focused_score | mean_composite | CI low composite | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| band_best | 0.708 | 0.541 | 0.471 | 0.064 | 0.176 | -0.085 | 0.267 | -0.062 |
| band_zero_del | 0.611 | 0.604 | 0.522 | 0.400 | 0.081 | -0.104 | 0.128 | -0.201 |
| band_small_death | 0.579 | 0.575 | 0.475 | 0.212 | 0.116 | -0.042 | 0.095 | -0.239 |
| band_small_triad | 0.341 | 0.592 | 0.484 | 0.292 | 0.357 | 0.049 | 0.063 | -0.289 |
| macro_stable | 0.336 | 0.483 | 0.428 | 0.032 | 0.169 | -0.123 | 0.277 | -0.344 |

## Pairwise sannsynligheter (mean composite)

| a | b | P(a > b) |
| --- | --- | --- |
| band_best | band_small_death | 0.380 |
| band_best | band_small_triad | 0.344 |
| band_best | band_zero_del | 0.204 |
| band_best | macro_stable | 0.732 |
| band_small_death | band_best | 0.620 |
| band_small_death | band_small_triad | 0.432 |
| band_small_death | band_zero_del | 0.356 |
| band_small_death | macro_stable | 0.816 |
| band_small_triad | band_best | 0.656 |
| band_small_triad | band_small_death | 0.568 |
| band_small_triad | band_zero_del | 0.388 |
| band_small_triad | macro_stable | 0.824 |
| band_zero_del | band_best | 0.796 |
| band_zero_del | band_small_death | 0.644 |
| band_zero_del | band_small_triad | 0.612 |
| band_zero_del | macro_stable | 0.908 |
| macro_stable | band_best | 0.268 |
| macro_stable | band_small_death | 0.184 |
| macro_stable | band_small_triad | 0.176 |
| macro_stable | band_zero_del | 0.092 |

## Størrelsesprofiler

| candidate | target | realized_initial | radius | overlap | quasi | composite | beta1_drift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| band_best | 48 | 48.0 | 5.11 | 0.633 | 0.850 | 0.764 | 0.33 |
| band_best | 96 | 96.0 | 7.00 | 0.573 | 0.457 | 0.467 | 0.56 |
| band_best | 192 | 192.0 | 8.22 | 0.661 | 0.534 | 0.533 | 0.78 |
| band_best | 256 | 256.0 | 8.44 | 0.608 | 0.358 | 0.402 | 1.33 |
| band_small_death | 48 | 48.0 | 6.00 | 0.561 | 0.683 | 0.596 | 0.33 |
| band_small_death | 96 | 96.0 | 6.78 | 0.681 | 0.617 | 0.601 | 0.67 |
| band_small_death | 192 | 192.0 | 9.56 | 0.741 | 0.496 | 0.550 | 0.67 |
| band_small_death | 256 | 256.0 | 7.11 | 0.685 | 0.369 | 0.551 | 1.67 |
| band_small_triad | 48 | 48.0 | 4.56 | 0.634 | 0.830 | 0.695 | 0.78 |
| band_small_triad | 96 | 96.0 | 5.44 | 0.681 | 0.547 | 0.627 | 0.89 |
| band_small_triad | 192 | 192.0 | 7.67 | 0.731 | 0.433 | 0.627 | 1.44 |
| band_small_triad | 256 | 256.0 | 8.00 | 0.639 | 0.237 | 0.419 | 2.44 |
| band_zero_del | 48 | 48.0 | 5.22 | 0.559 | 0.845 | 0.701 | 0.00 |
| band_zero_del | 96 | 96.0 | 7.00 | 0.464 | 0.744 | 0.527 | 0.00 |
| band_zero_del | 192 | 192.0 | 7.11 | 0.663 | 0.583 | 0.640 | 0.00 |
| band_zero_del | 256 | 256.0 | 7.78 | 0.597 | 0.553 | 0.547 | 0.00 |
| macro_stable | 48 | 48.0 | 4.89 | 0.619 | 0.831 | 0.745 | 0.44 |
| macro_stable | 96 | 96.0 | 7.11 | 0.566 | 0.613 | 0.474 | 0.89 |
| macro_stable | 192 | 192.0 | 8.89 | 0.578 | 0.257 | 0.337 | 1.22 |
| macro_stable | 256 | 256.0 | 8.33 | 0.529 | 0.313 | 0.375 | 1.33 |

## Tolkning

Hvis `band_best` fortsatt vinner eller ligger svært høyt mot sine nærmeste naboer, er det et tegn på at v0.10d ikke bare var et generatorartefakt. Hvis en nær nabo overtar på både `CI low composite` og mer stabile asymptotiske mål, er det et signal om at prosjektet nå bør flytte sentrum litt bort fra den gamle referansekandidaten.

Merk at dette fortsatt er en fokusert metodisk test. Resultatene sier noe om robusthet innen det anbefalte ensemble-regimet og i et lite lokalt parameterbånd, ikke om en ferdig fysisk teori.

