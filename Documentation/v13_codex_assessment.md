# v13 Codex assessment

Dette notatet oppsummerer den lokale Codex-runden etter innsynk av `relational_universe_bundle_v13`.

## Hva som ble aktivert

- Ny aktiv v0.10f-kode i `relational_universe_v10f_frontier_test.py`
- Ny plottingpakke i `relational_universe_v10f_plots.py`
- Ny verifikasjonspakke i `relational_universe_v10f_verify.py`
- Nye regresjonstester i `tests/test_v10f_regression.py`
- Ny v0.11-kode i `relational_universe_v11_frontier_resolution.py`

## v0.10f: lokal status

v13-frontierrunden ble kjørt lokalt ende til ende.

Den viktigste lokale lesningen er:

- `band_zero_del` er fortsatt råvinner på `mean_composite` og `top_prob`
- `frontier_triad_only` ble focused-score-vinner i den lokale v13-kjøringen
- `band_small_triad` falt tydelig ut av operativ frontier

Dermed er den mest presise lokale v13-dommen:

- rå standardkandidat: `band_zero_del`
- asymptotisk/focused kontroll: `frontier_triad_only`

Dette er litt skarpere enn bundle-README-en, som omtaler `frontier_diag_mid` som focused-vinner.

## v0.11: lokal status

Koden for v0.11 frontier resolution er lagt inn, men den ble ikke fullkjørt i denne runden.

Årsaken var ikke syntaks eller importfeil, men ren kjøretid i den tunge coupled frontier-broad-fasen.

Det betyr at:

- v0.11-sporet er klart som kode,
- men ikke validert lokalt ennå,
- så v13 bør foreløpig tolkes som en fullført v0.10f-runde pluss et klargjort v0.11-startpunkt.
