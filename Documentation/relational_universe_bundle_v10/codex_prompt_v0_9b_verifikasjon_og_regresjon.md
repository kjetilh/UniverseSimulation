# Codex-prompt: verifikasjon og regresjonstester for v0.9b

Du skal lage en liten verifikasjonspakke for v0.9b.

## Filer som skal brukes

- `relational_universe_v09b_asymptotic_refinement.py`
- `v09b_asymptotic_candidate_summary.csv`
- `v09b_asymptotic_size_profiles.csv`

## Oppgave

Lag tester som sjekker følgende:

1. At `alpha_jump = alpha_large - alpha_all` innenfor numerisk toleranse.
2. At `linear_margin = rmse_linear - min(rmse_log, rmse_sqrt)`.
3. At kandidatene rangeres konsistent når `asymptotic_score` er lagret.
4. At størrelseprofilene har forventet antall målskalaer.
5. At fravær av data håndteres ryddig.
6. At output-CSV-er kan regenereres uten å endre kolonnenavn unødvendig.

## Ekstra

Lag også en enkel sanity-test som eksplisitt demonstrerer hvorfor `balanced_pdel` ser dårligere ut enn `band_best` i v0.9b:
- høyere `alpha_jump`
- dårligere `linear_margin`

## Leveranse

- testfil(er)
- kort markdown-notat om hva testene beskytter prosjektet mot
