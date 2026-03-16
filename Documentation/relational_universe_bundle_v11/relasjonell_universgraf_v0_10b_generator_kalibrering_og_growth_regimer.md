# Relasjonell universgraf v0.10b–v0.10d: generator-kalibrering, nytt growth-regime og kalibrert skalarerun

## Hva dette steget gjør

Dette steget behandler et spesifikt metodisk problem som ble tydelig etter v0.9b:
de nominelle store naturlige ensemblene var ikke reelt store. Dermed kunne store
negative eller ekstreme skalerings-eksponenter like gjerne være generatorartefakter
som dynamiske funn.

Jeg har derfor delt arbeidet i tre sammenhengende deler:

1. **v0.10b**: kalibrering av dagens naturlige ensemble-generator.
2. **v0.10c**: design og test av alternative growth-regimer dersom kalibrering ikke er nok.
3. **v0.10d**: en fokusert ny skalarunde bare på ensemble-regimer som faktisk gir separerte størrelser.

## Ground truth og aktiv kodebase

Brukerens prompt refererte til en `relational_universe_v10_scale_collapse.py`, men den filen
finnes ikke i aktivt arbeidsområde her. Derfor er dette steget eksplisitt bygget direkte på
filene som faktisk finnes på disk:

- `relational_universe_v09_scale_and_natural_ensembles.py`
- `relational_universe_v09b_asymptotic_refinement.py`
- `relational_universe_v08b_natural_ensemble_robustness.py`
- `relational_universe_local_max_coupling_lab.py`

Dette er viktig, fordi hele poenget her er å skille mellom **faktisk aktiv kode** og antatt historisk kontekst.

## v0.10b: kalibrering av dagens generator

Jeg kalibrerte to varianter av dagens generator:

- `baseline`: fast burn-in og ekstra burn-in, i praksis samme logikk som tidligere.
- `adaptive`: samme mikrodynamikk, men med en enkel kontrollsløyfe som forsøker å stoppe på et in-band snapshot.

Resultatet er klart: de store nominelle nivåene kollapser fortsatt i praksis.

| method | burnin | target | realized_mean | q10 | q90 | abs_rel_err | hit_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| adaptive | deep | 24 | 24.0 | 23.2 | 24.8 | 0.042 | 1.00 |
| adaptive | deep | 48 | 44.0 | 43.2 | 44.8 | 0.083 | 1.00 |
| adaptive | deep | 96 | 86.0 | 85.2 | 86.8 | 0.104 | 0.50 |
| adaptive | deep | 192 | 96.5 | 95.3 | 97.7 | 0.497 | 0.00 |
| adaptive | deep | 256 | 103.0 | 100.6 | 105.4 | 0.598 | 0.00 |
| adaptive | light | 24 | 22.0 | 21.2 | 22.8 | 0.083 | 1.00 |
| adaptive | light | 48 | 44.0 | 43.2 | 44.8 | 0.083 | 1.00 |
| adaptive | light | 96 | 77.5 | 69.9 | 85.1 | 0.193 | 0.50 |
| adaptive | light | 192 | 88.5 | 87.3 | 89.7 | 0.539 | 0.00 |
| adaptive | light | 256 | 95.5 | 91.9 | 99.1 | 0.627 | 0.00 |
| baseline | deep | 24 | 32.5 | 30.5 | 34.5 | 0.354 | 0.00 |
| baseline | deep | 48 | 52.5 | 51.3 | 53.7 | 0.094 | 0.50 |
| baseline | deep | 96 | 87.0 | 75.8 | 98.2 | 0.146 | 0.50 |
| baseline | deep | 192 | 101.5 | 100.3 | 102.7 | 0.471 | 0.00 |
| baseline | deep | 256 | 115.5 | 114.3 | 116.7 | 0.549 | 0.00 |
| baseline | light | 24 | 26.5 | 26.1 | 26.9 | 0.104 | 0.50 |
| baseline | light | 48 | 42.5 | 40.5 | 44.5 | 0.115 | 0.50 |
| baseline | light | 96 | 71.5 | 62.3 | 80.7 | 0.255 | 0.00 |
| baseline | light | 192 | 86.0 | 84.4 | 87.6 | 0.552 | 0.00 |
| baseline | light | 256 | 103.0 | 102.2 | 103.8 | 0.598 | 0.00 |

