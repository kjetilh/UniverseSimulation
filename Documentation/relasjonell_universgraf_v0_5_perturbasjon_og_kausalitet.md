# Relasjonell universgraf v0.5  
## Perturbasjonslab, causal cone og metodisk opprydding i lokalitet

### Formål
Dette dokumentet beskriver neste operative steg i prosjektet: å undersøke om modellen ikke bare har
bevaringslover og metastabile regimer, men også en **operasjonell kausal struktur**.  
Det sentrale spørsmålet er nå:

> Hvis vi gjør én liten lokal endring i én gren av universgrafen, hvor raskt og på hvilken måte kan den forskjellen spre seg?

Dette er broen mellom:
- tidligere arbeid om invariants og quasi-invariants,
- diskusjonen om emergent relativitet,
- og spørsmålet om spacetime kan være et robust, kausalt makroregime.

---

## 1. Hvor prosjektet står etter v0.4

Ved slutten av v0.4 var følgende etablert:

### Ontologisk kjerne
- Universet modelleres som en dynamisk graf.
- Det finnes bare **én relasjonstype**.
- Endring skjer gjennom lokale **units of action**.
- Tid forstås operasjonelt som sekvenser av slike hendelser.
- Spacetime behandles ikke som grunnleggende, men som et mulig emergent makroregime.

### Streng matematisk fremgang
Vi hadde allerede isolert:
- en redusert feature-basis,
- regelbetingede \(\Delta F\)-matriser,
- og nullromsklassifikasjon av eksakte lineære invariants.

Særlig i den lukkede topologiske sektoren viste analysen at de ikke-trivielle kjernehinvariantene, i én sammenhengende komponent, i praksis er:
- `tokens`
- \(\beta_1\) (første Betti-tall / syklusrang)

Dette ga oss en presis versjon av utsagnet om at “energi-lignende” eller “charge-lignende” størrelser kan oppstå som invariants i bestemte regelklasser.

---

## 2. Hvorfor et nytt steg var nødvendig

Det neste naturlige spørsmålet var ikke lenger:
- *Hva er bevart?*

men:
- *Hvordan sprer forskjeller seg?*

Dersom modellen skal ha noen dyp forbindelse til relativistisk kinematikk, må vi ikke bare vise at den har maksimalt “stabile charges”; vi må også vise at den har noe som ligner en **causal cone**.

Det krevde imidlertid en metodisk opprydding.

---

## 3. Den viktige oppdagelsen: tidligere `avoid_disconnect` var ikke strengt lokal

I tidligere laboratorier ble et globalt bro-kriterium brukt for å hindre frakobling av grafen:
en kant ble bare slettet dersom den ikke var en bro.

Det er matematisk praktisk, men det er **ikke en strengt lokal regel**, fordi spørsmålet “er denne kanten en bro?” i alminnelighet krever global informasjon om grafen.

Dette er ikke en liten teknisk detalj. Det betyr:

1. Den eldre regelklassen var god nok til invariantanalyse.
2. Den var **ikke** god nok som ren test av emergent kausalitet.
3. Enhver påstand om “lysaktig maksimal hastighet” ville vært metodisk svak dersom den bygde på dette globale kriteriet.

Dermed var neste riktige steg å bygge en **perturbasjonslab i en strengt lokal regelklasse**.

---

## 4. v0.5: perturbasjonslab med kopla replikater

### 4.1 Hovedidé
Vi lager to nesten identiske replikater:
- en kontrollgren \(S_n\)
- en perturbert gren \(\tilde{S}_n\)

Begge starter fra samme initialtilstand, bortsett fra at den perturberte grenen får **én lokal omskriving** ved start.

Deretter utvikles begge under **samme stokastiske instruksjonsstrøm**:
- samme hendelsestider,
- samme valg av token-indeks,
- samme rule-roll,
- samme kandidat-ranger.

Dette er en klassisk “shared noise” / “common random numbers”-idé, men her brukt på relasjonell grafdynamikk.

### 4.2 Hvorfor koblingen er eksakt i dette laboratoriet
I v0.5 holdes token-antallet fast og vi bruker ingen birth/death-kanaler.

Da er totalraten:
\[
R = r_{seed} + K r_{token}
\]
den samme i begge grenene så lenge \(K\) er den samme.

Det betyr at Gillespie-tiden kan deles **eksakt** mellom grenene i denne sektoren.
Dette er metodisk viktig: vi sammenlikner ikke to ulike klokker, men to universgrener som virkelig drives av samme støyfelt.

### 4.3 Den strengt lokale regelklassen
Den nye simulatoren bruker som standard:
- seed attachment,
- token traversal,
- lokal delete,
- lokal triad closure,
- lokal swap.

I tillegg brukes bare **lokal** opprydding:
- hvis en sletting lokalt isolerer den forlatte enden, kan noden prunes,
- eventuelle tokens på den døde noden relokaliseres lokalt til nabonoden.

Dette er vesentlig renere enn global bridge-testing.

---

## 5. Den sentrale definisjonen: damage set og radius

