# v0.11 frontier resolution

Denne runden tester et finere lokalt grid rundt `band_zero_del` og diagonalbroen, med en liten `p_swap`-akse og `frontier_triad_only` som kontroll.

## Kandidatsammendrag

| candidate | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0025_0000_swap025 | 0.649 | 0.354 | 0.347 | 0.000 | 0.169 | -0.164 | 0.132 |
| band_zero_del | 0.461 | 0.527 | 0.488 | 0.000 | 0.414 | 0.069 | -0.153 |
| bridge_0025_0000 | 0.274 | 0.700 | 0.653 | 1.000 | 0.380 | 0.195 | -0.087 |

## Pairwise-sannsynligheter

| a | b | P(a > b) |
| --- | --- | --- |
| band_zero_del | bridge_0025_0000 | 0.000 |
| band_zero_del | bridge_0025_0000_swap025 | 1.000 |
| bridge_0025_0000 | band_zero_del | 1.000 |
| bridge_0025_0000 | bridge_0025_0000_swap025 | 1.000 |
| bridge_0025_0000_swap025 | band_zero_del | 0.000 |
| bridge_0025_0000_swap025 | bridge_0025_0000 | 0.000 |

## Tolkning

- Råvinneren er `bridge_0025_0000`, mens focused-vinneren er `bridge_0025_0000_swap025`.
- Bruk `bridge_0025_0000` som operativ standardkandidat i neste runde.
