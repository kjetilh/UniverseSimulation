# UniverseSimulation v16ac: isolated local-seed adapter gate

## Question

Does the frozen exposure-matched local seed clock remove the exact scheduler-locality blocker from v16a while preserving event support, relabel covariance, and disjoint-event commutation?

## Evidential separation

- Architecture fact: the adapter sets total seed rate to `rho_seed * H`, where `H` is the number of currently available seed hosts; the unchanged uniform kernel therefore gives each host rate `rho_seed`.
- Prior dynamical artifact: v16ab tested the frozen value on fresh scheduler runs. v16ac does not refit it and runs no large dynamical ensemble.
- New finite result: v16ac reruns the complete v16a graph-atlas commutation and hazard census through the isolated adapter.
- Physics status: no Lorentz, spacetime, particle, entanglement, or universal-causality claim is tested here.

## Frozen source chain

| check | observed | required | status |
| --- | --- | --- | --- |
| v16aa_selected_candidate | exposure_matched_local | exposure_matched_local | pass |
| v16aa_frozen_rate | 0.000504 | 0.000504 | pass |
| v16ab_preregistration_rows | 48.000000 | 48.000000 | pass |
| v16ab_preregistration_digest | 371ed15f495f76429f6a9e568032d4f45d1e1a6cf51b3704de021a7cae98c49e | 371ed15f495f76429f6a9e568032d4f45d1e1a6cf51b3704de021a7cae98c49e | pass |
| v16ab_preregistered_rate | 0.000504 | 0.000504 | pass |
| v16ab_fresh_holdout_decision | promote_local_seed_clock_to_v16a_rerun | promote_local_seed_clock_to_v16a_rerun | pass |
| v16ab_all_frozen_subgates | 0.000000 | 0.000000 | pass |

The adapter rate is fixed at `0.0005039538147742117`. The v16ab pre-registration digest is `371ed15f495f76429f6a9e568032d4f45d1e1a6cf51b3704de021a7cae98c49e`. No fitting path exists in this script.

## Adapter boundary

`LocalSeedClockAdapter` delegates kernels and concrete transformations to the existing runtime. It changes only `family_rates()["seed"]`. The core file `relational_universe_local_max_coupling_lab.py` is imported, not edited or overwritten by the run.

For token-bearing states, `H=K` and each `seed_tid` has intensity `(rho_seed*K)*(1/K)=rho_seed`. For token-free states, `H=N` and each `seed_node` has intensity `(rho_seed*N)*(1/N)=rho_seed`.

## Event support and local hazards

| event_kind | anchor_active | selection_read | bounded_local_clock | rule_variant |
| --- | --- | --- | --- | --- |
| seed | 1.000000 | fixed host-local rho_seed; no global K/N normalization | 1.000000 | exposure_matched_local_seed_clock |
| birth | 1.000000 | parent degree | 1.000000 | unchanged_anchor_family |
| death | 0.000000 | host degree plus global min_tokens guard | 0.000000 | unchanged_anchor_family |
| stuck | 1.000000 | host degree | 1.000000 | unchanged_anchor_family |
| move | 1.000000 | radius-2 neighborhood | 1.000000 | unchanged_anchor_family |
| delete | 0.000000 | radius-2 neighborhood | 1.000000 | unchanged_anchor_family |
| triad | 0.000000 | radius-2 neighborhood | 1.000000 | unchanged_anchor_family |
| swap | 1.000000 | radius-2 neighborhood | 1.000000 | unchanged_anchor_family |

Runtime formula audit:

| event_kind | anchor_active | runtime_formula_samples | formula_max_abs_error | formula_exact | bounded_local_clock | status |
| --- | --- | --- | --- | --- | --- | --- |
| seed | 1.000000 | 59999.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |
| birth | 1.000000 | 59999.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |
| death | 0.000000 | 53222.000000 | 0.000000 | 1.000000 | 0.000000 | inactive_anchor_global_guard |
| stuck | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |
| move | 1.000000 | 189272.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |
| delete | 0.000000 | 183759.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |
| triad | 0.000000 | 231514.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |
| swap | 1.000000 | 231514.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |

Seed formula maximum absolute error was `0.000000000000000`. The inactive death family retains its global minimum-token guard; it is not part of the active anchor gate.

## Remote-context and relabel controls

| context | event_kind | base_intensity | remote_intensity | absolute_difference | remote_invariant | required_for_active_anchor_gate |
| --- | --- | --- | --- | --- | --- | --- |
| seed_tid | seed | 0.000504 | 0.000504 | 0.000000 | 1.000000 | 1.000000 |
| seed_node | seed | 0.000504 | 0.000504 | 0.000000 | 1.000000 | 1.000000 |
| birth_tid | birth | 0.020000 | 0.020000 | 0.000000 | 1.000000 | 1.000000 |
| stuck | stuck | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 |
| move | move | 0.400000 | 0.400000 | 0.000000 | 1.000000 | 1.000000 |
| delete | delete | 0.200000 | 0.200000 | 0.000000 | 1.000000 | 0.000000 |
| triad | triad | 0.200000 | 0.200000 | 0.000000 | 1.000000 | 0.000000 |
| swap | swap | 0.200000 | 0.200000 | 0.000000 | 1.000000 | 1.000000 |

All `6` active-anchor remote-context probes were invariant. This includes both `seed_tid` and token-free `seed_node` hosts.

| connected_unlabeled_graphs | states | descriptor_comparisons | max_abs_error | failures | relabel_pass |
| --- | --- | --- | --- | --- | --- |
| 992.000000 | 33385.000000 | 59999.000000 | 0.000000 | 0.000000 | 1.000000 |

