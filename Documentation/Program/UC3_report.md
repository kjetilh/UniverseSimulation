# UC3 — mer graf, men aktiviteten forsvinner

Dato: 2026-09-11. **Én registrert kandidat utført og replay-verifisert.**
Publiseringsstatus: **publication_blocked** for full generativ RAG-verifisering;
sist påviste blokkering er leverandørens `credit_balance_exhausted`. Statisk
publisering og korpussynk kontrolleres separat i sluttkvitteringen.

## Resultat og beslutning

En lokal regel for fødsel, kollaps og kutt ble lagt til ved siden av UC2,
uten koordinater, vekter, nodeverdier eller historikk i overgangsloven.
Alle **16 kjøringer fikk netto flere noder, men alle 16 endte med samtlige
endringsenheter isolert**. Enhetene ble ikke slettet. Grafrester er ikke
automatisk aktive strukturer: summen av noder over frakoblede etterkommere
er bokføring over flere universer, ikke vekst i én sammenhengende organisasjon.

Det nye målet søker to gjentatte grove vekst-/nedgangsperioder med faktisk
utskifting av delene. Det skilte sine målte positive/null-kontroller, men
kandidaten ga **ingen komplette vinduer med tilstrekkelig størrelse og
2-kjerne gjennom begge perioder**. Nullskåren kan derfor ikke brukes som
en informativ avkreftelse av makroskopiske sykluser. Det direkte funnet er
kortvarig aktivitet, fragmentering og aktivitetsabsorpsjon under akkurat
denne regelen og disse startfordelingene.

**Beslutning:** Behold den testede kjernen, råloggene og den adskilte
observatøren. Ikke bruk mer kjøretid på absorberte UC3-tilstander, og ikke
senk sykluskravene etter utfallet. Neste regelarbeid må først avklare lokal
bevaring eller nydanning av **aktiv** endringskapasitet. Langvarig vekst av
inaktive rester er ikke det samme spørsmålet som vedvarende organisering.
Dette er fremgang i modellavklaring, ikke et positivt fysikkfunn.

Den foretrukne neste kandidaten er derfor en separat registrert regel for
lokal enhetsfødsel knyttet til faktisk endring, **før** absorpsjon. Den skal
ikke innføre en global redning av isolerte noder eller endre UC3 etter data.
Aktivitetsoverlevelse trenger da egne målte positive/null-referanser før en
gate brukes. Flere enheter kan også blokkere collapse gjennom samlokalisering
og dermed endre nodedriften; dette må auditeres eksplisitt. En kuttregel som
forbyr isolasjon er nyttig som mekanismekontroll, men ville bygge overlevelse
inn i loven og kan ikke telle som emergent selvopprettholdelse.

## Frys, premiss og den ene loven

[Planen](UC3_plan.md), [protokollen](UC3_preregistration.json), kode og tester
ble committet og pushet som
`e26c8c0412fb9600b2968dde05773bad1d02d2b9` **før full kalibrering og kandidat**.
Ingen kilde, vekt, terskel, lag eller frø er endret etter måling.
Resultat-JSON-ene hasher alle kjøringsavhengigheter og planen; kandidaten
binder også den replay-verifiserte kalibreringsfilen med SHA-256.

Velg én vedvarende enhet uniformt, også blant isolerte enheter. Velg så
`slide:bud:collapse:cut` med vektene **4:1:2:1**. Blokkert trekk registreres
som forsøk, men gir ingen fysisk endring, tikk eller ny trekning.

- Slide flytter en relasjonsende fra kilden til en eksisterende nabo og lar
  samme enhet fortsette ved naboen, som i UC2.
- Bud lager en ny node knyttet til kilden og én av dens naboer; samme enhet
  fortsetter ved den nye noden. Hoppet langs den nylig opprettede kanten er
  et eksplisitt fødselsunntak, ikke et skjult brudd med den deklarerte loven.
