# Relasjonell universgraf – forklart for ikke-spesialister (v0.9b)

## Hva prøver prosjektet å gjøre?

Tenk deg at universet ikke i bunn og grunn er ting som ligger i et ferdig rom, men et enormt nettverk av forbindelser som stadig endrer seg.

I prosjektet vårt prøver vi å se om noe som ligner:

- rom,
- tid,
- partikler,
- og stabil fysikk

kan vokse fram av et slikt nettverk.

## Hva gjør vi konkret?

Vi lar en datamodell bygge slike nettverk og så undersøker vi:

- om de kan lage stabile strukturer,
- om små forstyrrelser sprer seg kontrollert,
- og om noen regimer ser mer “fysiske” ut enn andre.

## Hva har vi funnet fram til nå?

Vi har funnet at noen innstillinger i modellen er mye bedre enn andre.

Men v0.9b viste noe enda viktigere:
det som så best ut i forrige runde, så ikke lenger best ut når vi testet strengere.

Det er faktisk bra.

Hvorfor?
Fordi det betyr at modellen ikke bare gir oss pene resultater uansett.
Den begynner å skille mellom:

- ting som bare ser fine ut i små tester,
- og ting som fortsatt ser lovende ut når testen blir vanskeligere.

## Hva er hovedresultatet i v0.9b?

Den nye favoritten er en kandidat vi kaller `band_best`.

Den er ikke den mest prangende på alle tall.
Men den ser mer stabil ut når vi spør:

“Hvis vi gjør systemet større, oppfører det seg fortsatt kontrollert?”

Det er et viktigere spørsmål enn bare å få høy totalscore på små eller middels store tester.

## Hva betyr det i vanlig språk?

Det betyr at prosjektet nå er blitt flinkere til å luke bort falske spor.

Vi er fortsatt langt fra å si at vi har “funnet universet”.
Men vi er nærmere et punkt der vi kan si:

“Disse regimene ser faktisk mer robuste ut enn de andre.”

## Hvor er vi nå?

Vi er i en fase der prosjektet har gått fra ren idé til noe som begynner å ligne forskningsmessig seleksjon:

- idé
- modell
- simulering
- testing
- strengere testing
- forkasting av dårlige kandidater
- innsnevring av gode kandidater

Det er nettopp slik et lovende forskningsprogram ofte ser ut i starten.

## Hva skjer videre?

Neste steg er å gjøre systemene enda større og sjekke om favorittkandidaten fortsatt holder når vi presser modellen enda hardere.
