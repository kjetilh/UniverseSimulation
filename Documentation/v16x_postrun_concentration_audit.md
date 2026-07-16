# v16x post-run concentration audit

This audit does not change the frozen v16x result `v16x_integer_measure_endpoint_diversity_not_qualified`. It regenerates the already declared endpoints, verifies their edge-set digests, and asks why the finite gate failed.

All `192/192` endpoint digests replayed exactly. No source spectrum or observed-effect statistic was computed.

## Failure decomposition

Uniqueness, pairwise distance, variable-edge union coverage, and effective variable support passed on all six sources. Four sources failed only because at least one globally variable edge appeared in all 16 primary endpoints. This criterion correctly remains failed in the frozen gate.

## Combined independent seed families

| growth_seed | run_offset | top_parent_event_id | top_child_event_id | primary_inclusion_count | sensitivity_inclusion_count | combined_inclusion_rate | combined_rate_pass | variable_edges_included_32_of_32 | variable_edges_included_at_least_31_of_32 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 170 | 201 | 16 | 14 | 0.937500 | 1 | 0 | 0 |
| 9299 | 123403 | 2081 | 2170 | 15 | 16 | 0.968750 | 0 | 0 | 1 |
| 9299 | 127341 | 2470 | 2790 | 16 | 16 | 1.000000 | 0 | 2 | 4 |
| 9365 | 123078 | 90 | 145 | 15 | 14 | 0.906250 | 1 | 0 | 0 |
| 9365 | 123403 | 2421 | 3071 | 16 | 16 | 1.000000 | 0 | 2 | 5 |
| 9365 | 127341 | 125 | 1545 | 15 | 16 | 0.968750 | 0 | 0 | 1 |

The combined 32-endpoint rate passes the old `0.95` ceiling on `2/6` sources. This is descriptive post-run evidence, not a retroactive gate pass.

## Center stability

The frozen half-batch gate failed `1/36` features; independent seed-family stability failed `0/36` features.

The half-batch failure was `mean_candidate_rank_fraction` at `9299/123403`: absolute median shift `0.004639` and range ratio `0.504021`.

## Decision boundary

If the 32-endpoint combined ceiling passes broadly, the smallest next gate is a preregistered endpoint-budget extension of this same measure, not an effect test. If high-inclusion edges remain above the ceiling, the measure is genuinely concentrated on those edge choices and needs a different probability law or explicit conditioning.

This audit establishes no uniformity, maximum entropy, canonical null, spectrum effect, energy, temperature, geometry, Lorentz symmetry, spacetime, particle, entanglement, or physical law.
