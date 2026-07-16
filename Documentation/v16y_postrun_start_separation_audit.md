# v16y post-run start-separation audit

## Frozen evidence

The v16y gate remains `v16y_2x2_chain_finite_centers_not_stable`. This audit only aggregates its frozen endpoint, pairwise, stability and marginal-profile CSV files. It reruns no chain, source spectrum or observed-effect statistic.

- Mean cross-start endpoint distance: `0.422373`.
- Mean within-source-start endpoint distance: `0.078443`.
- Mean within-random-start endpoint distance: `0.078510`.
- All `24` failed center rows are start-family comparisons: four features on each of six sources.
- Independent chain-seed and early/late-window comparisons have `0` failures.
- The chain leaves `460-548` globally variable edges present in every one of its 32 pooled endpoints per source.
- The chain maximum variable-edge inclusion rate is `1.000` on all six sources, and its mean variable-edge binary entropy is lower than the random-cost reference on all six.

## Interpretation

The implemented 2x2 chain is reversible, mobile and locally repeatable at the frozen budget, but its finite endpoint distribution remains strongly start-dependent. This is consistent with either very slow traversal or distinct accessibility components under 2x2 moves. It does **not** prove disconnection because no complete reachability or mixing argument was run.

Simply doubling the budget is not yet the most diagnostic next step: the finite chains changed only about eight percent of their own starting edges while the two endpoint clouds remain about forty-two percent apart. A targeted move-class audit can first determine whether longer alternating cycles provide explicit bridges that 2x2 swaps miss.

## Next gate

Run `v16z_alternating_cycle_bridge_gate` effect-blind on the same six state spaces and the same source/random-cost start pairs:

1. decompose each start-pair symmetric difference into valid alternating cycles;
2. report cycle-length and changed-edge coverage distributions;
3. test exact forward/reverse integrity for whole-cycle moves;
4. attempt bounded 2x2 bridge searches and label failure as unresolved, never as proof of disconnection;
5. only if a reversible longer-cycle kernel is qualified, compare its finite start/seed/time stability before any spectrum effect.

No statement here establishes global irreducibility, mixing, uniform sampling, a canonical null or physics.
