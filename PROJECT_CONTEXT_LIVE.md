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

## Handoff context for next agent (2026-04-28)

Denne seksjonen er lagt inn for aa kunne fortsette i ny traad uten aa miste siste operative retning.

- Sjekk alltid `git status -sb` forst. Lokale, ikke-stage-de filer kan finnes og er ikke automatisk del av UniverseSimulation-sporet. Ikke anta at noe er commit-et selv om det er live ground truth pa disk.
- `band_zero_del` er fortsatt operativt frontier-regime fra `v11e`. Ikke gjenapne frontier-tuning med mindre nye filer eksplisitt krever det.
- Lorentz-/spacetime-sporet er fortsatt `not_yet`: tidligere kontroller er nyttige, men mode-dependence, placement-sensitivity og lokal anisotropi er ikke ryddet bort.
- Den ferskeste aktive signalretningen er target-768 family-/p2-horizon-sporet etter `v15cd`-`v15cn`, ikke tidlig v15 pair-collision alene.
- `v15cd` fant et sterkt target-768 family-foerstesignal; `v15ce` holdt det bare delvis paa friske seeds. Les dette som lovende skala, ikke som loest family-map.
- `v15ch` er siste klare positive p2-anker: target-768 p2-horisonten holder paa holdout, med `local_swap_p2` mot p0 og samtidig `add_chord_p2` som delt feature-level p2-kandidat. Dette er ikke en partikkelpaastand.
- `v15ci`, `v15cj` og `v15ck` testet deretter rimelige outer-tail-mekanismer. Outer-genealogi ble for generisk, outer-occupancy var bare svakt og carrier-splittet, og outer-feeder-flux endte `feeder_flux_not_yet`.
- `v15cl` flyttet observabelaksen innover mot shell2/3-gate og global-budget-lignende redistribusjon. Den bekrefter ikke en ren indre gate- eller global-budget-forklaring: `shared_p2_inner_gate = inner_gate_not_yet`, `global_budget_coupling = global_budget_coupling_not_yet`.
- `v15cm` testet en renere lokal triggerforklaring med tidlig supportnaer launch-dynamikk. P2-horisonten lever videre, saerlig `local_swap_p2`, men p2 er ikke tidligere/raskere/sterkere enn p0 i tidlig launch; diagnosen er `local_trigger_not_yet` og `support_geometry_not_explanatory`.
- `v15cn` tok en smal skala-holdout: fresh target-768 anchor pluss target `1024` under samme absolute step budget. Anchor replikerer delvis (`local_swap_p2` stottes, `add_chord_p2` svakere), men target 1024 stotter ikke p2-horisonten; diagnosen er `target768_specific_under_current_budget`.
- `v15co` er en syntese-/beslutningsrunde, ikke ny dynamikk. Den konkluderer at univers-inspirerte egenskaper kan brukes som svak heuristikk bare etter repo-lokal oversettelse: artifact hygiene som hard gate, defect non-superposition/genealogy som beste positive akse, conditional spectral quasi-invariant som sekundar akse, Lorentz som diagnostikk/negativt filter, globale regler som instrumentering, og entanglement bare som forbudt claim/weak proxy.
- `v15cp` testet akkurat budsjettforklaringen: target `1024`, samme carriers/p0/p2/seeds som `v15cn`, men step budget skalert fra 768-budsjettet (`2560 -> 3414`). P2 ble ikke gjenopplivet; derimot fikk `add_chord_p0` lengre far-shell-horisont. Diagnosen er `scaled_budget_p2_not_supported` og `p0_budget_response_without_p2`.
- `v15cq` testet midpoint target `896` med skalert budsjett (`2987`). Det gir `intermediate_p2_partial_not_supported`: `add_chord_p2` har noe far-shell-aktivitet (`established = 0.500`, horizon `49.500`) men `add_chord_p0` er like etablert og sterkere i horizon (`75.000`), mens `local_swap_p2` ikke etableres. Ingen carrier passerer support-kriteriet.
- `v15cr` er en beslutningsvurdering uten ny dynamikk. Den nedgraderer p2 som primar skala-selector og peker ut `add_chord_p0_scale_response` som beste neste kandidat, fordi add_chord_p0 horizon gaar `2.000 -> 75.000 -> 86.000` over target `768 -> 896 -> 1024`.
- `v15cs` gjorde fresh-seed holdout av `add_chord_p0` ved 896/1024 med kontroller `add_chord_p2` og `local_swap_p0`. P0 holder sterkt ved 896 (`established = 1.000`, horizon `136.000`, score `6`), men kollapser ved 1024 (`established = 0.000`, horizon `0.000`, score `0`); ved 1024 er `add_chord_p2` kontrollen som etablerer horizon (`0.500`, `82.500`).
- `v15ct` er en respons-fingerprint-syntese uten ny dynamikk. Den samler `v15cn`/`v15cp`/`v15cq`/`v15cs` og klassifiserer response etter dynamisk fingerprint heller enn p0/p2-label. Den finner at 4/6 old-vs-fresh scaled-profile-sammenligninger skifter klasse; `p0_label_stability = not_stable`, `p2_label_stability = not_stable`, mens `carrier_level_signal = add_chord_placement_sensitive_live`.
- `v15cu` kjorer det anbefalte placement-kartet: `add_chord` only, target `896/1024`, placements `0..3`, friske seed-deltaer `7307/7351`. Artifact-control er clean. P0 faller ut ved begge target; p1 er strong persistent ved begge target (`75.000`/`86.000` horizon); p2 er bare persistent ved 896; p3 er strong og dominant ved 1024 (`established = 1.000`, horizon `172.000`). Diagnosen er `target_specific_placement_switch` med `add_chord_carrier_live`.
- `v15cv` rerunner bare `v15cu` sine p1/p3-cases med rikere supportgeometri og tidlig-launch snapshots. P1-broen holder (`strong_persistent_far_shell` ved 896 og 1024), p3-switchen holder (`no_horizon` ved 896, `strong_persistent_far_shell` ved 1024), men enkel tidlig launch og statisk supportgeometri forklarer ikke switchen (`early_launch_not_sufficient`, `support_geometry_not_sufficient`).
- `v15cw` legger komponentgenealogi paa samme p1/p3 seed-split. Landskapet reproduseres (`p1_bridge=1`, `p3_switch=1`). Genealogi skiller bare en begrenset seed-split rent: `1024:p1` har `birth_death_churn` uten horizon og `split_fragment` med horizon. `split_persistent_dual` er derimot blandet globalt, saa ikke overgeneraliser.
- `v15cx` holder ut akkurat den konkrete `1024:p1` genealogy-splitten paa fire nye seed-deltaer `7411/7477/7541/7603`. Artifact-control er clean. Den kategoriske v15cw-mappingen reproduseres ikke: alle fire holdout-runs blir `split_persistent_dual`, med `established_far_shell_rate = 0.750`, mean horizon `126.000`, mean churn `1381.000`, mean max mass `235.250`.
- `v15cy` er en no-new-dynamics syntese av v15cw/v15cx. Den tester kontinuerlig genealogy-intensitet, uten aa bruke horizon som input. Resultatet er `continuous_genealogy_intensity_promising_small_n`: intensity-index har AUC `0.800` globalt, `0.875` for `p1/1024`, og `1.000` i v15cx holdout-only. Beste `p1/1024`-enkeltmetrikk er `compress_per_step` med AUC `1.000` og Spearman mot horizon-span `0.893`.
- `v15cz` er den pre-registrerte continuous-intensity-holdouten: 24 nye `1024:p1/add_chord` runs med frossen score-spec fit bare paa v15cw/v15cx. Artifact-control er clean. Primarscoren rangerer den ene no-horizon-runnen lavest (`AUC = 1.000`, exact p `0.043`), men testen blir `pre_registered_intensity_inconclusive_balance` fordi decisive outcomes er sterkt ubalansert: `22 established`, `1 no_horizon`, `1 mixed`. Dette er sterk dynamisk evidens for at `1024:p1` er en robust far-shell-horizon-lomme under disse seedene, men ikke nok balansert negativdata til aa validere intensity som selector.
- `v15da` fulgte raadgiverpanelets anbefaling om fresh frozen-score placement-kontrast: 36 nye `1024/add_chord` runs paa `p0,p1,p2` over seed-deltaer `9341..9887`, med v15cz-score-spec frosset uten refit. Claude CLI var utilgjengelig (`Not logged in`), saa panelet bestod av to remote Codex-subagenter. Artifact-control er clean. Kontrasten ble balansert nok (`11 established`, `23 no_horizon`, `1 mixed`, `1 failed`), men primarscoren feilet som selector under kriteriene: `AUC = 0.711`, exact rank-DP p `0.025`, median delta `0.282`. `p1` replikerer sterkt (`10/12 established`), `p2` er ren negativ (`12/12 no_horizon`), mens `p0` gir mange score-hoye no-horizon false positives. Diagnosen er `frozen_intensity_placement_contrast_failed`; genealogy-intensity skal nedgraderes til deskriptiv observabel.
- `v15db` er en no-new-dynamics observabelsyntese paa v15da. Den viser at downstream routing/entry skiller p0 false positives fra p1 established rent (`tail_route_index` AUC `1.000`, `entry_timing_index` AUC `1.000`), mens beste early/pre-entry kandidat er svakere (`component_early_far8_mass_fraction` AUC `0.720` for p1-vs-p0-false-positive og `0.783` for established-vs-no). P0 false positives har median genealogy-intensity `0.816` mot p1 established `0.768`, men tail_route `0.317` mot `0.898` og entry_timing `0.000` mot `0.849`. Diagnosen er `downstream_routing_separates_but_not_pre_entry`.
- `v15dc` er en strengere no-new-dynamics pre-horizon-runde paa v15da-komponentbaner. Den sensurerer etablerte runs foer `first_high_step` og bruker `early_step_limit` for no-high-runs. Beste censored observabel er `pre_far8_slope_per_100`, men bare svakt/moderat (`AUC = 0.780` for p1 established vs p0 false positives, `0.794` for established vs no-horizon). `pre_route_coherence_index` er svakere (`0.620` mot p0 false positives), og baseline genealogy-intensity er fortsatt misvisende (`0.280`). Diagnosen er `pre_horizon_route_precursor_weak`.
- `v15dd` rerunner samme smale v15da-scope, men logger route-state direkte per snapshot: route phase, sustained high3, retention, dropout og outer-pressure-without-high. Artifact-control er clean. Direct route-entry/retention skiller p1 established fra p0 high-score/no-horizon false positives rent (`first_sustained_high3_earliness`, `direct_retention_rate_after_entry`, `last12_high_rate_direct`, `sustained_high3_rate` og `direct_high_rate` har alle AUC `1.000` for p1-vs-p0-false-positive). Gruppeavlesningen er konkret: p1 established er `sustained_high_retention:10`, mens p0 high-score/no-horizon er `outer_pressure_no_high_entry:5`; median retention `0.978` vs `0.000`, median outer-pressure-without-high `0.088` vs `0.937`. Dette er mekanistisk instrumentering, ikke en pre-entry selector.
- `v15de` er en no-new-dynamics syntese av v15dd snapshot-loggen med faste tidlige vinduer. Den innforer en lekkasjevakt: tidligste p1-established sustained high3-entry er step `104`, saa vinduer `<=96` er strict pre-entry. Resultatet er negativt for route-baserte pre-entry features: beste strict pre-entry feature er `w96_mean_outer_share` med AUC `0.560` for p1-vs-p0-false-positive og `0.617` established-vs-no. Senere entry-risk vinduer blir bedre (`w640_ready_both_rate` AUC `0.800` mot p0 false positives), men er for naer entry til aa brukes som claim. Diagnosen er `pre_entry_feature_not_found`.
- `v15df` er en no-new-dynamics syntese som folger v15de-anbefalingen og tester ikke-route strict pre-entry support/topologi. Den leser v15da component trajectories og v15dd run-summary, bruker bare statisk supportgeometri og komponent/topologi ved steps `<=32/64/96` som features, og holder route-entry/retention ute av kandidatfeatures. Primarresultatet er lovende, men med confound-vakt: beste strict dynamiske metric er `w32_mean_boundary_per_mass`, AUC `0.960` for p1-vs-p0-false-positive og `0.864` established-vs-no; statisk `static_mean_support_degree` skiller enda renere (`AUC = 1.000`), men er placement-level support-informasjon og maa rapporteres som confound/audit, ikke dynamisk selector. Diagnosen er `pre_entry_support_topology_promising`.
- `v15dg` er en fresh dynamisk holdout av den frosne v15df-kandidaten `w32_mean_boundary_per_mass` paa `1024/add_chord/p0,p1,p2`, med 8 nye seed-deltaer. Artifact-control er clean. Outcome-balansen er brukbar: `7 established`, `15 no_horizon`, `2 mixed`, med `p1-established = 7` og `p0 high-score/no-horizon = 8`. Primarmetric overlever: AUC `0.821` mot p0 false positives, AUC `0.857` established-vs-no, median p1-p0false delta `2.375`. Baseline genealogy-intensity er svakere mot p0 false positives (`AUC = 0.679`). Statisk `static_mean_support_degree` skiller fortsatt perfekt (`AUC = 1.000`) og maa holdes som placement/support-confound-audit, ikke dynamisk selector. Diagnosen er `boundary_mass_holdout_supported`.
- `v15dh` tester samme frosne `w32_mean_boundary_per_mass` paa ny base/growth seed `303`, med target `1024`, `add_chord`, placements `p0,p1,p2` og 8 nye seed-deltaer. Artifact-control er clean. Resultatet er en viktig korreksjon: growth-seed-303 har endret placement-landskapet. `p1` er `8/8 no_horizon` og `0 established`, mens `p0` har `4 established` og `p2` har `4 established`. Primarmetric transferer ikke under original p1-anchor: AUC `0.463` established-vs-no. Statisk supportretning transferer heller ikke som selector (`static_mean_support_degree` AUC `0.217`), mens baseline genealogy-intensity korrelerer overall (`AUC = 0.858`) men er ikke primary og skal ikke refittes til claim. Diagnosen er `boundary_mass_not_growth_seed_transferable_under_original_anchor`.
- `v15di` er no-new-dynamics syntesen av v15dg/v15dh. Den bekrefter at placement-landskapet ikke er growth-seed-stabilt: `p1` established-rate `0.875 -> 0.000`, `p0` `0.000 -> 0.500`, `p2` `0.000 -> 0.500`. Support-signaturer endres samtidig (`p1: 1,58,537 -> 12,13,22`; `p0: 13,72,343 -> 3,4,827`; `p2: 6,8,9 -> 25,177,430`). Boundary/mass er seed-conditioned, ikke generell: AUC `0.857` paa seed 202 men `0.463` paa seed 303. Statisk supportretning er heller ikke universell (`0.967 -> 0.217`). Diagnosen er `condition_on_base_support_before_more_dynamics`.
- `v15dj` er en no-new-dynamics support-conditioned pre-run audit paa v15di-sammendraget. Den tester billige support-/base-features som placement-prior. En liten klasse `low local support volume/gap`-regler treffer minst en aktiv placement i begge tilgjengelige growth seeds (`top1_hit_rate = 1.000`), men fanger bare `2/3` aktive placements totalt (`total_active_capture_fraction_top1 = 0.667`) og valideres ikke som selector. Diagnosen er `found_sparse_candidate` + `not_validated`; neste steg er en pre-registrert fresh growth-seed holdout der support-rangeringen velger top1/top2 pluss kontrast foer dynamikk kjores.
- `v15dk` er fresh growth-seed holdout av v15dj-scouten paa growth seed `404`. Pre-run support-ranking ble skrevet foer dynamikk: top1 `p0`, top2 `p0;p2`, kontrast `p1`. Dynamikken ga motsatt bilde: `p0 = 8/8 no_horizon`, `p2 = 8/8 no_horizon`, mens `p1` var eneste aktive placement (`4 established`, `1 mixed`, `3 no_horizon`, established-rate `0.500`). Top1/top2 capture var `0.000`; diagnosen er `support_rank_not_supported` og `retire_support_rank_as_selector_candidate`. Boundary/mass var ogsaa svak som audit (`w32_mean_boundary_per_mass` AUC `0.526` established-vs-no).
- `v15dl` er en no-new-dynamics base-landscape/morphology-syntese av v15dg/v15dh/v15dk. Den samler `1024/add_chord/p0,p1,p2` over growth seeds `202/303/404` og legger til pre-run morfologiobservabler fra basegrafen/add_chord-proben: lokal volumvekst, return-probability/spectral-dimension proxy, shortcut/efficiency og enkel Forman-style curvature. Resultatet bekrefter `base_conditioned_placement_landscape`: seed 202 har aktiv `p1`, seed 303 har aktiv `p0;p2`, seed 404 har aktiv `p1`. Beste nye post-hoc screen er `delta_return_t2` med placement-level AUC `0.900`, men som regel er den bare `weak_posthoc_top2_scout` (`top1_capture = 0.750`, `top2_capture = 0.750`). Dette kan hoyst fryses for en liten v15dm-holdout; det er ikke validert selector.
- Arbeidskonklusjon akkurat naa: `add_chord`-carrieren er fortsatt live som target-/placement-landskap, men fixed placement-labels og enkel pre-run support-volume/gap-rangering er ikke nok. `p1/1024` er ikke universell, men p1 reaktiveres paa growth seed 404 etter aa ha feilet paa 303; landskapet er base-betinget og ikke forklart av low support-volume. Boundary/mass, statisk support og genealogy-intensity er best lest som deskriptive/audit-observabler, ikke generelle selectors. `delta_return_t2` er beste nye morfologi-scout, men post-hoc og svak; hvis den testes videre maa den fryses foer ny dynamikk. Ikke oppgrader global invariant-, Lorentz-, entanglement-, partikkel- eller universell-geometri-sprak.
- Les foer ny implementering: `Documentation/v15ch_target768_local_swap_p2_horizon_holdout_lab.md`, `Documentation/v15ci_target768_p2_horizon_genealogy_mechanism_lab.md`, `Documentation/v15cj_target768_outer_occupancy_concentration_lab.md`, `Documentation/v15ck_target768_outer_feeder_flux_lab.md`, `Documentation/v15cl_target768_inner_gate_global_budget_lab.md`, `Documentation/v15cm_target768_local_trigger_lab.md`, `Documentation/v15cn_p2_horizon_scale_holdout_lab.md`, `Documentation/v15co_configuration_heuristic_assessment.md`, `Documentation/v15cp_target1024_scaled_budget_p2_horizon_lab.md`, `Documentation/v15cq_intermediate_scale_p2_horizon_lab.md`, `Documentation/v15cr_next_direction_assessment.md`, `Documentation/v15cs_add_chord_p0_scale_response_holdout.md`, `Documentation/v15ct_response_fingerprint_synthesis.md`, `Documentation/v15cu_add_chord_placement_response_map.md`, `Documentation/v15cv_add_chord_winning_placement_mechanism_probe.md`, `Documentation/v15cw_add_chord_p1_p3_genealogy_seed_split.md`, `Documentation/v15cx_p1_1024_genealogy_holdout.md`, `Documentation/v15cy_continuous_genealogy_intensity_synthesis.md`, `Documentation/v15cz_pre_registered_continuous_intensity_holdout.md`, `Documentation/v15da_frozen_intensity_placement_contrast.md`, `Documentation/v15db_routing_phase_observable_synthesis.md`, `Documentation/v15dc_pre_horizon_routing_precursor.md`, `Documentation/v15dd_direct_route_entry_retention.md`, `Documentation/v15de_pre_entry_feature_synthesis.md`, `Documentation/v15df_pre_entry_support_topology_synthesis.md`, `Documentation/v15dg_boundary_mass_holdout.md`, `Documentation/v15dh_boundary_mass_growth_seed_holdout.md`, `Documentation/v15di_growth_seed_signature_synthesis.md`, `Documentation/v15dj_support_conditioned_pre_run_audit.md`, `Documentation/v15dk_pre_registered_support_rank_holdout.md`, `Documentation/v15dl_base_landscape_morphology_synthesis.md`, og de tilhorende `v0_15ch`-`v0_15dl` anbefalingene.
- Ikke fabriker nye runtime-resultater. Hvis du ikke kjorer en ny lab, lag bare skjelett/plan/schema og skriv eksplisitt at CSV-resultater ikke finnes ennaa.

