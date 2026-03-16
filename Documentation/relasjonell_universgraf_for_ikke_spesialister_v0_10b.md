# Relasjonell universgraf v0.10b–v0.10d forklart for ikke-spesialister

## Hvor er vi nå?

Vi har brukt lang tid på å teste en idé om at universet kan beskrives som en dynamisk graf av noder og relasjoner.
Et viktig spørsmål er om slike grafer kan lage stabile, store strukturer som minner om noe fysisk.

Men før man kan stole på slike tester, må man vite at startgrafene faktisk er så store som man tror.

Det var nettopp problemet her.

## Hva var feilen?

Vi hadde startensembler som på papiret het ting som `192` og `256`.
Det skulle bety at de startet med omtrent 192 eller 256 noder.

Men når vi faktisk målte dem, viste det seg at de ofte bare startet med rundt 90–115 noder.

Det betyr at de ikke var ekte store tester.
De bare så store ut i navnet.

## Hvorfor er det viktig?

Fordi hvis man da finner rare eksponenter eller merkelige skaleringslover, kan det skyldes at generatoren laget feil størrelse på startgrafene — ikke at universmodellen har funnet noe dypt.

Kort sagt:
vi risikerte å tolke en generatorfeil som fysikk.

## Hva gjorde vi?

Vi gjorde tre ting:

### 1. Vi målte generatoren ærlig
Vi skilte mellom:
- **nominell størrelse**: hva vi ba om
- **realisert størrelse**: hva vi faktisk fikk

### 2. Vi prøvde å justere dagens generator
Det hjalp litt på små og mellomstore nivåer.
Men det reddet ikke de store nivåene.

### 3. Vi laget et nytt growth-regime
Det nye regimet er laget for å bygge store, mer realistiske startgrafer uten at nivåene kollapser ned til omtrent samme størrelse.

## Hva fant vi?

Det viktigste er dette:

- Den gamle generatoren er **ikke god nok** for store startensembler.
- En ny generatorvariant, kalt **`fast_balanced` i deep-variant**, fungerer klart bedre.
- Når vi bruker den nye generatoren, forsvinner mye av de rare, ekstreme skaleringsresultatene.
- Den kandidaten som tidligere så best ut, **`band_best`**, ser fortsatt best ut også etter at generatorfeilen er ryddet opp.

Det er et godt tegn.

## Hvorfor er det et godt tegn?

Fordi det betyr at `band_best` ikke bare vant fordi startgrafene var feil.
Den holder seg best også når testoppsettet blir strengere.

Det gjør ikke modellen bevist.
Men det gjør prosjektet mer interessant.

## Hva betyr dette i vanlig språk?

Vi er fortsatt ikke i mål med en universteori.

Men vi er forbi et viktig faresignal:
prosjektet klarer nå bedre å skille mellom

- ting som bare skyldes hvordan vi laget startdata,
- og ting som faktisk skyldes hvordan selve dynamikken oppfører seg.

Det er mye mer verdifullt enn å få “spennende” tall for fort.

## Hva bør brukes videre?

Hvis andre skal jobbe videre på prosjektet, bør de bruke:

**`fast_balanced` / deep**

som standardmåte å lage store naturlige startgrafer på.

Og hvis de vil teste kandidater videre, bør de først og fremst teste:

- `band_best`
- én eller to utfordrere
- én kontrollkandidat

## Kort oppsummert

- Vi fant en generatorfeil.
- Vi målte den i stedet for å ignorere den.
- Vi laget et bedre growth-regime.
- Den tidligere beste kandidaten holder seg fortsatt best.
- Prosjektet virker derfor mer robust nå enn før.

Det betyr ikke at universteorien er riktig.
Det betyr at prosjektet begynner å oppføre seg mer som seriøs forskning enn som bare idémyldring.
