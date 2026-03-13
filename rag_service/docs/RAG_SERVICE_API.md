# UniverseSimulation RAG Service API

Dette er en praktisk oversikt over de viktigste endepunktene i denne instansen.

## Helse

- `GET /health`

## Vanlige sporringer

- `POST /v1/query`
- `POST /v1/chat`
- `POST /v1/chat/stream`

Bruk `case_id` for a velge en av disse:

- `universe_project`
- `universe_tools`
- `universe_argumentation`
- `universe_prompts`

## Research-endepunkter

For lesende klienter som ikke skal ha admin-tilgang:

- `GET /v1/research/cases`
- `POST /v1/research/query`
- `GET /v1/research/cases/{case_id}/corpus`
- `GET /v1/research/cases/{case_id}/links`
- `GET /v1/research/cases/{case_id}/documents/{doc_id}/links`
- `GET /v1/research/documents/{doc_id}/download`

## Admin-endepunkter

Krever `X-API-Key`.

- `POST /v1/admin/rebuild`
- `POST /v1/admin/ingest`
- `POST /v1/admin/sync`
- `GET /v1/admin/coverage-report`
- `GET /v1/admin/coverage-actions`
- `GET /v1/admin/prompt-config`
- `PUT /v1/admin/prompt-config`

## Praktiske regler

### Nar bruke `/v1/query`

Bruk `/v1/query` for vanlige prosjektsporsmal der du vil ha et svar med kilder.

### Nar bruke `/v1/research/query`

Bruk research-API-et nar klienten skal:

- velge case eksplisitt
- browse korpus
- laste ned kildefiler
- holde lesetilgang adskilt fra admin-tilgang

### Nar bruke `/v1/admin/sync`

Bruk `sync` for repo-filer og dokumenter som skal bli liggende pa plass.

### Nar bruke `/v1/admin/ingest`

Bruk `ingest` for drop-foldere under `uploads/` der det er riktig at filer flyttes til `done/` eller `failed/`.
