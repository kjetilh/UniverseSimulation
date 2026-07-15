# UniverseSimulation agent workflow

Files on disk are ground truth. Do not fabricate runtime results or upgrade a
heuristic, generator check, or finite simulation result into a physics claim.

## Mandatory research-round closure

After every completed research round:

1. Write the result, raw/aggregate evidence, claim limits, and next decision to
   the tracked documentation before declaring the round complete.
2. Run the relevant verification and preserve preregistration or source hashes.
3. Commit the intended repository changes and push the active branch.
4. Build the public archive from the pushed commit, deploy it to
   `emergentuniverse.haven.digipomps.org`, and verify that the live manifest
   revision equals the pushed commit.
5. Sync the dedicated UniverseSimulation RAG corpus separately and run a real
   token-scoped query that passes authentication, citation-audit, rate-limit,
   and freshness checks.
6. Report any failed step as blocked. A local commit, successful static deploy,
   or successful RAG sync does not imply that the other closure steps passed.

See `Documentation/Research_Round_Closure_Policy.md` and
`Documentation/EmergentUniverse_Public_Site_Runbook.md` for the durable
verification contract.
