# Status v0.10f

## Hvor vi er

Prosjektet er nå forbi generator- og ensemblekrisen som preget v0.10/v0.10b. I v0.10f var de realiserte startstørrelsene 48, 96, 192 og 256 nøyaktig separert. Dermed er resultatene i denne runden i hovedsak dynamiske.

## Hva som skjedde i v0.10f

Vi kjørte en smal frontier-runde rundt den operative fronten fra v0.10e:

- `band_zero_del`
- `band_small_triad`

med en ny lokal brokandidat:

- `frontier_diag_mid = (p_triad, p_del) = (0.005, 0.005)`

## Hovedfunn

- `band_small_triad` holder ikke fronten.
- `band_zero_del` er fortsatt best på rå `mean_composite` og pairwise bootstrap.
- `frontier_diag_mid` er best på `focused_score` og ser mer asymptotisk disiplinert ut.

## Hva det innebærer

Den operative fronten er nå:

- `band_zero_del` som rå vinner
- `frontier_diag_mid` som asymptotisk vinner

Det er derfor ikke lenger riktig å omtale prosjektets sentrum som `band_zero_del` versus `band_small_triad`.
