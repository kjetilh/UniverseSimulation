# Beta1 bookkeeping audit

Generated: `2026-09-04T13:42:57Z`

## Result

This is a measurement of the two production perturbation constructors, not a repair.
The measured claim is limited to the source-declared v15 configuration schedule below.
It is not a physics claim and does not by itself invalidate v15.

| constructor | calls | fallback | fallback_rate | noop | noop_rate | mismatch | mismatch_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord | 791 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | 791 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |

A mismatch means recorded `delta_core.beta1` differed from actual `E - N + C`.
Fallback and no-op are measured at constructor entry around the imported production
`choose_center_token`; actual beta1 is recomputed independently with NetworkX before
and after each call.

## Preregistered outcome interpretation

The discrepancy rate is approximately zero in this measured schedule; the
tested v15 bookkeeping is cleared for this exact scope.

## Actual v15 configuration schedule

The tool imports every `relational_universe_v15*.py` module and reads its declared
target(s), growth seed(s), placement(s), perturbation family and, where present,
seed-delta schedule. This includes explicit validation of v15cz/v15da/v15dk/v15dr.
All audited bases use the v15 deep ensemble and `fast_balanced` growth regime.
The source-declared schedule has 791 configurations and is repeated
1 time(s) for each constructor. Each constructor is tested on every start
configuration even when its source module declared only one of the two families.
Seed-delta affects the later run RNG, not the deterministic constructor on the base
state; keeping every declared seed-delta preserves the program schedule's call weighting.

Exact imported growth parameters:

```json
{
  "hold_steps_deep": 90,
  "hold_steps_light": 30,
  "max_steps_factor": 10.0,
  "min_fraction": 0.08,
  "name": "fast_balanced",
  "phase1": {
    "min_tokens": 1,
    "move_rate": 0.2,
    "prune_rate": 0.003,
    "seed_rate": 1.0,
    "seed_triangle_prob": 0.08,
    "swap_rate": 0.02,
    "token_birth_rate": 0.012,
    "token_death_rate": 0.006,
    "triad_rate": 0.03
  },
  "phase2": {
    "min_tokens": 1,
    "move_rate": 0.5,
    "prune_rate": 0.004,
    "seed_rate": 0.2,
    "seed_triangle_prob": 0.04,
    "swap_rate": 0.03,
    "token_birth_rate": 0.008,
    "token_death_rate": 0.008,
    "triad_rate": 0.05
  },
  "rel_tol": 0.1
}
```

| ensemble | burnin_label | target_nodes | growth_seed | realized_nodes | realized_edges | realized_tokens | first_hit_step | growth_steps_executed | target_low | target_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| natural48_deep | deep | 48 | 101 | 48 | 52 | 7 | nan | 1932.0 | 43.0 | 53.0 |
| natural48_deep | deep | 48 | 202 | 48 | 49 | 7 | nan | 1932.0 | 43.0 | 53.0 |
| natural96_deep | deep | 96 | 101 | 96 | 106 | 7 | nan | 3646.0 | 86.0 | 106.0 |
| natural96_deep | deep | 96 | 202 | 96 | 109 | 8 | nan | 3646.0 | 86.0 | 106.0 |
| natural192_deep | deep | 192 | 202 | 192 | 218 | 10 | nan | 7068.0 | 172.0 | 212.0 |
| natural384_deep | deep | 384 | 202 | 384 | 425 | 15 | nan | 13820.0 | 345.0 | 423.0 |
| natural768_deep | deep | 768 | 202 | 768 | 869 | 13 | nan | 27193.0 | 691.0 | 845.0 |
| natural896_deep | deep | 896 | 202 | 896 | 1013 | 17 | nan | 31631.0 | 806.0 | 986.0 |
| natural1024_deep | deep | 1024 | 202 | 1024 | 1166 | 22 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 303 | 1024 | 1159 | 10 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 404 | 1024 | 1147 | 22 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 505 | 1024 | 1134 | 12 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 606 | 1024 | 1160 | 14 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 707 | 1024 | 1151 | 16 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 808 | 1024 | 1141 | 18 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 909 | 1024 | 1166 | 12 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 1001 | 1024 | 1157 | 16 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 1103 | 1024 | 1145 | 17 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 1201 | 1024 | 1157 | 17 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 1301 | 1024 | 1174 | 9 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 1409 | 1024 | 1155 | 11 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 1511 | 1024 | 1178 | 23 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 1601 | 1024 | 1138 | 17 | nan | 36064.0 | 921.0 | 1127.0 |
| natural1024_deep | deep | 1024 | 1709 | 1024 | 1146 | 14 | nan | 36064.0 | 921.0 | 1127.0 |

## Distribution by realized configuration size

| constructor | configuration_size | calls | fallback | fallback_rate | noop | noop_rate | mismatch | mismatch_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord | 48 | 44 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | 96 | 102 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | 192 | 48 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | 384 | 36 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | 768 | 84 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | 896 | 20 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | 1024 | 457 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | 48 | 44 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | 96 | 102 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | 192 | 48 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | 384 | 36 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | 768 | 84 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | 896 | 20 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | 1024 | 457 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |

