# UniverseSimulation Tool Runbook

Dette dokumentet beskriver hvordan dagens verktøy faktisk brukes.

## Verktøy som finnes na

### 1. Toy-simulatoren

Fil:

- `../relational_universe_sim.py`

Den implementerer:

- en dynamisk urettet graf
- mobile tokens som lokal handlingsmekanisme
- seed attachment
- triadic closure
- lokal rewire
- Gillespie-lignende stokastisk tidsutvikling

### 2. Baseline-data

Fil:

- `../trajectory.csv`

Denne gir et eksisterende eksempel pa hvordan default-parametrene oppforer seg over tid.

### 3. RAG-tjenesten

Mappe:

- `rag_service/`

Den gir:

- query/chat-endepunkter
- research-endepunkter for lesende klienter
- admin-synk og admin-rebuild
- promptprofiler per case

## Kjor simulatoren

Fra repo-roten:

```bash
python3 relational_universe_sim.py --steps 2000 --log-every 500 --out ''
```

For full parameteroversikt:

```bash
python3 relational_universe_sim.py --help
```

Viktigste parametere:

- `--r-token`
  - hvor ofte tokens handler
- `--r-seed`
  - hvor ofte nye noder kobles inn
- `--p-del`
  - sannsynlighet for a slette traversert kant
- `--p-triad`
  - sannsynlighet for triadic closure
- `--p-rewire`
  - sannsynlighet for lokal rewire
- `--r-birth` og `--r-death`
  - valgfri token-fodsel og token-dod
- `--log-every`
  - hvor ofte metrics logges

## Tolk outputen

Kolonnene i `trajectory.csv` betyr:

- `event`
  - antall hendelser som er gjennomfort
- `time`
  - intern kontinuerlig tid fra SSA
- `nodes`
  - antall noder i grafen
- `edges`
  - antall kanter
- `tokens`
  - antall aktive tokens
- `avg_degree`
  - gjennomsnittlig grad
- `clustering`
  - lokal trekanttendens
- `eff_dim`
  - en grov volumvekstproxy, ikke en full spektral dimensjon

## Hvordan bruke simulatoren til hypotesetesting

Det dagens kode er best egnet til:

- se om en stor komponent vedvarer
- se om lokal klustring bygges opp
- se om default-dynamikken runaway-densifiserer
- sammenligne parameterregimer med enkle makrometrikker

Det den ikke er best egnet til enn:

- streng testing av rapportens DPO-regler
- direkte maaling av `beta_1` eller andre invariants
- robust Lorentz-diagnostikk
- endelig "fysikkbevis"

## Start RAG-tjenesten lokalt

Fra `rag_service/`:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
python -m pip install -e '.[pdf,html,docx]'
cp .env.example .env
docker compose -f docker/docker-compose.yml up -d db
python -m scripts.rebuild_index
uvicorn app.main:app --reload --port 8000
```

## Last inn korpuset uten a flytte kildefiler

Bruk `sync_folder`, ikke `ingest_folder`, nar kildene ligger i repoet og skal bli liggende der.

Kjor fra `rag_service/`:

```bash
python -m scripts.sync_folder --path ../Documentation/grundig-research-rapport-16.md --source-type universe_argumentation --ingest-root .. --dry-run
python -m scripts.sync_folder --path ../README.md --source-type universe_status --ingest-root .. --dry-run
python -m scripts.sync_folder --path docs/UNIVERSE_RAG_STATUS.md --source-type universe_status --ingest-root .. --dry-run
python -m scripts.sync_folder --path docs/UNIVERSE_TOOL_RUNBOOK.md --source-type universe_tools --ingest-root .. --dry-run
python -m scripts.sync_folder --path docs/UNIVERSE_ARGUMENTATION_MAP.md --source-type universe_argumentation --ingest-root .. --dry-run
python -m scripts.sync_folder --path prompts --source-type universe_prompts --ingest-root .. --dry-run
```

Nar dry-run ser riktig ut, kjor de samme kommandoene uten `--dry-run`.

## Hvorfor ikke bruke ingest_folder direkte pa repo-filer

`ingest_folder` flytter ferdig prosesserte filer til `done/` eller `failed/`.

Det er riktig nar du jobber mot en opplastingsmappe under `uploads/`, men feil nar du vil bevare prosjektets egne kildedokumenter pa plass.

## Anbefalt arbeidsflyt

1. bruk simulatoren for a generere eller tolke data
2. dokumenter status, tolkning og hypoteser i `rag_service/docs/`
3. oppdater promptprofilene i `rag_service/prompts/` nar du ser at modeller trenger tydeligere styring
4. synk endrede docs/prompts inn i RAG-en med `sync_folder`
5. bruk `universe_project`, `universe_tools`, `universe_argumentation` eller `universe_prompts` avhengig av sporsmalstypen
