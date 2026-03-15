# Relasjonell universgraf: arbeidsavhandling v0.2

**Forfatterrolle:** skrevet i en professoral stil i skjæringspunktet mellom fysikk, matematikk og filosofi.  
**Status:** konseptuell forskningsskisse og matematisk arbeidsnotat, ikke etablert fysikk.  
**Formål:** samle modellen som er utviklet i samtalen, formulere et første matematisk rammeverk, klassifisere lineære invariants for den minimale regelklassen, og gjøre prosjektet direkte brukbart i simulatorer og med Codex.

---

## 0. Sammendrag

Vi tar utgangspunkt i en radikalt relasjonell ontologi:

- universet er informasjon,
- de enkleste bestanddelene er noder med relasjoner,
- det finnes bare **én** relasjonstype,
- endring skjer gjennom lokale **units of action**,
- tid er ikke bakgrunn, men oppstår gjennom hendelser,
- spacetime er et emergent stabilitetslag i samme relasjonelle stoff som alt annet,
- partikler er stabile klustre eller loops,
- entanglement er korrelasjon, ikke en separat kanal,
- nye seeds oppstår kontinuerlig, men er operasjonelt irrelevante før de får relasjon til en komponent.

Det mest presise resultatet så langt er dette:

1. En modell av denne typen kan **naturlig** gi opphav til en maksimal propagasjonshastighet, kausale kjegler, relasjonell tid og en proto-relativistisk kinematikk.
2. Den gir **ikke automatisk** full kvantemekanisk entanglement eller full Lorentz-invarians; disse må oppstå som effektive egenskaper av makroregimet.
3. Dersom man ønsker en energi-lignende størrelse som ikke bare er hendelsesrate, er den enkleste strenge kandidaten en kombinasjon av:
   - antall action-bærere/tokens \(K\), og
   - grafens første Betti-tall / cycle rank \(\beta_1 = |E|-|V|+C\).
4. For den minimale regelklassen vi har diskutert, kan man klassifisere eksakte lineære invariants ved nullrommet til regelmatrisen. Dette er det første virkelig "professorale" steget, fordi det løfter prosjektet fra metafor til kontrollerbar matematisk modell.
5. Resultatet av invariant-analysen er skarpt:
   - i en **topologisk sektor** der grafen vokser ved leaf-seeds og omkobles ved edge-swaps, men ikke skaper eller ødelegger frie sykler, er \(\beta_1\) eksakt bevart (opp til en konstant forskyvning i sammenhengende regime), og energi kan naturlig modelleres som \(E = \alpha K + \beta \beta_1\);
   - så snart man tillater fri intern edge-addisjon (triadic closure som faktisk lukker ny triangel) eller fri ikke-bro-sletting, forsvinner \(\beta_1\) som eksakt invariant, og man står igjen med \(K\) som eneste enkle eksakte invariant i sammenhengende, token-lukket sektor;
   - i mer åpne regimer må energibevaring derfor enten være **emergent/quasi-konservativ**, eller bero på dypere feature-set enn \((K,N,M,C)\).

Dette dokumentet samler modellen, formaliserer regelklassen, klassifiserer invariantene, forklarer hvordan de to simulatorene kan brukes, og legger ved Codex-prompter for videre utvikling.

---

## 1. Ontologisk og fysisk utgangspunkt

### 1.1 Fundamentale antagelser

Vi antar:

1. **Noder** er minimale informasjonsenheter.
2. **Relasjoner** er kanter i en dynamisk graf.
3. Det finnes **ingen fundamental forskjell** mellom "spacetime-relasjoner", "partikkel-relasjoner" eller "entanglement-relasjoner"; forskjeller er emergente mønstre.
4. **Units of action** er elementære lokale hendelser som omskriver relasjoner.
5. **Tilfeldighet** avgjør hvilke lokale hendelser som faktisk realiseres.
6. **Tid** er ikke bakgrunnstid, men hendelsesorden / intern telling av endringer.
7. **Spacetime** er et emergent, robust makrolag som organiserer støy.
8. **Partikler** er metastabile informasjonsklustre, ofte med loop-struktur.
9. **Entanglement** forstås i denne modellen som korrelasjon og felles constraint-struktur, ikke som superluminal signalering.
10. **Seeds** oppstår kontinuerlig, men uten relasjon til en komponent eksisterer de ikke operasjonelt for den komponenten.

