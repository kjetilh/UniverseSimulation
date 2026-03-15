# Relasjonell universgraf v0.6  
## Uniformisert kobling for åpne regimer, state-dependent birth/death og metodisk kontroll av kausal analyse

### Formål
Dette dokumentet beskriver neste operative steg etter v0.5.  
Målet er å utvide perturbasjons- og kausalitetsanalysen til **åpne regimer** der antallet action-bærere
(tokens) kan vokse eller krympe, uten at vi mister en felles stokastisk referanse mellom to nesten like universgrener.

Det sentrale problemet er dette:

> I v0.5 kunne vi bruke en eksakt delt Gillespie-klokke så lenge de to grenene hadde samme og fast totalrate.  
> Så snart birth/death gjør totalratene ulike, risikerer vi å blande sammen ekte kausal spredning med ren klokke-deskronisering.

v0.6 løser dette ved å innføre en **adaptive familywise uniformized coupling**:
en delt strøm av potensial-hendelser med state-dependent thinning i hver gren.

---

## 1. Hvor prosjektet står etter v0.5

Ved slutten av v0.5 hadde vi etablert:

### Ontologisk kjerne
- Universet modelleres som en dynamisk graf.
- Det finnes bare **én relasjonstype**.
- Endring skjer gjennom lokale **units of action**.
- Tid forstås operasjonelt som sekvenser av slike hendelser.
- Spacetime behandles ikke som grunnleggende, men som et mulig emergent makroregime.

### Matematisk kjerne
- Vi har en redusert feature-basis for invariants og quasi-invariants.
- Vi har en kausalitetslab med kopla replikater og delt stokastisk instruksjonsstrøm.
- Vi har en strengt lokal regelklasse som unngår tidligere globale bro-tester.

### Hva som fortsatt manglet
v0.5 var ren og sterk i lukkede regimer, men utilstrekkelig i åpne regimer:
så snart birth/death eller annen state-dependent rateendring gjør at to grener får ulik totalrate,
er en delt standard-SSA ikke lenger metodisk nøytral.

---

## 2. Hvorfor v0.6 var nødvendig

Hvis to grener utvikles under forskjellige totalrater, kan de se forskjellige ut av to helt ulike grunner:

1. **ekte lokal dynamisk divergens**, eller  
2. **forskjellig klokkehastighet**.

Hvis vi vil si noe seriøst om emergent causal cone, relativitetslignende begrenset spredning eller
lokalitet i åpne regimer, må disse to effektene skilles metodisk.

Dermed trengte prosjektet en koblingsmekanisme som:

- fortsatt bruker **felles potensial-hendelser**,
- men tillater at hver gren aksepterer eller forkaster hendelser avhengig av egen tilstand,
- og gjør dette på en måte som bevarer riktige marginale family-rater.

Det er nettopp dette uniformisert coupling gjør.

---

## 3. v0.6-konstruksjonen

### 3.1 Event-familier
Vi deler mikrodynamikken i fire familier:

- `seed`
- `token`
- `birth`
- `death`

For hver gren \(X \in \{A,B\}\) defineres family-rater

\[
\lambda_f^X
\]

for hver familie \(f\).

I koden er disse ratene **state-dependent**. Særlig:

- `token`: proporsjonal med token-antallet \(K\)
- `birth`: proporsjonal med en lokal mulighetsmasse basert på grad ved token-noder
- `death`: proporsjonal med en lokal sårbarhetsmasse, her kodet gjennom en invers-grad-vekt

Dette er viktig: hvis ratene bare var funksjoner av \(K\), og \(K\) forble lik i begge grener,
ville åpne regimer igjen kollapset tilbake til en degenerert “begge gjør det samme”-situasjon.

### 3.2 Dominerende family-rater
For to grener \(A\) og \(B\) definerer vi

\[
\mu_f = \max(\lambda_f^A, \lambda_f^B).
\]

Deretter definerer vi en total dominerende rate

\[
M = \sum_f \mu_f.
\]

Vi genererer potensial-hendelser fra

\[
\Delta t \sim \mathrm{Exp}(M).
\]

Ved hver slik potensial-hendelse velges først familie \(f\) med sannsynlighet

\[
\mu_f / M.
\]

### 3.3 Thinning i hver gren
Når familien er valgt, bruker vi en felles uniform \(U\) og sier at gren \(X\) aksepterer familie \(f\) hvis

\[
U < \lambda_f^X / \mu_f.
\]

Dermed blir:
- begge aksepterer når \(U\) er under begge terskler,
- bare én gren aksepterer når \(U\) ligger i restintervallet,
- ingen aksepterer ikke kan skje i vår familywise-konstruksjon når \(\mu_f\) er definert som maksimum, fordi minst én gren har terskel 1 for den aktuelle familie-komponenten hvis den ene er den dominerende; men den andre kan forkaste.

