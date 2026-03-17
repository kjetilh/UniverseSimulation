# Codex-prompt: verifikasjon og regresjonstester for v0.10e

Du arbeider i prosjektet `UniverseSimulation`.

Ground truth:
- `relational_universe_v10e_focused_band_validation.py`
- `v10e_focused_band_base_summary.csv`
- `v10e_focused_band_candidate_summary.csv`
- `v10e_focused_band_pairwise.csv`

Målet er å lage en lett verifikasjonspakke som sjekker:

1. at `fast_balanced / deep` fortsatt realiserer 48, 96, 192, 256 som reelt separerte nivåer,
2. at `band_best` ikke feilaktig blir stående som toppkandidat hvis CSV-ene faktisk viser noe annet,
3. at pairwise-tabellen er konsistent (om A>B er p, skal B>A være omtrent 1-p),
4. at `focused_score`-rangeringen kan regenereres fra kandidatsammendraget.

Lag:
- et lite testskript,
- tydelige assertions,
- og en kort Markdown om hva som er “røde flagg” i regressjon.
