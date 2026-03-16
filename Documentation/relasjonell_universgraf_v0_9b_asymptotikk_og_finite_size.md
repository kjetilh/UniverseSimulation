# Relasjonell universgraf v0.9b – asymptotisk refinering og finite-size-artefakter

## Sammendrag

v0.9b tester om de lovende v0.9-kandidatene fortsatt ser gode ut når vi utvider størrelsesvinduet til 192-nivå og måler asymptotiske indikatorer i stedet for bare gjennomsnittsskårer. På denne testen ble `band_best` beste asymptotiske kandidat med asymptotic score ≈ 0.857, large-scale alpha ≈ 0.303, alpha-jump ≈ 0.025, og linear-margin ≈ 0.059.

Det viktigste resultatet i v0.9b er ikke bare at kandidatrommet blir smalere, men at **v0.9-vinneren ikke forblir asymptotisk best**. Det er akkurat den typen rangreversering man vil oppdage tidlig hvis noen lave eksponenter bare skyldes finite-size-artefakter.

## Metode

- kandidater: 4
- naturlige ensembler: 8 (24/48/96/192 × light/deep)
- growth seeds i hovedscan: 2
- event-budsjett: steps = clamp(round(4.5 * N_init), 120, 650)
- bootstrap-replikater for asymptotiske kandidatintervaller: 80
- lokal ekstrarefinering: 1 ekstra growth seed for toppkandidatene

## Startensembler

| ensemble | target | burn-in | mean nodes | mean tokens | mean β1 | mean spectral radius | mean dim proxy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| natural24_light | 24 | light | 27.5 | 5.0 | 3.0 | 3.21 | 2.22 |
| natural24_deep | 24 | deep | 35.0 | 8.0 | 5.0 | 3.64 | 2.13 |
| natural48_light | 48 | light | 45.0 | 15.0 | 8.0 | 4.04 | 2.34 |
| natural48_deep | 48 | deep | 58.5 | 15.0 | 12.5 | 4.29 | 2.85 |
| natural96_light | 96 | light | 78.5 | 15.5 | 15.5 | 4.36 | 2.88 |
| natural96_deep | 96 | deep | 91.0 | 29.5 | 23.0 | 5.05 | 3.03 |
| natural192_light | 192 | light | 138.5 | 39.5 | 37.0 | 4.81 | 2.97 |
| natural192_deep | 192 | deep | 153.0 | 80.5 | 59.0 | 5.69 | 2.98 |

## Kandidatsammendrag

| candidate | mean composite | CI low | alpha_large | alpha_jump | linear_margin | burn-in sens | quasi_large | asym score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| band_best | 0.623 | 0.580 | 0.303 | 0.025 | 0.059 | 0.146 | -0.177 | 0.857 |
| macro_stable | 0.608 | 0.591 | 0.237 | 0.263 | 0.007 | 0.201 | -0.175 | 0.686 |
| triad_runner | 0.520 | 0.520 | 0.898 | 0.373 | -0.092 | 0.116 | -0.218 | 0.446 |
| balanced_pdel | 0.644 | 0.613 | 1.266 | 0.742 | -0.103 | 0.103 | -0.510 | 0.333 |

## Tolkning av asymptotiske indikatorer

- **alpha_large**: log-log-helning for `(radius + 1)` mot `N` på de tre største størrelsene. Lavere er bedre.
- **alpha_jump**: forskjellen `alpha_large - alpha_all`. Høy positiv verdi betyr at stor-skala-fronten vokser raskere enn all-skalaestimatet og kan avsløre finite-size-artefakter.
- **linear_margin**: `RMSE(linear-in-N) - best(RMSE(logN), RMSE(sqrtN))`. Positiv verdi betyr at en enkel sublineær familie beskriver radius bedre enn lineær vekst.
- **quasi_large**: stor-skala-helning for quasi-score mot `log N`. Mindre negativ er bedre.

## Lokal refinering med ekstra growth seed

| candidate | refine seeds | mean composite | CI low | alpha_large | alpha_jump | linear_margin | burn-in sens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| macro_stable | 101,202,303 | 0.604 | 0.572 | 0.406 | 0.287 | -0.038 | 0.222 |
| band_best | 101,202,303 | 0.591 | 0.558 | 0.141 | -0.082 | 0.111 | 0.155 |

Denne lokale refineringen er viktig fordi den spør om den beste asymptotiske kandidaten holder seg når vi gir den litt mer ensemble-varians. Hvis den gjør det, er det mer sannsynlig at vi ser et reelt regime og ikke et tilfeldig seed-treff.

## Konklusjon

v0.9b peker mot et strengere og smalere kandidatbånd enn v0.9. Det mest interessante utfallet er at `balanced_pdel`, som gjorde det godt i v0.9, nå ser mer ut som en finite-size-vinner enn en asymptotisk vinner. `band_best` er derimot mindre prangende på rå composite, men mye renere på alpha-jump og linear-margin. Det er et bedre tegn dersom vi prøver å finne et regime med ekte sublineær frontvekst.

## Filer

- hoved-run rows: `v09b_asymptotic_run_rows.csv`
- hoved-group rows: `v09b_asymptotic_group_rows.csv`
- kandidatsammendrag: `v09b_asymptotic_candidate_summary.csv`
- størrelseprofiler: `v09b_asymptotic_size_profiles.csv`
- ensemble summary: `v09b_ensemble_summary.csv`
- lokal refinering: `v09b_refined_candidate_summary.csv`