
# Relasjonell universgraf v0.4: redusert basis, regelbetingede ΔF-matriser og invariantklassifikasjon

## Formål

Dette dokumentet er neste presise steg etter v0.3-arbeidet med feature-rom og quasi-invarianter.  
Målet her er å gjøre tre ting matematisk skarpt:

1. redusere feature-rommet til en **algebraisk uavhengig basis**,
2. klassifisere **eksakte lineære invariants** som følger av ulike regelklasser,
3. skille mellom
   - rene grafidentiteter,
   - regelstyrte invariants,
   - og empiriske regimevariabler / quasi-invarians-kandidater.

Dette steget er viktig fordi det forhindrer at man feiltolker algebraiske identiteter som fysikk, eller regimeeffekter som fundamentale bevaringslover.

---

## 1. Utgangspunktet i hele prosjektet

Vi arbeider fortsatt innenfor den samme ontologien som er utviklet gjennom hele samtalen:

- universet forstås som informasjon,
- de fundamentale bestanddelene er noder og én type relasjon,
- dynamikken drives av lokale **units of action**,
- tid forstås relasjonelt, som ordning / telling av hendelser,
- spacetime antas å være et emergent makroregime i samme graf,
- partikler og felt tolkes som stabile eller metastabile relasjonelle mønstre,
- entanglement forstås som korrelasjon, ikke som en egen kanal,
- seeds kan oppstå kontinuerlig, men har ingen operasjonell eksistens for hverandre før de er koblet inn i samme komponent.

De tidligere stegene etablerte tre foreløpige innsikter:

1. lokal propagasjon gjør proto-relativitet plausibel,
2. energi bør ikke identifiseres direkte med hendelsesrate,
3. stabile makroregimer krever en presis analyse av hvilke størrelser som faktisk er invariantiske.

Dette dokumentet løser (3) på et mer modent nivå.

---

## 2. Reduksjon av feature-rommet

I v0.3 arbeidet vi med et større feature-rom. Det var nyttig som utforskning, men matematikken blir skarpere dersom vi først fjerner alle features som er algebraisk avledbare av andre.

### 2.1 Fullt feature-set

Det utvidede feature-settet var:

- `tokens`
- `nodes`
- `edges`
- `components`
- `beta1`
- `wedges`
- `triangles`
- `star3`
- `c4`
- `deg_sq_sum`
- `spectral_radius`
- `clustering`
- `dim_proxy`

### 2.2 Algebraiske identiteter

To identiteter er fundamentale:

\[
\beta_1 = E - N + C
\]

der \(E=\text{edges}\), \(N=\text{nodes}\), \(C=\text{components}\),

og

\[
Q_2 := \sum_v \deg(v)^2 = 2E + 2W
\]

der \(W=\text{wedges}\).

Dermed er både `edges` og `deg_sq_sum` algebraisk avledbare når man kjenner
\((nodes, components, beta1, wedges)\).

### 2.3 Redusert basis

Vi velger derfor følgende **reduserte basis**:

- `tokens`
- `nodes`
- `components`
- `beta1`
- `wedges`
- `triangles`
- `star3`
- `c4`
- `spectral_radius`
- `clustering`
- `dim_proxy`

Denne basisen er fortsatt rik nok til å skille mellom:

- lineær topologi / syklusstruktur (`beta1`),
- lokale motivtall (`wedges`, `triangles`, `star3`, `c4`),
- spektral/global struktur (`spectral_radius`),
- geometri-proxyer (`clustering`, `dim_proxy`).

---

## 3. Kjernebasis for eksakt lineær invariantanalyse

Når vi vil klassifisere eksakte lineære invariants av primitive regler, er det lurt å skille ut en enda mindre basis:

\[
F_{\text{core}} = (\text{tokens}, \text{nodes}, \text{components}, \beta_1).
\]

Dette er den minste lineære basisen som bærer:

- action-budsjett (`tokens`),
- volum/utstrekning (`nodes`),
- komponentstruktur (`components`),
- topologisk syklusrang (`beta1`).

Det er nettopp på dette nivået lineær invariantanalyse gir eksakte resultater.

---

## 4. Primitive regler og deres eksakte lineære inkrementer

I simulatorfamilien brukes følgende primitive regler:

- `seed`
- `birth`
- `death`
- `triad`
- `delete`
- `swap`
- `move`

Deres eksakte inkrementer i kjernebasis er:

| regel | Δtokens | Δnodes | Δcomponents | Δbeta1 | tolkning |
| --- | ---: | ---: | ---: | ---: | --- |
| `seed` | 0 | +1 | 0 | 0 | ny bladnode festes til eksisterende komponent |
| `birth` | +1 | 0 | 0 | 0 | et token fødes |
| `death` | -1 | 0 | 0 | 0 | et token dør |
| `triad` | 0 | 0 | 0 | +1 | en ny intern kant opprettes; én uavhengig syklus legges til |
| `delete` | 0 | 0 | 0 | -1 | en ikke-bro-kant fjernes; én uavhengig syklus forsvinner |
| `swap` | 0 | 0 | 0 | 0 | én kant fjernes og en annen legges inn; lineært ingen endring i kjernebasis |
| `move` | 0 | 0 | 0 | 0 | ren traversering uten omskriving |

Dette er ikke empiriske estimater; det er **eksakte regler** i den nåværende simulatorimplementasjonen.

---

## 5. Nullrom og eksakte lineære invariants

En lineær størrelse

\[
I = c \cdot F_{\text{core}}
\]

er eksakt invariant dersom

\[
\Delta F_r \cdot c = 0
\quad\text{for alle primitive regler } r \text{ i valgt regelklasse.}
\]

Dette er et rent nullromsproblem.

### 5.1 Lukket topologisk sektor

Regelsett:

- `seed`
- `swap`

Nullrommet i kjernebasis er spent opp av:

- `tokens`
- `components`
- `beta1`

Hvis vi i tillegg arbeider i én fast sammenhengende komponent (\(components=1\)), gjenstår de ikke-trivielle invariantene:

- `tokens`
- `beta1`

Dette formaliserer nøyaktig den tidligere, mer intuitive påstanden om at et lukket topologisk regime kan bevare både action-budsjett og syklusrang.

### 5.2 Åpen topologisk sektor

Regelsett:

- `seed`
- `triad`
- `delete`
- `swap`

Nullrommet i kjernebasis er spent opp av:

- `tokens`
- `components`

I én fast sammenhengende komponent gjenstår dermed bare:

- `tokens`

Dette er en viktig og streng konklusjon:
så snart du tillater fri intern syklusdannelse og ikke-bro-sletting, slutter \(\beta_1\) å være eksakt invariant.

### 5.3 Fullt åpen lineær sektor

Regelsett:

- `seed`
- `triad`
- `delete`
- `swap`
- `birth`
- `death`

Nullrommet i kjernebasis er da bare:

- `components`

I én fast sammenhengende komponent finnes dermed **ingen ikke-trivielle lineære invariants i kjernebasis**.

Dette setter en presis grense for hvor mye “energibevaring” man kan forvente uten videre struktur:
den må enten ligge
- i et mer restriktivt regelregime,
- i et ikke-lineært uttrykk,
- eller som emergent quasi-invarians, ikke som eksakt lineær invariant.

---

## 6. Kontekstbetingede eksakte formler i motivsektoren

Den store forbedringen i v0.4 er at flere motivendringer kan skrives eksakt i lokal kontekst.

### 6.1 Seed

Hvis en ny bladnode festes til en vert med grad \(h\), så gjelder:

\[
\Delta \text{wedges} = h,
\qquad
\Delta \text{triangles} = 0,
\qquad
\Delta \text{star3} = \binom{h}{2}.
\]

### 6.2 Triad

Hvis en ny kant legges inn mellom noder med grader \(d_v, d_w\), og de før regelen har \(c\) felles naboer, så gjelder:

\[
\Delta \text{wedges} = d_v + d_w,
\qquad
\Delta \text{triangles} = c,
\qquad
\Delta \text{star3} = \binom{d_v}{2} + \binom{d_w}{2}.
\]

### 6.3 Delete

Hvis en ikke-bro-kant mellom noder med grader \(d_v, d_u\) fjernes, og kanten før sletting deltar i \(c\) trekanter, så gjelder:

\[
\Delta \text{wedges} = -[(d_v-1)+(d_u-1)],
\]
\[
\Delta \text{triangles} = -c,
\]
\[
\Delta \text{star3} = -\left[\binom{d_v-1}{2} + \binom{d_u-1}{2}\right].
\]