## Siste sikre live status

Per dagens lokale state er `v11e` den siste frontier-avklaringen. `v12`, `v12b`, `v12c`, `v12d`, `v12e`, `v12f`, `v12g`, `v12h`, `v12i`, `v12j`, `v12k`, `v12l`, `v12m`, `v12n`, `v13`, `v13b`, `v13c`, `v13d`, `v13e`, `v13f`, `v13g`, `v13h`, `v13i`, `v13j`, `v13k`, `v13l`, `v13m`, `v13n`, `v14`, `v14b`, `v14c`, `v15`, `v15b`, `v15c`, `v15d`, `v15e`, `v15f`, `v15g`, `v15h`, `v15i`, `v15j`, `v15k`, `v15l`, `v15m`, `v15n`, `v15o`, `v15p`, `v15q`, `v15r`, `v15s`, `v15t`, `v15u`, `v15v`, `v15w`, `v15x`, `v15y`, `v15z`, `v15aa`, `v15ab`, `v15ac`, `v15ad`, `v15ae`, `v15af`, `v15ag`, `v15ai`, `v15aj`, `v15ak`, `v15al`, `v15am`, `v15an`, `v15ao`, `v15ap`, `v15aq`, `v15ar`, `v15as`, `v15at`, `v15au`, `v15av`, `v15aw`, `v15ax`, `v15ay`, `v15az`, `v15ba`, `v15bb`, `v15bc`, `v15bd`, `v15be`, `v15bf`, `v15bg`, `v15bh`, `v15bi`, `v15bj`, `v15bk`, `v15bl`, `v15bm`, `v15bn`, `v15bo`, `v15bp`, `v15bq`, `v15br`, `v15bs`, `v15bt`, `v15bu`, `v15bv`, `v15bw`, `v15bx`, `v15by`, `v15bz`, `v15ca`, `v15cb`, `v15cc`, `v15cd`, `v15ce`, `v15cf`, `v15cg`, `v15ch`, `v15ci`, `v15cj`, `v15ck`, `v15cl`, `v15cm`, `v15cn`, `v15co`, `v15cp`, `v15cq`, `v15cr`, `v15cs`, `v15ct`, `v15cu`, `v15cv`, `v15cw`, `v15cx`, `v15cy`, `v15cz`, `v15da`, `v15db`, `v15dc`, `v15dd`, `v15de`, `v15df`, `v15dg`, `v15dh`, `v15di`, `v15dj`, `v15dk` og `v15dl` er de aktive struktur-/transfer-/Lorentz-/defect-/heuristikk-rundene bygget pa den.

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
- Carrier-first-spectral-holdout-script: `relational_universe_v15bm_carrier_first_spectral_holdout.py`
- Carrier-first-spectral-holdout-rapport: `Documentation/v15bm_carrier_first_spectral_holdout.md`
- Carrier-first-spectral-holdout-target-sammendrag: `Documentation/v15bm_carrier_first_spectral_target_summary.csv`
- Carrier-first-spectral-holdout-rows: `Documentation/v15bm_carrier_first_spectral_rows.csv`
- Carrier-first-spectral-holdout-aggregate: `Documentation/v15bm_carrier_first_spectral_aggregate.csv`
- Carrier-first-spectral-holdout-diagnosis: `Documentation/v15bm_carrier_first_spectral_diagnosis.csv`
- Carrier-first-spectral-holdout-anbefaling: `Documentation/v0_15bm_operativ_anbefaling.md`
- Family-structure-symmetry-script: `relational_universe_v15bv_family_structure_symmetry_lab.py`
- Family-structure-symmetry-rapport: `Documentation/v15bv_family_structure_symmetry_lab.md`
- Family-structure-symmetry-target: `Documentation/v15bv_family_structure_symmetry_target_summary.csv`
- Family-structure-symmetry-rows: `Documentation/v15bv_family_structure_symmetry_rows.csv`
- Family-structure-symmetry-aggregate: `Documentation/v15bv_family_structure_symmetry_aggregate.csv`
- Family-structure-symmetry-family-summary: `Documentation/v15bv_family_structure_symmetry_family_summary.csv`
- Family-structure-symmetry-pairwise: `Documentation/v15bv_family_structure_symmetry_pairwise.csv`
- Family-structure-symmetry-diagnosis: `Documentation/v15bv_family_structure_symmetry_diagnosis.csv`
- Family-structure-symmetry-anbefaling: `Documentation/v0_15bv_operativ_anbefaling.md`
- Family-structure-holdout-script: `relational_universe_v15bw_family_structure_holdout.py`
- Family-structure-holdout-rapport: `Documentation/v15bw_family_structure_holdout_lab.md`
- Family-structure-holdout-target: `Documentation/v15bw_family_structure_holdout_target_summary.csv`
- Family-structure-holdout-rows: `Documentation/v15bw_family_structure_holdout_rows.csv`
- Family-structure-holdout-aggregate: `Documentation/v15bw_family_structure_holdout_aggregate.csv`
- Family-structure-holdout-summary: `Documentation/v15bw_family_structure_holdout_summary.csv`
- Family-structure-holdout-pairwise: `Documentation/v15bw_family_structure_holdout_pairwise.csv`
- Family-structure-holdout-diagnosis: `Documentation/v15bw_family_structure_holdout_diagnosis.csv`
- Family-structure-holdout-anbefaling: `Documentation/v0_15bw_operativ_anbefaling.md`
- Scale-jump-family-probe-script: `relational_universe_v15bx_scale_jump_family_probe.py`
- Scale-jump-family-probe-rapport: `Documentation/v15bx_scale_jump_family_probe_lab.md`
- Scale-jump-family-probe-target: `Documentation/v15bx_scale_jump_family_probe_target_summary.csv`
- Scale-jump-family-probe-rows: `Documentation/v15bx_scale_jump_family_probe_rows.csv`
- Scale-jump-family-probe-aggregate: `Documentation/v15bx_scale_jump_family_probe_aggregate.csv`
- Scale-jump-family-probe-family-summary: `Documentation/v15bx_scale_jump_family_probe_family_summary.csv`
- Scale-jump-family-probe-pairwise: `Documentation/v15bx_scale_jump_family_probe_pairwise.csv`
- Scale-jump-family-probe-diagnosis: `Documentation/v15bx_scale_jump_family_probe_diagnosis.csv`
- Scale-jump-family-probe-anbefaling: `Documentation/v0_15bx_operativ_anbefaling.md`
- Target192-plateau-holdout-script: `relational_universe_v15by_target192_plateau_holdout.py`
- Target192-plateau-holdout-rapport: `Documentation/v15by_target192_plateau_holdout_lab.md`
- Target192-plateau-holdout-target: `Documentation/v15by_target192_plateau_holdout_target_summary.csv`
- Target192-plateau-holdout-rows: `Documentation/v15by_target192_plateau_holdout_rows.csv`
- Target192-plateau-holdout-aggregate: `Documentation/v15by_target192_plateau_holdout_aggregate.csv`
- Target192-plateau-holdout-summary: `Documentation/v15by_target192_plateau_holdout_summary.csv`
- Target192-plateau-holdout-pairwise: `Documentation/v15by_target192_plateau_holdout_pairwise.csv`
- Target192-plateau-holdout-diagnosis: `Documentation/v15by_target192_plateau_holdout_diagnosis.csv`
- Target192-plateau-holdout-anbefaling: `Documentation/v0_15by_operativ_anbefaling.md`
- Target384-family-probe-script: `relational_universe_v15bz_target384_family_probe.py`
- Target384-family-probe-rapport: `Documentation/v15bz_target384_family_probe_lab.md`
- Target384-family-probe-target: `Documentation/v15bz_target384_family_probe_target_summary.csv`
- Target384-family-probe-rows: `Documentation/v15bz_target384_family_probe_rows.csv`
- Target384-family-probe-aggregate: `Documentation/v15bz_target384_family_probe_aggregate.csv`
- Target384-family-probe-family-summary: `Documentation/v15bz_target384_family_probe_family_summary.csv`
- Target384-family-probe-pairwise: `Documentation/v15bz_target384_family_probe_pairwise.csv`
- Target384-family-probe-diagnosis: `Documentation/v15bz_target384_family_probe_diagnosis.csv`
- Target384-family-probe-anbefaling: `Documentation/v0_15bz_operativ_anbefaling.md`
- Target192-radial-occupancy-script: `relational_universe_v15ca_target192_radial_occupancy_mechanism_lab.py`
- Target192-radial-occupancy-rapport: `Documentation/v15ca_target192_radial_occupancy_mechanism_lab.md`
- Target192-radial-occupancy-target: `Documentation/v15ca_target192_radial_occupancy_target_summary.csv`
- Target192-radial-occupancy-rows: `Documentation/v15ca_target192_radial_occupancy_rows.csv`
- Target192-radial-occupancy-aggregate: `Documentation/v15ca_target192_radial_occupancy_aggregate.csv`
- Target192-radial-occupancy-compare: `Documentation/v15ca_target192_radial_occupancy_compare.csv`
- Target192-radial-occupancy-diagnosis: `Documentation/v15ca_target192_radial_occupancy_diagnosis.csv`
- Target192-radial-occupancy-anbefaling: `Documentation/v0_15ca_operativ_anbefaling.md`
- Target384-candidate-holdout-script: `relational_universe_v15cb_target384_candidate_holdout.py`
- Target384-candidate-holdout-rapport: `Documentation/v15cb_target384_candidate_holdout_lab.md`
- Target384-candidate-holdout-target: `Documentation/v15cb_target384_candidate_holdout_target_summary.csv`
- Target384-candidate-holdout-rows: `Documentation/v15cb_target384_candidate_holdout_rows.csv`
- Target384-candidate-holdout-aggregate: `Documentation/v15cb_target384_candidate_holdout_aggregate.csv`
- Target384-candidate-holdout-summary: `Documentation/v15cb_target384_candidate_holdout_summary.csv`
- Target384-candidate-holdout-symmetry: `Documentation/v15cb_target384_candidate_holdout_symmetry_summary.csv`
- Target384-candidate-holdout-diagnosis: `Documentation/v15cb_target384_candidate_holdout_diagnosis.csv`
- Target384-candidate-holdout-anbefaling: `Documentation/v0_15cb_operativ_anbefaling.md`
- Target384-shell-turnover-script: `relational_universe_v15cc_target384_shell_turnover_observable.py`
- Target384-shell-turnover-rapport: `Documentation/v15cc_target384_shell_turnover_observable.md`
- Target384-shell-turnover-target: `Documentation/v15cc_target384_shell_turnover_target_summary.csv`
- Target384-shell-turnover-rows: `Documentation/v15cc_target384_shell_turnover_rows.csv`
- Target384-shell-turnover-aggregate: `Documentation/v15cc_target384_shell_turnover_aggregate.csv`
- Target384-shell-turnover-pairwise: `Documentation/v15cc_target384_shell_turnover_pairwise.csv`
- Target384-shell-turnover-summary: `Documentation/v15cc_target384_shell_turnover_summary.csv`
- Target384-shell-turnover-diagnosis: `Documentation/v15cc_target384_shell_turnover_diagnosis.csv`
- Target384-shell-turnover-anbefaling: `Documentation/v0_15cc_operativ_anbefaling.md`
- Target768-family-probe-script: `relational_universe_v15cd_target768_family_probe.py`
- Target768-family-probe-rapport: `Documentation/v15cd_target768_family_probe_lab.md`
- Target768-family-probe-target: `Documentation/v15cd_target768_family_probe_target_summary.csv`
- Target768-family-probe-rows: `Documentation/v15cd_target768_family_probe_rows.csv`
- Target768-family-probe-aggregate: `Documentation/v15cd_target768_family_probe_aggregate.csv`
- Target768-family-probe-family-summary: `Documentation/v15cd_target768_family_probe_family_summary.csv`
- Target768-family-probe-pairwise: `Documentation/v15cd_target768_family_probe_pairwise.csv`
- Target768-family-probe-diagnosis: `Documentation/v15cd_target768_family_probe_diagnosis.csv`
- Target768-family-probe-anbefaling: `Documentation/v0_15cd_operativ_anbefaling.md`
- Target768-plateau-holdout-script: `relational_universe_v15ce_target768_plateau_holdout.py`
- Target768-plateau-holdout-rapport: `Documentation/v15ce_target768_plateau_holdout_lab.md`
- Target768-plateau-holdout-target: `Documentation/v15ce_target768_plateau_holdout_target_summary.csv`
- Target768-plateau-holdout-rows: `Documentation/v15ce_target768_plateau_holdout_rows.csv`
- Target768-plateau-holdout-aggregate: `Documentation/v15ce_target768_plateau_holdout_aggregate.csv`
- Target768-plateau-holdout-summary: `Documentation/v15ce_target768_plateau_holdout_summary.csv`
- Target768-plateau-holdout-pairwise: `Documentation/v15ce_target768_plateau_holdout_pairwise.csv`
- Target768-plateau-holdout-symmetry: `Documentation/v15ce_target768_plateau_holdout_symmetry_summary.csv`
- Target768-plateau-holdout-diagnosis: `Documentation/v15ce_target768_plateau_holdout_diagnosis.csv`
- Target768-plateau-holdout-anbefaling: `Documentation/v0_15ce_operativ_anbefaling.md`
- Target768-support-locus-script: `relational_universe_v15cf_target768_support_locus_mechanism_lab.py`
- Target768-support-locus-rapport: `Documentation/v15cf_target768_support_locus_mechanism_lab.md`
- Target768-support-locus-target: `Documentation/v15cf_target768_support_locus_target_summary.csv`
- Target768-support-locus-runs: `Documentation/v15cf_target768_support_locus_runs.csv`
- Target768-support-locus-aggregate: `Documentation/v15cf_target768_support_locus_aggregate.csv`
- Target768-support-locus-locus-summary: `Documentation/v15cf_target768_support_locus_locus_summary.csv`
- Target768-support-locus-compare: `Documentation/v15cf_target768_support_locus_compare.csv`
- Target768-support-locus-diagnosis: `Documentation/v15cf_target768_support_locus_diagnosis.csv`
- Target768-support-locus-anbefaling: `Documentation/v0_15cf_operativ_anbefaling.md`
- Target768-far-shell-horizon-script: `relational_universe_v15cg_target768_far_shell_horizon_lab.py`
- Target768-far-shell-horizon-rapport: `Documentation/v15cg_target768_far_shell_horizon_lab.md`
- Target768-far-shell-horizon-target: `Documentation/v15cg_target768_far_shell_horizon_target_summary.csv`
- Target768-far-shell-horizon-runs: `Documentation/v15cg_target768_far_shell_horizon_runs.csv`
- Target768-far-shell-horizon-aggregate: `Documentation/v15cg_target768_far_shell_horizon_aggregate.csv`
- Target768-far-shell-horizon-compare: `Documentation/v15cg_target768_far_shell_horizon_compare.csv`
- Target768-far-shell-horizon-diagnosis: `Documentation/v15cg_target768_far_shell_horizon_diagnosis.csv`
- Target768-far-shell-horizon-anbefaling: `Documentation/v0_15cg_operativ_anbefaling.md`
- Target768-p2-horizon-holdout-script: `relational_universe_v15ch_target768_local_swap_p2_horizon_holdout.py`
- Target768-p2-horizon-holdout-rapport: `Documentation/v15ch_target768_local_swap_p2_horizon_holdout_lab.md`
- Target768-p2-horizon-holdout-target: `Documentation/v15ch_target768_local_swap_p2_horizon_target_summary.csv`
- Target768-p2-horizon-holdout-runs: `Documentation/v15ch_target768_local_swap_p2_horizon_runs.csv`
- Target768-p2-horizon-holdout-threshold-rows: `Documentation/v15ch_target768_local_swap_p2_horizon_threshold_rows.csv`
- Target768-p2-horizon-holdout-aggregate: `Documentation/v15ch_target768_local_swap_p2_horizon_aggregate.csv`
- Target768-p2-horizon-holdout-compare: `Documentation/v15ch_target768_local_swap_p2_horizon_compare.csv`
- Target768-p2-horizon-holdout-robustness: `Documentation/v15ch_target768_local_swap_p2_horizon_robustness.csv`
- Target768-p2-horizon-holdout-diagnosis: `Documentation/v15ch_target768_local_swap_p2_horizon_diagnosis.csv`
- Target768-p2-horizon-holdout-anbefaling: `Documentation/v0_15ch_operativ_anbefaling.md`
- Target768-p2-horizon-genealogy-script: `relational_universe_v15ci_target768_p2_horizon_genealogy_mechanism_lab.py`
- Target768-p2-horizon-genealogy-rapport: `Documentation/v15ci_target768_p2_horizon_genealogy_mechanism_lab.md`
- Target768-p2-horizon-genealogy-target: `Documentation/v15ci_target768_p2_horizon_genealogy_target_summary.csv`
- Target768-p2-horizon-genealogy-runs: `Documentation/v15ci_target768_p2_horizon_genealogy_runs.csv`
- Target768-p2-horizon-genealogy-components: `Documentation/v15ci_target768_p2_horizon_genealogy_component_rows.csv`
- Target768-p2-horizon-genealogy-events: `Documentation/v15ci_target768_p2_horizon_genealogy_event_rows.csv`
- Target768-p2-horizon-genealogy-aggregate: `Documentation/v15ci_target768_p2_horizon_genealogy_aggregate.csv`
- Target768-p2-horizon-genealogy-compare: `Documentation/v15ci_target768_p2_horizon_genealogy_compare.csv`
- Target768-p2-horizon-genealogy-diagnosis: `Documentation/v15ci_target768_p2_horizon_genealogy_diagnosis.csv`
- Target768-p2-horizon-genealogy-anbefaling: `Documentation/v0_15ci_operativ_anbefaling.md`
- Target768-outer-occupancy-script: `relational_universe_v15cj_target768_outer_occupancy_concentration_lab.py`
- Target768-outer-occupancy-rapport: `Documentation/v15cj_target768_outer_occupancy_concentration_lab.md`
- Target768-outer-occupancy-target: `Documentation/v15cj_target768_outer_occupancy_target_summary.csv`
- Target768-outer-occupancy-runs: `Documentation/v15cj_target768_outer_occupancy_runs.csv`
- Target768-outer-occupancy-aggregate: `Documentation/v15cj_target768_outer_occupancy_aggregate.csv`
- Target768-outer-occupancy-compare: `Documentation/v15cj_target768_outer_occupancy_compare.csv`
- Target768-outer-occupancy-diagnosis: `Documentation/v15cj_target768_outer_occupancy_diagnosis.csv`
- Target768-outer-occupancy-anbefaling: `Documentation/v0_15cj_operativ_anbefaling.md`
- Target768-outer-feeder-script: `relational_universe_v15ck_target768_outer_feeder_flux_lab.py`
- Target768-outer-feeder-rapport: `Documentation/v15ck_target768_outer_feeder_flux_lab.md`
- Target768-outer-feeder-target: `Documentation/v15ck_target768_outer_feeder_target_summary.csv`
- Target768-outer-feeder-runs: `Documentation/v15ck_target768_outer_feeder_runs.csv`
- Target768-outer-feeder-snapshots: `Documentation/v15ck_target768_outer_feeder_snapshot_rows.csv`
- Target768-outer-feeder-aggregate: `Documentation/v15ck_target768_outer_feeder_aggregate.csv`
- Target768-outer-feeder-compare: `Documentation/v15ck_target768_outer_feeder_compare.csv`
- Target768-outer-feeder-diagnosis: `Documentation/v15ck_target768_outer_feeder_diagnosis.csv`
- Target768-outer-feeder-anbefaling: `Documentation/v0_15ck_operativ_anbefaling.md`
- Target768-inner-gate-global-budget-script: `relational_universe_v15cl_target768_inner_gate_global_budget_lab.py`
- Target768-inner-gate-global-budget-rapport: `Documentation/v15cl_target768_inner_gate_global_budget_lab.md`
- Target768-inner-gate-global-budget-target: `Documentation/v15cl_target768_inner_gate_global_budget_target_summary.csv`
- Target768-inner-gate-global-budget-runs: `Documentation/v15cl_target768_inner_gate_global_budget_runs.csv`
- Target768-inner-gate-global-budget-snapshots: `Documentation/v15cl_target768_inner_gate_global_budget_snapshot_rows.csv`
- Target768-inner-gate-global-budget-aggregate: `Documentation/v15cl_target768_inner_gate_global_budget_aggregate.csv`
- Target768-inner-gate-global-budget-compare: `Documentation/v15cl_target768_inner_gate_global_budget_compare.csv`
- Target768-inner-gate-global-budget-diagnosis: `Documentation/v15cl_target768_inner_gate_global_budget_diagnosis.csv`
- Target768-inner-gate-global-budget-anbefaling: `Documentation/v0_15cl_operativ_anbefaling.md`
- Target768-local-trigger-script: `relational_universe_v15cm_target768_local_trigger_lab.py`
- Target768-local-trigger-rapport: `Documentation/v15cm_target768_local_trigger_lab.md`
- Target768-local-trigger-target: `Documentation/v15cm_target768_local_trigger_target_summary.csv`
- Target768-local-trigger-runs: `Documentation/v15cm_target768_local_trigger_runs.csv`
- Target768-local-trigger-snapshots: `Documentation/v15cm_target768_local_trigger_snapshot_rows.csv`
- Target768-local-trigger-aggregate: `Documentation/v15cm_target768_local_trigger_aggregate.csv`
- Target768-local-trigger-compare: `Documentation/v15cm_target768_local_trigger_compare.csv`
- Target768-local-trigger-diagnosis: `Documentation/v15cm_target768_local_trigger_diagnosis.csv`
- Target768-local-trigger-anbefaling: `Documentation/v0_15cm_operativ_anbefaling.md`
- Target768-local-trigger-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cm.md`
- P2-horizon-scale-holdout-script: `relational_universe_v15cn_p2_horizon_scale_holdout.py`
- P2-horizon-scale-holdout-rapport: `Documentation/v15cn_p2_horizon_scale_holdout_lab.md`
- P2-horizon-scale-holdout-target: `Documentation/v15cn_p2_horizon_scale_holdout_target_summary.csv`
- P2-horizon-scale-holdout-runs: `Documentation/v15cn_p2_horizon_scale_holdout_runs.csv`
- P2-horizon-scale-holdout-aggregate: `Documentation/v15cn_p2_horizon_scale_holdout_aggregate.csv`
- P2-horizon-scale-holdout-compare: `Documentation/v15cn_p2_horizon_scale_holdout_compare.csv`
- P2-horizon-scale-holdout-scale-summary: `Documentation/v15cn_p2_horizon_scale_holdout_scale_summary.csv`
- P2-horizon-scale-holdout-diagnosis: `Documentation/v15cn_p2_horizon_scale_holdout_diagnosis.csv`
- P2-horizon-scale-holdout-anbefaling: `Documentation/v0_15cn_operativ_anbefaling.md`
- P2-horizon-scale-holdout-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cn.md`
- Configuration-heuristic-script: `relational_universe_v15co_configuration_heuristic_assessment.py`
- Configuration-heuristic-rapport: `Documentation/v15co_configuration_heuristic_assessment.md`
- Configuration-heuristic-axes: `Documentation/v15co_configuration_heuristic_axes.csv`
- Configuration-heuristic-rules: `Documentation/v15co_configuration_candidate_rules.csv`
- Configuration-heuristic-decision-table: `Documentation/v15co_configuration_decision_table.csv`
- Configuration-heuristic-physics-anchors: `Documentation/v15co_configuration_physics_anchor_notes.csv`
- Configuration-heuristic-anbefaling: `Documentation/v0_15co_operativ_anbefaling.md`
- Configuration-heuristic-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15co.md`
- Target1024-scaled-budget-script: `relational_universe_v15cp_target1024_scaled_budget_p2_horizon.py`
- Target1024-scaled-budget-rapport: `Documentation/v15cp_target1024_scaled_budget_p2_horizon_lab.md`
- Target1024-scaled-budget-target: `Documentation/v15cp_target1024_scaled_budget_target_summary.csv`
- Target1024-scaled-budget-runs: `Documentation/v15cp_target1024_scaled_budget_runs.csv`
- Target1024-scaled-budget-aggregate: `Documentation/v15cp_target1024_scaled_budget_aggregate.csv`
- Target1024-scaled-budget-compare: `Documentation/v15cp_target1024_scaled_budget_compare.csv`
- Target1024-scaled-budget-budget-compare: `Documentation/v15cp_target1024_scaled_budget_budget_compare.csv`
- Target1024-scaled-budget-diagnosis: `Documentation/v15cp_target1024_scaled_budget_diagnosis.csv`
- Target1024-scaled-budget-anbefaling: `Documentation/v0_15cp_operativ_anbefaling.md`
- Target1024-scaled-budget-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cp.md`
- Intermediate-scale-script: `relational_universe_v15cq_intermediate_scale_p2_horizon.py`
- Intermediate-scale-rapport: `Documentation/v15cq_intermediate_scale_p2_horizon_lab.md`
- Intermediate-scale-target: `Documentation/v15cq_intermediate_scale_target_summary.csv`
- Intermediate-scale-runs: `Documentation/v15cq_intermediate_scale_runs.csv`
- Intermediate-scale-aggregate: `Documentation/v15cq_intermediate_scale_aggregate.csv`
- Intermediate-scale-compare: `Documentation/v15cq_intermediate_scale_compare.csv`
- Intermediate-scale-ladder: `Documentation/v15cq_intermediate_scale_ladder.csv`
- Intermediate-scale-diagnosis: `Documentation/v15cq_intermediate_scale_diagnosis.csv`
- Intermediate-scale-anbefaling: `Documentation/v0_15cq_operativ_anbefaling.md`
- Intermediate-scale-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cq.md`
- Next-direction-assessment: `Documentation/v15cr_next_direction_assessment.md`
- Next-direction-decision-matrix: `Documentation/v15cr_next_direction_decision_matrix.csv`
- Next-direction-anbefaling: `Documentation/v0_15cr_operativ_anbefaling.md`
- Next-direction-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cr.md`
- Add-chord-p0-scale-response-script: `relational_universe_v15cs_add_chord_p0_scale_response_holdout.py`
- Add-chord-p0-scale-response-rapport: `Documentation/v15cs_add_chord_p0_scale_response_holdout.md`
- Add-chord-p0-scale-response-target: `Documentation/v15cs_add_chord_p0_scale_response_target_summary.csv`
- Add-chord-p0-scale-response-runs: `Documentation/v15cs_add_chord_p0_scale_response_runs.csv`
- Add-chord-p0-scale-response-aggregate: `Documentation/v15cs_add_chord_p0_scale_response_aggregate.csv`
- Add-chord-p0-scale-response-control-compare: `Documentation/v15cs_add_chord_p0_scale_response_control_compare.csv`
- Add-chord-p0-scale-response-summary: `Documentation/v15cs_add_chord_p0_scale_response_summary.csv`
- Add-chord-p0-scale-response-historical-compare: `Documentation/v15cs_add_chord_p0_scale_response_historical_compare.csv`
- Add-chord-p0-scale-response-diagnosis: `Documentation/v15cs_add_chord_p0_scale_response_diagnosis.csv`
- Add-chord-p0-scale-response-anbefaling: `Documentation/v0_15cs_operativ_anbefaling.md`
- Add-chord-p0-scale-response-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cs.md`
- Response-fingerprint-synthesis-script: `relational_universe_v15ct_response_fingerprint_synthesis.py`
- Response-fingerprint-synthesis-rapport: `Documentation/v15ct_response_fingerprint_synthesis.md`
- Response-fingerprint-synthesis-fingerprints: `Documentation/v15ct_response_fingerprints.csv`
- Response-fingerprint-synthesis-class-summary: `Documentation/v15ct_response_class_summary.csv`
- Response-fingerprint-synthesis-seed-stability: `Documentation/v15ct_response_seed_stability.csv`
- Response-fingerprint-synthesis-decisions: `Documentation/v15ct_response_decisions.csv`
- Response-fingerprint-synthesis-anbefaling: `Documentation/v0_15ct_operativ_anbefaling.md`
- Response-fingerprint-synthesis-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ct.md`
- Add-chord-placement-response-script: `relational_universe_v15cu_add_chord_placement_response_map.py`
- Add-chord-placement-response-rapport: `Documentation/v15cu_add_chord_placement_response_map.md`
- Add-chord-placement-response-target: `Documentation/v15cu_add_chord_placement_response_target_summary.csv`
- Add-chord-placement-response-runs: `Documentation/v15cu_add_chord_placement_response_runs.csv`
- Add-chord-placement-response-aggregate: `Documentation/v15cu_add_chord_placement_response_aggregate.csv`
- Add-chord-placement-response-compare: `Documentation/v15cu_add_chord_placement_response_compare.csv`
- Add-chord-placement-response-target-patterns: `Documentation/v15cu_add_chord_placement_response_target_patterns.csv`
- Add-chord-placement-response-stability: `Documentation/v15cu_add_chord_placement_response_stability.csv`
- Add-chord-placement-response-diagnosis: `Documentation/v15cu_add_chord_placement_response_diagnosis.csv`
- Add-chord-placement-response-anbefaling: `Documentation/v0_15cu_operativ_anbefaling.md`
- Add-chord-placement-response-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cu.md`
- Add-chord-winning-placement-mechanism-script: `relational_universe_v15cv_add_chord_winning_placement_mechanism_probe.py`
- Add-chord-winning-placement-mechanism-rapport: `Documentation/v15cv_add_chord_winning_placement_mechanism_probe.md`
- Add-chord-winning-placement-mechanism-target: `Documentation/v15cv_add_chord_winning_placement_target_summary.csv`
- Add-chord-winning-placement-mechanism-support: `Documentation/v15cv_add_chord_winning_placement_support_geometry.csv`
- Add-chord-winning-placement-mechanism-snapshots: `Documentation/v15cv_add_chord_winning_placement_snapshot_rows.csv`
- Add-chord-winning-placement-mechanism-runs: `Documentation/v15cv_add_chord_winning_placement_runs.csv`
- Add-chord-winning-placement-mechanism-aggregate: `Documentation/v15cv_add_chord_winning_placement_aggregate.csv`
- Add-chord-winning-placement-mechanism-compare: `Documentation/v15cv_add_chord_winning_placement_compare.csv`
- Add-chord-winning-placement-mechanism-diagnosis: `Documentation/v15cv_add_chord_winning_placement_diagnosis.csv`
- Add-chord-winning-placement-mechanism-anbefaling: `Documentation/v0_15cv_operativ_anbefaling.md`
- Add-chord-winning-placement-mechanism-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cv.md`
- Add-chord-p1-p3-genealogy-script: `relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split.py`
- Add-chord-p1-p3-genealogy-rapport: `Documentation/v15cw_add_chord_p1_p3_genealogy_seed_split.md`
- Add-chord-p1-p3-genealogy-target: `Documentation/v15cw_add_chord_p1_p3_genealogy_target_summary.csv`
- Add-chord-p1-p3-genealogy-components: `Documentation/v15cw_add_chord_p1_p3_genealogy_component_trajectories.csv`
- Add-chord-p1-p3-genealogy-events: `Documentation/v15cw_add_chord_p1_p3_genealogy_event_log.csv`
- Add-chord-p1-p3-genealogy-runs: `Documentation/v15cw_add_chord_p1_p3_genealogy_runs.csv`
- Add-chord-p1-p3-genealogy-aggregate: `Documentation/v15cw_add_chord_p1_p3_genealogy_aggregate.csv`
- Add-chord-p1-p3-genealogy-chain-summary: `Documentation/v15cw_add_chord_p1_p3_genealogy_chain_summary.csv`
- Add-chord-p1-p3-genealogy-diagnosis: `Documentation/v15cw_add_chord_p1_p3_genealogy_diagnosis.csv`
- Add-chord-p1-p3-genealogy-anbefaling: `Documentation/v0_15cw_operativ_anbefaling.md`
- Add-chord-p1-p3-genealogy-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cw.md`
- Add-chord-p1-1024-genealogy-holdout-script: `relational_universe_v15cx_p1_1024_genealogy_holdout.py`
- Add-chord-p1-1024-genealogy-holdout-rapport: `Documentation/v15cx_p1_1024_genealogy_holdout.md`
- Add-chord-p1-1024-genealogy-holdout-target: `Documentation/v15cx_p1_1024_genealogy_holdout_target_summary.csv`
- Add-chord-p1-1024-genealogy-holdout-components: `Documentation/v15cx_p1_1024_genealogy_holdout_component_trajectories.csv`
- Add-chord-p1-1024-genealogy-holdout-events: `Documentation/v15cx_p1_1024_genealogy_holdout_event_log.csv`
- Add-chord-p1-1024-genealogy-holdout-runs: `Documentation/v15cx_p1_1024_genealogy_holdout_runs.csv`
- Add-chord-p1-1024-genealogy-holdout-aggregate: `Documentation/v15cx_p1_1024_genealogy_holdout_aggregate.csv`
- Add-chord-p1-1024-genealogy-holdout-chain-summary: `Documentation/v15cx_p1_1024_genealogy_holdout_chain_summary.csv`
- Add-chord-p1-1024-genealogy-holdout-diagnosis: `Documentation/v15cx_p1_1024_genealogy_holdout_diagnosis.csv`
- Add-chord-p1-1024-genealogy-holdout-anbefaling: `Documentation/v0_15cx_operativ_anbefaling.md`
- Add-chord-p1-1024-genealogy-holdout-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cx.md`
- Continuous-genealogy-intensity-script: `relational_universe_v15cy_continuous_genealogy_intensity_synthesis.py`
- Continuous-genealogy-intensity-rapport: `Documentation/v15cy_continuous_genealogy_intensity_synthesis.md`
- Continuous-genealogy-intensity-runs: `Documentation/v15cy_continuous_genealogy_intensity_runs.csv`
- Continuous-genealogy-intensity-metrics: `Documentation/v15cy_continuous_genealogy_intensity_metric_scores.csv`
- Continuous-genealogy-intensity-scope-summary: `Documentation/v15cy_continuous_genealogy_intensity_scope_summary.csv`
- Continuous-genealogy-intensity-top-metrics: `Documentation/v15cy_continuous_genealogy_intensity_top_metrics.csv`
- Continuous-genealogy-intensity-diagnosis: `Documentation/v15cy_continuous_genealogy_intensity_diagnosis.csv`
- Continuous-genealogy-intensity-anbefaling: `Documentation/v0_15cy_operativ_anbefaling.md`
- Continuous-genealogy-intensity-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cy.md`
- Pre-registered-continuous-intensity-holdout-script: `relational_universe_v15cz_pre_registered_continuous_intensity_holdout.py`
- Pre-registered-continuous-intensity-holdout-rapport: `Documentation/v15cz_pre_registered_continuous_intensity_holdout.md`
- Pre-registered-continuous-intensity-holdout-score-spec: `Documentation/v15cz_pre_registered_continuous_intensity_holdout_score_spec.csv`
- Pre-registered-continuous-intensity-holdout-calibration: `Documentation/v15cz_pre_registered_continuous_intensity_holdout_calibration_manifest.csv`
- Pre-registered-continuous-intensity-holdout-target: `Documentation/v15cz_pre_registered_continuous_intensity_holdout_target_summary.csv`
- Pre-registered-continuous-intensity-holdout-components: `Documentation/v15cz_pre_registered_continuous_intensity_holdout_component_trajectories.csv`
- Pre-registered-continuous-intensity-holdout-events: `Documentation/v15cz_pre_registered_continuous_intensity_holdout_event_log.csv`
- Pre-registered-continuous-intensity-holdout-blind-scores: `Documentation/v15cz_pre_registered_continuous_intensity_holdout_blind_scores.csv`
- Pre-registered-continuous-intensity-holdout-runs: `Documentation/v15cz_pre_registered_continuous_intensity_holdout_runs.csv`
- Pre-registered-continuous-intensity-holdout-metrics: `Documentation/v15cz_pre_registered_continuous_intensity_holdout_metric_scores.csv`
- Pre-registered-continuous-intensity-holdout-scope-summary: `Documentation/v15cz_pre_registered_continuous_intensity_holdout_scope_summary.csv`
- Pre-registered-continuous-intensity-holdout-diagnosis: `Documentation/v15cz_pre_registered_continuous_intensity_holdout_diagnosis.csv`
- Pre-registered-continuous-intensity-holdout-anbefaling: `Documentation/v0_15cz_operativ_anbefaling.md`
- Pre-registered-continuous-intensity-holdout-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cz.md`
- Frozen-intensity-placement-contrast-script: `relational_universe_v15da_frozen_intensity_placement_contrast.py`
- Frozen-intensity-placement-contrast-rapport: `Documentation/v15da_frozen_intensity_placement_contrast.md`
- Frozen-intensity-placement-contrast-target: `Documentation/v15da_frozen_intensity_placement_contrast_target_summary.csv`
- Frozen-intensity-placement-contrast-components: `Documentation/v15da_frozen_intensity_placement_contrast_component_trajectories.csv`
- Frozen-intensity-placement-contrast-events: `Documentation/v15da_frozen_intensity_placement_contrast_event_log.csv`
- Frozen-intensity-placement-contrast-blind-scores: `Documentation/v15da_frozen_intensity_placement_contrast_blind_scores.csv`
- Frozen-intensity-placement-contrast-runs: `Documentation/v15da_frozen_intensity_placement_contrast_runs.csv`
- Frozen-intensity-placement-contrast-placement-summary: `Documentation/v15da_frozen_intensity_placement_contrast_placement_summary.csv`
- Frozen-intensity-placement-contrast-matched-seeds: `Documentation/v15da_frozen_intensity_placement_contrast_matched_seed_compare.csv`
- Frozen-intensity-placement-contrast-metrics: `Documentation/v15da_frozen_intensity_placement_contrast_metric_scores.csv`
- Frozen-intensity-placement-contrast-scope-summary: `Documentation/v15da_frozen_intensity_placement_contrast_scope_summary.csv`
- Frozen-intensity-placement-contrast-diagnosis: `Documentation/v15da_frozen_intensity_placement_contrast_diagnosis.csv`
- Frozen-intensity-placement-contrast-advisor-notes: `Documentation/v15da_advisor_panel_notes.csv`
- Frozen-intensity-placement-contrast-anbefaling: `Documentation/v0_15da_operativ_anbefaling.md`
- Frozen-intensity-placement-contrast-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15da.md`
- Routing-phase-observable-synthesis-script: `relational_universe_v15db_routing_phase_observable_synthesis.py`
- Routing-phase-observable-synthesis-rapport: `Documentation/v15db_routing_phase_observable_synthesis.md`
- Routing-phase-observable-synthesis-run-features: `Documentation/v15db_routing_phase_run_features.csv`
- Routing-phase-observable-synthesis-group-summary: `Documentation/v15db_routing_phase_group_summary.csv`
- Routing-phase-observable-synthesis-metrics: `Documentation/v15db_routing_phase_metric_scores.csv`
- Routing-phase-observable-synthesis-false-positive-cases: `Documentation/v15db_routing_phase_false_positive_cases.csv`
- Routing-phase-observable-synthesis-diagnosis: `Documentation/v15db_routing_phase_diagnosis.csv`
- Routing-phase-observable-synthesis-anbefaling: `Documentation/v0_15db_operativ_anbefaling.md`
- Routing-phase-observable-synthesis-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15db.md`
- Pre-horizon-routing-precursor-script: `relational_universe_v15dc_pre_horizon_routing_precursor_lab.py`
- Pre-horizon-routing-precursor-rapport: `Documentation/v15dc_pre_horizon_routing_precursor.md`
- Pre-horizon-routing-precursor-run-features: `Documentation/v15dc_pre_horizon_run_features.csv`
- Pre-horizon-routing-precursor-group-summary: `Documentation/v15dc_pre_horizon_group_summary.csv`
- Pre-horizon-routing-precursor-metrics: `Documentation/v15dc_pre_horizon_metric_scores.csv`
- Pre-horizon-routing-precursor-false-positive-cases: `Documentation/v15dc_pre_horizon_false_positive_cases.csv`
- Pre-horizon-routing-precursor-diagnosis: `Documentation/v15dc_pre_horizon_diagnosis.csv`
- Pre-horizon-routing-precursor-anbefaling: `Documentation/v0_15dc_operativ_anbefaling.md`
- Pre-horizon-routing-precursor-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dc.md`
- Direct-route-entry-retention-script: `relational_universe_v15dd_direct_route_entry_retention_lab.py`
- Direct-route-entry-retention-rapport: `Documentation/v15dd_direct_route_entry_retention.md`
- Direct-route-entry-retention-target: `Documentation/v15dd_direct_route_target_summary.csv`
- Direct-route-entry-retention-snapshot-log: `Documentation/v15dd_direct_route_snapshot_log.csv`
- Direct-route-entry-retention-run-summary: `Documentation/v15dd_direct_route_run_summary.csv`
- Direct-route-entry-retention-group-summary: `Documentation/v15dd_direct_route_group_summary.csv`
- Direct-route-entry-retention-label-crosstab: `Documentation/v15dd_direct_route_label_crosstab.csv`
- Direct-route-entry-retention-metrics: `Documentation/v15dd_direct_route_metric_scores.csv`
- Direct-route-entry-retention-diagnosis: `Documentation/v15dd_direct_route_diagnosis.csv`
- Direct-route-entry-retention-anbefaling: `Documentation/v0_15dd_operativ_anbefaling.md`
- Direct-route-entry-retention-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dd.md`
- Pre-entry-feature-synthesis-script: `relational_universe_v15de_pre_entry_feature_synthesis.py`
- Pre-entry-feature-synthesis-rapport: `Documentation/v15de_pre_entry_feature_synthesis.md`
- Pre-entry-feature-synthesis-run-features: `Documentation/v15de_pre_entry_run_features.csv`
- Pre-entry-feature-synthesis-metrics: `Documentation/v15de_pre_entry_metric_scores.csv`
- Pre-entry-feature-synthesis-window-summary: `Documentation/v15de_pre_entry_window_summary.csv`
- Pre-entry-feature-synthesis-diagnosis: `Documentation/v15de_pre_entry_diagnosis.csv`
- Pre-entry-feature-synthesis-anbefaling: `Documentation/v0_15de_operativ_anbefaling.md`
- Pre-entry-feature-synthesis-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15de.md`
- Pre-entry-support-topology-synthesis-script: `relational_universe_v15df_pre_entry_support_topology_synthesis.py`
- Pre-entry-support-topology-synthesis-rapport: `Documentation/v15df_pre_entry_support_topology_synthesis.md`
- Pre-entry-support-topology-synthesis-run-features: `Documentation/v15df_pre_entry_support_topology_run_features.csv`
- Pre-entry-support-topology-synthesis-family-summary: `Documentation/v15df_pre_entry_support_topology_family_summary.csv`
- Pre-entry-support-topology-synthesis-group-summary: `Documentation/v15df_pre_entry_support_topology_group_summary.csv`
- Pre-entry-support-topology-synthesis-metrics: `Documentation/v15df_pre_entry_support_topology_metric_scores.csv`
- Pre-entry-support-topology-synthesis-diagnosis: `Documentation/v15df_pre_entry_support_topology_diagnosis.csv`
- Pre-entry-support-topology-synthesis-anbefaling: `Documentation/v0_15df_operativ_anbefaling.md`
- Pre-entry-support-topology-synthesis-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15df.md`
- Boundary-mass-holdout-script: `relational_universe_v15dg_boundary_mass_holdout.py`
- Boundary-mass-holdout-rapport: `Documentation/v15dg_boundary_mass_holdout.md`
- Boundary-mass-holdout-target: `Documentation/v15dg_boundary_mass_target_summary.csv`
- Boundary-mass-holdout-components: `Documentation/v15dg_boundary_mass_component_trajectories.csv`
- Boundary-mass-holdout-events: `Documentation/v15dg_boundary_mass_event_log.csv`
- Boundary-mass-holdout-blind-scores: `Documentation/v15dg_boundary_mass_blind_scores.csv`
- Boundary-mass-holdout-run-features: `Documentation/v15dg_boundary_mass_run_features.csv`
- Boundary-mass-holdout-groups: `Documentation/v15dg_boundary_mass_group_summary.csv`
- Boundary-mass-holdout-matched-seeds: `Documentation/v15dg_boundary_mass_matched_seed_compare.csv`
- Boundary-mass-holdout-metrics: `Documentation/v15dg_boundary_mass_metric_scores.csv`
- Boundary-mass-holdout-diagnosis: `Documentation/v15dg_boundary_mass_diagnosis.csv`
- Boundary-mass-holdout-anbefaling: `Documentation/v0_15dg_operativ_anbefaling.md`
- Boundary-mass-holdout-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dg.md`
- Boundary-mass-growth-seed-holdout-script: `relational_universe_v15dh_boundary_mass_growth_seed_holdout.py`
- Boundary-mass-growth-seed-holdout-rapport: `Documentation/v15dh_boundary_mass_growth_seed_holdout.md`
- Boundary-mass-growth-seed-holdout-target: `Documentation/v15dh_boundary_mass_target_summary.csv`
- Boundary-mass-growth-seed-holdout-components: `Documentation/v15dh_boundary_mass_component_trajectories.csv`
- Boundary-mass-growth-seed-holdout-events: `Documentation/v15dh_boundary_mass_event_log.csv`
- Boundary-mass-growth-seed-holdout-blind-scores: `Documentation/v15dh_boundary_mass_blind_scores.csv`
- Boundary-mass-growth-seed-holdout-run-features: `Documentation/v15dh_boundary_mass_run_features.csv`
- Boundary-mass-growth-seed-holdout-groups: `Documentation/v15dh_boundary_mass_group_summary.csv`
- Boundary-mass-growth-seed-holdout-matched-seeds: `Documentation/v15dh_boundary_mass_matched_seed_compare.csv`
- Boundary-mass-growth-seed-holdout-metrics: `Documentation/v15dh_boundary_mass_metric_scores.csv`
- Boundary-mass-growth-seed-holdout-diagnosis: `Documentation/v15dh_boundary_mass_diagnosis.csv`
- Boundary-mass-growth-seed-holdout-anbefaling: `Documentation/v0_15dh_operativ_anbefaling.md`
- Boundary-mass-growth-seed-holdout-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dh.md`
- Growth-seed-signature-synthesis-script: `relational_universe_v15di_growth_seed_signature_synthesis.py`
- Growth-seed-signature-synthesis-rapport: `Documentation/v15di_growth_seed_signature_synthesis.md`
- Growth-seed-signature-synthesis-placement-summary: `Documentation/v15di_growth_seed_placement_summary.csv`
- Growth-seed-signature-synthesis-support-delta: `Documentation/v15di_growth_seed_support_delta.csv`
- Growth-seed-signature-synthesis-outcome-matrix: `Documentation/v15di_growth_seed_outcome_matrix.csv`
- Growth-seed-signature-synthesis-metric-audit: `Documentation/v15di_growth_seed_metric_audit.csv`
- Growth-seed-signature-synthesis-diagnosis: `Documentation/v15di_growth_seed_diagnosis.csv`
- Growth-seed-signature-synthesis-anbefaling: `Documentation/v0_15di_operativ_anbefaling.md`
- Growth-seed-signature-synthesis-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15di.md`
- Support-conditioned-pre-run-audit-script: `relational_universe_v15dj_support_conditioned_pre_run_audit.py`
- Support-conditioned-pre-run-audit-rapport: `Documentation/v15dj_support_conditioned_pre_run_audit.md`
- Support-conditioned-pre-run-audit-placement-features: `Documentation/v15dj_support_conditioned_placement_features.csv`
- Support-conditioned-pre-run-audit-rule-predictions: `Documentation/v15dj_support_conditioned_rule_predictions.csv`
- Support-conditioned-pre-run-audit-rule-scores: `Documentation/v15dj_support_conditioned_rule_scores.csv`
- Support-conditioned-pre-run-audit-diagnosis: `Documentation/v15dj_support_conditioned_diagnosis.csv`
- Support-conditioned-pre-run-audit-anbefaling: `Documentation/v0_15dj_operativ_anbefaling.md`
- Support-conditioned-pre-run-audit-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dj.md`
- Pre-registered-support-rank-holdout-script: `relational_universe_v15dk_pre_registered_support_rank_holdout.py`
- Pre-registered-support-rank-holdout-rapport: `Documentation/v15dk_pre_registered_support_rank_holdout.md`
- Pre-registered-support-rank-holdout-target: `Documentation/v15dk_support_rank_target_summary.csv`
- Pre-registered-support-rank-holdout-pre-run-ranking: `Documentation/v15dk_support_rank_pre_run_ranking.csv`
- Pre-registered-support-rank-holdout-components: `Documentation/v15dk_support_rank_component_trajectories.csv`
- Pre-registered-support-rank-holdout-events: `Documentation/v15dk_support_rank_event_log.csv`
- Pre-registered-support-rank-holdout-blind-scores: `Documentation/v15dk_support_rank_blind_scores.csv`
- Pre-registered-support-rank-holdout-run-features: `Documentation/v15dk_support_rank_run_features.csv`
- Pre-registered-support-rank-holdout-placement-summary: `Documentation/v15dk_support_rank_placement_summary.csv`
- Pre-registered-support-rank-holdout-evaluation: `Documentation/v15dk_support_rank_evaluation.csv`
- Pre-registered-support-rank-holdout-groups: `Documentation/v15dk_support_rank_group_summary.csv`
- Pre-registered-support-rank-holdout-matched-seeds: `Documentation/v15dk_support_rank_matched_seed_compare.csv`
- Pre-registered-support-rank-holdout-metrics: `Documentation/v15dk_support_rank_metric_scores.csv`
- Pre-registered-support-rank-holdout-diagnosis: `Documentation/v15dk_support_rank_diagnosis.csv`
- Pre-registered-support-rank-holdout-anbefaling: `Documentation/v0_15dk_operativ_anbefaling.md`
- Pre-registered-support-rank-holdout-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dk.md`
- Base-landscape-morphology-synthesis-script: `relational_universe_v15dl_base_landscape_morphology_synthesis.py`
- Base-landscape-morphology-synthesis-rapport: `Documentation/v15dl_base_landscape_morphology_synthesis.md`
- Base-landscape-morphology-synthesis-target: `Documentation/v15dl_base_landscape_target_summary.csv`
- Base-landscape-morphology-synthesis-morphology: `Documentation/v15dl_base_landscape_morphology_features.csv`
- Base-landscape-morphology-synthesis-placement-summary: `Documentation/v15dl_base_landscape_placement_summary.csv`
- Base-landscape-morphology-synthesis-seed-summary: `Documentation/v15dl_base_landscape_seed_summary.csv`
- Base-landscape-morphology-synthesis-metric-scores: `Documentation/v15dl_base_landscape_metric_scores.csv`
- Base-landscape-morphology-synthesis-rule-scores: `Documentation/v15dl_base_landscape_rule_scores.csv`
- Base-landscape-morphology-synthesis-diagnosis: `Documentation/v15dl_base_landscape_diagnosis.csv`
- Base-landscape-morphology-synthesis-anbefaling: `Documentation/v0_15dl_operativ_anbefaling.md`
- Base-landscape-morphology-synthesis-for-ikke-spesialister: `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dl.md`
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

`v15bd`, `v15be`, `v15bf`, `v15bg`, `v15bh`, `v15bi`, `v15bj`, `v15bk`, `v15bl`, `v15bm`, `v15bn`, `v15bo`, `v15bp`, `v15bq`, `v15br`, `v15bs`, `v15bt`, `v15bu`, `v15bv`, `v15bw`, `v15bx`, `v15by`, `v15bz`, `v15ca`, `v15cb`, `v15cc`, `v15cd`, `v15ce`, `v15cf`, `v15cg`, `v15ch`, `v15ci`, `v15cj`, `v15ck`, `v15cl`, `v15cm`, `v15cn`, `v15co`, `v15cp`, `v15cq`, `v15cr`, `v15cs`, `v15ct`, `v15cu`, `v15cv`, `v15cw`, `v15cx`, `v15cy`, `v15cz`, `v15da` og `v15db` skjerpet local_swap-/conditional-quasi-/add_chord-scale-/heuristikk-sporet uten a aapne nye brede scans:

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
- `v15bm` tester akkurat denne lesningen pa friske holdout-seeds mot naerliggende kontroller
- holdouten bekrefter ikke en ren carrier-first splittelse
- bade vinnerne og de naerliggende kontrollene holder spectral rank 1 i denne lille holdouten
- dermed maa `v15bl` fortsatt leses som familiespesifikk sharpening, ikke som en ren cross-family-lov
- `v15bn` holder seg innen den sterkeste add_chord-familien og tester om `48/p2` har en liten slektning ved `96`
- beste 96-kandidat blir `p3`, men bare som `small_scale_jump_match_weak`
- `96/p3` holder spectral rank `1`, men combined-distance-gapet til `96/p1` er bare `0.019`
- `v15bo` tar den riktige tie-break-holdouten pa friske seeds
- der taper `96/p3` mot `96/p1` pa combined coarse+spectral-likhet til `48/p2`
- `96/p3` beholder spectral rank `1`, men glipper for mye pa coarse geometri
- `96/p1` holder coarse geometri bedre, men mister spectral-rangen
- `v15bp` forklarer dermed skalabruddet som en delt breaking
- `96/p3` leses best som `spectral_without_geometry_hold`
- `96/p1` leses best som `geometry_without_spectral_hold`
- `v15bq` tester om en rikere add_chord-coarse-geometri kan redde den samme lille scale-transfer-hypotesen
- shell-dynamikk og shell-topologi redder den ikke
- `96/p3` taper ogsa mot `96/p1` pa alternativ coarse-geometri, med `alt-gap = -0.100`
- dermed holder ikke akkurat denne add_chord-skalaovergangen selv nar vi bytter coarse observabel
- `v15br` pivoter deretter til `local_swap` og tester om `low_load_diffuse` holder pa friske seeds som bade modus og spectral lomme
- denne holdouten holder rent
- `p1` forblir `buffered_heavy_load`
- `p2` forblir `rare_load_risk`
- `p3` forblir `low_load_diffuse`
- alle tre holder spectral rank `1`, men `p3` holder samtidig den forventede modusen og dermed den beste kombinasjonen av mode + spectral pocket
- `v15bs` sammenlikner deretter add_chord og local_swap direkte pa samme `96/p3`-locus
- denne sammenlikningen blir blandet
- add_chord holder litt sterkere coarse return og litt sterkere kjerneandel
- local_swap holder litt lavere spectral drift og litt bedre dim-minus-spectral-margin
- men alle gapene er sma, og ingen ren delt arbeidsdeling holder ved akkurat samme locus
- `v15bt` prover sa en timingobservabel pa samme `96/p3`-duell
- heller ikke timingteksturen splitter carrierne rent
- begge gar tidlig inn i fragment-lock
- add_chord er bare litt oftere `anchored_early_fragment_lock`, mens local_swap bare litt oftere er `looser_early_fragment_lock`
- `v15bu` prover deretter en helt ny observabelklasse: occupancy-spekteret i halen
- heller ikke denne splitter carrierne rent ved samme locus
- haleunion, entropi og top-k-masseandeler er nesten like
- diagnosen ender pa `pause_same_locus_duels`
- `v15bv` forlater derfor samme-locus-duellen og leter etter familiestruktur pa target `96`, growth_seed `202`, placements `0..3`, for bade `add_chord` og `local_swap`
- artifact-control holder rent
- seks av atte profiler faller i en bred `geometry_core_family`
- `add_chord_p1` skiller seg ut som `expanded_shell_family`
- `local_swap_p3` skiller seg ut som `spectral_core_family`
- det finnes support-only og carrier-only near-symmetry-kandidater, men ingen par er naere i bade support- og carrier-feature-rom
- diagnosen ender pa `family_structure_without_symmetry_supported`, med eksplisitt forbehold om at symmetri her bare betyr feature-level near-symmetry, ikke automorfi eller fysisk symmetri
- `v15bw` holder ut denne target-96 family-map-en pa friske seeds
- holdouten replikerer ikke family-map-en rent: match-rate `0.375`, geometry-core-retention `0.500`, outlier-retention `0.000`
- den observerte target-96-strukturen flytter seg til `add_chord_p1`, `add_chord_p2`, `local_swap_p1`, `local_swap_p2`, `local_swap_p3` som geometry-core-medlemmer
- det finnes to full feature-level near-symmetry-kandidater i holdouten, men de redder ikke family-map-en
- diagnosen ender pa `family_structure_not_replicated`, og peker mot nytt skalahopp heller enn mer target-96 terskelfiksing
- `v15bx` tar derfor et smalt skalahopp til target `192`, samme growth_seed `202`, samme placements `0..3`, samme perturbasjoner og samme observabler
- target `192` gir et nytt, mer interessant plateau: seks av atte profiler faller i `spectral_diffuse_rare_family`
- begge p2-profiler (`add_chord_p2`, `local_swap_p2`) blir `mixed_family`, altsa skiller p2 seg ut pa tvers av perturbasjonstype
- det finnes ingen full support+carrier near-symmetry-kandidater ved target `192`, bare support-only naerhet
- diagnosen ender pa `scale_jump_family_plateau_supported`
- `v15by` holder ut target-192 plateauet pa friske seeds
- eksakt `v15bx`-map holder bare delvis: match-rate `0.625`
- forventet plateau-retention er `0.833`, mens p2-outlier-retention er `0.000`
- observert plateau er bredere enn forventet: syv av atte profiler blir `spectral_diffuse_rare_family`
- `local_swap_p1` faller ut som `mixed_family`, mens begge p2-profiler ikke lenger holder som `mixed_family`
- det finnes ett full feature-level near-symmetry-par i holdouten (`add_chord_p3` / `local_swap_p3`)
- diagnosen ender pa `target192_plateau_weak_holdout`
- `v15bz` hopper videre til target `384` med samme family-observabler
- target `384` gir repeterte family-labels og to full feature-level near-symmetry-kandidater
- `spectral_diffuse_rare_family` holder fire profiler
- `rare_diffuse_family` samler begge p2-profiler
- `add_chord_p3` blir `spectral_core_family`, mens `local_swap_p1` blir `mixed_family`
- diagnosen ender pa `target384_family_plus_symmetry_candidate`
- `v15ca` prover deretter en ny mekanismeobservabel ved target `192`: radial occupancy rundt support for p1/p2-grensen
- etter korrigert avstandsmaaling holder artifact-control fortsatt rent
- p2 ser ikke mer radialt diffus ut enn p1 pa en ren og konsistent mate
- shell4plus og rare-masse peker faktisk ikke i retning av en ren p2-uteovergang
- diagnosen ender pa `radial_diffuse_boundary_not_yet`
- `v15cb` holder ut de konkrete target-384-kandidatene fra `v15bz`
- den strenge target-384-mappen replikerer ikke rent: match-rate `0.500`
- spectral_diffuse_rare-kvartetten holder delvis (`0.750`)
- rare_diffuse-paret holder delvis (`0.500`)
- ingen av de to full near-symmetry-kandidatene holder som full near-symmetry i holdouten
- observert quartet blir `add_chord_p0`, `add_chord_p1`, `add_chord_p2`, `local_swap_p3`
- diagnosen ender pa `target384_candidates_not_replicated`
- `v15cc` prover deretter en ny target-384-observabel: tidsopplost shell-turnover rundt support
- artifact-control holder fortsatt rent, men turnover-observabelen splitter ikke target-384-profiler rent
- quartet-majoritet blir bare `2/4`, p2-paret splitter seg selv, og quartet->p2-avstanden er ikke storre enn quartet-intern avstand
- diagnosen ender pa `turnover_structure_not_yet`
- `v15cd` tar derfor et nytt skalahopp til target `768` med samme family-/symmetry-observabler som ved `192` og `384`
- target `768` gir et langt sterkere forstesignal: sju av atte profiler faller i `rare_diffuse_family`
- `add_chord_p0` blir eneste `spectral_diffuse_rare_family`-outlier
- det finnes to full feature-level near-symmetry-kandidater: `add_chord_p1` / `add_chord_p2` og `add_chord_p2` / `local_swap_p2`
- diagnosen ender pa `target768_family_plateau_supported`
- `v15ce` holder deretter ut target-768-plateauet pa friske seeds
- holdouten holder bare delvis: match-rate `0.750`, plateau-retention `0.714`, outlier-retention `1.000`, full-near-retention `0.500`
- `add_chord_p0` holder som spectral outlier, og `add_chord_p2` / `local_swap_p2` holder som full near-symmetry-par
- men `local_swap_p0` og `local_swap_p3` glir ut av plateauet og blir `spectral_diffuse_rare_family`
- diagnosen ender pa `target768_plateau_weak_holdout`
- `v15cf` tester deretter en smal support-locus-lesning ved target `768`: bare placement `0` og `2`, bare den stabile resten fra `v15ce`
- artifact-control holder fortsatt rent
- p2 ligger riktignok lenger ute enn p0 i weighted distance, men rare/core- og occupancy-signalet er ikke konsistent nok pa tvers av carrier
- pooled p2->p0-gap gir mer outer/rare-masse, men occupancy-entropy gaar faktisk svakere feil vei og support-core-fraksjonen splitter ikke
- diagnosen ender pa `support_locus_split_not_yet`

Den riktige live-lesningen na er derfor:

- growth_seed-202-splittelsen leses best gjennom en liten dynamisk retention+kjerne-akse
- men aksen maa fortsatt leses som en to-komponentsplitt, ikke som ett enkelt universelt maal
- og de to nabogapene inne i aksen er selv asymmetriske, ikke bare svakere/sterkere versjoner av samme overgang
- den balanserte `p3 > p2`-overgangen leses na best som retention pluss rare-loaded shell-drag
- `p2` ser samtidig ut til a ha en egen lokal støtte-/last-trigger, selv om den ikke alene forklarer hele `p1/p2/p3`-rekkefolgen
- `p2` og `p1` skilles na best som høy last uten nok stabilisering vs litt lavere last med sterkere stabilisering
- `v15bl` viser samtidig at spektral relativ drift blir mer interessant hvis vi condition-er pa disse lokale carrier-familiene
- den sterkeste nye quasi-invariant-lesningen er fortsatt familiespesifikk sharpening, ikke en ny global invariant
- `v15bm` svekker ideen om at denne spektrale lommen allerede holder som en ren carrier-first cross-family-splittelse
- `v15bn` viser at det fortsatt finnes en legitim liten add_chord-skalahypotese rundt `48/p2 -> 96/p3`, men bare som svak kandidat
- `v15bo` viser at denne hypotesen ikke holder rent pa holdout mot en naer kontroll
- `v15bp` viser samtidig at dette ikke er et tomt negativt resultat: skalabruddet er strukturert og splitter mellom spectral-bevaring og coarse-geometri-bevaring
- `v15bq` gjor add_chord-neiet hardere: heller ikke shell-dynamikk/topologi gir `48/p2 -> 96/p3` en ren liten scale-bridge
- dermed bor add_chord forelopig leses som familiespesifikk spectral sharpening ved fast storrelse, ikke som beste neste skritt for carrier-geometri over skala
- dette stabiliseringsunderskuddet er ikke flatt: det er retention-led, med core som tydelig sekundarkomponent
- growth_seed-202-kartet leses na best som tre lokale modi: tung last med buffer, tung last uten nok buffer, og lavere last med diffus retur
- den sterkeste nye add_chord-lesningen er derfor fortsatt familiespesifikk spectral sharpening ved fast storrelse, ikke en liten ren scale-transfer-familie
- `v15br` styrker samtidig local_swap som neste carrier-spor for geometri-/quasi-invariant-arbeid
- den viktigste lokale lommen er na `low_load_diffuse` ved `96/p3`: den holder pa holdout som bade modus og spectral lomme
- `v15bs` viser samtidig at en ren carrier-dualitet heller ikke bor overdrives: ved samme locus er add_chord og local_swap mye naermere hverandre enn historiene deres hver for seg kunne tyde pa
- `v15bt` og `v15bu` gjor denne lesningen hardere: det er ikke bare én svak metrikk som holder same-locus-duellen tilbake
- timing og occupancy-spekter bekrefter begge at carrierne fortsatt ligger for naert hverandre ved akkurat `96/p3`
- `v15bv` gir et svakt positivt svar pa familiestruktur-sporsmalet, men `v15bw` viser at akkurat den target-96 family-map-en ikke holder rent
- `v15bx` viser derimot at skalahoppet til target `192` kan gi et mer ordnet plateau: `spectral_diffuse_rare_family` dominerer seks av atte profiler, mens p2 skiller seg ut i begge perturbasjonstyper
- `v15by` bekrefter ikke den rene p2-splittelsen, men styrker ideen om et bredt spectral/diffuse/rare-plateau ved target `192`
- `v15bz` viser at et nytt skalahopp faktisk gir ny struktur: ved target `384` dukker baade repeterte familier og to full near-symmetry-kandidater opp
- `v15ca` viser samtidig at en enkel radial occupancy-forklaring ikke loser target-192 p1/p2-grensen
- `v15cb` viser deretter at akkurat denne target-384-kandidatmappen ikke holder rent pa holdout
- `v15cc` viser at mer target-384 observabeltuning alene ikke ga ren familieseparasjon
- `v15cd` viser at target `768` er den mest lovende nye skalaen i denne observable-stakken sa langt
- `v15ce` viser samtidig at plateauet ved `768` ennå ikke holder rent nok til mekanismeforklaring pa hele kartet
- `v15cf` viser deretter at en grov support-locus-lesning heller ikke er ren nok til a forklare den stabile resten ved `768`
- `v15cg` viser deretter at en far-shell-horisont faktisk gir et svakere, men ekte p2-signal: `local_swap_p2` er sterkest, `add_chord_p2` holder delvis, og p0-kontrollene holder seg rene
- diagnosen i `v15cg` ender likevel bare pa `far_shell_horizon_weak` fordi carrier-gapet ved p2 fortsatt er for stort til en ren carrier-robust lesning
- `v15ch` holder sa ut den sterkeste resten fra `v15cg` pa friske seeds og et lite nabolag av terskler
- denne holdouten holder overraskende rent: `local_swap_p2` holder i baseline og `3/3` terskelkonfigurasjoner mot p0-kontrollen, og `add_chord_p2` holder samtidig i alle `3/3` terskelkonfigurasjoner og litt sterkere ved baseline
- diagnosen ender derfor pa `local_swap_p2_horizon_holdout_supported`, men med viktig scope-presisering: dette leses na best som en delt feature-level `p2`-kandidat pa tvers av carrier, ikke som en local_swap-spesifikk anomalitet og ikke som en partikkelpaastand
- `v15ci` prover sa den mest direkte mekanikkforklaringen: outer-genealogi i halen
- den gir et nyttig negativt svar: alle fire profiler leses som `reseeded_outer_horizon`, og outer-aktivitet alene er derfor for generisk til aa forklare p2-lommen
- p2 har riktignok lavere turnover og høyere dominant mass enn p0, men ikke en ren ny mekanikk-label
- `v15cj` prover deretter outer-occupancy-konsentrasjon
- denne peker bare svakt mot p2: `local_swap_p2` er tydelig mer konsentrert enn `local_swap_p0`, men `add_chord_p2` holder ikke samme konsentrasjonsgap
- diagnosen ender pa `shared_p2_outer_concentration_weak`
- `v15ck` prover sa om ny outer-masse mates gjennom noen fa indre feeder-soner
- heller ikke denne aksen holder rent: `add_chord_p2` har lav birth-intensity og litt mer concentrated-feeder-rate enn `add_chord_p0`, mens `local_swap_p2` ser mer self-propagating ut enn mer feeder-konsentrert
- diagnosen ender pa `feeder_flux_not_yet`
- `v15cl` flytter derfor mekanismeaksen innover mot shell2/3-gate og global-budget-lignende redistribusjon
- p2-horisonten dukker fortsatt opp i denne nye seed-runden, spesielt `local_swap_p2` (`established_far_shell_rate = 0.750`) og svakere `add_chord_p2` (`0.250`)
- men shell2/3-gate skiller ikke p2 fra p0 rent: p2 har lavere pre-gate peak, lavere gate release og lavere opposite shell23/outer motion enn p0 i begge carrierne
- p2 har lavere spektral drift enn p0, men dette er ikke nok til aa kalle global-budget-kobling; diagnosen ender pa `inner_gate_not_yet` og `global_budget_coupling_not_yet`
- `v15cm` prover deretter den renere lokale triggerforklaringen: tidlig supportnaer launch, supportgeometri og downstream far-shell-horisont i samme smale target-768 oppsett
- p2-horisonten lever fortsatt (`local_swap_p2 = 0.750`, `add_chord_p2 = 0.250`), men p2 er ikke tidligere eller sterkere i tidlig launch enn p0
- konkret er p2 senere til first outer enn p0 i begge carrierne (`add_chord` gap `+512.0`, `local_swap` gap `+234.0`) og har lavere early radius slope og lavere early peak damage
- diagnosen ender derfor pa `local_trigger_not_yet` og `support_geometry_not_explanatory`
- `v15cn` holder sa p2-horisonten ut paa ett moderat skalahopp: fresh target-768 anchor pluss target `1024`, samme p0/p2-profiler og samme absolute step budget
- target-768 anchor replikerer bare delvis: `local_swap_p2` er stottet (`support_score = 5`, `established = 0.500`) mens `add_chord_p2` er svakere (`support_score = 3`)
- target `1024` stotter ikke p2-horisonten i noen carrier under samme budsjett: begge p2 established-rates er `0.000`, og support scores er `0`
- diagnosen ender pa `target768_specific_under_current_budget`, med eksplisitt budsjettforbehold: fravaer ved 1024 er ikke alene bevis mot skalaeffekt fordi tidsbudsjettet ikke er skalanormalisert
- den riktige live-lesningen na er derfor at target-768 p2-lommen er reell nok til aa beholdes, men ikke automatisk skalerbar under samme absolute step budget
- `v15co` gjor saa en beslutnings-/heuristikksyntese uten ny dynamikk
- konklusjonen er at univers-inspirerte egenskaper kan brukes som svak prioriteringsheuristikk bare etter oversettelse til repo-observabler
- beste positive akse er fortsatt defect non-superposition/genealogy; conditional spectral quasi-invariant er sekundar akse; artifact hygiene er hard gate
- Lorentz-likhet skal forelopig brukes som diagnostikk/negativt filter, globale regler som instrumentering, og entanglement-sprak er ikke tillatt utover en svak pair-non-superposition-proxy
- `v15cp` tester den minste budsjettforklaringen ved target `1024`: samme setup som `v15cn`, men step_budget skalert fra target 768 (`2560 -> 3414`)
- resultatet gjenoppliver ikke p2: begge p2-profiler ved 1024 har fortsatt `established_far_shell_rate = 0.000`, `support_score = 0` og `candidate_supported = 0`
- den eneste tydelige budsjettresponsen er motsatt av p2-hypotesen: `add_chord_p0` horizon-span oker fra `33.500` til `86.000`, mens p2 samlet horizon-span delta er `0.000`
- diagnosen blir `scaled_budget_p2_not_supported` og `p0_budget_response_without_p2`
- `v15cq` tester derfor midpoint target `896` med skalert budsjett (`2987`)
- target 896 gir ikke p2-support etter kriteriene: `add_chord_p2` har etablert aktivitet (`0.500`, horizon `49.500`), men `add_chord_p0` er like etablert og har lengre horizon (`75.000`), slik at support-score bare blir `1`
- `local_swap_p2` etableres ikke ved 896 (`established = 0.000`, horizon `0.000`, support-score `1`)
- scale-ladderen blir derfor: target 768 local_swap-p2 supported, target 896 partial/not-supported, target 1024 not-supported
- diagnosen blir `intermediate_p2_partial_not_supported`
- `v15cr` gjor saa en vurdering av neste retning uten ny dynamikk
- den anbefaler aa pensjonere p2 som primar skala-selector, men beholde p2 som target-768 lokal kontrast
- viktigste nye kandidat er `add_chord_p0_scale_response`: add_chord_p0 horizon gaar `2.000 -> 75.000 -> 86.000` over target `768 -> 896 -> 1024`
- fordi p0-signalet ble oppdaget som kontroll og bare har to seed-deltaer per target, maa neste steg vaere en fresh-seed holdout, ikke claim
- `v15cs` gjor fresh-seed holdout av p0-responsen med seed-deltaer `6203` og `6269`
- p0 holder sterkt ved target 896 (`established = 1.000`, horizon `136.000`, score `6`), men ikke ved target 1024 (`established = 0.000`, horizon `0.000`, score `0`)
- ved 1024 er `add_chord_p2` kontrollen som etablerer horizon (`established = 0.500`, horizon `82.500`)
- diagnosen blir `p0_scale_response_target_specific`, ikke scale-response-supported
- neste naturlige dynamiske steg er `replicate_or_bracket_p0_response` hvis vi vil fortsette dette sporet; alternativt er `response_fingerprint_synthesis` bedre enn mer ren label-budget
- `v15ct` tar derfor response-fingerprint-syntesen uten ny dynamikk
- syntesen klassifiserer `v15cn`/`v15cp`/`v15cq`/`v15cs` etter response-class heller enn etter p0/p2-label
- 4/6 old-vs-fresh scaled-profile-sammenligninger skifter response-class
- `p0_label_stability = not_stable` og `p2_label_stability = not_stable`
- `add_chord` har flest persistent-far-shell-observasjoner, men plassering/seed-identitet skifter
- diagnosen blir `add_chord_placement_sensitive_live`
- neste naturlige dynamiske steg er `v15cu_add_chord_placement_response_map`, ikke mer budsjett paa en enkelt p0/p2-label
- `v15cu` kjorer saa et smalt add_chord-placement-kart ved target `896/1024`
- placements `p0..p3` testes paa friske seed-deltaer `7307/7351`
- artifact-control holder rent
- ved target `896` er `p1` strong persistent og `p2` moderate persistent, mens `p0` og `p3` ikke har horizon
- ved target `1024` er `p3` dominant strong persistent (`established = 1.000`, horizon `172.000`) og `p1` er ogsaa strong persistent, mens `p0` og `p2` ikke har horizon
- p1 er dermed den eneste stabile strong placement over begge target, men beste placement skifter fra p1 til p3
- diagnosen blir `target_specific_placement_switch` og `add_chord_carrier_live`
- neste naturlige steg er `mechanism_probe_for_winning_placements`: supportgeometri og tidlig launch for p1/p3
- `v15cv` kjorer mekanismeproben for p1/p3 med samme seed-deltaer som `v15cu`
- p1-broen holder: p1 er `strong_persistent_far_shell` ved baade 896 og 1024
- p3-switchen holder: p3 er `no_horizon` ved 896 og `strong_persistent_far_shell` ved 1024
- enkel tidlig launch forklarer ikke switchen rent (`early_launch_not_sufficient`, score `0/6`)
- statisk supportgeometri forklarer heller ikke switchen rent (`support_geometry_not_sufficient`, score `0/5`)
- neste naturlige steg er `add_genealogy_to_p1_p3_seed_splits`, fordi landskapet holder men mekanismen ikke er forklart
- `v15cw` legger til komponentgenealogi og event chains for samme p1/p3-seed-scope
- landskapet reproduseres: `p1_bridge_p3_switch_reproduced`
- bare p1/1024 seed-splitten separeres rent av genealogy pattern: `birth_death_churn` gir no-horizon, mens `split_fragment` gir horizon
- `split_persistent_dual` er blandet globalt (`established_far_shell_rate = 0.500`), saa genealogy-aksen er ikke generell ennaa
- diagnosen blir `genealogy_separates_limited_seed_splits`
- neste naturlige steg er `holdout_p1_1024_genealogy_split_axis`, ikke generalisert genealogy-claim
- `v15cx` holder ut akkurat p1/1024-splitten paa friske seed-deltaer `7411/7477/7541/7603`
- den konkrete kategoriske mappingen holder ikke: alle fire holdout-runs er `split_persistent_dual`
- likevel har denne brede genealogy-intensiteten fortsatt signal: `established_far_shell_rate = 0.750`, mean horizon `126.000`, mean churn `1381.000`, mean max mass `235.250`
- diagnosen blir `p1_1024_specific_genealogy_axis_not_reproduced`
- neste naturlige steg er `build_continuous_genealogy_intensity_observable`, ikke mer grov event-chain-label-budget
- `v15cy` gjor saa den billige syntesen uten ny dynamikk
- kontinuerlig intensity-index har AUC `0.800` globalt, `0.875` for `p1/1024`, og `1.000` i v15cx holdout-only
- top-metrikker peker mot komponent-/kompresjonsintensitet: globalt `max_component_count_per_target` har AUC `0.943`, mens `p1/1024` har `compress_per_step` med AUC `1.000`
- diagnosen blir `continuous_genealogy_intensity_promising_small_n`
- neste naturlige steg er `pre_register_continuous_intensity_holdout`: frys score/top-metrikker og test paa nye dynamiske runs foer justering
- `v15cz` kjorer denne pre-registrerte holdouten paa 24 nye `1024:p1/add_chord` seed-deltaer
- score-spec er frosset fra v15cw/v15cx; holdout-scorene skrives blindt foer horizon-label/fasitering
- artifact-control holder rent, og primarscoren rangerer den ene no-horizon-runnen lavest (`AUC = 1.000`, exact p `0.043`)
- testen er likevel ikke en confirmatory selector-validering fordi decisive outcomes er sterkt ubalansert: `22 established`, `1 no_horizon`, `1 mixed`
- post-hoc-toppen `compress_per_step` fra v15cy holder ikke i denne holdouten (`AUC = 0.114`), saa enkeltmetrikk-historien maa svekkes
- diagnosen blir `pre_registered_intensity_inconclusive_balance`
- neste naturlige steg er ikke refit; enten behold v15cz som ubalansert positiv retningssjekk, eller pre-registrer en kontrast-/balanseringsrunde mot svakere/negative placements
- `v15da` kjorer raadgiverpanelets fresh placement-kontrast: `p0,p1,p2` ved `1024/add_chord`, 12 nye seed-deltaer per placement, og frossen v15cz-score uten refit
- Claude CLI var utilgjengelig (`Not logged in`), mens to remote Codex-subagenter anbefalte nettopp denne kontrast-/balanseringsrunden
- artifact-control holder rent og kontrasten er balansert nok: `11 established`, `23 no_horizon`, `1 mixed`, `1 failed`
- `p1` replikerer som sterk 1024-lomme (`10/12 established`, mean horizon `144.417`)
- `p2` blir ren negativ kontroll (`12/12 no_horizon`, mean horizon `0.000`)
- `p0` blir den viktige falsk-positive kontrollen: `10/12 no_horizon`, men mean frozen score `0.618`, nesten like hoyt som p1 `0.678`
- frozen `genealogy_intensity_index` feiler derfor som selector under kriteriene: AUC `0.711`, exact rank-DP p `0.025`, median delta `0.282`
- diagnosen blir `frozen_intensity_placement_contrast_failed`
- neste naturlige steg er aa nedgradere genealogy-intensity til deskriptiv observabel og lete etter hva som skiller p0 false-positive intensity fra p1 horizon
- `v15db` gjor den billige no-new-dynamics-syntesen av v15da for routing/phase-observabler
- downstream routing skiller rent: `tail_route_index` og `entry_timing_index` har AUC `1.000` for p1 established vs p0 high-score no-horizon
- men beste early/pre-entry kandidat er svakere: `component_early_far8_mass_fraction` har AUC `0.720` for p1-vs-p0-false-positive og `0.783` for established-vs-no
- p0 false positives har median intensity `0.816` mot p1 established `0.768`, men tail_route `0.317` mot `0.898`
- diagnosen blir `downstream_routing_separates_but_not_pre_entry`
- `v15dc` sensurerer pre-horizon-komponentproxyer foer `first_high_step` og finner bare svakt/moderat signal
- beste censored feature er `pre_far8_slope_per_100` med AUC `0.780` for p1 established vs p0 high-score no-horizon og `0.794` for established vs no-horizon
- `pre_route_coherence_index` er svakere (`0.620` mot p0 false positives), mens baseline genealogy-intensity fortsatt feiler (`0.280`)
- diagnosen blir `pre_horizon_route_precursor_weak`
- `v15dd` rerunner samme v15da-scope med direkte per-snapshot route-entry/retention logging
- p1 established blir `sustained_high_retention:10`, mens p0 high-score no-horizon blir `outer_pressure_no_high_entry:5`
- median retention er p1 `0.978` mot p0 false-positive `0.000`; median outer-pressure-without-high er p1 `0.088` mot p0 false-positive `0.937`
- direct-route-metrikker skiller rent (`first_sustained_high3_earliness`, `direct_retention_rate_after_entry`, `last12_high_rate_direct`, `sustained_high3_rate`, `direct_high_rate` alle AUC `1.000` for p1-vs-p0 false-positive)
- diagnosen blir `direct_route_entry_retention_separates_false_positives`, men dette er mekanistisk instrumentering og ikke en pre-entry selector
- `v15de` gjor den billige no-new-dynamics-syntesen av `v15dd_direct_route_snapshot_log.csv`
- lekkasjevakten er konkret: tidligste p1-established sustained high3-entry er step `104`, saa vinduer `<=96` behandles som strict pre-entry
- strict pre-entry route-features feiler som selector: beste strict feature er `w96_mean_outer_share`, AUC `0.560` for p1-vs-p0-false-positive og `0.617` for established-vs-no
- senere entry-risk vinduer blir bedre (`w640_ready_both_rate` AUC `0.800` mot p0 false positives), men er for naer entry/outcome til aa brukes som claim
- baseline genealogy-intensity forblir misvisende som selector i denne kontrasten (`AUC = 0.280`)
- diagnosen blir `pre_entry_feature_not_found`
- `v15df` tester derfor en ikke-route strict pre-entry observabelsyntese paa v15da-komponentbaner og v15dd-labels
- route-entry/retention brukes ikke som kandidatfeatures; features er statisk supportgeometri og komponent/topologi/support-distance ved steps `<=32/64/96`
- beste strict dynamiske ikke-route metric er `w32_mean_boundary_per_mass`, med AUC `0.960` for p1-vs-p0-false-positive og `0.864` for established-vs-no
- statisk `static_mean_support_degree` skiller enda renere (`AUC = 1.000` mot p0 false positives), men dette er placement-level support-informasjon og skal behandles som confound/audit, ikke dynamisk selector
- baseline genealogy-intensity forblir misvisende som selector (`AUC = 0.280` mot p0 false positives)
- diagnosen blir `pre_entry_support_topology_promising`
- `v15dg` fryser `w32_mean_boundary_per_mass` og tester den paa 8 nye seed-deltaer for `1024/add_chord/p0,p1,p2`
- artifact-control er clean og labelbalansen er brukbar: `7 established`, `15 no_horizon`, `2 mixed`, med `p1-established = 7` og `p0 high-score/no-horizon = 8`
- primarmetric overlever fresh holdout: AUC `0.821` mot p0 false positives, AUC `0.857` established-vs-no, median p1-p0false delta `2.375`
- static audit er fortsatt sterkere/perfekt: `static_mean_support_degree` har AUC `1.000` mot p0 false positives, saa placement/support-confound er live og maa rapporteres separat
- baseline genealogy-intensity er svakere mot p0 false positives (`AUC = 0.679`)
- diagnosen blir `boundary_mass_holdout_supported`
- `v15dh` tester samme frosne metric paa growth seed `303`, samme target `1024`, samme `add_chord/p0,p1,p2`, og 8 nye seed-deltaer
- artifact-control er clean, men placement-landskapet skifter: `p1` er `8/8 no_horizon`, mens `p0` har `4 established` og `p2` har `4 established`
- `w32_mean_boundary_per_mass` transferer ikke under original p1-anchor: AUC `0.463` established-vs-no
- `static_mean_support_degree` transferer heller ikke som selector-retning (`AUC = 0.217` established-vs-no)
- baseline genealogy-intensity korrelerer overall paa seed-303 (`AUC = 0.858`), men er ikke primary og skal ikke refittes til claim
- diagnosen blir `boundary_mass_not_growth_seed_transferable_under_original_anchor`
- `v15di` sammenligner v15dg/v15dh uten ny dynamikk
- placement-landskapet er ikke growth-seed-stabilt: p1 established-rate `0.875 -> 0.000`, p0 `0.000 -> 0.500`, p2 `0.000 -> 0.500`
- support-signaturene skifter samtidig: p1 `1,58,537 -> 12,13,22`, p0 `13,72,343 -> 3,4,827`, p2 `6,8,9 -> 25,177,430`
- boundary/mass er seed-conditioned, ikke generalisert selector: AUC `0.857` paa seed 202, `0.463` paa seed 303, `0.563` samlet
- statisk supportretning er heller ikke universell: `static_mean_support_degree` AUC `0.967 -> 0.217`
- diagnosen blir `condition_on_base_support_before_more_dynamics`
- `v15dj` bygger denne billige support-/base-kondisjonerte pre-run audit-en uten ny dynamikk
- beste enkle scout-klasse er `low local support volume/gap`: `low_ball2_minus_ball1`, `low_ball3_minus_ball1`, `low_ball3_minus_ball2`, `low_static_support_ball_2` og `low_static_support_ball_3` har alle `top1_hit_rate = 1.000` over de to kjente growth seeds
- scout-klassen er ikke validert selector: total top1-capture er bare `2/3` aktive placements (`0.667`), fordi seed-303 har baade p0 og p2 aktive mens low-volume-reglene typisk peker paa p2
- diagnosen blir `found_sparse_candidate` + `not_validated`
- `v15dk` tester denne scout-klassen paa fresh growth seed `404` med pre-run ranking skrevet foer dynamikk
- pre-run top1/top2 er `p0/p2`, men dynamikken gjor `p1` til eneste aktive placement: p0 `8/8 no_horizon`, p2 `8/8 no_horizon`, p1 `4 established;1 mixed;3 no_horizon`
- top1/top2 capture er `0.000`, og support-rank-resultatet blir `support_rank_not_supported`
- boundary/mass er svak som audit (`w32_mean_boundary_per_mass` AUC `0.526` established-vs-no)
- `v15dl` er den no-new-dynamics skala-/landskapsanalysen: den samler seeds `202/303/404`, legger til basegraf-morfologi og add_chord-probe-observabler, og finner `base_conditioned_placement_landscape`
- aktivt landskap er seed-betinget: seed 202 `p1`, seed 303 `p0;p2`, seed 404 `p1`
- beste nye pre-run morfologiscreen er `delta_return_t2`/high, med post-hoc placement-level AUC `0.900`, men regelen er bare `weak_posthoc_top2_scout` (`top1_capture=0.750`, `top2_capture=0.750`)
- neste naturlige steg, hvis vi vil bruke mer dynamisk budsjett, er en liten v15dm-holdout der `delta_return_t2`/high fryses foer dynamikk; alternativt maa vi fortsette observabeldesign/nullmodell uten selector-claim

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
