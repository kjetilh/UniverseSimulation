# UC3M — gir en sammenhengende rest mer ny vekst etter to sykluser?

Vi fant ingen påviselig vekstfordel. Av 512 nye verdener ga 54 en lovlig sammenligning med like umiddelbare vekstmuligheter. Etter to vekst- og tapssykluser vokste kjernen igjen i 1099 av 1728 fortsettelser med bevart rest (63,60 %) og 1108 av 1728 med omkoblet rest (64,12 %). Forskjellen var −0,52 prosentpoeng for bevart minus omkoblet, med et verdensvist 95 % bootstrapintervall fra −3,30 til +2,26 prosentpoeng. Målet fulgte samme enhet gjennom inntil 96 lokale endringer. Resultatet gjelder to flyttede forbindelser i en sammenhengende rest med minst fire kanter.

## Hva ble sammenlignet?

Utgangspunktet var første halvering av en tidligere lokal 2-kjerne på minst fire noder langs hvert enhetsspor. Vi valgte én match per verden. I de 54 parene hadde den utvalgte sammenhengende resten fra 4 til 40 uavbrutt overlevende kanter, med median 10. Kontrollens enhet krysset samme kant frem og tilbake og flyttet én tilstøtende restkant ved hvert hopp. I bevaringsarmen gjennomførte enheten en lovlig knoppskyting og den omvendte kollapsen. Dette bevarte hele restens topologi og alle gamle kantinstanser. Det nye nodenavnet ble brukt opp. Begge armene endte med samme enhetsplasseringer, nodegrader, komponenter og fokale kjernestørrelse.

I 43 av 54 kontroller ble de opprinnelige uavbrutte blokkantene delt i flere deler. Største gjenværende del hadde median 5 kanter. Omkoblede kanter og andre kanter i den fysiske grafen kunne fortsatt forbinde delene. Fargeraffinering bekreftet en forskjell i den faktiske grafens topologi sett fra enheten. For hver handlende enhet og hendelsesklasse matchet vi fordelingen av neste kjernestørrelse og ved kutt også oppsplitting.

## Gjentatt vekst i samme linje

Én persistent enhet definerte linjen. Etter et kutt fulgte vi den delen som inneholdt enheten. Hver pil krevde minst to kjernenoders endring på en ny lokal hendelse. Vi registrerte først vekst fra start, deretter fall fra løpende topp, vekst fra løpende bunn, et nytt fall og ny vekst. Enheten trengte ikke selv å utføre endringen.

| Antall fortsettelser som nådde trinnet | Bevart | Omkoblet |
| --- | ---: | ---: |
| Første vekst | 1375 | 1397 |
| Første fall etter vekst | 1375 | 1396 |
| Andre vekst | 1233 | 1248 |
| Andre fall etter vekst | 1233 | 1247 |
| Tredje vekst, primært utfall | 1099 | 1108 |

Alle 1728 fortsettelser i hver arm inngår i nevneren. I bevaringsarmen opphørte aktiviteten i den fulgte komponenten før treff i 611 forløp, og 18 nådde vinduets slutt. I den omkoblede armen var tallene 608 og 12. Ingen ble sensurert.

Ved startstørrelse 32 var treffene 302 mot 288 av 480 per arm (15 matchede verdener). Ved størrelse 96 var de 797 mot 820 av 1248 (39 verdener). Verdensforskjellen gikk i positiv retning i 22 verdener, var null i 5 og negativ i 27. Den forhåndsregistrerte ensidige fortegnstesten ga p = 0,804. Det var 32 stokastiske fortsettelser fra hver tilstand. Usikkerheten ble beregnet ved å trekke hele verdener innen hver startstørrelse.

## Kontroller og rekkevidde

Før naturlig oppfølging ga kontrollerte, lovlige knoppskytinger og kollapser 1728 av 1728 treff i hver arm. Nullforløp med et reversibelt skyv ga 0 av 1728 i hver arm. Begge referansene brukte de samme startgrafene og den samme observatøren som forsøket. Alle 512 verdener står i dekningstabellen. De 458 uten match gikk ut da ingen gjenværende aktiv tagg kunne gi et kvalifisert første tap.

Gjentatte vekstepisoder forekom ofte under begge betingelser. Det var ikke påkrevd at den gamle resten fortsatt fantes ved tredje vekst, eller at den senere kjernen lå på de samme nodene. En linje kan derfor oppfylle endepunktet gjennom lokale svingninger uten å akkumulere struktur. Forsøket endret to kanter i en blokk. Det estimerer ikke en dose–respons mellom blokkstørrelse og vekst. Beslutningen er å beholde gjentatt vekst som observasjon. Hvis spørsmålet videre er kumulativ organisering, må et nytt endepunkt følge hva som faktisk bæres videre mellom episodene.

## Datagrunnlag

[Protokoll](UC3M_protocol.md) · [Resultat og kildehasher](UC3M_result.json) · [Alle verdener](UC3M_worlds.csv) · [Startpar og inngrep](UC3M_pairs.jsonl) · [Alle forløp med lokale tikk og kjernestørrelse ved hver passering](UC3M_followups.csv.gz).

En separat verifikator rekonstruerte alle 512 prefikser og de 54 tapstilstandene. Den prøvde 9484 lovlige enkelttrekk i startparene og kontrollerte alle 10 368 oppfølgingsrader. Den fant terskelpasseringene på nytt fra de gjenskapte kjernestørrelsene. Identiske deterministiske nullforløp ble spilt én gang per arm og verden.

Frossen forsøksrevisjon før nye verdener: `a0c5fe508ebf75de6d6a631ad99ebfd2dc7f7619`. Reproduser med Python fra reporoten:

~~~sh
out=$(mktemp -d)
python3 -B Tools/run_uc3m.py --out "$out" --workers 6
python3 -B Tools/verify_uc3m.py --out "$out"
~~~
