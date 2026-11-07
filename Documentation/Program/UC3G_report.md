# UC3G — økte bevart reststruktur sjansen for ny lokal kjernevekst?

Vi fant ingen påviselig vekstfordel. I 53 av 128 nye verdener kunne vi sammenligne to lovlige nodehopp med like umiddelbare vekstmuligheter. Kjernen vokste med minst to noder innen 16 lokale endringer i 1263 av 1696 fortsettelser med bevart rest (74,47 %) og i 1286 av 1696 med omkoblet rest (75,83 %). Forskjellen, bevart minus omkoblet, var −1,36 prosentpoeng. Det verdensvise 95 % bootstrapintervallet gikk fra −3,83 til +1,18 prosentpoeng. Forsøket gjelder omkobling av én overlevende kant i matchbare tap. Små fordeler, større inngrep og oppbygging over gjentatte vekstsykluser står åpne.

## Hva som var likt ved start

UC3R viste at en ny knopp kan bruke en kant fra en tidligere kjerne. UC3G stiller et annet spørsmål. Vi tok to kopier ved det samme tapet av minst halve den lokale 2-kjernen. I begge kopiene flyttet den samme enheten seg fra samme kilde til samme mål. I den ene flyttet hoppet en kant utenfor resten og bevarte alle overlevende kjernekantene. I den andre flyttet hoppet én av de overlevende kjernekantene. Begge alternativene hadde samme sannsynlighet under loven ved tapet. De to nye grafene kunne skilles også etter at nodenavnene ble tatt bort, med taggens posisjon og enhetenes plasseringer bevart.

Før fortsettelsene startet, var komponentene, hver nodes grad, alle enhetsplasseringer og den fokale kjernens størrelse like mellom armene. For hver enhet og hver av de fire hendelsesklassene hadde alle lovlige trekk den samme fordelingen av mulige kjernestørrelser ved neste endring. Ved kutt matchet vi også om komponenten ble splittet, og fulgte taggens side. Dermed kan organiseringen fortsatt påvirke senere trekk, selv om vekstmuligheten på første trekk er lik. Den etterfølgende dynamikken får bare se nåværende graf og enheter.

## Hvor ofte kom ny vekst?

| Startstørrelse | Matchede / genererte verdener | Bevart | Omkoblet | Forskjell i prosentpoeng |
| --- | ---: | ---: | ---: | ---: |
| 32 noder | 22 / 64 | 512 / 704 | 523 / 704 | −1,56 |
| 96 noder | 31 / 64 | 751 / 992 | 763 / 992 | −1,21 |
| Samlet | 53 / 128 | 1263 / 1696 | 1286 / 1696 | −1,36 |

Hver matchet verden ga 32 uavhengig trukne fortsettelser per arm. I 22 verdener var treffandelen størst med bevart rest, i 26 med omkoblet rest, og i 5 var den lik. Den forhåndsregistrerte ensidige fortegnstesten ga p = 0,765 for en fordel ved å bevare resten. Både intervallet og fortegnstesten bruker verden som analyseenhet. Det negative punktestimatet gir heller ikke grunnlag for å hevde en fordel ved omkobling.

Alle 128 verdener fikk et første kjernetap i minst ett enhetsspor. 75 manglet et kvalifisert par. Ingen prefiks nådde en beregningsgrense. Blant de 53 parene hadde 16 tapt kjerne ved oppsplitting, og i 9 var hele 2-kjernen borte ved oppsettet. Gamle kanter kunne fortsatt ligge i komponenten. Medianen var 10 overlevende kanter og spennet var 1–35. Det var dermed en begrenset endring å koble om én slik kant.

I den bevarte armen stoppet 201 fortsettelser ved absorpsjon uten ny vekst, og 232 nådde vinduets slutt uten treff. I den omkoblede armen var tallene 185 og 225. Alle teller i nevneren. Ingen fortsettelse ble sensurert.

## Kontroll av målingen

I hver arm ga den lovlige nullreferansen 0 treff av 1696, mens den positive referansen ga 1696 av 1696. Nullreferansen vekslet mellom oppsettshoppet og dets inverse. I den positive referansen gjorde den merkede enheten lovlige knoppskytinger. Vi brukte de samme konkrete starttilstandene, 32 målinger per verden og arm, og den samme vekstdetektoren som i forsøket. Disse konstruerte forløpene kontrollerer at observatøren skiller vekst fra uteblitt vekst.

## Avgrensning og neste beslutning

Dette forsøket undersøkte formen som faktisk var igjen etter et tap. Sammenligningen gjelder valget av hvilken av to kanter ett hopp flytter, hos den første enheten i hver verden som ga en gyldig match. Den kan ikke tilordne en fysisk virkning til alderen på en kant. Tilgjengelige enhetsindekser og nodenavn avgjorde hvilken av flere mulige matcher observatøren tok først.

Behold UC3Rs observasjon av direkte viderebruk. UC3G gir ingen grunn til å bruke overlevelse av én kant som indikator på økt kortsiktig vekstsjanse. Et eget forsøk med et større sammenhengende restmønster eller gjentatte tap i samme linje krever først en ny lovlig kontroll som fortsatt matcher vekstmulighetene. Ingen av disse hypotesene ble avgjort her.

## Evidens og reproduksjon

[Forhåndsregistrert protokoll](UC3G_protocol.md) · [maskinlesbart resultat og hasher](UC3G_result.json) · [alle 128 verdener](UC3G_worlds.csv) · [tapstilstander, overlevende kantinstanser og oppsettshopp](UC3G_pairs.jsonl) · [alle 10 176 referanse- og forsøksforløp, komprimert CSV](UC3G_followups.csv.gz).

Forsøkskoden og protokollen ble fryst og pushet i revisjon `a329d59aaef7705af2311ead964a016b56980d20` før det første nye forsøket. Fra reporoten kan hele målingen gjentas med Python 3.13.2 i en tom målkatalog.

En ny full kjøring ga byteidentiske resultatfiler. En separat verifikator rekonstruerte de 128 verdenshistorikkene fram til stopp, alle 53 matchede tap og begge oppsett per par. Den kjørte 8940 lovlige enkelttrekk gjennom simulatoren for å kontrollere de umiddelbare mulighetene og kontrollerte alle 10 176 oppfølgingsrader. De deterministiske nullforløpene ble spilt én gang per verden og arm, deretter sammenlignet med hvert replikat. 59 målrettede tester besto.

~~~sh
out=$(mktemp -d)
python3 -B Tools/run_uc3g.py --out "$out" --workers 4
python3 -B Tools/verify_uc3g.py --out "$out"
~~~
