# Codex-prompt: v0.10f frontier-test rundt band_zero_del og band_small_triad

Du arbeider i prosjektet `UniverseSimulation`.

## Ground truth
Bruk filene på disk som ground truth. Ikke anta at eldre bundles er aktive bare fordi de finnes.

Særlig relevante filer nå:
- `relational_universe_v10e_focused_band_validation.py`
- `v10e_focused_band_candidate_summary.csv`
- `v10e_focused_band_pairwise.csv`
- `v10e_focused_band_size_profiles.csv`
- `relasjonell_universgraf_v0_10e_fokusert_bandvalidering.md`
- `v0_10e_operativ_anbefaling.md`

## Nåværende situasjon
v0.10e flyttet prosjektets lokale sentrum bort fra `band_best`.
Den operative fronten er nå:
- `band_zero_del`
- `band_small_triad`

`band_small_death` er en relevant nær nabo.
`band_best` bør behandles som referanse, ikke som automatisk vinner.

## Hovedoppgave
Lag en ny frontier-runde som:
1. holder `fast_balanced / deep` fast,
2. bruker flere growth seeds enn i v0.10e,
3. bruker flere run seeds enn i v0.10e,
4. tester et lite lokalt grid rundt `band_zero_del` og `band_small_triad`.

## Kandidatakser
Minstekrav:
- `p_triad`: fin grid rundt `0.00–0.02`
- `p_del`: fin grid rundt `0.00–0.01`

Valgfritt:
- liten `p_swap`-akse rundt `0.02`

## Rapportering
Svar eksplisitt på:
1. Holder den todelte fronten seg?
2. Smelter fronten sammen til én ny vinner når vi finprøver?
3. Er forbedringene robuste, eller bare marginale?
4. Endrer økt replikasjon pairwise-sannsynlighetene mye?
5. Er det nå grunnlag for å velge én standardkandidat, eller bør prosjektet fortsatt holde to kandidater åpne?

Lag:
- ny Python-kode,
- CSV-er,
- teknisk Markdown,
- kort note for ikke-spesialister,
- og en operativ anbefaling.
