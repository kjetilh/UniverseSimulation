# v0.10d calibrated scale rerun

Denne rerunden bruker growth-regimet `fast_balanced` og bare ensembles som faktisk realiserer reelt separerte startstørrelser.

Valgte operative nominelle nivåer: 48, 96, 128, 160, 192, 256

## Realiserte startstørrelser

| target | mean_realized_initial | q10 | q90 | selected |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 128 | 128.0 | 128.0 | 128.0 | 1 |
| 160 | 160.0 | 160.0 | 160.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Kandidatsammendrag

| candidate | mean_composite | ci_low | ci_high | mean_repair | mean_causal | mean_quasi | alpha_all | alpha_large | alpha_jump | linear_margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| band_best | 0.606 | 0.489 | 0.602 | 0.653 | 0.492 | 0.621 | 0.323 | 0.657 | 0.334 | -0.058 |
| macro_stable | 0.468 | 0.479 | 0.597 | 0.376 | 0.449 | 0.492 | 0.187 | 0.116 | -0.071 | 0.104 |
| balanced_pdel | 0.463 | 0.425 | 0.561 | 0.424 | 0.424 | 0.432 | 0.368 | -0.267 | -0.635 | 0.315 |

## Størrelsesprofiler

| candidate | target | realized_initial | radius | overlap | quasi | composite | beta1_drift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| balanced_pdel | 48 | 48.0 | 4.00 | 0.656 | 0.752 | 0.777 | 0.50 |
| balanced_pdel | 96 | 96.0 | 8.00 | 0.322 | 0.448 | 0.396 | 2.00 |
| balanced_pdel | 128 | 128.0 | 8.00 | 0.562 | 0.568 | 0.570 | 1.25 |
| balanced_pdel | 160 | 160.0 | 8.75 | 0.343 | 0.112 | 0.238 | 2.50 |
| balanced_pdel | 192 | 192.0 | 9.50 | 0.290 | 0.299 | 0.233 | 1.25 |
| balanced_pdel | 256 | 256.0 | 7.75 | 0.525 | 0.411 | 0.564 | 1.25 |
| band_best | 48 | 48.0 | 4.75 | 0.665 | 0.830 | 0.797 | 0.25 |
| band_best | 96 | 96.0 | 6.75 | 0.486 | 0.738 | 0.619 | 1.00 |
| band_best | 128 | 128.0 | 6.50 | 0.736 | 0.720 | 0.786 | 1.75 |
| band_best | 160 | 160.0 | 7.25 | 0.296 | 0.301 | 0.266 | 2.00 |
| band_best | 192 | 192.0 | 7.00 | 0.601 | 0.742 | 0.705 | 1.00 |
| band_best | 256 | 256.0 | 10.00 | 0.462 | 0.397 | 0.461 | 2.50 |
| macro_stable | 48 | 48.0 | 6.00 | 0.574 | 0.803 | 0.681 | 0.50 |
| macro_stable | 96 | 96.0 | 8.00 | 0.394 | 0.323 | 0.379 | 1.25 |
| macro_stable | 128 | 128.0 | 8.75 | 0.618 | 0.740 | 0.630 | 0.75 |
| macro_stable | 160 | 160.0 | 9.00 | 0.339 | 0.219 | 0.262 | 2.50 |
| macro_stable | 192 | 192.0 | 7.25 | 0.422 | 0.537 | 0.473 | 1.50 |
| macro_stable | 256 | 256.0 | 9.25 | 0.436 | 0.330 | 0.382 | 2.00 |

## Tolkning

Hvis ekstreme eller negative eksponenter forsvinner når startstørrelsene faktisk separerer, er det et tegn på at tidligere funn var generatorartefakter.
Hvis en kandidat fortsatt ser dårlig ut etter kalibrering, er det mer rimelig å tolke det som en dynamisk svakhet ved selve kandidaten.