Det viktige er marginalt:

\[
M \cdot \frac{\mu_f}{M} \cdot \frac{\lambda_f^X}{\mu_f} = \lambda_f^X.
\]

Altså får hver gren riktig family-rate.

### 3.4 Lokal kobling innen familien
Når en familie er akseptert, brukes felles tilfeldige tall også til lokale valg:
- token-ID via rang eller vektet rang
- nabovalg
- lokal rewrite-roll
- kandidatvalg for triad/swap
- node- eller token-allokering ved seed/birth

Dette er ikke en full maksimal kobling av hele overgangskjernen.
Men det er en **eksakt familywise-riktig** og praktisk robust kobling.

---

## 4. Hva som faktisk ble endret i simulatoren

Ny kodefil:

- `relational_universe_uniformized_coupling_lab.py`

Viktige nye elementer:
- persistent node-ID og token-ID på tvers av grener
- familywise dominerende klokke
- state-dependent `birth`- og `death`-vekter
- eksplisitt logging av:
  - `both_accept`
  - `one_sided`
  - `null`
  - feature-drift
  - radius av skadefront

Ekstra batch-kode:
- `relational_universe_uniformized_scan.py`

Denne brukes til parametergrid, flerkjøringsstatistikk og grov fasekartlegging.

---

## 5. Representative kjøringer

### 5.1 Token-open, topologisk moderat regime
Parametre:
- `p_triad = 0`
- `p_del = 0`
- `p_swap = 0.08`
- `r_birth = 0.01`
- `r_death = 0.009`

Representativ kjøring (`seed=7`, 10 000 steg):

- final radius (control): 4
- max radius (control): 5
- final edge difference: 28
- final \(\Delta tokens\): 33.0
- both_accept_total: 8935
- one_sided_total: 1065
- fit-speed (control): 0.00198611

Tolking:
- koblingen holder seg sterk (`both_accept` dominerer),
- men åpne effekter er reelle (`one_sided_total` er tydelig ikke-null),
- og skadefronten forblir målbar utover startområdet.

### 5.2 Fullt åpent moderat regime
Parametre:
- `p_triad = 0.05`
- `p_del = 0.03`
- `p_swap = 0.08`
- `r_birth = 0.01`
- `r_death = 0.009`

Representativ kjøring (`seed=9`, 10 000 steg):

- final radius (control): 2
- max radius (control): 3
- final edge difference: 45
- final \(\Delta tokens\): 119.0
- final \(\Delta \beta_1\): -1.0
- both_accept_total: 7852
- one_sided_total: 2148
- fit-speed (control): -0.0102182

Tolking:
- regimet er mye mer åpent,
- ensidige hendelser er langt vanligere,
- feature-rommet divergerer raskere enn den observerte geometriske fronten.

Dette peker mot at svært åpne regimer ikke nødvendigvis gir en pen, ren causal cone.
De kan i stedet gi sterk lokal scrambling og feature-drift.

---

## 6. Multikjøringsresultater

Vi kjørte 20 seeds for hvert av to moderate regimer (`steps = 5000`).

### 6.1 Token-open moderat
- antall kjøringer: 20
- mean final radius: 3.650
- sd final radius: 1.182
- mean max radius: 5.200
- median max radius: 5.000
- mean \(\Delta tokens\): -1.050
- median \(\Delta tokens\): 0.000
- mean fit-speed: 0.006345
- mean both-accept fraction: 0.873
- mean one-sided fraction: 0.127
- corr(one-sided frac, max radius): 0.455

### 6.2 Fullt åpent moderat
- antall kjøringer: 20
- mean final radius: 0.550
- sd final radius: 1.146
- mean max radius: 3.150
- median max radius: 3.000
- mean \(\Delta tokens\): 14.800
- median \(\Delta tokens\): -2.000
- mean fit-speed: 0.006497
- mean both-accept fraction: 0.585
- mean one-sided fraction: 0.415
- corr(one-sided frac, max radius): 0.173

### 6.3 Hva dette antyder
Det mest interessante mønsteret er ikke at “mer åpenhet alltid gir større radius”.
Tvert imot:

- i **token-open** regimer får vi fortsatt høy both-accept-fraksjon og samtidig tydelig radiusutbredelse,
- i **fullt åpne** regimer stiger one-sided-fraksjonen kraftig, men radiusen blir ikke nødvendigvis større; mye av divergensen ser i stedet ut til å gå inn i token- og feature-drift.

Dette er viktig for teorien:
et universregime som skal ligne spacetime må kanskje være **åpent nok til å være dynamisk**, men **ikke så åpent at all forskjell går over i ren scrambling**.