## Distribution by source configuration

| constructor | source_program | target_nodes | growth_seed | center_token_index | calls | fallback | fallback_rate | noop | noop_rate | mismatch | mismatch_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord | relational_universe_v15bs_add_chord_vs_local_swap_p3_carrier_compare | 96 | 202 | 3 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bt_same_locus_carrier_timing_lab | 96 | 202 | 3 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bu_same_locus_carrier_occupancy_spectrum_lab | 96 | 202 | 3 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bv_family_structure_symmetry_lab | 96 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bv_family_structure_symmetry_lab | 96 | 202 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bv_family_structure_symmetry_lab | 96 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bv_family_structure_symmetry_lab | 96 | 202 | 3 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bw_family_structure_holdout | 96 | 202 | 0 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bw_family_structure_holdout | 96 | 202 | 1 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bw_family_structure_holdout | 96 | 202 | 2 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bw_family_structure_holdout | 96 | 202 | 3 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bx_scale_jump_family_probe | 192 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bx_scale_jump_family_probe | 192 | 202 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bx_scale_jump_family_probe | 192 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bx_scale_jump_family_probe | 192 | 202 | 3 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15by_target192_plateau_holdout | 192 | 202 | 0 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15by_target192_plateau_holdout | 192 | 202 | 1 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15by_target192_plateau_holdout | 192 | 202 | 2 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15by_target192_plateau_holdout | 192 | 202 | 3 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bz_target384_family_probe | 384 | 202 | 0 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bz_target384_family_probe | 384 | 202 | 1 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bz_target384_family_probe | 384 | 202 | 2 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15bz_target384_family_probe | 384 | 202 | 3 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ca_target192_radial_occupancy_mechanism_lab | 192 | 202 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ca_target192_radial_occupancy_mechanism_lab | 192 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cb_target384_candidate_holdout | 384 | 202 | 0 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cb_target384_candidate_holdout | 384 | 202 | 1 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cb_target384_candidate_holdout | 384 | 202 | 2 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cb_target384_candidate_holdout | 384 | 202 | 3 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cc_target384_shell_turnover_observable | 384 | 202 | 0 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cc_target384_shell_turnover_observable | 384 | 202 | 1 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cc_target384_shell_turnover_observable | 384 | 202 | 2 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cc_target384_shell_turnover_observable | 384 | 202 | 3 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cd_target768_family_probe | 768 | 202 | 0 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cd_target768_family_probe | 768 | 202 | 1 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cd_target768_family_probe | 768 | 202 | 2 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cd_target768_family_probe | 768 | 202 | 3 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ce_target768_plateau_holdout | 768 | 202 | 0 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ce_target768_plateau_holdout | 768 | 202 | 1 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ce_target768_plateau_holdout | 768 | 202 | 2 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ce_target768_plateau_holdout | 768 | 202 | 3 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cf_target768_support_locus_mechanism_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cf_target768_support_locus_mechanism_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cg_target768_far_shell_horizon_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cg_target768_far_shell_horizon_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ci_target768_p2_horizon_genealogy_mechanism_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ci_target768_p2_horizon_genealogy_mechanism_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cj_target768_outer_occupancy_concentration_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cj_target768_outer_occupancy_concentration_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ck_target768_outer_feeder_flux_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ck_target768_outer_feeder_flux_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cl_target768_inner_gate_global_budget_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cl_target768_inner_gate_global_budget_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cm_target768_local_trigger_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cm_target768_local_trigger_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cn_p2_horizon_scale_holdout | 768 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cn_p2_horizon_scale_holdout | 768 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cn_p2_horizon_scale_holdout | 1024 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cn_p2_horizon_scale_holdout | 1024 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cp_target1024_scaled_budget_p2_horizon | 1024 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cp_target1024_scaled_budget_p2_horizon | 1024 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cq_intermediate_scale_p2_horizon | 896 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cq_intermediate_scale_p2_horizon | 896 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cu_add_chord_placement_response_map | 896 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cu_add_chord_placement_response_map | 896 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cu_add_chord_placement_response_map | 896 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cu_add_chord_placement_response_map | 896 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cu_add_chord_placement_response_map | 1024 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cu_add_chord_placement_response_map | 1024 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cu_add_chord_placement_response_map | 1024 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cu_add_chord_placement_response_map | 1024 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cv_add_chord_winning_placement_mechanism_probe | 896 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cv_add_chord_winning_placement_mechanism_probe | 896 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cv_add_chord_winning_placement_mechanism_probe | 1024 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cv_add_chord_winning_placement_mechanism_probe | 1024 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split | 896 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split | 896 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split | 1024 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split | 1024 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cx_p1_1024_genealogy_holdout | 1024 | 202 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15cz_pre_registered_continuous_intensity_holdout | 1024 | 202 | 1 | 24 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15da_frozen_intensity_placement_contrast | 1024 | 202 | 0 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15da_frozen_intensity_placement_contrast | 1024 | 202 | 1 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15da_frozen_intensity_placement_contrast | 1024 | 202 | 2 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dd_direct_route_entry_retention_lab | 1024 | 202 | 0 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dd_direct_route_entry_retention_lab | 1024 | 202 | 1 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dd_direct_route_entry_retention_lab | 1024 | 202 | 2 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dg_boundary_mass_holdout | 1024 | 202 | 0 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dg_boundary_mass_holdout | 1024 | 202 | 1 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dg_boundary_mass_holdout | 1024 | 202 | 2 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dh_boundary_mass_growth_seed_holdout | 1024 | 303 | 0 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dh_boundary_mass_growth_seed_holdout | 1024 | 303 | 1 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dh_boundary_mass_growth_seed_holdout | 1024 | 303 | 2 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dk_pre_registered_support_rank_holdout | 1024 | 404 | 0 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dk_pre_registered_support_rank_holdout | 1024 | 404 | 1 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dk_pre_registered_support_rank_holdout | 1024 | 404 | 2 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 303 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 303 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 303 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 404 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 404 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 404 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dm_frozen_return_probability_holdout | 1024 | 505 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dm_frozen_return_probability_holdout | 1024 | 505 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dm_frozen_return_probability_holdout | 1024 | 505 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 606 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 606 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 606 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 707 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 707 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 707 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 808 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 808 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 808 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 909 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 909 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 909 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1001 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1001 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1001 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1103 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1103 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1103 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1201 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1201 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1201 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1301 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1301 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1301 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1409 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1409 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1409 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1511 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1511 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1511 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1601 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1601 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1601 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1709 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1709 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1709 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 303 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 303 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 303 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 404 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 404 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 404 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 505 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 505 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 505 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 606 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 606 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 606 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 707 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 707 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 707 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 808 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 808 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 808 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 909 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 909 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 909 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1001 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1001 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1001 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1103 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1103 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1103 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1201 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1201 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1201 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1301 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1301 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1301 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1409 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1409 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1409 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1511 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1511 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1511 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1601 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1601 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1601 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1709 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1709 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1709 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 303 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 303 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 303 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 404 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 404 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 404 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 505 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 505 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 505 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 606 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 606 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 606 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 707 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 707 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 707 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 808 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 808 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 808 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 909 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 909 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 909 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1001 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1001 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1001 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1103 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1103 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1103 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1201 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1201 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1201 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1301 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1301 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1301 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1409 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1409 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1409 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1511 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1511 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1511 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1601 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1601 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1601 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1709 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1709 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1709 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 6 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 7 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 8 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 9 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 10 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 11 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 6 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 7 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 8 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 9 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 10 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 11 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 6 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 7 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 8 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 9 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 10 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 11 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 6 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 7 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 8 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 9 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 10 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 11 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 48 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 48 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 48 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 48 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 48 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 48 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 48 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 48 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 96 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 96 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 96 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 96 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 96 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 96 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 96 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| add_chord | relational_universe_v15q_single_defect_recurrence_lab | 96 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bs_add_chord_vs_local_swap_p3_carrier_compare | 96 | 202 | 3 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bt_same_locus_carrier_timing_lab | 96 | 202 | 3 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bu_same_locus_carrier_occupancy_spectrum_lab | 96 | 202 | 3 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bv_family_structure_symmetry_lab | 96 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bv_family_structure_symmetry_lab | 96 | 202 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bv_family_structure_symmetry_lab | 96 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bv_family_structure_symmetry_lab | 96 | 202 | 3 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bw_family_structure_holdout | 96 | 202 | 0 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bw_family_structure_holdout | 96 | 202 | 1 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bw_family_structure_holdout | 96 | 202 | 2 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bw_family_structure_holdout | 96 | 202 | 3 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bx_scale_jump_family_probe | 192 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bx_scale_jump_family_probe | 192 | 202 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bx_scale_jump_family_probe | 192 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bx_scale_jump_family_probe | 192 | 202 | 3 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15by_target192_plateau_holdout | 192 | 202 | 0 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15by_target192_plateau_holdout | 192 | 202 | 1 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15by_target192_plateau_holdout | 192 | 202 | 2 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15by_target192_plateau_holdout | 192 | 202 | 3 | 6 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bz_target384_family_probe | 384 | 202 | 0 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bz_target384_family_probe | 384 | 202 | 1 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bz_target384_family_probe | 384 | 202 | 2 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15bz_target384_family_probe | 384 | 202 | 3 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ca_target192_radial_occupancy_mechanism_lab | 192 | 202 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ca_target192_radial_occupancy_mechanism_lab | 192 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cb_target384_candidate_holdout | 384 | 202 | 0 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cb_target384_candidate_holdout | 384 | 202 | 1 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cb_target384_candidate_holdout | 384 | 202 | 2 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cb_target384_candidate_holdout | 384 | 202 | 3 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cc_target384_shell_turnover_observable | 384 | 202 | 0 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cc_target384_shell_turnover_observable | 384 | 202 | 1 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cc_target384_shell_turnover_observable | 384 | 202 | 2 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cc_target384_shell_turnover_observable | 384 | 202 | 3 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cd_target768_family_probe | 768 | 202 | 0 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cd_target768_family_probe | 768 | 202 | 1 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cd_target768_family_probe | 768 | 202 | 2 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cd_target768_family_probe | 768 | 202 | 3 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ce_target768_plateau_holdout | 768 | 202 | 0 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ce_target768_plateau_holdout | 768 | 202 | 1 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ce_target768_plateau_holdout | 768 | 202 | 2 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ce_target768_plateau_holdout | 768 | 202 | 3 | 3 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cf_target768_support_locus_mechanism_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cf_target768_support_locus_mechanism_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cg_target768_far_shell_horizon_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cg_target768_far_shell_horizon_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ci_target768_p2_horizon_genealogy_mechanism_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ci_target768_p2_horizon_genealogy_mechanism_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cj_target768_outer_occupancy_concentration_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cj_target768_outer_occupancy_concentration_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ck_target768_outer_feeder_flux_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ck_target768_outer_feeder_flux_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cl_target768_inner_gate_global_budget_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cl_target768_inner_gate_global_budget_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cm_target768_local_trigger_lab | 768 | 202 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cm_target768_local_trigger_lab | 768 | 202 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cn_p2_horizon_scale_holdout | 768 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cn_p2_horizon_scale_holdout | 768 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cn_p2_horizon_scale_holdout | 1024 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cn_p2_horizon_scale_holdout | 1024 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cp_target1024_scaled_budget_p2_horizon | 1024 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cp_target1024_scaled_budget_p2_horizon | 1024 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cq_intermediate_scale_p2_horizon | 896 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cq_intermediate_scale_p2_horizon | 896 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cu_add_chord_placement_response_map | 896 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cu_add_chord_placement_response_map | 896 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cu_add_chord_placement_response_map | 896 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cu_add_chord_placement_response_map | 896 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cu_add_chord_placement_response_map | 1024 | 202 | 0 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cu_add_chord_placement_response_map | 1024 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cu_add_chord_placement_response_map | 1024 | 202 | 2 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cu_add_chord_placement_response_map | 1024 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cv_add_chord_winning_placement_mechanism_probe | 896 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cv_add_chord_winning_placement_mechanism_probe | 896 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cv_add_chord_winning_placement_mechanism_probe | 1024 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cv_add_chord_winning_placement_mechanism_probe | 1024 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split | 896 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split | 896 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split | 1024 | 202 | 1 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split | 1024 | 202 | 3 | 2 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cx_p1_1024_genealogy_holdout | 1024 | 202 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15cz_pre_registered_continuous_intensity_holdout | 1024 | 202 | 1 | 24 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15da_frozen_intensity_placement_contrast | 1024 | 202 | 0 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15da_frozen_intensity_placement_contrast | 1024 | 202 | 1 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15da_frozen_intensity_placement_contrast | 1024 | 202 | 2 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dd_direct_route_entry_retention_lab | 1024 | 202 | 0 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dd_direct_route_entry_retention_lab | 1024 | 202 | 1 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dd_direct_route_entry_retention_lab | 1024 | 202 | 2 | 12 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dg_boundary_mass_holdout | 1024 | 202 | 0 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dg_boundary_mass_holdout | 1024 | 202 | 1 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dg_boundary_mass_holdout | 1024 | 202 | 2 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dh_boundary_mass_growth_seed_holdout | 1024 | 303 | 0 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dh_boundary_mass_growth_seed_holdout | 1024 | 303 | 1 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dh_boundary_mass_growth_seed_holdout | 1024 | 303 | 2 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dk_pre_registered_support_rank_holdout | 1024 | 404 | 0 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dk_pre_registered_support_rank_holdout | 1024 | 404 | 1 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dk_pre_registered_support_rank_holdout | 1024 | 404 | 2 | 8 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 303 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 303 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 303 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 404 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 404 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dl_base_landscape_morphology_synthesis | 1024 | 404 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dm_frozen_return_probability_holdout | 1024 | 505 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dm_frozen_return_probability_holdout | 1024 | 505 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dm_frozen_return_probability_holdout | 1024 | 505 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 606 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 606 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 606 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 707 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 707 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dp_active_set_type_guard_holdout | 1024 | 707 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 808 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 808 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 808 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 909 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 909 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 909 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1001 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1001 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1001 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1103 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1103 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dr_active_set_taxonomy_mapper_holdout | 1024 | 1103 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1201 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1201 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1201 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1301 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1301 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1301 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1409 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1409 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1409 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1511 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1511 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1511 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1601 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1601 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1601 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1709 | 0 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1709 | 1 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15ds_active_set_landscape_atlas | 1024 | 1709 | 2 | 4 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 303 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 303 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 303 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 404 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 404 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 404 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 505 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 505 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 505 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 606 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 606 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 606 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 707 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 707 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 707 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 808 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 808 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 808 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 909 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 909 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 909 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1001 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1001 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1001 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1103 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1103 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1103 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1201 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1201 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1201 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1301 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1301 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1301 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1409 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1409 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1409 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1511 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1511 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1511 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1601 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1601 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1601 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1709 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1709 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15du_relabel_symmetry_gate | 1024 | 1709 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 303 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 303 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 303 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 404 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 404 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 404 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 505 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 505 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 505 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 606 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 606 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 606 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 707 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 707 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 707 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 808 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 808 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 808 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 909 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 909 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 909 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1001 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1001 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1001 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1103 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1103 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1103 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1201 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1201 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1201 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1301 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1301 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1301 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1409 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1409 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1409 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1511 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1511 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1511 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1601 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1601 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1601 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1709 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1709 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15dv_relabel_invariant_chord_constructor | 1024 | 1709 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 101 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 48 | 202 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 101 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15m_single_defect_survival_lab | 96 | 202 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 6 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 7 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 8 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 9 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 10 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 101 | 11 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 6 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 7 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 8 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 9 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 10 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 48 | 202 | 11 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 6 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 7 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 8 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 9 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 10 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 101 | 11 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 4 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 5 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 6 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 7 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 8 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 9 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 10 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15n_token_shift_fragility_lab | 96 | 202 | 11 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 48 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 48 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 48 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 48 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 48 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 48 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 48 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 48 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 96 | 101 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 96 | 101 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 96 | 101 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 96 | 101 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 96 | 202 | 0 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 96 | 202 | 1 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 96 | 202 | 2 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |
| local_swap | relational_universe_v15q_single_defect_recurrence_lab | 96 | 202 | 3 | 1 | 0 | 0.000000% | 0 | 0.000000% | 0 | 0.000000% |

