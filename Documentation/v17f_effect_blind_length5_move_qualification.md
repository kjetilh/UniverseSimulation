# v17f effect-blind length-5 move qualification

Status: `v17f_finite_movement_not_qualified`.

## Purpose and measurable goal

Purpose `purpose://validation`: determine whether one genuinely new one-step move can be added without weakening probability, representation, traversal or resource discipline. Goal G1 requires frozen starts 12/12, length-5 reverse/batch/novelty witnesses 12/12, representation 12/12, finite movement 24/24 and resource 24/24.

## Evidential starting point

V17e retired further scale growth of the exact length-2-to-4 kernel after material cross-start contraction passed 0/6. V17f does not reinterpret that result. It qualifies a different move component before any new start-memory comparison.

## Proposal law

The expanded chain chooses the qualified v17c length-2-to-4 component or the new fixed length-5 component with probability 1/2. The length-5 auxiliary samples an ordered batch of four selected edges uniformly without replacement, chooses uniformly among batch edges with a deterministic completion witness under a 20,000-state DFS cap, then samples each raw parent and each witness-supported selected edge uniformly. A dead branch is a self-loop.

The reverse auxiliary uses the reversed added-edge path and a bijective map of the ordered first-edge batch. Exact auxiliary probabilities enter a lazy Metropolis correction. The declared target is uniform only within each connected component of this expanded proposal kernel.

## Excluded design pilot

| growth_seed | run_offset | start_family | attempts | valid_proposals | accepted_cycles | reverse_unsupported | maximum_proposal_seconds | elapsed_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | source_assignment | 64 | 6 | 3 | 0 | 0.0392573750577867 | 0.28749562497250736 |
| 9299 | 123078 | v16x_random_cost_a0 | 64 | 4 | 4 | 0 | 0.08331470796838403 | 0.4466596250422299 |

The pilot selected only algorithmic bounds. It was excluded from the formal six-source gate and computed no source spectrum or observed effect.

## Source qualification

| growth_seed | run_offset | frozen_start_passes | reversibility_passes | novel_one_step_passes | representation_passes | movement_passes | resource_passes | minimum_accepted_length5_cycles | maximum_chain_seconds | source_qualification_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 2 | 2 | 2 | 2 | 3 | 4 | 11 | 20.118772 | 0 |
| 9299 | 123403 | 2 | 2 | 2 | 2 | 3 | 4 | 13 | 12.363858 | 0 |
| 9299 | 127341 | 2 | 2 | 2 | 2 | 2 | 4 | 10 | 11.646691 | 0 |
| 9365 | 123078 | 2 | 2 | 2 | 2 | 2 | 4 | 11 | 12.935029 | 0 |
| 9365 | 123403 | 2 | 2 | 2 | 2 | 2 | 4 | 7 | 16.126832 | 0 |
| 9365 | 127341 | 2 | 2 | 2 | 2 | 3 | 4 | 9 | 22.681378 | 0 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_integrity | pass | spectrum=0;effect=0 | 0;0 | continue |
| frozen_start_and_assignment_integrity | pass | starts=12/12;final_integrity=24/24 | 12/12;24/24 | continue |
| length5_pathwise_detailed_balance | pass | 12/12 | 12/12 | continue |
| ordered_batch_reverse_pairing | pass | 12/12 | 12/12 | continue |
| new_one_step_length_support | pass | 12/12 | 12/12 | one_step_novelty_only |
| representation_covariance | pass | 12/12 | 12/12 | continue |
| length5_finite_exercise | pass | 24/24;min=7 | 24/24;each>=4 | continue |
| finite_traversal_and_resource | fail | movement=15/24;resource=24/24;max=22.681378s | 24/24;24/24;each<=120s | do_not_compare_start_memory |
| v17f_overall | v17f_finite_movement_not_qualified | exclusion=1;starts=12/12;integrity=24/24;reverse=12/12;batch=12/12;novelty=12/12;representation=12/12;exercise=24/24;movement=15/24;resource=24/24 | 1;12/12;24/24;12/12;12/12;12/12;12/12;24/24;24/24;24/24 | v17f_finite_movement_not_qualified |

## Finite chain evidence

Across 24 formal chains, the minimum accepted old-cycle count was `66`, the minimum accepted length-5 count `7`, minimum accepted-edge work `235`, minimum final displacement `0.058546`, and maximum runtime `22.681378` seconds.

## Claim boundary

A qualified result establishes only a finite, effect-blind move implementation with tested pathwise detailed balance, representation covariance, traversal and resource behavior. A length-5 transition being outside the old kernel's one-step length support does not show that it crosses an old connected component; it may still be a composition of old moves.

No source spectrum, observed effect, convergence, mixing, irreducibility, energy, temperature, Lorentz symmetry, spacetime, particle, Bell correlation, entanglement or universe model was tested.