### Tolkning av v0.10b

De små og moderate nivåene (`24`, `48`, delvis `96`) kan fortsatt brukes som naturlige starttilstander.
Men de store nominelle nivåene er **ikke troverdige** under dagens generator:

- `adaptive / deep / 192` realiserer i snitt bare `96.5` noder.
- `adaptive / deep / 256` realiserer i snitt bare `103.0` noder.
- `baseline / deep / 256` realiserer i snitt bare `115.5` noder.

Dette er ikke en subtil avvikseffekt. Det er et generatorproblem.

### Hvilke nivåer er operativt brukbare under dagens generator?

- `adaptive` / `deep`: 24,48,96,192,256
- `adaptive` / `light`: 24,48,96,192,256
- `baseline` / `deep`: 24,48,96,192,256
- `baseline` / `light`: 24,48,96,192,256

Denne listen må leses med forsiktighet:
et nivå kan være **statistisk separert** fra naboen og likevel være **metodisk ubrukelig**
fordi det ikke lenger tilsvarer sin nominelle størrelse. For eksempel er `192` og `256`
adskilt som realiserte fordelinger under dagens generator, men de ligger begge i et altfor lite realisert område.
De er derfor uegnet som basis for fysisk tolkning av storskalaeksponenter.

Mer nyttig som faktisk arbeidsregel er et strengere operativt kriterium:
- nivået må være statistisk separert fra forrige nivå, **og**
- mean relativ størrelsesfeil må være ≤ 0.15.

Da får vi:
- `baseline` / `light`: 24,48
- `baseline` / `deep`: 48,96
- `adaptive` / `light`: 24,48
- `adaptive` / `deep`: 24,48,96

## v0.10c: nytt growth-regime

Siden v0.10b viste at kalibrering av dagens regime ikke var nok, laget jeg et alternativt growth-spor.
Dette er viktig å si presist:

- De nye growth-regimene er **generatorer for startensembler**.
- De er **ikke** påstander om at selve universdynamikken er erstattet.
- De brukes for å teste om de senere dynamiske resultatene overlever når startstørrelsene faktisk er reelle.

Jeg testet tre generatorregimer:

- `fast_ref`
- `fast_balanced`
- `fast_push`

De bruker fortsatt lokale operasjoner (seed-vekst, token-move, triad closure, swap, token-birth/death, leaf-pruning),
men uten den tunge full-CTMC-enumerasjonen som gjorde referansegeneratoren treg og størrelsesblind.

### Sammenligning av growth-regimer

| regime | mean_abs_rel_err | hit_rate | naturalness | composite |
| --- | --- | --- | --- | --- |
| fast_ref | 0.000 | 1.00 | 0.485 | 0.871 |
| fast_push | 0.038 | 0.83 | 0.420 | 0.662 |
| fast_balanced | 0.043 | 0.79 | 0.509 | 0.654 |

Hvis vi ser bare på **deep-variantene**, som er mest relevante for videre bruk:

| deep-regime | mean_abs_rel_err | hit_rate | naturalness | composite |
| --- | --- | --- | --- | --- |
| fast_balanced | 0.000 | 1.00 | 0.514 | 0.878 |
| fast_ref | 0.000 | 1.00 | 0.485 | 0.871 |
| fast_push | 0.000 | 1.00 | 0.410 | 0.852 |

### Hvordan skal dette leses?

