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
curl -fsS https://emergentuniverse.haven.digipomps.org/data/latest_causal_structure/v17k_effect_blind_compound_matched_work_start_memory.md | head
```

The manifest source revision must match the deployed repository revision. The
page must distinguish the fresh v16s full-spectrum contrast, the v16t
realized-effort diagnosis, the v16u exact matched-effort pass, the v16v
independent global-construction feasibility/diversity result, and the v16w
representation/objective qualification failure. It must also report the v16x
integer-measure representation repair, exact-conflict state-space collapse and
frozen endpoint-concentration failure. It must also report the v16y local
reversibility/mobility passes, the failed start-family stability gate, and the
`0/6` concentration-profile result without calling start separation proof of
disconnected components. It must report the v16z exact pair-specific cycle
coverage/replay `6/6`, bounded bridges `0/6`, `98.1521-99.6892%` mismatch
reduction, preserved formal raw-key representation failure, and post-run
edge-move covariance `6/6` without turning the audit into a retroactive pass.
It must also report the v17a frozen-start/representation passes `12/12`, exact
reverse-support and pathwise-balance passes `84/84`, resource pass `24/24`,
finite-movement failure `0/24`, and post-run displacement range
`0.010632-0.030656`. These are proposal diagnostics, not global mixing or
source-effect evidence.
It must report the v17b frozen-start/representation passes `12/12`, exact
reverse-support and pathwise-balance passes `36/36`, matched valid-yield and
finite-movement passes `24/24`, median valid-yield ratio `2.898276`, resource
pass only `12/24`, and runtime range `27.479260-270.449001`. The v17b repair is
finite movement with an unqualified runtime, not convergence, mixing, source-
effect or physics evidence. The Bell methods report must remain a conceptual
claim boundary and must not imply that the repo has performed a Bell test.
It must report the v17c exact count/support parity `36/36`, exact v17b
transition trace/summary replay `24/24`, representation `12/12`, reverse support
and pathwise balance `36/36`, movement/resource `24/24`, maximum runtime
`14.921836`, and median v17c/v17b runtime ratio `0.161356`. This qualifies an
exact finite implementation for effect-blind stability testing; it does not
establish convergence, mixing, start independence, source-effect survival or
physics.
It must report the v17d integrity `384/384`, traversal/resource `24/24`,
endpoint-center result `85/108`, endpoint-distance agreement `12/18`,
residual-component centers `90/90`, and proposal-footprint overlap `18/18`.
All six distance failures are start-family contrasts. Exact residual-profile
identity across representative endpoints is matching algebra, not proof of
bounded-cycle state-graph connectivity. The source spectrum remains closed.
It must report the v17e matched-prefix replay `192/192`, integrity `384/384`,
reversibility `36/36`, representation `12/12`, traversal/resource `24/24`,
maximum runtime `107.676262`, and material cross-start contraction `0/6` with
ratios `0.978973-1.005348`. It must explain that within-start dispersion grew
`1.385802-1.470668`; the lower cross/within ratio is not absolute cross-start
convergence. Further scale growth of the length-2-to-4 kernel is retired, but
global disconnection and failure of other move classes are not claimed.
It must report the v17f frozen-start/final-integrity results `12/12` and
`24/24`, reverse/batch/one-step-novelty/representation results `12/12`, finite
length-5 exercise and resource `24/24`, minimum accepted length-5 moves `7`,
and maximum runtime `22.681378`. It must preserve formal movement `15/24` and
the `11/720` reverse-unsupported valid raw auxiliaries. The post-run result that
all `11/11` explicit reverse paths were structurally valid and a diagnostic 10x
ceiling recovered `9/11` localizes bounded-search support asymmetry; it does not
retroactively pass v17f, qualify a larger budget, or establish connectivity.
It must report v17g raw-generation/event parity `24576/24576`, exact identity
of the same `11` filtered auxiliaries, accepted-transition/final-endpoint and
retained-support results `24/24`, pathwise witness/representation `12/12`,
movement/resource `24/24`, minimum retained valid proposals `130`, and maximum
runtime `20.456393`. It must state that this qualifies the finite proposal law
without adding accepted dynamics, convergence, connectivity or mixing evidence.
It must report v17h exact accepted work/endpoint integrity/reverse support/
movement/resource `48/48`, expanded length-5 exercise `24/24`, primary
material cross-start reduction `0/6`, ratio range `0.980433-1.013939`, median
ratio `1.003301`, and directional reduction `3/6`. It must disclose that the
symmetric exact-work terminal rule is finite conditioning and may add a small
endpoint bias. The fixed 50/50 length-5 expansion is retired as a uniform
start-memory remedy; all larger moves, connectivity, mixing and the model are
not rejected by this result.
It must report v17i pair-basis/single-block accessibility `6/6`, complement
identity `96/96`, endpoint integrity `192/192`, finite distance response `6/6`
and ratio range `0.986207-1.004213`. It must state that the basis was derived
from both starts and is an engineered positive control, not a state-independent
proposal, source null, connectivity/mixing result or physical signal.
It must report v17j retained compound paths `554`, accepted blocks `152`, exact
reverse/involution/balance/integrity `554/554`, compound exercise/movement/
resource/endpoints `24/24`, representation `12/12`, and per-source
qualification `6/6`. It must state that v17j qualifies a finite
anchor-independent proposal law, not global connectivity, irreducibility,
mixing, convergence, stationary sampling, source-effect survival or physics.
It must report v17k exact gross work/proposal/movement/exercise/resource
`48/48`, work `192`, directional compound reduction `4/6`, material reduction
`0/6`, ratio range `0.991307-1.003176`, and median `0.995490`. It must keep
gross and net work separate and state that the result retires only the exact
two-subcycle net-6 law as a uniform finite start-memory remedy. It does not
prove disconnection, failed mixing, absent source effects, or failure of all
large moves.
It must separate these from
sampler qualification/mixing/uniformity and physical
interpretation, and state that Lorentz-like
behavior, universal invariants, particle species, spacetime, and a completed
universe model have not been established.

Static deployment does not update the dynamic RAG index. Run the tracked sync
orchestrator separately, then issue a token-scoped query about v17k and require
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
