# v16y reversible global-measure gate

Status: `v16y_2x2_chain_finite_centers_not_stable`.

## Evidential status

This is an effect-blind probability-law comparison on the same six frozen coarse global matching spaces used by v16x. It computes no source spectrum or observed-effect statistic.

The candidate chain is lazy and Metropolis-corrected. Its accepted transition probability is exactly `1 / (2 * max(degree(x), degree(y)))` in both directions. This gives a uniform stationary target only inside each connected component of the valid 2x2-switch graph. The run does not prove global connectivity or mixing.

Before preregistration, a design pilot measured the low acceptance of naive random selected-edge pairs and timed exact valid-neighbor enumeration. Those effect-blind implementation observations selected the fixed 512-step budget; they are not fresh evidence.

## Source qualification

| growth_seed | run_offset | reference_replay_pass | reversibility_pass | representation_pass | movement_pass | center_stability_pass | measure_comparison_pass | source_qualification_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 9299 | 123403 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 9299 | 127341 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 9365 | 123078 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 9365 | 123403 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| 9365 | 127341 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |

## Probability-law comparison

| growth_seed | run_offset | reference_max_inclusion_rate | chain_max_inclusion_rate | mean_binary_entropy_delta | effective_support_ratio_chain_over_reference | union_coverage_ratio_chain_over_reference | measure_comparison_pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 0.937500 | 1.000000 | -0.113552 | 0.463719 | 0.363358 | 0 |
| 9299 | 123403 | 0.968750 | 1.000000 | -0.117481 | 0.495593 | 0.401315 | 0 |
| 9299 | 127341 | 1.000000 | 1.000000 | -0.128262 | 0.499005 | 0.405144 | 0 |
| 9365 | 123078 | 0.906250 | 1.000000 | -0.109500 | 0.449445 | 0.356582 | 0 |
| 9365 | 123403 | 1.000000 | 1.000000 | -0.128397 | 0.502785 | 0.398990 | 0 |
| 9365 | 127341 | 0.968750 | 1.000000 | -0.103441 | 0.456975 | 0.354175 | 0 |

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_endpoint_integrity | pass | endpoints=192/192;spectrum=0;effect=0 | 192/192;0;0 | continue |
| frozen_random_cost_reference_replay | pass | 192/192 | 192/192 | continue |
| exact_detailed_balance_reversibility | pass | 48/48 | 48/48 | continue |
| representation_covariance | pass | 6/6 | 6/6 | continue |
| finite_chain_mobility | pass | chains=24/24 | chains=24/24 | continue |
| start_seed_time_center_stability | fail | features=102/126 | 126/126 | not_finitely_stable |
| concentration_profile_improvement | fail | sources=0/6 | sources>=4/6 | profile_not_improved |
| v16y_overall | v16y_2x2_chain_finite_centers_not_stable | integrity=1;reference=1;reversibility=1;representation=1;movement=1;centers=0;profile=0 | 1;1;1;1;1;1;1 | v16y_2x2_chain_finite_centers_not_stable |

## Interpretation boundary

A pass would establish finite qualification of this declared component-uniform chain under two starts, two independent seeds and three center comparisons. It would not prove irreducibility, convergence, global uniformity, maximum entropy or a canonical null.

A failure distinguishes algebra/reversibility defects, insufficient finite mobility, start/seed/time instability, and failure to improve the v16x concentration profile.

V16y establishes no spectrum effect, energy, temperature, invariant, dimension, manifold, Lorentz symmetry, spacetime, particle, entanglement, continuum, or physical law.
