# Codex-prompt: plotting og frontierdiagnostikk for v0.10f

Du arbeider i prosjektet `UniverseSimulation`.

Bruk disse filene:
- `v10f_frontier_broad_candidate_summary.csv`
- `v10f_frontier_final_candidate_summary.csv`
- `v10f_frontier_final_pairwise.csv`
- `v10f_frontier_final_size_profiles.csv`

Lag kode som produserer:
1. et scatterplot av `mean_composite` mot `focused_score`,
2. et scatterplot av `alpha_large` mot `ci_low_mean_composite`,
3. en liten heatmap eller annotert matrise for pairwise bootstrap-sannsynligheter i finalefeltet,
4. en enkel size-profile-figur for finalistene over 48, 96, 192, 256.

Krav:
- bruk matplotlib,
- én figur per plot,
- ingen spesifiserte farger med mindre det er nødvendig,
- lagre filene til disk med tydelige navn,
- og skriv kort Markdown som forklarer hva figurene faktisk viser.
