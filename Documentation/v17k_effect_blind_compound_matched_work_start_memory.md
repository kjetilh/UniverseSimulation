# v17k effect-blind compound matched-work start-memory gate

Status: `v17k_compound_no_uniform_matched_work_gain`.

## Purpose and frozen design

Purpose `purpose://validation`: test whether the qualified v17j two-subcycle law reduces finite start memory more efficiently than v17h's reverse-closed expanded single-cycle law. The gate uses the same six spaces and frozen start pairs with two new seed families. Source spectra and observed effects are prohibited.

Every chain targets exactly `192` accepted gross removed-edge units. Single-cycle work is the accepted cycle's removed-edge count. Compound work is the sum of the two accepted subcycle removed-edge counts. Net endpoint change is logged separately and is never substituted for gross work.

The terminal rule turns a Metropolis-accepted proposal into a self-loop if it overshoots the work target or leaves a remainder not representable by that arm's declared work increments. This is finite work conditioning, not stationary sampling, and may introduce endpoint bias.

## Frozen gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_integrity | pass | spectrum=0;effect=0 | 0;0 | continue |
| frozen_start_integrity | pass | 12/12 | 12/12 | continue |
| qualified_proposal_law_reuse | pass | 2/2;reimplemented=0 | 2/2;reimplemented=0 | continue |
| exact_matched_gross_work_and_endpoint_integrity | pass | 48/48;work=192 | 48/48;each=192 | continue |
| exact_reverse_balance_and_work_definition | pass | 48/48 | 48/48 | continue |
| finite_movement_and_arm_exercise | pass | movement=48/48;exercise=48/48 | 48/48;48/48 | continue |
| resource_bound | pass | 48/48;max=262.266565s | 48/48;each<=900s | continue |
| primary_compound_cross_start_reduction | fail | 0/6;ratio=0.991307-1.003176 | 6/6;each<=0.90 | retire_current_two_cycle_law_as_uniform_remedy |
| v17k_overall | v17k_compound_no_uniform_matched_work_gain | exclusion=1;starts=12/12;laws=1;work=48/48;proposal=48/48;movement=48/48;exercise=48/48;resource=48/48;primary=0/6 | 1;12/12;1;48/48;48/48;48/48;48/48;48/48;6/6 | v17k_compound_no_uniform_matched_work_gain |

## Primary matched-work response

| growth_seed | run_offset | expanded_median_cross_start_distance | compound_median_cross_start_distance | compound_over_expanded_cross_start_distance_ratio | directional_cross_start_reduction | material_cross_start_reduction_pass |
| --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 0.443908 | 0.440050 | 0.991307 | 1 | 0 |
| 9299 | 123403 | 0.394936 | 0.393397 | 0.996103 | 1 | 0 |
| 9299 | 127341 | 0.415555 | 0.413426 | 0.994877 | 1 | 0 |
| 9365 | 123078 | 0.447715 | 0.447996 | 1.000626 | 0 | 0 |
| 9365 | 123403 | 0.393174 | 0.394423 | 1.003176 | 0 | 0 |
| 9365 | 127341 | 0.445219 | 0.442849 | 0.994678 | 1 | 0 |

Directional reduction occurred in `4/6`; material reduction passed `0/6`. Compound/expanded cross-start ratios ranged `0.991307-1.003176` with median `0.995490`.

## Finite execution

The formal comparison contains `48` chains. Maximum runtime was `262.266565` seconds and maximum attempts were `3783`. The weakest compound chain accepted `28` blocks; the weakest expanded chain accepted `5` length-5 cycles. Gross work, net work and endpoint distance remain separate products.

## Claim boundary

This is a relative finite efficiency/start-memory comparison. Even a positive result would not establish global connectivity, irreducibility, convergence, mixing, a stationary distribution, source effects, geometry or physics. A negative result rejects only this exact two-subcycle law as a uniform remedy under the frozen design.

## Next decision

Retire this exact two-subcycle net-6 law as a uniform start-memory remedy. Keep source effects closed. Diagnose whether the remaining barrier is move diameter or accessibility-component structure before choosing a monolithic long-cycle proposal.
