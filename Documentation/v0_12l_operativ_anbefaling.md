# v0.12l operativ anbefaling

Behold `full_basis__full_followup` som arbeidsreferanse til en hybrid er baade raskere og naer nok pa hit/recall.
Les `spectral_only__full_followup` som den naermeste same-budget-utfordreren: `speedup=1.020`, `best_hit=0.662`, `recall=0.662`, men splitvis `near_match=0.650` er ikke hoy nok.
Les `full_basis__probe2_top_half` som den viktigste tidsutfordreren: `speedup=1.494`, `best_hit=0.575` og `recall=0.575` viser ekte besparelse, men fortsatt for stort kvalitetstap.
Hvis hybriden fortsatt ikke er god nok, peker repoet mot ett mer presist neste steg: hold screeningdelen fast og gjør en dypere adaptiv oppfølgingsrunde, i stedet for å finjustere flere screeningbasiser.
