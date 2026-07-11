# Relasjonell universgraf v0.15dw: constructor x coupling factorial gate

## Formaal og maal

`purposeRef`: `purpose://prompt.unknown`.
Candidate intake: avgjoer om target-1024 add_chord response overlever baade en relabel-invariant perturbation policy og et alternativt korrekt stochastic coupling.

| goal | metric | target | status |
| --- | --- | --- | --- |
| G1 constructor robustness | cell agreement, established gap, normalized horizon gap | >= 0.80, <= 0.20, <= 0.15 | fail |
| G2 coupling robustness | same three frozen metrics | >= 0.80, <= 0.20, <= 0.15 | fail |
| G3 next decision | allOf(G1,G2) | documented diagnosis | response_not_factorially_robust |

## Frozen scope

- target: `1024`
- growth seeds: `202;303`
- placements: `p0;p1;p2`
- fresh seed deltas: `19511;19571;19633;19697`
- constructors: `legacy_first_sorted;uniform_relabel_invariant`
- couplings: `maximal;rank`
- step budget: `3414`; log every `8`
- constructor RNG is separate from dynamic RNG; assignments were written before dynamics

## Cell outcomes

| growth_seed | placement | constructor | coupling | n_runs | label_counts | established_rate | active_cell | mean_normalized_horizon_span | mean_far_shell_share | mean_perturbed_node_drift_rel | mean_perturbed_beta1_drift_rel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 202 | 0 | legacy_first_sorted | maximal | 4 | no_far_shell_horizon:4 | 0.000 | 0 | 0.000 | 0.466 | 0.001 | 0.007 |
| 202 | 0 | legacy_first_sorted | rank | 4 | mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.000 | 0 | 0.052 | 0.623 | 0.001 | 0.007 |
| 202 | 0 | uniform_relabel_invariant | maximal | 4 | mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.000 | 0 | 0.025 | 0.347 | 0.002 | 0.007 |
| 202 | 0 | uniform_relabel_invariant | rank | 4 | established_far_shell_horizon:4 | 1.000 | 1 | 0.968 | 0.772 | 0.001 | 0.007 |
| 202 | 1 | legacy_first_sorted | maximal | 4 | established_far_shell_horizon:2;no_far_shell_horizon:2 | 0.500 | 1 | 0.449 | 0.639 | 0.002 | 0.007 |
| 202 | 1 | legacy_first_sorted | rank | 4 | established_far_shell_horizon:4 | 1.000 | 1 | 0.990 | 0.765 | 0.001 | 0.007 |
| 202 | 1 | uniform_relabel_invariant | maximal | 4 | established_far_shell_horizon:2;no_far_shell_horizon:2 | 0.500 | 1 | 0.427 | 0.648 | 0.002 | 0.007 |
| 202 | 1 | uniform_relabel_invariant | rank | 4 | established_far_shell_horizon:4 | 1.000 | 1 | 0.990 | 0.790 | 0.001 | 0.007 |
| 202 | 2 | legacy_first_sorted | maximal | 4 | no_far_shell_horizon:4 | 0.000 | 0 | 0.000 | 0.518 | 0.002 | 0.007 |
| 202 | 2 | legacy_first_sorted | rank | 4 | established_far_shell_horizon:2;late_far_shell_probe:1;no_far_shell_horizon:1 | 0.500 | 1 | 0.504 | 0.853 | 0.002 | 0.007 |
| 202 | 2 | uniform_relabel_invariant | maximal | 4 | no_far_shell_horizon:4 | 0.000 | 0 | 0.000 | 0.561 | 0.002 | 0.007 |
| 202 | 2 | uniform_relabel_invariant | rank | 4 | established_far_shell_horizon:3;no_far_shell_horizon:1 | 0.750 | 1 | 0.750 | 0.843 | 0.002 | 0.007 |
| 303 | 0 | legacy_first_sorted | maximal | 4 | no_far_shell_horizon:4 | 0.000 | 0 | 0.000 | 0.551 | 0.002 | 0.007 |
| 303 | 0 | legacy_first_sorted | rank | 4 | mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.000 | 0 | 0.006 | 0.568 | 0.003 | 0.007 |
| 303 | 0 | uniform_relabel_invariant | maximal | 4 | no_far_shell_horizon:4 | 0.000 | 0 | 0.000 | 0.521 | 0.002 | 0.007 |
| 303 | 0 | uniform_relabel_invariant | rank | 4 | established_far_shell_horizon:1;no_far_shell_horizon:3 | 0.250 | 0 | 0.250 | 0.679 | 0.003 | 0.007 |
| 303 | 1 | legacy_first_sorted | maximal | 4 | no_far_shell_horizon:4 | 0.000 | 0 | 0.000 | 0.395 | 0.001 | 0.007 |
| 303 | 1 | legacy_first_sorted | rank | 4 | no_far_shell_horizon:4 | 0.000 | 0 | 0.000 | 0.524 | 0.002 | 0.007 |
| 303 | 1 | uniform_relabel_invariant | maximal | 4 | mixed_far_shell_horizon:1;no_far_shell_horizon:3 | 0.000 | 0 | 0.160 | 0.522 | 0.002 | 0.007 |
| 303 | 1 | uniform_relabel_invariant | rank | 4 | established_far_shell_horizon:1;mixed_far_shell_horizon:1;no_far_shell_horizon:2 | 0.250 | 0 | 0.294 | 0.754 | 0.002 | 0.007 |
| 303 | 2 | legacy_first_sorted | maximal | 4 | no_far_shell_horizon:4 | 0.000 | 0 | 0.000 | 0.578 | 0.002 | 0.007 |
| 303 | 2 | legacy_first_sorted | rank | 4 | no_far_shell_horizon:4 | 0.000 | 0 | 0.000 | 0.589 | 0.001 | 0.007 |
| 303 | 2 | uniform_relabel_invariant | maximal | 4 | no_far_shell_horizon:4 | 0.000 | 0 | 0.000 | 0.575 | 0.002 | 0.007 |
| 303 | 2 | uniform_relabel_invariant | rank | 4 | no_far_shell_horizon:4 | 0.000 | 0 | 0.000 | 0.622 | 0.001 | 0.007 |

