# UC2 — én kort tidslig løkke, ikke etablert metastabilitet

Dato: 2026-09-10. **Avgrenset kandidat utført og verifisert.**
Publiseringsstatus: **publication_blocked for full generativ RAG-verifisering**;
leverandøren melder `insufficient_quota` / `credit_balance_exhausted`.

## Resultat og beslutning

Vi har nå en separat, kontrollert simulator som flytter en relasjonsende via
en eksisterende naborelasjon og lar samme endringsenhet fortsette fra målnoden.
I 16 forhåndsbestemte kjøringer med totalt **65 536 faktiske endringer** oppsto
én registrert kort sekvens med tre gjentakelser av en trestegs løkke. Både
enhetens bane og hele graf+enhet-tilstanden gjentok seg. Det er en konkret
observasjon av tidslig tilbakekomst uten en samtidig syklus i grafen.

Dette er **ikke** et funn av robust/metastabil struktur, en effekt utover
tilfeldighet eller en fysisk invariant. Målet er svært strengt og smalt, og
ingen matchet null for de større kandidatgrafene er kvalifisert. Resultatet
avviser ikke brukerens hypotese om svak spontan mønsterdannelse.

Neste retning bør være å spesifisere lokal node-/enhetsfødsel og avklare hvilke
topologiske endringer slike regler faktisk tillater, før større kjøringer.
Bare flere steg med akkurat denne flytteloven kan aldri gi grafsykluser fra
trær eller fragmentering: disse mulighetene er algebraisk utelukket. Vi bør
ikke anta at fødsel alene løser dette: en ny node med bare én tilkobling eller
en ekstra endringsenhet endrer ikke i seg selv sykkelrangen. Reglene må faktisk
tillate den topologiske endringen vi vil undersøke. Vi bør
også kvalifisere et mål for støyende, aktivt opprettholdt mønster dersom det er
neste mål; denne rundens eksakte løkkeord dekker ikke det spørsmålet.

## Frys før data og kvalifisering

Protokoll, kildekode, tester og første proveniensindeks ble committet og pushet
som `e908d60e6921035873816d8d574f4171775ccb57` **før full kalibrering og kandidat**.
Det er ingen parameter- eller terskelendring etter kandidatdataene.

Se [modellkontrakten](UC2_model_contract.md),
[preregistreringen](UC2_preregistration.json) og
[kvalifiseringen](UC2_qualification.md). 61 målrettede tester besto. En separat
stresstest med 32 enheter ga 40 000 forsøk uten invariantbrudd; blokkerte
forsøk bevarte enhetene og ga ingen endringstikk. Dette kvalifiserer den nye
kjernen for det begrensede forsøket, ikke alle historiske simulatorer.

## Målte dynamiske referanser før kandidaten

Positiv kontroll: en tvunget, lovlig trestegssekvens på et tre med tre noder.
Nullkontroll: stokastiske lovlige flyttinger med samme regel og samme starttre.
Grafen forble et tre i begge. Dette er dynamiske kontroller, ikke vandring på
en frosset graf. Det er 16 par, 2 048 steg per historie, totalt 65 536 endringer.

| Primært mål: tre runder av et eksakt nodeforløp, lengde 3–6 | Verdi |
| --- | ---: |
| Positiv mediandekning | 1,0 |
| Null mediandekning | 0,023193359375 |
| Null minimum–maksimum | 0,00439453125–0,0419921875 |
| Positive / negative / like parfortegn | 16 / 0 / 0 |
| Forhåndsvalgt ensidig binomial fortegnsskår | 0,0000152587890625 |
| Fortegn bevart etter kvadrering | 16 / 16 |
| Referansekrav | BESTÅTT |

Den positive sekvensen er konstruert; fortegnsskåren kvalifiserer bare
instrumentets separasjon på disse kontrollene. Den gir ingen sannsynlighet
for univershypotesen. Kontrollen på tre noder er ikke en mulighetsmatchet
effekt-null for kandidatene på 12 eller 24 noder.

## Den ene kandidatmodellen

Uniforme, merkede starttrær ble generert med Prüfer-sekvenser. Én enhet ble
plassert uniformt blant startnoder med grad minst to; denne aktivitetsbetingelsen
var registrert på forhånd. Det ble kjørt åtte frø per størrelse, 4 096 endringer
per frø. Alle flyttinger var stokastiske; ingen løkkesekvens ble påtvunget.

