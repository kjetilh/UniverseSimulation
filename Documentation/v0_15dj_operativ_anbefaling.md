# Operativ anbefaling v0.15dj

- `artifact_scope`: `no_new_dynamics`; v15dj bruker eksisterende v15di-sammendrag og lager ingen nye simulasjonsresultater.
- `best_scout_rule`: se `v15dj_support_conditioned_rule_scores.csv`; beste enkle regler er low local support volume/gap-regler.
- `selector_status`: `not_validated`; bare to growth seeds og seks placement-sammendrag er for lite, og scout-reglene fanger ikke alle aktive placements.
- `interpretation`: supportgeometri ser relevant ut som pre-run prior, men retningen er ikke en universell lov.
- `next_step`: pre-registrer en fresh growth-seed dynamisk holdout der placements velges av support-rangering foer dynamikken kjores: top1, top2 og en kontrast.

- Ikke gjenoppliv fixed `p1/1024` som generell anchor.
- Ikke bruk label-frekvensene til aa refitte en selector uten fresh holdout.
- Ikke oppgrader dette til invariant-, Lorentz-, entanglement-, partikkel- eller universell-geometri-evidens.
