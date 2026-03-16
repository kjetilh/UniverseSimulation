# Codex-prompt: plotting og asymptotikk for v0.9b

Bruk datafilene fra v0.9b:

- `v09b_asymptotic_candidate_summary.csv`
- `v09b_asymptotic_size_profiles.csv`
- `v09b_refined_candidate_summary.csv`
- `v09b_ensemble_summary.csv`

## Oppgave

Lag en plotting-pakke som produserer en liten, ryddig serie figurer for v0.9b.

## Figurer

1. Kandidatoversikt:
   - `alpha_large` mot `ci_low_mean_composite`
   - marker kandidatnavn
2. Finite-size artefakt-figur:
   - `alpha_jump` mot `linear_margin`
3. Størrelsesprofiler:
   - radius mot mean initial N for alle kandidater
   - gjerne både lineær skala og log-log
4. Fokusfigur:
   - sammenlign `band_best` og `balanced_pdel`
5. Refineringsfigur:
   - vis forskjellen mellom hovedscan og lokal refinering for toppkandidatene

## Krav

- Bruk bare matplotlib.
- Ikke bruk seaborn.
- Én figur per plot.
- Ikke sett eksplisitte farger med mindre det er nødvendig.
- Lag kode som skriver figurene til en egen output-mappe.
- Lag en kort markdown-fil som forklarer hvordan figurene skal leses.