- `fast_ref` er best på ren størrelse-treff. Den treffer målnivåene nærmest perfekt.
- `fast_balanced` er litt svakere samlet over både light og deep, men i **deep-regimet** er den best på den kombinerte vurderingen fordi den balanserer størrelse-treff og struktur bedre.
- `fast_push` gir store og separerte ensembler, men ser mer aggressiv og mindre strukturbevarende ut.

### Anbefalt regime videre

Den operativt beste anbefalingen videre er:

**Bruk `fast_balanced` i deep-variant som standard ensemble-regime for videre storskalaanalyse.**

Begrunnelse:

1. Den gir reelt separerte størrelser ved `48`, `96`, `192`, `256`.
2. Den treffer målstørrelsene presist i deep-varianten.
3. Den ligger nærmere den tidligere “naturlige” strukturprofilen enn `fast_push`.
4. Den virker mindre sterilt kalibrert enn `fast_ref`, som scorer litt lavere på naturalness-proxy.

Dette er ikke et endelig fysikk-utsagn. Det er en **generatoranbefaling**.

## v0.10d: kalibrert skalarerun

Når et fungerende growth-regime var på plass, reran jeg tre fokuskandidater:

- `band_best`
- `macro_stable`
- `balanced_pdel` (kontroll)

med bare ensemble-nivåer som faktisk var reelt separerte:
`48`, `96`, `192`, `256`, alle i `fast_balanced / deep`.

### Kandidatsammendrag

| candidate | mean_composite | repair | causal | quasi | geom | alpha_large | alpha_jump | linear_margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| band_best | 0.601 | 0.681 | 0.491 | 0.680 | 0.518 | 0.291 | -0.028 | -0.046 |
| balanced_pdel | 0.551 | 0.532 | 0.568 | 0.582 | 0.530 | -0.023 | -0.339 | 0.254 |
| macro_stable | 0.434 | 0.312 | 0.445 | 0.483 | 0.585 | 0.108 | -0.089 | 0.097 |

### Størrelsesprofiler

| candidate | target | initial_N | radius | overlap | quasi | composite |
| --- | --- | --- | --- | --- | --- | --- |
| balanced_pdel | 48 | 48.0 | 4.00 | 0.656 | 0.854 | 0.831 |
| balanced_pdel | 96 | 96.0 | 8.00 | 0.322 | 0.522 | 0.351 |
| balanced_pdel | 192 | 192.0 | 8.00 | 0.572 | 0.535 | 0.480 |
| balanced_pdel | 256 | 256.0 | 7.75 | 0.525 | 0.417 | 0.541 |
| band_best | 48 | 48.0 | 4.75 | 0.665 | 0.911 | 0.826 |
| band_best | 96 | 96.0 | 6.75 | 0.486 | 0.794 | 0.593 |
| band_best | 192 | 192.0 | 6.75 | 0.554 | 0.535 | 0.536 |
| band_best | 256 | 256.0 | 10.00 | 0.462 | 0.481 | 0.448 |
| macro_stable | 48 | 48.0 | 6.00 | 0.574 | 0.883 | 0.704 |
| macro_stable | 96 | 96.0 | 8.00 | 0.394 | 0.409 | 0.378 |
| macro_stable | 192 | 192.0 | 8.00 | 0.426 | 0.224 | 0.305 |
| macro_stable | 256 | 256.0 | 9.25 | 0.436 | 0.418 | 0.350 |

## Hva v0.10d betyr

Dette er hovedpoenget:

- `band_best` **holder seg som beste kandidat** når startstørrelsene faktisk er reelle.
- De ekstreme eller “umulige” negative eksponentene som var mistenkelige under generatorproblemet er i stor grad borte.
- Vi får fortsatt ikke perfekt, ren sublineær vekst; men vi får en langt mer troverdig situasjon der kandidatene kan sammenlignes uten å være dominert av ensemblekollaps.

Mer konkret:

- `band_best`: `alpha_large ≈ 0.291`, `alpha_jump ≈ -0.028`
- `macro_stable`: `alpha_large ≈ 0.108`, `alpha_jump ≈ -0.089`
- `balanced_pdel`: `alpha_large ≈ -0.023`, `alpha_jump ≈ -0.339`

Det betyr at den tidligere typen **store, svært negative eksponenter** ikke lenger er det dominerende bildet når ensemble-generatoren er reparert.
Én kandidat (`balanced_pdel`) viser fortsatt svak negativ stor-skala-tendens, men nå ser det ut som en dynamisk egenskap ved kandidaten,
ikke bare en generatorfeil.

## Svar på de åtte spørsmålene i prompten

### 1. Hvilke nominelle størrelser var faktisk oppnåelige?

Under dagens referansegenerator:
- `24` og `48`: ja
- `96`: delvis / marginalt
- `192` og `256`: nei, ikke som nominelle nivåer

Under anbefalt nytt regime (`fast_balanced`, deep):
- `48`, `96`, `192`, `256`: ja

### 2. Hvilke størrelsesnivåer kollapset til samme realiserte område?

Under dagens generator kollapset særlig:
- `192` og `256` ned mot omtrent `90–115` realiserte noder,
avhengig av variant.

### 3. Hjalp adaptiv kalibrering?

Bare delvis.
Den hjalp for små og moderate nivåer, men reddet ikke de store nivåene.

### 4. Trengte vi et nytt growth-regime?

Ja.
Det er den ærlige konklusjonen av v0.10b.

### 5. Hvilket ensemble-regime bør brukes videre?

**`fast_balanced`, deep-variant.**

### 6. Holder `band_best` seg som beste kandidat når skalaene blir reelt separert?

Ja.
I v0.10d er `band_best` fortsatt best på mean composite.

### 7. Forsvinner de ekstreme eller negative eksponentene når generatorproblemet reduseres?

Ja, i stor grad.
De mest mistenkelige ekstreme/negative eksponentene forsvinner som dominerende bilde.
Det gjenstår mild negativitet for én kontrollkandidat, men ikke som generell effekt.

### 8. Hvilke konklusjoner er algebraiske eller metodiske, og hvilke er dynamiske/fysiske?

**Metodiske / generatorrelaterte konklusjoner**
- Store deler av v0.9b/v0.10-problemet skyldtes ensemble-generatoren.
- Nominal target size og realized initial size må holdes eksplisitt adskilt.
- “Asymptotikk” uten reelt separerte nivåer er ikke metodisk forsvarlig.

**Dynamiske konklusjoner**
- `band_best` overlever overgangen til kalibrerte ensembler.
- `macro_stable` er fortsatt roligere, men svakere totalt.
- `balanced_pdel` ser mer ut som kontroll enn vinner i denne runden.

**Ikke-konklusjoner**
- Dette er fortsatt ikke en bekreftet fysisk teori.
- Growth-regimet er ennå en generatorløsning, ikke en avledet fundamental lov.

## Samlet dom

Prosjektet går fortsatt i en lovende retning, men på en mye mer metodisk streng måte enn før.

Det mest oppmuntrende ved dette steget er ikke at resultatene “ble bedre”.
Det mest oppmuntrende er at prosjektet nå **kan skille mellom**:

- algebraiske identiteter,
- generatorartefakter,
- og dynamiske kandidatforskjeller.

Det er akkurat den typen innsnevring man vil se i en tidlig forskningskodebase.

## Neste riktige steg

Det neste riktige steget er **v0.10e / v0.11**:

1. bruke `fast_balanced / deep` som standard ensemble-regime,
2. øke antall growth seeds og run seeds moderat,
3. kjøre et nytt, smalt kandidatsett (`band_best`, en eller to utfordrere, og én kontroll),
4. og undersøke om `band_best` fortsatt holder seg når vi går til flere reelt separerte størrelser og mer robust bootstrap.

Det ville være det første steget som virkelig begynner å ligne en moden kandidatseleksjon heller enn bare generatorreparasjon.
