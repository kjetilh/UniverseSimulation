# UC3I — gamle forbindelser i tre vekstkjerner gjennom to tap

I 32 av 512 nye verdener kunne vi sammenligne en bevart rest med en lovlig omkoblet rest med samme umiddelbare vekstmuligheter og de samme gamle kantene å følge. Minst én og samme forbindelse overlevde begge tapene og inngikk i alle tre vekstkjernene i 430 av 1024 naturlige fortsettelser med bevart rest (41,99 %) og 446 av 1024 med omkoblet rest (43,55 %). Bevaring minus omkobling ga −1,56 prosentpoeng, med et verdensvist 95 % bootstrapintervall fra −5,47 til +2,64 prosentpoeng. Vi observerte strukturell arv i begge armer i alle 32 matchede verdener. Forsøket påviste ingen fordel ved å bevare blokkens opprinnelige organisering.

## Hva overlevde?

Starten var første matchbare halvering av en tidligere lokal 2-kjerne. Begge armer fulgte samme enhet og de samme 1–23 kantinstansene per verden (median 6). Kantene kom fra den gamle kjernetoppen og var fremdeles i begge kjernene etter oppsett. En uavbrutt kant kunne gå ut av kjernen ved tapet og inngå i den igjen ved vekst. Hvis en kant ble fjernet, mistet den sin identitet selv om det samme nodeparet senere ble koblet sammen. Merkingen påvirket ingen trekk.

| Utfall innen 96 lokale endringer | Bevart, av 1024 | Omkoblet, av 1024 |
| --- | ---: | ---: |
| Tre vekstepisoder med to mellomliggende tap i samme linje | 729 | 723 |
| Minst én samme gammel kant i alle tre vekstkjerner | 430 | 446 |
| Minst to samme gamle kanter i alle tre vekstkjerner | 328 | 292 |
| Minst én samme gammel kant i kjernen også ved begge tap | 404 | 420 |

For eksempel startet den bevarte fortsettelsen 2 i verden m32-1000047 med fire kjernenoder. Etter 5, 7, 11, 12 og 20 lokale endringer var kjernestørrelsene henholdsvis 6, 4, 7, 5 og 7. Kantene mellom nodene 25 og 36 (født ved verdenstikk 23) og mellom 36 og 38 (født ved tikk 26) overlevde hele forløpet. Begge var kjernemedlemmer ved alle fem passeringer.

## Sammenligning og rekkevidde

I kontrollen flyttet enheten to kanter i den gamle sammenhengende blokken ved to lovlige hopp. I den andre armen gjenopprettet en knoppskyting og en umiddelbar kollaps den opprinnelige grafen. Felles kantliste hindret at kontrollen kunne tape målingen allerede ved oppsettet. De to armene hadde like nodegrader og enhetsplasseringer, og samme umiddelbare fordeling av kjernestørrelse for hver enhet og hendelsesklasse, inkludert oppsplitting ved kutt. Etter et kutt fulgte vi den komponenten som inneholdt den samme enheten. Kjernen var komponentens 2-kjerne, som også kan inneholde kanter et stykke fra den lokale endringen.

Av de 512 undersøkte verdenene ga 469 ingen match før de aktuelle enhetene var ferdig fulgt. I 11 andre var den felles kantlisten tom. De 32 matchede verdenene omfattet 9 med startstørrelse 32 og 23 med startstørrelse 96. Hver verden ga 32 uavhengig sådde fortsettelser per arm. Alle er med i nevneren. Henholdsvis 284 og 292 forløp endte ved isolasjon, og 11 og 9 nådde tidsvinduets slutt uten å ha fullført alle syklusene. Ingen forløp ble sensurert.

Forskjellen favoriserte bevart rest i 10 verdener og omkoblet i 18, med likt utfall i 4. Forhåndsregistrert ensidig fortegnstest ga p = 0,956. Det verdensvise intervallet tillater en mindre fordel i begge retninger. Den forhåndsregistrerte beslutningen gjelder minst én arvet kant. Antall med flere kanter og medlemskap ved tapene er beskrivende.

## Referanser og beslutning

Begge instrumentreferanser fullførte alle tre vekstepisoder og begge tap i 1024 av 1024 fortsettelser i hver arm. I den positive referansen vokste nye deler av kjernen ved knoppskyting og falt ved reverserende kollaps. Her målte vi arv i 1024 av 1024 i hver arm. I nullreferansen fortsatte den samme enheten i en ny komponent etter å ha brutt alle forbindelsene til utgangspunktet. Her målte vi arv i 0 av 1024 i hver arm.

Forsøket viser at konkrete gamle forbindelser kan være del av gjentatte vekstkjerner i denne modellen. Det står åpent om veksten skjer ved selve de arvede kantene, om kantene bidrar til å drive veksten, og om struktur akkumuleres. Beslutningen er å beholde kantarv som en målt observasjon. For å undersøke mekanismen videre må vi skille mellom vekst som bruker en arvet kant, og vekst andre steder i samme kjerne.

En separat verifikator gjenskapte alle 512 prefikser og 6144 forløp, kontrollerte 7200 lovlige ettstegsoverganger i startparene, fant de fem tersklene fra kjernestørrelsene og kontrollerte kantvitnene mot hver faktisk fjernet forbindelse.

[Forhåndsregistrert protokoll](UC3I_protocol.md) · [Maskinlesbart resultat og kildehasher](UC3I_result.json) · [Alle verdener](UC3I_worlds.csv) · [Tapstilstander og felles kantlister](UC3I_pairs.jsonl) · [Alle forløp og kantvitner ved hver passering](UC3I_followups.csv.gz).

Forsøksrevisjon før de nye verdenene ble kjørt: `632df04a230cb89dfa97623092c6904a7198627a`. Kjør fra reporoten med et tomt resultatmål:

~~~sh
out=$(mktemp -d)
python3 -B Tools/run_uc3i.py --out "$out"
python3 -B Tools/verify_uc3i.py --out "$out"
~~~