### 6.4 Swap

Ved `swap`, der kanten \((v,u)\) fjernes og \((v,w)\) legges inn, med lokale størrelser:

- \(d_u\): grad til noden som mister kanten,
- \(d_w\): grad til noden som får ny kant,
- \(c_{\text{del}}\): antall felles naboer for \((v,u)\) før sletting,
- \(c_{\text{add}}\): antall felles naboer for \((v,w)\) før sletting,

gjelder i implementasjonen:

\[
\Delta \text{wedges} = -(d_u - 1) + d_w,
\]
\[
\Delta \text{triangles} = -c_{\text{del}} + (c_{\text{add}} - 1),
\]
\[
\Delta \text{star3} = -\binom{d_u-1}{2} + \binom{d_w}{2}.
\]

Termen \((c_{\text{add}}-1)\) er viktig: den korrigerer for at noden \(u\), som var felles nabo før sletting, ikke lenger er felles nabo etter at kanten \((v,u)\) er fjernet.

---

## 7. Empirisk validering av de lokale formlene

I v0.4-simulatoren ble disse formlene testet eksplisitt ved å logge:

- lokal kontekst før hendelsen,
- faktisk \(\Delta F\),
- og predikert \(\Delta F\).

I representative kjøringer i både lukket og åpen topologisk sektor er residualene for:

- `wedges`
- `triangles`
- `star3`

lik null opp til flyttallsavrunding.

Det betyr at vi nå har et klart skille:

### Eksakt kombinatorisk kontroll
- `wedges`
- `triangles`
- `star3`

### Fortsatt empiriske / regimeavhengige makrovariabler
- `c4`
- `spectral_radius`
- `clustering`
- `dim_proxy`

Dette er et metodologisk fremskritt: deler av “felt-sektoren” er nå matematisk internalisert i reglene, ikke bare i observasjonene.

---

## 8. Standardiserte ΔF-matriser og empirisk tolkning

Ved å standardisere hver featurekolonne med sitt globale standardavvik i hendelsesmatrisen, får vi en skala der regler kan sammenliknes på tvers av enheter.

I den representative åpne topologiske kjøringen gir dette følgende mønster:

- `triad` dominerer positivt på
  - `beta1`
  - `wedges`
  - `triangles`
  - `star3`
  - `c4`
  - `spectral_radius`
- `delete` dominerer negativt på de samme størrelsene
- `seed` dominerer sterkt på `nodes`, og i mindre grad på `wedges` og `star3`
- `swap` er lineært nøytral i kjernebasis, men påvirker fortsatt lokale motiv- og spektrale størrelser

Dette er et viktig resultat:
`swap` er ikke fysisk “ingenting”; det er lineært usynlig i kjernebasis, men kan ha betydelig effekt i den ikke-lineære formsektoren.

Det er nettopp derfor prosjektet trenger både:
- en kjernebasis for eksakte invariants,
- og en utvidet basis for form- og geometriutvikling.

---

## 9. Hva dette betyr for energispørsmålet

Dette steget skjerper energidiskusjonen betydelig.

### 9.1 I lukket topologisk sektor
I en fast sammenhengende komponent er både:

- `tokens`
- `beta1`

eksakt bevarte.

Det gjør dem til reelle kandidater for primitive “energiformer” eller charges.

### 9.2 I åpen topologisk sektor
Så snart `triad` og `delete` tillates fritt, er bare `tokens` eksakt invariant i kjernebasis.

Det betyr at en energidefinisjon som involverer syklusrang \(\beta_1\) ikke lenger kan være eksakt konservert uten ekstra struktur.

### 9.3 Konsekvens
Den mest modne formuleringen så langt er derfor:

- `tokens` er en kandidat for et **konservert action-budsjett** i token-lukkede regimer,
- \(\beta_1\) er en kandidat for en **topologisk charge** bare i regelregimer som ikke tillater fri syklusskaping/-ødeleggelse,
- mer realistiske energibegreper må sannsynligvis være
  - ikke-lineære,
  - regimeavhengige,
  - eller emergente quasi-invarianter i spacetime-regimet.

Dette er langt mer presist enn å si at energi “bare er units of action”.

---