- Collapse hopper fra en grad-2-node i en trekant til naboen og fjerner
  kilden, bare når ingen annen enhet står på den.
- Cut krysser en eksisterende kant og fjerner den; alle noder og enheter,
  også isolerte og frakoblede etterkommere, beholdes.

En atomisk omskriving er ett endringstikk. Enhetsfødsel er fortsatt utelatt;
UC3 tester derfor ikke hele brukerens hypotese. Bud bygger trekanter direkte.
Identiteten **E−2N+antall_kutt = konstant** og ikke-avtakende komponentantall
er regnefølger av loven, ikke emergente invarianter.

## Nabotrådens bidrag og det grovere spørsmålet

«Vurder glemmestrukturer i verktøyk​» ble lest og direkte konsultert.
Det nyttige bidraget var å skille **deloverlevelse, formretur og tidslig orden**:
Organisasjon kan komme tilbake selv om delene er skiftet ut. En konstant form
er likevel ikke en vekstsyklus, og ren tilvekst er ikke tosidig delutskifting.

Dette er implementert i en observatør som følger hver enhets aktuelle
komponent. Hendelser i frakoblede etterkommere flytter ikke dens klokke.
Felles komponenthistorie gir korrelerte spor; frøkjøringen, ikke enheten eller
vinduet, er forsøksenheten. Historikk, 2-kjerne og tellinger påvirker aldri
simulatorens valg. Oja/lærte vekter ble ikke importert; se planens
primærkilder og begrunnelse. Biosfæren er en analogi for hva vi leter etter,
ikke evidens for denne mekanismen eller en påført vekstkurve i kandidaten.

Ved initial N=32/96 tas snapshots hver 8/24 komponentendringer. Laget er
alltid åtte snapshots: to perioder krever minst 128/384 lokale endringer.
Hele vinduet må ha N≥16 og minst fire kjernenoder, fasevis omtrent samme
størrelse/kjerneandel/sykkelrang, minst 1,5-fold størrelsesutslag i hver periode
og minst 25 % balansert utskifting av kjerne-noder og -kanter. Dette er ett
initialskalert mål; det dekker ikke alle former for vedvarende organisering.

## Målte referanser før kandidat

Alle kontrollhendelser er lovlige UC3-buds/collapses på en sammenhengende
vifte. Positiv kontroll vokser 16→32→16 noder per periode. Nullkontrollen
har samme antall fødsler/kollapser og samme start/sluttstørrelse, men uniformt
samplet hendelsesrekkefølge fra 3 631 908 tillatte Dyck-ord. Hvert nullord er
betinget på en stor **observert** ekskursjon. Det er 16 par, 32 perioder per
historie, totalt **32 768 endringer**.

| Primært sammensatt syklusmål | Målt verdi |
| --- | ---: |
| Positiv median | 1,0 |
| Nullmedian | 0,1410788382 |
| Null minimum–maksimum | 0,0788381743–0,3568464730 |
| Positive / negative / like parfortegn | 16 / 0 / 0 |
| Ensidig fortegnsskår | 0,0000152587890625 |
| Fortegn uendret etter kvadrering | Ja |
| Registrert referansekrav | BESTÅTT |

Dette kvalifiserer det sammensatte instrumentet på disse kontrollene, ikke
hvert delmål separat. Viftenes kjerneandel er konstant, og turnover følger
i stor grad av konstruksjonen. Nullskåren er ikke null og illustrerer at
kvalifiserende vinduer også kan oppstå uten påtvunget periodisk bølgeform.
Referansene er **ikke** en matchet effekt-null for hele kandidatens lov.

## Kandidat: vekst uten vedvarende aktivitet

Uniforme merkede Prüfer-trær; enheter plassert uavhengig og uniformt på alle
startnoder. Åtte frø per størrelse. Registrerte grenser: 16 384 forsøk,
4 096 endringer eller 1 024 noder. Alle kjøringer stoppet tidligere ved
aktivitetsabsorpsjon; ingen ble ressurs-sensurert eller erstattet.