## Import inventory

Among `relational_universe_v15*.py`, 30 files import
`relational_universe_local_max_coupling_lab` directly and 88 additional files reach it
transitively (118 total). This is static module reachability, not proof
that every module invokes both constructors on every control-flow path.

### Direct imports

- `relational_universe_v15_defect_lifetime_lab.py`
- `relational_universe_v15ae_add_chord_shell_topology_lab.py`
- `relational_universe_v15b_add_chord_collision_lab.py`
- `relational_universe_v15ca_target192_radial_occupancy_mechanism_lab.py`
- `relational_universe_v15cc_target384_shell_turnover_observable.py`
- `relational_universe_v15cg_target768_far_shell_horizon_lab.py`
- `relational_universe_v15ch_target768_local_swap_p2_horizon_holdout.py`
- `relational_universe_v15ci_target768_p2_horizon_genealogy_mechanism_lab.py`
- `relational_universe_v15cj_target768_outer_occupancy_concentration_lab.py`
- `relational_universe_v15ck_target768_outer_feeder_flux_lab.py`
- `relational_universe_v15cl_target768_inner_gate_global_budget_lab.py`
- `relational_universe_v15cm_target768_local_trigger_lab.py`
- `relational_universe_v15cn_p2_horizon_scale_holdout.py`
- `relational_universe_v15cv_add_chord_winning_placement_mechanism_probe.py`
- `relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split.py`
- `relational_universe_v15cx_p1_1024_genealogy_holdout.py`
- `relational_universe_v15cz_pre_registered_continuous_intensity_holdout.py`
- `relational_universe_v15da_frozen_intensity_placement_contrast.py`
- `relational_universe_v15dd_direct_route_entry_retention_lab.py`
- `relational_universe_v15dh_boundary_mass_growth_seed_holdout.py`
- `relational_universe_v15dk_pre_registered_support_rank_holdout.py`
- `relational_universe_v15dl_base_landscape_morphology_synthesis.py`
- `relational_universe_v15du_relabel_symmetry_gate.py`
- `relational_universe_v15dv_relabel_invariant_chord_constructor.py`
- `relational_universe_v15dw_constructor_coupling_factorial_gate.py`
- `relational_universe_v15dx_eventwise_beta1_invariant_gate.py`
- `relational_universe_v15dy_sector_conditioned_marginal_response_gate.py`
- `relational_universe_v15dz_local_sector_transport_gate.py`
- `relational_universe_v15g_collision_genealogy_lab.py`
- `relational_universe_v15q_single_defect_recurrence_lab.py`