### 1.2 Filosofisk posisjon

Dette er en streng relasjonalisme:

- objekter er ikke fundamentale substanser,
- rom er ikke en forhåndsgitt scene,
- identitet er historisk og relasjonell,
- eksistens er operasjonell: en node "finnes" for en komponent i den grad den er koblet inn i dens relasjonelle nett.

Dette setter modellen nær relasjonell metafysikk, prosessontologi og bakgrunnsløs fysikk, men uten å binde oss til én bestemt etablert teori.

---

## 2. Minimal dynamisk grafmodell

### 2.1 Mikrotilstand

La universet ved et gitt stadium beskrives av en urettet graf

\[
G = (V,E),
\]

der:

- \(V\) er mengden noder,
- \(E\) er mengden kanter,
- alle kanter er av samme type.

I simulatorene representeres units of action teknisk ved **tokens** som flytter seg på grafen. Dette er en implementasjonsstrategi, ikke en ontologisk ny primitive.

Vi innfører derfor også en tilstand

\[
S = (G,\tau_1,\ldots,\tau_K),
\]

der \(\tau_i \in V\) er posisjonen til token \(i\), og \(K\) er antall tokens.

### 2.2 Tolkning av tokens

Tokens kan forstås som:

- handlingsbærere,
- lokal action-kapasitet,
- et første, svært grovt "kinetisk" energibudsjett.

Det er viktig at dette **ikke** betyr at energi *er* det samme som antall hendelser per tidsenhet. Tokens er en tilstandsvariabel, ikke selve prosessraten.

### 2.3 Lokal dynamikk

Dynamikken er gitt ved lokale omskrivninger. I simulatorene skjer dette ved at et token:

1. velger en eksisterende kant,
2. traverserer den,
3. utfører en lokal rewrite i et nabolag av begrenset radius.

For å unngå å smugle inn en global klokke brukes en **asynkron stokastisk scheduler** (Gillespie-/SSA-lignende).

---

## 3. Emergent spacetime, bevegelse og relativitet

### 3.1 Spacetime som makrostruktur

Spacetime er ikke et eget stoff, men en stabil makrostruktur i grafen: et regime der den lokale stokastiske mikrodynamikken grovkornet fremstår som:

- omtrent homogen,
- omtrent isotrop,
- med veldefinerte kausale kjegler,
- med robuste avstands- og klokkeproksier.

### 3.2 Bevegelse

Bevegelse er sekvenser av relasjonsendringer som, i spacetime-regimet, tolkes som forflytning.

### 3.3 Relativitet: hva som virker plausibelt

Ut fra modellen følger følgende rimelig naturlig:

- maksimal propagasjonshastighet fordi påvirkning bare forplanter seg lokalt,
- kausale kjegler definert av hvilke noder som kan nås etter et gitt antall lokale hendelser,
- fravær av absolutt samtidighet fordi all tidsmåling er intern og signalbegrenset.

Det følger **ikke automatisk** at full Lorentz-invarians oppstår. For det må makroregimet skjule eventuell mikroskopisk privilegert oppdateringsstruktur.

### 3.4 Entanglement

I den nåværende formuleringen er entanglement best forstått som:

- korrelasjon,
- felles historisk relasjonsstruktur,
- delt constraint-sett.

Det bør **ikke** behandles som en egen snarvei for signalering gjennom spacetime.

---

## 4. Energi: fra metafor til funksjonal

### 4.1 Hvorfor "energi = antall actions" er utilstrekkelig

Hvis energi identifiseres med hendelsesrate, får man noe som ligner temperatur eller lokal støyintensitet. Det kan være nyttig, men er normalt **ikke** en konservert størrelse.

For å få et fysisk interessant energibegrep trenger vi i stedet en tilstandsfunksjonal

\[
E(S),
\]

som er:

- eksakt konservativ,
- eller lokalt konservativ,
- eller emergent quasi-konservativ i et stabilt makroregime.

### 4.2 Tre naturlige energikandidater

#### (A) Token-energi

\[
E_{\text{tok}}(S)=K
\]

Hvis token birth/death er skrudd av, og tokens ikke tapes ved pruning, er dette en eksakt invariant.

