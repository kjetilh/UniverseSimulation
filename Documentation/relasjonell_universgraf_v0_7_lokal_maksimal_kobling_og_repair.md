# Relasjonell universgraf v0.7 – lokal maksimal kobling, meeting og repair

## Sammendrag

Dette dokumentet beskriver v0.7-steg i prosjektet om en bakgrunnsløs, relasjonell universmodell der universet representeres som en dynamisk graf av noder og relasjoner, drevet av lokale `units of action`. 

Det nye i v0.7 er at vi ikke lenger bare kobler to nesten like universgrener på **familienivå** (seed, token, birth, death), men også på **lokalt overgangskjernenivå**. Når begge grener aksepterer samme hendelsesfamilie, bygger vi nå de endelige lokale overgangsfordelingene eksplisitt og kobler dem med **maksimal kobling**. Det betyr at sannsynligheten for identisk lokal hendelse blir så stor som de to distribusjonene tillater.

Dette er metodisk viktig av to grunner:

1. Det skiller rent mellom:
   - felles potensial-klokke (uniformisering),
   - familywise akseptkobling,
   - og konkret lokal hendelseskobling.
2. Det gjør det mulig å måle ikke bare **spredning av forskjell**, men også **repair**: om to grener tenderer mot å møtes igjen eller i det minste bevare mer felles struktur.

## 1. Hvor vi står i prosjektet

Prosjektet har nå passert flere faser:

1. **v0.1–v0.2:** minimale simulatorer for lokal grafdynamikk, seeds, units of action og primitive stabile mønstre.
2. **v0.2–v0.4:** energikandidater, invariantanalyse og redusert basis 

   \[
   F_{core}=(K, N, C, \beta_1)
   \]

   med regelbetingede \(\Delta F\)-matriser.
3. **v0.5:** perturbasjonslab for kausal spredning i lukkede eller nær-lukkede regimer.
4. **v0.6:** familywise uniformisering i åpne regimer med birth/death.
5. **v0.7:** lokal maksimal kobling av endelige overgangskjerner + meeting/survival-analyse.

Det betyr at prosjektet ikke lenger bare er en konseptuell eller filosofisk øvelse. Vi har nå et faktisk laboratorium for å teste:

- om små forskjeller sprer seg med begrenset radius,
- om noen regimer også viser repair,
- og om disse regimene overlapper med regimer som ser geometri-lignende ut.

## 2. Hva som var utilstrekkelig i v0.6

I v0.6 brukte vi:

- en delt dominerende potensial-klokke (uniformization),
- maksimal Bernoulli-kobling for aksept/rejekt per familie,
- og deretter en enkel rank- eller common-random-number-kobling for lokale valg.

Det var **marginalt korrekt**, men lokalt grovt. To grener kunne ha nesten identiske lokale overgangsfordelinger og likevel få unødig mange ulike konkrete hendelser.

Med andre ord: v0.6 kunne være metodisk riktig, men konservativ når det gjaldt å avdekke faktisk repair.

## 3. Hva v0.7 gjør matematisk

La \(X_t\) og \(Y_t\) være de to universgrenene.

### 3.1 Familywise uniformisering
For hver familie \(f\in\{seed, token, birth, death\}\) har grenene familie-rater
\[
\lambda_f^X, \qquad \lambda_f^Y.
\]
Vi bruker de dominerende ratene
\[
\mu_f = \max(\lambda_f^X, \lambda_f^Y),
\qquad
M = \sum_f \mu_f.
\]
Så trekkes en potensialhendelse fra \(\mathrm{Exp}(M)\), familie velges med sannsynlighet \(\mu_f/M\), og aksept i hver gren kobles med delt uniform variabel.

### 3.2 Lokale endelige kjerner
Gitt at begge grener aksepterer samme familie, konstruerer vi eksplisitt de lokale overgangsfordelingene
\[
P_f^X(\cdot \mid X_t), \qquad P_f^Y(\cdot \mid Y_t)
\]
over konkrete lokale hendelsesdeskriptorer, for eksempel:

- `("seed_tid", tid)`
- `("birth_tid", tid)`
- `("death_tid", tid)`
- `("move", tid, v, u)`
- `("triad", tid, v, u, w)`
- `("swap", tid, v, u, w)`

### 3.3 Maksimal kobling
For to endelige fordelinger \(p\) og \(q\) er maksimal felles treff-sannsynlighet
\[
\alpha(p,q) = \sum_i \min(p_i, q_i).
\]
Vi bruker nettopp denne størrelsen som operasjonell definisjon av **lokal overlap**. I v0.7 samplet vi fra overlap-delen med sannsynlighet \(\alpha\), og ellers fra residualene. Dermed får vi:

- korrekte marginals,
- maksimal sannsynlighet for identisk lokal hendelse,
- og absorpsjon etter meeting når tilstandene er identiske.

## 4. Hva som ble testet i v0.7

Vi valgte som hovedregime et moderat **birth/death-åpent**, men topologisk relativt enkelt regime:

