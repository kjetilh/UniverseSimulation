# v0.16ac for ikke-spesialister

Den gamle modellen lot sannsynligheten for en lokal veksthendelse avhenge av hvor mange tokens som fantes i hele grafen. Vi har naa lagt den nye klokkemekanismen i en separat adapter: hver mulig lokal vert har samme faste rate, uavhengig av fjerne deler av grafen.

Gaten rerunnet den fulle mikrostatsproeven med 33385 tilstander og 7123450 par av uavhengige hendelser. Resultatet var 0 kommutasjonsfeil og 0 relabel-feil. Den lokale hazardformelen og fjernkontekstkontrollen passerte ogsaa.

Dette reparerer en konkret arkitekturfeil og gjoer det legitimt aa undersoeke en intern kausal hendelsesgraf. Det viser fortsatt ikke at modellen har romtid, Lorentz-symmetri eller partikler.
