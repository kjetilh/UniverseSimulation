# v16y interpretation audit

Frozen overall status: `v16y_2x2_chain_finite_centers_not_stable`.

## What passed

- endpoint integrity and effect exclusion: `192/192`, with source-spectrum and observed-effect calls `0/0`
- exact frozen v16x reference replay: `192/192`
- tested detailed-balance witnesses: `48/48`
- replay, candidate-order and semantic-relabel representation checks: `6/6`
- finite chain mobility: `24/24`
- independent chain-seed and early/late-window center rows: `84/84`

The algebraic result is limited to detailed balance for the implemented lazy Metropolis transitions. The stationary target is uniform only inside each connected component of the valid 2x2-switch graph. The finite diagnostics do not prove that the sampled chains reached that target.

## What failed

Center stability passed only `102/126`. All `24` failures were start-family comparisons: `source_edge_fraction`, `concrete_conflict_fraction`, `mean_candidate_rank_fraction`, and `log_neighbor_degree` failed on every one of the six sources. No seed-family or early/late-window comparison failed.

The concentration-profile comparison passed on `0/6` sources against the preregistered requirement of at least `4/6`. The chain maximum inclusion rate for a globally variable edge was `1.000` on all six sources. Mean variable-edge binary entropy was lower than the v16x random-cost reference on all six, and variable-union coverage retained only `0.354176-0.405145` of the reference coverage.

## Post-run diagnosis

The frozen endpoint table shows that each chain moved only about eight percent away from its own start under the 512-step budget. The post-run audit gives mean pairwise changed-edge fractions of `0.422373` across starts, versus `0.078443` within the source start and `0.078510` within the random-cost start. It also finds `460-548` globally variable edges included in every one of the 32 pooled chain endpoints per source.

This is strong finite evidence of start-dependent accessibility under the current move class and budget. It is consistent with either slow traversal or distinct 2x2 accessibility components. It does **not** prove disconnection, because no complete reachability argument was executed. See `v16y_postrun_start_separation_audit.md` and `v16y_postrun_start_separation_audit.csv`.

No source spectrum or observed-effect statistic was computed. V16y therefore neither reproduces nor refutes the v16s effect and establishes no global uniformity, maximum entropy, canonical null, energy, temperature, invariant, dimension, Lorentz symmetry, spacetime, particle or entanglement claim.
