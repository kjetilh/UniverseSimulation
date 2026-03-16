# v0.9b plotting og asymptotikk

## Hvordan figurene skal leses

- Kandidatoversikten viser kompromisset mellom lav `alpha_large` og høy nedre composite-grense.
- Finite-size-artefakt-figuren viser om en kandidat har høy `alpha_jump` og dårlig `linear_margin`; det er nettopp der finite-size-risikoen blir synlig.
- Radiusprofilene viser de rå størrelsesbanene som asymptotikk-fitene bygger på.
- Fokusfiguren sammenligner `band_best` og `balanced_pdel` direkte, siden dette er den sentrale rangreverseringen i v0.9b.
- Refineringsfiguren viser om lokal ekstra ensemble-varians flytter toppkandidatene mye eller lite.

Den nåværende asymptotiske vinneren er `band_best` med `alpha_large` ≈ 0.303, `alpha_jump` ≈ 0.025 og `linear_margin` ≈ 0.059.

## Filer

- `v09b_candidate_overview.png`
- `v09b_finite_size_artifacts.png`
- `v09b_radius_profiles_linear.png`
- `v09b_radius_profiles_loglog.png`
- `v09b_focus_band_best_vs_balanced_pdel.png`
- `v09b_refinement_shift.png`
