# Relasjonell universgraf v0.15dz: local beta1-sector transport gate

## Formaal og maal

`purposeRef`: `purpose://prompt.unknown`.

Test om beta1-sektor +1 har justert lokal cycle-neighborhood-dynamikk utover den trivielle initiale chorden.

| goal | target | status |
| --- | --- | --- |
| G1 clean fresh holdout | 48 independent runs; zero invariant violations | satisfied |
| G2 adjusted local response | at least one frozen local metric passes | missed |
| G3 stop decision | transport, static footprint, or retire | satisfied |

## Frozen design

- target `1024`; growth seeds `404;505`; placements `p0,p1,p2`
- fresh seed deltas `21317;21379;21433;21491`; `3414` events; log every `16`
- independent base/+1 branches; uniform relabel-invariant add_chord
- primary metrics: `tail_delta_local_beta1_r1;tail_delta_local_beta1_r2;tail_delta_local_beta1_r3;tail_delta_cycle_density_r2`
- every primary metric is a within-branch change from its own t0 local geometry
- chord survival, local token occupancy and local event incidence are diagnostics only

## Local observable comparisons

| metric | n_pairs | median_beta1_base | median_beta1_plus1 | median_paired_difference | relative_median_gap | sign_consistency | holm_p | auc_separation | growth_seed_direction_match | placement_direction_match | metric_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tail_delta_local_beta1_r1 | 24 | 0.000 | 0.000 | 0.000 | 0.000 | 0.533 | 1.000 | 0.541 | 0.000 | 0.000 | not_supported |
| tail_delta_local_beta1_r2 | 24 | -0.361 | 0.000 | 0.000 | 1.000 | 0.579 | 1.000 | 0.508 | 0.000 | 0.000 | not_supported |
| tail_delta_local_beta1_r3 | 24 | 0.000 | 0.000 | 0.000 | 0.000 | 0.600 | 1.000 | 0.562 | 0.000 | 0.000 | not_supported |
| tail_delta_cycle_density_r2 | 24 | -0.004 | -0.003 | 0.008 | 0.373 | 0.609 | 1.000 | 0.542 | 0.500 | 1.000 | not_supported |

## Mechanism diagnostics

| sector | n_runs | plus1_chord_loss_rate | mean_tail_candidate_edge_presence_rate | mean_tail_local_event_rate_fixed_r2 | mean_tail_delta_local_token_fraction_r2 | global_beta1_clean_rate |
| --- | --- | --- | --- | --- | --- | --- |
| beta1_base | 24 | nan | 0.042 | 0.224 | -0.020 | 1.000 |
| beta1_plus1 | 24 | 0.042 | 0.958 | 0.230 | -0.030 | 1.000 |

## Claim adjudication

| claim_id | statement | evaluation | evidence_ref |
| --- | --- | --- | --- |
| claim.v15dz.local-sector-response | The beta1 +1 sector changes adjusted local cycle-neighborhood dynamics under band_zero_del. | unsupported | v15dz_local_observable_comparisons.csv |
| claim.v15dz.transport-beyond-chord | Any local sector response persists beyond the original chord edge. | unsupported | v15dz_sector_diagnostics.csv |
| claim.v15dz.physical-topological-charge | The beta1 sector is a physical topological charge analogous to a particle property. | unsupported | v15dz_gate_evaluation.csv:diagnosis |

## Decision

| key | value | evidence |
| --- | --- | --- |
| scope | fresh_local_cycle_neighborhood_response | runs=48; pairs=24; snapshots_per_run=215 |
| artifact_control | clean | 48 preregistered unique independent runs |
| global_beta1_conservation | pass | zero eventwise and final beta1 drift required |
| local_primary_gate | fail | passing_metrics=none |
| plus1_chord_loss_coverage | 0.042 | minimum_for_transport_claim=0.25 |
| diagnosis | no_adjusted_local_beta1_sector_response_detected | raw initial +1 offset excluded; global v15dy metrics remain negative controls |
| next_step | retire_beta1_as_dynamic_track_keep_as_conditional_sector_label | predeclared stop rule; no metric refit |

A negative result activates the preregistered stop rule for beta1 as a dynamic track. The exact conditional sector invariant remains valid independently of this response gate.
