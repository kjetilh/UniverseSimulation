# WP-A report: beta1-bookforingsaudit

Status: **Fullfort lokalt — avventer integratorens commit**

Fingeravtrykk: `beta1-bookkeeping-fidelity-measurement`

## Rammer og kildegrunnlag

- `Documentation/Program/WP-A_beta1_audit.md` er lest i sin helhet.
- `Documentation/Status_Og_Retninger_2026-08-23.md`, del 5, er lest.
- Grunnsannheten i denne auditen er faktisk sykkelrang `E - N + C` beregnet
  fra en NetworkX-graf konstruert fra den malte tilstanden for og etter hvert
  kall. Konstruktorens `delta_core` brukes bare som bokfort verdi.
- `relational_universe_local_max_coupling_lab.py` skal ikke endres.
- Integratoren har eksplisitt reservert all Git-mutering (stage/commit/push).
  Commit-hash fylles derfor av integratoren etter separat gjennomgang.

## Konfigurasjonsgrunnlag

De eksplisitt etterspurte, faktiske v15-konfigurasjonene er verifisert i
`relational_universe_v15cz_*`, `v15da_*`, `v15dk_*` og `v15dr_*`: alle bruker
deep-ensemble, `fast_balanced` og target 1024. Growth-seed/placements og de
faktiske seed-delta-multiplikasjonene er henholdsvis v15cz: seed 202, p1, 24;
v15da: seed 202, p0/p1/p2, 12 hver; v15dk: seed 404, p0/p1/p2, 8 hver; v15dr:
seeds 808/909/1001/1103, p0/p1/p2, 4 hver. En forste komplett maling av denne
132-kallsplanen gjentatt fire ganger ga 528 kall per konstruktor og 0 fallback,
0 no-op og 0 avvik for begge. For a unnga at terskelen nas ved ren duplisering,
er sampling-rammen deretter utvidet programmatisk til alle v15-moduler med
komplett deklarert target/growth-seed/placement og minst en av de to relevante
perturbasjonsfamiliene. Endelig rapport skal bare inneholde utvidet maling.

## Forelopig usikkerhet

Importinventaret skal bestemmes statisk fra Python-AST som direkte import av
`relational_universe_local_max_coupling_lab` og transitiv rekkevidde gjennom
lokale importkanter. Det er et modulavhengighetsinventar, ikke bevis pa at hver
modul faktisk kaller begge konstruktorer pa alle kontrollflytstier.

## Inkrementell fremdrift

- `Tools/beta1_bookkeeping_audit.py` er opprettet. Det importerer begge
  produksjonskonstruktorene, instrumenterer det importerte
  `choose_center_token` rundt hvert kall, og beregner uavhengig grunnsannhet via
  NetworkX for/etter. Det bygger starttilstandene med v15-programmets egne
  `deep_ensembles`, `build_bases` og `fast_balanced`.
- En preflight av faktisk v15-starttilstand for target 1024/growth-seed 202
  fullforte: 1024 noder, 1166 kanter og 22 tokens. Dette er kun en
  miljo-/byggekontroll; de rapporterte auditverdiene kommer fra full kjoring.
- Forste fullkjoring av den smale, eksplisitt navngitte rammen fullforte med
  1056 rader. Den brukes ikke som endelig evidens fordi fire identiske
  planrepetisjoner var nodvendige for 500-terskelen. Utvidet kildeoppdagelse
  finner 791 deklarerte startkonfigurasjoner over target 48, 96, 192, 384, 768,
  896 og 1024, nok til minst 500 ikke-repeterte kall per konstruktor.
- Forste forsok pa utvidet kjoring ble avbrutt manuelt da basebyggeren viste seg
  a bygge hele target x growth-seed-kryssproduktet (112 baser) i stedet for de
  24 kombinasjonene som finnes i kildeplanen. Ingen delresultater fra dette
  forsoket brukes. Byggeren er snevret inn til eksakt observerte par for nytt
  forsok. Dette var en ytelsesfeil, ikke et malingsavvik.

## 1. Filer opprettet

- `Tools/beta1_bookkeeping_audit.py`: 707 linjer. Sampling-ramme ved linje 114,
  NetworkX-grunnsannhet ved linje 205, per-kall-audit ved linje 257,
  importinventar ved linje 375 og hovedlop ved linje 662.