| Startstørrelse | Kjøringer | Endringer | Kjøringer med detektert tre-runders løkke | Mediandekning | Maksimal dekning |
| --- | ---: | ---: | ---: | ---: | ---: |
| 12 noder | 8 | 32 768 | 1 | 0 | 9/4096 = 0,002197265625 |
| 24 noder | 8 | 32 768 | 0 | 0 | 0 |

Primær nodeforløpsdekning og sekundær dekning av **enkle eksakte
graf+enhet-tilstandssykluser** hadde samme verdier i disse kjøringene.
Alle kjøringer bevarte én enhet, node-/kantantall og sammenheng. Sykkelrangen
var null hele veien. Dette følger også av flytteloven og er ikke emergent
fysikk. Vedvarende aktivitet for én opprinnelig aktiv enhet er sikret ved at
en invers flytting alltid finnes; den er heller ikke et metastabilitetsfunn.

### Det konkrete vitnet

I `n12-5`, frø `20260911205`, ved endringene **862–870**, var banen
`1 → 4 → 3 → 1 → 4 → 3 → 1 → 4 → 3 → 1`.
Hele graf+enhet-tilstanden kom tilbake etter hver tredje endring. De ni radene
er et etterfølgende utsnitt i [UC2_witness.csv](UC2_witness.csv), hentet fra
det allerede frosne råsporet; de er ikke en ny kandidat eller en endret gate.

Null dekning betyr **ikke ingen tilbakekomst**: hver kjøring besøkte færre
ulike tilstander enn antallet observasjoner. Vanlig reversering, enkeltreturer
og støyende/gjentatte sekvenser som ikke oppfyller tre-runderskravet faller
utenfor dette målet. Vi rangerer derfor ikke kandidatene som fysisk lovende
eller mislykkede ut fra disse nullene.

## Evidens og uavhengig kontroll

- [Kalibreringsresultat](UC2_calibration.json), [parsammendrag](UC2_calibration_summary.csv), [starttilstander](UC2_calibration_initial.json), [alle endringer](UC2_calibration_events.csv).
- [Kandidatresultat](UC2_candidate.json), [kjøringssammendrag](UC2_candidate_summary.csv), [starttilstander](UC2_candidate_initial.json), [alle endringer](UC2_candidate_events.csv).
- [Proveniensindeks](UC2_provenance.md): deklarerte sammenhenger mellom premiss, regel, protokoll, kode, evidens og begrensning, med kildehasher.

Begge datasett besto full replay av lovlighet, PRNG-sekvens, kilder, protokoll,
samtlige endringer og endepunkter: 32 kalibreringshistorier og 16 kandidathistorier.
En uavhengig gjennomgang rekonstruerte alle 65 536 kandidatflyttinger med egen
naboskapskode, uten å bruke kjernens overgangsfunksjoner eller detektor, og
bekreftet begge målene og det konkrete vitnet. Ingen full Documentation-suite
ble kjørt. Råfiler forblir i checksum-arkivet; RAG får rapportene og små summer.

## Publisering og gjenværende blokkering

SSH-feilen er løst med riktig dokumentert nøkkel. Første, frosne etappe ble
bygget fra sin eksakte commit og kontrollert via offentlig HTTPS: landing,
manifest og alle syv nye UC2-artefakter samsvarte. RAG-synken tok inn åtte nye
UC1/UC2-dokumenter og oppdaterte driftsveiledningen uten filsletting. Forrige
nettrelease er bevart; gamle regenererbare indeksversjoner erstattes ved synk.

Den virkelige tokenbeskyttede spørsmål–svar-testen fikk først klient-timeout;
serverloggen viste modellleverandørens `credit_balance_exhausted`, ikke en
SSH- eller sitatfeil. Ingen kreditter ble kjøpt, leverandør byttet eller
tokenrettigheter utvidet. Anonym tilgang ble avvist med 401, eksisterende token
ga 200, og de fem første UC2-dokumentene var aktive med chunks i korpuset.
Dette er **delvis synk-/tilgangsverifisering**, ikke bestått generativ
sitat-, PostgreSQL-rate-limit- og ferskhetsaudit. Hele den påkrevde query-gaten
forblir blokkert til eksisterende API-tilgang er gjenopprettet.

Resultatene publiseres og synkes i en egen andre etappe. Manifestet angir den
eksakte resultatcommitten; oppgavens sluttkvittering angir kontrollert live
revisjon og siste synkstatus. En egen grafdatabase er ikke lagt til: vi har en
liten eksplisitt proveniensgraf i eksisterende RAG, uten ny lagringsmotor eller
endrede gjenfinningsregler. Brukerens hele vekst-/strukturhypotese er fortsatt
åpen og er ikke testet fullt ut av UC2.
