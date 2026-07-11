# Relasjonell universgraf v0.15dx: eventwise beta1 invariant gate

## Formaal og maal

`purposeRef`: `purpose://prompt.unknown`.

Test om `beta1 = E - N + C` er en eksakt global invariant som hver lokal interaksjon respekterer i anchor-regimet, og skill dette fra universal eller emergent fysikk.

| goal | target | status |
| --- | --- | --- |
| G1 anchor eventwise conservation | zero nonzero beta1 events | satisfied |
| G2 add_chord sector offset | initial and final offset exactly +1 | satisfied |
| G3 universality falsifier | observed legal deformation with nonzero beta1 delta | satisfied |

## Frozen scope

- target `1024`; anchor growth seeds `202;303`; placements `p0,p1,p2`
- fresh dynamic seed deltas `20507;20563`
- `3414` transitions per branch; branches use independent RNG and independent id allocation
- perturbed branches use the uniform relabel-invariant add_chord constructor
- deformations change only `p_triad` or `p_del` from `0.00` to `0.02`

## Algebraic transition facts

| event | graph delta | beta1 consequence | status |
| --- | --- | --- | --- |
| seed | one node plus one edge | 0 | implementation fact |
| birth/death/move/stuck | no graph change | 0 | implementation fact |
| swap | remove v-u, add v-w through u-neighbor w | 0 when component count is preserved | runtime audited |
| triad | add v-w where v-u-w already connects endpoints | +1 | runtime falsifier |
| delete | remove v-u; bridge status determines component delta | -1 or 0 | runtime audited |

These are rule-level facts. Runtime agreement checks implementation fidelity; it does not turn the identity into emergent physics.

## Regime outcomes

| regime | n_runs | zero_drift_run_rate | total_nonzero_beta1_events | total_triad_events | total_delete_events | expected_delta_violation_count |
| --- | --- | --- | --- | --- | --- | --- |
| band_zero_del | 24 | 1.000 | 0 | 0 | 0 | 0 |
| delete_002 | 4 | 0.000 | 86 | 0 | 182 | 0 |
| triad_002 | 4 | 0.000 | 188 | 188 | 0 | 0 |

## Transition deltas

| regime | event_type | n_events | delta_beta1_counts | nonzero_rate | expected_delta_match_rate |
| --- | --- | --- | --- | --- | --- |
| band_zero_del | birth | 5070 | 0:5070 | 0.000 | 1.000 |
| band_zero_del | move | 75668 | 0:75668 | 0.000 | 1.000 |
| band_zero_del | seed | 39 | 0:39 | 0.000 | 1.000 |
| band_zero_del | swap | 1159 | 0:1159 | 0.000 | 1.000 |
| delete_002 | birth | 807 | 0:807 | 0.000 | 1.000 |
| delete_002 | delete | 182 | -1:86;0:96 | 0.473 | 1.000 |
| delete_002 | move | 12463 | 0:12463 | 0.000 | 1.000 |
| delete_002 | seed | 8 | 0:8 | 0.000 | 1.000 |
| delete_002 | swap | 196 | 0:196 | 0.000 | 1.000 |
| triad_002 | birth | 793 | 0:793 | 0.000 | 1.000 |
| triad_002 | move | 12517 | 0:12517 | 0.000 | 1.000 |
| triad_002 | seed | 4 | 0:4 | 0.000 | 1.000 |
| triad_002 | swap | 154 | 0:154 | 0.000 | 1.000 |
| triad_002 | triad | 188 | 1:188 | 1.000 | 1.000 |

## Sector offsets

| growth_seed | placement | seed_delta | initial_beta1_offset | final_beta1_offset | both_branches_zero_drift |
| --- | --- | --- | --- | --- | --- |
| 202 | 0 | 20507 | 1 | 1 | 1 |
| 202 | 0 | 20563 | 1 | 1 | 1 |
| 202 | 1 | 20507 | 1 | 1 | 1 |
| 202 | 1 | 20563 | 1 | 1 | 1 |
| 202 | 2 | 20507 | 1 | 1 | 1 |
| 202 | 2 | 20563 | 1 | 1 | 1 |
| 303 | 0 | 20507 | 1 | 1 | 1 |
| 303 | 0 | 20563 | 1 | 1 | 1 |
| 303 | 1 | 20507 | 1 | 1 | 1 |
| 303 | 1 | 20563 | 1 | 1 | 1 |
| 303 | 2 | 20507 | 1 | 1 | 1 |
| 303 | 2 | 20563 | 1 | 1 | 1 |

## Claim adjudication

| claim_id | statement | evaluation | evidence_ref |
| --- | --- | --- | --- |
| claim.v15dx.anchor-beta1-invariant | Every observed independent-branch transition in band_zero_del preserves beta1 exactly. | supported | v15dx_transition_delta_summary.csv:band_zero_del |
| claim.v15dx.add-chord-sector | The uniform add_chord perturbation creates a beta1 sector offset of exactly one that is preserved by anchor dynamics. | supported | v15dx_sector_offsets.csv |
| claim.v15dx.universal-beta1-invariant | Beta1 is invariant across the broader local rule family. | contradicted | v15dx_transition_delta_summary.csv:triad_002;delete_002 |
| claim.v15dx.emergent-physics | The observed beta1 conservation is evidence of emergent universe-like physics. | unsupported | v15dx_gate_evaluation.csv:diagnosis |

## Decision

| key | value | evidence |
| --- | --- | --- |
| scope | independent_branch_eventwise_beta1 | runs=32; events=109248 |
| artifact_control | clean | pre_registered rows equal runs; independent RNG per branch |
| anchor_eventwise_conservation | pass | zero_drift_rate=1.000; nonzero_events=0 |
| add_chord_sector_offset | pass | paired_assignments=12; required offset=1 at initial and final |
| triad_deformation_falsifier | pass | triad_events=188; nonzero_events=188 |
| delete_deformation_coverage | pass | delete_events=182; nonzero_events=86 |
| universal_beta1_invariance | contradicted | one valid nonzero deformation event is a counterexample |
| diagnosis | conditional_exact_beta1_sector_invariant_not_universal | anchor conservation and sector offset are conditional on the frozen rule family |
| next_step | derive_sector_mechanism_then_test_sector_conditioned_dynamics | do not relabel algebraic conservation as emergent physics |

Den presise evidensstatusen er en betinget topologisk sektor-invariant i `band_zero_del`. Den er global i den smale betydningen at alle tillatte anchor-overganger respekterer den. Triad-deformasjonen viser samtidig at den ikke er en universell lov for hele regelfamilien.