| Startstørrelse | N=32, 8 enheter | N=96, 24 enheter |
| --- | ---: | ---: |
| Kjøringer | 8 | 8 |
| Forsøk | 5 430 | 23 768 |
| Faktiske endringer | 1 138 | 3 387 |
| Endringer til absorpsjon, min / median / maks | 81 / 140 / 225 | 302 / 433,5 / 526 |
| Sluttnoder, min / median / maks | 37 / 43,5 / 54 | 120 / 139 / 144 |
| Sluttkomponenter, min / median / maks | 16 / 20,5 / 30 | 42 / 64,5 / 76 |
| Buds / collapses / cuts | 245 / 142 / 254 | 748 / 425 / 797 |
| Enhetsspor med for kort tidsserie | 61 / 64 | 192 / 192 |
| Mulige to-periodersvinduer før størrelse/kjerne-krav | 9 | 0 |
| Vinduer som oppfyller størrelse/kjerne gjennom hele vinduet | 0 | 0 |
| Kvalifiserende syklusvinduer | 0 | 0 |
| Kjøringer med alle enheter isolert | 8 / 8 | 8 / 8 |

Totalt **29 198 forsøk, 4 525 endringer, 24 673 blokkerte forsøk**. Alle
256 enheter består og er isolert ved slutt. Det forekom 993 buds, 567
collapses, 1 051 cuts og 1 914 slides. Globalt over alle etterkommere steg
nodeantallet fra 1 024 til 1 450; 653 komponentbrudd ga 669 sluttkomponenter.

Det er viktig å skille **øyeblikkelig struktur** fra komplett målemulighet:
alle 16 kjøringer hadde enkelte snapshots med både N≥16 og kjerne≥4.
Bare tre av 256 enhetsspor hadde tidslengde til noe to-periodersvindu, og
deres ni vinduer feilet størrelse/kjerne før de øvrige sykluskravene.
253 spor var tidsmessig utilstrekkelige. Vi har ikke vist fravær av sykluser
i et godt eksponert, langlivet makroskopisk regime.

### Etterfølgende regne-/mekanismeaudit, ikke ny gate

Loven ga før måling den betingede forventningen
E[ΔN|tilstand]=(A−2D)/8, hvor A er andelen aktive enheter og D andelen med
lovlig collapse. Summert over de faktisk besøkte tilstandene var den
integrerte forventede nodedriften **494,2083333**; realisert nettovekst var
**426**. Dette er ikke en test mot en null, og differansen er ingen fysisk
effekt. Selv mulighet for begge momentane driftfortegn betyr ikke fravær
av vekstbias i de besøkte tilstandene.

Isolerte enheter kan ikke få naboer med noen UC3-operasjon. Antallet aktive
enheter er derfor ikke-økende. Kutt kan strande den flyttende enheten ved
en tidligere grad-1-målnode, eller andre enheter ved en isolert kilde.
Dette gir en lokal, irreversibel tapsmekanisme. At alle 16 faktisk absorberte
beviser ikke at alle mulige starttilstander eller uendelige baner må gjøre det.
Flere forsøk etter en allerede absorbert tilstand kan derimot ikke hjelpe.
En read-only hendelsesaudit fant 256 tap av aktive enheter fordelt på 240
kutt, maksimalt tre tap i én hendelse, og ingen økning av aktivt enhetstall.
Ved slutt fantes fortsatt **163 kantbærende komponenter uten enheter**, med
944 noder og 809 kanter. 18 av disse hadde en 2-kjerne, totalt 80 kjernenoder.
De er frosne, forlatte grafrester, ikke aktivt vedlikeholdt struktur. Eksemplet
viser hvorfor ren formoverlevelse ville vært et misvisende hovedmål her.

## Verifisering og evidens