## 10. Hvor dette plasserer prosjektet nå

Etter v0.4 har prosjektet fire sikre metodologiske nivåer:

### Nivå 1: Ontologi
- noder
- én relasjonstype
- lokal omskriving
- stokastisk hendelsesstruktur

### Nivå 2: Kjernekonservering
- eksakt nullromsanalyse i redusert lineær basis

### Nivå 3: Lokal motivdynamikk
- eksakte kontekstformler for flere viktige motivfeatures

### Nivå 4: Makroregimeanalyse
- spektrale, klustrings- og dimensjons-proxyer som fortsatt må studeres empirisk

Dette betyr at vi nå har en mye klarere plattform for neste fase.

---

## 11. Neste riktige steg

Det neste riktige steget etter v0.4 er, etter min vurdering, ikke enda flere invariants, men **kausal og geometrisk responsanalyse**.

Det innebærer å bygge en perturbasjonslab der man:

1. kjører to kopla simuleringer med identisk stokastisk strøm,
2. innfører én lokal forskjell,
3. måler hvordan forskjellen sprer seg i grafdistanse og feature-rom,
4. estimerer en effektiv propagasjonsfront / causal cone.

Grunnen til at dette er neste riktige steg, er at vi nå allerede har:

- en ren basis,
- en eksakt invariantklassifikasjon,
- og kontroll over flere lokale motivendringer.

Det som mangler for å koble modellen tilbake til relativitet og emergent spacetime, er en presis studie av **hvordan lokal forskjell sprer seg**.

---

## 12. Konklusjon

v0.4 er et avgjørende modningssteg i prosjektet.

Det viktigste resultatet er ikke bare at noen quantities ser stabile ut, men at vi nå kan skille presist mellom:

- hva som er en grafidentitet,
- hva som er en eksakt invariant av en regelklasse,
- hva som er en lokal kombinatorisk konsekvens av en regel,
- og hva som fortsatt bare er en empirisk regimevariabel.

Den viktigste fysiske konsekvensen er denne:

> En “energi” som skal spille rollen til en fundamental bevaringslov i modellen kan ikke bare postuleres; den må identifiseres enten som en eksakt invariant av en bestemt regelklasse, eller som en robust emergent quasi-invariant i et veldefinert makroregime.

Det er akkurat slik fysikken bør tvinges fram i et prosjekt som dette: ikke ved metafor alene, men ved gradvis strengere matematisk disiplin.

---

## Vedlegg: relevante filer i dette steget

- `relational_universe_rule_delta_lab.py`
- `rule_delta_closed_summary.md`
- `rule_delta_open_summary.md`

Disse filene dokumenterer henholdsvis:

- selve den instrumenterte simulatoren,
- en representativ lukket topologisk kjøring,
- og en representativ åpen topologisk kjøring.

---

## Begrepsliste

### \(\beta_1\) / første Betti-tall
Antall uavhengige sykluser i grafen. For en graf er
\[
\beta_1 = E - N + C.
\]

### Kjernebasis
Den minste lineære feature-basis som brukes til eksakt invariantanalyse:
\[
(tokens, nodes, components, beta1).
\]

### Nullrom
Mengden av koeffisientvektorer \(c\) slik at \(A c = 0\). Her representerer nullrommet alle lineære kombinasjoner av features som er eksakt invariant under en gitt regelklasse.

### Wedge
Et par kanter som deler en felles node; tilsvarer en lengde-2-sti sentrert i én node.

### 3-star / `star3`
Et motiv med én sentral node koblet til tre naboer.

### `c4`
Antall enkle 4-sykluser i grafen.

### Spektralradius
Største egenverdi til grafens adjakensmatrise. Brukes her som en global strukturell proxy.

### Standardisert \(\Delta F\)-matrise
En hendelsesmatrise der hver featurekolonne er skalert med sitt globale standardavvik, slik at reglers relative effekt kan sammenliknes på tvers av features med ulike naturlige størrelsesskalaer.

### Topologisk sektor
Et regelregime der det primært er grafens syklusstruktur og relasjonelle omkobling som endres, uten at token-populasjonen nødvendigvis endres.

### Quasi-invariant
En størrelse som ikke er eksakt konservert, men som viser liten drift eller høy robusthet i et bestemt metastabilt regime.
