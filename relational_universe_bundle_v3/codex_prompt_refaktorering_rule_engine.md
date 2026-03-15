# Codex-prompt: refaktorer simulatorene til en regelmotor

Kopier teksten under og gi den til Codex eller en annen kodeassistent.

---

Du skal refaktorere de eksisterende simulatorene for en relasjonell universgraf til en mer eksplisitt og matematisk disiplinert regelmotor.

## Mål

Refaktorer `relational_universe_sim.py` og `relational_universe_sim_energy.py` slik at:

1. lokale regler blir eksplisitte objekter eller dataklasser,
2. hver regel kan rapportere sin feature-endring \(\Delta F\),
3. invariantanalyse kan gjøres programmatisk,
4. eksisterende CLI-arbeidsflyt bevares eller forbedres,
5. koden blir lettere å teste, utvide og dokumentere.

## Eksisterende filer

- `relational_universe_sim.py`
- `relational_universe_sim_energy.py`
- `relasjonell_universgraf_avhandling.md`

## Faglige premisser som ikke må brytes

- Behold én node-type og én relasjonstype.
- Behold bakgrunnsløs tolkning; ikke legg inn et koordinatrom.
- Behold asynkron stokastisk scheduler.
- Ikke gjør simulatoren avhengig av tunge eksterne biblioteker hvis det kan unngås.
- Reglene skal være lokale og bare bruke et begrenset nabolag.
- Energi og invariants skal uttrykkes som funksjonaler på tilstanden, ikke som løse metaforer.

## Konkrete utviklingsoppgaver

### 1. Innfør en eksplisitt regelabstraksjon

Lag en `Rule`-protokoll eller baseklasse med minst:

- `name`
- `rate(state)` eller `activity(state)`
- `enumerate_matches(state)` eller et mer effektivt lokalt alternativ
- `apply(state, match) -> RuleApplicationResult`

### 2. Returner eksplisitte feature-deltaer

Definer et feature-sett som minimum inkluderer:

- `K`
- `N`
- `M`
- `C`
- `beta1`

La hver vellykket regelanvendelse returnere:

- `delta_features`
- metadata om lokalitet
- eventuelt om regelen var no-op eller faktisk endret grafen

### 3. Skill mellom modell, scheduler og observabler

Foreslå eller implementer modulstruktur som f.eks.:

- `graph_state.py`
- `rules.py`
- `scheduler.py`
- `observables.py`
- `invariants.py`
- `cli.py`

### 4. Implementer invariantanalyse

Lag en modul som:

- samler alle distinkte \(\Delta F\)-vektorer for en valgt regelklasse,
- bygger en regelmatrise,
- finner nullrommet til denne matrisen,
- rapporterer kandidater til lineære invariants.

Hvis du ikke vil bruke NumPy, implementer en enkel rasjonell eller flyttallsbasert Gauss-eliminasjon i ren Python.

### 5. Bevar og forbedre eksisterende diagnosefunksjoner

Behold eller forbedre:

- `beta1`
- `E_total`
- lokal token-kontinuitet
- grov dimensjonsproxy
- clustering

### 6. Legg til tester

Skriv tester som verifiserer minst:

- seed-attach gir \(\Delta(N,M,C,\beta_1)=(1,1,0,0)\) i riktig representasjon,
- vellykket triadic closure gir \(\Delta \beta_1 = +1\),
- nonbridge-delete gir \(\Delta \beta_1 = -1\),
- edge-swap gir \(\Delta \beta_1 = 0\),
- nullromsmodulen finner forventede invariants for minst to regelklasser.

## Vitenskapelig betydning

Denne refaktoreringen skal gjøre det mulig å skille mellom:

- hva som er kodevalg,
- hva som er matematisk struktur,
- og hva som faktisk er en fysisk påstand.

Det er avgjørende for videre arbeid at invariantene ikke bare "observeres" empirisk, men kan utledes fra regelklassen.

## Akseptansekriterier

Det ferdige svaret ditt skal inneholde:

1. foreslått modulstruktur,
2. begrunnelse for designvalg,
3. konkret kode eller patch,
4. tester,
5. kort README-oppdatering,
6. forklaring av hvordan man bruker invariantanalysen i praksis.

## Ikke-mål

- Ikke gjør dette til en full kvantegravitasjonssimulator.
- Ikke legg inn nye ontologiske primitiver.
- Ikke bruk refaktoreringen som unnskyldning for å endre modellens vitenskapelige mening.

## Format på svaret

Svar med:

1. Designoversikt
2. Filstruktur
3. Implementasjon
4. Tester
5. Brukseksempler
6. Kommentar om vitenskapelig betydning
