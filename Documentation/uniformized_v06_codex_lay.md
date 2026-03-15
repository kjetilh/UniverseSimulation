# v0.6 forklart enkelt

Vi har nå en bedre måte å sammenligne to nesten like universgrener på når modellen er åpen og antall tokens kan endre seg.

Det viktige er dette: i eldre tester kunne grenene komme ut av takt bare fordi de fikk ulik totalrate. Da visste vi ikke om forskjellen spredte seg fordi modellen hadde ekte lokal kausalitet, eller bare fordi vi sammenlignet to forskjellige klokker. I v0.6 bruker vi derfor en felles overordnet hendelsesklokke og avgjør deretter om hver gren aksepterer hendelsen. Det gjør sammenligningen mye renere.

Vi kjørte to representative regimer. Det moderate token-open regimet ser best ut for videre spacetime-testing: grenene deler fortsatt mye felles støy, men er åpne nok til at testen er reell. Det moderate full-open regimet er mer levende, men ser også mer rotete ut; mer av forskjellen går inn i token-drift og scrambling enn i en pen voksende front.

Den foreløpige dommen er derfor: v0.6 er et metodisk viktig steg, og den moderate token-open sektoren er den beste nåværende kandidaten hvis vi vil lete etter lyskjegle-lignende oppførsel. Det neste riktige steget er å skanne parameterrommet rundt dette regimet og deretter forbedre den lokale koblingen videre i v0.7.
