# v0.11 frontier resolution

Denne runden tester et finere lokalt grid rundt `band_zero_del` og diagonalbroen, med en liten `p_swap`-akse og `frontier_triad_only` som kontroll.

## Kandidatsammendrag

| candidate | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0025_0000 | 0.800 | 0.647 | 0.622 | 0.950 | 0.674 | 0.271 | -0.199 |
| band_zero_del | 0.200 | 0.536 | 0.501 | 0.050 | 0.716 | 0.273 | -0.218 |

## Pairwise-sannsynligheter

| a | b | P(a > b) |
| --- | --- | --- |
| band_zero_del | bridge_0025_0000 | 0.050 |
| bridge_0025_0000 | band_zero_del | 0.950 |

## Tolkning

- Råvinner og focused-vinner har konvergert til `bridge_0025_0000`.
- Bruk `bridge_0025_0000` som operativ standardkandidat i neste runde.
