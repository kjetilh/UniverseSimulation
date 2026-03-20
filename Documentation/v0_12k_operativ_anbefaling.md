# v0.12k operativ anbefaling

Behold `full_followup` som referanse. Ingen adaptive policyer er naer nok full oppfolging til a bli en ny standard direkte fra denne runden.
Les `probe1_only` som den raske yttergrensen: `time_frac=0.159`, men `best_hit=0.500` og `recall=0.500` er for svake.
Les `probe2_top_half` som den mest balanserte adaptive utfordreren: `time_frac=0.677`, `best_hit=0.750` og `recall=0.750`.
Neste naturlige steg etter v12k er enten å gjøre en litt dypere adaptiv oppfølgingsrunde, eller å kombinere den beste adaptive follow-up-politikken med den eksisterende screeningbenchmarken for en ekte end-to-end arbeidsflyt.