#### (B) Topologisk energi via loop charge

\[
\beta_1(G)=|E|-|V|+C(G)
\]

der \(C(G)\) er antall sammenhengskomponenter.

Dette er grafens første Betti-tall / cycle rank: antall uavhengige loops.

Denne størrelsen er spesielt interessant fordi:

- den er ren struktur,
- den er lineær i de grunnleggende tellevariablene,
- den passer med intuisjonen om at stabile eksitasjoner er loop-bårne.

#### (C) Stress-energi

\[
E_{\text{stress}}(G)=\sum_{v\in V}(\deg(v)-d_0)^2
\]

Denne er ikke en naturlig eksakt invariant, men en nyttig makrodiagnostikk for "geometrisk stivhet" eller avvik fra et ønsket gradregime.

### 4.3 Kombinert energifunksjonal

En enkel kombinert kandidat er

\[
E_{\text{tot}}(S)=w_K K + w_{\beta}\beta_1(G) + w_s E_{\text{stress}}(G).
\]

- \(w_K\), \(w_{\beta}\), \(w_s\) er vekter,
- \(E_{\text{stress}}\) brukes primært som diagnostikk,
- de strenge lineære invariantene oppstår i praksis fra \(K\) og \(\beta_1\).

---

## 5. Professoralt steg: klassifikasjon av lineære invariants

Dette er det sentrale nye trinnet.

### 5.1 Feature-vektor

Vi starter med den lineære feature-vektoren

\[
x = (K,N,M,C)^{\top},
\]

der:

- \(K\) = antall tokens,
- \(N=|V|\) = antall noder,
- \(M=|E|\) = antall kanter,
- \(C\) = antall sammenhengskomponenter.

Videre er

\[
\beta_1 = M - N + C
\]

en lineær kombinasjon av disse, så \(\beta_1\) trenger ikke tas som en uavhengig basisvariabel.

### 5.2 Regler som stoikiometriske vektorer

Hver lokal regel representeres ved en endringsvektor \(\Delta_r\) i feature-rommet.

Vi bruker følgende primitivliste:

| Regel | Beskrivelse | \(\Delta K\) | \(\Delta N\) | \(\Delta M\) | \(\Delta C\) | \(\Delta \beta_1\) |
|---|---|---:|---:|---:|---:|---:|
| \(T\) | Traversering uten topologisk endring | 0 | 0 | 0 | 0 | 0 |
| \(W\) | Edge-swap / rewire med bevart \(|E|\) og \(|C|\) | 0 | 0 | 0 | 0 | 0 |
| \(S\) | Seed-attach: ny leaf kobles til eksisterende komponent | 0 | +1 | +1 | 0 | 0 |
| \(A\) | Intern edge-addisjon (f.eks. vellykket triadic closure) | 0 | 0 | +1 | 0 | +1 |
| \(D_{\mathrm{cyc}}\) | Sletting av ikke-bro-kant | 0 | 0 | -1 | 0 | -1 |
| \(D_{\mathrm{br}}\) | Sletting av bro-kant uten pruning | 0 | 0 | -1 | +1 | 0 |
| \(D_{\mathrm{leaf}}\) | Sletting av leaf-kant + pruning av isolert leaf-node | 0 | -1 | -1 | 0 | 0 |
| \(B_+\) | Token birth | +1 | 0 | 0 | 0 | 0 |
| \(B_-\) | Token death | -1 | 0 | 0 | 0 | 0 |

Kommentarer:

1. \(A\) beskriver **vellykket** intern edge-addisjon, altså at en ny kant faktisk skapes.
2. \(W\) er den ideelle edge-swapen: \(|E|\), \(|C|\) og dermed \(\beta_1\) bevares.
3. \(D_{\mathrm{leaf}}\) er en sammensatt makroregel: først slettes en bridge mot en leaf, deretter prunes den isolerte leaf-noden.

### 5.3 Hva er en lineær invariant?

En lineær invariant er en funksjon

\[
L(x)=aK+bN+cM+dC
\]

slik at

\[
L(x+\Delta_r)=L(x)
\]

for alle tillatte regler \(r\).

Dette er ekvivalent med kravet

\[
(a,b,c,d)\cdot \Delta_r = 0
\]

