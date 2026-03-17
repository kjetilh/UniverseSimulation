# Relasjonell universgraf v0.11b: bridge-corridor resolution

## Repo-verifisert arbeidshypotese

- On-disk v0.11 files support the bridge-corridor reading.
- Tidligere lokal råvinner: `bridge_0025_0000`.
- Tidligere lokal focused-vinner: `bridge_0025_0000_swap025`.
- Pairwise fra v0.11 mid focus: `P(bridge_0025_0000 > band_zero_del) = 1.000`, `P(bridge_0025_0000 > bridge_0025_0000_swap025) = 1.000`.

## Eksperimentdesign

Denne runden bruker et smalt, lokalt bridge-grid med `p_del = 0` overalt.
Kandidatene varierer bare `p_triad` rundt `0.0025` og `p_swap` rundt `0.020-0.025`.
`band_zero_del` beholdes som kontroll, ikke som forhåndsantatt vinner.

## Realiserte startstørrelser

| target | mean_initial | q10 | q90 | separated_from_prev | mean_tokens | mean_beta1 | mean_triangles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 | 6.5 | 5.5 | 4.5 |
| 96 | 96.0 | 96.0 | 96.0 | 1 | 9.0 | 10.5 | 9.0 |
| 192 | 192.0 | 192.0 | 192.0 | 1 | 9.5 | 23.5 | 21.0 |
| 256 | 256.0 | 256.0 | 256.0 | 1 | 8.0 | 36.5 | 36.0 |

Generator-lesning: dette er metodisk input, ikke dynamisk resultat. Hvis `separated_from_prev` faller, er det et generatorproblem.

## Broad-runde

| candidate | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0015_0000 | 0.594 | 0.717 | 0.623 | 0.850 | -0.020 | -0.250 | 0.097 | 0.131 |
| bridge_0025_0000_swap025 | 0.484 | 0.499 | 0.477 | 0.000 | 0.123 | -0.202 | 0.310 | 0.149 |
| bridge_0035_0000 | 0.444 | 0.566 | 0.509 | 0.000 | 0.185 | -0.205 | 0.383 | -0.117 |
| band_zero_del | 0.441 | 0.626 | 0.549 | 0.150 | 0.412 | 0.041 | 0.100 | -0.032 |
| bridge_0025_0000_swap0225 | 0.377 | 0.552 | 0.493 | 0.000 | 0.177 | -0.127 | 0.232 | -0.262 |
| bridge_0025_0000 | 0.288 | 0.559 | 0.499 | 0.000 | 0.298 | -0.246 | 0.506 | -0.453 |

## Finalister

| candidate | focused_score | mean_composite | CI low | top_prob | alpha_large | alpha_jump | linear_margin | quasi_large |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bridge_0015_0000 | 0.604 | 0.650 | 0.549 | 0.475 | 0.226 | -0.130 | 0.264 | 0.124 |
| band_zero_del | 0.537 | 0.645 | 0.588 | 0.475 | 0.241 | -0.114 | 0.262 | -0.093 |
| bridge_0025_0000_swap025 | 0.490 | 0.593 | 0.502 | 0.050 | 0.134 | -0.158 | 0.233 | -0.023 |
| bridge_0025_0000 | 0.200 | 0.462 | 0.412 | 0.000 | 0.264 | -0.184 | 0.404 | -0.208 |

## Pairwise-matrise blant finalistene

| a \\ b | bridge_0015_0000 | band_zero_del | bridge_0025_0000_swap025 | bridge_0025_0000 |
| --- | --- | --- | --- | --- |
| bridge_0015_0000 | — | 0.475 | 0.875 | 1.000 |
| band_zero_del | 0.525 | — | 0.863 | 1.000 |
| bridge_0025_0000_swap025 | 0.125 | 0.138 | — | 0.975 |
| bridge_0025_0000 | 0.000 | 0.000 | 0.025 | — |

## Tolkning

- Råvinner: `bridge_0015_0000`.
- Focused-vinner: `bridge_0015_0000`.
- Focused-vinneren `bridge_0015_0000` er også råvinner; den interne raw-vs-focused-spenningen for denne kandidaten ser derfor ut til a vaere lukket.
- Bro-korridoren er fortsatt uavklart mellom `bridge_0015_0000` og `band_zero_del`: P(bridge_0015_0000 > band_zero_del) = 0.475, P(band_zero_del > bridge_0015_0000) = 0.525, CI-low = 0.549 mot 0.588, top_prob = 0.475 mot 0.475.

## Svar pa arbeidsfragene

1. Beste operative default er ikke rent avgjort; `bridge_0015_0000` leder pa mean_composite, men `band_zero_del` henger fortsatt tett pa.
2. `bridge_0015_0000` har fordel, men det er samme kandidat som ravinneren.
3. Dermed er det ikke lenger en egen raw-vs-focused-spenning for denne kandidaten.
4. `band_zero_del` er ikke bare kontroll i denne runden; den er fortsatt en reell utfordrer.

## Hva som er hva

- Algebraiske identiteter: ingen nye påstander her; denne runden dreier seg ikke om eksakte invariants.
- Generatorartefakter: vurderes via realiserte startstørrelser og `separated_from_prev`.
- Scoringartefakter: focused-score kan løfte kandidater som ikke vinner rå pairwise.
- Dynamiske resultater: `mean_composite`, `CI low` og pairwise-sannsynligheter i finalen er de operative størrelsene.

## Operativ dom

Denne bridge-korridoren er fortsatt uavklart. Hold bade `bridge_0015_0000` og `band_zero_del` åpne videre.
