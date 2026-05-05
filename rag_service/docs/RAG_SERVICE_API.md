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


### Nar bruke `/v1/admin/catalog/publish`

Bruk `catalog.publish` for strukturerte CellProtocol/CellScaffold chunks som
allerede er ferdig segmentert av en celle, for eksempel
`ServiceCatalogCell.ragChunks`.

Endepunkter:

- `POST /v1/admin/catalog/publish`
- `POST /v1/admin/catalog/reindex`
- `GET /v1/admin/catalog/status`

Dette er ikke en erstatning for filbasert sync. Det er en eksplisitt,
admin-beskyttet RAG-katalogkontrakt for dokumentasjonschunks med metadata som
`repo`, `serviceID`, `cell`, `contract` og `status`.

### Nar bruke `/v1/admin/media/publish`

Bruk `media.publish` nar en CellProtocol-klient skal levere et dokument eller
en mediafil som bytes over JSON. V1 stotter bare:

- `delivery.mode = inlineBase64`
- maks 2 MB
- `.md`, `.markdown`, `.txt`, `.html`, `.htm`, `.pdf`, `.docx`

Ikke send ra `ValueType.data` som ekstern wire-kontrakt. Bruk eksplisitt
`bytes_base64`, `sha256`, `mime_type`, `filename` og `size_bytes`, slik at
payloaden kan valideres deterministisk pa begge sider.
