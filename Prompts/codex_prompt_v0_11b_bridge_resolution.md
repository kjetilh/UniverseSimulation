# Codex-prompt: resolve the bridge corridor after focused v0.11

You are working in `UniverseSimulation`.

## Ground rule

Use the files on disk as ground truth. Do not assume older bundle conclusions still hold if newer local runs disagree.

## Active context

Relevant files now include:

- `relational_universe_v11_frontier_resolution.py`
- `Documentation/v11_dedicated_min_frontier_resolution.md`
- `Documentation/v11_mid_focus_frontier_resolution.md`
- `Documentation/v11_mid_focus_frontier_resolution_broad_candidate_summary.csv`
- `Documentation/v11_mid_focus_frontier_resolution_final_candidate_summary.csv`
- `Documentation/v11_mid_focus_frontier_resolution_final_pairwise.csv`
- `Documentation/v11_mid_focus_codex_assessment.md`

## Current state

The local project state has moved beyond `band_zero_del` as the default winner.

In the focused local v0.11 run:

- `bridge_0025_0000` is the raw winner
- `bridge_0025_0000_swap025` is the focused-score winner
- `band_zero_del` loses to `bridge_0025_0000` pairwise
- `bridge_0025_0000` beats both `band_zero_del` and `bridge_0025_0000_swap025` pairwise in the final focused run

This means the live frontier is now the bridge corridor, not the old band corridor.

## Task

Design and implement the next narrow iteration, call it something like:

- `relational_universe_v11b_bridge_resolution.py`

The purpose is to resolve whether the swap-tilted bridge variant is genuinely better or whether it is mostly a focused-score / regularization artifact.

## Required work

### 1. Narrow the candidate set to the bridge corridor

Build a small candidate family around:

- `bridge_0025_0000`
- `bridge_0025_0000_swap025`
- `band_zero_del` as control

Plus a few nearby bridge points, for example by varying:

- `p_triad` around `0.0025`
- `p_swap` around `0.020-0.025`
- keep `p_del = 0` in the main branch unless there is a clear reason to reopen it

Do not fall back to a wide frontier scan.

### 2. Separate raw and focused interpretations

Be explicit about the difference between:

- raw dynamical strength (`mean_composite`, pairwise win probability, CI low),
- and focused-score advantage.

If a candidate wins focused-score but clearly loses raw pairwise comparison, say so plainly.

### 3. Make the scoring tension visible

Add reporting that explicitly shows:

- raw winner
- focused winner
- pairwise matrix among finalists
- a note on whether the focused winner is still operationally credible

### 4. Run a somewhat deeper local experiment

Use more replication than the minimal smoke round, but keep it targeted enough to finish in practice.

The goal is not maximal breadth. The goal is to resolve the bridge corridor cleanly.

### 5. Report what changed from v0.11 mid focus

The report must explicitly answer:

1. Is `bridge_0025_0000` still the best operational default?
2. Does `bridge_0025_0000_swap025` retain any meaningful advantage?
3. Is that advantage raw-dynamical or just focused/regularized?
4. Does `band_zero_del` remain useful only as a control?

## Constraints

- Keep using four size levels so the v0.9b-style asymptotic diagnostics remain valid.
- Do not oversell focused-score wins if they are not supported by raw pairwise outcomes.
- Document everything in Markdown.
- Prefer a small, interpretable candidate grid over a large diffuse scan.

## Deliverables

- the new bridge-resolution script
- CSV outputs
- technical Markdown report
- short lay summary
- operational recommendation

## Desired outcome

At the end of this iteration, the repo should have a cleaner answer to this question:

Is the right standard candidate now simply `bridge_0025_0000`, or is there a real reason to carry a swap-tilted bridge variant forward as more than a diagnostic control?