---

## 7. Hva v0.6 faktisk etablerer

v0.6 etablerer ikke en ferdig relativitetsteori.

Det etablerer noe mer beskjedent, men viktig:

1. Åpne regimer kan nå undersøkes uten å miste en felles stokastisk referanse.
2. “Causal cone” i slike regimer kan nå diskuteres på en metodisk renere måte.
3. Vi kan skille mellom:
   - spredning av geometrisk skade,
   - spredning av token-antallsforskjell,
   - og ren feature-drift.
4. Vi har nå et tydelig tegn på at **mellomåpne regimer** er mer lovende enn sterkt åpne regimer dersom målet er emergent spacetime-lignende struktur.

---

## 8. Hva dette innebærer for den større teorien

I prosjektets egen logikk betyr dette følgende:

### 8.1 For relativitetssporet
Hvis en universell eller nesten universell maksimal front-hastighet skal oppstå, må den studeres i regimer der:
- lokalitet er streng,
- åpenhet er kontrollert,
- og felles stokastisk kobling fortsatt er sterk nok til at geometri ikke drukner i ren rate-divergens.

v0.6 identifiserer slike regimer som kandidater.

### 8.2 For energisporet
Energi som “ren aktivitetsrate” er fortsatt for grovt.
Men v0.6 viser at antall action-bærere (tokens) og strukturavhengige event-masser kan separeres metodisk.
Det åpner for en mer moden diskusjon om:
- conserved charges,
- quasi-invariants,
- og effective energy density i spacetime-regimer.

### 8.3 For dimensjonssporet
Vi er ennå ikke ved en seriøs dimensjonsteori.
Men v0.6 gjør det mulig å teste om regimer med stabil eller moderat skadefront også er regimer med mer robust volumvekst og dimensjonsproxy.
Det er en konkret vei videre.

---

## 9. Det neste riktige steget

Det neste riktige steget er nå **v0.7: lokal maksimal kobling innen familier og eksplisitt parameterfasekart**.

Mer presist:

1. Bygg en mer finmasket maksimal kobling for de lokale overgangskjernene, ikke bare familywise aksept.
2. Kjør systematiske grids i:
   - `r_birth`
   - `r_death`
   - `p_triad`
   - `p_del`
   - `p_swap`
   - vekter for birth/death
3. Kartlegg hvilke regimer som samtidig gir:
   - høy both-accept-fraksjon
   - moderat one-sided-fraksjon
   - stabil ikke-triviell radiusutbredelse
   - lav runaway i \(\Delta tokens\) og \(\Delta \beta_1\)

Det er i dette parameterrommet en fremtidig spacetime-hypotese må leve eller dø.

---

## 10. Kort dom

Den viktigste konseptuelle gevinsten i v0.6 er denne:

> Vi kan nå undersøke åpne universregimer uten å forveksle fysisk divergens med ren klokke-deskronisering.

Den viktigste empiriske gevinsten er denne:

> Middels åpne regimer ser mer lovende ut enn sterkt åpne regimer hvis man ønsker emergent, geometrisk lesbar kausal struktur.

Det er ikke et bevis for spacetime.
Men det er et klart fremskritt i retning av en teori som kan testes, forbedres og eventuelt falsifiseres.

---

## Ord- og begrepsliste

- **SSA**: *Stochastic Simulation Algorithm*, ofte brukt om Gillespie-type stokastisk hendelsessimulering i kontinuerlig tid.
- **CTMC**: *Continuous-Time Markov Chain*, Markov-prosess i kontinuerlig tid.
- **Uniformization / randomization**: teknikk der en CTMC representeres via en dominerende Poisson-klokke og thinning.
- **Familywise coupling**: kobling der man først velger en hendelsesfamilie og så kobler aksept/rejeksjon mellom prosesser.
- **Thinning**: prosedyre der potensial-hendelser forkastes med en bestemt sannsynlighet slik at riktig målprosess gjenstår.
- **Both-accept fraction**: andel potensial-hendelser der begge grener utfører hendelsen.
- **One-sided fraction**: andel potensial-hendelser der bare én gren utfører hendelsen.
- **Damage set / skademengde**: de noder, kanter og token-posisjoner som skiller de to grenene.
- **Radius**: maksimal grafavstand fra perturbasjonens støtte til skademengden.
- **Feature drift**: endring i makroskopiske mål som triangler, spektralradius, clustering eller dimensjonsproxy.
- **Scrambling**: her brukt om sterk lokal/mesoskopisk differensiering uten en pen, voksende geometrisk front.
- **Persistent ID**: node- eller token-identitet som bevares på tvers av grenene når hendelser deles.
