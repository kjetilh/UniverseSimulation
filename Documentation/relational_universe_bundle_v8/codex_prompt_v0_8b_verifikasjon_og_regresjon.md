# Codex-prompt: v0.8b verifikasjon og regresjonstester

Les først:

- `relational_universe_v08b_natural_ensemble_robustness.py`
- `v08b_natural_ensemble_runs.csv`
- `v08b_natural_ensemble_aggregate.csv`
- `v08b_candidate_robustness.csv`
- `relasjonell_universgraf_v0_8b_naturlige_ensembler_og_bootstrap.md`

## Oppgave

Lag en verifikasjonsmodul og et lite regresjonstestoppsett for v0.8b.

### Del 1: verifikasjon
Sjekk programmatisk at:
1. naturlige ensembler faktisk er større enn `toy_cycle8`,
2. bootstrap-intervallene er konsistente med punktestimatene,
3. ranking etter `ci_low_mean_composite_natural` er stabil mot små endringer i bootstrap-seed.

### Del 2: regresjonstester
Lag tester som feiler hvis:
1. topprangert kandidat plutselig faller langt under tidligere nivå,
2. naturlige ensembler mister mye størrelse uten at det er tilsiktet,
3. kolonnenavn eller CSV-struktur bryter bakoverkompatibilitet.

### Leveranser
- ny Python-fil for verifikasjon
- testfil(er)
- kort `.md`-rapport som forklarer hva som ble sjekket og hva som eventuelt feilet
