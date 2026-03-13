# rag-service (FastAPI + PostgreSQL/pgvector)

Prosjektspesifikk RAG-tjeneste for `UniverseSimulation`.

Formalet er ikke bare generell dokument-RAG, men en eksplisitt kunnskapsbase for:

- prosjektstatus og faktisk implementert tilstand
- forskningsargumentasjonen i `Documentation/grundig-research-rapport-16.md`
- hvordan dagens simulator og tilhorende verktøy brukes
- prompts og instruksjoner til språkmodeller som skal jobbe med prosjektet

## Cases i denne instansen

- `universe_project`: kombinert prosjektassistent
- `universe_tools`: bruk av simulator, RAG og arbeidsflyt
- `universe_argumentation`: ontologi, regelsett, bevaringsideer og testprogram
- `universe_prompts`: promptdesign og modellinstruksjoner for prosjektet

## Viktigste prosjektfiler

- hovedrapport: `../Documentation/grundig-research-rapport-16.md`
- simulator: `../relational_universe_sim.py`
- baseline-data: `../trajectory.csv`
- prosjektdocs for RAG: `docs/`
- promptprofiler: `prompts/`
- case-oppsett: `config/rag_cases.yml`

## Dokumentasjon i denne mappen

Se `docs/README.md`. Viktigste filer er:

- `docs/UNIVERSE_RAG_STATUS.md`
- `docs/UNIVERSE_ARGUMENTATION_MAP.md`
- `docs/UNIVERSE_TOOL_RUNBOOK.md`
- `docs/UNIVERSE_CORPUS_PLAN.md`
- `docs/UNIVERSE_DEEP_RESEARCH_PROMPT.md`
- `docs/RAG_SERVICE_API.md`

## Lokal kjøring

### 1. Opprett venv og installer avhengigheter

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
python -m pip install -e '.[pdf,html,docx]'
```

Valgfritt for embeddings/reranking:

```bash
python -m pip install -e '.[emb]'
```

### 2. Klargjor miljo

```bash
cp .env.example .env
```

Sett minst:

- `LLM_API_KEY`
- `ADMIN_API_KEY`
- `DATABASE_URL=postgresql+psycopg://rag:rag@localhost:5432/ragdb`

### 3. Start database

```bash
docker compose -f docker/docker-compose.yml up -d db
```

### 4. Opprett schema/indexer

```bash
python -m scripts.rebuild_index
```

### 5. Synk prosjektkorpuset inn i RAG-en

Bruk `sync_folder`, ikke `ingest_folder`, for repo-filer du vil beholde pa plass.

Eksempler fra `rag_service/`:

```bash
python -m scripts.sync_folder --path ../Documentation/grundig-research-rapport-16.md --source-type universe_argumentation --ingest-root ..
python -m scripts.sync_folder --path ../README.md --source-type universe_status --ingest-root ..
python -m scripts.sync_folder --path docs/UNIVERSE_RAG_STATUS.md --source-type universe_status --ingest-root ..
python -m scripts.sync_folder --path docs/UNIVERSE_TOOL_RUNBOOK.md --source-type universe_tools --ingest-root ..
python -m scripts.sync_folder --path docs/UNIVERSE_ARGUMENTATION_MAP.md --source-type universe_argumentation --ingest-root ..
python -m scripts.sync_folder --path prompts --source-type universe_prompts --ingest-root ..
```

Bruk `--dry-run` forst hvis du vil se hva som vil skje.

### 6. Start API

```bash
uvicorn app.main:app --reload --port 8000
```

### 7. Verifiser helse

```bash
curl http://localhost:8000/health
```

### 8. Eksempelsporringer

```bash
curl -X POST http://localhost:8000/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "universe_project",
    "query": "Hvor er prosjektet na, og hva er gapet mellom rapporten og simulatoren?"
  }'
```

```bash
curl -X POST http://localhost:8000/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "universe_argumentation",
    "query": "Hvordan begrunner rapporten at energi kan formaliseres som aktivitetsrate, invariants og mønsterenergi?"
  }'
```

```bash
curl -X POST http://localhost:8000/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "universe_tools",
    "query": "Hvordan bør jeg bruke dagens simulator for a teste metastabilitet og runaway densifisering?"
  }'
```

## Docker kjøring

```bash
cp .env.example .env
docker compose -f docker/docker-compose.yml up -d --build
curl http://localhost:8000/health
```

Docker-instansen mapper `uploads/` til `/data/uploads`.

For admin-batch-ingest i Docker ma filer ligge under `uploads/`.
For repo-filer og dokumenter du vil la ligge i ro, bruk i stedet `sync_folder.py` lokalt eller tilpass `config/sync_orchestrator.example.toml`.

## Hva denne instansen ikke later som

- Den later ikke som dagens toy-simulator er identisk med rapportens formelle DPO/CTMC-modell.
- Den later ikke som `trajectory.csv` er bevis for emergent romtid eller Lorentz-lik symmetri.
- Den skal skille mellom:
  - rapportens formelle ramme
  - faktisk implementert kode
  - observerte kjoredata
  - inferens og videre forslag
