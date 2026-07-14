# v16j interpretation audit

## Why this audit exists

The frozen v16j composite gate returned
`causal_interval_abundance_not_supported_under_degree_age_null` because it was
defined as a conjunction of five evidential subgates. Four passed. The only
failure was the frozen v16d-to-v16h effect-magnitude transfer ratio:
`0.4696605292256925`, just below the preregistered lower bound `0.5`.

That binary status must be retained as the frozen gate result. It must not be
paraphrased as "the strict-null signal disappeared", because the effect-existence
evidence says the opposite:

- `384/384` holdout nulls passed structure, mixing, and uniqueness checks.
- `12/12` runs had a Jensen-Shannon effect ratio above `1`.
- `12/12` runs had empirical upper-tail `p = 1/33 = 0.030303...`.
- The primary local arm had median ratio `7.975000`, positive fraction `1.0`,
  and `p <= 0.10` fraction `1.0`; its frozen local gate passed.
- Both growth-seed groups and both scheduler groups passed.

## Correct evidential reading

The causal-interval abundance contrast survives a null preserving event count,
scheduler order, exact direct in/out-degree, exact causal depth, the full depth
profile, and the global dyadic parent-age histogram. Its effect magnitude is
not stable enough relative to the v16d calibration baseline under the frozen
`[0.5, 2.0]` transfer interval.

The concise status for scientific communication is therefore:

`strict_null_contrast_supported_magnitude_transfer_not_stable`

This is a post-run semantic audit, not a replacement preregistered gate. It
does not authorize a dimension fit or a geometry claim. The null still does
not preserve per-child/exact-edge parent age, event family, or read/write
resource type.

## Smallest next decision

Do not retire the interval observable as if it vanished, and do not promote it
to spacetime evidence. The smallest justified next gate is one fresh-history
replication with the frozen v16j observable and strict null, using a wider
predeclared effect-size model that reports existence and magnitude stability as
separate outcomes.
