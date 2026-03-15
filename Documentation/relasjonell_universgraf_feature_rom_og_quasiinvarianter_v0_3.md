
# Relasjonell universgraf v0.3: utvidet feature-rom, algebraiske identiteter og quasi-invarianter

**Stil:** skrevet i en professoral tone i skjæringspunktet mellom fysikk, matematikk og filosofi.  
**Status:** forskningsnotat og arbeidsavhandling; ikke etablert fysikk.  
**Formål:** dokumentere neste naturlige steg i prosjektet: å utvide feature-rommet, skille rene algebraiske identiteter fra dynamiske invariants, og undersøke om åpne regimer har ikke-trivielle quasi-invarianter.

---

## 0. Hvorfor dette er neste riktige steg

I den forrige fasen kom vi frem til tre viktige innsikter:

1. Den minimale modellen kan formaliseres som en dynamisk relasjonell graf med lokale omskrivninger.
2. Et første energi-begrep kan bygges av **action-budsjett** \(K\) og **syklusladning** \(\beta_1\).
3. I en topologisk lukket sektor er \(K\) og \(\beta_1\) naturlige eksakte invariants.

Det neste nødvendige grepet er da ikke å oppfinne nye ontologiske elementer, men å undersøke om de mer finmaskede makrostrukturene — triangler, 4-noders motiver og spektrale størrelser — gir oss:

- nye eksakte invariants,
- eller bare **quasi-invarianter**,
- eller i verste fall bare artefakter av dårlig valgte koordinater i feature-rommet.

Dette er et avgjørende metodologisk punkt. I enhver seriøs teoriutvikling må man skille mellom:

- **kinematiske identiteter** (som følger av definisjoner),
- **dynamiske invariants** (som følger av reglene),
- **empiriske quasi-invarianter** (som følger av et metastabilt regime).

Hvis man ikke gjør det, risikerer man å ta en tautologi for en fysisk lov.

---

## 1. Utvidet feature-rom

La tilstanden være \(S=(G,\{\tau_i\}_{i=1}^K)\), der \(G=(V,E)\) er grafen og \(\tau_i\) er token-posisjonene.

Vi innfører følgende feature-vektor:

\[
F(S) =
(K,N,M,C,\beta_1,W,T,S_3,C_4,Q_2,\rho_A,\mathcal{C},d_{\mathrm{eff}})
\]

der

- \(K\): antall tokens,
- \(N=|V|\): antall noder,
- \(M=|E|\): antall kanter,
- \(C\): antall sammenhengskomponenter,
- \(\beta_1=M-N+C\): første Betti-tall / cycle rank,
- \(W=\sum_v \binom{\deg(v)}{2}\): antall wedges (lengde-2 stier med felles sentrum),
- \(T\): antall triangler,
- \(S_3=\sum_v \binom{\deg(v)}{3}\): antall 3-stjerner (et 4-noders motiv),
- \(C_4\): antall 4-sykluser,
- \(Q_2=\sum_v \deg(v)^2\): andre gradmoment,
- \(\rho_A\): spektralradius til adjakensmatrisen,
- \(\mathcal{C}\): clustering-koeffisient,
- \(d_{\mathrm{eff}}\): en grov dimensjonsproxy fra volumvekst.

Dette feature-rommet er ikke valgt vilkårlig. Det er konstruert for å representere tre lag samtidig:

### 1.1 Topologisk sektor
\[
(K,N,M,C,\beta_1)
\]

Dette er den groveste strukturen: størrelse, sammenheng og loop-rang.

### 1.2 Lokal geometri / motivsektor
\[
(W,T,S_3,C_4,Q_2,\mathcal{C})
\]

Her begynner “stoffet” i spacetime-regimet å få lokalt mønster.

### 1.3 Spektral sektor
\[
(\rho_A,d_{\mathrm{eff}})
\]

Her fanger vi globale distribusjonsegenskaper og grov emergent geometri.

---

## 2. Algebraiske identiteter som må skilles fra fysikk

Det mest overraskende og samtidig mest nyttige resultatet i denne fasen er at flere tilsynelatende “bevaringslover” i realiteten er **rene algebraiske identiteter**.

### 2.1 Den første identiteten
For enhver graf gjelder

\[
\beta_1 = M - N + C.
\]

Dette er ikke en lov om dynamikk. Det er en definisjonell identitet.