for alle tillatte \(\Delta_r\).

Med andre ord: invariants finnes som nullrommet til regelmatrisen.

---

## 6. Nullromsanalyse for relevante regelklasser

### 6.1 Klasse I: ren topologisk drift uten cycle creation/annihilation

Tillatte regler:

\[
\{T,W,S\}
\]

Betingelsen kommer bare fra \(S\):

\[
b+c=0.
\]

Dermed er invariantrommet

\[
L = aK + b(M-N) + dC.
\]

Altså:

- \(K\) er invariant,
- \(M-N\) er invariant,
- \(C\) er invariant.

I et sammenhengende regime (\(C=1\) konstant) blir dette ekvivalent med at invariantrommet spennes av

\[
K \quad \text{og} \quad \beta_1=M-N+1.
\]

**Fysisk tolkning:** et univers kan vokse i noder og kanter ved leaf-seeds uten å endre loop charge.

### 6.2 Klasse II: topologisk sektor med bridge-deletions

Tillatte regler:

\[
\{T,W,S,D_{\mathrm{br}}\}
\]

Da får vi:

- fra \(S\): \(b+c=0\),
- fra \(D_{\mathrm{br}}\): \(-c+d=0\).

Løsningen er

\[
d=c,\qquad b=-c.
\]

Dermed:

\[
L = aK + c(-N+M+C)=aK + c\beta_1.
\]

Altså er invariantrommet

\[
\mathrm{span}\{K,\beta_1\}.
\]

Dette er et svært viktig resultat.

**Dom:** dersom man vil ha en streng energi-lignende topologisk størrelse, er \(\beta_1\) den naturlige kandidaten i nettopp denne regelklassen.

### 6.3 Klasse III: topologisk sektor med leaf-pruning i stedet for eksplisitt komponentdeling

Tillatte regler:

\[
\{T,W,S,D_{\mathrm{leaf}}\}
\]

Da får vi:

- fra \(S\): \(b+c=0\),
- fra \(D_{\mathrm{leaf}}\): \(-b-c=0\),

som er samme ligning.

Dermed er invariantrommet

\[
L = aK + b(M-N) + dC.
\]

Hvis vi samtidig holder oss i ett sammenhengende univers-regime, er igjen den relevante fysiske konklusjonen at

\[
\mathrm{span}\{K,\beta_1\}
\]

er den operative invariantbasen.

### 6.4 Klasse IV: tillat fri cycle creation

Tillatte regler:

\[
\{T,W,S,A\}
\]

Da får vi:

- fra \(S\): \(b+c=0\),
- fra \(A\): \(c=0\).

Derfor:

\[
b=0,
\]

og invariantrommet blir

\[
L=aK+dC.
\]

I et sammenhengende regime er \(C\) konstant, og vi sitter igjen med

\[
L \sim K.
\]

**Konklusjon:** fri intern edge-addisjon ødelegger \(\beta_1\) som eksakt invariant.

### 6.5 Klasse V: tillat fri cycle deletion

Tillatte regler:

\[
\{T,W,S,D_{\mathrm{cyc}}\}
\]

Da får vi:

- fra \(S\): \(b+c=0\),
- fra \(D_{\mathrm{cyc}}\): \(c=0\),

så igjen er \(b=0\), og invariantrommet blir

\[
L=aK+dC.
\]

I sammenhengende regime: bare \(K\).

### 6.6 Klasse VI: tillat både cycle creation og cycle deletion

Tillatte regler:

\[
\{T,W,S,A,D_{\mathrm{cyc}}\}
\]

Da er konklusjonen enda skarpere:

- \(c=0\),
- \(b=0\),

så bare \(aK+dC\).  
I sammenhengende regime: bare \(K\).

### 6.7 Klasse VII: åpne token-regimer

Hvis man tillater \(B_+\) eller \(B_-\), får man i tillegg kravet

\[
a=0.
\]

Da:

- i den rene topologiske sektoren med \(S\) og \(D_{\mathrm{br}}\) kan \(\beta_1\) fortsatt være eksakt invariant,
- i et regime med fri cycle creation/deletion og token birth/death finnes i sammenhengende regime **ingen ikke-triviell enkel lineær invariant** i feature-settet \((K,N,M,C)\).

