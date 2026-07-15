# v16t realized-effort interpretation audit

Date: 2026-07-15

## Why this audit is required

The frozen v16t gate executed correctly under its preregistered code and
criteria. All `384/384` perturbations passed integrity, and all `18/18`
null-center comparisons passed the frozen ratio threshold. The source spectra
and observed-effect metrics remained excluded.

Post-run inspection of the sampler audit exposed a design-level semantic
problem: target swap multipliers were not the same as realized chain lengths.
The shared requirement to keep sampling until at least `10%` of source edges
were changed dominated all three direct stopping rules.

## Realized effort

| protocol | mean accepted swaps | minimum | maximum | mean nominal target |
| --- | ---: | ---: | ---: | ---: |
| direct short `0.075` | 993.145833 | 618 | 1493 | 269.333333 |
| direct reference `0.100` | 1005.020833 | 682 | 1729 | 358.500000 |
| direct long `0.200` | 998.343750 | 714 | 1370 | 716.500000 |
| staged `0.100 + 0.100` | 2023.343750 | 1399 | 2966 | 717.000000 |

The three direct protocols therefore did not create materially distinct
realized chain lengths. Their stable centers are valid seed/protocol
diagnostics, but they do not establish chain-length stability.

The staged protocol performed about twice as many accepted swaps as the direct
long protocol. Its comparison therefore combines path segmentation with extra
realized effort. It cannot isolate path segmentation at matched chain length.

## Corrected interpretation

The frozen machine status
`v16t_footprint_null_centers_stable_across_tested_paths` is retained as a record
of the preregistered gate. The correct scientific interpretation is narrower:

`v16t_center_stability_observed_but_length_path_decomposition_inconclusive`.

V16t shows that the effect-blind null centers remained inside the frozen
stability region across multiple independent seeds and across roughly one
versus two thousand accepted swaps. It does not separately establish direct
chain-length stability or path-segmentation stability.

This audit does not inspect or alter the v16s observed effect. It also does not
establish irreducibility, mixing, convergence, stationarity,
representativeness, uniformity, concrete-resource independence, dimension,
Lorentz symmetry, spacetime, particles, entanglement, invariants, or physical
law.

## Required repair

The next gate must decouple burn-in/change qualification from realized chain
length:

1. reach the existing `10%` changed-edge burn-in without computing source
   spectra;
2. branch from that frozen burn-in state;
3. advance branches by exact, matched accepted-swap increments;
4. compare burn-in, `+K`, and `+2K` centers for realized-length stability;
5. compare direct `+2K` with segmented `+K + K` at exactly matched accepted
   effort;
6. retain the `2.0` center-shift-ratio threshold and all-source-DAG pass rule;
7. compute no observed/source spectrum or effect ratio.

Only after this corrected gate passes should the project move to an
independently constructed null family.
