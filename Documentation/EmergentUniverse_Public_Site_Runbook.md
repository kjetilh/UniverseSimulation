# Emergent Universe public site runbook

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
every copied artifact.

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
curl -fsS https://emergentuniverse.haven.digipomps.org/data/latest_taxonomy/v15dq_active_set_taxonomy_synthesis.md | head
```

The page must state that Lorentz-like behavior, universal invariants, particle
species, and a completed universe model have not been established.
