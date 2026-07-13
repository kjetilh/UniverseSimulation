# v0.16a for ikke-spesialister

Vi testet om to hendelser langt nok fra hverandre kan bytte rekkefolge uten at resultatet endres. Det bestod i den endelige mikrostatscensusen.

Men vi fant samtidig at sannsynligheten for en seed-hendelse ved ett token avhenger av hvor mange tokens som finnes i hele grafen. Dermed er dagens tidsmekanisme ikke rent lokal, selv om den konkrete grafendringen er lokal.

Dette er ikke et fysikkfunn. Det er en presis arkitekturdiagnose: seed-klokken maa redesignes eller erkjennes som global bakgrunn foer vi kan teste en observer-uavhengig kausal struktur.
