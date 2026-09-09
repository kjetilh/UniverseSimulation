# UC2 — presis relasjonsflytting før kandidatmåling

Dato: 2026-09-10. Status: preregistrert kandidat, ikke kjørt ved kontraktens
opprettelse. Frosne valg: [UC2_preregistration.json](UC2_preregistration.json).

## Brukerens presisering og vår avgrensning

«Units of change endrer en relasjon fra en node til en annen og fortsetter
traverseringen videre fra mål-noden.» Vi implementerer dette som en lokal
flytting av én relasjonsende. Endringsenheten fortsetter fra den nye enden.
Ingen nodeverdier, kantvekter, koordinater eller skjult retning tilføyes.

Den konkrete tilstanden er grafen og endringsenhetenes plasseringer. Dette er
en eksplisitt representasjon av primitive endringsenheter, **ikke** en påstand
om at deres plasseringer kan utledes av en utypet naboskapsmatrise alene.
Identifikatorer og hendelseslogger er observatørens bokføring, ikke fysiske
egenskaper. Dette operasjonaliserer presiseringen; det løser ikke filosofisk
ekvivalens mellom primitive enheter og grafmotiver.

For en enhet ved v og eksisterende relasjoner v–u og v–a velges et lovlig
ordnet nabopar u,a stokastisk. Når u–a ikke finnes, erstattes v–a med u–a.
v–u beholdes, og den samme enheten fortsetter fra u. Ingen global fallback,
sletting av enheter eller teleportering tillates. Mislykkede forsøk er ikke
relasjonelle tikk. Endringsenheter som ikke kan handle, blir værende.

Denne runden isolerer kjernen med fast antall noder og endringsenheter.
Brukerens mulighet for nye noder og spontane nye endringsenheter er fortsatt
del av prosjektets hypotese, men **ikke implementert i denne kandidaten**.
Historiske simulatorer endres ikke: den nye, avgrensede kjernen verifiseres
separat, så tidligere målinger beholder sine faktiske kildeversjoner.

## Et viktig algebraisk skille

Flyttingen bevarer antall noder, antall kanter og komponenttilhørighet: den
gamle forbindelsen a–v erstattes av a–u–v. Dermed bevares også sykkelrangen
E−V+C. Fra et tre kan denne loven aldri skape en samtidig grafsyklus, og den
kan ikke splitte en komponent. Dette er innebygde begrensninger, ikke nye
fysiske bevaringslover eller negative simuleringstestresultater.

Men et **tidsforløp** kan sirkulere. Start med kantene 0–1 og 0–2 og en enhet
ved 0. Tre lovlige flyttinger, med mål 1, 2 og 0, bringer både graf og enhet
tilbake til start, selv om grafen hele tiden er et tre. Den tvungne sekvensen
brukes bare som en konstruert dynamisk positiv kontroll. Den stokastiske
kontrollen bruker samme tre og samme lov, uten å tvinge sekvensen.

## Hva kandidaten kan svare på

Etter kvalifisering og målte referanser kjøres én fast lov på forhåndsvalgte
tilfeldige trær. Vi måler eksakt gjentatte nodeforløp og beskriver separat
tilbakekomst av hele graf+enhet-tilstanden. Vi påstår ikke at referansen på
tre noder er en matchet effekt-null for større grafer. Kandidatutfallet blir
derfor en avgrenset, beskrivende måling av tidslig tilbakekomst, ikke en
signifikanstest av metastabilitet eller univershypotesen.

Dette valget unngår en kjent dårlig kontroll: en enhet som blir ved kilden
etter hver flytting, mister en naborelasjon hver gang og kan stanse raskt.
Målfortsettelsen får derimot en ny relasjon og har alltid en mulig invers.
En aktivitetsforskjell mellom dem ville derfor være innebygd i forsøket.

Neste modellutvidelse må spesifisere vekst og eventuell fragmentering som
egne lokale regler, med nye kontroller. Verken høy aktivitet eller tilbakekomst
i UC2 kan brukes som begrunnelse for å smugle inn disse reglene etterpå.

## Drift og gjenfinning

SSH-feilen fra UC1 er lokalisert: forbindelsen utenfor sandbox nådde verten,
men standardnøklene ble avvist. Den dokumenterte Hetzner-nøkkelen med `ops`
og `root` ga tilgang. Se oppdatert publiseringsrunbook; hemmeligheter endres
eller publiseres ikke.

RAG har allerede en Markdown-lenkegraf, men ikke en grafdatabase brukt i
gjenfinningen. Denne runden legger til en eksplisitt, kildehashet
proveniensindeks. En egen grafdatabase utsettes inntil en målt gjenfinningsfeil
viser at graftraversering gir merverdi, og tilgang, sletting og revisjoner er
spesifisert. Det gjøres ingen endringer i HAVEN-/DiMy-korpusene.
