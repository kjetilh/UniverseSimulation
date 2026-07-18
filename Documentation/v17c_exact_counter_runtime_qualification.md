# v17c exact-counter runtime qualification

Status: `v17c_exact_counter_runtime_qualified`.

## Purpose and frozen goal

Purpose: determine whether the exact v17b proposal law can meet its already frozen finite resource bound without changing its dynamics. Goal: exact support/count parity 36/36, exact chain replay 24/24, movement 24/24 and runtime <=60 seconds 24/24.

## Method

v17c keeps the v17b starts, seeds, 512-step budget, cycle lengths, laziness and exact reverse auxiliary. It replaces complete-tuple materialization and duplicate forward enumeration with an exact dynamic-programming completion counter. One random rank is sampled uniformly and traversed in the same depth-first order as v17b.

## Source qualification

| growth_seed | run_offset | counter_parity_passes | representation_passes | reversibility_passes | exact_replay_passes | movement_passes | resource_passes | maximum_chain_seconds | source_qualification_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 6 | 2 | 6 | 4 | 4 | 4 | 14.921836 | 1 |
| 9299 | 123403 | 6 | 2 | 6 | 4 | 4 | 4 | 9.982094 | 1 |
| 9299 | 127341 | 6 | 2 | 6 | 4 | 4 | 4 | 6.956678 | 1 |
| 9365 | 123078 | 6 | 2 | 6 | 4 | 4 | 4 | 8.529966 | 1 |
| 9365 | 123403 | 6 | 2 | 6 | 4 | 4 | 4 | 12.886217 | 1 |
| 9365 | 127341 | 6 | 2 | 6 | 4 | 4 | 4 | 13.693119 | 1 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_integrity | pass | spectrum=0;effect=0 | 0;0 | continue |
| frozen_start_replay | pass | 12/12 | 12/12 | continue |
| exact_counter_support_parity | pass | 36/36 | 36/36 | continue |
| exact_v17b_transition_replay | pass | trace=24/24;summary=24/24 | 24/24;24/24 | continue |
| representation_covariance | pass | 12/12 | 12/12 | continue |
| exact_reverse_support | pass | 36/36 | 36/36 | continue |
| pathwise_detailed_balance | pass | 36/36 | 36/36 | continue |
| finite_movement | pass | 24/24 | 24/24 | continue |
| resource_bound | pass | 24/24 | 24/24 | continue |
| v17c_overall | v17c_exact_counter_runtime_qualified | exclusion=1;starts=12/12;counter=36/36;replay=24/24;representation=12/12;reverse=36/36;balance=36/36;movement=24/24;resource=24/24 | 1;12/12;36/36;24/24;12/12;36/36;36/36;24/24;24/24 | v17c_exact_counter_runtime_qualified |

## Runtime and finite movement

Across 24 chains, minimum valid proposals were `119`, minimum accepted cycles `72`, minimum accepted length>=3 cycles `34`, minimum final displacement `0.051944`, and maximum runtime `14.921836` seconds.

Runtime improved in `24/24` matched cells; the median v17c/v17b runtime ratio was `0.161356`. Exact transition replay, not similarity of aggregate outcomes, is the implementation-equivalence test.

## Claim boundary

This gate tests an implementation of one finite proposal law. It does not establish global irreducibility, convergence, mixing, a canonical measure, source-effect survival, Bell correlations, entanglement, Lorentz symmetry, spacetime or a universe model.
