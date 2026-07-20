# v17g effect-blind reverse-closure qualification

Status: `v17g_reverse_closed_length5_move_qualified`.

## Purpose and goal

Purpose `purpose://validation`: determine whether the exact v17f raw generator can be made reverse-closed by a deterministic support filter without changing accepted dynamics. The frozen goal requires 24,576/24,576 raw-generation parity, exact identity of all 11 filtered auxiliaries, accepted-transition and endpoint parity 24/24, retained reverse support 24/24, representation 12/12, movement 24/24 and resource 24/24.

## Law change

The batch size, length-5 constructor, 20,000-state bounded witness law, old-kernel mixture, starts, seeds and 1024-step budget are unchanged. A raw length-5 auxiliary whose explicitly mapped reverse auxiliary is unsupported under that same bounded law becomes a self-loop before valid-proposal accounting. No extra random draw is made. Retained auxiliary probabilities and the lazy Metropolis ratio are unchanged.

## Frozen gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_integrity | pass | spectrum=0;effect=0 | 0;0 | continue |
| raw_generation_and_event_parity | pass | raw=24576/24576;event=24576/24576 | 24576/24576;24576/24576 | continue |
| filtered_auxiliary_identity | pass | filtered=11;identity=24/24;counts=24/24 | 11;24/24;24/24 | continue |
| accepted_transition_and_endpoint_parity | pass | accepted=24/24;endpoint=24/24 | 24/24;24/24 | continue |
| retained_reverse_support_and_balance | pass | runtime=24/24;witness=12/12 | 24/24;12/12 | continue |
| representation_covariance | pass | 12/12 | 12/12 | continue |
| finite_movement_and_resource | pass | movement=24/24;resource=24/24 | 24/24;24/24 | continue |
| v17g_overall | v17g_reverse_closed_length5_move_qualified | raw=24576;filtered=11;accepted=24/24;endpoint=24/24;support=24/24;representation=12/12;movement=24/24;resource=24/24 | raw=24576;filtered=11;accepted=24/24;endpoint=24/24;support=24/24;representation=12/12;movement=24/24;resource=24/24 | v17g_reverse_closed_length5_move_qualified |

## Finite evidence

Across 24 chains, `11` raw auxiliaries were filtered. Minimum retained valid proposals were `130`, minimum accepted length-5 cycles `7`, and maximum runtime `20.456393` seconds.

## Interpretation boundary

This gate changes the declared proposal support and valid-yield accounting, but deliberately reproduces every accepted v17f transition. A pass is probability-law and instrumentation qualification, not new dynamical evidence, connectivity, convergence, mixing, a source effect or physics.
