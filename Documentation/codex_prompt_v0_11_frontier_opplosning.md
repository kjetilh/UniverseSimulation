# Codex-prompt: v0.11 frontier resolution mellom band_zero_del og frontier_diag_mid

Du arbeider i prosjektet `UniverseSimulation`.

## Ground truth
Bruk filene på disk som ground truth. Ikke anta at eldre bundles er aktive bare fordi de finnes.

Særlig relevante filer nå:
- `relational_universe_v10f_frontier_test.py`
- `v10f_frontier_broad_candidate_summary.csv`
- `v10f_frontier_final_candidate_summary.csv`
- `v10f_frontier_final_pairwise.csv`
- `v10f_frontier_final_size_profiles.csv`
- `relasjonell_universgraf_v0_10f_frontier_runde.md`
- `v0_10f_operativ_anbefaling.md`

## Nåværende situasjon
v0.10f flyttet fronten igjen.

Det operative bildet er nå:
- `band_zero_del` vinner på rå `mean_composite` og pairwise bootstrap.
- `frontier_diag_mid` vinner på `focused_score` og asymptotisk disiplin.
- `band_small_triad` bør ikke lenger regnes som frontkandidat.

## Hovedoppgave
Lag en v0.11 frontier resolution round som eksplisitt undersøker spenningen mellom `band_zero_del` og `frontier_diag_mid`.

### Del A: Finere lokal grid
Test et lite lokalt grid i området:
- `(p_triad, p_del) = (0.0000, 0.0000)`
- `(0.0025, 0.0000)`
- `(0.0025, 0.0025)`
- `(0.0050, 0.0025)`
- `(0.0050, 0.0050)`

Hold i første omgang:
- `r_birth = 0.02`
- `r_death = 0.00`
- `p_swap = 0.02`

### Del B: Liten p_swap-akse for zero-del-familien
Test minst:
- `p_swap = 0.020`
- `p_swap = 0.025`

for `band_zero_del` og minst ett mellompunkt nær diagonalbroen.

### Del C: Mer replikasjon
Bruk flere growth seeds og flere run seeds enn i v0.10f hvis det er praktisk mulig uten å gjøre runden uforholdsmessig tung.
Hvis du må velge, prioriter mer growth-variasjon først og bruk ekstra run-seeds på finalistene.

### Del D: To vinnerbegreper
Rapporter eksplisitt:
1. hvem som vinner på rå `mean_composite`,
2. hvem som vinner på `focused_score`,
3. om disse nå begynner å konvergere mot samme punkt.

### Del E: Rapportering
Svar tydelig på:
- Holder spenningen mellom raw winner og asymptotic winner seg?
- Er `frontier_diag_mid` bare et kompromisspunkt, eller ser den ut som et faktisk bedre sentrum?
- Forbedrer liten positiv `p_del` eller liten positiv `p_triad` stabiliteten uten å skade rå ytelse for mye?
- Er `p_swap = 0.025` en relevant sekundær akse, eller bare en bred-scan-anomali?

Lag:
- ny Python-kode,
- CSV-er,
- teknisk Markdown,
- kort note for ikke-spesialister,
- og en operativ anbefaling.
