# v0.10f frontier-test

Denne runden holder `fast_balanced / deep` fast og tester et lite lokalt grid rundt `band_zero_del` og `band_small_triad` med høyere replikasjon enn v0.10e.

## Kandidatsammendrag

| candidate | frontier_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| band_zero_del | 0.761 | 0.676 | 0.612 | 0.950 | -0.008 | -0.263 | 0.199 |
| band_small_death | 0.623 | 0.551 | 0.471 | 0.037 | 0.230 | 0.002 | 0.113 |
| band_best | 0.317 | 0.416 | 0.396 | 0.000 | 0.100 | -0.158 | 0.270 |
| band_small_triad | 0.015 | 0.395 | 0.366 | 0.013 | 0.604 | 0.247 | -0.182 |

## Pairwise-sannsynligheter

| a | b | P(a > b) |
| --- | --- | --- |
| band_best | band_small_death | 0.075 |
| band_best | band_small_triad | 0.562 |
| band_best | band_zero_del | 0.000 |
| band_small_death | band_best | 0.925 |
| band_small_death | band_small_triad | 0.963 |
| band_small_death | band_zero_del | 0.037 |
| band_small_triad | band_best | 0.438 |
| band_small_triad | band_small_death | 0.037 |
| band_small_triad | band_zero_del | 0.013 |
| band_zero_del | band_best | 1.000 |
| band_zero_del | band_small_death | 0.963 |
| band_zero_del | band_small_triad | 0.988 |

## Størrelsesprofiler

| candidate | target | realized_initial | radius | overlap | quasi | composite |
| --- | --- | --- | --- | --- | --- | --- |
| band_best | 48 | 48.0 | 5.38 | 0.647 | 0.757 | 0.614 |
| band_best | 96 | 96.0 | 8.00 | 0.691 | 0.640 | 0.485 |
| band_best | 192 | 192.0 | 9.00 | 0.622 | 0.403 | 0.284 |
| band_best | 256 | 256.0 | 8.81 | 0.673 | 0.383 | 0.280 |
| band_small_death | 48 | 48.0 | 5.38 | 0.626 | 0.874 | 0.609 |
| band_small_death | 96 | 96.0 | 6.19 | 0.696 | 0.760 | 0.605 |
| band_small_death | 192 | 192.0 | 8.88 | 0.671 | 0.500 | 0.405 |
| band_small_death | 256 | 256.0 | 7.56 | 0.794 | 0.672 | 0.584 |
| band_small_triad | 48 | 48.0 | 4.94 | 0.639 | 0.678 | 0.490 |
| band_small_triad | 96 | 96.0 | 4.81 | 0.714 | 0.490 | 0.560 |
| band_small_triad | 192 | 192.0 | 7.69 | 0.688 | 0.287 | 0.327 |
| band_small_triad | 256 | 256.0 | 9.56 | 0.642 | 0.210 | 0.201 |
| band_zero_del | 48 | 48.0 | 4.19 | 0.734 | 1.000 | 0.845 |
| band_zero_del | 96 | 96.0 | 6.94 | 0.686 | 0.882 | 0.656 |
| band_zero_del | 192 | 192.0 | 8.44 | 0.719 | 0.795 | 0.578 |
| band_zero_del | 256 | 256.0 | 6.44 | 0.721 | 0.732 | 0.624 |

## Operativ lesning

- Fronten smalner inn; `band_zero_del` ser ut til å ha et tydeligere overtak over `band_small_death`.
- Bruk `band_zero_del` som operativ standardkandidat og `band_small_death` som nær kontroll.