**78 målrettede tester besto**, med UC1/UC2-regresjoner. Kjernen ble dessuten
kontrollert på 1 120 uttømmende smågraf-overganger og en separat, uavhengig
reprodusert stresstest med 8 000 fler-enhetsforsøk uten invariantfeil.
Se [kvalifiseringen](UC3_qualification.md). Dette kvalifiserer denne avgrensede
implementasjonen, ikke enhver simulator eller alle lange vekstregimer.

Full frossen replay gjenskapte alle fem rå-/avledede produkter per stadium:
32 referansehistorier med 32 768 endringer og 16 kandidatforløp med 29 198
forsøk. Kilde-/protokollhasher, PRNG, hendelser, observasjoner, summer og
referansegate samsvarte. Kandidatverifikasjonen replay-verifiserer også
kalibreringen. Ingen verifisering mot hele `Documentation/` ble kjørt.

En separat observatøraudit uten import av runner/observatør rekonstruerte
vinduene fra 1 189 frame-rader og bekreftet alle eksponeringssummer og nullene.
Alle ni mulige vinduer feilet både størrelse- og kjernekravet; bare tre
inneholdt starttreets bilde. Seks senere vinduer feilet altså også, ved
komponenter på 2–4 noder uten kjerne. 176/256 spor nådde enkeltbilder med
begge størrelseskrav (49/64 og 127/192). Frame-CSV alene inneholder ikke
identitetssettene for uavhengig turnover-rekonstruksjon; nullene er allerede
avgjort av de tidligere kravene. Full seeded replay rekonstruerer også settene.

En annen uavhengig audit uten repo-importer rekonstruerte hele kandidatens
29 198 forsøk: seedede starttrær/verter, klasseskjema og målvalg, lovlige
omskrivinger, bevart enhetsidentitet, fragmentering og komponentklokker.
Den sammenlignet alle 1 189 frames og observatør-/sammendragsfelter og fant
ingen avvik. Dette inkluderer de frosne, ubemannede sluttstrukturene ovenfor.

- [Kalibrering og hasher](UC3_calibration.json), [summer](UC3_calibration_summary.csv), [start](UC3_calibration_initial.json), [alle hendelser](UC3_calibration_events.csv), [frames](UC3_calibration_frames.csv), [observasjoner](UC3_calibration_observations.json).
- [Kandidat og hasher](UC3_candidate.json), [summer](UC3_candidate_summary.csv), [start](UC3_candidate_initial.json), [alle forsøk](UC3_candidate_events.csv), [frames](UC3_candidate_frames.csv), [observasjoner](UC3_candidate_observations.json).
- [Deklarert, kildehashet proveniensgraf](UC3_provenance.md), uten ny database eller automatisk slutning.

## Publiseringsgrense

Rapport, rådata og avgrensninger committes/pushes i resultatetappen. Det
statiske arkivet bygges fra akkurat denne resultatcommitten og kontrolleres
via HTTPS mot manifest og alle 20 UC3-artefakter. Åtte små UC3-dokumenter
synkes til egen RAG-kildemappe; rå hendelser forblir i checksum-arkivet.
Eldre kilder bevares. Nettarkivets manifest og oppgavens sluttkvittering
angir kontrollert resultatcommit og faktisk synkutfall.

Oppbrukte API-kreditter blokkerte forrige virkelige generative RAG-query.
Ingen endret kredittilstand er bekreftet; testen skal ikke gjentas uendret,
kreditter kjøpes eller tokenrettigheter utvides for å få en grønn kvittering.
Modellfri token-/korpuskontroll kan vise tilgang og nye kildebytes, men
erstatter ikke den påkrevde generative sitat-, PostgreSQL-rate-limit- og
ferskhetsauditen. Full rundepublisering forblir derfor `publication_blocked`.
Ingen fysikk-, livs-, Lorentz- eller generell vekstpåstand følger av UC3.
