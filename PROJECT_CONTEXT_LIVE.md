# PROJECT_CONTEXT_LIVE

Dette dokumentet er den korteste operative inngangen til dagens repo-state i `UniverseSimulation`.

## Arbeidsregler

- Filer pa disk er ground truth.
- Nyere lokale `.py`, `.md` og `.csv`-filer overstyrer eldre promptoppsummeringer hvis de sier noe annet.
- `focused_score` alene avgjor ikke frontier-vinnere.
- `uavklart` er en legitim konklusjon hvis raw score, CI-low og pairwise peker ulikt.
- Skill alltid mellom:
  - algebraiske identiteter,
  - generator-/ensembleartefakter,
  - scoringartefakter,
  - dynamiske simulasjonsresultater.

## Siste sikre live status

Per dagens lokale state er `v11e` den siste frontier-avklaringen. `v12`, `v12b`, `v12c`, `v12d`, `v12e`, `v12f`, `v12g`, `v12h`, `v12i`, `v12j`, `v12k`, `v12l`, `v12m`, `v12n`, `v13`, `v13b`, `v13c`, `v13d`, `v13e`, `v13f`, `v13g`, `v13h`, `v13i`, `v13j`, `v13k`, `v13l`, `v13m`, `v13n`, `v14`, `v14b`, `v14c`, `v15`, `v15b`, `v15c`, `v15d`, `v15e`, `v15f`, `v15g`, `v15h`, `v15i`, `v15j`, `v15k`, `v15l`, `v15m`, `v15n`, `v15o`, `v15p`, `v15q`, `v15r`, `v15s`, `v15t`, `v15u`, `v15v`, `v15w`, `v15x`, `v15y`, `v15z`, `v15aa`, `v15ab`, `v15ac`, `v15ad`, `v15ae`, `v15af`, `v15ag`, `v15ah`, `v15ai`, `v15aj`, `v15ak`, `v15al`, `v15am`, `v15an`, `v15ao`, `v15ap`, `v15aq`, `v15ar`, `v15as`, `v15at`, `v15au`, `v15av`, `v15aw`, `v15ax`, `v15ay`, `v15az`, `v15ba`, `v15bb`, `v15bc`, `v15bd`, `v15be`, `v15bf`, `v15bg`, `v15bh`, `v15bi`, `v15bj`, `v15bk` og `v15bl` er de aktive struktur-/transfer-/Lorentz-/defect-rundene bygget pa den.

