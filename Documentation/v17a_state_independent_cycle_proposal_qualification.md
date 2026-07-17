# v17a state-independent cycle proposal qualification

Status: `v17a_cycle_proposal_finite_movement_not_qualified`.

## Evidential status

The proposal uses only the current valid assignment and the frozen candidate graph. It does not inspect the paired target assignment, source spectrum, or observed effect.

A proposal is a distinguished oriented alternating cycle of length `2-8`. Its reverse auxiliary is the reversed ordered list of added edges. The lazy Metropolis acceptance uses the exact ratio of those two auxiliary-path probabilities. This establishes only pathwise detailed balance for tested transitions and a component-uniform target, never global connectivity or mixing.

## Source qualification

| growth_seed | run_offset | representation_passes | reversibility_passes | movement_passes | minimum_accepted_cycles | minimum_final_start_changed_edge_fraction | maximum_chain_seconds | source_qualification_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 2 | 14 | 0 | 21 | 0.014333 | 3.399975 | 0 |
| 9299 | 123403 | 2 | 14 | 0 | 15 | 0.010632 | 3.094291 | 0 |
| 9299 | 127341 | 2 | 14 | 0 | 26 | 0.017031 | 3.422457 | 0 |
| 9365 | 123078 | 2 | 14 | 0 | 20 | 0.015419 | 3.498641 | 0 |
| 9365 | 123403 | 2 | 14 | 0 | 18 | 0.014428 | 3.254897 | 0 |
| 9365 | 127341 | 2 | 14 | 0 | 24 | 0.020072 | 3.397751 | 0 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_integrity | pass | spectrum=0;effect=0 | 0;0 | continue |
| frozen_start_replay | pass | 12/12 | 12/12 | continue |
| representation_covariance | pass | 12/12 | 12/12 | continue |
| exact_reverse_auxiliary_support | pass | 84/84 | 84/84 | continue |
| pathwise_detailed_balance | pass | 84/84 | 84/84 | continue |
| finite_movement | fail | 0/24 | 24/24 | retire_or_redesign_proposal |
| resource_bound | pass | 24/24 | 24/24 | continue |
| v17a_overall | v17a_cycle_proposal_finite_movement_not_qualified | exclusion=1;starts=12/12;representation=12/12;reverse=84/84;balance=84/84;movement=0/24;resource=24/24 | 1;12/12;12/12;84/84;84/84;24/24;24/24 | v17a_cycle_proposal_finite_movement_not_qualified |

## Interpretation boundary

Across the finite chains, minimum accepted cycles were `15`, minimum accepted length>=3 cycles were `5`, minimum final start change was `0.010632`, and maximum chain runtime was `3.498641` seconds.

State-independent here means target-independent: the proposal law depends on the current state, as every Markov kernel does. A qualified finite proposal does not establish irreducibility, convergence, mixing, a global uniform law, or a physical ensemble.

V17a establishes no source-spectrum effect, energy, temperature, invariant, dimension, Lorentz symmetry, spacetime, particle, entanglement, continuum, or universe model.