Dermed følger også:

\[
M - N - \beta_1 = -C.
\]

I sammenhengende regime (\(C=1\)) blir dette

\[
M - N - \beta_1 = -1.
\]

Så enhver singulærverktor i empirisk analyse som peker i retning av \(M-N-\beta_1\), er ikke nødvendigvis en ny fysisk invariant; den kan være den trivielle grafidentiteten i forkledning.

### 2.2 Den andre identiteten
For ethvert enkelt urettet nettverk gjelder

\[
Q_2 = \sum_v \deg(v)^2 = 2W + 2M.
\]

Beviset er elementært:

\[
\binom{d}{2} = \frac{d(d-1)}{2}
\quad\Rightarrow\quad
2W = \sum_v d(v)(d(v)-1)=Q_2-\sum_v d(v)=Q_2-2M.
\]

Altså:

\[
Q_2 - 2W - 2M = 0.
\]

I sammenhengende regime kan vi erstatte \(M\) med \(N+\beta_1-1\), og få

\[
Q_2 - 2W - 2N - 2\beta_1 + 2 = 0.
\]

Dette er ekstremt viktig. Det betyr at noe som i en rå SVD-analyse ser ut som en “mystisk” konservativ kombinasjon av \(W, M, Q_2, N, \beta_1\), ofte bare er en lineær avbildning av rene grafidentiteter.

### 2.3 Metodologisk konsekvens
Før man leter etter dynamiske quasi-invarianter, må man derfor **reduksjons-faktorisere** feature-rommet med hensyn til de eksakte algebraiske identitetene.

Ellers vil nullrommet i dataanalysen domineres av tautologier.

---

## 3. Regler og eksakte feature-endringer

Vi bruker en lokal regelklasse nær simulatorenes faktiske implementasjon:

1. **Leaf seed attachment**  
   Ny node \(x\) kobles til eksisterende vert \(a\).

2. **Triadic closure / edge-addisjon**  
   En ny kant legges til mellom to allerede sammenhengende noder \(u,v\), vanligvis via et felles nabolag.

3. **Non-bridge edge deletion**  
   En kant \((u,v)\) fjernes bare dersom det ikke disconnecter komponenten.

4. **Strict edge-swap**  
   Kanten \((v,u)\) fjernes og \((v,w)\) legges til, med krav om at den nye kanten ikke allerede finnes.

La \(d_u,d_v,d_w\) være gradene før hendelsen. La \(c_{uv}=|N(u)\cap N(v)|\) være antall felles naboer, og \(p^{(3)}_{uv}\) antall enkle lengde-3 stier mellom \(u\) og \(v\).

### 3.1 Leaf seed attachment
For vert \(a\) med grad \(d_a\):

\[
\Delta N=+1,\quad
\Delta M=+1,\quad
\Delta C=0,\quad
\Delta \beta_1=0,\quad
\Delta K=0
\]

og

\[
\Delta W=d_a,
\qquad
\Delta T=0,
\qquad
\Delta S_3=\binom{d_a}{2},
\qquad
\Delta Q_2=2d_a+2,
\qquad
\Delta C_4=0.
\]

Her ser man tydelig hvordan “spacetime-volum” kan vokse uten å skape ny loop-rang. Dette gjør leaf-seeds til en særdeles god kandidat for “romlig ekspansjon uten energiinjeksjon”, hvis energi primært identifiseres med \(K\) og/eller \(\beta_1\).

### 3.2 Edge-addisjon
For en ny kant mellom to eksisterende, ikke-adjiserte noder \(u,v\):

\[
\Delta N=0,\quad
\Delta M=+1,\quad
\Delta C=0,\quad
\Delta \beta_1=+1.
\]

Videre:

\[
\Delta W=d_u+d_v,
\qquad
\Delta T=c_{uv},
\qquad
\Delta S_3=\binom{d_u}{2}+\binom{d_v}{2},
\]

\[
\Delta Q_2=2(d_u+d_v)+2,
\qquad
\Delta C_4=p^{(3)}_{uv}.
\]

Tolkningen er klar: når man lukker en ny relasjon internt i en komponent, skaper man både ny syklusladning og lokal motivtetthet.

### 3.3 Non-bridge edge deletion
For en kant \((u,v)\) som ikke er bro:

\[
\Delta N=0,\quad
\Delta M=-1,\quad
\Delta C=0,\quad
\Delta \beta_1=-1.
\]

Og:

\[
\Delta W=-(d_u+d_v-2),
\qquad
\Delta T=-c_{uv},
\]

\[
\Delta S_3=-\binom{d_u-1}{2}-\binom{d_v-1}{2},
\qquad
\Delta Q_2=-2(d_u+d_v)+2,
\qquad
\Delta C_4=-p^{(3)}_{uv}.
\]

Dette er den motsatte prosessen av edge-addisjon: sykluser tappes, lokal struktur glattes ut, og det andre gradmomentet faller.

### 3.4 Strict edge-swap
For \((v,u)\mapsto(v,w)\):

\[
\Delta N=0,\quad
\Delta M=0,\quad
\Delta C=0,\quad
\Delta \beta_1=0,\quad
\Delta K=0.
\]

Dessuten:

\[
\Delta W = d_w-d_u+1,
\qquad
\Delta Q_2 = 2(d_w-d_u+1).
\]

For \(T\) og \(C_4\) finnes det ingen ren universell formel som er like enkel, fordi de avhenger av den lokale konteksten før og etter omskrivingen. Den presise og praktiske metoden er derfor å regne dem ved før/etter-differanse.

Dette er allerede et viktig resultat: **topologiske invariants kan være eksakte selv når motiv- og spektralsektoren flyter.**

---

## 4. Eksakte invariants i utvidet feature-rom

Når feature-rommet er utvidet, oppstår to forskjellige typer nullretninger:

### 4.1 Kinematiske nullretninger
Disse følger av grafidentitetene alene:

- \(M-N-\beta_1+C=0\)
- \(Q_2-2W-2M=0\)

De er ikke et resultat av reglene. De er geometriske identiteter.

### 4.2 Dynamiske nullretninger
Disse følger av reglene.

For den **topologisk lukkede sektoren**:
- leaf-seed,
- strict swap,
- ingen fri edge-addisjon,
- ingen fri edge-delete,
- ingen token birth/death,

får vi:

- \(K\) eksakt invariant,
- \(\beta_1\) eksakt invariant.

I sammenhengende regime er også \(M-N\) invariant, men dette er bare den samme informasjonen skrevet annerledes, fordi

\[
\beta_1=M-N+1.
\]

Altså: det reelle eksakte invariantrommet er spent opp av \(K\) og \(\beta_1\), mens \(M-N\) er en redundant koordinat i sammenhengende sektor.

### 4.3 Åpen sektor
Når triadic closure og non-bridge deletion begge er tillatt, faller \(\beta_1\) som eksakt invariant:

- edge-add gir \(\Delta \beta_1=+1\),
- delete gir \(\Delta \beta_1=-1\).

Da står bare \(K\) igjen som enkel eksakt invariant, forutsatt at token-antallet er lukket.

Dette er en sentral fysisk innsikt: så snart du lar universet aktivt generere og destruere loops, er loop-ladning ikke lenger grunnleggende bevart. Da må eventuell energibevaring være enten:

- emergent,
- eller knyttet til et rikere feature-rom.

---

## 5. Empirisk analyse: to representative regimer

Jeg kjørte to representative tester med den nye simulatoren `relational_universe_feature_lab.py`.

### 5.1 Lukket topologisk sektor
Parametre:
- leaf-seeds aktive,
- strict swaps aktive,
- ingen triadic closure,
- ingen edge-delete,
- sammenheng forsøkes bevart.

Resultat:
- \(K\) var eksakt konstant.
- \(\beta_1\) var eksakt konstant.
- \(N\) og \(M\) vokste låst sammen, slik at \(M-N\) var konstant.
- Triangler, 4-sykluser og spektralradius var ikke eksakte invariants; de driftet eller fluktuerte.

Den reduserte analysen ga:

- **rank 1:** \(+1.0000\cdot K\)
- **rank 2:** \(-1.0000\cdot \beta_1\)

Det er akkurat det teorien forutsier.

### 5.2 Åpent balansert regime
Parametre:
- leaf-seeds aktive,
- triadic closure og delete omtrent balansert,
- strict swaps aktive,
- sammenheng forsøkes bevart.

Her viste råanalysen umiddelbart en nøyaktig lineær relasjon mellom \(N\), \(M\) og \(\beta_1\). Men dette er, som vist ovenfor, bare grafidentiteten i forkledning.

