# Relasjonell universgraf status v0.12l

## Kort status

Prosjektet er fortsatt i struktur- og arbeidsflytfasen, ikke i ny frontier-tuning.
`band_zero_del` er fortsatt den aktive frontier-standarden fra `v11e`.

`v12l` er den første runden som kombinerer:

- screening av starttilstander,
- og adaptiv oppfølging av de valgte basene,

i én målt workflow.

## Live operative konklusjoner

### Frontier

- Live frontier-standard: `band_zero_del`
- Dette bygger fortsatt på `v11e`, ikke på eldre bridge-runder.

### Geometri / struktur

Det robuste struktursignalet er fortsatt:

- `initial_avg_degree`, `initial_spectral_per_sqrtN` og `initial_dim_proxy` er nyttige normaliserte startfeatures
- radius-transferen er lokal og regimebundet
- små basisrom bærer noe informasjon, men ingen liten basis har vunnet alle oppgaver

### Hybrid arbeidsflyt

`v12l` viser tre ting samtidig:

- `full_basis__full_followup` holder seg som arbeidsreferanse
- `spectral_only__full_followup` er den nærmeste same-budget-utfordreren på middelverdier
- `full_basis__probe2_top_half` er den tydeligste reelle tidsutfordreren

Men:

- `spectral_only__full_followup` er ikke robust nok split-for-split
- `full_basis__probe2_top_half` taper for mye kvalitet

Derfor har repoet fortsatt ikke en ny billig standardworkflow.

## Viktige tall fra v0.12l

Fra `Documentation/v12l_hybrid_screening_followup_summary.csv`:

- `full_basis__full_followup`
  - `mean_total_seconds ~= 26.890`
  - `mean_best_hit ~= 0.656`
  - `mean_recall ~= 0.656`
  - `near_match_rate_eps_02 = 1.000`

- `spectral_only__full_followup`
  - `mean_total_seconds ~= 26.372`
  - `speedup_vs_ref ~= 1.020`
  - `mean_best_hit ~= 0.662`
  - `mean_recall ~= 0.662`
  - `near_match_rate_eps_02 ~= 0.650`

- `full_basis__probe2_top_half`
  - `mean_total_seconds ~= 18.052`
  - `speedup_vs_ref ~= 1.494`
  - `mean_best_hit ~= 0.575`
  - `mean_recall ~= 0.575`
  - `near_match_rate_eps_02 ~= 0.675`

## Riktig lesning

`v0.12l` sier ikke at vi nå har funnet en ny best policy.

Det den faktisk sier er:

- det finnes en svak same-budget-utfordrer i `spectral_only__full_followup`
- det finnes en tydelig tidsutfordrer i `full_basis__probe2_top_half`
- men ingen av dem er robuste nok til å erstatte referansen

Dette er derfor fortsatt et arbeidsflytproblem, ikke en ny matematisk lov.

## Neste naturlige steg

Det riktige neste steget er ikke mer screeningfinjustering.

Det riktige neste steget er en dypere adaptiv oppfølgingsrunde, for eksempel:

- behold screeningdelen fast,
- behold `full_basis@0.50` som referanseinngang,
- og test om adaptiv oppfølging kan gjøres smartere enn `probe2_top_half`

Målet bør være å løfte kvaliteten nærmere referansen uten å gi fra seg hele tidsgevinsten.
