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

Per dagens lokale state er `v11e` den siste frontier-avklaringen. `v12`, `v12b`, `v12c`, `v12d`, `v12e`, `v12f`, `v12g`, `v12h`, `v12i`, `v12j`, `v12k`, `v12l`, `v12m` og `v12n` er de aktive struktur-/transfer-rundene bygget pa den.

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

## Viktige signaler fra v12 / v12b / v12c / v12d / v12e / v12f / v12g / v12h / v12i / v12j / v12k / v12l / v12m / v12n

`v12`, `v12b`, `v12c`, `v12d`, `v12e`, `v12f`, `v12g`, `v12h`, `v12i`, `v12j`, `v12k`, `v12l`, `v12m` og `v12n` er ikke nye frontier-runder. De fryser `band_zero_del` og ser etter enklere struktur.

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