- `r_seed = 0.04`
- `r_token = 1.0`
- `r_birth = 0.05`
- `r_death = 0.05`
- `p_swap = 0.08`
- `p_triad = 0.0`
- `p_del = 0.0`
- perturbasjon: `local_swap`

Dette er et godt testregime fordi:
- det er åpent nok til å utfordre koblingen,
- men ikke så åpent at alt drukner i ren topologisk drift.

Vi sammenlignet to lokale koblingsmodi:

1. `rank` (baseline)
2. `maximal` (v0.7)

begge over de samme 12 seedene.

## 5. Hovedresultater

### 5.1 Multirun-resultat i hovedregimet

| mål | rank | maximal |
| --- | ---: | ---: |
| meeting fraction | 0.000 | 0.000 |
| mean final radius (control) | 2.917 | 2.333 |
| mean total unequal time | 41.468 | 39.344 |
| mean local overlap | 0.050 | 0.082 |
| mean same-descriptor rate | 0.033 | 0.079 |
| mean shared token fraction final | 0.064 | 0.216 |
| mean shared node fraction final | 0.799 | 0.814 |

### 5.2 Tolkning av tallene

De viktigste v0.7-funnene er:

1. **Meeting ble ikke vanlig i dette regimet.**  
   Vi observerte ingen full meeting i de 12 representative kjøringene. Det er viktig å være ærlig om dette: v0.7 har **ikke** vist at repair er vanlig.

2. **Likevel forbedret maksimal lokal kobling den felles lokale strukturen klart.**  
   Lokal overlap økte fra omtrent **0.050** til **0.082**, og same-descriptor-raten økte fra **0.033** til **0.079**.

3. **Felles token-lineage ble langt bedre bevart.**  
   Delt token-fraksjon ved slutt økte fra **0.064** til **0.216**.

4. **Unequal time ble litt kortere, og skadefronten litt mindre.**  
   Det er et moderat, men konsistent tegn på at v0.7 ikke bare gjør koblingen penere på papiret; den gjør den også mer diagnostisk nyttig.

## 6. Representativ enkeltkjøring: seed 109

For seed 109 fikk vi en særlig tydelig kontrast mellom baseline og maksimal lokal kobling.

### Rank-baseline
- `avg_local_overlap_both_accept = 0.0335`
- `avg_same_descriptor_both_accept = 0.0179`
- `shared_token_fraction_final = 0.0272`

### Maksimal lokal kobling
- `avg_local_overlap_both_accept = 0.1268`
- `avg_same_descriptor_both_accept = 0.1302`
- `shared_token_fraction_final = 0.4126`

Det er en stor forskjell. Selv når de to grenene **ikke** møtes, bevarer maksimal lokal kobling langt mer felles identitet i hva slags lokale hendelser som faktisk skjer.

Dette er metodisk viktig fordi vi nå bedre kan skille mellom:
- **ekte dynamisk irreversibel divergens**, og
- **artefaktisk divergens som skyldtes en grov koblingsmetode**.

## 7. Faseprobe mot v0.8

Vi kjørte også en liten v0.7-faseprobe for å finne lovende kandidater før et fullere fasekart.

De mest lovende punktene for høy lokal overlap lå i området:

- `r_birth ≈ 0.05`
- `r_death ≈ 0.00–0.05`
- `p_swap ≈ 0.04`
- `p_triad ≈ 0.00–0.03`
- `p_del = 0.0`

Særlig to kandidater skilte seg ut:

| r_birth | r_death | p_swap | p_triad | meeting_frac | mean_overlap | mean_same_descriptor | unequal_time | shared_token_frac | final_radius |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.05 | 0.00 | 0.04 | 0.00 | 0.000 | 0.199 | 0.198 | 29.734 | 0.436 | 2.333 |
| 0.05 | 0.00 | 0.04 | 0.03 | 0.000 | 0.185 | 0.186 | 22.837 | 0.493 | 1.500 |

Det mest interessante her er ikke at meeting fortsatt er 0, men at vi ser **mye høyere lokal overlap** og **kortere unequal time** i et ganske smalt regime. Dette peker på en kandidatklasse av “repair-vennlige” og potensielt geometri-vennlige sektorer.

## 8. Fysisk og filosofisk betydning

Dette steget har tre implikasjoner.

### 8.1 For fysikken i modellen
Hvis lokal maksimal kobling gir mer vedvarende felles struktur, betyr det at modellen har en reell lokal konvergensmekanisme – ikke nødvendigvis sterk nok til full repair, men sterk nok til å være målelig.

Det er relevant for:
- emergent causal cones,
- quasi-lokalitet,
- og spørsmålet om stabile makroregimer.