Dette er viktig, fordi det forteller oss nøyaktig når den enkle energifunksjonalen er for svak.

---

## 7. Hovedkonklusjon fra invariant-analysen

### 7.1 Streng formulering

For den minimale regelklassen som er naturlig i simulatorene, gjelder:

1. **Seed-attach alene** bevarer \(\beta_1\).
2. **Edge-swaps** bevarer \(\beta_1\).
3. **Bridge deletion** kan bevares kompatibelt med \(\beta_1\), enten direkte eller via leaf-pruning.
4. **Fri intern edge-addisjon** endrer \(\beta_1\) med \(+1\).
5. **Fri ikke-bro-sletting** endrer \(\beta_1\) med \(-1\).

Derfor er \(\beta_1\) en eksakt invariant **bare** i en regelklasse der frie syklers opprettelse og tilintetgjørelse enten er forbudt eller bundet sammen i høyere ordens regler som samlet gir \(\Delta \beta_1=0\).

### 7.2 Fysisk tolkning

Dette leder til en dypere tese:

> Dersom vårt univers er en enorm, selvstabiliserende informasjonsklynge med noe som makroskopisk fremstår som energibevaring, må mikrodynamikken enten:
>
> - i hovedsak ligge i en \(\beta_1\)-bevarende topologisk sektor,
> - eller balansere \(\beta_1\)-skapende og \(\beta_1\)-destruerende prosesser statistisk,
> - eller ha dypere skjulte invariants utover \((K,N,M,C)\).

Dette er ikke bare en matematisk detalj; det er et reelt seleksjonskriterium for hvilke mikroteorier som kan gi et stabilt makrounivers.

---

## 8. Forholdet mellom energi og stabilitet

### 8.1 Må energi være bevart for at struktur skal eksistere?

Nei, ikke strengt tatt. Mange ikke-likevekts- og dissipative systemer kan ha stabile attractors.

### 8.2 Må noe være bevart for at et univers som vårt skal være lovmessig?

Svært sannsynlig ja.

Et makroregime med:

- langlivede eksitasjoner,
- repeterbar dynamikk,
- kontrollerbar transport,
- robust geometri,

krever nesten alltid minst noen strenge eller quasi-strenge invariants.

### 8.3 Derfor er spørsmålet egentlig dette

Ikke "må energi bevares?" i absolutt forstand, men:

- hvilke features må være robuste nok til å danne et stabilitetslag,
- og hvilke kombinasjoner av disse features kan fungere som energi i effektiv teori?

I den nåværende modellen er svaret:

- \(K\) er den enkleste handlings-relaterte kandidaten,
- \(\beta_1\) er den enkleste topologiske kandidaten,
- \(E_{\text{stress}}\) er en nyttig, men sekundær, geometri-diagnostikk.

---

## 9. Lokal bevaring

### 9.1 Token-kontinuitet

I den utvidede simulatoren kan man definere en fast initial region \(A\) og bokføre eksakt:

\[
\Delta K_A = \text{inn-fluks} - \text{ut-fluks} + \text{births} - \text{deaths} + \text{relocations} - \text{prune-loss}.
\]

Dette gir en ren diskret kontinuitetsligning for token-energi.

### 9.2 Hva dette betyr filosofisk

Selv uten et bakgrunnsrom kan man formulere lokal bevaring, fordi lokalitet er definert ved grafnabolag og randfluks, ikke ved koordinater i \(\mathbb{R}^3\).

---

## 10. Hva simulatorene faktisk betyr

### 10.1 `relational_universe_sim.py`

Dette er en minimal sandbox for:

- stokastisk lokal grafdynamikk,
- seed-vekst,
- token-båren action,
- enkel metrikk: clustering, volumvekst, grov dimensjonsproxy.

Den brukes for å undersøke:

- om store sammenhengende komponenter overlever,
- om loops og triangler spontant dannes,
- om det oppstår metastabile mønstre.

### 10.2 `relational_universe_sim_energy.py`

Dette er en utvidelse med:

- eksplisitt beregning av \(\beta_1\),
- energifunksjonaler,
- kontinuitetsdiagnostikk for tokens,
- eksakt energisjekk i lukkede/tilnærmet lukkede regimer,
- driftanalyse for quasi-konservering.

### 10.3 Viktig lesemåte