- Frontier-script: `relational_universe_v11e_band_vs_bridge0075.py`
- Frontier-rapport: `Documentation/v11e_band_vs_bridge0075.md`
- Frontier-kandidatsammendrag: `Documentation/v11e_band_vs_bridge0075_candidate_summary.csv`
- Frontier-pairwise: `Documentation/v11e_band_vs_bridge0075_pairwise.csv`
- Frontier-startstorrelser: `Documentation/v11e_band_vs_bridge0075_target_summary.csv`
- Frontier-anbefaling: `Documentation/v0_11e_operativ_anbefaling.md`
- Geometri-/invariant-script: `relational_universe_v12_geometry_invariant_lab.py`
- Geometri-/invariantrapport: `Documentation/v12_geometry_invariant_lab.md`
- Geometri-stabilitet: `Documentation/v12_geometry_feature_stability.csv`
- Quasi-invariant-rangering: `Documentation/v12_geometry_relative_drift_ranking.csv`
- Redusert basis: `Documentation/v12_geometry_reduced_basis_summary.csv`
- Geometri-anbefaling: `Documentation/v0_12_operativ_anbefaling.md`
- Transfer-/surrogate-script: `relational_universe_v12b_transfer_surrogate_lab.py`
- Transfer-rapport: `Documentation/v12b_transfer_surrogate_lab.md`
- Transfer-basis: `Documentation/v12b_transfer_basis_summary.csv`
- Transfer-startstorrelser: `Documentation/v12b_transfer_target_summary.csv`
- Transfer-anbefaling: `Documentation/v0_12b_operativ_anbefaling.md`
- Radius-transfer-raffinement-script: `relational_universe_v12c_radius_transfer_refinement.py`
- Radius-transfer-raffinement-rapport: `Documentation/v12c_radius_transfer_refinement.md`
- Radius-transfer-basis: `Documentation/v12c_radius_basis_summary.csv`
- Radius-transfer-ranking: `Documentation/v12c_radius_basis_ranking.csv`
- Radius-transfer-anbefaling: `Documentation/v0_12c_operativ_anbefaling.md`
- Kryssakse-transfer-script: `relational_universe_v12d_cross_axis_radius_transfer.py`
- Kryssakse-transfer-rapport: `Documentation/v12d_cross_axis_radius_transfer.md`
- Kryssakse-basis: `Documentation/v12d_cross_axis_basis_summary.csv`
- Kryssakse-ranking: `Documentation/v12d_cross_axis_basis_ranking.csv`
- Kryssakse-anbefaling: `Documentation/v0_12d_operativ_anbefaling.md`
- Screening-/sorteringsscript: `relational_universe_v12e_start_state_screening.py`
- Screening-rapport: `Documentation/v12e_start_state_screening.md`
- Screening-sammendrag: `Documentation/v12e_screening_summary.csv`
- Screening-anbefaling: `Documentation/v0_12e_operativ_anbefaling.md`
- Budsjettscreening-script: `relational_universe_v12f_budget_screening.py`
- Budsjettscreening-rapport: `Documentation/v12f_budget_screening.md`
- Budsjettscreening-sammendrag: `Documentation/v12f_budget_summary.csv`
- Budsjettscreening-anbefaling: `Documentation/v0_12f_operativ_anbefaling.md`
- Oppfolgingspipeline-script: `relational_universe_v12g_followup_budget_pipeline.py`
- Oppfolgingspipeline-rapport: `Documentation/v12g_followup_budget_pipeline.md`
- Oppfolgingspipeline-sammendrag: `Documentation/v12g_followup_pipeline_summary.csv`
- Oppfolgingspipeline-anbefaling: `Documentation/v0_12g_operativ_anbefaling.md`
- Kostnadsbevisst pipeline-script: `relational_universe_v12h_cost_aware_pipeline.py`
- Kostnadsbevisst pipeline-rapport: `Documentation/v12h_cost_aware_pipeline.md`
- Kostnadsbevisst pipeline-sammendrag: `Documentation/v12h_cost_aware_pipeline_summary.csv`
- Kostnadsbevisst pipeline-anbefaling: `Documentation/v0_12h_operativ_anbefaling.md`
- Malt runtime-pipeline-script: `relational_universe_v12i_measured_runtime_pipeline.py`
- Malt runtime-pipeline-rapport: `Documentation/v12i_measured_runtime_pipeline.md`
- Malt runtime-oppfolgingstid: `Documentation/v12i_measured_runtime_pipeline_followup_timing_summary.csv`
- Malt runtime-sammendrag: `Documentation/v12i_measured_runtime_pipeline_summary.csv`
- Malt runtime-anbefaling: `Documentation/v0_12i_operativ_anbefaling.md`
- Storrelses-stresset runtime-pipeline-script: `relational_universe_v12j_size_stress_runtime_pipeline.py`
- Storrelses-stresset runtime-pipeline-rapport: `Documentation/v12j_size_stress_runtime_pipeline.md`
- Storrelses-stresset target-sammendrag: `Documentation/v12j_size_stress_runtime_pipeline_target_summary.csv`
- Storrelses-stresset runtime-sammendrag: `Documentation/v12j_size_stress_runtime_pipeline_summary.csv`
- Storrelses-stresset runtime-anbefaling: `Documentation/v0_12j_operativ_anbefaling.md`
- Adaptiv oppfolgingsscript: `relational_universe_v12k_adaptive_followup_budget.py`
- Adaptiv oppfolgingsrapport: `Documentation/v12k_adaptive_followup_budget.md`
- Adaptiv oppfolgings-target-sammendrag: `Documentation/v12k_adaptive_followup_budget_target_summary.csv`
- Adaptiv oppfolgings-sammendrag: `Documentation/v12k_adaptive_followup_budget_summary.csv`
- Adaptiv oppfolgings-anbefaling: `Documentation/v0_12k_operativ_anbefaling.md`
- Hybrid screening+oppfolgingsscript: `relational_universe_v12l_hybrid_screening_followup.py`
- Hybrid screening+oppfolgingsrapport: `Documentation/v12l_hybrid_screening_followup.md`
- Hybrid screening+oppfolgings-target-sammendrag: `Documentation/v12l_hybrid_screening_followup_target_summary.csv`
- Hybrid screening+oppfolgings-sammendrag: `Documentation/v12l_hybrid_screening_followup_summary.csv`
- Hybrid screening+oppfolgings-anbefaling: `Documentation/v0_12l_operativ_anbefaling.md`
- Dypere adaptiv oppfolgingsscript: `relational_universe_v12m_deeper_adaptive_followup.py`
- Dypere adaptiv oppfolgingsrapport: `Documentation/v12m_deeper_adaptive_followup.md`
- Dypere adaptiv oppfolgings-target-sammendrag: `Documentation/v12m_deeper_adaptive_followup_target_summary.csv`
- Dypere adaptiv oppfolgings-sammendrag: `Documentation/v12m_deeper_adaptive_followup_summary.csv`
- Dypere adaptiv oppfolgings-anbefaling: `Documentation/v0_12m_operativ_anbefaling.md`
- Binaer adaptiv valideringsscript: `relational_universe_v12n_binary_adaptive_validation.py`
- Binaer adaptiv valideringsrapport: `Documentation/v12n_binary_adaptive_validation.md`
- Binaer adaptiv validerings-target-sammendrag: `Documentation/v12n_binary_adaptive_validation_target_summary.csv`
- Binaer adaptiv validerings-sammendrag: `Documentation/v12n_binary_adaptive_validation_summary.csv`
- Binaer adaptiv validerings-anbefaling: `Documentation/v0_12n_operativ_anbefaling.md`
- Geometri-/signalvalideringsscript: `relational_universe_v13_geometry_signal_validation.py`
- Geometri-/signalvalideringsrapport: `Documentation/v13_geometry_signal_validation.md`
- Geometri-/signalvaliderings-stabilitet: `Documentation/v13_geometry_signal_stability_summary.csv`
- Geometri-/signalvaliderings-drift: `Documentation/v13_quasi_invariant_bootstrap_summary.csv`
- Geometri-/signalvaliderings-basis: `Documentation/v13_geometry_signal_validation_summary.csv`
- Geometri-/signalvaliderings-anbefaling: `Documentation/v0_13_operativ_anbefaling.md`
- Kryssregime quasi-invariant-script: `relational_universe_v13b_cross_regime_quasiinvariant_test.py`
- Kryssregime quasi-invariant-rapport: `Documentation/v13b_cross_regime_quasiinvariant_test.md`
- Kryssregime quasi-invariant-drift: `Documentation/v13b_cross_regime_drift_summary.csv`
- Kryssregime quasi-invariant-anchor-delta: `Documentation/v13b_cross_regime_anchor_delta_summary.csv`
- Kryssregime quasi-invariant-anbefaling: `Documentation/v0_13b_operativ_anbefaling.md`
- Spektral quasi-invariant-valideringsscript: `relational_universe_v13c_spectral_quasiinvariant_validation.py`
- Spektral quasi-invariant-valideringsrapport: `Documentation/v13c_spectral_quasiinvariant_validation.md`
- Spektral quasi-invariant-fokus: `Documentation/v13c_spectral_validation_focus_summary.csv`
- Spektral quasi-invariant-anchor-delta: `Documentation/v13c_spectral_validation_anchor_delta_summary.csv`
- Spektral quasi-invariant-anbefaling: `Documentation/v0_13c_operativ_anbefaling.md`
- Lokal spektral-skarpingsscript: `relational_universe_v13d_local_spectral_sharpening.py`
- Lokal spektral-skarpingsrapport: `Documentation/v13d_local_spectral_sharpening.md`
- Lokal spektral-skarpingslokal-summary: `Documentation/v13d_spectral_validation_local_summary.csv`
- Lokal spektral-skarpingsanbefaling: `Documentation/v0_13d_operativ_anbefaling.md`
- Triad-korridor-skarpingsscript: `relational_universe_v13e_triad_corridor_sharpening.py`
- Triad-korridor-skarpingsrapport: `Documentation/v13e_triad_corridor_sharpening.md`
- Triad-korridor-skarpingscorridor-summary: `Documentation/v13e_spectral_validation_corridor_summary.csv`
- Triad-korridor-skarpingsanbefaling: `Documentation/v0_13e_operativ_anbefaling.md`
- Triad-notch-testscript: `relational_universe_v13f_triad_notch_test.py`
- Triad-notch-testrapport: `Documentation/v13f_triad_notch_test.md`
- Triad-notch-local-summary: `Documentation/v13f_spectral_validation_local_summary.csv`
- Triad-notch-summary: `Documentation/v13f_spectral_validation_notch_summary.csv`
- Triad-notch-anbefaling: `Documentation/v0_13f_operativ_anbefaling.md`
- Målrettet triad-valideringsscript: `relational_universe_v13g_targeted_triad_validation.py`
- Målrettet triad-valideringsrapport: `Documentation/v13g_targeted_triad_validation.md`
- Målrettet triad-valideringscorridor-summary: `Documentation/v13g_spectral_validation_corridor_summary.csv`
- Målrettet triad-valideringsanbefaling: `Documentation/v0_13g_operativ_anbefaling.md`
- Upper-triad-overgangsscript: `relational_universe_v13h_upper_triad_transition.py`
- Upper-triad-overgangsrapport: `Documentation/v13h_upper_triad_transition.md`
- Upper-triad-overgangssummary: `Documentation/v13h_spectral_validation_transition_summary.csv`
- Upper-triad-overgangsdiagnose: `Documentation/v13h_spectral_validation_upper_diagnosis.csv`
- Upper-triad-overgangsanbefaling: `Documentation/v0_13h_operativ_anbefaling.md`
- Upper-recovery-raffineringsscript: `relational_universe_v13i_upper_recovery_refinement.py`
- Upper-recovery-raffineringsrapport: `Documentation/v13i_upper_recovery_refinement.md`
- Upper-recovery-raffineringssummary: `Documentation/v13i_spectral_validation_refinement_summary.csv`
- Upper-recovery-diagnose: `Documentation/v13i_spectral_validation_recovery_diagnosis.csv`
- Upper-recovery-anbefaling: `Documentation/v0_13i_operativ_anbefaling.md`
- Upper-clean-band-script: `relational_universe_v13j_upper_clean_band_refinement.py`
- Upper-clean-band-rapport: `Documentation/v13j_upper_clean_band_refinement.md`
- Upper-clean-band-summary: `Documentation/v13j_spectral_validation_refinement_summary.csv`
- Upper-clean-band-diagnose: `Documentation/v13j_spectral_validation_band_diagnosis.csv`
- Upper-clean-band-anbefaling: `Documentation/v0_13j_operativ_anbefaling.md`
- Målrettet upper-band-valideringsscript: `relational_universe_v13k_targeted_upper_band_validation.py`
- Målrettet upper-band-valideringsrapport: `Documentation/v13k_targeted_upper_band_validation.md`
- Målrettet upper-band-valideringssummary: `Documentation/v13k_spectral_validation_refinement_summary.csv`
- Målrettet upper-band-valideringsdiagnose: `Documentation/v13k_spectral_validation_band_diagnosis.csv`
- Målrettet upper-band-valideringsanbefaling: `Documentation/v0_13k_operativ_anbefaling.md`
- Lokal upper-pivot-raffineringsscript: `relational_universe_v13l_local_upper_pivot_refinement.py`
- Lokal upper-pivot-raffineringsrapport: `Documentation/v13l_local_upper_pivot_refinement.md`
- Lokal upper-pivot-raffineringssummary: `Documentation/v13l_spectral_validation_refinement_summary.csv`
- Lokal upper-pivot-diagnose: `Documentation/v13l_spectral_validation_pivot_diagnosis.csv`
- Lokal upper-pivot-anbefaling: `Documentation/v0_13l_operativ_anbefaling.md`
- Upper-break-edge-script: `relational_universe_v13m_upper_break_edge_test.py`
- Upper-break-edge-rapport: `Documentation/v13m_upper_break_edge_test.md`
- Upper-break-edge-summary: `Documentation/v13m_spectral_validation_refinement_summary.csv`
- Upper-break-edge-diagnose: `Documentation/v13m_spectral_validation_break_diagnosis.csv`
- Upper-break-edge-anbefaling: `Documentation/v0_13m_operativ_anbefaling.md`
- Lower-drop-edge-script: `relational_universe_v13n_lower_drop_edge_test.py`
- Lower-drop-edge-rapport: `Documentation/v13n_lower_drop_edge_test.md`
- Lower-drop-edge-summary: `Documentation/v13n_spectral_validation_refinement_summary.csv`
- Lower-drop-edge-diagnose: `Documentation/v13n_spectral_validation_break_diagnosis.csv`
- Lower-drop-edge-anbefaling: `Documentation/v0_13n_operativ_anbefaling.md`
- Lorentz-diagnostikkscript: `relational_universe_v14_lorentz_diagnostics.py`
- Lorentz-diagnostikkrapport: `Documentation/v14_lorentz_diagnostics.md`
- Lorentz-target-sammendrag: `Documentation/v14_lorentz_target_summary.csv`
- Lorentz-aggregate-sammendrag: `Documentation/v14_lorentz_aggregate_summary.csv`
- Lorentz-pairwise-perturbasjonssammendrag: `Documentation/v14_lorentz_pairwise_perturbation_summary.csv`
- Lorentz-artefaktkontroll: `Documentation/v14_lorentz_artifact_checks.csv`
- Lorentz-regime-gap-sammendrag: `Documentation/v14_lorentz_regime_gap_summary.csv`
- Lorentz-anbefaling: `Documentation/v0_14_operativ_anbefaling.md`
- Placement-aware Lorentz-script: `relational_universe_v14b_lorentz_placement_diagnostics.py`
- Placement-aware Lorentz-rapport: `Documentation/v14b_lorentz_placement_diagnostics.md`
- Placement-aware Lorentz-placement-summary: `Documentation/v14b_lorentz_placement_summary.csv`
- Placement-aware Lorentz-within-mode-summary: `Documentation/v14b_lorentz_within_mode_summary.csv`
- Placement-aware Lorentz-between-mode-summary: `Documentation/v14b_lorentz_between_mode_summary.csv`
- Placement-aware Lorentz-diagnose: `Documentation/v14b_lorentz_mode_vs_placement_diagnosis.csv`
- Placement-aware Lorentz-anbefaling: `Documentation/v0_14b_operativ_anbefaling.md`
- Lokal isotropi-diagnostikkscript: `relational_universe_v14c_local_isotropy_diagnostics.py`
- Lokal isotropi-diagnostikkrapport: `Documentation/v14c_local_isotropy_diagnostics.md`
- Lokal isotropi-placement-summary: `Documentation/v14c_local_isotropy_placement_summary.csv`
- Lokal isotropi-feature-summary: `Documentation/v14c_local_isotropy_feature_signal_summary.csv`
- Lokal isotropi-alignment-summary: `Documentation/v14c_local_isotropy_alignment_summary.csv`
- Lokal isotropi-anbefaling: `Documentation/v0_14c_operativ_anbefaling.md`
- Defect lifetime-script: `relational_universe_v15_defect_lifetime_lab.py`
- Defect lifetime-rapport: `Documentation/v15_defect_lifetime_lab.md`
- Defect lifetime-aggregate: `Documentation/v15_defect_lifetime_aggregate.csv`
- Defect lifetime-by-target: `Documentation/v15_defect_lifetime_by_target.csv`
- Defect lifetime-anbefaling: `Documentation/v0_15_operativ_anbefaling.md`
- Add_chord-collision-script: `relational_universe_v15b_add_chord_collision_lab.py`
- Add_chord-collision-rapport: `Documentation/v15b_add_chord_collision_lab.md`
- Add_chord-collision-interactions: `Documentation/v15b_add_chord_collision_interactions.csv`
- Add_chord-collision-aggregate: `Documentation/v15b_add_chord_collision_aggregate.csv`
- Add_chord-collision-anbefaling: `Documentation/v0_15b_operativ_anbefaling.md`
- Add_chord collision-type-script: `relational_universe_v15c_collision_type_lab.py`
- Add_chord collision-type-rapport: `Documentation/v15c_collision_type_lab.md`
- Add_chord collision-type-rows: `Documentation/v15c_collision_type_rows.csv`
- Add_chord collision-type-aggregate: `Documentation/v15c_collision_type_aggregate.csv`
- Add_chord collision-type-anbefaling: `Documentation/v0_15c_operativ_anbefaling.md`
- Add_chord collision-window-script: `relational_universe_v15d_collision_window_lab.py`
- Add_chord collision-window-rapport: `Documentation/v15d_collision_window_lab.md`
- Add_chord collision-window-rows: `Documentation/v15d_collision_window_rows.csv`
- Add_chord collision-window-aggregate: `Documentation/v15d_collision_window_aggregate.csv`
- Add_chord collision-window-anbefaling: `Documentation/v0_15d_operativ_anbefaling.md`
- Pair-family refinement-script: `relational_universe_v15e_pair_family_refinement.py`
- Pair-family refinement-rapport: `Documentation/v15e_pair_family_refinement.md`
- Pair-family refinement-rows: `Documentation/v15e_pair_family_rows.csv`
- Pair-family refinement-aggregate: `Documentation/v15e_pair_family_aggregate.csv`
- Pair-family refinement-anbefaling: `Documentation/v0_15e_operativ_anbefaling.md`
- Pair 2-3 budget-extension-script: `relational_universe_v15f_pair23_budget_extension.py`
- Pair 2-3 budget-extension-rapport: `Documentation/v15f_pair23_budget_extension.md`
- Pair 2-3 budget-extension-rows: `Documentation/v15f_pair23_rows.csv`
- Pair 2-3 budget-extension-aggregate: `Documentation/v15f_pair23_aggregate.csv`
- Pair 2-3 budget-extension-anbefaling: `Documentation/v0_15f_operativ_anbefaling.md`
- Collision genealogy-script: `relational_universe_v15g_collision_genealogy_lab.py`
- Collision genealogy-rapport: `Documentation/v15g_collision_genealogy_lab.md`
- Collision genealogy-component-trajectories: `Documentation/v15g_collision_genealogy_component_trajectories.csv`
- Collision genealogy-event-log: `Documentation/v15g_collision_genealogy_event_log.csv`
- Collision genealogy-event-aggregate: `Documentation/v15g_collision_genealogy_event_aggregate.csv`
- Collision genealogy-event-chains: `Documentation/v15g_collision_genealogy_event_chains.csv`
- Collision genealogy-anbefaling: `Documentation/v0_15g_operativ_anbefaling.md`
- Representative trace-script: `relational_universe_v15h_representative_collision_traces.py`
- Representative trace-rapport: `Documentation/v15h_representative_collision_traces.md`
- Representative trace-component-trajectories: `Documentation/v15h_representative_trace_component_trajectories.csv`
- Representative trace-event-log: `Documentation/v15h_representative_trace_event_log.csv`
- Representative trace-summary: `Documentation/v15h_representative_trace_summary.csv`
- Representative trace-anbefaling: `Documentation/v0_15h_operativ_anbefaling.md`
- Tail-transition-script: `relational_universe_v15i_tail_transition_lab.py`
- Tail-transition-rapport: `Documentation/v15i_tail_transition_lab.md`
- Tail-transition-order-rows: `Documentation/v15i_tail_transition_order_rows.csv`
- Tail-transition-segments: `Documentation/v15i_tail_transition_segments.csv`
- Tail-transition-summary: `Documentation/v15i_tail_transition_summary.csv`
- Tail-transition-aggregate: `Documentation/v15i_tail_transition_aggregate.csv`
- Tail-transition-anbefaling: `Documentation/v0_15i_operativ_anbefaling.md`
- Tail-mechanism-script: `relational_universe_v15j_tail_mechanism_lab.py`
- Tail-mechanism-rapport: `Documentation/v15j_tail_mechanism_lab.md`
- Tail-mechanism-order-rows: `Documentation/v15j_tail_mechanism_order_rows.csv`
- Tail-mechanism-summary: `Documentation/v15j_tail_mechanism_summary.csv`
- Tail-mechanism-aggregate: `Documentation/v15j_tail_mechanism_aggregate.csv`
- Tail-mechanism-anbefaling: `Documentation/v0_15j_operativ_anbefaling.md`
- Mechanism-holdout-script: `relational_universe_v15k_mechanism_holdout_validation.py`
- Mechanism-holdout-rapport: `Documentation/v15k_mechanism_holdout_validation.md`
- Mechanism-holdout-v15h-summary: `Documentation/v15k_mechanism_holdout_v15h_summary.csv`
- Mechanism-holdout-v15i-summary: `Documentation/v15k_mechanism_holdout_v15i_summary.csv`
- Mechanism-holdout-v15j-summary: `Documentation/v15k_mechanism_holdout_v15j_summary.csv`
- Mechanism-holdout-aggregate: `Documentation/v15k_mechanism_holdout_aggregate.csv`
- Mechanism-holdout-anbefaling: `Documentation/v0_15k_operativ_anbefaling.md`
- Holdout-failure-explainer-script: `relational_universe_v15l_holdout_failure_explainer.py`
- Holdout-failure-explainer-rapport: `Documentation/v15l_holdout_failure_explainer.md`
- Holdout-failure-comparison: `Documentation/v15l_holdout_failure_comparison.csv`
- Holdout-failure-aggregate: `Documentation/v15l_holdout_failure_aggregate.csv`
- Holdout-failure-anbefaling: `Documentation/v0_15l_operativ_anbefaling.md`
- Single-defect-survival-script: `relational_universe_v15m_single_defect_survival_lab.py`
- Single-defect-survival-rapport: `Documentation/v15m_single_defect_survival_lab.md`
- Single-defect-survival-runs: `Documentation/v15m_single_defect_survival_runs.csv`
- Single-defect-survival-aggregate: `Documentation/v15m_single_defect_survival_aggregate.csv`
- Single-defect-survival-target-summary: `Documentation/v15m_single_defect_survival_target_summary.csv`
- Single-defect-survival-anbefaling: `Documentation/v0_15m_operativ_anbefaling.md`
- Token-shift-fragility-script: `relational_universe_v15n_token_shift_fragility_lab.py`
- Token-shift-fragility-rapport: `Documentation/v15n_token_shift_fragility_lab.md`
- Token-shift-fragility-runs: `Documentation/v15n_token_shift_fragility_runs.csv`
- Token-shift-fragility-aggregate: `Documentation/v15n_token_shift_fragility_aggregate.csv`
- Token-shift-fragility-feature-summary: `Documentation/v15n_token_shift_fragility_feature_summary.csv`
- Token-shift-fragility-placement-contrast: `Documentation/v15n_token_shift_fragility_placement_contrast.csv`
- Token-shift-fragility-target-summary: `Documentation/v15n_token_shift_fragility_target_summary.csv`
- Token-shift-fragility-anbefaling: `Documentation/v0_15n_operativ_anbefaling.md`
- Token-shift-fragility-replication-script: `relational_universe_v15o_token_shift_fragility_replication.py`
- Token-shift-fragility-replication-rapport: `Documentation/v15o_token_shift_fragility_replication.md`
- Token-shift-fragility-profile-pairs: `Documentation/v15o_token_shift_fragility_profile_pairs.csv`
- Token-shift-fragility-replication-runs: `Documentation/v15o_token_shift_fragility_replication_runs.csv`
- Token-shift-fragility-replication-aggregate: `Documentation/v15o_token_shift_fragility_replication_aggregate.csv`
- Token-shift-fragility-pair-diagnosis: `Documentation/v15o_token_shift_fragility_pair_diagnosis.csv`
- Token-shift-fragility-replication-target-summary: `Documentation/v15o_token_shift_fragility_target_summary.csv`
- Token-shift-fragility-replication-anbefaling: `Documentation/v0_15o_operativ_anbefaling.md`
- Token-shift-profile-refinement-script: `relational_universe_v15p_token_shift_profile_refinement.py`
- Token-shift-profile-refinement-rapport: `Documentation/v15p_token_shift_profile_refinement.md`
- Token-shift-profile-refinement-runs: `Documentation/v15p_token_shift_profile_refinement_runs.csv`
- Token-shift-profile-refinement-aggregate: `Documentation/v15p_token_shift_profile_refinement_aggregate.csv`
- Token-shift-profile-refinement-diagnosis: `Documentation/v15p_token_shift_profile_refinement_diagnosis.csv`
- Token-shift-profile-refinement-target-summary: `Documentation/v15p_token_shift_profile_refinement_target_summary.csv`
- Token-shift-profile-refinement-anbefaling: `Documentation/v0_15p_operativ_anbefaling.md`
- Single-defect-recurrence-script: `relational_universe_v15q_single_defect_recurrence_lab.py`
- Single-defect-recurrence-rapport: `Documentation/v15q_single_defect_recurrence_lab.md`
- Single-defect-recurrence-runs: `Documentation/v15q_single_defect_recurrence_runs.csv`
- Single-defect-recurrence-aggregate: `Documentation/v15q_single_defect_recurrence_aggregate.csv`
- Single-defect-recurrence-target-summary: `Documentation/v15q_single_defect_recurrence_target_summary.csv`
- Single-defect-recurrence-anbefaling: `Documentation/v0_15q_operativ_anbefaling.md`
- Add-chord-long-horizon-script: `relational_universe_v15r_add_chord_long_horizon_recurrence.py`
- Add-chord-long-horizon-rapport: `Documentation/v15r_add_chord_long_horizon_recurrence.md`
- Add-chord-long-horizon-runs: `Documentation/v15r_add_chord_long_horizon_runs.csv`
- Add-chord-long-horizon-aggregate: `Documentation/v15r_add_chord_long_horizon_aggregate.csv`
- Add-chord-long-horizon-target-summary: `Documentation/v15r_add_chord_long_horizon_target_summary.csv`
- Add-chord-long-horizon-anbefaling: `Documentation/v0_15r_operativ_anbefaling.md`
- Add-chord-cycle-family-script: `relational_universe_v15s_add_chord_cycle_family_map.py`
- Add-chord-cycle-family-rapport: `Documentation/v15s_add_chord_cycle_family_map.md`
- Add-chord-cycle-family-runs: `Documentation/v15s_add_chord_cycle_family_runs.csv`
- Add-chord-cycle-family-diagnosis: `Documentation/v15s_add_chord_cycle_family_diagnosis.csv`
- Add-chord-cycle-family-target-summary: `Documentation/v15s_add_chord_cycle_family_target_summary.csv`
- Add-chord-cycle-family-anbefaling: `Documentation/v0_15s_operativ_anbefaling.md`
- Add-chord-cycle-center-script: `relational_universe_v15t_add_chord_cycle_center_holdout.py`
- Add-chord-cycle-center-rapport: `Documentation/v15t_add_chord_cycle_center_holdout.md`
- Add-chord-cycle-center-runs: `Documentation/v15t_add_chord_cycle_center_runs.csv`
- Add-chord-cycle-center-aggregate: `Documentation/v15t_add_chord_cycle_center_aggregate.csv`
- Add-chord-cycle-center-diagnosis: `Documentation/v15t_add_chord_cycle_center_diagnosis.csv`
- Add-chord-cycle-center-target-summary: `Documentation/v15t_add_chord_cycle_center_target_summary.csv`
- Add-chord-cycle-center-anbefaling: `Documentation/v0_15t_operativ_anbefaling.md`
- Add-chord-p1-microcenter-script: `relational_universe_v15u_add_chord_p1_microcenter.py`
- Add-chord-p1-microcenter-rapport: `Documentation/v15u_add_chord_p1_microcenter.md`
- Add-chord-p1-microcenter-runs: `Documentation/v15u_add_chord_p1_microcenter_runs.csv`
- Add-chord-p1-microcenter-aggregate: `Documentation/v15u_add_chord_p1_microcenter_aggregate.csv`
- Add-chord-p1-microcenter-diagnosis: `Documentation/v15u_add_chord_p1_microcenter_diagnosis.csv`
- Add-chord-p1-microcenter-target-summary: `Documentation/v15u_add_chord_p1_microcenter_target_summary.csv`
- Add-chord-p1-microcenter-anbefaling: `Documentation/v0_15u_operativ_anbefaling.md`
- Add-chord-triplet-mechanism-script: `relational_universe_v15v_add_chord_triplet_mechanism_lab.py`
- Add-chord-triplet-mechanism-rapport: `Documentation/v15v_add_chord_triplet_mechanism_lab.md`
- Add-chord-triplet-mechanism-runs: `Documentation/v15v_add_chord_triplet_mechanism_runs.csv`
- Add-chord-triplet-mechanism-tail-rows: `Documentation/v15v_add_chord_triplet_mechanism_tail_rows.csv`
- Add-chord-triplet-mechanism-aggregate: `Documentation/v15v_add_chord_triplet_mechanism_aggregate.csv`
- Add-chord-triplet-mechanism-diagnosis: `Documentation/v15v_add_chord_triplet_mechanism_diagnosis.csv`
- Add-chord-triplet-mechanism-target-summary: `Documentation/v15v_add_chord_triplet_mechanism_target_summary.csv`
- Add-chord-triplet-mechanism-anbefaling: `Documentation/v0_15v_operativ_anbefaling.md`
- Add-chord-p0-p1-support-contrast-script: `relational_universe_v15w_add_chord_p0_p1_support_contrast.py`
- Add-chord-p0-p1-support-contrast-rapport: `Documentation/v15w_add_chord_p0_p1_support_contrast.md`
- Add-chord-p0-p1-support-summary: `Documentation/v15w_add_chord_p0_p1_support_summary.csv`
- Add-chord-p0-p1-duel-rows: `Documentation/v15w_add_chord_p0_p1_duel_rows.csv`
- Add-chord-p0-p1-duel-aggregate: `Documentation/v15w_add_chord_p0_p1_duel_aggregate.csv`
- Add-chord-p0-p1-support-diagnosis: `Documentation/v15w_add_chord_p0_p1_support_diagnosis.csv`
- Add-chord-p0-p1-target-summary: `Documentation/v15w_add_chord_p0_p1_target_summary.csv`
- Add-chord-p0-p1-anbefaling: `Documentation/v0_15w_operativ_anbefaling.md`
- Add-chord-first-tail-segment-script: `relational_universe_v15x_add_chord_p0_p1_first_tail_segment.py`
- Add-chord-first-tail-segment-rapport: `Documentation/v15x_add_chord_p0_p1_first_tail_segment.md`
- Add-chord-first-tail-segment-runs: `Documentation/v15x_add_chord_p0_p1_first_tail_segment_runs.csv`
- Add-chord-first-tail-segment-duels: `Documentation/v15x_add_chord_p0_p1_first_tail_segment_duels.csv`
- Add-chord-first-tail-segment-aggregate: `Documentation/v15x_add_chord_p0_p1_first_tail_segment_aggregate.csv`
- Add-chord-first-tail-segment-diagnosis: `Documentation/v15x_add_chord_p0_p1_first_tail_segment_diagnosis.csv`
- Add-chord-first-tail-segment-target-summary: `Documentation/v15x_add_chord_p0_p1_first_tail_segment_target_summary.csv`
- Add-chord-first-tail-segment-anbefaling: `Documentation/v0_15x_operativ_anbefaling.md`
- P0-vs-p1-case-duel-script: `relational_universe_v15y_p0_p1_case_duel_lab.py`
- P0-vs-p1-case-duel-rapport: `Documentation/v15y_p0_p1_case_duel_lab.md`
- P0-vs-p1-case-duel-runs: `Documentation/v15y_p0_p1_case_duel_runs.csv`
- P0-vs-p1-case-duel-segments: `Documentation/v15y_p0_p1_case_duel_segments.csv`
- P0-vs-p1-case-duel-duels: `Documentation/v15y_p0_p1_case_duel_duels.csv`
- P0-vs-p1-case-duel-aggregate: `Documentation/v15y_p0_p1_case_duel_aggregate.csv`
- P0-vs-p1-case-duel-diagnosis: `Documentation/v15y_p0_p1_case_duel_diagnosis.csv`
- P0-vs-p1-case-duel-target-summary: `Documentation/v15y_p0_p1_case_duel_target_summary.csv`
- P0-vs-p1-case-duel-anbefaling: `Documentation/v0_15y_operativ_anbefaling.md`
- P0-vs-p1-case-trigger-script: `relational_universe_v15z_case_trigger_explainer.py`
- P0-vs-p1-case-trigger-rapport: `Documentation/v15z_case_trigger_explainer.md`
- P0-vs-p1-case-trigger-rows: `Documentation/v15z_case_trigger_rows.csv`
- P0-vs-p1-case-trigger-aggregate: `Documentation/v15z_case_trigger_aggregate.csv`
- P0-vs-p1-case-trigger-diagnosis: `Documentation/v15z_case_trigger_diagnosis.csv`
- P0-vs-p1-case-trigger-target-summary: `Documentation/v15z_case_trigger_target_summary.csv`
- P0-vs-p1-case-trigger-anbefaling: `Documentation/v0_15z_operativ_anbefaling.md`
- P0-vs-p1-case-trigger-holdout-script: `relational_universe_v15aa_case_trigger_holdout.py`
- P0-vs-p1-case-trigger-holdout-rapport: `Documentation/v15aa_case_trigger_holdout.md`
- P0-vs-p1-case-trigger-holdout-runs: `Documentation/v15aa_case_trigger_holdout_runs.csv`
- P0-vs-p1-case-trigger-holdout-segments: `Documentation/v15aa_case_trigger_holdout_segments.csv`
- P0-vs-p1-case-trigger-holdout-rows: `Documentation/v15aa_case_trigger_holdout_rows.csv`
- P0-vs-p1-case-trigger-holdout-aggregate: `Documentation/v15aa_case_trigger_holdout_aggregate.csv`
- P0-vs-p1-case-trigger-holdout-diagnosis: `Documentation/v15aa_case_trigger_holdout_diagnosis.csv`
- P0-vs-p1-case-trigger-holdout-target-summary: `Documentation/v15aa_case_trigger_holdout_target_summary.csv`
- P0-vs-p1-case-trigger-holdout-anbefaling: `Documentation/v0_15aa_operativ_anbefaling.md`
- Add-chord-cycle-lag-script: `relational_universe_v15ab_add_chord_cycle_lag_lab.py`
- Add-chord-cycle-lag-rapport: `Documentation/v15ab_add_chord_cycle_lag_lab.md`
- Add-chord-cycle-lag-runs: `Documentation/v15ab_add_chord_cycle_lag_runs.csv`
- Add-chord-cycle-lag-aggregate: `Documentation/v15ab_add_chord_cycle_lag_aggregate.csv`
- Add-chord-cycle-lag-diagnosis: `Documentation/v15ab_add_chord_cycle_lag_diagnosis.csv`
- Add-chord-cycle-lag-target-summary: `Documentation/v15ab_add_chord_cycle_lag_target_summary.csv`
- Add-chord-cycle-lag-anbefaling: `Documentation/v0_15ab_operativ_anbefaling.md`
- Add-chord-core-shell-script: `relational_universe_v15ac_add_chord_core_shell_lab.py`
- Add-chord-core-shell-rapport: `Documentation/v15ac_add_chord_core_shell_lab.md`
- Add-chord-core-shell-runs: `Documentation/v15ac_add_chord_core_shell_runs.csv`
- Add-chord-core-shell-aggregate: `Documentation/v15ac_add_chord_core_shell_aggregate.csv`
- Add-chord-core-shell-diagnosis: `Documentation/v15ac_add_chord_core_shell_diagnosis.csv`
- Add-chord-core-shell-target-summary: `Documentation/v15ac_add_chord_core_shell_target_summary.csv`
- Add-chord-core-shell-anbefaling: `Documentation/v0_15ac_operativ_anbefaling.md`
- Add-chord-boundary-shell-script: `relational_universe_v15ad_add_chord_boundary_shell_lab.py`
- Add-chord-boundary-shell-rapport: `Documentation/v15ad_add_chord_boundary_shell_lab.md`
- Add-chord-boundary-shell-runs: `Documentation/v15ad_add_chord_boundary_shell_runs.csv`
- Add-chord-boundary-shell-aggregate: `Documentation/v15ad_add_chord_boundary_shell_aggregate.csv`
- Add-chord-boundary-shell-diagnosis: `Documentation/v15ad_add_chord_boundary_shell_diagnosis.csv`
- Add-chord-boundary-shell-target-summary: `Documentation/v15ad_add_chord_boundary_shell_target_summary.csv`
- Add-chord-boundary-shell-anbefaling: `Documentation/v0_15ad_operativ_anbefaling.md`
- Add-chord-shell-topology-script: `relational_universe_v15ae_add_chord_shell_topology_lab.py`
- Add-chord-shell-topology-rapport: `Documentation/v15ae_add_chord_shell_topology_lab.md`
- Add-chord-shell-topology-runs: `Documentation/v15ae_add_chord_shell_topology_runs.csv`
- Add-chord-shell-topology-snapshots: `Documentation/v15ae_add_chord_shell_topology_snapshots.csv`
- Add-chord-shell-topology-aggregate: `Documentation/v15ae_add_chord_shell_topology_aggregate.csv`
- Add-chord-shell-topology-diagnosis: `Documentation/v15ae_add_chord_shell_topology_diagnosis.csv`
- Add-chord-shell-topology-target-summary: `Documentation/v15ae_add_chord_shell_topology_target_summary.csv`
- Add-chord-shell-topology-anbefaling: `Documentation/v0_15ae_operativ_anbefaling.md`
- Add-chord-shell-fragment-event-script: `relational_universe_v15af_add_chord_shell_fragment_event_lab.py`
- Add-chord-shell-fragment-event-rapport: `Documentation/v15af_add_chord_shell_fragment_event_lab.md`
- Add-chord-shell-fragment-event-runs: `Documentation/v15af_add_chord_shell_fragment_runs.csv`
- Add-chord-shell-fragment-event-segments: `Documentation/v15af_add_chord_shell_fragment_segments.csv`
- Add-chord-shell-fragment-event-aggregate: `Documentation/v15af_add_chord_shell_fragment_aggregate.csv`
- Add-chord-shell-fragment-event-diagnosis: `Documentation/v15af_add_chord_shell_fragment_diagnosis.csv`
- Add-chord-shell-fragment-event-target-summary: `Documentation/v15af_add_chord_shell_fragment_target_summary.csv`
- Add-chord-shell-fragment-event-anbefaling: `Documentation/v0_15af_operativ_anbefaling.md`
- Add-chord-shell-exception-script: `relational_universe_v15ag_shell_exception_explainer.py`
- Add-chord-shell-exception-rapport: `Documentation/v15ag_shell_exception_explainer.md`
- Add-chord-shell-exception-rows: `Documentation/v15ag_shell_exception_rows.csv`
- Add-chord-shell-exception-aggregate: `Documentation/v15ag_shell_exception_aggregate.csv`
- Add-chord-shell-exception-diagnosis: `Documentation/v15ag_shell_exception_diagnosis.csv`
- Add-chord-shell-exception-target-summary: `Documentation/v15ag_shell_exception_target_summary.csv`
- Add-chord-shell-exception-anbefaling: `Documentation/v0_15ag_operativ_anbefaling.md`
- Add-chord-shell-exception-holdout-script: `relational_universe_v15ah_shell_exception_holdout.py`
- Add-chord-shell-exception-holdout-rapport: `Documentation/v15ah_shell_exception_holdout.md`
- Add-chord-shell-exception-holdout-runs: `Documentation/v15ah_shell_exception_holdout_runs.csv`
- Add-chord-shell-exception-holdout-aggregate: `Documentation/v15ah_shell_exception_holdout_aggregate.csv`
- Add-chord-shell-exception-holdout-diagnosis: `Documentation/v15ah_shell_exception_holdout_diagnosis.csv`
- Add-chord-shell-exception-holdout-target-summary: `Documentation/v15ah_shell_exception_holdout_target_summary.csv`
- Add-chord-shell-exception-holdout-anbefaling: `Documentation/v0_15ah_operativ_anbefaling.md`
- Add-chord-early-lock-band-script: `relational_universe_v15ai_early_lock_band_lab.py`
- Add-chord-early-lock-band-rapport: `Documentation/v15ai_early_lock_band_lab.md`
- Add-chord-early-lock-band-runs: `Documentation/v15ai_early_lock_band_runs.csv`
- Add-chord-early-lock-band-snapshots: `Documentation/v15ai_early_lock_band_snapshots.csv`
- Add-chord-early-lock-band-aggregate: `Documentation/v15ai_early_lock_band_aggregate.csv`
- Add-chord-early-lock-band-diagnosis: `Documentation/v15ai_early_lock_band_diagnosis.csv`
- Add-chord-early-lock-band-target-summary: `Documentation/v15ai_early_lock_band_target_summary.csv`
- Add-chord-early-lock-band-anbefaling: `Documentation/v0_15ai_operativ_anbefaling.md`
- Add-chord-early-lock-band-onset-script: `relational_universe_v15aj_early_lock_band_onset_lab.py`
- Add-chord-early-lock-band-onset-rapport: `Documentation/v15aj_early_lock_band_onset_lab.md`
- Add-chord-early-lock-band-onset-runs: `Documentation/v15aj_early_lock_band_onset_runs.csv`
- Add-chord-early-lock-band-onset-aggregate: `Documentation/v15aj_early_lock_band_onset_aggregate.csv`
- Add-chord-early-lock-band-onset-diagnosis: `Documentation/v15aj_early_lock_band_onset_diagnosis.csv`
- Add-chord-early-lock-band-onset-target-summary: `Documentation/v15aj_early_lock_band_onset_target_summary.csv`
- Add-chord-early-lock-band-onset-anbefaling: `Documentation/v0_15aj_operativ_anbefaling.md`
- Add-chord-band-entry-trigger-script: `relational_universe_v15ak_band_entry_trigger_lab.py`
- Add-chord-band-entry-trigger-rapport: `Documentation/v15ak_band_entry_trigger_lab.md`
- Add-chord-band-entry-trigger-runs: `Documentation/v15ak_band_entry_trigger_runs.csv`
- Add-chord-band-entry-trigger-aggregate: `Documentation/v15ak_band_entry_trigger_aggregate.csv`
- Add-chord-band-entry-trigger-diagnosis: `Documentation/v15ak_band_entry_trigger_diagnosis.csv`
- Add-chord-band-entry-trigger-target-summary: `Documentation/v15ak_band_entry_trigger_target_summary.csv`
- Add-chord-band-entry-trigger-anbefaling: `Documentation/v0_15ak_operativ_anbefaling.md`
- Add-chord-boundary-zone-split-script: `relational_universe_v15al_boundary_zone_split_lab.py`
- Add-chord-boundary-zone-split-rapport: `Documentation/v15al_boundary_zone_split_lab.md`
- Add-chord-boundary-zone-split-runs: `Documentation/v15al_boundary_zone_split_runs.csv`
- Add-chord-boundary-zone-split-aggregate: `Documentation/v15al_boundary_zone_split_aggregate.csv`
- Add-chord-boundary-zone-split-diagnosis: `Documentation/v15al_boundary_zone_split_diagnosis.csv`
- Add-chord-boundary-zone-split-target-summary: `Documentation/v15al_boundary_zone_split_target_summary.csv`
- Add-chord-boundary-zone-split-anbefaling: `Documentation/v0_15al_operativ_anbefaling.md`
- Add-chord-boundary-overlap-explainer-script: `relational_universe_v15am_boundary_overlap_explainer.py`
- Add-chord-boundary-overlap-explainer-rapport: `Documentation/v15am_boundary_overlap_explainer.md`
- Add-chord-boundary-overlap-explainer-runs: `Documentation/v15am_boundary_overlap_explainer_runs.csv`
- Add-chord-boundary-overlap-explainer-aggregate: `Documentation/v15am_boundary_overlap_explainer_aggregate.csv`
- Add-chord-boundary-overlap-explainer-diagnosis: `Documentation/v15am_boundary_overlap_explainer_diagnosis.csv`
- Add-chord-boundary-overlap-explainer-target-summary: `Documentation/v15am_boundary_overlap_explainer_target_summary.csv`
- Add-chord-boundary-overlap-explainer-anbefaling: `Documentation/v0_15am_operativ_anbefaling.md`
- Add-chord-boundary-high-hold-script: `relational_universe_v15an_boundary_high_hold_lab.py`
- Add-chord-boundary-high-hold-rapport: `Documentation/v15an_boundary_high_hold_lab.md`
- Add-chord-boundary-high-hold-runs: `Documentation/v15an_boundary_high_hold_runs.csv`
- Add-chord-boundary-high-hold-aggregate: `Documentation/v15an_boundary_high_hold_aggregate.csv`
- Add-chord-boundary-high-hold-diagnosis: `Documentation/v15an_boundary_high_hold_diagnosis.csv`
- Add-chord-boundary-high-hold-target-summary: `Documentation/v15an_boundary_high_hold_target_summary.csv`
- Add-chord-boundary-high-hold-anbefaling: `Documentation/v0_15an_operativ_anbefaling.md`
- Add-chord-terminal-probe-boundary-script: `relational_universe_v15ao_terminal_probe_boundary_lab.py`
- Add-chord-terminal-probe-boundary-rapport: `Documentation/v15ao_terminal_probe_boundary_lab.md`
- Add-chord-terminal-probe-boundary-runs: `Documentation/v15ao_terminal_probe_boundary_runs.csv`
- Add-chord-terminal-probe-boundary-aggregate: `Documentation/v15ao_terminal_probe_boundary_aggregate.csv`
- Add-chord-terminal-probe-boundary-diagnosis: `Documentation/v15ao_terminal_probe_boundary_diagnosis.csv`
- Add-chord-terminal-probe-boundary-target-summary: `Documentation/v15ao_terminal_probe_boundary_target_summary.csv`
- Add-chord-terminal-probe-boundary-anbefaling: `Documentation/v0_15ao_operativ_anbefaling.md`
- Add-chord-pre-high-launch-script: `relational_universe_v15ap_pre_high_launch_lab.py`
- Add-chord-pre-high-launch-rapport: `Documentation/v15ap_pre_high_launch_lab.md`
- Add-chord-pre-high-launch-runs: `Documentation/v15ap_pre_high_launch_runs.csv`
- Add-chord-pre-high-launch-aggregate: `Documentation/v15ap_pre_high_launch_aggregate.csv`
- Add-chord-pre-high-launch-diagnosis: `Documentation/v15ap_pre_high_launch_diagnosis.csv`
- Add-chord-pre-high-launch-target-summary: `Documentation/v15ap_pre_high_launch_target_summary.csv`
- Add-chord-pre-high-launch-anbefaling: `Documentation/v0_15ap_operativ_anbefaling.md`
- Add-chord-high-launch-impulse-script: `relational_universe_v15aq_high_launch_impulse_lab.py`
- Add-chord-high-launch-impulse-rapport: `Documentation/v15aq_high_launch_impulse_lab.md`
- Add-chord-high-launch-impulse-runs: `Documentation/v15aq_high_launch_impulse_runs.csv`
- Add-chord-high-launch-impulse-aggregate: `Documentation/v15aq_high_launch_impulse_aggregate.csv`
- Add-chord-high-launch-impulse-diagnosis: `Documentation/v15aq_high_launch_impulse_diagnosis.csv`
- Add-chord-high-launch-impulse-target-summary: `Documentation/v15aq_high_launch_impulse_target_summary.csv`
- Add-chord-high-launch-impulse-anbefaling: `Documentation/v0_15aq_operativ_anbefaling.md`
- Add-chord-high-retention-horizon-script: `relational_universe_v15ar_high_retention_horizon_lab.py`
- Add-chord-high-retention-horizon-rapport: `Documentation/v15ar_high_retention_horizon_lab.md`
- Add-chord-high-retention-horizon-runs: `Documentation/v15ar_high_retention_horizon_runs.csv`
- Add-chord-high-retention-horizon-aggregate: `Documentation/v15ar_high_retention_horizon_aggregate.csv`
- Add-chord-high-retention-horizon-diagnosis: `Documentation/v15ar_high_retention_horizon_diagnosis.csv`
- Add-chord-high-retention-horizon-target-summary: `Documentation/v15ar_high_retention_horizon_target_summary.csv`
- Add-chord-high-retention-horizon-anbefaling: `Documentation/v0_15ar_operativ_anbefaling.md`
- Add-chord-horizon-holdout-script: `relational_universe_v15as_horizon_map_holdout.py`
- Add-chord-horizon-holdout-rapport: `Documentation/v15as_horizon_map_holdout.md`
- Add-chord-horizon-holdout-runs: `Documentation/v15as_horizon_map_holdout_runs.csv`
- Add-chord-horizon-holdout-aggregate: `Documentation/v15as_horizon_map_holdout_aggregate.csv`
- Add-chord-horizon-holdout-diagnosis: `Documentation/v15as_horizon_map_holdout_diagnosis.csv`
- Add-chord-horizon-holdout-target-summary: `Documentation/v15as_horizon_map_holdout_target_summary.csv`
- Add-chord-horizon-holdout-anbefaling: `Documentation/v0_15as_operativ_anbefaling.md`
- Add-chord-high-burst-window-script: `relational_universe_v15at_high_burst_window_lab.py`
- Add-chord-high-burst-window-rapport: `Documentation/v15at_high_burst_window_lab.md`
- Add-chord-high-burst-window-runs: `Documentation/v15at_high_burst_window_runs.csv`
- Add-chord-high-burst-window-aggregate: `Documentation/v15at_high_burst_window_aggregate.csv`
- Add-chord-high-burst-window-diagnosis: `Documentation/v15at_high_burst_window_diagnosis.csv`
- Add-chord-high-burst-window-target-summary: `Documentation/v15at_high_burst_window_target_summary.csv`
- Add-chord-high-burst-window-anbefaling: `Documentation/v0_15at_operativ_anbefaling.md`
- Add-chord-post-peak-fade-script: `relational_universe_v15au_post_peak_fade_explainer.py`
- Add-chord-post-peak-fade-rapport: `Documentation/v15au_post_peak_fade_explainer.md`
- Add-chord-post-peak-fade-runs: `Documentation/v15au_post_peak_fade_runs.csv`
- Add-chord-post-peak-fade-diagnosis: `Documentation/v15au_post_peak_fade_diagnosis.csv`
- Add-chord-post-peak-fade-target-summary: `Documentation/v15au_post_peak_fade_target_summary.csv`
- Add-chord-post-peak-fade-anbefaling: `Documentation/v0_15au_operativ_anbefaling.md`
- Add-chord-post-peak-fade-holdout-script: `relational_universe_v15av_post_peak_fade_holdout.py`
- Add-chord-post-peak-fade-holdout-rapport: `Documentation/v15av_post_peak_fade_holdout.md`
- Add-chord-post-peak-fade-holdout-runs: `Documentation/v15av_post_peak_fade_holdout_runs.csv`
- Add-chord-post-peak-fade-holdout-diagnosis: `Documentation/v15av_post_peak_fade_holdout_diagnosis.csv`
- Add-chord-post-peak-fade-holdout-target-summary: `Documentation/v15av_post_peak_fade_holdout_target_summary.csv`
- Add-chord-post-peak-fade-holdout-anbefaling: `Documentation/v0_15av_operativ_anbefaling.md`
- Local-swap-core-shell-script: `relational_universe_v15aw_local_swap_core_shell_lab.py`
- Local-swap-core-shell-rapport: `Documentation/v15aw_local_swap_core_shell_lab.md`
- Local-swap-core-shell-runs: `Documentation/v15aw_local_swap_core_shell_runs.csv`
- Local-swap-core-shell-aggregate: `Documentation/v15aw_local_swap_core_shell_aggregate.csv`
- Local-swap-core-shell-diagnosis: `Documentation/v15aw_local_swap_core_shell_diagnosis.csv`
- Local-swap-core-shell-target-summary: `Documentation/v15aw_local_swap_core_shell_target_summary.csv`
- Local-swap-core-shell-anbefaling: `Documentation/v0_15aw_operativ_anbefaling.md`
- Local-swap-size-split-script: `relational_universe_v15ax_local_swap_size_split_explainer.py`
- Local-swap-size-split-rapport: `Documentation/v15ax_local_swap_size_split_explainer.md`
- Local-swap-size-split-aggregate: `Documentation/v15ax_local_swap_size_split_aggregate.csv`
- Local-swap-size-split-placements: `Documentation/v15ax_local_swap_size_split_placements.csv`
- Local-swap-size-split-diagnosis: `Documentation/v15ax_local_swap_size_split_diagnosis.csv`
- Local-swap-size-split-anbefaling: `Documentation/v0_15ax_operativ_anbefaling.md`
- Local-swap-96-pocket-script: `relational_universe_v15ay_local_swap_96_pocket_explainer.py`
- Local-swap-96-pocket-rapport: `Documentation/v15ay_local_swap_96_pocket_explainer.md`
- Local-swap-96-pocket-rows: `Documentation/v15ay_local_swap_96_pocket_rows.csv`
- Local-swap-96-pocket-aggregate: `Documentation/v15ay_local_swap_96_pocket_aggregate.csv`
- Local-swap-96-pocket-diagnosis: `Documentation/v15ay_local_swap_96_pocket_diagnosis.csv`
- Local-swap-96-pocket-anbefaling: `Documentation/v0_15ay_operativ_anbefaling.md`
- Local-swap-p3-seed-flip-script: `relational_universe_v15az_local_swap_p3_seed_flip_explainer.py`
- Local-swap-p3-seed-flip-rapport: `Documentation/v15az_local_swap_p3_seed_flip_explainer.md`
- Local-swap-p3-seed-flip-rows: `Documentation/v15az_local_swap_p3_seed_flip_rows.csv`
- Local-swap-p3-seed-flip-summary: `Documentation/v15az_local_swap_p3_seed_flip_summary.csv`
- Local-swap-p3-seed-flip-diagnosis: `Documentation/v15az_local_swap_p3_seed_flip_diagnosis.csv`
- Local-swap-p3-seed-flip-anbefaling: `Documentation/v0_15az_operativ_anbefaling.md`
- Local-swap-compressed-shell-script: `relational_universe_v15ba_local_swap_compressed_shell_explainer.py`
- Local-swap-compressed-shell-rapport: `Documentation/v15ba_local_swap_compressed_shell_explainer.md`
- Local-swap-compressed-shell-rows: `Documentation/v15ba_local_swap_compressed_shell_rows.csv`
- Local-swap-compressed-shell-summary: `Documentation/v15ba_local_swap_compressed_shell_summary.csv`
- Local-swap-compressed-shell-diagnosis: `Documentation/v15ba_local_swap_compressed_shell_diagnosis.csv`
- Local-swap-compressed-shell-anbefaling: `Documentation/v0_15ba_operativ_anbefaling.md`
- Local-swap-growth202-mode-map-script: `relational_universe_v15bb_local_swap_growth202_mode_map.py`
- Local-swap-growth202-mode-map-rapport: `Documentation/v15bb_local_swap_growth202_mode_map.md`
- Local-swap-growth202-mode-map-rows: `Documentation/v15bb_local_swap_growth202_mode_rows.csv`
- Local-swap-growth202-mode-map-aggregate: `Documentation/v15bb_local_swap_growth202_mode_aggregate.csv`
- Local-swap-growth202-mode-map-diagnosis: `Documentation/v15bb_local_swap_growth202_mode_diagnosis.csv`
- Local-swap-growth202-mode-map-anbefaling: `Documentation/v0_15bb_operativ_anbefaling.md`
- Local-swap-p3-vs-p1-p2-contrast-script: `relational_universe_v15bc_local_swap_p3_vs_p1_p2_contrast.py`
- Local-swap-p3-vs-p1-p2-contrast-rapport: `Documentation/v15bc_local_swap_p3_vs_p1_p2_contrast.md`
- Local-swap-p3-vs-p1-p2-contrast-rows: `Documentation/v15bc_local_swap_p3_vs_p1_p2_rows.csv`
- Local-swap-p3-vs-p1-p2-contrast-pairs: `Documentation/v15bc_local_swap_p3_vs_p1_p2_pairs.csv`
- Local-swap-p3-vs-p1-p2-contrast-diagnosis: `Documentation/v15bc_local_swap_p3_vs_p1_p2_diagnosis.csv`
- Local-swap-p3-vs-p1-p2-contrast-anbefaling: `Documentation/v0_15bc_operativ_anbefaling.md`
- Local-swap-trigger-axis-script: `relational_universe_v15bd_local_swap_trigger_axis_lab.py`
- Local-swap-trigger-axis-rapport: `Documentation/v15bd_local_swap_trigger_axis_lab.md`
- Local-swap-trigger-axis-placements: `Documentation/v15bd_local_swap_trigger_axis_placements.csv`
- Local-swap-trigger-axis-candidates: `Documentation/v15bd_local_swap_trigger_axis_candidates.csv`
- Local-swap-trigger-axis-diagnosis: `Documentation/v15bd_local_swap_trigger_axis_diagnosis.csv`
- Local-swap-trigger-axis-anbefaling: `Documentation/v0_15bd_operativ_anbefaling.md`
- Local-swap-trigger-axis-components-script: `relational_universe_v15be_local_swap_trigger_axis_component_lab.py`
- Local-swap-trigger-axis-components-rapport: `Documentation/v15be_local_swap_trigger_axis_component_lab.md`
- Local-swap-trigger-axis-components-pairs: `Documentation/v15be_local_swap_trigger_axis_pairs.csv`
- Local-swap-trigger-axis-components-aggregate: `Documentation/v15be_local_swap_trigger_axis_aggregate.csv`
- Local-swap-trigger-axis-components-anbefaling: `Documentation/v0_15be_operativ_anbefaling.md`
- Local-swap-gap-asymmetry-script: `relational_universe_v15bf_local_swap_gap_asymmetry_explainer.py`
- Local-swap-gap-asymmetry-rapport: `Documentation/v15bf_local_swap_gap_asymmetry_explainer.md`
- Local-swap-gap-asymmetry-rows: `Documentation/v15bf_local_swap_gap_asymmetry_rows.csv`
- Local-swap-gap-asymmetry-diagnosis: `Documentation/v15bf_local_swap_gap_asymmetry_diagnosis.csv`
- Local-swap-gap-asymmetry-anbefaling: `Documentation/v0_15bf_operativ_anbefaling.md`
- Local-swap-shell-drag-script: `relational_universe_v15bg_local_swap_shell_drag_decomposition.py`
- Local-swap-shell-drag-rapport: `Documentation/v15bg_local_swap_shell_drag_decomposition.md`
- Local-swap-shell-drag-placements: `Documentation/v15bg_local_swap_shell_drag_placements.csv`
- Local-swap-shell-drag-rows: `Documentation/v15bg_local_swap_shell_drag_rows.csv`
- Local-swap-shell-drag-diagnosis: `Documentation/v15bg_local_swap_shell_drag_diagnosis.csv`
- Local-swap-shell-drag-anbefaling: `Documentation/v0_15bg_operativ_anbefaling.md`
- Local-swap-rare-load-trigger-script: `relational_universe_v15bh_local_swap_rare_load_trigger_lab.py`
- Local-swap-rare-load-trigger-rapport: `Documentation/v15bh_local_swap_rare_load_trigger_lab.md`
- Local-swap-rare-load-trigger-placements: `Documentation/v15bh_local_swap_rare_load_trigger_placements.csv`
- Local-swap-rare-load-trigger-axes: `Documentation/v15bh_local_swap_rare_load_trigger_axes.csv`
- Local-swap-rare-load-trigger-diagnosis: `Documentation/v15bh_local_swap_rare_load_trigger_diagnosis.csv`
- Local-swap-rare-load-trigger-anbefaling: `Documentation/v0_15bh_operativ_anbefaling.md`
- Local-swap-load-stabilizer-script: `relational_universe_v15bi_local_swap_load_stabilizer_flip.py`
- Local-swap-load-stabilizer-rapport: `Documentation/v15bi_local_swap_load_stabilizer_flip.md`
- Local-swap-load-stabilizer-placements: `Documentation/v15bi_local_swap_load_stabilizer_placements.csv`
- Local-swap-load-stabilizer-axes: `Documentation/v15bi_local_swap_load_stabilizer_axes.csv`
- Local-swap-load-stabilizer-diagnosis: `Documentation/v15bi_local_swap_load_stabilizer_diagnosis.csv`
- Local-swap-load-stabilizer-anbefaling: `Documentation/v0_15bi_operativ_anbefaling.md`
- Local-swap-stabilizer-components-script: `relational_universe_v15bj_local_swap_stabilizer_component_lab.py`
- Local-swap-stabilizer-components-rapport: `Documentation/v15bj_local_swap_stabilizer_component_lab.md`
- Local-swap-stabilizer-components-csv: `Documentation/v15bj_local_swap_stabilizer_components.csv`
- Local-swap-stabilizer-components-diagnosis: `Documentation/v15bj_local_swap_stabilizer_diagnosis.csv`
- Local-swap-stabilizer-components-anbefaling: `Documentation/v0_15bj_operativ_anbefaling.md`
- Local-swap-load-stabilizer-mode-map-script: `relational_universe_v15bk_local_swap_load_stabilizer_mode_map.py`
- Local-swap-load-stabilizer-mode-map-rapport: `Documentation/v15bk_local_swap_load_stabilizer_mode_map.md`
- Local-swap-load-stabilizer-mode-map-rows: `Documentation/v15bk_local_swap_load_stabilizer_mode_rows.csv`
- Local-swap-load-stabilizer-mode-map-diagnosis: `Documentation/v15bk_local_swap_load_stabilizer_mode_diagnosis.csv`
- Local-swap-load-stabilizer-mode-map-anbefaling: `Documentation/v0_15bk_operativ_anbefaling.md`
- Conditional-quasi-invariant-script: `relational_universe_v15bl_conditional_quasi_invariant_lab.py`
- Conditional-quasi-invariant-rapport: `Documentation/v15bl_conditional_quasi_invariant_lab.md`
- Conditional-quasi-invariant-target-sammendrag: `Documentation/v15bl_conditional_quasi_invariant_target_summary.csv`
- Conditional-quasi-invariant-rows: `Documentation/v15bl_conditional_quasi_invariant_rows.csv`
- Conditional-quasi-invariant-aggregate: `Documentation/v15bl_conditional_quasi_invariant_aggregate.csv`
- Conditional-quasi-invariant-diagnosis: `Documentation/v15bl_conditional_quasi_invariant_diagnosis.csv`
- Conditional-quasi-invariant-anbefaling: `Documentation/v0_15bl_operativ_anbefaling.md`
- Samlet status for ikke-spesialister: `Documentation/relasjonell_universgraf_status_for_ikke_spesialister_v0_13i.md`
- Oppdatert samlet status for ikke-spesialister: `Documentation/relasjonell_universgraf_status_for_ikke_spesialister_v0_13j.md`
- Nyeste samlede status for ikke-spesialister: `Documentation/relasjonell_universgraf_status_for_ikke_spesialister_v0_13k.md`
- Oppdatert samlet status for ikke-spesialister etter `v13l`: `Documentation/relasjonell_universgraf_status_for_ikke_spesialister_v0_13l.md`
- Oppdatert samlet status for ikke-spesialister etter `v13m`: `Documentation/relasjonell_universgraf_status_for_ikke_spesialister_v0_13m.md`
- Oppdatert samlet status for ikke-spesialister etter `v13n`: `Documentation/relasjonell_universgraf_status_for_ikke_spesialister_v0_13n.md`

