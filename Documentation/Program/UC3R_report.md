# UC3R — en overlevende relasjon blir faktisk brukt i ny vekst

4. november 2026. Etteranalyse av alle 16 eksisterende UC3-verdener.
Ingen ny simulering, ingen endring av loven og ingen ny effektgate.

**Ja, direkte viderebruk forekom.** Etter et lokalt fall i kjernestørrelse
brukte 35 forskjellige knoppskytinger en relasjon fra den tidligere kjernen
som hadde overlevd uten avbrudd. Dette skjedde i 15/16 verdener. 18 av de
35 brukte en relasjon som selv var opprettet under kjøringen, i 9/16
verdener. I 13/16 verdener fant vi også ny kjernevekst ved eller etter et
treff. Dette er en observasjon av videreføring; den viser ikke at restene
økte veksten, at organiseringen akkumulerte, eller at noe overlevde den
endelige aktivitetsstansen.

## Et forløp man kan etterprøve

Verden `n32-5`, spor 5. Tikk er vellykkede endringer i hele verdenen;
observasjonsvinduet teller bare endringer i sporets egen komponent.

| Tikk | Hva som skjedde |
| ---: | --- |
| 1 | En knoppskyting fra 14 med anker 15 dannet node 32. Kanten 14–32 begynte her, ikke i starttreet. |
| 9 | Komponentens 2-kjerne nådde en topp på 10 noder. 14–32 var da en kjernekant. |
| 15 | Node 33 kollapset. Kjernen falt til 3 noder; ni av toppens kantinstanser var fremdeles tilgjengelige i komponenten, ikke nødvendigvis i kjernen. |
| 16 | Enheten ved 32 brukte nettopp kanten 32–14 som anker for ny node 34. Kjernen vokste til 4. Begge de to tilgjengelige kantene var rester. |
| 22 | Den nye noden 34 ble selv brukt som kilde for neste knopp, node 35 med anker 32. Kjernen hadde nå 5 noder, to mer enn ved tapet. |

Dette er mer enn gjenkjennelse av et nodenavn eller en lignende form:
vi kan identifisere både den uavbrutt overlevende kanten og den konkrete
senere hendelsen den inngikk i. Det betydde likevel ikke at enheten ved
tikk 16 foretrakk gamle forbindelser; den kunne ikke velge noe annet enn
en rest. Tikk 22 viser en videreføring, ikke mange gjentatte sykluser.
Eksemplet er valgt etter opptelling for å vise adskilte tikk, ikke som
grunnlag for hyppighetsberegningen.

## Definisjon og dekning

[Uttrekksregelen](UC3R_protocol.md) ble skrevet før den nye opptellingen.
De tidligere UC3-resultatene var kjent; dette er ikke en blind, prospektiv
test. En 2-kjerne er den delen av komponenten som står igjen når noder med
færre enn to naboer fjernes gjentatte ganger. Det er et mål på en del av
topologien, ikke en påstand om at vi har identifisert et fysisk objekt.

Vi fulgte alle 256 opprinnelige enheter. Første gang en kjerne på minst
fire noder falt til halvparten eller mindre av sin tidligere topp, merket
observatøren de overlevende kantinstansene fra toppen. Hver senere knopp i
de neste 16 lokale endringene ble undersøkt. Den måtte bruke samme par
endepunkter **uten sletting og gjenoppretting** for å telle som treff.
Etter en oppsplitting teller bare enhetens egen etterkommerkomponent.
Ingen historiske merker ble lest av dynamikken.

| Opptelling | Start N=32 | Start N=96 | Totalt |
| --- | ---: | ---: | ---: |
| Verdener | 8 | 8 | 16 |
| Spor med topp og påfølgende tap / alle spor | 55/64 | 170/192 | 225/256 |
| Spor med minst én overlevende kant | 53 | 164 | 217 |
| Spor med noen senere knopp | 49 | 155 | 204 |
| Distinkte knopper i de observerte vinduene | 42 | 90 | 132 |
| Distinkte knopper som brukte en rest | 12 | 23 | 35 |
| Derav treff på kant dannet etter start | 5 | 13 | 18 |
| Verdener med treff | 8 | 7 | 15 |
| Verdener med treff på kant dannet etter start | 4 | 5 | 9 |
| Verdener med treff og samtidig/senere ny kjernevekst | 6 | 7 | 13 |

31 spor nådde aldri en stor nok topp. Blant de 225 tapene var 83 knyttet
til oppsplitting, 52 til kutt uten oppsplitting, 89 til nodekollaps og
ett til en relasjonsflytting. Tallene er **spor**, ikke 225 uavhengige
kollapser. 8 av de 225 sporene hadde tom rest. 187 fikk alle 16
oppfølgingsendringene, 38 færre enn 16, derav 5 ingen. Spor uten ny vekst
er beholdt. Alle de opprinnelige kjøringene endte med alle enheter isolert.

## Hvor mye skyldes tilgjengeligheten?