La
\[
D_n
\]
være forskjellsmengden mellom de to grenene ved eventindeks \(n\), definert ved:
- symmetrisk differanse i kantmengde,
- nodeforskjeller,
- og token-indekser som står på ulike noder i de to grenene.

Fra perturbasjonens støtte \(P_0\) måler vi så en radius:
\[
R_n = \max_{v \in D_n} d(v, P_0)
\]
der avstanden måles i kontrollgrenens aktuelle graf.

Denne radiusen er ikke “fundamental fysikk” i seg selv.
Den er et **operasjonelt mål** på hvor langt forskjellen har kommet i den emergente geometrien til referansegrenen.

---

## 6. En lokalitetsproposisjon (arbeidshypotese, men med sterk støtte fra implementasjonen)

I den strengt lokale v0.5-regelklassen gjelder intuitivt følgende:

> Hvis to grener er identiske i den lokale disken som en delt instruksjon faktisk leser og skriver til,
> så vil oppdateringen også være identisk i denne disken.
> Nye forskjeller kan derfor bare oppstå når instruksjonen treffer en allerede skadet disk eller en disk i dens umiddelbare nærhet.

Dette er ikke ennå formulert som et fullstendig teorem med alle randtilfeller, men det er den riktige matematiske strukturen:
skade kan ikke oppstå “ut av ingenting” langt unna dersom reglene virkelig er lokale.

Dermed får modellen en **diskret causal-cone-egenskap**:
skadens støtte kan bare utvide seg med et begrenset antall grafhopp per hendelse.

---

## 7. To typer perturbasjoner

Simulatoren støtter allerede to viktige perturbasjonstyper.

### 7.1 `local_swap`
En lokal edge-swap som **bevarer kjernekvantiteter**:
- tokens
- nodes
- components
- \(\beta_1\)

Dette er den beste testen for ren kausal spredning, fordi vi da ikke bare endrer invariant-sektor.

### 7.2 `add_chord`
En lokal akkordtilføyelse som typisk gir:
- \(\Delta \beta_1 = +1\)

Dette er en “charge-injiserende” perturbasjon og er nyttig for å se hvordan en forskjell som ligger i en eksakt invariant sprer seg geometrisk.

---

## 8. Representative resultater

### 8.1 Lukket topologisk regime (`seed + swap`)
Representativ kjøring (`local_swap`, 20 000 steg):

- final radius (control): 13
- max radius (control): 18
- final edge difference: 378
- final core L1: 0.0
- final \(\Delta \beta_1\): 0.0
- lineær fit-hastighet for fronten: 0.002258

Tolking:
- Kjerneinvariantene forblir identiske mellom grenene.
- Forskjellen sprer seg likevel utover i grafen.
- Dette er akkurat det man håper på dersom spacetime-lignende kausalitet skal være et emergent fenomen:
  lokal forskjell, bevart invariant-sektor, men voksende skadesone.

### 8.2 Åpent topologisk regime (`seed + triad + delete + swap`)
Representativ kjøring (`local_swap`, 20 000 steg):

- final radius (control): 3
- max radius (control): 4
- final edge difference: 1382
- final core L1: 92.0
- final \(\Delta \beta_1\): -84.0
- lineær fit-hastighet for fronten: 0.000169

Tolking:
- Her sprer ikke forskjellen seg først og fremst som en ren, voksende front.
- I stedet får vi mye sterkere **lokal topologisk scrambling**:
  mange flere kantforskjeller og stor drift i \(\beta_1\), men relativt liten radius.
- Dette antyder at åpne regimer kan være mer dissipative / kaotiske lokalt, uten nødvendigvis å gi en “ren” ballistisk causal cone.

Dette er et viktig resultat, fordi det viser at “stor forskjell” og “stor geometrisk rekkevidde” ikke er det samme.

### 8.3 Charge-injiserende kontrolltest (`add_chord`)
I lukket regime, representativt:

- final \(\Delta \beta_1 = 1.0\)
- final radius (control): 11
- fit speed (control): 0.005159

Dette viser at perturbasjonslaben også kan brukes til å sammenlikne:
- kausal spredning innen samme invariant-sektor,
- og kausal spredning når invariant-sektoren selv er forskjellig.

---

## 9. Multikjøringsstatistikk

For å unngå å overtolke én enkelt bane ble det kjørt 6 representative kjøringer per regime
(8 000 steg, `local_swap`).

### Lukket regime
- mean final radius (control): 9.666667
- std final radius (control): 1.861899
- mean max radius (control): 11.500000
- mean fit speed (control): 0.003549 ± 0.001146
- mean final \(\Delta \beta_1\): 0.000000
- mean final core L1: 0.000000

### Åpent regime
- mean final radius (control): 2.500000
- std final radius (control): 0.836660
- mean max radius (control): 3.666667
- mean fit speed (control): 0.000298 ± 0.000436
- mean final \(\Delta \beta_1\): -41.333333
- mean final core L1: 88.500000

### Viktig tolkning
Dette peker mot et klart skille mellom to typer dynamiske sektorer:

1. **Lukkede topologiske sektorer**  
   Forskjeller tenderer til å spre seg romlig mens kjernekvantiteter holdes fast.

