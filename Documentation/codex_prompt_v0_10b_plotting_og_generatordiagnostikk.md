# Codex-prompt: plotting og generator-diagnostikk etter v0.10b

Lag plottingkode for å visualisere generatorproblemet og reparasjonen.

## Relevante filer
- `v10b_ensemble_calibration_summary.csv`
- `v10b_ensemble_size_overlap.csv`
- `v10c_growth_regime_summary.csv`
- `v10c_growth_regime_overall.csv`
- `v10d_calibrated_scale_size_profiles.csv`

## Plot som ønskes
1. nominell størrelse vs realisert mean størrelse
2. q10–q90-intervaller per målstørrelse
3. sammenligning av growth-regimer på:
   - size error
   - hit rate
   - naturalness score
4. size profiles for kandidater etter kalibrert rerun

## Krav
- bruk matplotlib
- én figur per plott
- ingen seaborn
- ikke hardkod farger med mindre eksplisitt bedt om det
- skriv ut korte tekstforklaringer av hva plottet faktisk viser

## Viktig
Plott skal hjelpe med å skille:
- generatorfeil
- finite-size-problemer
- reelle kandidatskiller
