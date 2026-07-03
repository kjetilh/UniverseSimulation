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

Krever `Authorization: Bearer <token>` fra `RESEARCH_API_TOKENS_JSON`.
`access_token` i query string er deaktivert som default fordi slike tokens lett
havner i logger og nettleserhistorikk. Signerte nedlastingslenker bruker egne
`exp`/`sig`/`cases`-parametre og er fortsatt korte, avgrensede grants.

### Research hardening

`/v1/research/query` legger `research_hardening` inn i `retrieval_debug`:

- `auth`: token-label, token-fingeravtrykk, scopes og om tokenet er case-scoped
- `rate_limit`: brukt/igjen innen gjeldende minuttvindu
- `citation_audit`: antall citations, unike dokumenter og eventuelle brudd
- `freshness`: aktivt dokumentantall, tombstone-pending og corpus-alder

Default policy:

- `RESEARCH_ALLOW_QUERY_ACCESS_TOKEN=false`
- `RESEARCH_RATE_LIMIT_BACKEND=memory`
- `RESEARCH_RATE_LIMIT_PER_MINUTE=60`
- `RESEARCH_RATE_LIMIT_BURST=120`
- `RESEARCH_MIN_CITATIONS=2`
- `RESEARCH_MIN_UNIQUE_DOCS=1`
- `RESEARCH_ENFORCE_RESPONSE_AUDIT=true`
- `RESEARCH_FRESHNESS_MAX_AGE_SECONDS=0`
- `RESEARCH_ENFORCE_FRESHNESS=false`

`RESEARCH_ENFORCE_FRESHNESS=false` betyr at freshness rapporteres, men ikke
blokkerer svar. Sett `RESEARCH_FRESHNESS_MAX_AGE_SECONDS` og
`RESEARCH_ENFORCE_FRESHNESS=true` for en public deployment der stale corpus skal
feile lukket.

For produksjon med flere workers eller flere instanser skal
`RESEARCH_RATE_LIMIT_BACKEND=postgres` brukes. Den backenden bruker tabellen
`rag_research_rate_limits`, opprettet av migrasjonen
`app/rag/index/migrations/0001_research_rate_limits.sql`, og gir delt
rate-limit state på tvers av prosesser. Kjør `python -m scripts.apply_migrations`
eller `python -m scripts.rebuild_index` før research-API-et startes med denne
backenden.

For `emergentuniverse.haven.digipomps.org` bor dynamisk RAG ikke eksponeres for
allmennheten for denne policyen er konfigurert og verifisert mot live corpus.

### Produksjons-smoke for research-hardening

For staging eller en loopback-only produksjonskandidat, kjør først migrasjoner
og start API-et med minst:

```bash
RESEARCH_API_TOKENS_JSON='{"<token>":{"label":"staging-smoke","scopes":["research:read"],"case_ids":["universe_project"]}}'
RESEARCH_DOWNLOAD_SIGNING_KEY='<long-random-secret>'
RESEARCH_RATE_LIMIT_BACKEND=postgres
RESEARCH_ENFORCE_RESPONSE_AUDIT=true
```

Deretter kjører du smoke-skriptet fra `rag_service/`:

```bash
RESEARCH_API_TOKEN='<token>' \
RESEARCH_BASE_URL='http://127.0.0.1:8000' \
RESEARCH_EXPECTED_RATE_LIMIT_BACKEND=postgres \
python -m scripts.research_hardening_smoke \
  --case-id universe_project
```

Smoken feiler hvis anonym research-tilgang ikke avvises, tokenet ikke kan se
`case_id`, `/v1/research/query` mangler `retrieval_debug.research_hardening`,
rate-limit backenden ikke er `postgres`, eller bearer-tokenet lekker tilbake i
JSON-svaret. Bruk `--skip-query` bare for en smal auth/case-sjekk; den er ikke
tilstrekkelig for å eksponere dynamisk RAG. Bruk `--allow-audit-fail-closed`
når målet er å bekrefte at citation/freshness-policyen stopper svake svar,
ikke når målet er å bekrefte en fungerende public query-opplevelse.

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