## Full v16a rerun

The rerun covered `992` connected unlabeled graph-atlas graphs, `33385` microstates, and `7123450` declared-disjoint event pairs. It found `0` commutation failures and `0` transformation relabel failures.

| left_kind | right_kind | declared_disjoint | isomorphic_commutation | relabel_pass | failures |
| --- | --- | --- | --- | --- | --- |
| birth | birth | 166467.000000 | 166467.000000 | 166467.000000 | 0.000000 |
| birth | death | 106444.000000 | 106444.000000 | 106444.000000 | 0.000000 |
| birth | delete | 323630.000000 | 323630.000000 | 323630.000000 | 0.000000 |
| birth | move | 335912.000000 | 335912.000000 | 335912.000000 | 0.000000 |
| birth | seed | 452932.000000 | 452932.000000 | 452932.000000 | 0.000000 |
| birth | stuck | 2.000000 | 2.000000 | 2.000000 | 0.000000 |
| birth | swap | 411048.000000 | 411048.000000 | 411048.000000 | 0.000000 |
| birth | triad | 411048.000000 | 411048.000000 | 411048.000000 | 0.000000 |
| death | death | 26611.000000 | 26611.000000 | 26611.000000 | 0.000000 |
| death | delete | 161815.000000 | 161815.000000 | 161815.000000 | 0.000000 |
| death | move | 167956.000000 | 167956.000000 | 167956.000000 | 0.000000 |
| death | seed | 106444.000000 | 106444.000000 | 106444.000000 | 0.000000 |
| death | swap | 205524.000000 | 205524.000000 | 205524.000000 | 0.000000 |
| death | triad | 205524.000000 | 205524.000000 | 205524.000000 | 0.000000 |
| delete | delete | 103625.000000 | 103625.000000 | 103625.000000 | 0.000000 |
| delete | move | 488748.000000 | 488748.000000 | 488748.000000 | 0.000000 |
| delete | seed | 202014.000000 | 202014.000000 | 202014.000000 | 0.000000 |
| delete | swap | 154296.000000 | 154296.000000 | 154296.000000 | 0.000000 |
| delete | triad | 263316.000000 | 263316.000000 | 263316.000000 | 0.000000 |
| move | move | 281932.000000 | 281932.000000 | 281932.000000 | 0.000000 |
| move | seed | 335912.000000 | 335912.000000 | 335912.000000 | 0.000000 |
| move | swap | 585588.000000 | 585588.000000 | 585588.000000 | 0.000000 |
| move | triad | 663558.000000 | 663558.000000 | 663558.000000 | 0.000000 |
| seed | seed | 79380.000000 | 79380.000000 | 79380.000000 | 0.000000 |
| seed | stuck | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| seed | swap | 203128.000000 | 203128.000000 | 203128.000000 | 0.000000 |
| seed | triad | 255108.000000 | 255108.000000 | 255108.000000 | 0.000000 |
| swap | swap | 38840.000000 | 38840.000000 | 38840.000000 | 0.000000 |
| swap | triad | 198420.000000 | 198420.000000 | 198420.000000 | 0.000000 |
| triad | triad | 188228.000000 | 188228.000000 | 188228.000000 | 0.000000 |

The adapter changes event timing, not concrete event transformations. `v16ac_v16a_parity.csv` nevertheless checks every aggregate transformation count against the original v16a output; this prevents a changed census from masquerading as a scheduler-only rerun.

Parity rows passing: `30/30`.

## Gate decision

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| frozen_source_chain | pass | 7.000000 | 7.000000 | continue |
| support_schema_coverage | pass | 8.000000 | 8.000000 | continue |
| nontrivial_disjoint_coverage | pass | pairs=7123450;active_pair_kinds=11 | >=1000 pairs;>=3 active pair kinds | continue |
| exact_disjoint_commutation | pass | 0.000000 | 0.000000 | continue |
| transformation_relabel_transport | pass | 0.000000 | 0.000000 | continue |
| runtime_hazard_formula | pass | 0.000000 | <=1e-12 | continue |
| bounded_local_clock_active_anchor | pass |  | none | continue |
| active_remote_context_invariance | pass | 0.000000 | <=1e-12 | continue |
| seed_rate_relabel_covariance | pass | 0.000000 | 0.000000 | continue |
| v16a_target_parity | pass | graphs=992;states=33385;pairs=7123450 | graphs=992;states=33385;pairs=7123450 | continue |
| v16a_pair_aggregate_parity | pass | 30.000000 | 30.000000 | continue |
| v16ac_overall | pass_adapter_to_v16b | 1.000000 | 1.000000 | design_v16b_with_isolated_adapter |

Overall status: `pass_adapter_to_v16b`.

## Interpretation

If the overall gate passes, the exact v16a scheduler-locality blocker is removed for this isolated rule variant. Together with v16ab, that is enough to justify the next architecture experiment: a narrow intrinsic event-DAG gate using this adapter.

It is not enough to promote the adapter to the final project anchor. The local rate was originally calibrated from older trajectories, the fresh holdout was scheduler-scale rather than multiscale physics validation, and no emergent geometry claim follows from local clocks plus commutation alone.

## Next gate

Build v16b around an event DAG whose vertices are executed concrete events and whose directed edges are induced only by declared read/write dependence. Test relabel covariance, independence of disjoint event order, antichain structure, and whether coarse causal depth is stable across matched runs. Keep the adapter isolated and keep the old global scheduler as a diagnostic control.
