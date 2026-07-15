# Research round closure policy

Effective date: 2026-07-15

## Purpose

Every completed UniverseSimulation research round must leave one consistent,
auditable state across the repository, the public scientific archive, and the
dedicated retrieval corpus. This policy prevents local results from outranking
published evidence and prevents a current static page from being mistaken for
a current RAG index.

## Required closure gates

A round is `published` only when all of these gates pass:

| Gate | Required evidence |
|---|---|
| Research integrity | Runtime products came from a real run, or unexecuted work is explicitly marked as a proposal; algebra, generator artifacts, scores, dynamics, and inference remain separated. |
| Repository | Intended files pass relevant tests and integrity checks, are committed, and the commit is pushed to the active remote branch. |
| Static archive | The public bundle is built from that commit; its manifest records the same full source revision and contains the new public artifacts without developer-local paths or secrets. |
| Live HTTPS | The landing page, manifest, and at least one new round artifact are fetched successfully from `https://emergentuniverse.haven.digipomps.org/`. |
| Dynamic RAG | The corpus sync plan is reviewed, the sync completes without errors, and a real token-scoped query passes authentication, PostgreSQL rate-limit, citation-audit, and freshness checks. |
| Final report | The user receives the commit, pushed branch, tests, live revision, RAG status, scientific result, and explicit evidential limits. |

Static publication and RAG publication are independent gates. Neither may be
inferred from the other.

## Failure handling

If a gate cannot pass, preserve valid research outputs and commit/push them when
safe, but report the round as `publication_blocked` with the exact failed gate.
Do not fabricate a deployment, live response, citation count, or freshness
result. Retry only after the blocking condition changes.

## Scientific boundary

Publication means that evidence is available and traceable. It does not make a
finite result universal, turn a null-procedure check into physics, or establish
energy, temperature, invariants, particles, Lorentz symmetry, spacetime, or a
universe model beyond the claims supported by that round.
