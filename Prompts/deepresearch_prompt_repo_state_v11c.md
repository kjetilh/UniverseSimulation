You are doing a research synthesis for the `UniverseSimulation` project.

Important:
- You are not executing code locally.
- Treat the repository-derived findings below as current ground truth unless they are internally inconsistent.
- Do not overwrite local runtime findings with speculation.
- Separate clearly between:
  - algebraic identities,
  - generator / ensemble artifacts,
  - scoring artifacts,
  - and dynamical simulation results.

## Goal

Write a research-grade synthesis of:

1. where the project is now,
2. how it got there,
3. what has actually been found so far,
4. what outside literature is genuinely relevant,
5. and what the best next research question is.

## Ground truth from the local repo

Start with these two files as the shortest local context:

- `PROJECT_CONTEXT_LIVE.md`
- `PROJECT_HISTORY_INDEX.md`

Then use the files below as the active evidence base.

### Current live frontier state

The older `v11b` story is not the newest local frontier state.
A newer local run `v11c` exists and should be treated as more authoritative than `v11b` if they differ.

### v11c result

A narrow local `p_triad` axis was tested at fixed:

- `p_swap = 0.02`
- `p_del = 0.0`

Candidates:

- `band_zero_del`
- `bridge_0005_0000`
- `bridge_0010_0000`
- `bridge_0015_0000`
- `bridge_0020_0000`

Local result:

- `bridge_0010_0000` is now the robust winner on operational metrics.
- It wins:
  - raw `mean_composite`
  - `CI low`
  - pairwise bootstrap
- `P(bridge_0010_0000 > band_zero_del) = 0.942`
- `band_zero_del` still has the best focused/local score
- therefore focused-score and operational metrics are now clearly split
- `bridge_0015_0000` is no longer the best bridge point
- swap does not appear to be the center of the frontier anymore

### Generator state

The local reading is that the earlier generator-size problem has largely been cleaned up in the active regime.
In the newer calibrated / focused runs, the real starting size levels are separated cleanly, so recent frontier conclusions look more dynamical than generator-driven.

### Current operational local recommendation

- carry forward `bridge_0010_0000` as the standard candidate
- do not treat `band_zero_del` as the operational winner just because it wins focused-score

## Relevant repo-derived files

Treat these as the key local artifacts to reason from:

- `PROJECT_CONTEXT_LIVE.md`
- `PROJECT_HISTORY_INDEX.md`
- `Documentation/v10d_calibrated_scale_candidate_summary.csv`
- `Documentation/v10d_calibrated_scale_size_profiles.csv`
- `Documentation/v10e_focused_band_candidate_summary.csv`
- `Documentation/v10e_focused_band_pairwise.csv`
- `Documentation/v10e_focused_band_size_profiles.csv`
- `Documentation/v10f_frontier_final_candidate_summary.csv`
- `Documentation/v10f_frontier_final_pairwise.csv`
- `Documentation/v10f_frontier_final_size_profiles.csv`
- `Documentation/v11b_bridge_resolution.md`
- `Documentation/v11b_bridge_resolution_final_candidate_summary.csv`
- `Documentation/v11b_bridge_resolution_final_pairwise.csv`
- `Documentation/v11c_binary_bridge_vs_band.md`
- `Documentation/v11c_binary_bridge_vs_band_candidate_summary.csv`
- `Documentation/v11c_binary_bridge_vs_band_pairwise.csv`
- `Documentation/v11c_binary_bridge_vs_band_target_summary.csv`
- `Documentation/v11c_binary_bridge_vs_band_verdict.csv`

## What you should produce

Please produce these sections:

### 1. Current state

Give a precise, repo-loyal summary of the current project state.

### 2. How the frontier moved

Explain the methodological and empirical path:

- generator calibration
- focused frontier narrowing
- bridge-corridor emergence
- binary bridge-vs-band refinement
- why `bridge_0010_0000` is now the best-supported operational candidate

### 3. What has really been found

Be explicit about:

- what is robust
- what is only provisional
- what was overturned by newer local files
- what remains unproven

### 4. External relevance

Identify the most relevant outside research areas and explain why they are relevant:

- stochastic graph rewriting / graph grammars
- interacting particle systems / coupling / propagation bounds
- dynamic random graphs / rewiring
- emergent spacetime analogies
- graph dimension / curvature / coarse geometry
- metastability / quasi-invariants / finite-size scaling

Be careful:

- analogies are not confirmations
- do not imply that existing theories already validate this project
- say clearly when a comparison is only heuristic

### 5. Best next research question

Recommend the single best next narrow local experiment, given the current repo state.

## Constraints

- Do not claim you executed code.
- Do not pretend older summaries outrank newer local artifacts.
- Do not promote focused-score over raw/CI/pairwise unless you can justify it.
- Be comfortable saying that some claims are still weak or only suggestive.
- Prefer a sharp, disciplined synthesis over a broad speculative essay.

## Desired tone

Write like a careful research analyst:

- precise
- skeptical
- constructive
- explicit about evidential status
