# PROJECT_HISTORY_INDEX

Dette er en komprimert historikk over de viktigste metodiske vendepunktene frem til dagens live state.

## 1. Generatorproblemet ble eksplisitt

Tidlige stor-skala-runder viste at nominelle storrelser ikke alltid ble realisert som faktisk storre startensembler.
Det betydde at asymptotiske tolkninger kunne vaere generatorartefakter i stedet for fysikk.

Viktige filer:

- `relational_universe_v10b_ensemble_calibration.py`
- `Documentation/v0_10b_operativ_anbefaling.md`

## 2. Kalibrert skalarerun ble etablert

Etter generatorrensingen ble fokus flyttet til kalibrerte ensembler og reelt separerte startstorrelser.
Dette ga et mye tryggere grunnlag for videre frontier-tolkning.

Viktige filer:

- `relational_universe_v10d_calibrated_scale_collapse.py`
- `Documentation/v10d_calibrated_scale_candidate_summary.csv`
- `Documentation/v10d_calibrated_scale_size_profiles.csv`

## 3. Focused band-validering innsnevret fronten

Band-familien ble testet mer direkte, og spenningen mellom raw score og focused-score ble tydeligere.
Her ble det klart at raw dynamikk og focused-score ikke automatisk peker mot samme kandidat.

Viktige filer:

- `relational_universe_v10e_focused_band_validation.py`
- `Documentation/v10e_focused_band_candidate_summary.csv`
- `Documentation/v10e_focused_band_pairwise.csv`
- `Documentation/v10e_focused_band_size_profiles.csv`

## 4. v10f ga siste sikre band-baseline

I `v10f` var:

- raw-vinner: `band_zero_del`
- focused-vinner: `frontier_triad_only`

Dette er siste sikre baseline før bridge-korridoren ble lokal frontier.

Viktige filer:

- `relational_universe_v10f_frontier_test.py`
- `Documentation/v10f_frontier_final_candidate_summary.csv`
- `Documentation/v10f_frontier_final_pairwise.csv`
- `Documentation/v10f_frontier_final_size_profiles.csv`
- `Documentation/relasjonell_universgraf_v0_10f_frontier_runde.md`

## 5. Bridge-korridoren dukket opp

I den mellomtunge `v11`-kjeden flyttet raw-fronten seg bort fra ren band-korridor og over mot bridge-varianter.
Dette var det forste tydelige tegnet pa at den operative fronten ikke lenger bare handlet om `band_zero_del`.

Viktige filer:

- `Documentation/v11_mid_focus_frontier_resolution_final_candidate_summary.csv`
- `Documentation/v11_mid_focus_frontier_resolution_final_pairwise.csv`

## 6. v11b snevret inn, men løste ikke fronten rent

`v11b` bygget en smal bridge-korridor rundt `bridge_0015_0000`.
Der fikk vi en ekte mellomkonklusjon:

- `bridge_0015_0000` sa sterk ut pa noen operative mal
- `band_zero_del` beholdt styrke pa andre
- dommen var fortsatt `uavklart`

Viktige filer:

- `relational_universe_v11b_bridge_resolution.py`
- `Documentation/v11b_bridge_resolution.md`
- `Documentation/v11b_bridge_resolution_final_candidate_summary.csv`
- `Documentation/v11b_bridge_resolution_final_pairwise.csv`
- `Documentation/v0_11b_operativ_anbefaling.md`

## 7. v11c overstyrte v11b som live frontier

En renere lokal `p_triad`-akse ved fast `p_swap = 0.02` og `p_del = 0.0` flyttet optimumet videre.
Resultatet var at `bridge_0015_0000` falt tilbake, og `bridge_0010_0000` ble den sterke operative kandidaten.

I `v11c`:

- raw `mean_composite`: `bridge_0010_0000`
- `CI low`: `bridge_0010_0000`
- pairwise: `bridge_0010_0000`
- focused-score: `band_zero_del`

Dette betyr at splitten na ikke er mellom to like gode operative vinnere, men mellom:

- en operativ dynamisk vinner: `bridge_0010_0000`
- en focused/local-score-vinner: `band_zero_del`

Viktige filer:

- `relational_universe_v11c_binary_bridge_vs_band.py`
- `Documentation/v11c_binary_bridge_vs_band.md`
- `Documentation/v11c_binary_bridge_vs_band_candidate_summary.csv`
- `Documentation/v11c_binary_bridge_vs_band_pairwise.csv`
- `Documentation/v11c_binary_bridge_vs_band_target_summary.csv`
- `Documentation/v0_11c_operativ_anbefaling.md`

## 8. v11d svekket bridge_0010_0000-fortellingen

Den smale `v11d`-runden viste at `bridge_0010_0000` ikke holdt som rent lokalt optimum.
I stedet oppstod en ny, mye smalere splitt:

- raw og CI-low pekte mot `band_zero_del`
- pairwise og focused-score pekte mot `bridge_00075_0000`

Dette var en ekte lokal tvetydighet, men fortsatt under ren size-separasjon.

Viktige filer:

- `relational_universe_v11d_local_triad_refinement.py`
- `Documentation/v11d_local_triad_refinement.md`
- `Documentation/v11d_local_triad_refinement_candidate_summary.csv`
- `Documentation/v11d_local_triad_refinement_pairwise.csv`
- `Documentation/v0_11d_operativ_anbefaling.md`

## 9. v11e løste den smale duellen tilbake til band_zero_del

I stedet for en ny bred scan gikk prosjektet videre med en dypere binarrunde:

- `band_zero_del`
- `bridge_00075_0000`

Denne runden løste konflikten rent til fordel for `band_zero_del`.

I `v11e`:

- raw `mean_composite`: `band_zero_del`
- `CI low`: `band_zero_del`
- pairwise: `band_zero_del`
- focused-score: `band_zero_del`

Den viktigste lesningen her er at `v11d`-splittet ikke holdt under dypere binar diskriminering.

Viktige filer:

- `relational_universe_v11e_band_vs_bridge0075.py`
- `Documentation/v11e_band_vs_bridge0075.md`
- `Documentation/v11e_band_vs_bridge0075_candidate_summary.csv`
- `Documentation/v11e_band_vs_bridge0075_pairwise.csv`
- `Documentation/v11e_band_vs_bridge0075_target_summary.csv`
- `Documentation/v0_11e_operativ_anbefaling.md`

## 10. v12 markerte et skifte fra frontier til struktur

Etter at `band_zero_del` vant rent igjen, ble neste fase ikke en ny frontier-runde, men en strukturfase:

- hvilke normaliserte geometrifeatures er stabile pa tvers av størrelse,
- hvilke storrelser driver tregest,
- og om en liten geometrisk basis kan predikere viktige dynamiske utfall.

Denne runden er viktig fordi den flytter prosjektet fra "hvem vinner frontieren?" til "finnes det en liten effektiv beskrivelse av dynamikken?".

De mest interessante signalene sa langt er:

- `initial_avg_degree` er den mest stabile normaliserte startstorrelsen
- `initial_spectral_per_sqrtN` og `initial_dim_proxy` ser relativt stabile ut
- `initial_spectral_per_sqrtN + initial_clustering` er den beste 2-feature-basisen for `final_radius_control`
- `abs_delta_nodes_rel` og `abs_delta_beta1_rel` er eksakt null i denne runden, men dette ma ikke tas som ny dyp matematikk uten videre forklaring

Viktige filer:

- `relational_universe_v12_geometry_invariant_lab.py`
- `Documentation/v12_geometry_invariant_lab.md`
- `Documentation/v12_geometry_feature_stability.csv`
- `Documentation/v12_geometry_relative_drift_ranking.csv`
- `Documentation/v12_geometry_reduced_basis_summary.csv`
- `Documentation/v0_12_operativ_anbefaling.md`

## 11. v12b testet transfer i stedet for bare anchor-fit

`v12b` tok den lille geometribasen fra `v12` og testet om den bare virker inne i `band_zero_del`, eller om den faktisk transfererer til naerliggende triad-varianter.

Det viktigste resultatet er:

- det finnes et moderat positivt transfer-signal for `final_radius_control`
- transferen er svak eller negativ for `avg_local_overlap`
- off-anchor er `spectral_only` svaakt sterkere enn `spectral_plus_clustering`
- derfor ser det ut som prosjektet har et ekte, men fortsatt smalt radius-/geometrisignal

Viktige filer:

- `relational_universe_v12b_transfer_surrogate_lab.py`
- `Documentation/v12b_transfer_surrogate_lab.md`
- `Documentation/v12b_transfer_basis_summary.csv`
- `Documentation/v12b_transfer_target_summary.csv`
- `Documentation/v0_12b_operativ_anbefaling.md`

## 12. v12c raffinerte radius-transferen

`v12c` tok transfersporet ett hakk videre:

- flere naerliggende triadpunkter ble testet,
- bare `final_radius_control` ble holdt som hovedmal,
- og sma surrogate-baser ble sammenlignet direkte mot hverandre.

Det viktigste resultatet er:

- `spectral_plus_dim` er svaakt best pa mean off-anchor radius-skill
- `spectral_only` ligger nesten likt og ma beholdes som naer kontroll
- `spectral_plus_clustering` faller litt tilbake som arbeidsbasis, selv om det fortsatt er positivt
- alle basisene blir svakt negative ved `bridge_0015_0000`, som peker mot en lokal gyldighetsgrense for radius-transferen

Viktige filer:

- `relational_universe_v12c_radius_transfer_refinement.py`
- `Documentation/v12c_radius_transfer_refinement.md`
- `Documentation/v12c_radius_basis_summary.csv`
- `Documentation/v12c_radius_basis_ranking.csv`
- `Documentation/v0_12c_operativ_anbefaling.md`

## 13. v12d testet radius-surrogatet pa tvers av lokale akser

`v12d` tok neste naturlige steg etter `v12c`:

- behold `band_zero_del` som fast arbeidsregime,
- behold radius som hovedmal,
- men flytt testingen utenfor ren triad-akse til sma delete- og death-avvik.

Det viktigste resultatet er:

- `spectral_plus_dim` er fortsatt best pa kryssakse mean skill
- `spectral_only` ligger tett nok til a vaere naermeste enkle kontroll
- `full_basis` er ikke lenger den riktige operative motkandidaten, selv om den nesten matcher pa ren kryssakse-mean
- derfor bor prosjektet forelopig jobbe med et lite enkelt basis-plateau, ikke med en stor feature-bunt

Viktige filer:

- `relational_universe_v12d_cross_axis_radius_transfer.py`
- `Documentation/v12d_cross_axis_radius_transfer.md`
- `Documentation/v12d_cross_axis_basis_summary.csv`
- `Documentation/v12d_cross_axis_basis_ranking.csv`
- `Documentation/v0_12d_operativ_anbefaling.md`

## 14. v12e testet faktisk nytte: screening og sortering

`v12e` spurte ikke lenger bare om transfer virker, men om de samme basisene kan brukes til en konkret oppgave:

- billigere rangering av starttilstander,
- bedre screening av lovende kandidater,
- uten a kjore hele dynamikken pa alle mulige baser.

Det viktigste resultatet er:

- `full_basis` er best pa within-target screening i denne runden
- `spectral_plus_dim` er fortsatt beste kompakte basis
- derfor er den riktige operative lesningen ikke "den lille basisen vant alt", men "vi har na et benchmark vs kompakt arbeidsbasis-par"

Viktige filer:

- `relational_universe_v12e_start_state_screening.py`
- `Documentation/v12e_start_state_screening.md`
- `Documentation/v12e_screening_summary.csv`
- `Documentation/v0_12e_operativ_anbefaling.md`

## 15. v12f gjorde screening til en eksplisitt budsjettpolicy

`v12f` tok neste naturlige steg etter `v12e`:

- behold `band_zero_del` som fast regime,
- behold radius som praktisk etikett,
- men maal na hva som skjer hvis vi faktisk bare lar toppfraksjonen innen hver størrelse gaa videre til dyre oppfolgingskjoringer.

Det viktigste resultatet er:

- `full_basis` holder seg som budsjettbenchmark
- `spectral_only` slar `spectral_plus_dim` som beste lille policy i denne konkrete oppgaven
- men denne seieren er smal: `spectral_only` ligger bare hairline foran `random_baseline` pa curve-wide AUC
- derfor er den riktige lesningen ikke at en liten regel "har losningen", men at `spectral_only` er den beste enkle kandidaten a ta med videre inn i en mer direkte pipeline-test

Viktige filer:

- `relational_universe_v12f_budget_screening.py`
- `Documentation/v12f_budget_screening.md`
- `Documentation/v12f_budget_summary.csv`
- `Documentation/v0_12f_operativ_anbefaling.md`

## 16. v12g oversatte budsjettkurven til en direkte oppfolgingspipeline

`v12g` tok neste naturlige steg etter `v12f`:

- behold `full_basis@0.50` som referanse,
- behold `spectral_only` og `spectral_plus_dim` som kompakte kandidater,
- og maal na ikke bare kurve-score, men om en kompakt policy faktisk kan vaere billigere enn referansen ved omtrent samme kvalitet.

Det viktigste resultatet er:

- `spectral_only@0.50` er den naermeste kompakte erstatningen
- men den gir ingen ekstra oppfolgingsbesparelse mot referansen fordi den bruker samme budsjett
- `spectral_only@0.333` gir ekte ekstra sparing, men taper for mye pa hit og recall
- `spectral_only@0.667` eller `spectral_plus_dim@0.667` matcher lettere, men er dyrere enn referansen

Den riktige lesningen er derfor:

- vi har en enkel same-budget-substitutt
- vi har ennå ikke en klart billigere kompakt policy med omtrent samme kvalitet

Viktige filer:

- `relational_universe_v12g_followup_budget_pipeline.py`
- `Documentation/v12g_followup_budget_pipeline.md`
- `Documentation/v12g_followup_pipeline_summary.csv`
- `Documentation/v0_12g_operativ_anbefaling.md`

## 17. Dagens operative lesning

Dagens beste korte lesning er:

- frontier-standard: `band_zero_del`
- aktiv forskningsfase: geometri / invariants / redusert basis / transfer
- screening-benchmark akkurat na: `full_basis`
- beste kompakte screeningpolicy akkurat na: `initial_spectral_per_sqrtN`
- naer kompakt strukturkontroll: `initial_spectral_per_sqrtN + initial_dim_proxy`
- mest lovende ikke-trivielle geometrispor ellers: `initial_clustering` og `initial_dim_proxy`
- viktig advarsel: eksakte null-drifter ma skilles fra ekte ny matematikk til de er forklart bedre
- viktig nyansering: radius-transferen ser lokal ut; ved ytre triadpunkt og sterkere delete-avvik blir signalet svakere enn pa de naere regimepunktene
- ny budsjettadvarsel: `spectral_only` er bare marginalt bedre enn random-baseline pa curve-wide screening-AUC
- ny pipelineadvarsel: `spectral_only@0.50` er naermest benchmarken, men gir ikke ekstra budsjettgevinst mot `full_basis@0.50`

## 18. Hva som bor gjores videre

Hvis prosjektet fortsetter lokalt, er det naturlige neste steget ikke mer frontier-tuning, men videre struktur-/transferarbeid som tester:

- om den reduserte basisen transfererer til flere naerliggende regimer,
- om de samme feature-kombinasjonene predikerer flere dynamiske mal enn bare radius,
- og om noen av de langsomme driftstorrelsene kan forklares eller formaliseres bedre.

Etter `v12b`-`v12g` er den oppdaterte anbefalingen:

- fortsett geometri-/transfersporet heller enn frontier-tuning
- bruk `band_zero_del` som fast arbeidsregime
- prioriter `final_radius_control` som primart transfer-mal
- bruk `full_basis` som screening-benchmark
- bruk `spectral_only@0.50` som naavaerende kompakt same-budget-kandidat
- behold `spectral_plus_dim` som viktig strukturkontroll, ikke som automatisk beste policy
- test neste en enda mer direkte arbeidsflyt der `spectral_only@0.50` faktisk brukes til a velge hvilke baser som far oppfolgingskjoringer, og maal om enkelheten alene gir praktisk gevinst eller bare metodisk lesbarhet