Etter å ha redusert bort de mest trivielle identitetene sto vi igjen med:

- **rank 1:** \(K\) (eksakt invariant)
- **rank 2:** \(\rho_A\) (spektralradius) som den langsomst driftende ikke-trivielle størrelsen i akkurat denne kjøringen
- **rank 3:** en blanding av \(N,\beta_1,W,T\)

Dette er lovende, men må tolkes med stor forsiktighet.

### 5.3 Kritisk tolkning av spektralradius
At \(\rho_A\) fremstår som en “god” quasi-invariant i en rå SVD-analyse betyr **ikke** at spektralradius er en fundamental bevart størrelse.

Det kan like gjerne skyldes:
- at \(\rho_A\) numerisk har mye mindre skala enn de grove tellevariablene,
- at den vokser langsomt fordi den er en global gjennomsnittsstørrelse,
- eller at valgt regime favoriserer relativ homogenisering.

Det riktige utsagnet er derfor:

> I det åpne testregimet ser \(\rho_A\) ut til å være den mest stabile ikke-trivielle makrostørrelsen i det valgte, ustandardiserte feature-rommet.

Det er interessant, men ikke bevis.

---

## 6. Hva dette betyr for energibegrepet

Nå kan vi formulere et mer modent svar på spørsmålet om energi.

### 6.1 Første lag: eksakt topologisk energi
I en lukket topologisk sektor er den enkleste energikandidaten

\[
E_{\mathrm{top}} = \alpha K + \beta \beta_1.
\]

Dette er matematisk rent og fysisk tolkbart:
- \(K\): action-budsjett,
- \(\beta_1\): loop-ladning.

### 6.2 Andre lag: emergent makroenergi
I åpne regimer er ikke \(\beta_1\) eksakt bevart. Da bør man i stedet tenke at energien i spacetime-regimet er en **quasi-konservativ makrostørrelse**, noe slikt som

\[
E_{\mathrm{eff}} = \alpha K + \beta \beta_1 + \gamma \Phi_{\mathrm{macro}},
\]

der \(\Phi_{\mathrm{macro}}\) kan være en sammensetning av:
- spektralradius,
- lokal motivtetthet,
- eller andre reduserte makrofeatures.

Poenget er ikke at denne formelen allerede er kjent, men at vi nå har et konkret program for å finne slike kandidater empirisk og deretter teoretisk.

### 6.3 Viktig filosofisk poeng
I denne modellen er ikke energi nødvendigvis en fundamental “substansmengde”. Den er snarere:

- en **organiserende constraint** på hvilke mikrodynamikker som kan bære et stabilt makroregime,
- og en **makroskopisk ladning** som vokser frem når spacetime-regimet er robust nok.

Det er mer i slekt med hvordan energi opptrer som generator og bevaringslov i effektiv fysikk, enn med ideen om “et lager av små energikuler”.

---

## 7. Hva vi nå har lært

Dette er, etter mitt syn, de viktigste resultatene av steg v0.3:

1. Det utvidede feature-rommet gjør modellen mer testbar uten å endre ontologien.
2. Flere tilsynelatende “bevarte” lineære kombinasjoner er i realiteten algebraiske identiteter.
3. I en lukket topologisk sektor er \(K\) og \(\beta_1\) de reelle eksakte invariantene.
4. I åpne regimer finnes det ikke ennå en entydig ny eksakt invariant utover \(K\).
5. Det finnes empiriske tegn til non-trivielle quasi-invarianter, men de er ennå regimatiske og koordinatavhengige.
6. Derfor er neste riktige forskningssteg å arbeide i et **redusert feature-rom**, der man først kvotienterer ut de trivielle identitetene, og deretter undersøker:
   - standardisert SVD,
   - regelbetingede forventningsverdier for \(\Delta F\),
   - og eventuelle lineære eller svakt ikke-lineære slow variables.

---

## 8. Operasjonell betydning for simulatorene

Den nye simulatoren `relational_universe_feature_lab.py` gjør fire ting som de tidligere ikke gjorde:

1. den måler utvidede motiver,
2. den måler en spektral størrelse,
3. den eksporterer et rikere feature-rom til CSV,
4. den kan skrive en første empirisk quasi-invariantanalyse til Markdown.