## Live frontier akkurat na

Den nyeste repo-stottede operative kandidaten er:

- `band_zero_del`

Dette er fordi `v11e` viser at `band_zero_del` vinner pa:

- raw `mean_composite`
- `CI low`
- pairwise bootstrap
- focused-score

## Nyeste local_swap-live state

`v15bd`, `v15be`, `v15bf`, `v15bg`, `v15bh`, `v15bi`, `v15bj`, `v15bk` og `v15bl` skjerpet local_swap-/conditional-quasi-sporet uten a aapne nye brede scans:

- `v15bd` viser at den reneste lille triggeraksen for `growth_seed 202`-modiene er dynamisk, ikke geometrisk
- den beste aksen er `retention_core_axis = coarse_return + core_to_shell`
- enkle stotteakser som `support_compactness_axis` og `support_density_axis` holder ikke ren ordering
- `v15be` viser at denne aksen ikke er monolittisk
- `p1 > p3` drives mest av `core_to_shell`
- `p3 > p2` drives av en mer balansert blanding av `coarse_return` og `core_to_shell`
- `v15bf` viser at disse to nabogapene heller ikke er samme type overgang
- `p1 > p3` leses best som `core_shape_separation`
- `p3 > p2` leses best som `retention_plus_shell_drag`
- `v15bg` viser at shell-drag-siden i `p3 > p2` nesten helt bæres av `rare`-last, ikke av bredere ordinær shell
- `p2` har nesten samme shell-share som `p3`, men klart høyere rare-share
- `v15bh` viser at `p2` også kan leses som en egen lokal støtte-/last-retning
- flere små akser setter `p2` tydelig øverst, men ingen av dem løser samtidig hele rare-rangeringen `p2 > p3 > p1`
- `v15bi` viser at `p2` og `p1` faktisk skilles av en liten load-vs-stabilizer-flip
- `p2` topper alle små last-akser
- `p1` topper alle små stabiliseringsakser
- `v15bj` viser at stabiliseringsunderskuddet i `p2` er retention-led
- retention dekker `0.561` av stabiliseringsgapet, core `0.298`, shell-lagdeling `0.140`
- `v15bk` samler dette til et lite moduskart
- `p1` blir `buffered_heavy_load`
- `p2` blir `rare_load_risk`
- `p3` blir `low_load_diffuse`
- `v15bl` gar tilbake til quasi-invariant-sporet, men condition-er pa lokale carrier-familier i stedet for a blande alle run sammen
- i add_chord-bandet blir spektral drift skarpere i `cycle_band_p2` enn i pooled familie
- i local_swap-moduskartet blir spektral drift skarpere i `low_load_diffuse` enn i pooled mode-familie
- dermed har repoet na minst ett delt familiespesifikt spektralt delsignal i bade add_chord og local_swap, uten at dette skal leses som en universell lov ennå