### Transitive-only imports

- `relational_universe_v15aa_case_trigger_holdout.py`
- `relational_universe_v15ab_add_chord_cycle_lag_lab.py`
- `relational_universe_v15ac_add_chord_core_shell_lab.py`
- `relational_universe_v15ad_add_chord_boundary_shell_lab.py`
- `relational_universe_v15af_add_chord_shell_fragment_event_lab.py`
- `relational_universe_v15ag_shell_exception_explainer.py`
- `relational_universe_v15ah_shell_exception_holdout.py`
- `relational_universe_v15ai_early_lock_band_lab.py`
- `relational_universe_v15aj_early_lock_band_onset_lab.py`
- `relational_universe_v15ak_band_entry_trigger_lab.py`
- `relational_universe_v15al_boundary_zone_split_lab.py`
- `relational_universe_v15am_boundary_overlap_explainer.py`
- `relational_universe_v15an_boundary_high_hold_lab.py`
- `relational_universe_v15ao_terminal_probe_boundary_lab.py`
- `relational_universe_v15ap_pre_high_launch_lab.py`
- `relational_universe_v15aq_high_launch_impulse_lab.py`
- `relational_universe_v15ar_high_retention_horizon_lab.py`
- `relational_universe_v15as_horizon_map_holdout.py`
- `relational_universe_v15at_high_burst_window_lab.py`
- `relational_universe_v15au_post_peak_fade_explainer.py`
- `relational_universe_v15av_post_peak_fade_holdout.py`
- `relational_universe_v15aw_local_swap_core_shell_lab.py`
- `relational_universe_v15ax_local_swap_size_split_explainer.py`
- `relational_universe_v15ay_local_swap_96_pocket_explainer.py`
- `relational_universe_v15az_local_swap_p3_seed_flip_explainer.py`
- `relational_universe_v15ba_local_swap_compressed_shell_explainer.py`
- `relational_universe_v15bb_local_swap_growth202_mode_map.py`
- `relational_universe_v15bc_local_swap_p3_vs_p1_p2_contrast.py`
- `relational_universe_v15bd_local_swap_trigger_axis_lab.py`
- `relational_universe_v15be_local_swap_trigger_axis_component_lab.py`
- `relational_universe_v15bf_local_swap_gap_asymmetry_explainer.py`
- `relational_universe_v15bg_local_swap_shell_drag_decomposition.py`
- `relational_universe_v15bh_local_swap_rare_load_trigger_lab.py`
- `relational_universe_v15bi_local_swap_load_stabilizer_flip.py`
- `relational_universe_v15bj_local_swap_stabilizer_component_lab.py`
- `relational_universe_v15bk_local_swap_load_stabilizer_mode_map.py`
- `relational_universe_v15bl_conditional_quasi_invariant_lab.py`
- `relational_universe_v15bm_carrier_first_spectral_holdout.py`
- `relational_universe_v15bn_add_chord_scale_jump_family_map.py`
- `relational_universe_v15bo_add_chord_scale_jump_holdout.py`
- `relational_universe_v15bp_add_chord_scale_break_explainer.py`
- `relational_universe_v15bq_add_chord_alt_coarse_geometry_lab.py`
- `relational_universe_v15br_local_swap_mode_spectral_holdout.py`
- `relational_universe_v15bs_add_chord_vs_local_swap_p3_carrier_compare.py`
- `relational_universe_v15bt_same_locus_carrier_timing_lab.py`
- `relational_universe_v15bu_same_locus_carrier_occupancy_spectrum_lab.py`
- `relational_universe_v15bv_family_structure_symmetry_lab.py`
- `relational_universe_v15bw_family_structure_holdout.py`
- `relational_universe_v15bx_scale_jump_family_probe.py`
- `relational_universe_v15by_target192_plateau_holdout.py`
- `relational_universe_v15bz_target384_family_probe.py`
- `relational_universe_v15c_collision_type_lab.py`
- `relational_universe_v15cb_target384_candidate_holdout.py`
- `relational_universe_v15cd_target768_family_probe.py`
- `relational_universe_v15ce_target768_plateau_holdout.py`
- `relational_universe_v15cf_target768_support_locus_mechanism_lab.py`
- `relational_universe_v15cp_target1024_scaled_budget_p2_horizon.py`
- `relational_universe_v15cq_intermediate_scale_p2_horizon.py`
- `relational_universe_v15cs_add_chord_p0_scale_response_holdout.py`
- `relational_universe_v15cu_add_chord_placement_response_map.py`
- `relational_universe_v15d_collision_window_lab.py`
- `relational_universe_v15db_routing_phase_observable_synthesis.py`
- `relational_universe_v15dc_pre_horizon_routing_precursor_lab.py`
- `relational_universe_v15de_pre_entry_feature_synthesis.py`
- `relational_universe_v15df_pre_entry_support_topology_synthesis.py`
- `relational_universe_v15dg_boundary_mass_holdout.py`
- `relational_universe_v15dm_frozen_return_probability_holdout.py`
- `relational_universe_v15dp_active_set_type_guard_holdout.py`
- `relational_universe_v15dr_active_set_taxonomy_mapper_holdout.py`
- `relational_universe_v15ds_active_set_landscape_atlas.py`
- `relational_universe_v15dt_ood_first_stratified_selector_synthesis.py`
- `relational_universe_v15e_pair_family_refinement.py`
- `relational_universe_v15f_pair23_budget_extension.py`
- `relational_universe_v15h_representative_collision_traces.py`
- `relational_universe_v15k_mechanism_holdout_validation.py`
- `relational_universe_v15m_single_defect_survival_lab.py`
- `relational_universe_v15n_token_shift_fragility_lab.py`
- `relational_universe_v15o_token_shift_fragility_replication.py`
- `relational_universe_v15p_token_shift_profile_refinement.py`
- `relational_universe_v15r_add_chord_long_horizon_recurrence.py`
- `relational_universe_v15s_add_chord_cycle_family_map.py`
- `relational_universe_v15t_add_chord_cycle_center_holdout.py`
- `relational_universe_v15u_add_chord_p1_microcenter.py`
- `relational_universe_v15v_add_chord_triplet_mechanism_lab.py`
- `relational_universe_v15w_add_chord_p0_p1_support_contrast.py`
- `relational_universe_v15x_add_chord_p0_p1_first_tail_segment.py`
- `relational_universe_v15y_p0_p1_case_duel_lab.py`
- `relational_universe_v15z_case_trigger_explainer.py`