Simulatorene er **ikke** modeller av vårt faktiske kosmos. De er eksperimentelle testbenker for å avgjøre:

- hvilke typer regler som er kompatible med stabil struktur,
- hvilke invariants som finnes,
- og hvilke makroregimer som er verdige videre fysikalsk tolkning.

---

## 11. Operativ bruk av simulatorene

### 11.1 Lukkede topologiske tester

Bruk dette når du vil teste eksakt bevaring av \(K\) og \(\beta_1\):

```bash
python relational_universe_sim_energy.py \
  --closed \
  --check-exact \
  --w-tokens 1 \
  --w-beta1 1 \
  --w-stress 0 \
  --out closed_energy.csv
```

Tolkning:

- ingen fri cycle creation/deletion,
- ingen token birth/death,
- edge-swaps + seeds dominerer,
- \(E = K + \beta_1\) bør være eksakt konstant.

### 11.2 Åpne metastabile regimer

Bruk dette når du vil se om \(\beta_1\) er quasi-bevart i forventning:

```bash
python relational_universe_sim_energy.py \
  --steps 200000 \
  --p-triad 0.10 \
  --p-del 0.10 \
  --w-tokens 1 \
  --w-beta1 1 \
  --w-stress 0 \
  --out open_energy.csv
```

Tolkning:

- fri syklusproduksjon og syklustap er tillatt,
- eksakt bevaring forsvinner,
- liten netto drift tyder på emergent balanse.

### 11.3 Lokal kontinuitetstest

```bash
python relational_universe_sim_energy.py \
  --steps 50000 \
  --local-radius 3 \
  --out local_tokens.csv
```

Da skal `region_residual` være null dersom bokføringen er korrekt.

---

## 12. Forskningsprogram: hva som følger herfra

### 12.1 Neste matematiske trinn

Den naturlige fortsettelsen er å utvide feature-settet fra

\[
(K,N,M,C)
\]

til noe rikere, f.eks.

\[
F=(K,N,M,C,T,\chi_4,\ldots),
\]

der:

- \(T\) = antall triangler,
- \(\chi_4\) = teller for utvalgte 4-noders motiver,
- eventuelt spektrale størrelser.

Deretter kan man søke etter:

1. eksakte lineære invariants,
2. nær-nullretninger i forventet drift,
3. makroregimer med liten drift og lav sensitivitet.

### 12.2 Fysisk ønskelige egenskaper

En lovende mikroteori bør kunne gi:

- metastabile loops/klustre,
- begrenset propagasjonshastighet,
- stor robust sammenhengende komponent,
- lokal kontinuitet,
- ett eller flere quasi-konserverte makrovariabler.

### 12.3 Når modellen blir fysisk interessant

Modellen begynner å nærme seg fysikk når den kan gi:

- en enkel regelklasse,
- få frie parametere,
- robuste makroregimer,
- testbare påstander om hvilke observabler som bør være universelle.

---

## 13. Stram dom over prosjektets nåværende status

Det intellektuelt sterkeste ved modellen er ikke at den allerede forklarer alt, men at den begynner å få **selektive restriksjoner**:

- ikke alle lokale rewrites er like gode,
- noen regelklasser tillater energilignende stabilitet,
- andre ødelegger den umiddelbart.

Dermed er prosjektet allerede forbi ren metafor. Det er ikke ennå en fysisk teori, men det er en **kontrollerbar teori-skisse**.

Den mest lovende presise tesen akkurat nå er:

> Et stabilt, bakgrunnsløst univers med emergent spacetime og energilignende makrolover krever en mikrodynamikk der loop-charge enten er eksakt topologisk beskyttet eller statistisk nær-balansert.

Det er en tese man faktisk kan simulere, falsifisere og raffinere.

---

## 14. Bundle: filer i denne pakken

| Fil | Formål |
|---|---|
| `relasjonell_universgraf_avhandling.md` | Hoveddokumentet |
| `README_relational_universe_bundle.md` | Kort introduksjon til hele pakken |
| `codex_meta_prompt_for_prompt_generation.md` | Meta-prompt for å få Codex til å skrive gode prompts til kodeassistenter |
| `codex_prompt_simulator_bruk_og_tolkning.md` | Direkte prompt for å få en kodeassistent til å bruke simulatorene faglig riktig |
| `codex_prompt_refaktorering_rule_engine.md` | Direkte prompt for refaktorering til regelmotor |
| `codex_prompt_invariantanalyse.md` | Ekstra prompt for nullroms- og invariantanalyse |
| `relational_universe_sim.py` | Minimal simulator |
| `relational_universe_sim_energy.py` | Utvidet simulator med energi- og kontinuitetsdiagnostikk |

