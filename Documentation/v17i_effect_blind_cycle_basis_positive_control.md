# v17i effect-blind cycle-basis accessibility positive control

Status: `v17i_pair_basis_positive_control_qualified`.

## Frozen design

The exact v16z whole-cycle decomposition for each frozen start pair is treated as a pair-derived hypercube basis. A fair bit mask toggles any subset as one algebraic block. This is an engineered positive control that knows both starts; it is not a state-independent proposal or candidate global null.

## Results

The six bases contained `343-384` disjoint whole cycles. Full-mask single-block replay connected both directions in `6/6`. Complement-coupled masks produced exact endpoint identity in `96/96`, and independent fair masks preserved endpoint integrity in `192/192`.

Finite cross/within median-distance ratios were `0.986207-1.004213`; all `6/6` lay in the frozen `0.85-1.15` positive-control interval.

The `stage` column in inherited per-source prefixes remains `v17h`; filenames, preregistration, mask seeds and gate identifiers are v17i. This is a disclosed provenance-label artifact and does not enter any mask, endpoint or distance computation.

## Gates

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| effect_blind_integrity | pass | spectrum=0;effect=0 | 0;0 | continue |
| frozen_cycle_basis_and_single_block_accessibility | pass | 6/6 | 6/6 | continue |
| exact_complement_coupled_endpoint_identity | pass | 96/96 | 96/96 | continue |
| independent_uniform_mask_integrity | pass | 192/192 | 192/192 | continue |
| finite_cycle_exercise | pass | 6/6 | 6/6 | continue |
| finite_cross_start_distance_positive_control | pass | 6/6 | 6/6;ratio=0.85-1.15 | instrumentation_supported |
| v17i_overall | v17i_pair_basis_positive_control_qualified | exclusion=1;basis=6/6;coupling=96/96;integrity=192/192;exercise=6/6;distance=6/6 | 1;6/6;96/96;192/192;6/6;6/6 | v17i_pair_basis_positive_control_qualified |

## Claim boundary

The pass validates the distance instrumentation under an exact pair-engineered accessibility measure. It does not qualify a reusable sampler, prove global connectivity or mixing, or test the source effect, geometry or physics.
