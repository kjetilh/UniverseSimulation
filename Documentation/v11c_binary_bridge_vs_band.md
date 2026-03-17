# Relasjonell universgraf v0.11c: binary bridge vs band

## Repo-verifisert arbeidshypotese

- On-disk v0.11b files support a binary bridge_0015_0000 vs band_zero_del contest.
- v0.11b raw-vinner: `bridge_0015_0000`.
- v0.11b CI-low-vinner: `band_zero_del`.
- v0.11b focused-vinner: `bridge_0015_0000`.
- Pairwise i v0.11b: `P(bridge_0015_0000 > band_zero_del) = 0.475`, `P(band_zero_del > bridge_0015_0000) = 0.525`.

## Eksperimentdesign

Denne runden holder kandidatfamilien pa en ren lokal `p_triad`-akse ved fast `p_swap = 0.02` og `p_del = 0.0`.
Swap er ikke med i hovedgridet, fordi v0.11b ikke støttet at swap fortsatt var sentrum av frontieren.

## Realiserte startstørrelser

| target | mean_initial | q10 | q90 | separated_from_prev | mean_tokens | mean_beta1 | mean_triangles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 | 7.7 | 5.0 | 3.7 |
| 96 | 96.0 | 96.0 | 96.0 | 1 | 8.7 | 10.3 | 9.0 |
| 192 | 192.0 | 192.0 | 192.0 | 1 | 6.3 | 25.3 | 22.0 |
| 256 | 256.0 | 256.0 | 256.0 | 1 | 8.3 | 33.0 | 29.3 |

Generator-lesning: hvis disse startnivåene ikke separerer, er analysen metodisk skjør. I denne runden separerer de.

## Kandidatsammendrag

| candidate | focused_score | mean_composite | CI low | top_prob | pairwise_mean | pairwise_min | alpha_large | alpha_jump |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0010_0000 | 0.601 | 0.688 | 0.629 | 0.933 | 0.981 | 0.942 | 0.060 | -0.166 |
| band_zero_del | 0.625 | 0.570 | 0.540 | 0.058 | 0.579 | 0.058 | 0.076 | -0.146 |
| bridge_0020_0000 | 0.541 | 0.538 | 0.492 | 0.000 | 0.340 | 0.000 | 0.193 | -0.040 |
| bridge_0005_0000 | 0.431 | 0.536 | 0.492 | 0.000 | 0.294 | 0.000 | 0.003 | -0.159 |
| bridge_0015_0000 | 0.211 | 0.532 | 0.495 | 0.008 | 0.306 | 0.017 | 0.186 | -0.040 |

## Pairwise-matrise

| a \\ b | band_zero_del | bridge_0010_0000 | bridge_0020_0000 | bridge_0005_0000 | bridge_0015_0000 |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | — | 0.058 | 0.733 | 0.767 | 0.758 |
| bridge_0010_0000 | 0.942 | — | 1.000 | 1.000 | 0.983 |
| bridge_0020_0000 | 0.267 | 0.000 | — | 0.550 | 0.542 |
| bridge_0005_0000 | 0.233 | 0.000 | 0.450 | — | 0.492 |
| bridge_0015_0000 | 0.242 | 0.017 | 0.458 | 0.508 | — |

## Svar pa arbeidsfragene

1. Høyest raw `mean_composite`: `bridge_0010_0000`.
2. Sterkest `CI low`: `bridge_0010_0000`.
3. Sterkest pairwise-bootstrap: `bridge_0010_0000`.
4. Beste focused/local score: `band_zero_del`.
5. Er dette samme kandidat? Nei.
6. Resultatstatus: `resolved`.

## Tolkning

- `bridge_0010_0000` er robust nok til a regnes som vinner: raw, CI-low og pairwise peker samme vei, og P(bridge_0010_0000 > band_zero_del) = 0.942.
- Focused-score peker mot `band_zero_del`, men det er ikke nok alene til a overstyre raw/CI/pairwise.

## Hva som er hva

- Generatorstabilitet: vurderes via de realiserte startstørrelsene over de fire nivåene.
- Scoringartefakter: focused-score holdes separat fra raw/CI/pairwise og skal ikke alene avgjøre vinner.
- Finite-sample-ambiguity: hvis raw, CI-low og pairwise peker ulikt, er resultatet fortsatt uavklart.
- Robust dynamisk fordel: krever at samme kandidat dominerer flere operative mål samtidig.

## Operativ dom

Bruk `bridge_0010_0000` som standardkandidat videre.
