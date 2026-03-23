# v0.12n operativ anbefaling

Behold `full_followup` som referanse under fast `full_basis@0.50` screening.
Les `probe3_top_half` som hovedkandidaten: `speedup=1.356`, `best_hit=0.650`, `recall=0.650` og `pairwise=0.590`.
`probe3_top_half_screen_tiebreak` og `probe3_guarded_half` forbedrer ikke dette bildet: tie-break holder samme tall som hovedkandidaten, mens guarded-varianten blir tregere uten kvalitetsgevinst.
Den repo-lojale dommen etter v12n er derfor: `probe3_top_half` er fortsatt en nyttig rask utfordrer, men den er ikke robust nok til å erstatte `full_followup` ennå.
Hvis vi skal videre herfra, bør neste steg være en smartere tidlig beslutningsstatistikk eller et større valideringssett, ikke flere nesten-like lokale varianter.
