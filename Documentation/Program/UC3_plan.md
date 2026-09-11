# UC3 — lokal vekst, dekomponering og tilbakekomst med utskiftede deler

Dato: 2026-09-11. Work ID `UC3`; base `95df96c5037b9a48bf4abe5ff32b4b7f763b45e3`;
branch `program/wp-f2-f3-20260908`; koordinator/integrator root.
Status ved opprettelse: **CLAIMED — plan og instrumentering, ingen kandidatdata**.

## Formål og utføringsplan

Undersøk én eksplisitt lokal utvidelse av UC2 som tillater nodevekst, lokal
tilbakedanning og fragmentering. Mål om en grov organisasjonsprofil vender
tilbake gjennom vekst og nedgang mens deler faktisk skiftes ut. Dette er et
mer overordnet spørsmål enn eksakt mikrotilstandsretur, men ikke en modell
av liv, biosfæren, energi eller termodynamikk.

1. Velg regel ut fra lokalitet og algebra, ikke kandidatresultater.
2. Implementer og test kjernen og en adskilt observatør. Bevar UC2 uendret.
3. Frys protokoll/kilder og push før fulle referanse- og kandidatkjøringer.
4. Mål positive/null-referanser; stopp før kandidat hvis instrumentet feiler.
5. Kjør én frossen kandidat på to forhåndsvalgte størrelser, uten parametersøk.
6. Replay-verifiser, dokumenter rådata, eksponering og begrensninger, commit/push,
   publiser nettarkiv og synk den separate RAG-en. Generativ RAG-gate var sist
   blokkert av oppbrukte leverandørkreditter; ingen kjøp eller leverandørbytte
   er autorisert av denne planen.

Exclusive ownership: `historical_signal_check` har kun
`Tools/local_growth_candidate.py` og dens testfil; `provenance_index` har kun
`Tools/local_growth_observer.py` og dens testfil; `latest_results_review` har
read-only fagkontroll og deretter kun `tests/test_local_growth_runner.py`.
Root har runner, protokoll, rapport, publisering og Git. Eksisterende skitne
filer og nabotrådens arbeid berøres ikke.

## Premiss og valgte unntak

Tilstanden er en enkel, urettet, uvektet graf og vedvarende endringsenheter
med plasseringer. Ingen koordinater, nodeverdier, kantaldre, lærte vekter,
ressurspoeng eller historikk mates inn i overgangsloven. Tilfeldighetsstrøm,
identifikatorer og tellere er simulatorens bokføring. Nye node-ID-er gjenbrukes
aldri, slik at observatøren ikke forveksler gjenbruk med overlevelse.

Brukeren tillater nye noder. Fødsel nedenfor får derfor et **uttrykkelig lokalt
fødselshopp** langs en kant som opprettes i hendelsen. Alle andre hopp følger
en kant som eksisterer før hendelsen. Dette er en valgt operasjonalisering,
ikke en utledning av at brukerens ord bare kan bety denne loven. En fødsel
eller kollaps er én atomisk grafomskriving og ett endringstikk selv om flere
naboskapsoppføringer endres. Ingen mellomtilstand behandles som fysisk.

Nodefjerning er valgt som én form for lokal dekomponering; endringsenheter
fjernes aldri. Spontan **enhetsfødsel er fortsatt utelatt** for å isolere
topologireglene. Dette begrenser konklusjoner om langsiktig vekst og gjenstart.

## Den ene loven

Velg en enhet uniformt, inkludert blokkerte enheter. Velg deretter hendelsesklasse
med heltallsvektene **slide:bud:collapse:cut = 4:1:2:1**. Et ulovlig klassevalg
gir ett registrert forsøk, ingen fysisk endring, ingen tikk og ingen ny trekning.

| Klasse | Lokal omskriving og hvor samme enhet fortsetter |
| --- | --- |
| Slide | UC2: fra v, velg lovlig ordnet nabopar u,a med u–a fraværende; erstatt v–a med u–a, behold v–u, fortsett ved u. |
| Bud | Velg eksisterende nabo u til v; opprett w med kantene v–w og u–w, behold v–u, fortsett ved w langs den nydannede v–w. |
| Collapse | Bare når v har nøyaktig to innbyrdes forbundne naboer og ingen annen enhet ved v: velg målnabo u, kryss v–u, fjern v og dens to kanter, fortsett ved u. |
| Cut | Velg nabo u, kryss v–u og fjern denne kanten; fortsett ved u. Isolerte noder, enheter og begge komponenter beholdes. |

