# v12 Codex assessment

Dette notatet oppsummerer den lokale Codex-runden etter innsynk av `relational_universe_bundle_v12`.

## Hva som ble aktivert

- Ny aktiv v0.10e-kode i `relational_universe_v10e_focused_band_validation.py`
- Ny plottingpakke i `relational_universe_v10e_plots.py`
- Ny verifikasjonspakke i `relational_universe_v10e_verify.py`
- Ny frontier-lab i `relational_universe_v10f_frontier_test.py`

Bundle-v12 er beholdt urørt i `Documentation/relational_universe_bundle_v12/`.

## v0.10e: viktigste lokale funn

Den lokale v0.10e-kjøringen viste en reell splittelse mellom to typer kandidatdom:

- `band_best` kom øverst på `focused_score`
- `band_zero_del` kom klart øverst på `mean_composite`
- `band_zero_del` slo `band_best` pairwise med sannsynlighet `0.796`

Det betyr at v0.10e ikke bør oppsummeres som “`band_best` vant” eller “`band_best` tapte” uten presisering.
Den riktige lesningen er:

- `focused_score` holder `band_best` høyt
- rå composite og pairwise flytter sentrum mot `band_zero_del`

## v0.10f: hva frontier-runden gjorde

Den lokale frontier-runden ble kjørt i en minimal variant med:

- `band_zero_del`
- `band_small_triad`
- `band_best`
- `band_small_death`

Resultatet var tydelig:

- `band_zero_del` ble klar vinner
- `band_small_death` ble nærmeste kontroll
- `band_best` falt videre tilbake
- `band_small_triad` holdt ikke fronten i denne runden

De viktigste tallene var:

- `band_zero_del`: `mean_composite ≈ 0.676`, `CI low ≈ 0.612`, `top_prob ≈ 0.950`
- `band_zero_del > band_best`: `1.000`
- `band_zero_del > band_small_triad`: `0.988`
- `band_zero_del > band_small_death`: `0.963`

## Operativ tolkning

Etter v12 er den mest nøkterne lokale konklusjonen:

- `band_best` er ikke lenger den operative standardkandidaten
- `band_zero_del` bør være ny standardkandidat
- `band_small_death` er den mest nyttige nærkontrollen i denne frontier-runden

## Praktisk status

v0.10e-pakken er nå komplett med:

- teknisk rapport
- plott
- verifikasjonsrapport
- regresjonstester

v0.10f er også landet som en lokal frontier-test, men i en kompakt variant for å holde kjøretiden praktisk i denne økten.