Den riktige live-lesningen na er derfor:

- growth_seed-202-splittelsen leses best gjennom en liten dynamisk retention+kjerne-akse
- men aksen maa fortsatt leses som en to-komponentsplitt, ikke som ett enkelt universelt maal
- og de to nabogapene inne i aksen er selv asymmetriske, ikke bare svakere/sterkere versjoner av samme overgang
- den balanserte `p3 > p2`-overgangen leses na best som retention pluss rare-loaded shell-drag
- `p2` ser samtidig ut til a ha en egen lokal støtte-/last-trigger, selv om den ikke alene forklarer hele `p1/p2/p3`-rekkefolgen
- `p2` og `p1` skilles na best som høy last uten nok stabilisering vs litt lavere last med sterkere stabilisering
- `v15bl` viser samtidig at spektral relativ drift blir mer interessant hvis vi condition-er pa disse lokale carrier-familiene
- den sterkeste nye quasi-invariant-lesningen er fortsatt familiespesifikk sharpening, ikke en ny global invariant
- dette stabiliseringsunderskuddet er ikke flatt: det er retention-led, med core som tydelig sekundarkomponent
- growth_seed-202-kartet leses na best som tre lokale modi: tung last med buffer, tung last uten nok buffer, og lavere last med diffus retur
- neste riktige steg er enten a forklare risiko-siden enda smalere, eller a bruke dette kartet i en mer direkte local_swap-vs-add_chord-sammenlikning

og slar den siste smale utfordreren `bridge_00075_0000` rent:

- `P(band_zero_del > bridge_00075_0000) = 1.000`
- `P(bridge_00075_0000 > band_zero_del) = 0.000`

## Viktige tall fra v11e

Fra `Documentation/v11e_band_vs_bridge0075_candidate_summary.csv`:

- `band_zero_del`
  - `mean_composite ~= 0.554`
  - `CI low ~= 0.505`
  - `top_prob ~= 1.000`
  - `pairwise_mean ~= 1.000`
  - `focused_score ~= 0.600`

- `bridge_00075_0000`
  - `mean_composite ~= 0.417`
  - `CI low ~= 0.376`
  - `top_prob ~= 0.000`
  - `pairwise_mean ~= 0.000`
  - `focused_score ~= 0.400`

Fra `Documentation/v11e_band_vs_bridge0075_pairwise.csv`:

- `P(band_zero_del > bridge_00075_0000) = 1.000`
- `P(bridge_00075_0000 > band_zero_del) = 0.000`

## Viktige signaler fra v12 / v12b / v12c / v12d / v12e / v12f / v12g / v12h / v12i / v12j / v12k / v12l / v12m / v12n / v13 / v13b / v13c / v13d / v13e / v13f / v13g / v13h / v13i

`v12`, `v12b`, `v12c`, `v12d`, `v12e`, `v12f`, `v12g`, `v12h`, `v12i`, `v12j`, `v12k`, `v12l`, `v12m`, `v12n`, `v13`, `v13b`, `v13c`, `v13d`, `v13e`, `v13f`, `v13g`, `v13h` og `v13i` er ikke nye frontier-runder. De fryser `band_zero_del` og ser etter enklere struktur.

Det nye i `v14` er at prosjektet tok et bevisst sideblikk mot Lorentz-likhet uten a blande det inn i frontier-tuning:

- startstorrelsene er fortsatt rent separert
- fallback-raten for de faktiske lokale perturbasjonene er `0.0`
- derfor er `v14` ikke artefaktbegrenset av ensemblekollaps eller perturbasjonsfallback
- men frontfarten er fortsatt tydelig mode-avhengig
- operativ dom er derfor `mode_dependent_not_yet`, ikke Lorentz-likhet

Det viktigste fra `Documentation/v14_lorentz_diagnostics.md` er:

- `band_zero_del`, `local_swap` vs `add_chord`: `mean_rel_delta_fit_speed ~= 0.712`
- `band_pdel_0005`, `local_swap` vs `add_chord`: `mean_rel_delta_fit_speed ~= 0.559`
- naer-regime-gapet i mean fit-speed er lite (`~0.002` for `local_swap`, `~0.018` for `add_chord` og `token_shift`), men ikke nok til a redde universell frontfart
- derfor peker `v14` mot ekte lokalitet under rene kontroller, men ikke mot noen robust universell `c*` ennå

`v14b` testet deretter om `v14`-gapet kanskje bare var lokal placement-stoy:

- samme perturbasjonstype ble kjort fra flere lokale plasseringer pa samme basegraf og samme seed
- alle placement-rader holdt fortsatt `strict_match = 1.0`
- men within-mode placement-variasjonen er omtrent like stor som between-mode-gapen

Det viktigste fra `Documentation/v14b_lorentz_placement_diagnostics.md` er:

- `band_zero_del`: `within_rel_speed_mean ~= 0.648`, `mode_rel_speed_mean ~= 0.658`
- `band_pdel_0005`: `within_rel_speed_mean ~= 0.526`, `mode_rel_speed_mean ~= 0.510`
- begge regimer lander derfor pa `placement_noise_competes`

Den riktige live-lesningen na er:

- `v14` fjernet enkle artefaktforklaringer
- `v14b` viste at lokal anisotropi/placement-stoy fortsatt er en sterk alternativ forklaring
- Lorentz-sporet er derfor fortsatt `not_yet`, og neste steg ma vaere smalt og isotropi-orientert hvis vi fortsetter den linjen

`v14c` testet deretter om enkel lokal støttegeometri faktisk forklarer placement-variansen i ankerregimet:

- bare `band_zero_del`
- bare `local_swap`
- flere placements per base

Det viktigste fra `Documentation/v14c_local_isotropy_diagnostics.md` er:

- alle placement-rader holder fortsatt `strict_match = 1.0`
- placement-variansen er reell
- men enkle lokale støttegeometrifeaturer forklarer den nesten ikke

Konkrete signaler:

- `support_ball_3` er best av de testede feature-ene, men fortsatt svakt:
  - `spearman_vs_fit_speed ~= -0.098`
  - `spearman_vs_neg_hit_r2 ~= -0.324`
- within-base alignment er lav for alle feature-ene:
  - `align_speed_rate <= 0.083`
  - `align_hit_rate <= 0.167`

Den riktige live-lesningen na er derfor enda strammere:

- Lorentz-sporet er fortsatt `not_yet`
- placement-stoy konkurrerer fortsatt med mellom-modus-gapen
- og de enkle lokale geometrifeaturene vi testet gir ikke noen god mikroframe-forklaring ennå

`v15` skiftet derfor blikket bort fra Lorentz og over til mesoskopiske eksitasjoner i samme stabile regime:

- samme `band_zero_del`
- samme dype, size-separerte ensembler
- lokale perturbasjoner klassifisert etter levetid og morfologi

Det viktigste fra `Documentation/v15_defect_lifetime_lab.md` er:

- `add_chord` domineres sterkt av `persistent_split` (`0.938`)
- `local_swap` er ogsa oftest `persistent_split` (`0.688`), men med mer `persistent_diffuse` (`0.250`)
- `token_shift` viser fortsatt mye `persistent_split` (`0.750`), men er den eneste som også dør ut i merkbar andel (`0.188`)

Den riktige live-lesningen na er:

- vi har fortsatt ikke Lorentz-likhet
- men vi har na et klart mer interessant mesoskalasignal enn tidligere
- den mest lovende retningen er ikke bredere validering, men a folge opp `persistent_split`-familien direkte med lengre levetid eller kollisjonstester

`v15b` tok deretter akkurat den kollisjonstesten med et strammere artifact-oppsett:

- samme `band_zero_del`
- samme dype, size-separerte ensembler
- matched single-runs og pair-runs pa samme base og seed
- begge orders (`ab`, `ba`) for a avslore ordresensitivitet
- eksplisitt kontroll av at matched control-grenene holder seg samkjorte

Det viktigste fra `Documentation/v15b_add_chord_collision_lab.md` er:

- `interaction_supported = 1.000`
- `mean_pair_union_jaccard` ligger omtrent mellom `0.208` og `0.462`
- `mean_pair_order_jaccard = 1.000`
- `mean_control_edge_jaccard_ab_ba = 1.000`

Den riktige live-lesningen na er derfor:

- dette er fortsatt ikke bevis pa partikler
- men det er et klart og artefaktkontrollert kollisjonssignal i `add_chord`-familien
- pair-runene ser ikke ut som ren superposisjon av to matched single-runs
- neste naturlige steg er a klassifisere interaksjonstypen direkte: annihilation, pass-through, binding eller secondary split

`v15c` tok akkurat denne smalere klassifiseringen:

- samme `band_zero_del`
- samme dype, size-separerte ensembler
- samme matched single/pair-run-oppsett
- samme AB/BA-kontroll, men med en strammere lesning av sluttgeometrien

Det viktigste fra `Documentation/v15c_collision_type_lab.md` er:

- artifact-control er fortsatt `clean`
- `binding_like` finnes, men bare i `0.188` av run-ene
- `secondary_split_like` finnes oftere, men fortsatt bare i `0.250`
- majoriteten er fortsatt `mixed_collision` (`0.562`)

Den riktige live-lesningen na er derfor:

- kollisjonssignalet fra `v15b` holder
- men interaksjonstypen er fortsatt ikke skarpt løst
- den mest sannsynlige retningen er ikke bredere batch, men enda strammere møtesporing rundt selve kollisjonstidspunktet

`v15d` tok sa det smalere møtevinduet direkte:

- bare `48` og `96`
- tettere snapshots
- samme matched single/pair-run-oppsett
- eksplisitt sammenlikning av komponentforskjeller i det snapshotet der pair-runen avviker mest fra unionen av single-runs

Det viktigste fra `Documentation/v15d_collision_window_lab.md` er:

- artifact-control er fortsatt `clean`
- `mixed_window` dominerer fortsatt (`0.750`)
- men vi ser na minst ett klart `compress_then_split`-løp og ett klart `persistent_binding_tendency`-løp

Den riktige live-lesningen na er derfor:

- kollisjonssignalet holder fortsatt
- møtevinduet gjør bildet mer informativt enn ren sluttklassifisering
- men én dominant interaksjonstype er fortsatt ikke etablert
- neste naturlige steg er en enda smalere `48`-runde rundt de konkrete pair-familiene som ga binding- og compress-then-split-signaler

`v15e` tok så akkurat denne `48`-raffineringen:

- bare target `48`
- bare pair `2-3` og `3-4`
- mer budsjett per pair
- samme matched AB/BA-oppsett og samme tette vindusdiagnostikk

Det viktigste fra `Documentation/v15e_pair_family_refinement.md` er:

- artifact-control er fortsatt `clean`
- `2-3` heller litt mot `compress_then_split`, men ikke nok (`0.333`)
- `3-4` bekrefter ikke en ren binding-familie (`binding = 0.083`, `mixed = 0.667`)

Den riktige live-lesningen nå er derfor:

- pair-familiene er fortsatt blandet
- `2-3` er mer lovende enn `3-4` som videre oppfølgingsfamilie
- neste naturlige steg er en enda smalere `2-3`-runde med mer budsjett per family, ikke mer bredde

`v15f` tok sa denne rene `2-3`-budsjettutvidelsen:

- bare target `48`
- bare growth-seed `101`, der pair `2-3` faktisk er stabilt tilgjengelig
- mange flere run-offsets
- enda tettere snapshots gjennom møtevinduet

Det viktigste fra `Documentation/v15f_pair23_budget_extension.md` er:

- artifact-control er fortsatt `clean`
- `compress_then_split` holder seg bare svakt som beste ikke-mixed type (`0.125`)
- `mixed_window` dominerer nå tydelig (`0.750`)

Den riktige live-lesningen nå er derfor:

- mer budsjett på `2-3` gjorde ikke signalet renere
- denne mikroraffineringen ser ut til å ha avtagende verdi
- neste naturlige steg er trolig ikke enda mer av samme type budsjett, men enten lengre enkelttrajektorier eller et nytt defect-spørsmål

`v15g` tok så dette skiftet direkte:

- samme `band_zero_del`
- samme `add_chord`
- samme matched single/pair-run-oppsett
- samme smale `48`-korridor med bare pair `2-3` og `3-4`
- men genealogy, event-logg og event-kjeder som hovedprodukt i stedet for bare coarse window-klasser

Det viktigste fra `Documentation/v15g_collision_genealogy_lab.md` er:

- artifact-control er fortsatt `clean`
- begge pair-familiene finnes på den delte `101`-basen
- `order_ambiguous_count = 0` for begge pair-familiene
- genealogy-sporingen reduserer faktisk de gamle `mixed_window`-utfallene:
  - `2-3`: `compress_split_rebind = 0.333`, `merge_hold_split = 0.333`, `split_persistent_dual = 0.333`
  - `3-4`: `compress_split_rebind = 0.333`, `split_persistent_dual = 0.667`
- de gamle coarse vindusklassene er fortsatt blandede (`old_window_mixed_rate = 0.500` for begge), men genealogy-bildet er mer strukturert enn før

Den riktige live-lesningen nå er derfor:

- `v15g` reduserer usikkerheten reelt
- men pair-familiene kollapser fortsatt ikke til helt rene arter
- det mest informative neste steget er ikke mer pair-offset-søk, men lengre representative trajectories med de samme genealogy-observablene

`v15h` tok sa dette neste smale steget direkte:

- samme `band_zero_del`
- samme `add_chord`
- samme matched single/pair-run-oppsett
- bare noen fa representative traces valgt fra `v15g`
- mye lengre horisont med de samme genealogy-observablene

Det viktigste fra `Documentation/v15h_representative_collision_traces.md` er:

- artifact-control er fortsatt `clean`
- alle de valgte representative tracene matcher forventet `v15g`-chain pa prefix-horisonten
- de tidlige chain-navnene holder seg for disse tracene ogsa pa full horisont
- senfasen kollapser likevel ikke til ett felles tail-mønster
- vi ser minst to tail-typer i denne smale runden: `mixed_tail` og `rebound_merge_tail`

Den riktige live-lesningen na er derfor:

- `v15h` styrker at collision-sporet ikke bare er et coarse label-fenomen
- men det peker ogsa mot at forskjellen mellom representative forlop ligger mer i sen genealogisk morfologi enn i a lete etter enda flere pair-offsets
- neste naturlige steg er a folge trace-genealogiene enda mer direkte, ikke starte ny bred pair-scan

`v15i` tok sa dette neste smale steget direkte:

- ikke ny simulering i bredde
- bare analyse av de representative `v15h`-trace-ne
- eksplisitt fokus pa senfase-overganger
- mål: gjore `mixed_tail` og `rebound_merge_tail` mer presise

Det viktigste fra `Documentation/v15i_tail_transition_lab.md` er:

- artifact-control er fortsatt `clean`
- tail-overgangene er order-stabile
- `v15h` sine grove tail-typer brytes videre ned i tre repeterbare overgangstyper:
  - `quiet_singleton_lock`
  - `merge_rebound_lock`
  - `fragmenting_lock`
- `pair23_split_persistent_dual` ender som `quiet_singleton_lock`
- `pair23_merge_hold_split` ender som `merge_rebound_lock`
- `pair23_compress_split_rebind` og `pair34_split_persistent_dual` ender som `fragmenting_lock`

Den riktige live-lesningen na er derfor:

- defect-sporet blir mer forklarbart i senfasen enn i `v15h`
- forskjellen mellom representative traces ser ut til a ligge i repeterbare tail-overganger, ikke bare i tidlige coarse chain-navn
- neste naturlige steg er a forklare disse overgangene eksplisitt med hendelseskjeder og segmenter, ikke a starte ny pair-scan

`v15j` tok sa dette neste smale steget direkte:

- ingen nye brede simuleringer
- bare forklaring av `v15i`-tailene med eksplisitte segmentmekanismer
- mål: gjore senfasen enklere a lese enn bare overgangsnavn

Det viktigste fra `Documentation/v15j_tail_mechanism_lab.md` er:

- artifact-control er fortsatt `clean`
- mekanismelabelene er order-stabile
- de tre `v15i`-tail-overgangene kan forklares av tre enklere segmentmekanismer:
  - `quiet_relaxation_lock`
  - `balanced_rebound_cycle`
  - `fragmenting_repair_cycle`
- `pair23_split_persistent_dual` leses na som `quiet_relaxation_lock`
- `pair23_merge_hold_split` leses na som `balanced_rebound_cycle`
- `pair23_compress_split_rebind` og `pair34_split_persistent_dual` leses na som `fragmenting_repair_cycle`

Den riktige live-lesningen na er derfor:

- defect-sporet er blitt enklere a forklare uten ny bredde
- senfasen ser ut til a organiseres av noen fa repeterbare segmentmekanismer
- neste naturlige steg er a teste hvilke terskler som utloser disse mekanismene, ikke a starte ny pair-scan

`v15k` tok sa denne smale holdout-testen direkte:

- samme `band_zero_del`
- samme lange trace-oppsett
- men nye, naerliggende holdout-offsets fra de samme `v15g`-familiene
- mal: se om `v15j`-mekanismene faktisk generaliserer

Det viktigste fra `Documentation/v15k_mechanism_holdout_validation.md` er:

- artifact-control er fortsatt `clean`
- holdout-tracene reproduserer forventet prefix-chain
- men mekanismelesningen generaliserer ikke rent til holdout-tracene
- alle fire holdout-traces ender som `mixed_mechanism`
- holdout match-rate mot `v15j`-mekanismene er `0.000`

Den riktige live-lesningen na er derfor:

- `v15j` var nyttig som lokal forklaring, men ikke sterk nok som generalisert mekanismelov
- vi bor ikke overdrive terskel- eller mekanismepaastander pa dette stadiet
- neste naturlige steg er en mindre og mer forsiktig forklaringsrunde, eller et sideblikk til et annet defect-sporsmal, ikke mer generaliseringsretorikk

`v15l` tok sa akkurat denne forklaringsrunden:

- ingen ny bred simulering
- bare sammenlikning av `v15j`-mekanismelesningen mot `v15k`-holdoutene
- mal: forklare hvorfor generaliseringen brot sammen uten a late som signalet var vilkarlig

Det viktigste fra `Documentation/v15l_holdout_failure_explainer.md` er:

- holdout-bruddet kan forklares lokalt med noen fa bruddmodi, ikke bare som ustrukturert stoy
- de to tydeligste driverne er `birth_death_intrusion` og `quiet_suffix_collapse`
- dette redder ikke generaliseringspaastanden, men det gjor negative resultatet mer informativt

Den riktige live-lesningen na er derfor:

- `v15j` gir fortsatt nyttig lokal forklaring
- `v15k` viser at forklaringen ikke generaliserer rent
- `v15l` viser at dette bruddet likevel har lokal struktur
- neste naturlige steg kan derfor vaere et nytt defect-sporsmal, ikke bare mer av samme collision-generaliseringslinje

`v15m` tok sa nettopp dette sideblikket:

- behold `band_zero_del` som arbeidsregime
- bytt bort fra kollisjonssporet
- test om `token_shift` har en egen survival/extinction-dynamikk, med `add_chord` som levende kontroll

Det viktigste fra `Documentation/v15m_single_defect_survival_lab.md` er:

- artifact-control holder fortsatt rent
- `token_shift` viser noe extinction (`0.167` ved `48`, `0.083` ved `96`)
- men `token_shift` skiller seg ikke rent nok fra `add_chord` til a bære et eget sterkt survival/extinction-spor ennå
- `add_chord` holder seg levende i alle runene i denne runden

Den riktige live-lesningen na er derfor:

- dette er et ekte nytt defect-sporsmal, ikke mer kollisjonsretorikk
- `token_shift` er interessant fordi det fortsatt er den skjoreste familien
- men survival/extinction-signalet er fortsatt for svakt til sterke paastander
- neste naturlige steg bor vaere et nytt defect-sporsmal eller en mer forsiktig survival-oppfolging, ikke survival-claiming i bredde

`v15n` tok sa denne mer forsiktige survival-oppfolgingen:

- behold `band_zero_del`
- behold `token_shift` som den skjoreste familien fra `v15m`
- behold `add_chord` som levende kontroll
- test om den lille extinction-andelen i `token_shift` folger lokal stottegeometri, i stedet for a late som det allerede er en ren familie-lov

Det viktigste fra `Documentation/v15n_token_shift_fragility_lab.md` er:

- artifact-control holder fortsatt rent
- `token_shift` har fortsatt noe extinction (`0.143` ved `48`, `0.067` ved `96`)
- `add_chord` holder fortsatt `0.000` extinction i denne runden
- extinct `token_shift`-runs ligger ikke tilfeldig; de har gjennomgaende hoyere enkle stottegeometri-mal enn de levende `token_shift`-runene
- tre placements gir eksplisitt `token_shift extinct` samtidig som `add_chord` pa samme plassering holder seg levende

Den riktige live-lesningen na er derfor:

- survival-sporet er fortsatt ikke en ren stor lov
- men `token_shift`-skjorheten ser na mer lokalt strukturert ut enn i `v15m`
- det riktige neste steget er en enda smalere token_shift-fragility-runde rundt de skjoreste stotteprofilene, ikke brede survival-paastander

`v15o` tok sa nettopp denne smale replikeringsrunden:

- behold bare de tre extinct `token_shift`-profilene fra `v15n`
- match hver av dem mot en levende `token_shift`-kontroll pa samme base
- rerun begge profilene med flere seeds
- behold `add_chord` pa de samme plasseringene som levende kontrollfamilie

Det viktigste fra `Documentation/v15o_token_shift_fragility_replication.md` er:

- artifact-control holder fortsatt rent
- den sterkeste skjore profilen (`t48_g101_p3_vs_p4`) replikerer med et rent token_shift-gap: `0.250` mot `0.000`
- de to andre profilene replikerer bare svakt: `0.250` mot `0.125`
- `add_chord` holder fortsatt `0.000` extinction i alle de replikerte profilene

Den riktige live-lesningen na er derfor:

- `token_shift`-skjorheten ser delvis replikert ut som lokal profil, ikke bare som enkeltoffset-stoy
- men bare en av de tre profilene holder som tydelig skjore profil sa langt
- neste naturlige steg bor vaere en enda smalere profilrunde rundt den sterkeste kandidaten, med bedre lokalt matchede kontroller, ikke brede survival-paastander

`v15p` tok sa denne mikro-raffineringen direkte:

- bare den sterkeste kandidaten fra `v15o`: `target 48`, `growth_seed 101`, `token_shift` pa `p3`
- to bedre matchede levende kontroller pa samme base: `p1` og `p4`
- samme replikeringslogikk, men uten a late som en svak lokal profil allerede er generalisert

Det viktigste fra `Documentation/v15p_token_shift_profile_refinement.md` er:

- artifact-control holder fortsatt rent
- den antatt skjore `p3`-profilen holder ikke extinction-gap mot de bedre matchede kontrollene
- `token_shift` extinction blir `0.188` for `p3`, men `0.312` for `p1` og `0.250` for `p4`
- `add_chord` holder fortsatt `0.000` extinction over alle tre profiler

Den riktige live-lesningen na er derfor:

- `v15o` sitt delvise lokale fragility-signal var nyttig, men ikke robust nok til a overleve bedre matchende kontroller
- den mest lovende token_shift-profilen holder derfor ikke som ren lokal skjorehetsprofil
- neste naturlige steg bor vaere et annet smalt defect-sporsmal, ikke mer token_shift-fragility langs denne linjen

`v15q` tok sa dette nye defect-sporsmalet:

- legg bort token_shift-fragility som hovedspor
- behold samme `band_zero_del`
- test om single defects viser senfase-retur til tidligere morfologier, i stedet for bare a drive videre
- mal baade eksakt retur og grovere morfologisk retur

Det viktigste fra `Documentation/v15q_single_defect_recurrence_lab.md` er:

- artifact-control holder fortsatt rent
- alle tre perturbasjonstyper viser sterk morfologisk retur i denne smale runden
- `add_chord` og `local_swap` er renest: `0.875` morphology_return ved `48`, og `0.875-1.000` ved `96`
- `token_shift` viser ogsa retur, men blandet med `extinct_after_return` ved `48`
- eksakt syklisk retur er mye svakere enn grov morfologisk retur, sa dette skal ikke leses som ren periodisitet

Den riktige live-lesningen na er derfor:

- recurrence/return-sporet er sterkere enn den siste token_shift-fragility-linjen
- det vi ser er grov morfologisk retur, ikke en robust eksakt sykluslov
- neste naturlige steg bor vaere en enda smalere retur-/recurrence-runde for `add_chord`, ikke brede defect-paastander

`v15r` tok sa akkurat denne smale `add_chord`-oppfolgingen:

- behold bare representative `add_chord`-profiler fra `v15q`
- forleng horisonten kraftig i stedet for a aapne flere profiler
- skil eksplisitt mellom prefix-retur og full-horisont-retur
- bruk dette til a avgjore om cycle-signalet faktisk overlever

Det viktigste fra `Documentation/v15r_add_chord_long_horizon_recurrence.md` er:

- artifact-control holder fortsatt rent
- minst en `add_chord`-profil holder ekte `cyclic_return` ogsa pa lang horisont
- en sekundar syklisk kandidat mykner til `morphology_return`
- to morfologiske kontrollprofiler tipper faktisk over til `cyclic_return` pa full horisont
- dette betyr at lang-horisont-retur ikke bare er grov hale-stabilitet; det finnes en smal, ekte cycle-familie

Den riktige live-lesningen na er derfor:

- `add_chord`-recurrence er na det reneste aktive defect-sporet i repoet
- signalet er fortsatt smalt og lokalt, ikke en generell lov for alle defects
- neste naturlige steg bor vaere a kartlegge cycle-familien rundt den overlevende `add_chord`-profilen, ikke a gjenapne brede sweeps

`v15s` tok sa nettopp denne family-mapen rundt den overlevende profilen:

- behold bare samme base som i den sterkeste `v15r`-profilen: `target 48`, `growth_seed 202`
- behold bare de fire lokale `add_chord`-plasseringene `0-3`
- bruk samme lange horisont som i `v15r`
- avgjor om `p2` er et enkelt lokalt unntak eller del av et lite cycle-band

Det viktigste fra `Documentation/v15s_add_chord_cycle_family_map.md` er:

- artifact-control holder fortsatt rent
- alle fire lokale profiler tipper til eller holder `cyclic_return` pa full horisont
- `p2` holder fortsatt som ekte `sustained_cyclic_return`
- `p0`, `p1` og `p3` tipper fra `morphology_return` til `cyclic_return` pa full horisont
- den sterkeste lokale profilen er faktisk `p1`, ikke `p2`

Den riktige live-lesningen na er derfor:

- `add_chord`-cycle-signalet er ikke bare ett enkelt punkt; det ser ut som et lite lokalt cycle-band pa samme base
- dette er fortsatt en smal lokal familie, ikke en generell cycle-lov for `add_chord`
- neste naturlige steg bor vaere en enda smalere kartlegging inne i dette lokale cycle-bandet, mest naturlig rundt `p1` og `p2`

`v15t` tok sa denne smale holdout-testen inne i bandet:

- behold bare samme base: `target 48`, `growth_seed 202`
- behold bare `p1` og `p2` som de mest informative lokale profilene
- bruk noen fa nye dynamikk-seeds i stedet for a apne flere plasseringer
- avgjor om `p1` faktisk er et sterkere lokalt sentrum enn `p2`

Det viktigste fra `Documentation/v15t_add_chord_cycle_center_holdout.md` er:

- artifact-control holder fortsatt rent
- `p1` holder `cyclic_return` i alle holdout-kjoringene
- `p2` holder seg sterk, men glipper en gang til `morphology_return`
- `p1` har hoyere mean full exact return (`0.897`) enn `p2` (`0.744`)
- head-to-head pa samme seed_delta ender `p1_wins=4`, `p2_wins=2`

Den riktige live-lesningen na er derfor:

- det lokale cycle-bandet er ekte, men ikke flatt
- sentrum ser ut til a vaere forskjovet mot `p1`
- dette er fortsatt en lokal mikrofamilie pa en enkelt base, ikke en generell `add_chord`-lov
- neste naturlige steg bor vaere en enda smalere mikrotest rundt `p1` som lokalt cycle-sentrum

`v15u` tok sa denne mikrotesten mot begge flanker:

- behold bare samme base: `target 48`, `growth_seed 202`
- behold bare `p0`, `p1` og `p2`
- bruk et helt nytt lite holdout-sett av seeds
- avgjor om `p1` faktisk ligger over begge umiddelbare flanker samtidig

Det viktigste fra `Documentation/v15u_add_chord_p1_microcenter.md` er:

- artifact-control holder fortsatt rent
- alle tre plasseringene holder `cyclic_return` i alle holdout-kjoringene
- `p1` slar fortsatt `p2` tydeligere enn for `v15t`
- men `p0` holder faktisk svaakt hoyere mean full exact return (`0.859`) enn `p1` (`0.846`)
- `p1` vs `p0` ender bare `3-2-1` i seed-dueller, sa sentrum er ikke rent losnet

Den riktige live-lesningen na er derfor:

- det lokale `add_chord`-bandet holder fortsatt som ekte mikrofamilie
- men `p1` kan ikke enda kalles et sikkert lokalt sentrum over begge flanker
- repoet star na pa `microcenter_still_mixed`, ikke pa en hard sentrumskonklusjon
- neste naturlige steg bor vaere en liten mekanistisk forklaringsrunde inne i `p0-p1-p2`-triplet, ikke bredere scanning

