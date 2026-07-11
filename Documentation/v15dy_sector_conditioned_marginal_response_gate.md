# Relasjonell universgraf v0.15dy: sector-conditioned marginal response gate

## Formaal og maal

`purposeRef`: `purpose://prompt.unknown`.

Test om beta1-sektor `+1` endrer kontrolluavhengige marginale dynamikker etter at beta1 og algebraisk avhengige edge-identiteter er fjernet fra kandidatsettet.

| goal | target | status |
| --- | --- | --- |
| G1 clean independent holdout | 48 preregistered runs; zero invariant violations | satisfied |
| G2 sector-conditioned response | at least one frozen metric passes all thresholds | missed |
| G3 next decision | no metric refit | satisfied |

## Frozen design

- target `1024`; growth seeds `202;303`; placements `p0,p1,p2`
- fresh seed deltas `20711;20773;20809;20857`; `3414` events per run
- 24 matched contexts, each with independently randomized beta1-base and beta1-plus1 branches
- uniform relabel-invariant add_chord creates the +1 sector
- primary metrics: `birth_rate_first_half;birth_rate_full;swap_rate_first_half;swap_rate_full;mean_dt_full`
- gate: Holm p <= `0.05`, AUC separation >= `0.7`, relative median gap >= `0.1`, same direction on both growth seeds and at least two placements

Beta1, raw edge offset, far-shell, damage sets and placement labels are excluded from the primary metric set.

## Observable comparisons

| metric | n_pairs | median_beta1_base | median_beta1_plus1 | median_paired_difference | relative_median_gap | sign_consistency | holm_p | auc_separation | growth_seed_direction_match | placement_direction_match | metric_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| birth_rate_first_half | 24 | 0.062 | 0.066 | 0.001 | 0.057 | 0.609 | 1.000 | 0.615 | 1.000 | 1.000 | not_supported |
| birth_rate_full | 24 | 0.062 | 0.062 | 0.002 | 0.009 | 0.625 | 1.000 | 0.568 | 0.500 | 0.667 | not_supported |
| swap_rate_first_half | 24 | 0.015 | 0.015 | 0.000 | 0.020 | 0.500 | 1.000 | 0.500 | 0.000 | 0.000 | not_supported |
| swap_rate_full | 24 | 0.015 | 0.015 | -0.001 | 0.019 | 0.583 | 1.000 | 0.509 | 0.500 | 1.000 | not_supported |
| mean_dt_full | 24 | 0.012 | 0.012 | -0.000 | 0.056 | 0.583 | 1.000 | 0.509 | 1.000 | 0.333 | not_supported |

## Claim adjudication

| claim_id | statement | evaluation | evidence_ref |
| --- | --- | --- | --- |
| claim.v15dy.sector-marginal-response | The beta1 +1 sector changes at least one frozen beta1-free marginal dynamics observable under band_zero_del. | unsupported | v15dy_observable_comparisons.csv |
| claim.v15dy.sector-dynamical-species | The beta1 sectors constitute distinct physical species. | unsupported | v15dy_gate_evaluation.csv:diagnosis |
| claim.v15dy.emergent-symmetry | A sector-conditioned marginal response would establish emergent physical symmetry. | unsupported | v15dy_gate_evaluation.csv:diagnosis |

## Decision

| key | value | evidence |
| --- | --- | --- |
| scope | fresh_independent_sector_response | runs=48; pairs=24; steps_per_run=3414 |
| artifact_control | clean | 48 preregistered unique independent sector runs |
| anchor_beta1_conservation | pass | eventwise and final beta1 drift must remain zero |
| primary_metric_gate | fail | passing_metrics=none |
| diagnosis | no_beta1_sector_response_detected_in_frozen_marginals | beta1 itself and edge-count identities excluded from primary metrics |
| next_step | retain_beta1_as_sector_label_only_and_test_local_sector_boundary_observable | deduced from frozen multi-metric gate without refit |

A pass would identify a fresh statistical candidate, not a particle or physical species. A fail means only that these five global marginal observables do not expose a sector effect at this budget.