## Factor gates

| effect | fixed_level | n_paired_cells | cell_label_agreement | majority_flip_count | median_absolute_established_rate_gap | median_absolute_normalized_horizon_gap | median_absolute_perturbed_node_drift_gap | median_absolute_perturbed_beta1_drift_gap | factor_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| constructor_effect | maximal | 6 | 1.000 | 0 | 0.000 | 0.011 | 0.000 | 0.000 | stable_under_factor |
| constructor_effect | rank | 6 | 0.833 | 1 | 0.250 | 0.245 | 0.000 | 0.000 | factor_sensitive |
| coupling_effect | legacy_first_sorted | 6 | 0.833 | 1 | 0.000 | 0.029 | 0.001 | 0.000 | stable_under_factor |
| coupling_effect | uniform_relabel_invariant | 6 | 0.667 | 2 | 0.375 | 0.406 | 0.000 | 0.000 | factor_sensitive |

## Claim adjudication

| claim_id | statement | evaluation | evidence_ref |
| --- | --- | --- | --- |
| claim.v15dw.constructor-robust | The target-1024 add_chord response is robust to legacy versus uniform relabel-invariant constructor policy. | contradicted | v15dw_factor_comparisons.csv:constructor_effect |
| claim.v15dw.coupling-robust | The target-1024 add_chord damage/horizon response is robust to maximal versus rank coupling. | contradicted | v15dw_factor_comparisons.csv:coupling_effect |
| claim.v15dw.factorially-robust-response | The current far-shell response is robust enough to justify the next physics-facing gate. | unsupported | v15dw_factorial_evaluation.csv:diagnosis |

Root composition: `allOf(constructor robustness, coupling robustness)`. A failed premise makes the root unsupported; it does not prove that all local dynamics are trivial.

## Evidential separation

The joint damage/far-shell classification is factor-sensitive, while the factor contrasts keep the largest median perturbed-node drift gap at `0.000610` and the largest median perturbed-beta1 drift gap at `0.000000`.

This is evidence against treating the present far-shell observable as a robust physics-facing signal. It is not evidence that the marginal graph dynamics are identical, trivial, symmetric, or universe-like; those are separate claims requiring separately preregistered observables.

## Decision

| key | value | evidence |
| --- | --- | --- |
| scope | fresh_constructor_by_coupling_factorial | runs=96; growth_seeds=2; placements=3; seed_deltas=4 |
| artifact_control | clean | target_separated=1; requested_match=1 |
| uniform_matches_legacy_assignment_rate | 0.167 | constructor effect is informative only when uniform sampling often selects a different valid chord |
| constructor_gate | fail | maximal:agree=1.000,est_gap=0.000,horizon_gap=0.011;rank:agree=0.833,est_gap=0.250,horizon_gap=0.245 |
| coupling_gate | fail | legacy_first_sorted:agree=0.833,est_gap=0.000,horizon_gap=0.029;uniform_relabel_invariant:agree=0.667,est_gap=0.375,horizon_gap=0.406 |
| diagnosis | response_not_factorially_robust | allOf(constructor robustness, coupling robustness) with fixed thresholds |
| next_step | stop_far_shell_physics_interpretation_and_return_to_marginal_observables | deduced from failed or satisfied factor gates; no selector refit |

Marginal branch drifts are reported separately from joint damage. Constructor hygiene and coupling robustness are necessary artifact gates, not sufficient evidence for physical symmetry or a universe-like law.
