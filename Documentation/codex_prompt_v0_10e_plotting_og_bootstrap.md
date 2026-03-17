# Codex-prompt: plotting og bootstrapdiagnostikk for v0.10e

Du arbeider i prosjektet `UniverseSimulation`.

Bruk disse filene:
- `v10e_focused_band_base_summary.csv`
- `v10e_focused_band_candidate_summary.csv`
- `v10e_focused_band_pairwise.csv`
- `v10e_focused_band_size_profiles.csv`

Lag kode som produserer:
1. et enkelt panel med realiserte startstørrelser per target,
2. rangert stolpediagram for `mean_composite` med bootstrap-intervaller,
3. rangert stolpediagram for `focused_score`,
4. heatmap for pairwise sannsynligheter,
5. profilplot av `mean_radius` mot realisert størrelse for kandidatene.

Krav:
- bruk matplotlib, ikke seaborn,
- ingen stil- eller fargeoverstyring utover standard,
- skriv også ut en kort tolkning av hvert plot i Markdown.
