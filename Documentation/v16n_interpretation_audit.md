# v16n interpretation audit

Status: `v16n_coarse_event_resource_sampler_not_qualified`.

## What failed

The failure is sharper than an insufficient ceiling:

- six fresh calibration histories and all event-ID/resource metadata mappings passed;
- `99.714%` or more of source edges belonged to a coarse-color bucket containing at least two edges;
- all `1152` perturbation attempts across ceilings `240`, `480`, `960`, and `1920` preserved the unchanged source structure;
- total accepted swaps were exactly `0` at every ceiling;
- changed-edge fraction was exactly `0` at every ceiling;
- uniqueness failed because every replicate remained the source graph.

The selected same-color proposal therefore has no observed legal transition under the combined actual-cross-resource, order, duplicate-edge, age-bin, and exact-depth rules. Increasing the attempt ceiling further is not justified.

## What did not fail

This is not a v16m effect failure. V16n computed no interval spectra and used no effect values in the calibration decision. It is also not a metadata or source-DAG integrity failure.

## Correct conclusion

The exact status remains `v16n_coarse_event_resource_sampler_not_qualified`. The v16m contrast is neither supported nor refuted under event/resource conditioning.

The next smallest step is a reachability audit, not a spectrum run. It should compare:

1. the frozen same-color proposal used in v16n; and
2. the more general global color-multiset rule originally considered by the panel, where the two old colors may differ but their multiset must equal the two new colors.

If the general rule also has no legal moves, retire this actual-conflict edge-color null and consider the weaker event-side footprint null. If it has adequate legal support, qualify a new proposal sampler effect-blind before any spectrum is computed.
