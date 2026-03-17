# Codex-prompt: resolve `bridge_0015_0000` vs `band_zero_del` after v0.11b

You are working inside the `UniverseSimulation` repository as a local research engineering assistant.

Your job is to inspect the code and files on disk, determine the live project state, implement the next narrow experiment, and report what the repository actually supports.

## Ground rule

Use the files on disk as ground truth.
Do not assume that older bundles, earlier assistant summaries, or prior winners are still active if newer local runs disagree.
If the prompt summary below conflicts with the on-disk evidence, follow the files and say so explicitly.

## Active context

Relevant files now include:

- `relational_universe_v11b_bridge_resolution.py`
- `Documentation/v11b_bridge_resolution.md`
- `Documentation/v11b_bridge_resolution_hypothesis_check.csv`
- `Documentation/v11b_bridge_resolution_broad_candidate_summary.csv`
- `Documentation/v11b_bridge_resolution_final_candidate_summary.csv`
- `Documentation/v11b_bridge_resolution_final_pairwise.csv`
- `Documentation/v0_11b_operativ_anbefaling.md`

## Working hypothesis to verify

The repo state appears to support the following reading:

- older v0.11 files did support a shift from the old `bridge_0025_0000` / swap tension toward a bridge corridor,
- but the new narrow v0.11b run changed the local leader to `bridge_0015_0000`,
- and the real live contest is now between `bridge_0015_0000` and `band_zero_del`,
- while the old swap-tilted bridge candidate no longer looks like the main issue.

Treat this as a claim to verify from the files, not as an axiom.
If the repo evidence disagrees, report the disagreement plainly.

## Task

Design and implement the next very narrow iteration, called something like:

- `relational_universe_v11c_binary_bridge_vs_band.py`

The purpose is to answer a tighter question than before:

Is `bridge_0015_0000` actually better than `band_zero_del`, or is the current edge just finite-sample / scoring noise?

## Required work

### 1. Narrow the candidate set further

Build a very small candidate family centered on:

- `band_zero_del`
- `bridge_0015_0000`

Add only a few nearby bridge perturbations, for example:

- one smaller-triad bridge point near `0.0010-0.0015`
- one larger-triad bridge point near `0.0020-0.0025`

Keep the grid small and interpretable.

Do not reopen a broad `p_del` search unless the local evidence forces it.

### 2. Treat swap as optional diagnostic only

If you include a swap-tilted bridge point at all, it should be a diagnostic control, not the center of the experiment.
The repo currently does not support treating swap as the main frontier unless the new run shows otherwise.

### 3. Push replication up slightly

Use more replication than v0.11b if practical, but keep the experiment narrow enough to finish locally.
The goal is not breadth; the goal is to decide whether the `bridge_0015_0000` edge over `band_zero_del` is real.

### 4. Separate these questions explicitly

Your report must answer separately:

1. Which candidate has the highest raw `mean_composite`?
2. Which candidate has the strongest `CI low`?
3. Which candidate wins pairwise bootstrap comparison most often?
4. Are these the same candidate?
5. If not, is the result still unresolved?

### 5. Allow an unresolved answer

If `bridge_0015_0000` and `band_zero_del` remain too close to call, say so plainly.
Do not force a winner just because one candidate leads on one summary metric.

### 6. Keep the interpretation disciplined

Distinguish clearly between:

- generator stability,
- scoring artifacts,
- finite-sample ambiguity,
- and robust dynamical advantage.

Do not call the outcome resolved unless the local evidence actually supports that.

## Constraints

- Keep four size levels so the v0.9b-style asymptotic diagnostics remain valid.
- Prefer a tiny, interpretable grid over a larger exploratory scan.
- Document everything in Markdown.
- Use the repository state, not prompt rhetoric, as the authority.

## Deliverables

- the new v0.11c script
- CSV outputs
- technical Markdown report
- short lay summary
- operational recommendation

## Desired outcome

At the end of this iteration, the repo should answer one question more clearly:

Should the project carry forward `bridge_0015_0000`, `band_zero_del`, or both?

If the answer is still "both", say that directly and explain exactly why.