### 8.2 For energidiskusjonen
Vi har tidligere sett at visse størrelser (som \(K\) og i lukkede sektorer \(\beta_1\)) oppfører seg invariant-lignende. Nå ser vi i tillegg at noen regimer ser ut til å være **repair-vennlige**. Hvis disse regimene overlapper med regimer som også viser liten makrodrift, er det et sterkt tegn på at “stabil spacetime” og “emergent conservation” kan være to sider av samme dynamiske fenomen.

### 8.3 For filosofien
Det er et viktig metodologisk skille mellom:
- “to modeller divergerer alltid, altså er repair umulig” og
- “to modeller divergerer under en for grov kobling.”

v0.7 viser at noe av det som tidligere kunne se ut som fundamental divergens, faktisk var koblingssensitivt. Det gjør prosjektet mer modent filosofisk: vi tester ikke bare en idé, vi tester også **hvordan ideen måles**.

## 9. Hva v0.7 ikke viser

Det er like viktig å si hva dette steget **ikke** har etablert:

1. Vi har ikke vist full meeting i hovedregimet.
2. Vi har ikke bevist en streng Lieb–Robinson-lignende bound i denne toy-modellen.
3. Vi har ikke vist at de mest repair-vennlige regimene også er de mest dimensjons- eller energi-vennlige.

v0.7 er derfor et **metodisk skarpere mellomsteg**, ikke sluttpunktet.

## 10. Neste riktige steg: v0.8

v0.8 bør være et egentlig **fasekart** som legger fire ting på samme parameterrom:

1. `meeting_fraction` / repair
2. front-hastighet / radiusutbredelse
3. quasi-invariants / makrodrift
4. geometri-proksier (`spectral_radius`, `clustering`, `dim_proxy`)

Det er først da vi kan begynne å si noe virkelig sterkt om hvilke regimer som er kandidater for emergent spacetime i denne modellen.

## 11. Filene fra dette steget

Kjernefiler:
- `relational_universe_local_max_coupling_lab.py`
- `relational_universe_v07_phase_probe.py`

Resultatfiler:
- `v07_bd_closed_swap_multirun.csv`
- `v07_bd_closed_swap_multirun_summary.md`
- `v07_bd_closed_swap_seed109_rank_summary.md`
- `v07_bd_closed_swap_seed109_max_summary.md`
- `v07_phase_probe_repr.csv`
- `v07_phase_probe_repr.md`

## 12. Referanser og matematisk bakgrunn

Følgende ideer ligger i bakgrunnen for v0.7, uten at vi hevder at toy-modellen er et direkte eksemplar av noen av dem:

1. **Uniformization / randomization for CTMC**  
   Idéen om å representere en kontinuerlig-tids Markovkjede via en dominerende Poisson-klokke og thinning.

2. **Koblingsmetoden**  
   Idéen om å konstruere to prosesser på samme sannsynlighetsrom for å studere møte, kontraksjon eller asymptotikk.

3. **Lieb–Robinson / endelig propagasjonshastighet**  
   Den generelle tanken at lokale interaksjoner kan gi en effektiv “lyskjegle” og begrenset spredningshastighet.

4. **Causal graph dynamics**  
   Idéen om at lokal omskriving på grafer kan gi en dynamisk, men fortsatt kausalt begrenset utvikling.

## 13. Ordliste og forklaringer

**CTMC** – *Continuous-Time Markov Chain.*  
En stokastisk prosess der hopp skjer i kontinuerlig tid.

**Uniformization / randomization**  
En måte å skrive en CTMC som en felles Poisson-klokke + diskrete hopp med thinning.

**Coupling / kobling**  
En metode der to tilfeldige prosesser bygges på samme sannsynlighetsrom for å sammenligne dem direkte.

**Maximal coupling / maksimal kobling**  
En kobling som maksimerer sannsynligheten for at to tilfeldige valg blir identiske.

**Familywise coupling**  
Kobling først på nivået “hvilken hendelsesfamilie skjer”.

**Local kernel / lokal overgangskjerne**  
Den konkrete sannsynlighetsfordelingen over lokale hendelser gitt aktuell tilstand og valgt familie.

**Meeting**  
Tidspunktet der de to grenene er nøyaktig identiske som tilstander.

**Survival curve / overlevelseskurve**  
Her: sannsynligheten for at grenene fortsatt ikke har møttes innen tid \(t\).

**Unequal time**  
Total tid de to grenene er forskjellige.

**Repair**  
At forskjellen mellom grenene minker eller forsvinner, helt eller delvis.

**Descriptor / hendelsesdeskriptor**  
En eksplisitt kode for en lokal hendelse, f.eks. hvilken token som beveger seg og hvilke noder som berøres.

**Shared token fraction**  
Andelen token-ID-er som fortsatt finnes i begge grener ved slutt.

**Quasi-invariant**  
En størrelse som ikke er eksakt bevart, men som drifter lite i et metastabilt regime.

**Causal cone / kausal kjegle**  
Området der en lokal forskjell har rukket å påvirke systemet etter en gitt tid.

**\(\beta_1\)**  
Første Betti-tall / cycle rank for grafen: et mål på antall uavhengige loops.