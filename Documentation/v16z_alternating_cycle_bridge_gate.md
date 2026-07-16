# v16z alternating-cycle bridge gate

Status: `v16z_cycle_representation_not_qualified`.

## Evidential status

This gate is effect-blind. It reuses the six frozen v16x/v16y coarse state spaces and the same source/random-cost start pairs. No source spectrum or observed-effect statistic is computed.

The alternating-cycle rows are exact finite combinatorial witnesses between each declared start pair. They qualify pair-specific whole-cycle exchanges, not a state-independent stochastic proposal and not a global probability law.

The 2x2 search is bounded at `2048` path steps and `2048` expanded states per pair, with plateau depth `3` and beam `16`. Failure to find a path is `unresolved`, never proof of disconnected components.

## Source results

| growth_seed | run_offset | pair_changed_selected_edge_fraction | cycle_count | maximum_cycle_changed_edge_count | whole_cycle_reversibility_pass | bridge_status | bridge_steps | bridge_final_mismatch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 0.443495 | 347 | 152 | 1 | unresolved_no_admissible_progress | 1292 | 5 |
| 9299 | 123403 | 0.393677 | 345 | 104 | 1 | unresolved_no_admissible_progress | 1064 | 26 |
| 9299 | 127341 | 0.414420 | 359 | 152 | 1 | unresolved_no_admissible_progress | 1107 | 11 |
| 9365 | 123078 | 0.447435 | 361 | 134 | 1 | unresolved_no_admissible_progress | 1237 | 23 |
| 9365 | 123403 | 0.394562 | 384 | 78 | 1 | unresolved_no_admissible_progress | 1039 | 18 |
| 9365 | 127341 | 0.443825 | 343 | 126 | 1 | unresolved_no_admissible_progress | 1253 | 26 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_integrity | pass | spectrum=0;effect=0 | 0;0 | continue |
| frozen_start_pair_replay | pass | 6/6 | 6/6 | continue |
| whole_cycle_exact_reversibility | pass | 6/6 | 6/6 | continue |
| representation_covariance | fail | 0/6 | 6/6 | repair_representation |
| bounded_2x2_pair_accessibility | unresolved | exact_bridges=0/6 | descriptive_bounded_result | unresolved_not_disconnected |
| v16z_overall | v16z_cycle_representation_not_qualified | exclusion=1;digests=1;cycles=1;representation=0;bridges=0/6 | 1;1;1;1;descriptive | v16z_cycle_representation_not_qualified |

## Interpretation boundary

An exact 2x2 bridge proves only that the tested pair lies in one 2x2-switch component. It does not prove global connectivity or mixing. An unresolved bounded search proves neither separation nor slow mixing.

V16z establishes no spectrum effect, global null law, energy, temperature, invariant, dimension, manifold, Lorentz symmetry, spacetime, particle, entanglement, continuum, or physical law.
