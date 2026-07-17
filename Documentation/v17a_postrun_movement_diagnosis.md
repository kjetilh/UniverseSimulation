# v17a post-run movement diagnosis

The frozen formal status remains `v17a_cycle_proposal_finite_movement_not_qualified`. This audit does not relax thresholds or rerun the chains.

Representation, exact reverse support, pathwise detailed balance and resource bounds passed in the formal gate. All `24/24` chains also passed the unique-state floor, with `16-40` visited states.

Finite movement nevertheless failed for two coupled reasons. Valid proposals ranged from `31` to `61` and passed the frozen floor on `0/24`. Accepted cycles passed on `6/24`, accepted length-three-or-greater cycles on `2/24`, and final five-percent displacement on `0/24`. Observed final displacement was `0.010632-0.030656`.

The correct diagnosis is proposal inefficiency under the frozen finite budget, not a reversibility, representation or runtime failure. Do not advance to start/seed/time stability and do not merely lengthen the chains. The smallest next research gate is a residual-graph cycle constructor that raises valid-cycle yield while preserving distinguished reverse auxiliaries and exact proposal ratios; it must be qualified anew before any spectrum/effect test.
