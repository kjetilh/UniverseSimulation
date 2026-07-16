# v16z post-run representation audit

Formal frozen status remains `v16z_cycle_representation_not_qualified`. This post-run audit does not rewrite the preregistered gate.

The formal raw dictionary-key comparison passed `0/6`. Semantic relabeling changes `SlotClass` keys, so raw key equality is not a covariance test. The concrete valid 2x2 move sets at both frozen starts passed candidate-order and semantic-relabel covariance on `6/6` sources.

This diagnoses the sole formal representation failure as a comparison artifact. It supports using edge-level move-set covariance in the next proposal qualification, but it does not retroactively turn v16z into a preregistered pass. The bounded bridge result remains `0/6` exact paths with all six failures unresolved, and no spectrum or observed-effect statistic was computed.