---

## 15. Ordliste og forklaringer

### Action-bærer / token
En teknisk representasjon av en unit of action i simulatoren. Ontologisk er token ikke en ny substans, men en måte å gjøre lokal action simulerbar på.

### Attractor
Et område i tilstandsrommet som dynamikken tenderer mot og blir i.

### Bakgrunnsløs
En teori er bakgrunnsløs når den ikke forutsetter et ferdig rom eller en ferdig tid som scene for dynamikken.

### Betti-tall
Topologisk størrelse som teller uavhengige hull eller sykler. For grafer er første Betti-tall \(\beta_1\) antall uavhengige loops.

### Bridge / bro-kant
En kant hvis fjerning øker antall sammenhengskomponenter.

### Clustering coefficient
Mål på hvor tett en nodes naboer er koblet sammen. Høy clustering betyr mange trekanter / lokal loopdannelse.

### Continuous-time / SSA / Gillespie
Asynkron stokastisk simulering der hendelser skjer med rater i kontinuerlig tid, i stedet for med en global diskret klokke.

### Cycle rank
Et annet navn på første Betti-tall for en graf.

### Emergent
Noe er emergent når det ikke er fundamentalt lagt inn, men oppstår robust på makronivå fra mikrodynamikken.

### Entanglement
I denne modellen: korrelasjon og felles constraint-struktur, ikke en kanal for fri superluminal signalering.

### Exact invariant
En størrelse som er uforandret under hver tillatt mikroskopisk regelanvendelse.

### Feature-vektor
En valgt liste av observerbare størrelser, f.eks. \((K,N,M,C)\), som brukes for å analysere dynamikken.

### Gillespie-algoritme
Standard metode for stokastisk simulering av hendelser i kontinuerlig tid.

### Invariant
En størrelse som ikke endres under dynamikken.

### Kausal kjegle
Mengden hendelser eller noder som kan påvirkes fra et gitt utgangspunkt under den lokale dynamikken etter et gitt antall steg eller innen en gitt tid.

### Leaf
Node av grad 1, altså en node med bare én relasjon.

### Lineær invariant
En invariant som kan skrives som lineær kombinasjon av features, f.eks. \(aK+bN+cM+dC\).

### Makroregime
Et robust stor-skala-mønster som kan beskrives med grovkornede variabler.

### Metastabil
Stabil over lange, men ikke nødvendigvis uendelige, tider.

### Nullrom
Mengden av koeffisientvektorer som gir null når de ganges med regelmatrisen; her er det rommet av lineære invariants.

### Pruning
Fjerning av isolerte noder som ikke lenger har relasjoner.

### Quasi-konservering
Ikke eksakt bevaring, men liten eller ingen netto drift i et stabilt regime.

### Rewire / edge-swap
Lokal omkobling av relasjoner uten at antall kanter nødvendigvis endres.

### Seed
Ny node eller ny mikroskopisk struktur som oppstår og eventuelt kobles inn i en eksisterende komponent.

### Spacetime-regime
Det emergente makrolaget der grafen fremstår geometrisk og relativistisk nok til å tolkes som romtid.

### Stoikiometrisk vektor
En endringsvektor som beskriver hvordan én regel endrer utvalgte features.

### Stress-energi
En diagnostisk funksjon som måler hvor langt gradfordelingen ligger fra et valgt referansenivå.

### Topologisk sektor
En regelklasse der bestemte topologiske størrelser, som \(\beta_1\), er eksakt eller nesten eksakt bevart.

---

## 16. Kort sluttord

Prosjektet står nå i en god fase. Det er fortsatt spekulativt, men ikke lenger formløst. Det finnes allerede en klar matematisk struktur som begynner å sile bort dårlige antagelser. Det er nettopp dette som må skje dersom en metafysisk idé skal vokse til en fysikalsk teori.
