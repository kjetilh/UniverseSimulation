# Emergent Universe public site runbook

## Mandatory per-round closure

Every completed research round must be committed and pushed, then published to
both this static archive and the separate UniverseSimulation RAG corpus. The
round is not `published` until the live manifest revision matches the pushed
commit, a new HTTPS artifact is readable, and a real token-scoped RAG query
passes citation and freshness audits. See
`Documentation/Research_Round_Closure_Policy.md`.

If one publication surface is unavailable, report `publication_blocked`; do
not infer static-site freshness from RAG freshness or vice versa.

## Purpose

`emergentuniverse.haven.digipomps.org` publishes a static, scientific-style
snapshot of the UniverseSimulation project for public reading and data download.
The site is intentionally conservative: it separates theory, implemented
experiments, generated artifacts, and interpretation boundaries.

## Build

Build the static bundle from the repository root:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/pycache-emergent \
  python3 Tools/build_emergentuniverse_public_site.py \
  --out /tmp/emergentuniverse_public
```

The bundle contains:

- `index.html`
- `assets/site.css`
- `data/manifest.json`
- `data/manifest.csv`
- curated Markdown and CSV artifacts under `data/<category>/`
- `robots.txt`
- `README.md`

The manifest records source path, public path, byte count, and SHA-256 digest for
every copied artifact, plus the source Git revision. The public manifest must
not expose a developer-local filesystem path.

## RAG boundary

The repository contains a UniverseSimulation-specific RAG service under
`rag_service/`. The public site does not expose that dynamic service, admin UI,
or API endpoints. RAG corpus notes are published only as static documentation.

Expose a public RAG endpoint only after a separate hardening pass covers:

- authentication and rate limiting
- corpus freshness policy
- citation auditing
- prompt/output claim boundaries
- no admin or ingestion endpoints on the public host

The first implementation target for that hardening is the token-scoped
`/v1/research/*` surface in `rag_service/`, not the open local developer
endpoints under `/v1/query` and `/v1/chat`. See
`rag_service/docs/RAG_SERVICE_API.md` for the current research hardening
settings.

Production deployments should use `RESEARCH_RATE_LIMIT_BACKEND=postgres` after
running `python -m scripts.apply_migrations`. The in-memory limiter is only a
local/dev fallback and must not be treated as enough for public traffic.

Before any dynamic RAG endpoint is routed from the public host, verify a
loopback-only or staging instance with the dedicated hardening smoke:

```bash
cd rag_service
RESEARCH_API_TOKEN='<token>' \
RESEARCH_BASE_URL='http://127.0.0.1:8000' \
RESEARCH_EXPECTED_RATE_LIMIT_BACKEND=postgres \
python -m scripts.research_hardening_smoke \
  --case-id universe_project
```

The smoke must prove that anonymous research access is rejected, token-scoped
case listing works, `/v1/research/query` emits `research_hardening` with
`rate_limit.backend=postgres`, citation audit and freshness metadata are
present, and the bearer token is not echoed in response JSON. Do not expose
dynamic RAG publicly from a run that only used `--skip-query`; that option is
for auth/case diagnostics, not production readiness.

## Deployment target

The staging VPS already hosts `staging.haven.digipomps.org` and related nginx
server blocks. This site is deployed as static files on the same server.

Suggested docroot:

```text
/var/www/emergentuniverse
```

Suggested nginx host:

```text
emergentuniverse.haven.digipomps.org
```

The tracked deployed nginx config is:

```text
ops/emergentuniverse_nginx.conf
```

## Verification

After deployment, verify at minimum:

```bash
curl -fsS https://emergentuniverse.haven.digipomps.org/ | grep -E "Emergent Universe|Interpretation boundary"
curl -fsS https://emergentuniverse.haven.digipomps.org/data/manifest.json | head
curl -fsS https://emergentuniverse.haven.digipomps.org/data/latest_causal_structure/v16w_interpretation_audit.md | head
```

The manifest source revision must match the deployed repository revision. The
page must distinguish the fresh v16s full-spectrum contrast, the v16t
realized-effort diagnosis, the v16u exact matched-effort pass, the v16v
independent global-construction feasibility/diversity result, and the v16w
representation/objective qualification failure. It must separate these from
sampler qualification/mixing/uniformity and physical
interpretation, and state that Lorentz-like
behavior, universal invariants, particle species, spacetime, and a completed
universe model have not been established.

Static deployment does not update the dynamic RAG index. Run the tracked sync
orchestrator separately, then issue a token-scoped query about v16w and require
current citations plus freshness metadata. See
`rag_service/docs/UNIVERSE_TOOL_RUNBOOK.md`.

## Loopback-only production RAG

The server-side Universe instance is intentionally separate from the existing
Innovasjon and DiMy RAG deployments. Its tracked compose definition is:

```text
ops/emergentuniverse_rag_compose.yml
```

The API binds only to `127.0.0.1:8103`. Keep its real environment file outside
Git, mode `0600`, and use `ops/emergentuniverse_rag.env.example` only as a
schema. The compose deployment mounts `rag_service/app`, `scripts`, `config`,
and `prompts` read-only from a revision-locked UniverseSimulation checkout.

For a first deployment only, provision isolated secrets from the existing
provider configuration without printing them:

```bash
ops/provision_emergentuniverse_rag_env.sh
```

The provisioner refuses to overwrite an existing environment. Subsequent
deployments reuse the existing file and operator token.

After updating the checkout and mirroring the corpus, start or refresh it with:

```bash
docker compose \
  --env-file /srv/ops/universe_rag/.env \
  -f /srv/ops/repos/UniverseSimulation/ops/emergentuniverse_rag_compose.yml \
  up -d
```

Do not add an nginx route for this service until the public exposure gate in
the RAG boundary section has been satisfied independently.
