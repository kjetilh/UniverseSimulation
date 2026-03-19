# Relasjonell universgraf v0.11e: band_zero_del vs bridge_00075_0000

## Repo-verifisert utgangspunkt

- On-disk v11d files support a narrow unresolved split between band_zero_del and bridge_00075_0000.
- v11d raw-vinner: `band_zero_del`.
- v11d CI-low-vinner: `band_zero_del`.
- v11d pairwise-vinner: `bridge_00075_0000`.
- v11d focused-vinner: `bridge_00075_0000`.
- v11d head-to-head: `P(bridge_00075_0000 > band_zero_del) = 0.511`, `P(band_zero_del > bridge_00075_0000) = 0.489`.

## Eksperimentdesign

Denne runden holder modellen og scoringen fast og bruker mer replikeringsbudsjett pa den smale binare duellen.

## Realiserte startstørrelser

| target | mean_initial | q10 | q90 | separated_from_prev | mean_tokens | mean_beta1 | mean_triangles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 | 6.8 | 4.0 | 2.6 |
| 96 | 96.0 | 96.0 | 96.0 | 1 | 7.2 | 11.4 | 10.0 |
| 192 | 192.0 | 192.0 | 192.0 | 1 | 9.0 | 27.2 | 25.2 |
| 256 | 256.0 | 256.0 | 256.0 | 1 | 10.6 | 33.8 | 30.4 |

## Kandidatsammendrag

| candidate | focused_score | mean_composite | CI low | top_prob | pairwise_mean | pairwise_min | alpha_large | alpha_jump |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| band_zero_del | 0.600 | 0.554 | 0.505 | 1.000 | 1.000 | 1.000 | 0.222 | -0.094 |
| bridge_00075_0000 | 0.400 | 0.417 | 0.376 | 0.000 | 0.000 | 0.000 | 0.132 | -0.156 |

## Pairwise

| a | b | P(a > b) |
| --- | --- | --- |
| band_zero_del | bridge_00075_0000 | 1.000 |
| bridge_00075_0000 | band_zero_del | 0.000 |

## Operativ lesning

1. Høyest raw `mean_composite`: `band_zero_del`.
2. Sterkest `CI low`: `band_zero_del`.
3. Sterkest pairwise-bootstrap: `band_zero_del`.
4. Beste focused/local score: `band_zero_del`.
5. Status: `resolved`.

## Tolkning

- `band_zero_del` vinner raw, CI-low og pairwise med tydelig margin mot `bridge_00075_0000`.
- Focused-score er ikke separat fra den operative lesningen i denne runden.