- `Documentation/beta1_bookkeeping_audit.md`: 975 linjer. Hovedresultat ved
  linje 5, startkonfigurasjoner ved linje 26, storrelsesfordeling ved linje 100,
  konfigurasjonsfordeling ved linje 119, importinventar ved linje 780,
  kildehasher ved linje 911 og kravgrenser ved linje 967.
- `Documentation/beta1_bookkeeping_audit.csv`: 1583 linjer, hvorav 1 header og
  1582 ra per-kall-rader.
- `Documentation/Program/WP-A_report.md`: denne inkrementelle arbeidsrapporten.
- `.program_logs/WP-A.heartbeat`: lopende hjerteslag; filen er ignorert av Git.

## 2. Malte tall

| konstruktor | kall | fallback | fallback-frekvens | add_edge no-op | no-op-frekvens | avvik | avviksfrekvens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `local_swap` | 791 | 0 | 0.000000 % | 0 | 0.000000 % | 0 | 0.000000 % |
| `add_chord` | 791 | 0 | 0.000000 % | 0 | 0.000000 % | 0 | 0.000000 % |

Forhandsdefinert nullutfall gjelder: bokforingen er renvasket for denne eksakte,
kildedeklarerte v15-sampling-rammen. Dette er ikke en pastand om alle mulige
grafer. Fordelingen dekker realiserte storrelser 48, 96, 192, 384, 768, 896 og
1024; detaljtall star i hovedrapporten. En syntetisk trekant-positivkontroll
utloste begge kjente avviksmekanismer korrekt: `local_swap` bokfort 0/faktisk
-1 og `add_chord` bokfort +1/faktisk 0, med fallback=no-op=avvik=1 i begge.

## 3. Berorte v15-script og importinventar

Malingsavvik berorte **0 script** i sampling-rammen. Statisk AST-rekkevidde
viser samtidig **118 v15-script** som avhenger av konstruktormodulen: 30 direkte
og 88 bare transitivt. Dette er et konservativt modulavhengighetsinventar, ikke
bevis pa at alle kontrollflytstier kaller begge konstruktorer.

Direkte (30):

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

Bare transitivt (88):

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

## 4. Commit-hash

Ikke opprettet i denne deloppgaven. Rotintegratoren reserverte eksplisitt all
Git-mutering og skal gjennomga disse fire sporbare leveransene, opprette den
separate `WP-A: measure beta1 bookkeeping fidelity ...`-commiten og fylle inn
hashen i sin integrasjonsrapport. Ingen stage, commit, pull eller push er gjort
her.

## 5. Verifikasjon, blokkeringer og usikkerhet

Full kommando:

```sh
PYTHONPATH=.codex_pydeps python3 Tools/beta1_bookkeeping_audit.py
```

Kjort to ganger med identisk aggregat: 791 kall per konstruktor, 0 fallback,
0 no-op og 0 avvik; importinventar 30 direkte + 88 transitivt = 118. Statisk
kompilering med `PYTHONPATH=.codex_pydeps python3 -m py_compile
Tools/beta1_bookkeeping_audit.py` besto.

En separat CSV-/formelverifikasjon bekreftet 1582 rader, 791 per konstruktor,
alle `beta1_before/after = E - N + C`, target-settet
`[48, 96, 192, 384, 768, 896, 1024]`, 43 kildeprogrammer og alle observerte
fallback/no-op/avvik lik null. Samme kommando kjorte trekant-positivkontrollen
beskrevet over uten feil. Ra-CSV SHA-256 er
`34d40b7dddd1bc2e6c88931669a9533d6098a7d38a2674b9112728c6fc94d6e9`.
Audited constructor source SHA-256 er
`695ed59ca168336334d5745076ee8924596447ee6db237963468abde526f0e1c`;
`git diff -- relational_universe_local_max_coupling_lab.py` var tom.

Ingen stoppregel ble utlost og ingenting er blokkert i selve malingen. Den
eneste utestaende avhengigheten er integratorens Git-gjennomgang og separate
commit. Viktige grenser: dette er source-schedule-vektede kall, ikke 791 unike
graf/lokus-par; seed-delta endrer ikke den deterministiske startperturbasjonen;
og AST-rekkevidde er ikke runtime-dekning. Ingen konklusjon utover de malte
tallene, og ingen fysikkpastand, er berettiget.
