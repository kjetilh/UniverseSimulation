# Relasjonell universgraf v0.15cr: next direction assessment

## Formal

Denne runden kjorer ingen ny dynamikk. Den vurderer hva som boer vaere neste steg etter:

- `v15co`: univers-inspirerte egenskaper kan brukes som svak heuristikk, men bare etter repo-lokal oversettelse.
- `v15cp`: skalert target-1024-budsjett gjenopplivet ikke p2.
- `v15cq`: target-896 midpoint gir bare `intermediate_p2_partial_not_supported`.

Maalet er aa velge neste retning uten aa overbeskytte en svekket p2-hypotese.

## Current evidence

| target | carrier | p2 supported | p2 established | p2 horizon | key contrast |
| --- | --- | --- | --- | --- | --- |
| 768 | add_chord | 0 | 0.500 | 64.500 | p2 active, but support score only 3 |
| 768 | local_swap | 1 | 0.500 | 64.500 | strongest p2 row |
| 896 | add_chord | 0 | 0.500 | 49.500 | p0 is equally established and has longer horizon 75.000 |
| 896 | local_swap | 0 | 0.000 | 0.000 | p2 absent |
| 1024 | add_chord | 0 | 0.000 | 0.000 | scaled budget does not revive p2 |
| 1024 | local_swap | 0 | 0.000 | 0.000 | p2 absent |

The important inversion is that the p2 scale story weakened, while `add_chord_p0` became more interesting:

| target | add_chord_p0 established | add_chord_p0 horizon |
| --- | --- | --- |
| 768 | 0.000 | 2.000 |
| 896 | 0.500 | 75.000 |
| 1024 | 0.500 | 86.000 |

This does not prove a new scale law. It is a small-n clue discovered through a control profile. But it is now more informative than more p2 budget.

## Decision matrix

| option | verdict |
| --- | --- |
| Replicate midpoint p2 | Secondary only if we want extra conservatism before retiring p2. |
| More target-1024 p2 budget | Not recommended; v15cp already tested the direct budget caveat. |
| Retire p2 as scale-selector | Recommended policy. Keep p2 as target-768 local contrast. |
| Add_chord p0 scale-response holdout | Recommended next dynamic lab. |
| Conditional quasi-invariant carrier-first | Good secondary path after a clearer response anchor. |
| Reopen Lorentz/global rules | Not recommended; evidence is still `not_yet`. |
| Broad scale sweep | Not yet; choose a better observable first. |

See `Documentation/v15cr_next_direction_decision_matrix.csv` for the full scored matrix.

## Recommended next step

Run a narrow holdout tentatively named:

`relational_universe_v15cs_add_chord_p0_scale_response_holdout.py`

Primary question:

Does the `add_chord_p0` far-shell response observed at targets `896` and `1024` survive fresh seed deltas strongly enough to become the next scale-positive observable?

Recommended design:

- regime: `band_zero_del`
- growth seed: `202`
- targets: `896` and `1024`
- budgets: scaled from target 768 (`2987` and `3414`)
- primary profile: `add_chord_p0`
- controls: `add_chord_p2` and `local_swap_p0`
- seed deltas: fresh seed deltas, not the v15cn/v15cp/v15cq pair
- keep output comparable to v15cp/v15cq: runs, aggregate, p0-vs-controls, target summary, diagnosis

Decision criteria:

- If `add_chord_p0` remains established at both `896` and `1024`, and controls remain weaker, promote it to a new scale-response candidate.
- If `add_chord_p0` collapses on fresh seed deltas, treat the p0 signal as small-n/control artifact and pivot to no-new-dynamics response-fingerprint synthesis.
- If `add_chord_p2` or `local_swap_p0` matches it, do not tell a p0-specific story; instead classify the scale response by carrier/control pattern.

## Why not p2 next?

The p2 line has now consumed the direct budget and midpoint checks:

- target `768`: one strong carrier (`local_swap_p2`) and one partial carrier (`add_chord_p2`)
- target `896`: partial add_chord activity, but not p2 support
- target `1024`: no p2 support under same-absolute or scaled budget

More p2 work is possible, but it is no longer the best marginal use of budget. The correct repo-loyal move is to downgrade p2 as a scale-selector and let the data nominate the next observable.

## Interpretation limits

- Do not read `add_chord_p0` as a particle, invariant, Lorentz-like behavior, or universal geometry.
- Do not read p2 retirement as proof that no scale effects exist.
- Do read this as a shift from label-first search to response-first search.
