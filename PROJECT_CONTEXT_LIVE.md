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

Per dagens lokale state er `v11e` den siste frontier-avklaringen. `v12`, `v12b`, `v12c`, `v12d`, `v12e`, `v12f`, `v12g`, `v12h`, `v12i`, `v12j`, `v12k`, `v12l`, `v12m`, `v12n`, `v13`, `v13b`, `v13c`, `v13d`, `v13e`, `v13f`, `v13g`, `v13h`, `v13i`, `v13j`, `v13k`, `v13l`, `v13m`, `v13n`, `v14`, `v14b`, `v14c`, `v15`, `v15b`, `v15c`, `v15d`, `v15e`, `v15f`, `v15g`, `v15h` og `v15i` er de aktive struktur-/transfer-/Lorentz-/defect-rundene bygget pa den.

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