Dette er viktig fordi prosjektet nå ikke bare er spekulativ ontologi. Det er blitt et **laboratorium for regelbasert makrofysikk**.

Med Codex kan man nå:
- iterere på regelklasser,
- måle hvilke invariants som overlever,
- og se om emergent geometri og emergent bevaringslover virkelig er robuste.

---

## 9. Neste naturlige steg etter dette

Etter v0.3 er det metodologisk riktige neste steget ikke å legge til enda flere features ukritisk, men å gjøre tre presise forbedringer:

### 9.1 Redusert basis
Arbeid i et basis der de trivielle identitetene allerede er eliminert.  
Eksempel:

\[
F_{\mathrm{red}} = (K,N,\beta_1,W,T,S_3,C_4,\rho_A,d_{\mathrm{eff}})
\]

eller enda mer aggressivt, hvis \(N\) og \(\beta_1\) skal tolkes som volum- og loop-koordinater.

### 9.2 Standardisert invariantanalyse
Kjør SVD både på rå inkrementer og på standardiserte inkrementer.  
Ellers risikerer man at små-skala features alltid ser “mer konservative” ut bare fordi tallene deres er mindre.

### 9.3 Regelbetinget \(\Delta F\)-analyse
I stedet for bare å se på tidsserier, bør man estimere

\[
\mathbb{E}[\Delta F \mid \text{regeltype}=r]
\]

for hver regeltype.  
Da kan man skille mellom:
- invariants som er null for hver regel,
- og invariants som bare er null i tidsmiddel.

Dette vil løfte modellen betydelig.

---

## 10. Filer som hører til dette steget

- `relational_universe_feature_lab.py`
- `feature_closed_summary.md`
- `feature_open_summary.md`
- `closed_reduced_analysis.md`
- `open_reduced_analysis.md`

Disse filene er ikke bare vedlegg; de er en del av teorien i operasjonell forstand. De viser hvordan prosjektet kan bevege seg fra begrepsdannelse til strukturell test.

---

## 11. Kort konklusjon

Den viktigste intellektuelle gevinsten i denne fasen er at modellen er blitt **mindre metaforisk og mer disiplinert**.

Vi har nå:

- et utvidet feature-rom,
- en eksplisitt forskjell mellom algebraiske identiteter og dynamiske invariants,
- en eksakt klassifikasjon av invariants i den lukkede topologiske sektoren,
- og en første empirisk metode for å lete etter quasi-invarianter i åpne regimer.

Det betyr at spørsmålet om energi ikke lenger bare er filosofisk. Det er nå et konkret problem om hvilke makrostørrelser som faktisk er stabile under lokal, stokastisk grafdynamikk.

Det er nettopp der en ekte teori begynner.

---

## Forklaringer på termer og forkortelser

- **Feature-rom:** et koordinatsystem av målbare størrelser som beskriver grafens makrotilstand.
- **Invariant:** en størrelse som ikke endres under dynamikken.
- **Quasi-invariant:** en størrelse som endrer seg svært sakte eller bare fluktuerer rundt en stabil verdi.
- **Kinematisk identitet:** en likhet som følger av definisjoner, ikke av dynamikken.
- **Dynamisk invariant:** en likhet eller bevaringslov som følger av reglene for hvordan systemet utvikler seg.
- **\(\beta_1\) (første Betti-tall):** antall uavhengige loops i grafen, \(\beta_1=M-N+C\).
- **Wedge:** et to-stegs motiv med én sentrum-node og to naboer; teller lokal “forgrening”.
- **\(S_3\) / 3-stjerne:** et 4-noders motiv med én sentrum-node koblet til tre andre.
- **\(C_4\):** en 4-syklus, altså en loop med fire noder.
- **Spektralradius \(\rho_A\):** største egenverdi til adjakensmatrisen; et mål på global koblingstetthet og konsentrasjon.
- **SVD (singular value decomposition):** lineær-algebraisk metode som her brukes til å finne kombinasjoner av features som endrer seg minst.
- **Strict edge-swap:** en regel der én kant flyttes lokalt uten å endre totalt antall kanter.
- **SSA / Gillespie:** en standard metode for kontinuerlig-tids stokastisk simulering.
- **Redusert basis:** et feature-set der trivielle identiteter er fjernet, slik at man analyserer reell dynamikk snarere enn tautologier.