## Reproducibility and source hashes

- Python: `3.13.5`
- NetworkX: `3.4.2`
- Raw rows: `1582`
- `relational_universe_local_max_coupling_lab.py` SHA-256: `695ed59ca168336334d5745076ee8924596447ee6db237963468abde526f0e1c`
- `relational_universe_v15bs_add_chord_vs_local_swap_p3_carrier_compare.py` SHA-256: `4e243f05c947005ec59fd6f42285d3c16f9698c89713a7a14d46fff1ee20d767`
- `relational_universe_v15bt_same_locus_carrier_timing_lab.py` SHA-256: `43f070b3c05c03b18f27f6b5f9bf836e3e780d3095d03cc99525684e900ae971`
- `relational_universe_v15bu_same_locus_carrier_occupancy_spectrum_lab.py` SHA-256: `b5513233b143701c704058bdc90fdbb453d84bf263d05eda9658e43f17fdb5c8`
- `relational_universe_v15bv_family_structure_symmetry_lab.py` SHA-256: `6d6b8fcda1b377e90a6b01011533618315edb94250e61c68baf967fb83e85df1`
- `relational_universe_v15bw_family_structure_holdout.py` SHA-256: `f765daf2ee203a4be656b3f8bfcf286a9ccd0da268582b6c6b3151b4ccdf52ab`
- `relational_universe_v15bx_scale_jump_family_probe.py` SHA-256: `55ebf123b71e6f6b76bf68f16adef6f7d5c61bbe8c6dc2317fd1de39fce6d154`
- `relational_universe_v15by_target192_plateau_holdout.py` SHA-256: `e0aa700522f443d7af4800229632cc028a82f6721700e37822df41782cdde83b`
- `relational_universe_v15bz_target384_family_probe.py` SHA-256: `546b789916abe0edc528504ee4c1b6804d6888260a4f4a0d5a7e50e060a4532a`
- `relational_universe_v15ca_target192_radial_occupancy_mechanism_lab.py` SHA-256: `563dbb95f6b9cf8b01a8cf33aa21be60c3f48513625bd04b81ab671c14990331`
- `relational_universe_v15cb_target384_candidate_holdout.py` SHA-256: `1eb871f0cad195f053f358ab04ac2bea6188a9970fd1d66c4b2c471b4747ed5a`
- `relational_universe_v15cc_target384_shell_turnover_observable.py` SHA-256: `28d0e2390d608e576dec8ba767430b5ca79a9f22471e1f560e735fb9f1f3bcff`
- `relational_universe_v15cd_target768_family_probe.py` SHA-256: `9497c1777209e9aa987224d342a84658296cfbb56fa566fe181b223a633c74be`
- `relational_universe_v15ce_target768_plateau_holdout.py` SHA-256: `ce5d1b8303ea364809e02ec02d0686dfe1bda8824367c898959ccce7b2b66081`
- `relational_universe_v15cf_target768_support_locus_mechanism_lab.py` SHA-256: `f33e2be215b67625e86a47664f1161ae05be8b7e262f4edc7682c7f8cfc7fe0d`
- `relational_universe_v15cg_target768_far_shell_horizon_lab.py` SHA-256: `044ccbe13b4868f37191172ca1068b6e557883b9d27f397611745f1cdd522b89`
- `relational_universe_v15ci_target768_p2_horizon_genealogy_mechanism_lab.py` SHA-256: `4f105d49344c7f66cec61d37232952c56655d17e55a590ff48c1678233f7aa54`
- `relational_universe_v15cj_target768_outer_occupancy_concentration_lab.py` SHA-256: `0deb4f3aa257e71b1b222bb3034088658a20268706babfd05d34bf8437e7f850`
- `relational_universe_v15ck_target768_outer_feeder_flux_lab.py` SHA-256: `c0349b59faf18fa62d4588b2058e6402216f9e9aa2cd42a0dc8d44bf7a1a2e42`
- `relational_universe_v15cl_target768_inner_gate_global_budget_lab.py` SHA-256: `94317507dcc6c33a897657dbc2af1e8de653dfd53a091324095b58358bdf2fc1`
- `relational_universe_v15cm_target768_local_trigger_lab.py` SHA-256: `2c444a381e4a321089731f00e212ad2c84ca338a1908ca2bef6fc3a31ee777a6`
- `relational_universe_v15cn_p2_horizon_scale_holdout.py` SHA-256: `eb8a00b1fea8ae65827d3afc1acec17e59bc4c5a65c686c7ac57944e3ff3165a`
- `relational_universe_v15cp_target1024_scaled_budget_p2_horizon.py` SHA-256: `14927e276311e10c7ca9ba2f6281d3e28c2a2a73e60bf24d9498227eb306e903`
- `relational_universe_v15cq_intermediate_scale_p2_horizon.py` SHA-256: `76a213e1ac4f997aa3b7f8a840ab2d46a70a4ef34557bbfb5511f68f7a6c6c53`
- `relational_universe_v15cu_add_chord_placement_response_map.py` SHA-256: `d0c5d91b6ca66256920676cba5bd6073715285bb54dd7d1185a4fff3f608a7db`
- `relational_universe_v15cv_add_chord_winning_placement_mechanism_probe.py` SHA-256: `1fdb2ad55f7e73224e35313a05390ea539f63bdbbfb017c765f6dcfd458a6852`
- `relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split.py` SHA-256: `2affa3c0d69c841707fb501489bba3f60a93525ace2c95e0b354564aa8d069f6`
- `relational_universe_v15cx_p1_1024_genealogy_holdout.py` SHA-256: `32ac20e974d530a8e7d6b09b69298f8633aa23db131f408513eec8a1468dae01`
- `relational_universe_v15cz_pre_registered_continuous_intensity_holdout.py` SHA-256: `87bfb64eae8c4688451e7f119b2e3f8ba25a7b2b92498895f84eb09118938be7`
- `relational_universe_v15da_frozen_intensity_placement_contrast.py` SHA-256: `98b452a9420d2f3b8dce4dfb44cc415ff3d8ce9909e7c561168f411a81926c42`
- `relational_universe_v15dd_direct_route_entry_retention_lab.py` SHA-256: `28055c7a5391895f2371c9476e19fc96ed96ae6c09def773184449cbb68aa3e1`
- `relational_universe_v15dg_boundary_mass_holdout.py` SHA-256: `c79d7d90b5f975b12b57d1ec5ca68b82ecb7fb1a3449d24ba04df148d2211f1f`
- `relational_universe_v15dh_boundary_mass_growth_seed_holdout.py` SHA-256: `2b0d121cddce94d2c4415a1ee99ab3b8e152fc69d2a56fb0e27d31b5036e7010`
- `relational_universe_v15dk_pre_registered_support_rank_holdout.py` SHA-256: `2bea01148d1dd783a734ac7e6591e1916095406321149569837cdd7c62f74f6c`
- `relational_universe_v15dl_base_landscape_morphology_synthesis.py` SHA-256: `72c64532d7d93b611909709af92a12cf7e3ef8b79a82314d117dd9348d888387`
- `relational_universe_v15dm_frozen_return_probability_holdout.py` SHA-256: `898b58823cf840b9a1bf25b2b0da2e8826391f98e7a6888b3f020b4aa090bad8`
- `relational_universe_v15dp_active_set_type_guard_holdout.py` SHA-256: `f251836c9ace1ba926ca71959422bc5d0fc81b6bcbee4d3412c81e8689e54caf`
- `relational_universe_v15dr_active_set_taxonomy_mapper_holdout.py` SHA-256: `368a5aaed596668981d833d74664525c19dcf25a2b2f6e42d276740950009aad`
- `relational_universe_v15ds_active_set_landscape_atlas.py` SHA-256: `a8f67cdead3fa03c500def4789fe13235f02cf540966f5946b865593b62b881a`
- `relational_universe_v15du_relabel_symmetry_gate.py` SHA-256: `da6a985e900a4ba587976663e127486da68f99a3b06726c6a133fbdd1936721f`
- `relational_universe_v15dv_relabel_invariant_chord_constructor.py` SHA-256: `1727be8047b4254b0c85f8c729128fe21a6908dfed612d57f9f9598ebc17d0bb`
- `relational_universe_v15m_single_defect_survival_lab.py` SHA-256: `f69cc31ad14318287ff0cb0411aa9316cd4102ee3a9de5795f463aa2943d1eff`
- `relational_universe_v15n_token_shift_fragility_lab.py` SHA-256: `e17fc3be4ca42bc8cf98e41218552cbce1c779e2296949c31617210cb0c76c71`
- `relational_universe_v15q_single_defect_recurrence_lab.py` SHA-256: `8780df2405f26c9511d8e4cd55a45366769ed456cd0e2469ed7d50a8d83826d5`

Run from repository root:

```sh
PYTHONPATH=.codex_pydeps python3 Tools/beta1_bookkeeping_audit.py
```

## Claim limits

- Results cover v15 modules with a complete source-declared target/growth-seed/placement
  configuration and at least one of the two audited perturbation families.
- Declared seed-deltas can map to the same deterministic base-state constructor call;
  frequencies are source-schedule-weighted, not a count of unique graph/locus pairs.
- The audit measures initial perturbation bookkeeping, not later coupled dynamics.
- Import reachability is a conservative dependency inventory, not runtime coverage.
- No physics inference follows from this finite software audit.
