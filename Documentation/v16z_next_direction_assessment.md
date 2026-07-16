# v16z next direction

Formal status: `v16z_cycle_representation_not_qualified`.

Post-run diagnosis: raw `SlotClass` dictionary equality was not a covariant
representation check. Concrete source/random-start 2x2 move sets passed
candidate-order and semantic-relabel covariance on `6/6`, without changing the
formal gate retroactively.

The next narrow gate should be
`v17a_state_independent_cycle_proposal_qualification`. On the same six spaces,
define a target-independent set of alternating-cycle proposals from each
current assignment. Require the exact reverse cycle to occur in the proposed
state's candidate set and use the explicit forward/reverse proposal ratio in a
lazy Metropolis correction. Qualify replay, candidate-order covariance,
edge-level semantic-relabel covariance, reverse support, finite movement and
resource bounds before any start/seed/time sampler comparison.

Do not infer 2x2 disconnection from v16z. The bounded heuristic reduced pair
mismatch by `98.1521-99.6892%` but found `0/6` complete paths. Do not simply
increase the same target-directed search budget, and do not open spectrum or
effect statistics until a state-independent probability law passes the
accessibility and stability layers.
