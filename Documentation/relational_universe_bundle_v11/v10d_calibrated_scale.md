# v0.10d calibrated scale rerun

Denne rerunden bruker growth-regimet `fast_balanced` og bare ensembles som faktisk realiserer reelt separerte startstørrelser.

## Kandidatsammendrag

| candidate | mean_composite | mean_repair | mean_causal | mean_quasi | mean_geom | alpha_all | alpha_large | alpha_jump | linear_margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| band_best | 0.601 | 0.681 | 0.491 | 0.680 | 0.518 | 0.320 | 0.291 | -0.028 | -0.046 |
| balanced_pdel | 0.551 | 0.532 | 0.568 | 0.582 | 0.530 | 0.316 | -0.023 | -0.339 | 0.254 |
| macro_stable | 0.434 | 0.312 | 0.445 | 0.483 | 0.585 | 0.197 | 0.108 | -0.089 | 0.097 |

## Størrelsesprofiler

| candidate | target | realized_initial | radius | overlap | quasi | composite | beta1_drift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| balanced_pdel | 48 | 48.0 | 4.00 | 0.656 | 0.854 | 0.831 | 0.50 |
| balanced_pdel | 96 | 96.0 | 8.00 | 0.322 | 0.522 | 0.351 | 2.00 |
| balanced_pdel | 192 | 192.0 | 8.00 | 0.572 | 0.535 | 0.480 | 1.50 |
| balanced_pdel | 256 | 256.0 | 7.75 | 0.525 | 0.417 | 0.541 | 1.25 |
| band_best | 48 | 48.0 | 4.75 | 0.665 | 0.911 | 0.826 | 0.25 |
| band_best | 96 | 96.0 | 6.75 | 0.486 | 0.794 | 0.593 | 1.00 |
| band_best | 192 | 192.0 | 6.75 | 0.554 | 0.535 | 0.536 | 2.00 |
| band_best | 256 | 256.0 | 10.00 | 0.462 | 0.481 | 0.448 | 2.50 |
| macro_stable | 48 | 48.0 | 6.00 | 0.574 | 0.883 | 0.704 | 0.50 |
| macro_stable | 96 | 96.0 | 8.00 | 0.394 | 0.409 | 0.378 | 1.25 |
| macro_stable | 192 | 192.0 | 8.00 | 0.426 | 0.224 | 0.305 | 2.00 |
| macro_stable | 256 | 256.0 | 9.25 | 0.436 | 0.418 | 0.350 | 2.00 |

## Tolkning

Hvis ekstreme eller negative eksponenter forsvinner når startstørrelsene faktisk separerer, er det et tegn på at tidligere funn var generatorartefakter.
Hvis en kandidat fortsatt ser dårlig ut etter kalibrering, er det mer rimelig å tolke det som en dynamisk svakhet ved selve kandidaten.