2. **Åpne topologiske sektorer**  
   Forskjeller kan bli store i feature-rommet uten å spre seg like langt som romlig front.

Det er teoretisk interessant, fordi det antyder at en ren causal cone mest sannsynlig bør studeres i nær-konservative sektorer,
mens mer åpne sektorer kanskje heller beskriver dissipasjons- eller målelignende regimer.

---

## 10. Hva vi nå faktisk vet

Etter v0.5 kan vi si følgende med større presisjon enn før:

### Etablert
- Prosjektet har nå en eksplisitt metode for **kopla perturbasjonseksperimenter**.
- Lokalitet er renset metodisk ved å flytte causal-cone-analysen til en strengt lokal regelklasse.
- Det finnes representative og multikjøringsmessige tegn på **begrenset spredning av forskjeller**.

### Ikke etablert ennå
- Vi har ikke vist et fullstendig teorem av Lieb–Robinson-type for denne modellen.
- Vi har ikke vist at den målte front-hastigheten er universell eller invariant over regimer.
- Vi har ikke ennå koblet denne hastigheten til en full emergent metrikksstruktur.

### Men dette er nå sannsynlig
- Relativitet-lignende kinematikk bør søkes i den delen av modellen der
  lokalitet er streng,
  invariant-sektoren er kontrollert,
  og skadefronten sprer seg omtrent lineært og begrenset.

---

## 11. Filosofisk betydning

Dette er et viktig modningstrinn i hele prosjektet.

Tidligere var utsagnet
“kanskje spacetime er et error-correcting felt”
fortsatt i stor grad metafysisk.

Nå har vi en konkret, operasjonell test:

- Gi systemet en liten lokal forskjell.
- La alt annet være det samme.
- Se om forskjellen sprer seg med begrenset hastighet.

Hvis svaret fortsetter å være ja, og hvis hastigheten stabiliserer seg på tvers av observatørtyper og regimer, begynner spacetime å ligne mindre på en metafor og mer på et faktisk emergent kausalmedium.

---

## 12. Neste riktige steg

Det neste riktige steget er nå todelt.

### A. Utvide koblingen til åpne token-regimer
Når birth/death skal inn, holder ikke denne enkle eksakte shared-SSA-koblingen lenger.
Da trenger vi:
- uniformisering,
- eller maksimal Poisson-kobling,
- eller en tilsvarende kontrollert koplingskonstruksjon.

### B. Gjøre causal cone til statistisk objekt
Vi trenger:
- mange kjøringer,
- konfidensintervaller,
- radius-som-funksjon-av-tid-plott,
- skaleringslover i parametrene,
- og sammenlikning mellom `local_swap` og `add_chord`.

---

## 13. Konklusjon

v0.5 er et av de viktigste trinnene så langt, fordi prosjektet nå har gått fra:

- ontologi,
- til invariants,
- til **operasjonell kausal analyse**.

Det mest verdifulle funnet er ikke bare at skade kan spre seg.  
Det mest verdifulle funnet er at vi nå vet **hvordan vi må formulere lokalitet riktig** for at spørsmålet om emergent relativitet skal være velstilt.

Med andre ord:

> Prosjektet har nå en matematisk og simulativ plattform der spørsmålet
> “oppstår en relativistisk causal cone?”  
> kan undersøkes presist, i stedet for bare å diskuteres intuitivt.

---

## Begrepsliste / forklaringer

### `beta1`
Første Betti-tall for grafen. Her betyr det antall uavhengige sykluser / loops.

### `core L1`
Summen av absolutte forskjeller i kjernebasis:
`tokens, nodes, components, beta1`.

### `regime L1`
Samlet forskjell i mer komplekse makrofeatures, som triangler, 4-sykluser, spektralradius, clustering og dimensjonsproxy.

### `shared noise`
At begge grener drives av samme tilfeldige instruksjonsstrøm.

### `causal cone`
Mengden punkter som kan påvirkes av en lokal forskjell etter et gitt antall hendelser eller gitt tid.

### `strictly local rule sector`
En regelklasse der oppdateringer bare bruker informasjon fra et begrenset lokalt nabolag, ikke globale tester.

### `scrambling`
At forskjeller blir komplekse og store i tilstandsrommet, uten nødvendigvis å spre seg langt som en ren romlig front.

---

## Referanser

1. D. T. Gillespie, *Exact stochastic simulation of coupled chemical reactions*, Journal of Physical Chemistry 81 (1977), 2340–2361.  
2. P. Arrighi og G. Dowek, *Causal graph dynamics*, Information and Computation 223 (2013), 78–93.  
3. P. Arrighi og S. Martiel, *Quantum causal graph dynamics*, Physical Review D 96 (2017), 024026.  
4. B. Martin, *Damage spreading and μ-sensitivity on cellular automata*, Ergodic Theory and Dynamical Systems 27 (2007), 545–565.  
5. E. H. Lieb og D. W. Robinson, *The finite group velocity of quantum spin systems*, Communications in Mathematical Physics 28 (1972), 251–257.
