# v16w global-null qualification gate

Status: `v16w_global_null_qualification_instrumentation_failed`.

## Frozen design

The six v16s source DAGs and v16v edge-slot constraints remain fixed. Each source receives `32` source-retention-minimizing endpoints and `16` pure random-priority endpoints. The script computes no source spectrum and no observed-effect statistic.

The primary tie-break is keyed by the candidate edge rather than candidate-column order. Its total possible contribution is below `0.25`, so a one-edge source-retention difference remains lexicographically dominant with margin above `0.75`.

## Source qualification summary

| growth_seed | run_offset | primary_unique_fraction | primary_median_pairwise_change | primary_candidate_union_coverage | primary_effective_edge_support_ratio | batch_center_pass | objective_sensitivity_pass | source_qualification_pass |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | 1.0 | 0.3004410143329658 | 0.2319471817106819 | 0.13087456774124237 | 1 | 0 | 0 |
| 9299 | 123403 | 1.0 | 0.24678231673195294 | 0.19960672747050456 | 0.12093531725232008 | 1 | 0 | 0 |
| 9299 | 127341 | 1.0 | 0.2642634118648879 | 0.22377385841990818 | 0.14057351460729564 | 1 | 0 | 0 |
| 9365 | 123078 | 1.0 | 0.32043734230445753 | 0.2423651852447159 | 0.13701374729278423 | 1 | 0 | 0 |
| 9365 | 123403 | 1.0 | 0.23695893451720307 | 0.2157733175914994 | 0.13377551798681983 | 1 | 0 | 0 |
| 9365 | 127341 | 1.0 | 0.3031781432952328 | 0.22450306520527588 | 0.12370256578265464 | 1 | 0 | 0 |

## Gate evaluation

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| endpoint_integrity_and_effect_exclusion | pass | endpoints=288/288;switch=0;spectrum=0;effect=0 | 288/288;0;0;0 | continue |
| replay_and_representation_covariance | fail | replay_order=8/24;relabel=24/24 | 24/24;24/24 | repair_representation_dependence |
| primary_endpoint_diversity | fail | sources=0/6 | 6/6 | family_collapsed_or_concentrated |
| finite_batch_center_stability | pass | features=36/36 | 36/36 | continue |
| objective_sensitivity | fail | features=15/36 | 36/36 | define_explicit_stochastic_measure |
| v16w_overall | v16w_global_null_qualification_instrumentation_failed | integrity=1;replay=0;relabel=1;diversity=0;center=1;objective=0;exclusion=1 | 1;1;1;1;1;1;1 | v16w_global_null_qualification_instrumentation_failed |

## Objective sensitivity

The following null-only feature comparisons exceeded the frozen range-ratio threshold:

| growth_seed | run_offset | feature | primary_median | sensitivity_median | center_shift_range_ratio | maximum_allowed_ratio |
| --- | --- | --- | --- | --- | --- | --- |
| 9299 | 123078 | source_edge_fraction | 0.37651598676957 | 0.5558158765159867 | 0.9524158125915081 | 0.35 |
| 9299 | 123078 | concrete_conflict_fraction | 0.37816979051819183 | 0.556367144432194 | 0.9479472140762465 | 0.35 |
| 9299 | 123078 | mean_pairwise_changed_fraction | 0.3002231745918839 | 0.44436787945608236 | 0.9757913068601334 | 0.35 |
| 9299 | 123403 | source_edge_fraction | 0.4255735870173475 | 0.6017067711247901 | 0.9044540229885053 | 0.35 |
| 9299 | 123403 | concrete_conflict_fraction | 0.42697257974258535 | 0.6026860660324567 | 0.8971428571428574 | 0.35 |
| 9299 | 123403 | mean_candidate_rank_fraction | 0.35509243749541464 | 0.3617785126819465 | 0.5003197511176362 | 0.35 |
| 9299 | 123403 | mean_pairwise_changed_fraction | 0.2467552394534 | 0.3985357209475844 | 0.9674920700672366 | 0.35 |
| 9299 | 127341 | source_edge_fraction | 0.3959693443088277 | 0.5830258302583027 | 0.9468390804597708 | 0.35 |
| 9299 | 127341 | concrete_conflict_fraction | 0.39909168322452454 | 0.5851546977008232 | 0.9364285714285717 | 0.35 |
| 9299 | 127341 | mean_candidate_rank_fraction | 0.37226973311153766 | 0.3818238181222033 | 0.4440247685319748 | 0.35 |
| 9299 | 127341 | mean_pairwise_changed_fraction | 0.2643412414273026 | 0.419680196801968 | 0.9711470942923873 | 0.35 |
| 9365 | 123078 | source_edge_fraction | 0.3779086066722736 | 0.5480796187272218 | 0.9484375000000003 | 0.35 |
| 9365 | 123078 | concrete_conflict_fraction | 0.3801513877207738 | 0.5493411830670031 | 0.9429687499999997 | 0.35 |
| 9365 | 123078 | mean_candidate_rank_fraction | 0.3770566171876485 | 0.3836212207521047 | 0.42031855803705376 | 0.35 |
| 9365 | 123078 | mean_pairwise_changed_fraction | 0.3204644727203668 | 0.4512382020371928 | 0.9584913080750499 | 0.35 |
| 9365 | 123403 | source_edge_fraction | 0.4225860155382908 | 0.605299667036626 | 0.9461206896551724 | 0.35 |
| 9365 | 123403 | concrete_conflict_fraction | 0.4264705882352941 | 0.6082130965593785 | 0.9397417503586802 | 0.35 |
| 9365 | 123403 | mean_pairwise_changed_fraction | 0.23677544663635386 | 0.3937569367369589 | 0.977603620878018 | 0.35 |
| 9365 | 127341 | source_edge_fraction | 0.3693894619459158 | 0.5476721494284917 | 0.9587706146926532 | 0.35 |
| 9365 | 127341 | concrete_conflict_fraction | 0.3700864231948704 | 0.5482297184276554 | 0.9580209895052472 | 0.35 |
| 9365 | 127341 | mean_pairwise_changed_fraction | 0.3034524312706278 | 0.4513428120063191 | 0.963892307992888 | 0.35 |

## Interpretation boundary

A pass qualifies only replay, finite endpoint diversity, representation covariance, finite batch-center stability, and limited objective robustness for this algorithmic family. It does not establish uniform sampling, mixing, stationarity, a canonical probability measure, or representativeness.

A failure is also informative: it means the feasible global family is materially selected by an arbitrary solver objective or another implementation choice. Do not run an observed-effect comparison until the failed qualification layer is repaired and frozen effect-blind.

V16w establishes no energy, temperature, invariant, dimension, manifold, Lorentz symmetry, spacetime, particle, entanglement, continuum, or physical law.
