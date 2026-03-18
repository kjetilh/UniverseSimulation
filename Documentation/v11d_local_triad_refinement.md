# Relasjonell universgraf v0.11d: lokal triad-raffinement rundt bridge_0010_0000

## Repo-verifisert utgangspunkt

- On-disk v11c files support bridge_0010_0000 as the live operational frontier winner.
- v11c raw-vinner: `bridge_0010_0000`.
- v11c CI-low-vinner: `bridge_0010_0000`.
- v11c pairwise-vinner: `bridge_0010_0000`.
- v11c focused-vinner: `band_zero_del`.
- Pairwise i v11c: `P(bridge_0010_0000 > band_zero_del) = 0.942`, `P(band_zero_del > bridge_0010_0000) = 0.058`.

## Eksperimentdesign

Denne runden holder modellen fast og raffinerer bare den lokale `p_triad`-aksen ved fast `p_swap = 0.02` og `p_del = 0.0`.
Kandidatsettet er smalt for a bruke budsjettet pa diskriminering, ikke pa bredde.

## Realiserte startstørrelser

| target | mean_initial | q10 | q90 | separated_from_prev | mean_tokens | mean_beta1 | mean_triangles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 | 5.5 | 4.5 | 3.0 |
| 96 | 96.0 | 96.0 | 96.0 | 1 | 7.5 | 9.0 | 7.5 |
| 192 | 192.0 | 192.0 | 192.0 | 1 | 8.0 | 21.8 | 17.8 |
| 256 | 256.0 | 256.0 | 256.0 | 1 | 6.8 | 31.2 | 29.2 |

Generator-lesning: hvis disse startnivåene ikke separerer, er frontier-lesningen metodisk skjør.

## Kandidatsammendrag

| candidate | focused_score | mean_composite | CI low | top_prob | pairwise_mean | pairwise_min | alpha_large | alpha_jump |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| band_zero_del | 0.732 | 0.609 | 0.559 | 0.383 | 0.803 | 0.489 | 0.483 | 0.121 |
| bridge_00075_0000 | 0.914 | 0.607 | 0.557 | 0.422 | 0.814 | 0.511 | 0.455 | 0.200 |
| bridge_00125_0000 | 0.498 | 0.568 | 0.493 | 0.144 | 0.589 | 0.250 | 0.506 | 0.285 |
| bridge_0010_0000 | 0.424 | 0.560 | 0.502 | 0.039 | 0.528 | 0.161 | 0.587 | 0.247 |
| bridge_0015_0000 | 0.128 | 0.488 | 0.440 | 0.011 | 0.258 | 0.022 | 0.693 | 0.370 |
| bridge_0005_0000 | 0.472 | 0.374 | 0.371 | 0.000 | 0.008 | 0.000 | 0.430 | 0.176 |

## Pairwise-matrise

| a \\ b | bridge_00075_0000 | band_zero_del | bridge_00125_0000 | bridge_0005_0000 | bridge_0010_0000 | bridge_0015_0000 |
| --- | --- | --- | --- | --- | --- | --- |
| bridge_00075_0000 | — | 0.511 | 0.744 | 1.000 | 0.839 | 0.978 |
| band_zero_del | 0.489 | — | 0.750 | 1.000 | 0.822 | 0.956 |
| bridge_00125_0000 | 0.256 | 0.250 | — | 1.000 | 0.572 | 0.867 |
| bridge_0005_0000 | 0.000 | 0.000 | 0.000 | — | 0.000 | 0.039 |
| bridge_0010_0000 | 0.161 | 0.178 | 0.428 | 1.000 | — | 0.872 |
| bridge_0015_0000 | 0.022 | 0.044 | 0.133 | 0.961 | 0.128 | — |

## Operativ lesning

1. Høyest raw `mean_composite`: `band_zero_del`.
2. Sterkest `CI low`: `band_zero_del`.
3. Sterkest pairwise-bootstrap: `bridge_00075_0000`.
4. Beste focused/local score: `bridge_00075_0000`.
5. Status: `unresolved`.

## Tolkning

- Raw, CI-low, pairwise og/eller generator-kontroll gir ikke et rent nok bilde til a kalle dette et robust lokalt optimum.
- Focused-score peker fortsatt mot `bridge_00075_0000`, men det avgjor ikke frontier alene hvis raw/CI/pairwise peker et annet sted.

## Hva som er hva

- Algebraiske identiteter: ikke det som avgjor frontieren her.
- Generatorartefakter: vurderes via target summary; hvis separasjonen bryter sammen, ma frontier-tolkningen holdes tilbake.
- Scoringartefakter: focused-score holdes separat fra raw/CI/pairwise og kan ikke alene avgjore standardkandidat.
- Dynamiske resultater: raw score, CI-low og pairwise under ren size-separasjon er den operative kjernen.

## Operativ dom

Hold frontier-lesningen apen videre; metrikken eller generator-kontrollen er fortsatt for splittet til a kalle dette avgjort.
