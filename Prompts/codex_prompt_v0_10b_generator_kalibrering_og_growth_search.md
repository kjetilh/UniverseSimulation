# Codex-prompt: videre arbeid etter v0.10b–v0.10d

Du arbeider i prosjektet `UniverseSimulation`.

## Aktiv kontekst
Bruk filer på disk som ground truth. Særlig relevante filer nå:

- `relational_universe_v10b_ensemble_calibration.py`
- `relational_universe_v10c_growth_regime_search.py`
- `relational_universe_v10d_calibrated_scale_collapse.py`
- `v10b_ensemble_calibration_summary.csv`
- `v10c_growth_regime_overall.csv`
- `v10d_calibrated_scale_candidate_summary.csv`
- `relasjonell_universgraf_v0_10b_generator_kalibrering_og_growth_regimer.md`

## Nåværende status
- Gammel referansegenerator kollapser store nominelle nivåer.
- `fast_balanced / deep` er anbefalt som videre ensemble-regime.
- `band_best` holder seg som beste kandidat etter kalibrert rerun.

## Oppgave
Bygg neste smale runde, v0.10e eller v0.11, med disse kravene:

1. Bruk bare reelt separerte startstørrelser.
2. Bruk `fast_balanced / deep` som default growth-regime.
3. Test et smalt kandidatsett:
   - `band_best`
   - `macro_stable`
   - én kontroll
4. Øk antall growth seeds og run seeds moderat.
5. Lag bootstrap-intervaller for:
   - mean composite
   - alpha_large
   - alpha_jump
   - overlap_large
6. Skill eksplisitt mellom:
   - generatorrelaterte resultater
   - dynamiske kandidatresulater
7. Ikke kall noe asymptotisk hvis realiserte startstørrelser ikke faktisk separerer.

## Leveranser
- ny Python-kode
- run-level og candidate-level CSV
- teknisk Markdown
- kort note for ikke-spesialister
- operativ anbefaling for videre arbeid
