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

## Endpoint quantities: two measured references before any gate

Adopted from `Documentation/v17_program_closure.md` section 7, where it was
written as the rule that should be here and then was not, for a fortnight.

> A primary endpoint quantity shall have a MEASURED null reference and a
> MEASURED positive reference before it is used as a gate. Missing either, the
> round is an instrumentation round and does not count as a test of the
> hypothesis.

This is R7 applied to observables instead of to data sources. It would have
stopped the v17 series after round four: v17d had a working instrument and the
series left it for seven more rounds on a ratio already shown to be determined
by the start pair.

Two consequences that are not optional:

- **A statistic that cannot separate its own two references gates nothing.**
  Change the statistic, not the threshold.
- **A gain that survives no transform-invariant test is not a finding.** Every
  monotone transform of a positive observable has the same sign vector, so a
  weighted statistic can climb a long way on zero new directional evidence --
  measured on 2026-09-08 as 2.64 to 3.44 on a holdout with the sign vector
  bit-for-bit unchanged. Report a sign test, or an equivalent invariant test,
  beside any weighted statistic used to rank candidates.

`Tools/nodegraph/purpose.py` implements all three refusals; a `PurposeContract`
without both references refuses to gate at all. `Tools/nodegraph/INSTRUKSJONER.md`
is the operating manual. Nothing in `Tools/nodegraph/` is a physics claim, and a
result from it enters the v-series only by the closure procedure above.