En UC3-knopp må bruke en eksisterende kant. Vi sammenlignet derfor hvert
treff med andelen tilgjengelige restkanter blant **akkurat den handlende
enhetens naboer ved den hendelsen**. Dette er et regnestykke fra den kjente
loven, ikke en målt, matchet nullmodell for hele utviklingen.

Overlappende enhetsspor ga 765 observasjoner av 132 forskjellige knopper.
I 484 observasjoner fantes ingen tilgjengelig restkant; i 170 var alle
tilgjengelige kanter rester. I de 111 med et reelt valg mellom typene ble
en rest brukt 75 ganger. Summen ble 245 spor-treff mot en betinget
forventningssum på 230,73. Verdensvise fortegn på observert minus forventet:
6 positive, 6 like og 4 negative. Hver fysisk knopp telles bare én gang
per verden og tikk i hovedtallet 35 (treff i minst ett spor). 35/132 er
ikke en sannsynlighet for vilkårlig vekst eller en replikert effektstørrelse.
Det finnes ingen ny kausal gate, p-verdi eller preferansekonklusjon.

## Hva som er åpent, og neste beslutning

Den gamle UC3-målingen krevde to formmessig like perioder. Her spurte vi om
en enkelt nedbygging kunne etterlate en identifiserbar forbindelse som ny
vekst benyttet, uten at formen måtte gjenta seg. Resultatene motsier ikke
hverandre. Vi undersøker en liten kjerneskala, første tap per spor og et
kort vindu. En relasjon som skifter endepunkt teller ikke som bokstavelig
overlevelse her; annen slags organisatorisk videreføring kan derfor være
oversett. Et kjernetap ved fragmentering er heller ikke ensbetydende med at
noder er fysisk fjernet.

**Neste beslutning:** Behold dette som et observasjonsmål. For å undersøke
om restens organisering gjør en forskjell, må resultatet måles uavhengig
av restmerkene (f.eks. videre lokal kjernevekst, også når den uteblir) i
lovlige, sammenlignbare fortsettelser med bevart versus endret resttopologi.
Lik størrelse, aktivitet, muligheter for lokale trekk og fragmentering må
kontrolleres uten å forutsette at en slik null finnes. Mål både null og
positiv referanse gjennom samme konstruksjon, arm og utvalgsstørrelse før
en gate; bruk ferske verdener. Akkumulering krever i tillegg flere
etterfølgende vekst-/tapsepisoder i samme etterkommerlinje. Ingen av disse
testene er utført her.

## Evidens og reproduksjon

[Resultat og hasher](UC3R_result.json) · [alle verdener](UC3R_worlds.csv) ·
[alle enhetsspor og restkanter](UC3R_tags.csv) · [alle observerte knopper og
deres lokale valgmuligheter](UC3R_buds.csv). Originale hendelser og
starttilstander er uendret: `Documentation/Program/UC3_candidate.json`
i repoet, eller [det arkiverte UC3-kildemanifestet](https://emergentuniverse.haven.digipomps.org/data/uc3_local_growth/UC3_candidate.json).

Fra reporoten, med en ny tom målkatalog:

~~~sh
out=$(mktemp -d)
python3 -B Tools/observe_uc3_remnants.py --out "$out"
python3 -B Tools/verify_uc3_remnants.py --out "$out"
python3 -B -m unittest tests.test_uc3_remnants
~~~

De to implementasjonene rekonstruerte de samme 29 198 forsøkene og 4 525
endringene, uten nye tilfeldige trekk. Den uavhengige kontrollen brukte
egne naboskap, kjerneberegning og lokale historikker; den kontrollerte
16 sluttilstandshasher, 1 189 arkivrammer, alle 256 spor og alle 765
knoppobservasjoner, inkludert kantgenerasjon og teller/nevner for lokal
tilgjengelighet. Fem konstruerte kodekontroller dekker blant annet kutt,
gjenopprettet kant, kant utenfor nåværende kjerne og 16-endringersgrensen.
De er ikke effektkontroller. Den separate maskinlesbare kvitteringen
for UC3R er beskrivende; den avgjør ingen fysikkhypotese.

## Status ved lokal resultatcommit

51 målrettede tester besto. Lokal arkivbygging ga seks UC3R-filer med
korrekte sjekksummer; konfigurasjonen for den dedikerte RAG-en peker kun på
rapport, uttrekksregel og verdenstabell. Ingen av disse kontrollene er en
live- eller RAG-query-kvittering.

Publisering ved lokal sluttkontroll: **publication_blocked**. Før
resultatcommit var aktiv branch fem andre lokale commits foran den verifiserte
fjernreferansen `408c00b00d7482e6158fc381bf8c0d65a0312ea1`. En vanlig push
av aktiv branch inkluderer også disse. Den avklaringen er skilt fra
selve målingen; det er ikke gjort force-push, omskriving eller sammenblanding
av evidens. Inntil en revisjon med resultatet faktisk er pushet, publisert
og verifisert, er det ingen UC3R-livekvittering eller bekreftet RAG-synk.
