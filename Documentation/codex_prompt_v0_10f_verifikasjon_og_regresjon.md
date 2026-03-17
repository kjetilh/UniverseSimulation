# Codex-prompt: verifikasjon og regresjon for v0.10f

Du arbeider i prosjektet `UniverseSimulation`.

## Oppgave
Lag en liten verifikasjons- og regresjonspakke for v0.10f.

Bruk spesielt:
- `relational_universe_v10f_frontier_test.py`
- `v10f_frontier_base_summary.csv`
- `v10f_frontier_final_candidate_summary.csv`

## Minstekrav
Sjekk at:
1. realiserte startstørrelser faktisk er 48, 96, 192, 256 i den anbefalte runden,
2. `band_small_triad` ligger under både `band_zero_del` og `frontier_diag_mid` i finalefeltet på `mean_composite`,
3. `frontier_diag_mid` ligger over `band_zero_del` på `focused_score`,
4. `band_zero_del` ligger over `frontier_diag_mid` på `top_prob_mean_composite`,
5. ingen rapport feilaktig omtaler `band_small_triad` som del av den operative fronten.

Lag:
- en lett Python-testfil eller sjekkskript,
- og en kort Markdown-note om hvilke regresjoner som nå regnes som kritiske.