Lovlige par/naboer velges uniformt. Ingen global komponent-/sykeltest velger
trekk. Globale kontroller er kun assertions og observasjoner. Ingen kuttet
komponent kan kobles til en annen igjen med denne loven.

### Regneaudit før måling

Bud gir ΔN=1, ΔE=2, Δβ=1; collapse gir det motsatte, hvor β=E−N+C.
Slide bevarer N,E,C,β. Cut gir ΔE=−1 og enten ΔC=1 eller Δβ=−1.
Dermed er **E−2N+antall_kutt konstant** og C ikke-avtakende. Dette er
reglenes bokføring, ikke emergente fysiske invarianter. Trekanter er bygd
direkte inn i bud; telling av dem er ingen oppdagelse av organisering.

La A være andelen enheter med minst én nabo og D andelen med lovlig collapse.
Like klassevekter ville gitt forventet ΔN=(A−D)/4≥0: innebygd vekstbias.
De valgte vektene gir i stedet **E[ΔN|tilstand]=(A−2D)/8** og
**E[ΔE|tilstand]=2E[ΔN|tilstand]−A/8**. Begge fortegn for nodedrift er
mulige. Dette er ikke en kalibrert likevekt eller en garanti for stabilitet.
Nyfødte noder blokkerer slide fordi naboene allerede er forbundet.
Kutt mot en grad-1-målnode isolerer enheten permanent. Mulig absorpsjon må
rapporteres, ikke kalles metastabilitet. Nødvendig total absorpsjon er ikke bevist.

Alternativer vurdert: enkel kant-subdivisjon og brobevart fission bevarer β;
brofri fission kan ikke øke β og kan ikke alene skape sykluser fra trær.
Ved bevart E og uten isolerte noder gjelder N≤2E. Slike alternativer er derfor
ikke alene tilstrekkelige for den valgte topologiske muligheten. De er heller
ikke fullstendig matchede nuller for bud, siden de endrer tilgjengelige hopp.

## Bidrag fra «Vurder glemmestrukturer i verktøyk​»

Nabotråden ble lest og direkte konsultert 2026-09-11. Dens read-only svar
anbefaler å skille deloverlevelse, organisasjonslikhet og tidslig orden.
Dette er brukt i observatøren nedenfor. Samme aktuelle graf/enhetsplassering
må gi samme overgangslov uansett historikk; historisk «nyttige» kanter er ikke
tilgjengelig informasjon uten et representert minne. Derfor innføres verken
Oja, kantaldre eller observatørens historikk i fysikklaget.

