# v16k interpretation audit

## Frozen result

The preregistered overall status is permanently:

`v16k_instrumentation_failed`

It failed because the gate required complete perturbation integrity for both
the unchanged primary sampler and the longer-perturbation diagnostic:

- primary: `383/384` passed
- longer diagnostic: `160/192` passed

The single primary failure occurred in `current_global`, not the primary
`exposure_matched_local` arm. It preserved every declared structure, changed
`10.606953 %` of direct edges, and was unique, but stopped at `254/255`
accepted swaps after the frozen attempt ceiling.

The longer diagnostic failed its accepted-swap target in all 16 replicates of
two runs. Every failed perturbation still preserved the declared structure,
was unique, and changed `10.824891 %` to `13.371925 %` of direct edges. The
failure is therefore an attempt-budget/completion failure, not a structural
preservation failure. It cannot be relabeled as a pass after the run.

## Valid component result

The six preregistered primary-arm histories have `192/192` complete primary
perturbations. Their frozen effect-existence component gate passed:

- median JS effect ratio: `8.59267128528609`
- positive fraction: `1.0` (`6/6`)
- empirical `p <= 0.10` fraction: `1.0` (`6/6`)

The descriptive magnitude point classification is
`compatible_with_both_prior_anchors`; the fresh median is `0.506036` times the
v16d anchor and `1.077451` times the v16h anchor. This is not a confirmatory
magnitude-stability result. The bootstrap median interval is wide
(`4.553808` to `14.167312`).

Correct wording:

> On six fresh `exposure_matched_local` histories, all 192 frozen primary
> perturbations passed integrity and the preregistered effect-existence
> component thresholds were met. The full v16k replication nevertheless
> failed its frozen instrumentation gate.

Do not state that v16k replicated the contrast as a completed gate. Do not use
the longer-diagnostic effect ratios as confirmatory evidence because one
primary run did not satisfy the frozen completion contract.

## Next gate

Do not proceed directly to a more constrained event/resource null. First
qualify the current sampler on the saved v16k DAGs with a larger attempt
ceiling selected only from completion behavior, without using effect ratios.
That qualification is nonconfirmatory. If it completes cleanly, freeze the
qualified sampler and run a new 12-run fresh-history holdout with new seeds.

Even a completed sampler does not prove convergence, stationarity,
independence, representativeness, or uniform sampling over the constrained DAG
space. No v16k result establishes dimension, manifoldlikeness, Lorentz
symmetry, spacetime, continuum behavior, particles, entanglement, or a physical
causal law.
