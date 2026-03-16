# v11 Codex assessment

Dette notatet oppsummerer den lokale Codex-runden etter innsynk av `relational_universe_bundle_v11`.

## Hva som ble aktivert

- Nye aktive skript:
  - `relational_universe_v10b_ensemble_calibration.py`
  - `relational_universe_v10c_growth_regime_search.py`
  - `relational_universe_v10d_calibrated_scale_collapse.py`
  - `relational_universe_v10b_generator_plots.py`
- Bundle-v11 er beholdt urørt i `Documentation/relational_universe_bundle_v11/`.
- Promptene er også kopiert til `Prompts/`.

## Lokale verifikasjonskjøringer

Det ble kjørt en lokal smoke-runde med egne output-prefikser for å unngå sammenblanding med bundle-eksempeldata:

- `Documentation/v11_local_v10b_smoke_*`
- `Documentation/v11_local_v10c_smoke_*`
- `Documentation/v11_local_v10d_smoke_*`
- `Documentation/v11_local_v10b_plots/`

## Viktigste lokale observasjoner

### v0.10b generator-kalibrering

I smoke-runden (`targets = 24,48,96`, `seeds = 1`) var den viktigste kontrasten:

- `baseline/deep` overskjøt `24` kraftig og bommet også på `96`.
- `adaptive` traff alle tre nivåene i denne runden.

Dette støtter bundle-v11s hovedpåstand om at gammel generatorlogikk ikke bør tas som asymptotisk grunnlag uten kalibrering.

### v0.10c growth-regime search

Den lokale smoke-runden ga ikke helt samme aggregate-dom som bundle-eksempelet:

- `fast_ref` kom best ut på ren `overall` composite i denne lille runden.
- Men `fast_balanced/deep` ga også eksakt størrelse-treff på alle testede nivåer.

Dermed er den riktige lokale lesningen:

- bundle-dommen `fast_balanced / deep` kan være riktig i større runder,
- men smoke-runden alene viser at man må skille mellom `overall`-aggregat og det faktiske deep-regimet man vil bruke videre.

### v0.10d kalibrert rerun

Den lokale rerunden valgte operative nivåer:

- `48, 96, 128, 160, 192, 256`

I denne runden holdt `band_best` seg som beste kandidat:

- `mean_composite ≈ 0.606`
- `mean_repair ≈ 0.653`
- `mean_causal ≈ 0.492`
- `mean_quasi ≈ 0.621`
- `alpha_large ≈ 0.657`

Sammenlignet med kontrollene:

- `macro_stable` endte rundt `mean_composite ≈ 0.468`
- `balanced_pdel` endte rundt `mean_composite ≈ 0.463`

Det viktigste er ikke de eksakte tallene i smoke-runden, men at `band_best` fortsatt leder etter at startstørrelsene er eksplisitt separert.

## Metodisk status

Den tydeligste metodiske gevinsten i v11 er at generatorproblemet nå er gjort eksplisitt og målbart.

Prosjektet er derfor i en bedre posisjon enn før til å skille:

- generatorartefakter,
- finite-size-problemer,
- og faktisk kandidatatferd.

## Praktisk note

Plottingen krevde en lokal workspace-installert `matplotlib` i `.codex_pydeps/`.
Det ble ikke gjort noen systeminstallasjon.