`v15v` tok sa nettopp denne mekanistiske forklaringsrunden:

- behold bare samme `p0-p1-p2`-triplet
- behold samme holdout-seeds som i `v15u`
- legg ikke til nye profiler
- mal i stedet hvor tidlig og hvor stabilt hver profil lases inn i senfase exact-return

Det viktigste fra `Documentation/v15v_add_chord_triplet_mechanism_lab.md` er:

- artifact-control holder fortsatt rent
- `p0` domineres av `intermittent_cycle_lock`
- `p1` domineres ogsa av `intermittent_cycle_lock`, med bare litt mer `early_stable_lock`
- `p2` er den eneste profilen som far noe tydelig `coarse_cycle_shell`
- `p1` kommer litt tidligere til første exact return enn flankene, men switcher ogsa mer enn `p0`
- mekanismelesningen gjor triplet-en mer forklarbar, men ikke ren nok til a lose sentrumssporsmalet

Den riktige live-lesningen na er derfor:

- usikkerheten sitter na mest i forskjellen mellom `p0` og `p1`, ikke i hele bandet
- `p2` ser tydeligst svakere ut mekanistisk enn de to andre
- repoet star fortsatt pa `stay_micro`, men med et skarpere neste sporsmal: forklar `p0` vs `p1`

`v15w` tok sa denne smale `p0`-vs-`p1`-stottekontrasten:

- behold samme base og samme smale holdout-dueller
- apne ingen nye dynamikk-kjoringer
- sammenlign i stedet lokal stottegeometri for `p0` og `p1`
- test om den geometriske kontrasten faktisk matcher speed-vs-stability-mønsteret i duellene

Det viktigste fra `Documentation/v15w_add_chord_p0_p1_support_contrast.md` er:

- artifact-control holder fortsatt rent
- `p1` sitter i litt tettere lokal støtte enn `p0` (`degree_gap=0.667`, `ball1_gap=2.0`)
- `p0` har samtidig litt større relativ videre ekspansjon (`expansion_gap=-0.106` sett fra `p1-p0`)
- duel-bildet er ikke rent: to `p1_clean_advantage`, én `p1_calm_advantage`, én `p0_clean_advantage`, én `speed_stability_tradeoff`, én `mixed_duel`
- støttekontrasten gjør forskjellen mer konkret, men ikke enkel nok til én hard forklaring

Den riktige live-lesningen na er derfor:

- `p1` ser litt tettere og litt mer "lokal" ut geometrisk
- `p0` holder fortsatt noen dueller roligere eller sterkere enn denne enkle geometrien alene skulle tilsi
- repoet star fortsatt pa `stay_local`, men med et enda skarpere neste sporsmal: sammenlign den unike noden `5` i `p0` mot den unike noden `10` i `p1`, eller forklar aller første tail-segment direkte

`v15x` tok sa denne første-tail-segment-runden:

- behold bare `p0` og `p1`
- behold samme base og samme smale holdout-seeds
- rerun dynamikken, men mal bare det første tail-segmentet fram til exact-return lock
- avgjor om forskjellen kan forklares som tidligere konsolidering, roligere tail-lock eller en tydelig tradeoff

Det viktigste fra `Documentation/v15x_add_chord_p0_p1_first_tail_segment.md` er:

- artifact-control holder fortsatt rent
- alle seks seed-duellene ender fortsatt som `mixed_first_segment`
- mean onset-bilde er svakt og blandet: `p1` kommer bare litt tidligere (`first_gap=-6.7`), men har litt hoyere pre-lock komponenttall og flere post-lock switcher
- ingen av de smale onset-labelene (`p1_earlier_consolidation`, `speed_stability_tradeoff`, `p0_calmer_tail`) blir dominante

Den riktige live-lesningen na er derfor:

- onset alene rydder ikke opp i `p0` vs `p1`
- repoet star fortsatt pa `stay_tiny`, ikke fordi signalet er borte, men fordi selv første tail-segment fortsatt er genuint blandet
- neste naturlige steg bor vaere en enda mindre forklaringsrunde pa én eller to konkrete seed-caser, ikke nye aggregate-runder

`v15y` tok sa denne rene case-duel-runden:

- behold bare de tre mest informative seedene fra `p0` vs `p1`
- `151` som sterk `p1`-case
- `239` som mulig tradeoff-case
- `271` som sterk `p0`-case
- avgjor om disse faktisk holder som tre ulike lokale case-typer

Det viktigste fra `Documentation/v15y_p0_p1_case_duel_lab.md` er:

- artifact-control holder fortsatt rent
- de tre seed-casene kollapser ikke tilbake til én blandet type
- `151` holder som `p1_clean_case`
- `239` holder som `tradeoff_case`
- `271` holder som `p0_clean_case`
- diagnosen ender pa `three_case_family_supported`

Den riktige live-lesningen na er derfor:

- den lokale `p0`-vs-`p1`-usikkerheten er ikke bare stoy; den deler seg i minst tre repeterbare case-typer
- det riktige neste sporsmalet er ikke flere aggregate-runder, men hva som faktisk utloser hvert case
- neste naturlige steg bor vaere en liten trigger-forklaringsrunde for `151`, `239` og `271`, ikke bredere scanning

`v15z` tok sa den smaleste forklaringsrunden pa toppen av dette:

- ingen nye simuleringer
- bruk bare `v15w`-stottekontrasten og `v15y`-case-duel-dataene
- avgjor om `151`, `239` og `271` faktisk kan forklares av et lite sett onset-triggere

Det viktigste fra `Documentation/v15z_case_trigger_explainer.md` er:

- artifact-control holder fortsatt rent
- `p1` har fortsatt en svak statisk stottefordel, men den realiseres ikke likt i alle seeds
- `151` holder som `p1_compact_radius_trigger`
- `239` holder som `fragmented_fast_tradeoff_trigger`
- `271` holder som `p0_calm_singleton_trigger`
- diagnosen ender pa `three_local_triggers_supported`

Den riktige live-lesningen na er derfor:

- de tre lokale case-typene fra `v15y` kan forklares mer presist enn før
- `p1`-fordelen ser ut til a kreve kompakt onset, ikke bare tettere statisk stotte
- tradeoff- og `p0`-casene ser ut til a oppsta nar `p1` starter mer fragmentert
- neste naturlige steg bor vaere en liten holdout-test av disse triggerne pa noen fa naerliggende seeds, ikke en bred ny scan

`v15aa` tok sa den lille holdout-testen av akkurat disse triggerne:

- behold samme base, samme `p0`/`p1`-duell og samme `band_zero_del`
- test bare to naerliggende holdout-seeds rundt hvert av de tre ankercasene
- avgjor om `v15z`-triggerne baerer lokalt utover `151`, `239` og `271`

Det viktigste fra `Documentation/v15aa_case_trigger_holdout.md` er:

- artifact-control holder fortsatt rent
- ingen av de tre triggerfamiliene matcher i de naerliggende holdouts
- alle seks holdout-radene ender som `mixed_trigger`
- familieaggregatet blir derfor:
  - `151`-familien: `not_supported`
  - `239`-familien: `not_supported`
  - `271`-familien: `not_supported`
- diagnosen ender pa `trigger_holdout_not_yet`

Den riktige live-lesningen na er derfor:

- `v15z` forklarer de tre ankercasene bedre, men triggerhistorien holder ikke som lokal lov i naerliggende seeds
- dette er et nyttig negativt resultat: det stanser videre trigger-generalisering tidlig
- neste naturlige steg bor vaere en ny observabel eller et annet defect-sporsmal, ikke mer arbeid pa samme triggerlinje

`v15ab` tok sa neste naturlige observabel inne i det sterkeste lokale `add_chord`-bandet:

- behold samme `t48_g202`-mikroband med `p0`, `p1` og `p2`
- behold samme smale holdout-seeds som i `v15u`
- bytt sporsmal fra "hvem vinner?" til "har retur-signalet en skarp lag/periodestruktur?"

Det viktigste fra `Documentation/v15ab_add_chord_cycle_lag_lab.md` er:

- artifact-control holder fortsatt rent
- alle tre plasseringene holder fortsatt `cyclic_rate = 1.0`
- men ingen av dem har `stable_single_lag_cycle` eller `few_lag_cycle_family`
- alle tre ender som `diffuse_cycle_family`
- diagnosen ender pa `cycle_band_is_diffuse`

Den riktige live-lesningen na er derfor:

- det lokale `add_chord`-cycle-bandet er reelt som recurrence-signal
- men signalet ser ikke ut til a komme fra en skarp lokal periode
- hoy exact-return-rate ser i stedet ut til a komme fra bred multi-lag-retur
- neste naturlige steg bor derfor vaere en annen observabel enn periodisitet

`v15ac` tok sa den neste observabelen som passer direkte etter dette:

- behold samme `t48_g202`-mikroband med `p0`, `p1` og `p2`
- behold de samme smale holdout-seedene som i `v15u` og `v15ab`
- bytt sporsmal fra periode til kjerne/rand-struktur

Det viktigste fra `Documentation/v15ac_add_chord_core_shell_lab.md` er:

- artifact-control holder fortsatt rent
- alle tre plasseringene holder fortsatt `cyclic_rate = 1.0`
- alle tre viser hoy `core_share_of_union` (`~0.855` til `~0.892`)
- alle tre har `support_core_frac = 1.0`
- ingen av dem er diffuse i denne observabelen
- diagnosen ender pa `cycle_band_is_core_shell`

Den riktige live-lesningen na er derfor:

- recurrence-bandet ser ut til a vaere drevet av en stabil skadekjerne med variabel rand
- periodisitet var feil observabel for a forklare signalet
- neste naturlige steg bor vaere a male randdynamikken direkte

`v15ad` tok sa nettopp denne rand-observabelen:

- behold samme lokale add_chord-band
- behold samme smale seeds
- avgjor om den variable randen skifter rolig eller i bursts

Det viktigste fra `Documentation/v15ad_add_chord_boundary_shell_lab.md` er:

- artifact-control holder fortsatt rent
- `p0` holder `calm_shell_rate = 1.0`
- `p1` og `p2` holder `calm_shell_rate = 0.667`
- ingen av plasseringene blir `bursty_shell_cycle`
- mean shell refresh holder seg lav (`~0.080` til `~0.091`)
- diagnosen ender pa `core_shell_variation_is_calm`

Den riktige live-lesningen na er derfor:

- det lokale add_chord-signalet ser ikke bare ut som kjerne + rand, men som kjerne + rolig flimrende rand
- dette er et sterkere mesoskalasignal enn periodehistorien og triggerhistorien ga
- neste naturlige steg bor vaere randtopologi eller rand-hendelser, ikke mer arbeid pa perioder eller trigger-generalisering

`v15ae` tok sa nettopp dette shell-topologi-steget:

- behold samme lokale `t48_g202`-band med `p0`, `p1` og `p2`
- behold de samme smale holdout-seedene som i `v15ab-v15ad`
- bytt sporsmal fra "rolig eller bursty rand?" til "er randen vanligvis sammenhengende, fragmentert eller lokalt loope-preget?"

Det viktigste fra `Documentation/v15ae_add_chord_shell_topology_lab.md` er:

- artifact-control holder fortsatt rent
- alle tre plasseringene holder fortsatt `cyclic_rate = 1.0`
- `p0` og `p1` blir `fragmented_shell_band` i alle seks runene
- `p2` blir `fragmented_shell_band` i fem av seks og `mixed_shell_topology` i ett
- mean shell component count ligger hoyt (`~3.35`, `~3.55`, `~4.18`)
- mean shell connected rate holder seg lav (`~0.090`, `~0.108`, `~0.177`)
- mean shell loop rate er `0.0` for alle tre
- diagnosen ender pa `cycle_band_has_fragmented_shell_zone`

Den riktige live-lesningen na er derfor:

- recurrence-bandet er fortsatt ekte, men randen ser topologisk fragmentert ut heller enn som ett sammenhengende band
- den rolige randflimringen fra `v15ad` er ikke det samme som topologisk ro; shellen skifter fortsatt mellom flere separate biter
- lokal cycle-rank i shellen forklarer ikke signalet her
- neste naturlige steg bor vaere a lokalisere nar i halen fragmenteringene oppstar, ikke a scanne bredere

`v15af` tok sa nettopp denne timing-runden pa `v15ae`-snapshottene:

- behold samme lokale `t48_g202`-band med `p0`, `p1`, `p2`
- bruk bare de ekte `v15ae`-snapshottene, ikke nye simuleringer
- lokaliser nar shell-fragmenteringen starter og om den holder som tidlig lock eller bare som sen churn

Det viktigste fra `Documentation/v15af_add_chord_shell_fragment_event_lab.md` er:

- artifact-control holder fortsatt rent
- `p0` har `early_fragment_lock_rate = 0.833`
- `p1` har `early_fragment_lock_rate = 0.500`, `delayed_fragment_lock_rate = 0.167` og `intermittent_fragment_churn_rate = 0.167`
- `p2` har `early_fragment_lock_rate = 0.667`, `intermittent_fragment_churn_rate = 0.167` og `connected_resistance_churn_rate = 0.167`
- mean first fragment step ligger tett pa tail-start for `p0` og `p2` (`~1537.3`) og litt senere for `p1` (`~1549.3`)
- mean fragmented suffix rate er fortsatt hoy (`~0.912`, `~0.904`, `~0.823`)
- diagnosen ender pa `fragmentation_is_usually_early_lock`

Den riktige live-lesningen na er derfor:

- shell-fragmenteringen ser oftest ut til a starte tidlig i halevinduet og deretter holde seg som en lokal lock
- `p1` har et lite minoritetsspor av forsinket onset
- `p2` har et lite minoritetsspor der connected shell holder igjen lenger for den fragmenterer
- neste naturlige steg bor forklare disse minoritetsavvikene, ikke bredere scanning

`v15ag` tok sa akkurat denne unntaksforklaringen:

- behold bare minoritetsavvikene fra `v15af`
- kjør ingen nye simuleringer
- avgjor om unntakene kollapser til et lite sett lokale mekanismer eller fortsatt er blandet stoy

Det viktigste fra `Documentation/v15ag_shell_exception_explainer.md` er:

- artifact-control holder fortsatt rent
- de seks minoritetsrunene kollapser til fire lokale mekanismelabels
- `alternating_to_late_lock` dekker tre av seks unntak
- `two_stage_fragment_lock` forklarer `p1` sitt delayed-onset-case
- `singleton_resistance_case` forklarer `p2` sitt connected-resistance-case
- `near_lock_boundary_case` dekker det gjenværende grensetilfellet i `p1`
- diagnosen ender pa `minority_exceptions_are_locally_explainable`

Den riktige live-lesningen na er derfor:

- minoritetsavvikene i shell-fragmenteringen ser ikke lenger ut som ren blandet stoy
- de kollapser til et lite lokalt mekanismesett, med en klar hovedfamilie (`alternating_to_late_lock`) og tre smalere unntaksmekanismer
- neste naturlige steg bor vaere en liten holdout-test av akkurat disse unntaksmekanismene, ikke en ny bred scan

`v15ah` tok sa nettopp denne holdout-testen av unntaksmekanismene:

- behold samme lokale `t48_g202`-band
- behold bare de seks unntaksankrene fra `v15ag`
- legg inn to naerliggende holdout-seeds rundt hvert unntaksanker
- avgjor om unntaksmekanismene replikerer, eller om de fleste holdouts faller tilbake til `early_fragment_lock`

Det viktigste fra `Documentation/v15ah_shell_exception_holdout.md` er:

- artifact-control holder fortsatt rent
- `expected_match_rate = 0.0` for alle seks unntaksankrene
- fire av seks ankre har `main_family_revert_rate = 1.0`
- de to gjenværende ankerfamiliene splitter mellom `early_fragment_lock` og `unresolved_holdout`
- ingen holdout går over i en annen kjent unntaksmekanisme
- diagnosen ender pa `exceptions_mostly_revert_to_main_family`

Den riktige live-lesningen na er derfor:

- dette ga faktisk ny viten: unntaksmekanismene fra `v15ag` ser ikke ut til a generalisere lokalt
- de ser best ut som lokale avvik rundt en sterk og robust hovedfamilie `early_fragment_lock`
- repoet bor derfor ikke bruke mer tid pa bredere unntaks-ekspansjon langs denne aksen
- hvis vi fortsetter herfra, bor neste steg være en ny observabel inne i hovedfamilien, ikke mer jakt pa unntaksarter

`v15ai` tok sa nettopp dette observabelskiftet inne i hovedfamilien:

- behold samme lokale `t48_g202` add_chord-band
- behold bare run som faktisk ligger i `early_fragment_lock`
- bruk ankerrun fra `v15ae-v15af` og holdout-run fra `v15ah` som falt tilbake til hovedfamilien
- bytt fra eksakt shell-komponenttelling til coarse fragment-load-band: `low = 1..3`, `mid = 4..6`, `high = 7+`

Det viktigste fra `Documentation/v15ai_early_lock_band_lab.md` er:

- artifact-control holder fortsatt rent
- `structured_band_rate = 1.0` for ankerrun og `0.9` for holdout-revert-run
- kombinert `structured_band_rate = 0.955`
- kombinert `band_lock_rate = 0.727`, med bare `band_drift_rate = 0.045`
- `mean_dominant_band_share = 0.687`, mens `mean_dominant_exact_share = 0.365`
- uplift fra coarse band over eksakt telling er derfor stor: `0.322`
- ankerrun domineres mest av `mid`, mens holdout-revert-run domineres mest av `low`
- diagnosen ender pa `early_lock_has_structured_band_ladder`

Den riktige live-lesningen na er derfor:

- dette ga ny viten inne i hovedfamilien, ikke bare en ny beskrivelse
- `early_fragment_lock` ser mye bedre ut som en strukturert low/mid/high band-stige med litt naboband-drift enn som ett eksakt shell-komponenttall
- dette er fortsatt ikke rene defect-arter eller en lov; det er en mer robust mesoskopisk observabel
- neste riktige steg er a forklare band-onset og band-skifter, ikke a ga tilbake til unntaksjakt eller eksakt periodestory

`v15aj` tok sa nettopp dette onset-steget:

- behold de ekte `v15ai`-snapshottene
- bruk ingen nye simuleringer
- finn tidligste suffix der et run holder seg innenfor ett band eller et naboband-par
- avgjor om run gaar rett inn i `low-mid`, senere glir inn i `mid-high`, eller blir igjen i tre-band-churn

Det viktigste fra `Documentation/v15aj_early_lock_band_onset_lab.md` er:

- artifact-control holder fortsatt rent
- kombinert `structured_onset_rate = 0.818`
- kombinert `immediate_structured_rate = 0.591`
- kombinert `delayed_structured_rate = 0.227`
- kombinert `persistent_three_band_churn_rate = 0.182`
- `p0` gaar nesten alltid rett inn i `low-mid`: `immediate_low_mid_ladder_rate = 0.857`
- `p2` er tyngst pa senere `mid-high`-settling og churn: `delayed_mid_high_ladder_rate = 0.375`, `persistent_three_band_churn_rate = 0.250`
- diagnosen ender pa `band_onset_structure_supported`

Den riktige live-lesningen na er derfor:

- dette ga ny viten utover `v15ai`: onseten er selv strukturert, ikke bare sluttfordelingen
- `early_fragment_lock` er ikke flatt i halen; placement `0` gaar oftest direkte inn i `low-mid`, mens placement `2` oftere trenger tid for a komme inn i `mid-high` eller blir igjen i bredere churn
- den neste riktige retningen er derfor ikke ny bred scan, men a forklare inngangstriggerne til disse onset-typene

`v15ak` tok sa nettopp denne trigger-runden:

- behold de ekte `v15ai`-snapshottene og `v15aj`-onsettypene
- bruk ingen nye simuleringer
- maal bare enkle tidlige hale-features i de forste 24 snapshottene
- avgjor om disse skiller immediate `low-mid`, `mid-high`-entry og vedvarende churn

Det viktigste fra `Documentation/v15ak_band_entry_trigger_lab.md` er:

- artifact-control holder fortsatt rent
- immediate low-family har `compact_low_entry_rate = 0.917`
- mid-high-entry-family har `boundary_mixed_rate + heavy_high_pressure_rate = 1.000`
- persistent churn-family har `boundary_mixed_rate = 1.000`
- diagnosen ender pa `entry_trigger_map_partly_supported`

Den riktige live-lesningen na er derfor:

- dette ga ny viten: tidlig hale skiller immediate `low-mid` ganske rent fra resten
- immediate `low-mid` ser nesten alltid ut som kompakte low-entry-caser med lav last og rolig switching
- `mid-high`-entry og vedvarende churn ligger derimot fortsatt i samme boundary/heavy-sone tidlig i halen
- neste riktige steg er derfor a splitte denne boundary-sonen, ikke a lete etter nye brede familier

`v15al` tok sa nettopp dette boundary-steget:

- behold bare `boundary_mixed_trigger`-runene fra `v15ak`
- bruk ingen nye simuleringer
- se litt lenger frem i den tidlige halen, de forste 72 snapshottene
- avgjor om boundary-sonen deler seg i noen fa senere profiler

Det viktigste fra `Documentation/v15al_boundary_zone_split_lab.md` er:

- artifact-control holder fortsatt rent
- boundary-sonen er ikke ren, men deler seg i tre lokale profiler:
  - `late_high_rise_boundary`
  - `mid_plateau_boundary`
  - `residual_boundary`
- `mid_high_entry_family` har `late_high_rise_rate = 0.500`
- `persistent_churn_family` har `mid_plateau_rate = 0.750`
- diagnosen ender pa `boundary_zone_partly_split`

Den riktige live-lesningen na er derfor:

- dette ga litt ny viten: boundary-sonen er ikke homogen
- `mid-high`-entry havner oftere i en sen high-rise-gren
- vedvarende churn havner oftere i en roligere mid-plateau-gren
- men overlap-caseene er fortsatt viktige, sa dette er fortsatt en delvis og ikke endelig splitting
- neste riktige steg er derfor a forklare overlap-caseene, ikke a ga bredere med en gang

`v15am` tok sa nettopp denne overlap-forklaringsrunden:

- behold bare de tre overlap-caseene fra `v15al`
- behold de typiske referanselopene for late high-rise og mid-platå
- bruk ingen nye simuleringer
- sammenlign overlap-runene direkte mot familieprofilene i samme 72-snapshot-vindu

Det viktigste fra `Documentation/v15am_boundary_overlap_explainer.md` er:

- artifact-control holder fortsatt rent
- `5002161` blir godt forklart som `churn_to_high_rise_crossover`
- `5002240` blir godt forklart som `suppressed_high_rise_plateau`
- `5002220` blir bare delvis forklart som `residual_tilt_to_mid_plateau`
- diagnosen ender derfor pa `overlap_cases_still_partly_mixed`

Den riktige live-lesningen na er derfor:

- dette ga ny viten, men i smal form
- to av tre overlap-case er na lokalt mer forklarbare enn i `v15al`
- residual-caset er fortsatt ikke rent forklart, bare tydeligere lokaliseret
- neste riktige steg er derfor ikke mer pressing av samme overlap-forklaring, men en ny observabel inne i overlap-sonen

`v15an` tok sa nettopp denne high-hold-runden:

- behold samme fokuserte run-sett fra `v15am`
- behold de ekte `v15ai`-snapshottene
- bruk ingen nye simuleringer
- maal ikke bare om high-band dukker opp, men om det faktisk holder, glipper eller bare blinker til helt pa slutten

Det viktigste fra `Documentation/v15an_boundary_high_hold_lab.md` er:

- artifact-control holder fortsatt rent
- `5002161` blir skarpt lest som `delayed_high_hold_crossover`
- `5002240` blir skarpt lest som `no_high_hold_plateau`
- `5002220` blir skarpt lest som `late_terminal_high_probe`
- diagnosen ender pa `high_hold_observable_sharpens_overlap_zone`

Den riktige live-lesningen na er derfor:

- dette ga ekte ny viten utover `v15am`
- overlap-sonen blir bedre forklart av om high-band faktisk holder enn av bare mer generelle familieavstander
- residual-caset er ikke lenger bare "delvis mid-platå"; det ser ut som en sen terminal high-probe, ikke et ekte high-hold-lop
- neste riktige steg er derfor a teste grensen mellom ekte sen high-hold og bare terminal high-probe

`v15ao` tok sa nettopp dette grense-steget:

- behold det fokuserte `v15an`-settet
- legg til ett naerliggende delayed-probe-kontrollop
- bruk ingen nye simuleringer
- avgjor om high-grensen faktisk deler seg i noen fa lesbare haleutfall

Det viktigste fra `Documentation/v15ao_terminal_probe_boundary_lab.md` er:

- artifact-control holder fortsatt rent
- `5002161` blir `established_high_hold`
- `5002220` blir `terminal_high_probe`
- `5002221` blir `failed_early_high_probe`
- `5002240` og mid-platåreferansene blir `no_high_hold_plateau`
- diagnosen ender pa `terminal_probe_boundary_is_structured`

Den riktige live-lesningen na er derfor:

- dette ga ekte ny viten utover `v15an`
- high-grensen ser ikke lenger ut som bare en diffus residualsone
- den deler seg i minst fire lesbare haleutfall: ekte high-hold, terminal probe, mislykket tidlig probe og ingen high-hold
- neste riktige steg er derfor a forklare hva som bestemmer om sen high kommer tidlig nok til a bli hold i stedet for bare terminal probe

`v15ap` tok sa nettopp dette launch-steget:

- behold det fokuserte `v15ao`-settet
- bruk ingen nye simuleringer
- maal bare det lille pre-high-vinduet rett for high enten holder, feiler eller uteblir
- avgjor om de fire haleutfallene allerede kan leses der

Det viktigste fra `Documentation/v15ap_pre_high_launch_lab.md` er:

- artifact-control holder fortsatt rent
- `established_high_hold` leses som `mixed_threshold_launch`
- `terminal_high_probe` leses som `compact_terminal_launch`
- `failed_early_high_probe` leses som `premature_probe_launch`
- `no_high_hold_plateau` leses som `no_launch_plateau`
- diagnosen ender pa `pre_high_launch_map_supported`

Den riktige live-lesningen na er derfor:

- dette ga ekte ny viten utover `v15ao`
- forskjellen mellom hold, terminal probe og failed probe ser ut til a vaere synlig allerede i launch-vinduet rett for high-forsoket
- high-grensen er derfor ikke bare en haleeffekt; den har et lite pre-high launch-kart
- neste riktige steg er en liten holdout-test av dette launch-kartet, ikke en bredere scan

`v15aq` tok sa nettopp dette impulse-steget:

- behold det fokuserte `v15ap`-settet
- bruk ingen nye simuleringer
- maal bare det aller forste post-launch-vinduet etter at high begynner eller nesten begynner
- avgjor om forskjellen mellom hold og probe blir enda skarpere der

Det viktigste fra `Documentation/v15aq_high_launch_impulse_lab.md` er:

- artifact-control holder fortsatt rent
- `5002161` og `5002205` blir `sustained_hold_impulse`
- `5002241` blir `rebounding_hold_impulse`
- `5002220` blir `compact_late_spike`
- `5002221` blir bare `soft_failed_impulse`
- diagnosen ender pa `launch_impulse_map_still_mixed`

Den riktige live-lesningen na er derfor:

- dette ga noe ny struktur, men mindre ny viten enn `v15ap`
- det forste impulse-vinduet skiller hold fra sen spike ganske godt
- men failed-probe-sporet blir fortsatt ikke rent nok lest i samme observabel
- neste riktige steg er derfor ikke mer press pa impulse-vinduet alene, men en annen liten observabel eller en liten holdout rundt launch-kartet

`v15ar` tok sa nettopp dette horizon-steget:

- behold det fokuserte `v15ap`-settet
- bruk ingen nye simuleringer
- les high-grensen gjennom hvor lenge high faktisk holder seg etter start
- avgjor om hold, terminal probe og failed probe blir skarpere lest som horisont-forlop

Det viktigste fra `Documentation/v15ar_high_retention_horizon_lab.md` er:

- artifact-control holder fortsatt rent
- `5002161`, `5002205` og `5002241` blir `established_hold_horizon`
- `5002220` blir `terminal_probe_horizon`
- `5002221` blir `failed_probe_horizon`
- `5002240`, `5002272`, `5002273` og `5002307` blir `no_high_presence`
- diagnosen ender pa `horizon_map_supported`

Den riktige live-lesningen na er derfor:

- dette ga ekte ny viten utover `v15aq`
- high-grensen blir na bedre lest som et lite horisont-kart enn som bare launch-impuls
- failed-probe-sporet er skarpere her enn i `v15aq`
- neste riktige steg er en liten holdout-test av horisont-kartet, ikke en bredere scan

`v15as` tok sa nettopp denne holdout-runden:

- behold bare fire representative horisontankre
- bruk samme lokale `t48_g202` add_chord-oppsett
- rerun bare to naerliggende seeds rundt hvert anker
- avgjor om horisont-kartet faktisk har lokal baereevne utover anker-runene

Det viktigste fra `Documentation/v15as_horizon_map_holdout.md` er:

- artifact-control holder fortsatt rent
- `no_high_presence` holder rent lokalt med `match_rate = 1.000`
- `established_hold_horizon` holder ikke rent; ett holdout blir `mixed_horizon` og ett faller til `no_high_presence`
- `terminal_probe_horizon` faller helt til `no_high_presence`
- `failed_probe_horizon` faller ogsa helt til `no_high_presence`
- diagnosen ender pa `horizon_map_holdout_mixed`

Den riktige live-lesningen na er derfor:

- `v15ar` sitt horisont-kart ga ekte ankerkunnskap
- men `v15as` viser at bare `no_high_presence` ser lokalt robust ut sa langt
- de andre horizon-familiene ligger pa en skjotere grense og kollapser ofte ned til fravaer av high i naerliggende seeds
- neste riktige steg er derfor en enda smalere observabel rundt failed-probe og terminal-probe-grensen, ikke mer bred horisont-ekspansjon

`v15at` tok sa nettopp dette burst-steget:

- behold samme fire anker-run og aatte holdout-run
- rerun dem med samme lokale `t48_g202` add_chord-oppsett
- les grensen gjennom et lite burst-kart i stedet for bare horisont-etiketter
- avgjor om holdout-kollapsen ser best ut som manglende high-burst, fading burst eller ekte probe

Det viktigste fra `Documentation/v15at_high_burst_window_lab.md` er:

- artifact-control holder fortsatt rent
- anker-runene deler seg rent i `sustained_hold_burst`, `terminal_compact_burst`, `early_failed_burst` og `no_high_burst`
- holdout-runene er `0.875` `no_high_burst`
- bare ett holdout-run, `5002233`, holder et lite restspor som `fading_late_burst`
- diagnosen ender pa `burst_map_sharpens_holdout_collapse`

Den riktige live-lesningen na er derfor:

- burst-observabelen er bedre enn horisont alene for a beskrive hva holdoutene faktisk gjor
- den skjore high-grensen ser mest ut som en no-high-kollaps med ett lite fading-restspor, ikke som flere nesten-like horizon-familier
- neste riktige steg er derfor a forklare akkurat `fading_late_burst`, ikke a presse holdout-kartet bredere

`v15au` tok sa nettopp denne post-peak-forklaringsrunden:

- behold bare triplet-en `anchor_hold`, `fading_holdout` og `no_high_holdout`
- bruk ingen bredere scan
- maal bare hva som skjer etter peak-bursten
- avgjor om fading-sporet faktisk er et eget post-peak-forlop

Det viktigste fra `Documentation/v15au_post_peak_fade_explainer.md` er:

- artifact-control holder fortsatt rent
- `anchor_hold` blir `post_peak_hold`
- `fading_holdout` blir `post_peak_fade`
- `no_high_holdout` blir `no_launch_tail`
- diagnosen ender pa `post_peak_map_supported`

Den riktige live-lesningen na er derfor:

- dette ga ekte ny viten utover `v15at`
- det lille restsporet er ikke bare "mindre hold"; det er et eget post-peak-fade-forlop
- boundary-familien er na best lest som: rent hold, rent no-high, og et lite mellomforlop der en ekte peak bygges men glipper etterpa
- neste riktige steg er en minimal holdout rundt `post_peak_fade`, ikke en ny bred scan

`v15av` tok sa nettopp denne minimal-holdouten:

- behold bare placement `2`
- behold bare overgangen rundt seed `231`
- rerun to nye nedre naboer, `215` og `223`
- bruk `239` og `247` bare som ovre kontekst

Det viktigste fra `Documentation/v15av_post_peak_fade_holdout.md` er:

- artifact-control holder fortsatt rent
- `231` holder som `post_peak_fade`
- begge nye nedre nabopunkter, `215` og `223`, blir `no_launch_tail`
- `239` holder som `post_peak_hold`
- `247` holder som `no_launch_tail`
- diagnosen ender pa `fade_singleton_not_supported`

Den riktige live-lesningen na er derfor:

- `post_peak_fade` er ekte nok som lokalt forlop
- men det ser ikke ut til a holde som et lite naboband rundt `231`
- det er best lest som et singleton-aktig overgangspunkt mellom stabilt hold og rent no-launch
- neste riktige steg bor derfor ikke vaere bredere fade-scan, men et nytt defect-sporsmal eller en annen observabel

De viktigste signalene i `Documentation/v12_geometry_invariant_lab.md` er:

- `initial_avg_degree` er den mest stabile normaliserte startstorrelsen.
- `initial_spectral_per_sqrtN` og `initial_dim_proxy` er ogsa relativt stabile.
- `abs_delta_nodes_rel = 0` og `abs_delta_beta1_rel = 0` i denne runden, men dette skal behandles som mulig regime-/koblingsartefakt til det er bedre forklart.
- Den mest interessante reduserte basisen sa langt er `initial_spectral_per_sqrtN + initial_clustering`, som gir best positiv skill for `final_radius_control`.
- `v12b` viser at transfer-signalet er moderat positivt for `final_radius_control` mot naerliggende regimer, men ikke robust for `avg_local_overlap`.
- I off-anchor transfer i `v12b` er `spectral_only` faktisk svaakt sterkere enn `spectral_plus_clustering`, sa den lille 2-feature-basisen ma behandles som lovende, men ikke endelig bekreftet.
- `v12c` tester flere naerliggende triadpunkter og sammenligner sma surrogate-baser direkte for radius.
- I `v12c` er `spectral_plus_dim` den sterkeste off-anchor radius-basen, men `spectral_only` ligger nesten likt bak.
- Alle basisene blir svakt negative ved `bridge_0015_0000`, sa radius-transferen ser lokal ut heller enn global.
- `v12d` flytter testen utenfor ren triad-akse og viser at `spectral_plus_dim` og `spectral_only` fortsatt ligger naermest hverandre som de beste enkle basisene.
- `full_basis` er fortsatt en nyttig sanity check, men taper pa samlet off-anchor-robusthet mot `spectral_plus_dim`.
- Den operative lesningen etter `v12d` er derfor et lite arbeidsplateau av `spectral_plus_dim` og `spectral_only`, ikke en hard enkeltrangering.
- `v12e` tar neste nytte-steg og tester billig sortering av starttilstander.
- I `v12e` er `full_basis` best pa within-target screening, men `spectral_plus_dim` er fortsatt den beste kompakte basisen.
- Den operative lesningen etter `v12e` er derfor: bruk `full_basis` som benchmark for screening og `spectral_plus_dim` som den beste lille arbeidsbasisen.
- `v12f` gjor neste steg mer konkret: en budsjettstyrt screeningpolicy der bare topp-fraksjonen innen hver størrelse far dyre oppfolgingskjoringer.
- I `v12f` holder `full_basis` seg som budsjettbenchmark, men `spectral_only` slar `spectral_plus_dim` som beste lille policy i selve budsjettoppgaven.
- Samtidig er dette et smalt signal: `spectral_only` ligger bare hairline foran `random_baseline` pa curve-wide AUC, sa hovedverdien ser ut til a ligge ved medium budsjett heller enn som en sterk universell screeningregel.
- Den operative lesningen etter `v12f` er derfor: behold `full_basis` som benchmark, test `spectral_only` som kompakt policy i neste pipeline-runde, og ikke overselg gevinsten ennå.
- `v12g` gjor denne pipeline-runden eksplisitt ved a sammenligne konkrete policypar mot referansen `full_basis@0.50`.
- I `v12g` er `spectral_only@0.50` den naermeste kompakte erstatningen, men den gir ingen ekstra sparing mot benchmarken fordi den bruker samme oppfolgingsbudsjett.
- `spectral_only@0.333` sparer mer, men taper for mye pa hit og recall. `spectral_only@0.667` matcher lettere, men koster mer.
- Den operative lesningen etter `v12g` er derfor: vi har en enkel same-budget-substitutt, men ennå ikke en klart billigere kompakt policy med omtrent samme kvalitet.
- `v12h` legger et eksplisitt kostnadsregnskap oppa denne lesningen.
- Hvis screeningkostnaden er liten eller ukjent, holder `full_basis@0.50` seg som riktig standardbenchmark.
- `spectral_only@0.50` er fortsatt den enkleste same-budget-kandidaten.
- Naar screeningkostnaden blir tydelig ikke-neglisjerbar i arbeidsmodellen, blir `spectral_plus_dim@0.667` den mest interessante kostnadsnoytrale utfordreren.
- Den operative lesningen etter `v12h` er derfor betinget: ikke én universell kompakt vinner, men ulike arbeidskandidater avhengig av hvor dyr vi antar screeningfasen er.
- `v12i` erstatter denne abstrakte kostknappen med malt lokal veggklokketid for den faktiske kodebanen.
- I `v12i` er oppfolgingstiden sa dominerende ved dagens størrelser at screeningdelen blir praktisk neglisjerbar i totalen.
- `full_basis@0.50` holder seg derfor som operativ benchmark i maelt workflow-tid.
- `spectral_only@0.50` er fortsatt den riktige same-budget-kandidaten, men gevinsten er i praksis nesten null i total tid fordi oppfolgingsdynamikken dominerer.
- `spectral_plus_dim@0.667` beholder hoy kvalitet, men blir tydelig tregere i maelt workflow fordi den sender flere baser videre til dyre oppfolginger.
- Den operative lesningen etter `v12i` er derfor skarpere enn i `v12h`: kompakte basisrom er fortsatt interessante som struktur og forklaring, men ved dagens grafstørrelser gir de ennå ikke en tydelig praktisk tidsgevinst.
- `v12j` flytter den samme maelte workflow-testen til litt større størrelser: `96, 192, 320, 384`.
- Size-separasjonen holder fortsatt rent i `v12j`, sa dette ser ikke ut som en ny generatorartefakt.
- Screeningandelen er fortsatt praktisk neglisjerbar i total workflow (`~5e-6` for referansen), sa oppfolgingen er fortsatt den operative flaskehalsen.
- `spectral_only@0.50` holder ikke som sterk same-budget-kandidat i denne større runden; den taper pa quality metrics mot `full_basis@0.50`.
- `spectral_plus_dim@0.667` er kvalitetsmessig sterkere enn referansen i denne runden, men den er tydelig dyrere i total workflow og blir derfor ikke en ny arbeidsvinner.
- `random_baseline@0.50` matcher faktisk referansen pa mean best-hit og recall i denne lille større-runden, noe som er en klar advarsel om at screening-signalet ikke automatisk styrker seg med litt større grafer.
- Den operative lesningen etter `v12j` er derfor: kompakte basisrom er fortsatt interessante som struktur, men de gir fortsatt ikke en robust maelt arbeidsgevinst, og `spectral_only` svekkes snarere enn styrkes i denne moderate størrelsesstresstesten.
- `v12k` flytter derfor fokuset inn i selve oppfolgingsbudsjettet.
- Ingen adaptive follow-up-policyer er naer-match mot `full_followup` i denne runden.
- `probe1_only` er den raske yttergrensen (`time_frac ~= 0.159`), men den faller for mye i kvalitet.
- `probe2_top_half` er den mest balanserte adaptive kandidaten (`time_frac ~= 0.677`, `best_hit ~= 0.750`, `recall ~= 0.750`), men heller ikke den er sterk nok til a erstatte full oppfolging.
- Den operative lesningen etter `v12k` er derfor: hvis vi skal hente ekte arbeidsgevinst videre, bor neste steg vaere hybrid eller dypere adaptiv oppfolging heller enn enda mer ren pre-screening.
- `v12l` gjor denne hybridtesten eksplisitt ved a kombinere screening og adaptiv oppfolging i samme workflow.
- Referansen i `v12l` er `full_basis__full_followup`.
- `spectral_only__full_followup` er den naermeste same-budget-utfordreren pa middelverdier: den er litt raskere og litt bedre pa mean hit/recall enn referansen, men splitvis `near_match ~= 0.650` er ikke hoy nok til a kalle den en ny standard.
- `full_basis__probe2_top_half` er den tydeligste reelle tidsutfordreren: `speedup ~= 1.494`, men `best_hit ~= 0.575` og `recall ~= 0.575` betyr at kvalitetstapet fortsatt er for stort.
- `spectral_only__probe2_top_half` er den rene kompakt+adaptive hybriden, men den taper enda mer kvalitet enn `full_basis__probe2_top_half`.
- Den operative lesningen etter `v12l` er derfor: hybridsporet er mer lovende gjennom dypere adaptiv oppfolging enn gjennom enda mer finjustering av screeningbasiser.
- `v12m` holder screening fast ved `full_basis@0.50` og tester bare dypere adaptive follow-up-policyer.
- `probe3_top_half` er den viktigste nye kandidaten: den matcher referansen `full_followup` pa mean `best_hit` og `recall`, men bruker bare halvparten av de screenede basene til full forlengelse og blir derfor tydelig raskere (`speedup ~= 1.358`).
- Pairwise er fortsatt litt svakere for `probe3_top_half` enn for `full_followup`, sa dette er den forste sterke adaptive utfordreren, men ikke en endelig ny standard ennå.
- `probe2_top_two_thirds` og `probe3_top_two_thirds` kollapser metodisk til `full_followup` i denne settingen, fordi `0.667` av to screenede baser per størrelse betyr at begge blir forlenget. Det er nyttig som kontroll, men ikke som ny arbeidsregel.
- Den operative lesningen etter `v12m` er derfor: neste riktige steg er en smal valideringsrunde rundt `probe3_top_half` mot `full_followup`, eventuelt med en smartere tie-break- eller forlengelsesregel.
- `v12n` gjor akkurat denne smale valideringen.
- `probe3_top_half` holder seg som en rask utfordrer (`speedup ~= 1.356`), men den faller tilbake til `best_hit ~= 0.650`, `recall ~= 0.650` og `pairwise ~= 0.590` mot referansen `full_followup`.
- `probe3_top_half_screen_tiebreak` forbedrer ikke bildet i det hele tatt.
- `probe3_guarded_half` bruker mer tid, men forbedrer heller ikke kvaliteten.
- Den operative lesningen etter `v12n` er derfor mer nøktern enn etter `v12m`: `probe3_top_half` er fortsatt interessant som rask utfordrer, men ikke robust nok til å erstatte `full_followup`.
- Hvis prosjektet skal videre herfra på arbeidsflytsporet, bør neste steg være en smartere tidlig beslutningsstatistikk eller et større valideringssett, ikke flere nesten-like lokale varianter.
- `v13` tar et bevisst steg tilbake fra workflow-sporet og spør om geometri-/invariantsignalene faktisk er sterke nok til å forsvare et større valideringssett.
- I `v13` er `initial_avg_degree` den klart mest stabile normaliserte startfeature, mens `initial_spectral_per_sqrtN` er den tydeligste ikke-trivielle stabile geometriaksen.
- `mean_abs_delta_nodes_rel` og `mean_abs_delta_beta1_rel` er fortsatt eksakt null, men `v13` leser dem eksplisitt som mulige regime-/koblingsartefakter heller enn ny dyp matematikk.
- Den mest interessante ikke-trivielle quasi-invariant-kandidaten i `v13` er `mean_abs_delta_spectral_radius_rel`, med stabil lav drift og `top3_prob = 1.000`.
- Radius-signalet overlever i `v13`, men svakere enn ønsket: `spectral_only` er best liten basis for `mean_final_radius_control`, men `q10_skill < 0` og status blir derfor `not_yet`.
- Overlap-signalet er enda svakere i `v13`; ingen liten basis er sterk nok til å forsvare større validering der.
- Den operative lesningen etter `v13` er derfor: bruk stabile startfeatures som kontroller, behold `spectral_only` og `spectral_plus_clustering` som liten radius-duo, men ikke bruk større valideringssett som førsteprioritet for radius før signalet er sterkere.
- `v13b` tar neste naturlige steg og tester quasi-invariant-sporet på tvers av små triad-, delete- og death-avvik.
- `v13b` viser at de eksakte null-driftene ikke holder gjennom hele den lokale regimefamilien. `mean_abs_delta_nodes_rel` bryter under delete-avvik, og `mean_abs_delta_beta1_rel` bryter enda tydeligere. De skal derfor leses som regime-/koblingsartefakter, ikke som nye bevaringslover.
- Samtidig holder `mean_abs_delta_spectral_radius_rel` seg lav og top-3 i alle testede regimer, inkludert off-anchor delete- og death-punkter.
- Den operative lesningen etter `v13b` er derfor skarpere enn etter `v13`: større valideringssett er fortsatt ikke førsteprioritet for radius-basis eller overlap, men det er nå naturlig for målrettet spektral quasi-invariant-testing.
- `v13c` skalerer opp akkurat dette spektralsporet med litt bredere lokal familie og større budsjett.
- `v13c` bekrefter at spektraldriften fortsatt er det sterkeste ikke-trivielle sporet, men den er ikke sterk nok til å stå alene som neste store valideringsmål.
- `dim_proxy` holder seg nær nok i flere regimer til at spektralsporet må leses som lovende, men fortsatt lokalt og delvis uavklart.
- Den operative lesningen etter `v13c` er derfor mer nøktern enn etter `v13b`: vent med større valideringssett til spektralsporet er skarpere eller bredere testet.
- `v13d` tar neste naturlige steg som en ren knife-edge-runde: ikke bredere familie, bare mer lokalt diskrimineringsbudsjett på de vanskeligste regimepunktene.
- `v13d` bekrefter igjen at spektraldriften er den beste ikke-trivielle kandidaten, og i denne lokale runden er `band_pdel_0005` sterkest med `p_spectral_lt_dim ~= 0.813`.
- Samtidig er triadpunktene fortsatt bare `good_but_local`, ikke sterke nok til å gjøre hele spektralsporet skarpt.
- Den operative lesningen etter `v13d` er derfor enda klarere enn etter `v13c`: spektralsporet er fortsatt interessant, men fortsatt `mixed`, og større valideringssett er fortsatt `not_yet`.
- `v13e` flytter hele trykket over på triad-korridoren og legger inn mellompunktene `bridge_000625_0000` og `bridge_000875_0000`.
- `v13e` viser at triad-korridoren ikke er jevnt blandet: `bridge_000625_0000` og `bridge_000875_0000` blir `sharp_local`, `bridge_0010_0000` er `good_but_local`, mens `bridge_00075_0000` fortsatt er `mixed`.
- Den operative lesningen etter `v13e` er derfor mer informativ enn etter `v13d`: spektralsporet er fortsatt `mixed`, men blandingen er nå lokalisert til et smalere triadpunkt istedenfor hele korridoren.
- `v13f` gaar ett hakk smalere og legger inn fine nabopunkt rundt `bridge_00075_0000`.
- `v13f` viser at det tidligere blandede punktet ikke ser ut til a vaere et ekte lokalt hakk: `bridge_00075_0000` blir `sharp_local`, `bridge_0006875_0000` og `bridge_0008125_0000` blir `good_but_local`, og notch-diagnosen ender pa `notch_not_supported`.
- Den operative lesningen etter `v13f` er derfor skarpere enn etter `v13e`: den smale triad-korridoren ser renere ut lokalt, selv om `beta1` fortsatt bryter off-anchor og derfor ikke skal leses som lov.
- `v13g` tar neste naturlige steg og gir den rensede triad-korridoren et større, men fortsatt lokalt budsjett.
- `v13g` demper optimismen fra `v13f`: `bridge_0006875_0000` og `bridge_00075_0000` holder som `good_but_local`, men `bridge_0008125_0000` og `bridge_000875_0000` faller tilbake til `mixed`.
- Den operative lesningen etter `v13g` er derfor nøktern igjen: spektralsporet er fortsatt best, men selv den rensede triad-korridoren er ikke ren nok til å kalles målrettet validert, og bredere validering er fortsatt `not_yet`.
- `v13h` gaar enda smalere og tester bare oversiden av triad-korridoren.
- `v13h` viser at oversiden ikke degraderes monotont: `bridge_00084375_0000` blir `sharp_local`, mens `bridge_00078125_0000` og `bridge_0008125_0000` fortsatt er `mixed`, og `bridge_000875_0000` holder `good_but_local`.
- Overgangsdiagnosen i `v13h` blir derfor `upper_recovery_exists`, ikke ren overside-degradering.
- Den operative lesningen etter `v13h` er fortsatt `mixed`: det finnes et lokalt gjenopprettet oversidepunkt, men ikke et rent nok oversidespor til bredere validering.
- `v13i` gaar enda smalere og tester bare om det gjenopprettede punktet `bridge_00084375_0000` holder under finere bracketing.
- `v13i` viser at recovery-punktet ikke holder: `bridge_0008125_0000` og `bridge_000828125_0000` blir `sharp_local`, mens `bridge_00084375_0000` selv bare er `good_but_local`, og recovery-diagnosen ender pa `recovery_not_supported`.
- Den operative lesningen etter `v13i` er derfor skarpere igjen: oversiden har struktur, men ikke den forventede toppen. Spektralsporet er fortsatt `mixed`, og bredere validering er fortsatt `not_yet`.
- `v13j` tar neste naturlige steg og tester bare det smale bandet mellom `bridge_0008125_0000` og `bridge_000828125_0000`, med kontrollpunkter rett over.
- `v13j` viser at dette bandet faktisk holder som den reneste lokale oversidesonen: `bridge_0008125_0000`, `bridge_0008203125_0000` og `bridge_000828125_0000` er alle `sharp_local`, mens kontrollpunktene `bridge_0008359375_0000` og `bridge_00084375_0000` bare er `good_but_local`.
- Banddiagnosen i `v13j` blir `clean_band_supported`, `spectral_quasi_invariant` blir `good_but_local`, og `larger_validation_set` flytter fra `not_yet` til `yes_targeted`.
- Den operative lesningen etter `v13j` er derfor den skarpeste hittil i dette sporet: spektraldriften er fortsatt ikke bredt validert, men et lite målrettet valideringssett rundt upper-bandet er nå metodisk rimelig.
- `v13k` tar akkurat dette målrettede valideringssteget, men med litt større lokalt budsjett og uten å åpne nye akser.
- `v13k` demper optimismen fra `v13j`: bare `bridge_0008203125_0000` holder som `sharp_local`, mens `bridge_0008125_0000`, `bridge_000828125_0000`, `bridge_0008359375_0000` og `bridge_00084375_0000` alle blir `good_but_local`.
- Banddiagnosen i `v13k` ender derfor på `sampling_ambiguous`, `spectral_quasi_invariant` faller tilbake til `mixed`, og `larger_validation_set` går tilbake til `not_yet`.
- Den operative lesningen etter `v13k` er derfor mer nøktern enn etter `v13j`: upper-bandet er fortsatt lovende, men fortsatt ikke rent nok til å være målrettet validert.
- `v13l` går enda smalere og tester bare om `bridge_0008203125_0000` er et ekte lokalt pivotpunkt når vi bracketter det finere på begge sider.
- `v13l` viser at sentrumspunktet fortsatt er sterkt, men ikke rent nok til å stå alene: `bridge_00081640625_0000`, `bridge_0008203125_0000` og `bridge_000828125_0000` er `sharp_local`, mens `bridge_00082421875_0000` faller til `mixed`.
- Pivotdiagnosen i `v13l` ender derfor fortsatt på `sampling_ambiguous`, `spectral_quasi_invariant` blir værende `mixed`, og `larger_validation_set` forblir `not_yet`.
- Den operative lesningen etter `v13l` er derfor: upper-området er fortsatt lovende, men ser mer asymmetrisk enn rent ut. Det peker mot et neste steg som tester den øvre bruddkanten, ikke bredere validering.
- `v13m` tar akkurat dette neste steget og tester den øvre bruddkanten rundt `bridge_00082421875_0000`.
- `v13m` viser at bruddkanten fortsatt ikke er rent løst, men nå er mønsteret skarpere: `bridge_0008203125_0000`, `bridge_000826171875_0000` og `bridge_000828125_0000` er `sharp_local`, mens både `bridge_000822265625_0000` og `bridge_00082421875_0000` er `mixed`.
- Breakdiagnosen i `v13m` ender fortsatt på `sampling_ambiguous`, `spectral_quasi_invariant` blir værende `mixed`, og `larger_validation_set` forblir `not_yet`.
- Den operative lesningen etter `v13m` er derfor enda mer presis enn etter `v13l`: usikkerheten ser nå ut som en liten lokal drop-sone rundt `0.000822`–`0.000824`, ikke bare ett enkelt svakt punkt.
- `v13n` tar neste naturlige steg og skiller den nedre drop-kanten fra resten av drop-sonen ved å legge inn to finere naboer rundt `bridge_000822265625_0000`.
- `v13n` viser at den nedre kanten heller ikke holder rent som egen knekk: `bridge_0008203125_0000` er fortsatt `sharp_local`, `bridge_0008212890625_0000` er `good_but_local`, mens `bridge_000822265625_0000`, `bridge_0008232421875_0000` og `bridge_00082421875_0000` alle er `mixed`.
- Breakdiagnosen i `v13n` ender fortsatt på `sampling_ambiguous`, men med negativ margin- og delta-forverring mot de nærmeste naboene. Det peker mer mot et smalt lokalt plateau enn mot en ren nedre bruddkant.
- Den operative lesningen etter `v13n` er derfor: spektralsporet er fortsatt reelt, men fortsatt bare `mixed`, og større valideringssett er fortsatt `not_yet`.

## Generatorstatus

Den eldre generator-/storrelseskrisen ser ut til a vaere ryddet bort i den aktive kjeden.

I `Documentation/v11e_band_vs_bridge0075_target_summary.csv` er realiserte startstorrelser rent separert:

- 48 -> 48
- 96 -> 96
- 192 -> 192
- 256 -> 256

Derfor ser baade den naavaerende frontier-lesningen og strukturlesningen i `v12`-`v12h` mer dynamiske enn generator-drevne ut.

## Hva som ikke lenger bor brukes som live sannhet

Disse er fortsatt viktige historisk, men ikke siste frontier:

- `v10f`: siste sikre baseline for band-korridoren
- `v11_mid_focus`: mellomsteg der bridge-korridoren tok over
- `v11b`: legitim mellomkonklusjon om `bridge_0015_0000` vs `band_zero_del`, men overstyrt av `v11c`
- `v11c`: viktig overgangsstate der `bridge_0010_0000` vant lokalt, men overstyrt av senere `v11e`
- `v11d`: ekte men midlertidig lokal splitt mellom `band_zero_del` og `bridge_00075_0000`, overstyrt av dypere `v11e`

## Hvis noen skal sette seg inn raskt

Les i denne rekkefolgen:

1. `PROJECT_CONTEXT_LIVE.md`
2. `PROJECT_HISTORY_INDEX.md`
3. `Documentation/v11e_band_vs_bridge0075.md`
4. `Documentation/v11e_band_vs_bridge0075_candidate_summary.csv`
5. `Documentation/v11e_band_vs_bridge0075_pairwise.csv`
6. `Documentation/v11e_band_vs_bridge0075_target_summary.csv`
7. `Documentation/v0_11e_operativ_anbefaling.md`
8. `Documentation/v12_geometry_invariant_lab.md`
9. `Documentation/v12_geometry_feature_stability.csv`
10. `Documentation/v12_geometry_relative_drift_ranking.csv`
11. `Documentation/v12_geometry_reduced_basis_summary.csv`
12. `Documentation/v12b_transfer_surrogate_lab.md`
13. `Documentation/v12b_transfer_basis_summary.csv`
14. `Documentation/v0_12b_operativ_anbefaling.md`
15. `Documentation/v12c_radius_transfer_refinement.md`
16. `Documentation/v12c_radius_basis_ranking.csv`
17. `Documentation/v0_12c_operativ_anbefaling.md`
18. `Documentation/v12d_cross_axis_radius_transfer.md`
19. `Documentation/v12d_cross_axis_basis_ranking.csv`
20. `Documentation/v0_12d_operativ_anbefaling.md`
21. `Documentation/v12e_start_state_screening.md`
22. `Documentation/v12e_screening_summary.csv`
23. `Documentation/v0_12e_operativ_anbefaling.md`
24. `Documentation/v12f_budget_screening.md`
25. `Documentation/v12f_budget_summary.csv`
26. `Documentation/v0_12f_operativ_anbefaling.md`
27. `Documentation/v12g_followup_budget_pipeline.md`
28. `Documentation/v12g_followup_pipeline_summary.csv`
29. `Documentation/v0_12g_operativ_anbefaling.md`
30. `Documentation/v12h_cost_aware_pipeline.md`
31. `Documentation/v12h_cost_aware_pipeline_summary.csv`
32. `Documentation/v0_12h_operativ_anbefaling.md`
33. `Documentation/v12i_measured_runtime_pipeline.md`
34. `Documentation/v12i_measured_runtime_pipeline_followup_timing_summary.csv`
35. `Documentation/v12i_measured_runtime_pipeline_summary.csv`
36. `Documentation/v0_12i_operativ_anbefaling.md`
37. `Documentation/v12j_size_stress_runtime_pipeline.md`
38. `Documentation/v12j_size_stress_runtime_pipeline_target_summary.csv`
39. `Documentation/v12j_size_stress_runtime_pipeline_summary.csv`
40. `Documentation/v0_12j_operativ_anbefaling.md`
41. `Documentation/v12k_adaptive_followup_budget.md`
42. `Documentation/v12k_adaptive_followup_budget_summary.csv`
43. `Documentation/v0_12k_operativ_anbefaling.md`
44. `Documentation/v12l_hybrid_screening_followup.md`
45. `Documentation/v12l_hybrid_screening_followup_summary.csv`
46. `Documentation/v0_12l_operativ_anbefaling.md`
47. `Documentation/v12m_deeper_adaptive_followup.md`
48. `Documentation/v12m_deeper_adaptive_followup_summary.csv`
49. `Documentation/v0_12m_operativ_anbefaling.md`
50. `Documentation/v12n_binary_adaptive_validation.md`
51. `Documentation/v12n_binary_adaptive_validation_summary.csv`
52. `Documentation/v0_12n_operativ_anbefaling.md`
53. `Documentation/v13_geometry_signal_validation.md`
54. `Documentation/v13_geometry_signal_stability_summary.csv`
55. `Documentation/v13_quasi_invariant_bootstrap_summary.csv`
56. `Documentation/v13_geometry_signal_validation_summary.csv`
57. `Documentation/v0_13_operativ_anbefaling.md`
58. `Documentation/v13b_cross_regime_quasiinvariant_test.md`
59. `Documentation/v13b_cross_regime_drift_summary.csv`
60. `Documentation/v13b_cross_regime_anchor_delta_summary.csv`
61. `Documentation/v0_13b_operativ_anbefaling.md`
62. `Documentation/v13c_spectral_quasiinvariant_validation.md`
63. `Documentation/v13c_spectral_validation_focus_summary.csv`
64. `Documentation/v13c_spectral_validation_anchor_delta_summary.csv`
65. `Documentation/v0_13c_operativ_anbefaling.md`