Ojas originalarbeid gjelder en lineær, vektet nevronmodell med stasjonære
input; det gir ingen direkte regel for dette uvektede universet.
[Oja 1982](https://math.bu.edu/people/gkocker/ma769/oja_1982.pdf).
Tidslige nettverksmotiver skiller topologi fra hendelsesrekkefølge, men
validerer ikke vår observabel. [Kovanen mfl. 2011](https://arxiv.org/abs/1107.5646).
Nullmodeller må angi hvilke egenskaper de bevarer; tilfeldig omstokking kan
endre flere enn den tilsiktede egenskapen. [Gauvin mfl. 2022](https://arxiv.org/abs/1806.04032).

## Observatør: retur av grov form med faktisk delutskifting

Hver vedvarende enhet får et **observatørspor for sin aktuelle sammenhengende
komponent**. En vellykket endring teller som eksponering for alle enheter i
den berørte komponenten før endringen; ved et brudd får begge etterkommere
denne siste felles hendelsen. Etter bruddet flyttes ikke klokken av endringer
i en annen komponent. Disse klokkene påvirker aldri dynamikken.

Snapshots tas hver n₀/4 slike endringer, hvor n₀ er initial størrelse: 8 ved
32 noder, 24 ved 96 noder. Ett fast lag L=8 snapshots gir 2n₀ komponentendringer
per prøvd periode. Vi søker ikke over lag. Når komponentstørrelsen endres,
er dette fortsatt en probe på **initialskalaen**, ikke en skala-uavhengig
detektor eller en påstand om reell makroskopisk størrelse.

Registrer komponentens N, E, β og 2-kjerne K med kjernekanter F. En 2-kjerne
er det som gjenstår etter gjentatt fjerning av noder med grad mindre enn to;
det er ikke automatisk en organisme eller et metastabilt objekt.

Et vindu med 2L+1 snapshots kvalifiserer bare dersom:

- Alle faser har N≥16 og |K|≥4.
- For hver tilsvarende fase er relativ N-forskjell ≤0,10, forskjell i |K|/N
  ≤0,05 og forskjell i β/max(E,1) ≤0,05.
- Hver av de to periodene har max(N)/min(N)≥1,5: en konstant profil teller ikke.
- Begge perioder har minst 0,25 balansert utskifting av både K og F mellom
  endefasene: min(|gammelt\nytt|,|nytt\gammelt|)/max(1,|gammelt|,|nytt|).

Primært mål er gjennomsnittet over de faste enhetssporene av andelen mulige
vinduer som kvalifiserer. For få snapshots gir 0 **med egen utilstrekkelig-
eksponeringsmarkør**, ikke evidens for fravær. Størrelse/kjerne-eksponering
rapporteres separat. Enheter i samme komponent er korrelerte observasjoner,
ikke uavhengige replikater; uavhengig forsøksenhet er én frøkjøring.
Rå identiteter brukes bare til å påvise reell utskifting og kontinuitet.
Konsistent ommerking av hele historien endrer ikke målet.

Kvalifiserende vinduer merkes særskilt dersom et faktisk komponentbrudd
inngår: et plutselig massetap kan skyldes oppsplitting, ikke nodekollaps.
Global størrelse, kutt, vekst, kollaps, inaktive enheter og sensur registreres
ved siden av målet. Dette er ingen generell test av selvopprettholdelse.

## Referanser før kandidat

Start med en vifte: anker 0, kjede 1…15, alle kjedenoder koblet til ankeret,
to enheter ved kjedens ender. Bud ved høyre ende og collapse ved venstre ende
kan fornye delene uten å miste sammenheng. Alle kontrollhendelser skal være
lovlige UC3-hendelser og replay-verifiseres.

Positiv: 16 buds ved høyre ende, så 16 collapses ved venstre, 32 perioder.
Null: per periode et **uniformt Dyck-ord** med 16 buds og 16 collapses,
betinget på at høyden ved minst ett observert firestegspunkt er ≥8.
Eksakte fullføringsantall brukes til sampling, ikke naive myntkast/retry.
Dette bevarer start/sluttstørrelse, fødsels-/kollapstall, antall endringer
og en observert stor ekskursjon per justert periode, men ikke faseformen.
Kjør 16 par. Krev positiv median større enn nullmedian og ensidig paret
fortegnsskår ≤0,05; fortegn skal være uendret ved kvadrering.

Kontrollene validerer bare det **sammensatte instrumentet**. Viftene har
kjerneandel 1, og turnover følger i stor grad av konstruksjonen. Hvert delmål
er ikke dermed uavhengig dynamisk kvalifisert. Kontroller for frosset struktur,
ren akkresjon og konsekvent ommerking legges i testene. Ingen av disse nullene
er en effekt-null for hele kandidatens stokastiske lov. Biosfæren brukes som
spørsmålsstillende analogi, ikke som belegg for at mekanismen er riktig.

## Kandidat og stopp

Uniforme merkede Prüfer-trær med N=32 og 96, åtte frø hver; henholdsvis 8 og 24
enheter uniformt plassert på alle noder, uten aktivitetsbetinging. Maksimalt
16 384 forsøk eller 4 096 vellykkede endringer. Stopp også ved alle enheter
isolert eller N≥1024; ressursgrensen sensurerer hele kjøringen og deaktiverer
ikke stille fødselsregelen. Ingen tilpasning etter data. Alle forsøk logges.

Utfallet er beskrivende. Positiv primærskår er et vitne om akkurat dette
endepunktet, ikke en signifikant effekt utover en matchet null. Nullskår
avkrefter verken støyende vedvarende form, andre skalaer eller hele hypotesen.
Hvis en drifts-/kodefeil finnes, er to avgrensede implementasjonsrettelser
tillatt før det berørte sporet stoppes. Kilde-/protokollendring etter måling
krever en ny registrert runde; ingen skjult rerun av kandidaten.
