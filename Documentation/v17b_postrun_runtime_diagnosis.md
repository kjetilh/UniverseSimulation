# v17b post-run runtime diagnosis

Status inherited from the frozen gate: `v17b_resource_not_qualified`.

## Measured result

- finite movement passed `24/24`
- matched valid-proposal improvement passed `24/24`
- median valid-proposal ratio versus v17a was `2.898276`
- resource bound passed only `12/24`
- runtime range was `27.479260` to `270.449001` seconds per chain
- only `1/6` source cells passed all four per-chain resource checks

The slowest chain was growth seed `9365`, run offset
`123078`, start `source_assignment`, seed family
`chain_seed_a` at `270.449001` seconds.

## Trace diagnosis

Recorded completed length-4 sequences account for
`0.965295` of all recorded completion counts.
The Pearson correlation between per-chain runtime and the sum of recorded
completion counts is only `0.125554`.

This weak correlation prevents treating the logged completion count as a
complete cost model. The trace records completed cycles, but not failed branch
visits or allocation cost. It is therefore evidence that length-4 enumeration
dominates the returned candidate mass, not proof that it alone explains runtime.

## Static implementation diagnosis

The frozen v17b implementation enumerates the forward cycle set once in
`propose_cycle()`, then enumerates the same forward set again in
`path_probability()`. It also materializes every completed cycle as a tuple
before sampling. Reverse probability legitimately requires a separate count in
the proposed state; the duplicate forward enumeration does not.

These are algorithmic costs, not dynamical effects. Optimizing them must leave
the exact auxiliary probability and reverse pairing unchanged.

## Next gate: v17c exact-counter runtime qualification

Freeze a new effect-blind gate with the same six spaces, starts, seeds, 512-step
budget, cycle lengths, laziness, movement floors, exact reverse auxiliary and
`<=60 s` resource threshold. Change only the constructor implementation:

1. compute the forward completion count once and reuse it in the auxiliary
   probability
2. replace full tuple materialization with exact completion counting plus
   uniform rank/reservoir sampling
3. add parity tests showing identical completion counts and proposal support
   against v17b on frozen witness states
4. retain exact `min(1,q_reverse/q_forward)` and full assignment-integrity checks
5. require resource pass `24/24` and movement pass `24/24`

Do not open source spectrum, observed effect, start/seed/time stability, Bell,
entanglement or Lorentz claims in v17c. If the exact optimized constructor still
misses the runtime bound, retire full bounded-cycle enumeration as the active
sampler path rather than relaxing the threshold.

## Evidence and claim limits

- v17b trace SHA-256: `2d88a3018ba34e0f9355ebb8e9442282dfdd0126706e38dd0815cdacf225f18b`
- v17b transition summary SHA-256: `974998255c9b26f75f08b472022b53f8b88c7350f3f2c6c858dcce2a38ff8019`
- this is a disclosed post-run diagnosis, not a preregistered v17b endpoint
- no source spectrum or observed-effect statistic was computed
- no convergence, mixing, global irreducibility or physical claim follows
