# PROJECT_HISTORY_INDEX

Dette er en komprimert historikk over de viktigste metodiske vendepunktene frem til dagens live state.

## 0. v14 og v14b skilte Lorentz-diagnostikk fra frontier og invariants

Etter `v13n` ble det tydelig at videre hyperlokal spektralraffinering ikke svarer direkte pa relativitets-sporsmalet.
`v14` tok derfor et smalt, artefaktbevisst sideblikk:

- samme deep startensembler,
- samme basegrafer,
- samme run-seeds pa tvers av perturbasjonstyper,
- eksplisitt logging av faktisk perturbasjonstype etter fallback.

Det viktigste resultatet er:

- size-separasjonen holder fortsatt rent
- perturbasjonene er faktisk lokale under denne oppsettet
- men `local_swap` og `add_chord` gir fortsatt for ulike frontfartsestimater til at repoet kan kalle dette Lorentz-likt

Dermed ble statusen pa Lorentz-sporet strammet inn fra "uklar heuristikk" til:

- ikke dominert av aapenbare simulasjonsartefakter i denne runden
- men fortsatt `mode_dependent_not_yet`

Viktige filer:

- `relational_universe_v14_lorentz_diagnostics.py`
- `Documentation/v14_lorentz_diagnostics.md`
- `Documentation/v14_lorentz_artifact_checks.csv`
- `Documentation/v14_lorentz_pairwise_perturbation_summary.csv`
- `Documentation/v14_lorentz_regime_gap_summary.csv`
- `Documentation/v0_14_operativ_anbefaling.md`

`v14b` tok neste naturlige steg etter dette:

- samme type perturbasjon fra flere lokale plasseringer
- samme basegraf, samme seed, samme regime
- eksplisitt sammenlikning av within-mode placement-variasjon mot between-mode-gapen fra `v14`

Det viktigste resultatet er at placement-variasjonen konkurrerer med mellom-modus-gapet:

- `band_zero_del`: within `~0.648` vs mode `~0.658`
- `band_pdel_0005`: within `~0.526` vs mode `~0.510`

Dermed ble Lorentz-sporet strammet inn enda et hakk:

- ikke bare "ikke universell frontfart ennå"
- men ogsa "den observerte mode-forskjellen kan fortsatt forklares av lokal anisotropi / placement-stoy"

Viktige filer:

- `relational_universe_v14b_lorentz_placement_diagnostics.py`
- `Documentation/v14b_lorentz_placement_diagnostics.md`
- `Documentation/v14b_lorentz_placement_summary.csv`
- `Documentation/v14b_lorentz_within_mode_summary.csv`
- `Documentation/v14b_lorentz_between_mode_summary.csv`
- `Documentation/v14b_lorentz_mode_vs_placement_diagnosis.csv`
- `Documentation/v0_14b_operativ_anbefaling.md`

`v14c` tok deretter den smaleste isotropirunden som fortsatt ga ny informasjon:

- bare ankerregimet `band_zero_del`
- bare `local_swap`
- flere placements per base
- eksplisitt test av om enkel lokal støttegeometri forklarer placement-variansen

Det viktigste resultatet er negativt, men nyttig:

- placement-variansen er fortsatt reell
- men de enkle lokale feature-ene (`support_ball_2`, `support_ball_3`, `support_shell_2`, `mean_support_degree`) forklarer den nesten ikke
- beste feature var `support_ball_3`, men fortsatt svakt:
  - spearman mot fart `~ -0.098`
  - spearman mot rask hit `~ -0.324`
- within-base alignment er lav for alle feature-ene

Dermed ble Lorentz-sporet strammet inn enda et hakk:

- vi ser fortsatt ingen ren universell frontfart
- lokal anisotropi er fortsatt ikke utelukket
- men heller ikke de enkle støttegeometriene gir en god forklaring

Viktige filer:

- `relational_universe_v14c_local_isotropy_diagnostics.py`
- `Documentation/v14c_local_isotropy_diagnostics.md`
- `Documentation/v14c_local_isotropy_feature_signal_summary.csv`
- `Documentation/v14c_local_isotropy_alignment_summary.csv`
- `Documentation/v0_14c_operativ_anbefaling.md`

## 0b. v15 fant det første klare mesoskalasignalet

Etter at `v14`-sporet strammet inn Lorentz-lesningen uten å åpne noe klart nytt fysisk signal, skiftet `v15` fokus:

- behold `band_zero_del` som stabilt arbeidsregime
- behold de rene, dype startensemble-ne
- men klassifiser lokale perturbasjoner etter levetid og morfologi i stedet for bare frontfart

Det viktigste resultatet er det mest positive i denne fasen:

- `add_chord` gir `persistent_split` i `0.938` av run-ene
- `local_swap` gir `persistent_split` i `0.688` av run-ene og `persistent_diffuse` i `0.250`
- `token_shift` gir fortsatt mye `persistent_split`, men også den eneste tydelige `dies_out`-andelen

Det betyr ikke at vi har funnet partikler.
Men det betyr at prosjektet for første gang har et tydeligere signal om repeterbare mesoskopiske objekt- eller defect-lignende utfall enn bare frontier-score eller Lorentz-diagnostikk.

Viktige filer:

- `relational_universe_v15_defect_lifetime_lab.py`
- `Documentation/v15_defect_lifetime_lab.md`
- `Documentation/v15_defect_lifetime_aggregate.csv`
- `Documentation/v15_defect_lifetime_by_target.csv`
- `Documentation/v0_15_operativ_anbefaling.md`

## 0c. v15b viste at add_chord-defects ikke bare superponerer

Etter at `v15` fant `add_chord` som den sterkeste mesoskalefamilien, tok `v15b` neste smale steg:

- samme `band_zero_del`
- samme deep, size-separerte ensembler
- to lokalt separerte `add_chord`-placements pa samme basegraf
- matched single-runs og pair-runs med samme seed
- begge orders (`ab`, `ba`) for a skille ekte interaksjon fra ordresensitiv konstruksjon
- eksplisitt kontroll av at control-grenene for AB og BA holder seg samkjorte

Det viktigste resultatet er det sterkeste interaksjonssignalet sa langt:

- artifact-control holder rent
- `control_edge_jaccard_ab_ba = 1.0` i alle rader
- `pair_order_jaccard = 1.0` i alle rader
- men pair-runene ligger langt fra unionen av matched single-runs
  - `mean_pair_union_jaccard` ligger omtrent mellom `0.208` og `0.462`
- alle rader klassifiseres som `interaction_supported`

Dette betyr fortsatt ikke at prosjektet har vist partikler.
Men det betyr at prosjektet na har et klart, artefaktkontrollert signal om at to lokale `add_chord`-defects kan interagere pa en maate som ikke ser ut som ren superposisjon.

Viktige filer:

- `relational_universe_v15b_add_chord_collision_lab.py`
- `Documentation/v15b_add_chord_collision_lab.md`
- `Documentation/v15b_add_chord_collision_interactions.csv`
- `Documentation/v15b_add_chord_collision_aggregate.csv`
- `Documentation/v0_15b_operativ_anbefaling.md`

## 0d. v15c viste at interaksjonstypen fortsatt er blandet

Etter at `v15b` viste et klart og artefaktkontrollert kollisjonssignal, tok `v15c` neste smale steg:

- behold samme `band_zero_del`
- behold samme deep, size-separerte ensembler
- behold samme matched single/pair-run-oppsett
- men klassifiser sluttgeometrien mer direkte som `binding_like`, `secondary_split_like`, `annihilation_like`, `pass_through_like` eller `mixed_collision`

Det viktigste resultatet er todelt:

- artifact-control holder fortsatt rent
- men interaksjonstypen er fortsatt ikke rent løst

Konkrete signaler:

- `binding_like`: `0.188`
- `secondary_split_like`: `0.250`
- `mixed_collision`: `0.562`
- `annihilation_like`: `0.000`
- `pass_through_like`: `0.000`

Dermed ble defect-sporet strammet inn enda et hakk:

- kollisjonssignalet fra `v15b` holder
- men prosjektet kan ennå ikke si at `add_chord`-familien har én tydelig dominant interaksjonstype
- neste riktige steg er derfor ikke bredere validering, men enda strammere møtesporing rundt selve kollisjonstidspunktet

Viktige filer:

- `relational_universe_v15c_collision_type_lab.py`
- `Documentation/v15c_collision_type_lab.md`
- `Documentation/v15c_collision_type_rows.csv`
- `Documentation/v15c_collision_type_aggregate.csv`
- `Documentation/v0_15c_operativ_anbefaling.md`

## 0e. v15d gjorde møtevinduet skarpere, men ikke endelig

Etter at `v15c` viste at sluttklassifiseringen fortsatt var blandet, tok `v15d` et smalere og mer tidsoppløst steg:

- bare `48` og `96`
- samme matched single/pair-run-oppsett
- tettere snapshots
- eksplisitt fokus på det snapshotet der pair-runen avviker mest fra unionen av single-runs

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `mixed_window` dominerer fortsatt (`0.750`)
- men vi ser nå to tydeligere møtevindustyper:
  - ett `compress_then_split`
  - ett `persistent_binding_tendency`

Dette betyr:

- kollisjonssignalet fra `v15b` holder fortsatt
- `v15d` gjør bildet mer informativt enn `v15c`
- men prosjektet kan fortsatt ikke si at én dominant interaksjonstype styrer `add_chord`-familien
- neste riktige steg er derfor enda smalere pair-selection i `48`-korridoren

Viktige filer:

- `relational_universe_v15d_collision_window_lab.py`
- `Documentation/v15d_collision_window_lab.md`
- `Documentation/v15d_collision_window_rows.csv`
- `Documentation/v15d_collision_window_aggregate.csv`
- `Documentation/v0_15d_operativ_anbefaling.md`

## 0f. v15e viste at pair-familiene fortsatt er blandet

Etter at `v15d` pekte på to mer interessante 48-pair-familier, tok `v15e` neste smale steg:

- bare target `48`
- bare pair `2-3` og `3-4`
- mer budsjett per pair
- samme matched AB/BA-oppsett og samme vindusklassifisering

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `2-3` heller litt mot `compress_then_split`, men ikke rent nok (`0.333`)
- `3-4` bekrefter ikke en ren binding-familie (`binding = 0.083`)
- begge pair-familiene forblir dominert av `mixed_window`

Dermed ble defect-sporet strammet inn enda et hakk:

- `2-3` er fortsatt den mest lovende videre oppfølgingsfamilien
- `3-4` ser mer heterogen ut enn vi håpet
- neste riktige steg er derfor enda mer budsjett på `2-3`, ikke mer bredde

Viktige filer:

- `relational_universe_v15e_pair_family_refinement.py`
- `Documentation/v15e_pair_family_refinement.md`
- `Documentation/v15e_pair_family_rows.csv`
- `Documentation/v15e_pair_family_aggregate.csv`
- `Documentation/v0_15e_operativ_anbefaling.md`

## 0g. v15f viste avtagende verdi i mer budsjett pa bare pair 2-3

Etter at `v15e` pekte ut `2-3` som den mest lovende pair-familien, tok `v15f` neste smale steg:

- bare target `48`
- bare pair `2-3`
- mer run-budsjett pa samme base
- samme matched AB/BA-oppsett og samme vindusklassifisering

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `compress_then_split` overlever, men styrkes ikke (`0.125`)
- `mixed_window` dominerer tydeligere (`0.750`)
- signalet blir dermed ikke renere av mer av samme mikrobudsjett

Dette betyr:

- `2-3` er fortsatt den mest informative lokale pair-familien
- men denne spesifikke raffineringslinjen ser ut til a ha avtagende verdi
- neste riktige steg er derfor sannsynligvis ikke bare flere offsets, men en annen type defect-oppfolging

Viktige filer:

- `relational_universe_v15f_pair23_budget_extension.py`
- `Documentation/v15f_pair23_budget_extension.md`
- `Documentation/v15f_pair23_rows.csv`
- `Documentation/v15f_pair23_aggregate.csv`
- `Documentation/v15f_pair23_availability.csv`
- `Documentation/v0_15f_operativ_anbefaling.md`

## 0h. v15g byttet fra coarse labels til genealogy og event-kjeder

Etter at `v15f` viste avtagende verdi i mer av samme mikrobudsjett, tok `v15g` et smalt, men metodisk viktig skifte:

- behold `band_zero_del`
- behold `add_chord`
- behold matched single/pair-run-oppsettet
- behold den smale `48`-korridoren
- men la component trajectories, event-logg og event-kjeder vaere hovedproduktet

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- begge pair-familiene finnes pa den delte `101`-basen
- `order_ambiguous_count = 0` for begge pair-familiene
- de gamle `mixed_window`-utfallene blir mer strukturert under genealogy-lesning
  - `2-3`: `compress_split_rebind = 0.333`, `merge_hold_split = 0.333`, `split_persistent_dual = 0.333`
  - `3-4`: `compress_split_rebind = 0.333`, `split_persistent_dual = 0.667`

Dette betyr:

- defect-sporet blir mer informativt enn i `v15e`/`v15f`
- men pair-familiene kollapser fortsatt ikke til helt rene arter
- neste riktige steg er derfor ikke mer pair-offset-sok, men lengre representative trajectories med de samme observablene

Viktige filer:

- `relational_universe_v15g_collision_genealogy_lab.py`
- `Documentation/v15g_collision_genealogy_lab.md`
- `Documentation/v15g_collision_genealogy_component_trajectories.csv`
- `Documentation/v15g_collision_genealogy_event_log.csv`
- `Documentation/v15g_collision_genealogy_event_aggregate.csv`
- `Documentation/v15g_collision_genealogy_event_chains.csv`
- `Documentation/v0_15g_operativ_anbefaling.md`

## 0i. v15h flyttet spørsmalet fra label-miks til representative langtrajektorier

Etter at `v15g` viste at de gamle `mixed_window`-utfallene kunne brytes ned i noen fa genealogy-kjeder, tok `v15h` neste smale steg:

- behold `band_zero_del`
- behold `add_chord`
- behold matched single/pair-run-oppsettet
- velg bare noen fa representative traces fra `v15g`
- kjor dem mye lenger med de samme genealogy-observablene

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- alle de valgte representative tracene reproduserer forventet `v15g`-chain pa prefix-horisonten
- de tidlige chain-navnene holder seg ogsa pa full horisont for disse tracene
- men senfasen kollapser ikke til ett felles tail-mønster
  - noen traces ender i `rebound_merge_tail`
  - andre ender i `mixed_tail`

Dette betyr:

- `v15h` styrker at collision-sporet er mer enn bare coarse labels
- men det sier ogsa at neste informasjonsgevinst trolig ligger i tettere trace-genealogi og senfaseanalyse, ikke i ny bred pair-scan
- prosjektet bor derfor fortsatt lese defect-sporet som "strukturert men ikke rent artdelt"

Viktige filer:

- `relational_universe_v15h_representative_collision_traces.py`
- `Documentation/v15h_representative_collision_traces.md`
- `Documentation/v15h_representative_trace_component_trajectories.csv`
- `Documentation/v15h_representative_trace_event_log.csv`
- `Documentation/v15h_representative_trace_summary.csv`
- `Documentation/v0_15h_operativ_anbefaling.md`

## 0j. v15i gjorde senfasen skarpere enn `mixed_tail` og `rebound_merge_tail`

Etter at `v15h` viste at representative collisions ikke kollapser til én felles senfase, tok `v15i` neste smale steg:

- ingen ny bred simuleringsrunde
- bare analyse av `v15h`-trace-ne
- eksplisitt fokus pa tail-overganger og senfase-segmenter

Det viktigste resultatet er:

- tail-overgangene er order-stabile
- de grove `v15h`-typene brytes videre ned i tre repeterbare senfase-overganger:
  - `quiet_singleton_lock`
  - `merge_rebound_lock`
  - `fragmenting_lock`
- `pair23_split_persistent_dual` viser en stillere singleton-lock
- `pair23_merge_hold_split` viser en tydelig merge/rebound-lock
- `pair23_compress_split_rebind` og `pair34_split_persistent_dual` ender i mer fragmenterende lock-forlop

Dette betyr:

- collision-sporet blir mer forklarbart uten ny bredde
- senfaseforskjellen mellom representative traces er ikke bare "mixed" mot "rebound", men minst tre repeterbare overgangstyper
- neste riktige steg er derfor a forklare disse overgangene med eksplisitte hendelsessegmenter og eventuelle terskelmekanismer, ikke flere pair-offset-sok

Viktige filer:

- `relational_universe_v15i_tail_transition_lab.py`
- `Documentation/v15i_tail_transition_lab.md`
- `Documentation/v15i_tail_transition_order_rows.csv`
- `Documentation/v15i_tail_transition_segments.csv`
- `Documentation/v15i_tail_transition_summary.csv`
- `Documentation/v15i_tail_transition_aggregate.csv`
- `Documentation/v0_15i_operativ_anbefaling.md`

## 0k. v15j forklarte tail-overgangene med enklere segmentmekanismer

Etter at `v15i` gjorde senfasen skarpere i tre tail-overganger, tok `v15j` neste smale steg:

- ingen nye brede simuleringer
- bare forklaring av `v15i`-tailene
- eksplisitt fokus pa segmenter, eventlast og stille suffix

Det viktigste resultatet er:

- mekanismelabelene er order-stabile
- de tre `v15i`-tail-overgangene kan forklares av tre enklere mekanismer:
  - `quiet_relaxation_lock`
  - `balanced_rebound_cycle`
  - `fragmenting_repair_cycle`
- `pair23_split_persistent_dual` blir en stille singleton-lock
- `pair23_merge_hold_split` blir en balansert rebound-syklus uten birth/death
- `pair23_compress_split_rebind` og `pair34_split_persistent_dual` blir mer fragmenterende repair-sykluser

Dette betyr:

- senfasen blir enklere a forklare enn i `v15i` alene
- defect-sporet er na mer strukturert i form av noen fa repeterbare mekanismer
- neste riktige steg er derfor terskeltesting: hva avgjor om et representativt trace havner i den ene eller andre mekanismen?

Viktige filer:

- `relational_universe_v15j_tail_mechanism_lab.py`
- `Documentation/v15j_tail_mechanism_lab.md`
- `Documentation/v15j_tail_mechanism_order_rows.csv`
- `Documentation/v15j_tail_mechanism_summary.csv`
- `Documentation/v15j_tail_mechanism_aggregate.csv`
- `Documentation/v0_15j_operativ_anbefaling.md`

## 0l. v15k viste at v15j-mekanismene ikke generaliserer rent ennå

Etter at `v15j` ga en pen lokal mekanikk-lesning av de fire representative tracene, tok `v15k` neste smale steg:

- samme lange trace-oppsett
- samme `band_zero_del`
- men nye holdout-offsets fra de samme `v15g`-familiene
- eksplisitt test av om `v15j`-mekanismene holder pa naerliggende eksempler

Det viktigste resultatet er negativt, men verdifullt:

- artifact-control holder fortsatt rent
- holdout-tracene reproduserer forventet prefix-chain
- men `v15j`-mekanismene generaliserer ikke rent
- alle fire holdout-traces ender som `mixed_mechanism`
- match-rate mot `v15j`-mekanismene er `0.000`

Dette betyr:

- `v15j` var nyttig som lokal forklaringsrunde
- men repoet stotter ikke at disse mekanismene allerede er stabile "lover" for naerliggende traces
- neste riktige steg er derfor en mer forsiktig og mindre generaliserende forklaringslinje, eller et nytt defect-sporsmal, ikke mer mekanismepastaand i bredde

Viktige filer:

- `relational_universe_v15k_mechanism_holdout_validation.py`
- `Documentation/v15k_mechanism_holdout_validation.md`
- `Documentation/v15k_mechanism_holdout_v15h_summary.csv`
- `Documentation/v15k_mechanism_holdout_v15i_summary.csv`
- `Documentation/v15k_mechanism_holdout_v15j_summary.csv`
- `Documentation/v15k_mechanism_holdout_aggregate.csv`
- `Documentation/v0_15k_operativ_anbefaling.md`

## 0m. v15l gjorde holdout-bruddet mer forklarbart uten a redde generaliseringen

Etter at `v15k` ga et verdifullt negativt resultat, tok `v15l` et rent forklaringssteg:

- ingen ny bred simulering
- bare direkte sammenlikning mellom `v15j`-mekanismene og `v15k`-holdoutene
- mal: finne ut om generaliseringsbruddet var helt vilkarlig eller kunne beskrives med noen fa lokale bruddmodi

Det viktigste resultatet er:

- holdout-bruddet er ikke helt ustrukturert
- to bruddmodi dominerer:
  - `birth_death_intrusion`
  - `quiet_suffix_collapse`
- dette gjør `v15k` mer forklarlig, men ikke mer generaliserbart

Dette betyr:

- `v15j` forblir en nyttig lokal forklaringsrunde
- `v15k` forblir et ekte negativt generaliseringsresultat
- `v15l` gir en bedre forklaring pa hvorfor bruddet skjer
- neste riktige steg er derfor et nytt defect-sporsmal eller en annen observabel, ikke enda mer mekanismegeneralisering av samme type

Viktige filer:

- `relational_universe_v15l_holdout_failure_explainer.py`
- `Documentation/v15l_holdout_failure_explainer.md`
- `Documentation/v15l_holdout_failure_comparison.csv`
- `Documentation/v15l_holdout_failure_aggregate.csv`
- `Documentation/v0_15l_operativ_anbefaling.md`

## 0n. v15m testet et nytt defect-sporsmal om survival/extinction

Etter at collision-generaliseringssporet begynte a gi avtagende verdi, tok `v15m` et bevisst sideblikk:

- behold `band_zero_del` som arbeidsregime
- behold dype, size-separerte ensembler
- bytt fra kollisjon til enkeltdefect
- test om `token_shift` har en tydelig survival/extinction-signatur, med `add_chord` som levende kontrollfamilie

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `token_shift` viser noe extinction:
  - `0.167` ved `48`
  - `0.083` ved `96`
- `add_chord` holder seg levende i alle runene i denne runden
- men skillet er fortsatt ikke rent nok til a kalle dette et sterkt survival/extinction-spor

Dette betyr:

- prosjektet har et legitimt nytt defect-sporsmal uten a late som collision-mekanismene allerede er lover
- `token_shift` er fortsatt interessant som den skjoreste defect-familien
- men survival/extinction-lesningen ma fortsatt behandles forsiktig
- neste riktige steg er ikke sterke survival-paastander, men et nytt smalt defect-sporsmal eller en mer disiplinert survival-oppfolging

Viktige filer:

- `relational_universe_v15m_single_defect_survival_lab.py`
- `Documentation/v15m_single_defect_survival_lab.md`
- `Documentation/v15m_single_defect_survival_runs.csv`
- `Documentation/v15m_single_defect_survival_aggregate.csv`
- `Documentation/v15m_single_defect_survival_target_summary.csv`
- `Documentation/v0_15m_operativ_anbefaling.md`

## 0o. v15n gjorde survival-sporsmalet smalere og mer lokalt

Etter at `v15m` viste at `token_shift` hadde noe extinction, men ikke nok til en ren survival-lov, tok `v15n` neste naturlige steg:

- behold samme `band_zero_del`
- behold `token_shift` som den skjoreste defect-familien
- behold `add_chord` som levende kontroll
- test om `token_shift`-skjorheten folger enkel lokal stottegeometri, i stedet for a late som signalet allerede er en generell family truth

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `token_shift` har fortsatt noe extinction:
  - `0.143` ved `48`
  - `0.067` ved `96`
- `add_chord` holder seg fortsatt levende i hele runden
- extinct `token_shift`-runs ser ikke helt tilfeldige ut; de har hoyere enkle stottegeometri-mal enn levende `token_shift`-runs
- tre placements gir `token_shift extinct` samtidig som `add_chord` pa samme plassering fortsatt er levende

Dette betyr:

- `v15m` sitt survival-sporsmal blir ikke loest fullt ut
- men `v15n` gjor det mer lokalt og mer forklarbart
- `token_shift` ser na mer ut som en delvis plassering-/stottestruert skjorehetsfamilie enn som ren stoy
- neste riktige steg er derfor en enda smalere token_shift-fragility-runde rundt de skjoreste stotteprofilene, ikke brede survival-paastander

Viktige filer:

- `relational_universe_v15n_token_shift_fragility_lab.py`
- `Documentation/v15n_token_shift_fragility_lab.md`
- `Documentation/v15n_token_shift_fragility_runs.csv`
- `Documentation/v15n_token_shift_fragility_aggregate.csv`
- `Documentation/v15n_token_shift_fragility_feature_summary.csv`
- `Documentation/v15n_token_shift_fragility_placement_contrast.csv`
- `Documentation/v15n_token_shift_fragility_target_summary.csv`
- `Documentation/v0_15n_operativ_anbefaling.md`

## 0p. v15o replikerte de skjore token_shift-profilene mer direkte

Etter at `v15n` antydet at `token_shift`-extinction kunne vaere delvis plassering-/stottestruert, tok `v15o` neste naturlige steg:

- behold bare de tre extinct `token_shift`-profilene fra `v15n`
- match hver av dem mot en levende `token_shift`-kontroll pa samme base
- rerun begge med flere seeds
- behold `add_chord` pa de samme plasseringene som levende kontrollfamilie

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- den sterkeste skjore profilen replikerer rent:
  - `t48_g101_p3_vs_p4`
  - `token_shift`: `0.250` extinction mot `0.000` for kontrollen
- de to andre profilene replikerer bare svakt:
  - `0.250` mot `0.125`
- `add_chord` holder fortsatt `0.000` extinction i alle de replikerte profilene

Dette betyr:

- `v15n` sitt fragility-spor var ikke bare enkeltoffset-flaks
- men replikasjonen er fortsatt bare delvis
- én lokal skjorehetsprofil holder tydelig, to andre holder bare svakt
- neste riktige steg er derfor en enda smalere profilrunde rundt den beste kandidaten, med bedre lokalt matchede kontroller, ikke brede survival-paastander

Viktige filer:

- `relational_universe_v15o_token_shift_fragility_replication.py`
- `Documentation/v15o_token_shift_fragility_replication.md`
- `Documentation/v15o_token_shift_fragility_profile_pairs.csv`
- `Documentation/v15o_token_shift_fragility_replication_runs.csv`
- `Documentation/v15o_token_shift_fragility_replication_aggregate.csv`
- `Documentation/v15o_token_shift_fragility_pair_diagnosis.csv`
- `Documentation/v15o_token_shift_fragility_target_summary.csv`
- `Documentation/v0_15o_operativ_anbefaling.md`

## 0q. v15p viste at den beste token_shift-profilen ikke holder mot bedre kontroller

Etter at `v15o` ga ett tydelig og to svake lokale fragility-profiler, tok `v15p` neste naturlige steg:

- bare den sterkeste kandidaten:
  - `target 48`
  - `growth_seed 101`
  - `token_shift` pa placement `3`
- to bedre matchede levende kontroller pa samme base:
  - `p1`, valgt fordi den matcher `support_ball_3`
  - `p4`, valgt fordi den er lokal og grad-naer
- samme replikeringslogikk, men enda smalere og mer kontrollert

Det viktigste resultatet er negativt, men nyttig:

- artifact-control holder fortsatt rent
- den antatt skjore `p3`-profilen holder ikke extinction-gap mot de bedre matchede kontrollene
- `token_shift` extinction blir:
  - `0.188` for `p3`
  - `0.312` for `p1`
  - `0.250` for `p4`
- `add_chord` holder fortsatt `0.000` extinction over alle tre profiler

Dette betyr:

- `v15o` sitt delvise lokale fragility-signal var ekte nok til a teste videre
- men den beste kandidaten overlevde ikke bedre kontrollmatching
- token_shift-fragility langs denne profillinjen er derfor ikke sterk nok som neste hovedspor
- neste riktige steg er et nytt smalt defect-sporsmal, ikke mer token_shift-fragility langs samme akse

Viktige filer:

- `relational_universe_v15p_token_shift_profile_refinement.py`
- `Documentation/v15p_token_shift_profile_refinement.md`
- `Documentation/v15p_token_shift_profile_refinement_runs.csv`
- `Documentation/v15p_token_shift_profile_refinement_aggregate.csv`
- `Documentation/v15p_token_shift_profile_refinement_diagnosis.csv`
- `Documentation/v15p_token_shift_profile_refinement_target_summary.csv`
- `Documentation/v0_15p_operativ_anbefaling.md`

## 0r. v15q flyttet defect-sporet til senfase-retur og recurrence

Etter at `v15p` svekket token_shift-fragility som hovedspor, tok `v15q` et nytt og smalt defect-sporsmal:

- behold `band_zero_del`
- behold single defects
- legg bort fragility og kollisjon som primarsporsmal
- test om defects i senfasen faktisk vender tilbake til tidligere morfologier, i stedet for bare a drive videre

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- alle tre perturbasjonstyper viser sterk grov morfologisk retur i denne smale runden
- `add_chord` og `local_swap` er renest:
  - `0.875` morphology_return ved `48`
  - `0.875-1.000` ved `96`
- `token_shift` viser ogsa retur, men blandet med `extinct_after_return` ved `48`
- eksakt syklisk retur er mye svakere enn den grove morfologiske returen

Dette betyr:

- recurrence/return-sporet er et sterkere nytt defect-spor enn den siste token_shift-fragility-linjen
- prosjektet ser ikke en ren eksakt sykluslov, men en tydeligere grov morfologisk retur
- neste riktige steg er derfor en enda smalere recurrence-runde, mest naturlig for `add_chord`, ikke brede defect-paastander

Viktige filer:

- `relational_universe_v15q_single_defect_recurrence_lab.py`
- `Documentation/v15q_single_defect_recurrence_lab.md`
- `Documentation/v15q_single_defect_recurrence_runs.csv`
- `Documentation/v15q_single_defect_recurrence_aggregate.csv`
- `Documentation/v15q_single_defect_recurrence_target_summary.csv`
- `Documentation/v0_15q_operativ_anbefaling.md`

## 0s. v15r viste at en smal add_chord-cyclefamilie faktisk overlever pa lang horisont

Etter at `v15q` fant grov morfologisk retur for alle tre single-defect-familiene, tok `v15r` neste naturlige steg:

- behold bare noen fa representative `add_chord`-profiler fra `v15q`
- folg dem lenger i tid i stedet for a aapne nye profiler
- skil eksplisitt mellom prefix-retur og full-horisont-retur
- avgjor om den beste cycle-kandidaten faktisk holder

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `t48_g202_p2` holder `cyclic_return` ogsa pa full horisont
- `t96_g202_p3` starter som `cyclic_return`, men mykner til `morphology_return`
- de to morfologiske kontrollprofilene tipper faktisk over til `cyclic_return` pa full horisont
- anbefalingen blir derfor `long_horizon_recurrence = cyclic_return_survives`

Dette betyr:

- `v15q` sitt recurrence-spor var ikke bare grov hale-stabilitet
- repoet har na ett ekte, men smalt, `add_chord`-cycle-signal
- dette er fortsatt ikke en generell defect-lov eller partikkelpastand
- neste riktige steg er a kartlegge cycle-familien lokalt rundt den overlevende profilen

Viktige filer:

- `relational_universe_v15r_add_chord_long_horizon_recurrence.py`
- `Documentation/v15r_add_chord_long_horizon_recurrence.md`
- `Documentation/v15r_add_chord_long_horizon_runs.csv`
- `Documentation/v15r_add_chord_long_horizon_aggregate.csv`
- `Documentation/v15r_add_chord_long_horizon_target_summary.csv`
- `Documentation/v0_15r_operativ_anbefaling.md`

## 0t. v15s viste at cycle-signalet er et lite lokalt band, ikke bare ett punkt

Etter at `v15r` viste at minst én `add_chord`-profil holdt ekte `cyclic_return` pa lang horisont, tok `v15s` neste naturlige steg:

- behold bare samme base: `target 48`, `growth_seed 202`
- behold bare de fire lokale `add_chord`-plasseringene `0-3`
- bruk samme lange horisont som i `v15r`
- avgjor om `p2` er et enslig lokalt unntak eller del av en liten familie

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- alle fire lokale profiler ender som `cyclic_return` pa full horisont
- `p2` holder som `sustained_cyclic_return`
- `p0`, `p1` og `p3` tipper fra `morphology_return` til `cyclic_return`
- den sterkeste lokale profilen er `p1`, ikke `p2`
- diagnosen ender pa `local_cycle_band`

Dette betyr:

- `v15r` sitt cycle-signal var ikke bare ett heldig enkeltspor
- repoet har na et smalt lokalt `add_chord`-cycle-band pa samme base
- dette er fortsatt en lokal familie, ikke en generell sykluslov
- neste riktige steg er en enda smalere kartlegging inne i bandet, mest naturlig rundt `p1` og `p2`

Viktige filer:

- `relational_universe_v15s_add_chord_cycle_family_map.py`
- `Documentation/v15s_add_chord_cycle_family_map.md`
- `Documentation/v15s_add_chord_cycle_family_runs.csv`
- `Documentation/v15s_add_chord_cycle_family_diagnosis.csv`
- `Documentation/v15s_add_chord_cycle_family_target_summary.csv`
- `Documentation/v0_15s_operativ_anbefaling.md`

## 0u. v15t viste at det lokale cycle-bandet ikke er flatt, men forskyves mot p1

Etter at `v15s` viste et lite lokalt `add_chord`-cycle-band pa samme base, tok `v15t` neste naturlige steg:

- behold bare samme base: `target 48`, `growth_seed 202`
- behold bare `p1` og `p2`
- bruk noen fa nye dynamikk-seeds som smale holdouts
- avgjor om `p1` faktisk er et sterkere lokalt sentrum enn `p2`

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `p1` holder `cyclic_return` i alle seks holdout-kjoringene
- `p2` holder `cyclic_return` i fem av seks, men glipper en gang til `morphology_return`
- `p1` far `mean_full_exact_return_rate = 0.897`
- `p2` far `mean_full_exact_return_rate = 0.744`
- seed-duellene ender `p1_wins=4`, `p2_wins=2`, `ties=0`
- diagnosen ender pa `shifted_center_p1`

Dette betyr:

- `v15s` sitt lokale cycle-band holder ogsa under smale holdout-seeds
- men bandet er ikke flatt; sentrum ser na forskyvet ut mot `p1`
- dette er fortsatt en lokal mikrofamilie pa en enkelt base, ikke en generell `add_chord`-lov
- neste riktige steg er en enda smalere mikrotest rundt `p1`, ikke bredere scanning

Viktige filer:

- `relational_universe_v15t_add_chord_cycle_center_holdout.py`
- `Documentation/v15t_add_chord_cycle_center_holdout.md`
- `Documentation/v15t_add_chord_cycle_center_runs.csv`
- `Documentation/v15t_add_chord_cycle_center_aggregate.csv`
- `Documentation/v15t_add_chord_cycle_center_diagnosis.csv`
- `Documentation/v15t_add_chord_cycle_center_target_summary.csv`
- `Documentation/v0_15t_operativ_anbefaling.md`

## 0v. v15u viste at p1 fortsatt ikke er et rent losnet sentrum over begge flanker

Etter at `v15t` pekte mot `p1` som forskyvet lokalt sentrum, tok `v15u` neste naturlige steg:

- behold bare samme base: `target 48`, `growth_seed 202`
- behold bare `p0`, `p1` og `p2`
- bruk et nytt lite holdout-sett av seeds
- avgjor om `p1` faktisk holder seg over begge umiddelbare flanker samtidig

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- alle tre plasseringene holder `cyclic_return` i alle seks holdout-kjoringene
- `p1` slar fortsatt `p2` tydelig, med `p1_wins=4`, `p2_wins=1`, `ties=1`
- men `p1` slar ikke `p0` rent; seed-duellene ender `p1_wins=3`, `p0_wins=2`, `ties=1`
- `p0` far faktisk hoyere mean full exact return (`0.859`) enn `p1` (`0.846`)
- diagnosen ender derfor pa `microcenter_still_mixed`

Dette betyr:

- `v15t` sitt p1-sentrum holder ikke som fullt losnet konklusjon
- det lokale `add_chord`-bandet er fortsatt ekte, men den indre mikrostrukturen er fortsatt blandet
- neste riktige steg er en liten mekanistisk forklaringsrunde inne i `p0-p1-p2`, ikke bredere mapping

Viktige filer:

- `relational_universe_v15u_add_chord_p1_microcenter.py`
- `Documentation/v15u_add_chord_p1_microcenter.md`
- `Documentation/v15u_add_chord_p1_microcenter_runs.csv`
- `Documentation/v15u_add_chord_p1_microcenter_aggregate.csv`
- `Documentation/v15u_add_chord_p1_microcenter_diagnosis.csv`
- `Documentation/v15u_add_chord_p1_microcenter_target_summary.csv`
- `Documentation/v0_15u_operativ_anbefaling.md`

## 0w. v15v gjorde triplet-en mer forklarbar, men fortsatt ikke rent losnet

Etter at `v15u` lot `p0-p1-p2` sta igjen som ekte mikrofamilie, men uten rent sentrum, tok `v15v` neste naturlige steg:

- behold bare samme triplet
- behold samme holdout-seeds som i `v15u`
- apne ingen nye profiler
- mal i stedet tail-lock-mekanismer: hvor tidlig og hvor stabilt hver profil lases inn i exact-return

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `p0` domineres av `intermittent_cycle_lock`
- `p1` domineres ogsa av `intermittent_cycle_lock`, med bare litt mer `early_stable_lock`
- `p2` er den eneste profilen som far tydelig `coarse_cycle_shell`
- `p1` kommer litt tidligere til første exact return enn flankene, men har hoyere switch-count enn `p0`
- diagnosen ender pa `triplet_mechanism_still_mixed`

Dette betyr:

- `v15v` gjor triplet-en mer forklarbar enn `v15u`, men loser ikke sentrumssporsmalet rent
- `p2` ser na tydeligst svakere ut mekanistisk enn de to andre
- den viktigste usikkerheten sitter na mellom `p0` og `p1`
- neste riktige steg er en enda mindre forklaringsrunde for `p0` vs `p1`, ikke bredere scanning

Viktige filer:

- `relational_universe_v15v_add_chord_triplet_mechanism_lab.py`
- `Documentation/v15v_add_chord_triplet_mechanism_lab.md`
- `Documentation/v15v_add_chord_triplet_mechanism_runs.csv`
- `Documentation/v15v_add_chord_triplet_mechanism_tail_rows.csv`
- `Documentation/v15v_add_chord_triplet_mechanism_aggregate.csv`
- `Documentation/v15v_add_chord_triplet_mechanism_diagnosis.csv`
- `Documentation/v15v_add_chord_triplet_mechanism_target_summary.csv`
- `Documentation/v0_15v_operativ_anbefaling.md`

## 0x. v15w gjorde p0-vs-p1 mer konkret, men fortsatt ikke enkelt forklart

Etter at `v15v` gjorde `p0-p1-p2`-triplet-en mer forklarbar, men lot `p0` vs `p1` sta igjen som hovedusikkerhet, tok `v15w` neste naturlige steg:

- behold bare `p0` og `p1`
- behold samme smale holdout-dueller
- apne ingen nye dynamikk-runder
- sammenlign i stedet lokal stottegeometri mot det observerte duel-bildet

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `p1` sitter i litt tettere lokal støtte enn `p0`
  - `mean_support_degree`: `6.333` mot `5.667`
  - `support_ball_1`: `17` mot `15`
- `p0` har samtidig litt større relativ videre ekspansjon
  - `ball3_over_ball1`: `2.400` mot `2.294`
- duel-bildet er fortsatt blandet
  - `p1_clean_advantage`: `0.333`
  - `p1_calm_advantage`: `0.167`
  - `p0_clean_advantage`: `0.167`
  - `speed_stability_tradeoff`: `0.167`
  - `mixed_duel`: `0.167`
- diagnosen ender derfor pa `contrast_still_mixed`

Dette betyr:

- `v15w` gjor p0-vs-p1 mer konkret enn `v15v`
- men enkel støttegeometri alene forklarer ikke hele forskjellen
- `p1` ser litt tettere og litt mer lokal ut, men `p0` kompenserer fortsatt i noen dueller
- neste riktige steg er en enda mindre forklaringsrunde pa de unike nodene (`5` vs `10`) eller pa første tail-segment

Viktige filer:

- `relational_universe_v15w_add_chord_p0_p1_support_contrast.py`
- `Documentation/v15w_add_chord_p0_p1_support_contrast.md`
- `Documentation/v15w_add_chord_p0_p1_support_summary.csv`
- `Documentation/v15w_add_chord_p0_p1_duel_rows.csv`
- `Documentation/v15w_add_chord_p0_p1_duel_aggregate.csv`
- `Documentation/v15w_add_chord_p0_p1_support_diagnosis.csv`
- `Documentation/v15w_add_chord_p0_p1_target_summary.csv`
- `Documentation/v0_15w_operativ_anbefaling.md`

## 0y. v15x viste at første tail-segment heller ikke losner p0-vs-p1 rent

Etter at `v15w` viste at enkel støttegeometri ikke forklarte p0-vs-p1 fullt ut, tok `v15x` neste naturlige steg:

- behold bare `p0` og `p1`
- behold samme base og samme smale holdout-seeds
- rerun dynamikken
- mal bare første tail-segment fram til exact-return lock

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- alle seks seed-duellene ender pa `mixed_first_segment`
- mean onset-bilde er fortsatt svakt og blandet
  - `p1_minus_p0_first_gap = -6.7`
  - `p1_minus_p0_component_gap = 0.208`
  - `p1_minus_p0_largest_gap = -0.004`
  - `p1_minus_p0_boundary_gap = 0.002`
  - `p1_minus_p0_post_switch_gap = 3.333`
  - `p1_minus_p0_exact_gap = -0.013`
- ingen av de sma onset-labelene blir dominante

Dette betyr:

- første tail-segment gjor p0-vs-p1 mer konkret, men ikke renere
- onset alene forklarer ikke hvorfor de to sterkeste lokale punktene fortsatt ligger sa tett
- neste riktige steg er en enda mindre forklaringsrunde pa en eller to konkrete seed-caser, ikke nye aggregate-runder

Viktige filer:

- `relational_universe_v15x_add_chord_p0_p1_first_tail_segment.py`
- `Documentation/v15x_add_chord_p0_p1_first_tail_segment.md`
- `Documentation/v15x_add_chord_p0_p1_first_tail_segment_runs.csv`
- `Documentation/v15x_add_chord_p0_p1_first_tail_segment_duels.csv`
- `Documentation/v15x_add_chord_p0_p1_first_tail_segment_aggregate.csv`
- `Documentation/v15x_add_chord_p0_p1_first_tail_segment_diagnosis.csv`
- `Documentation/v15x_add_chord_p0_p1_first_tail_segment_target_summary.csv`
- `Documentation/v0_15x_operativ_anbefaling.md`

## 0z. v15y viste at tre små p0-vs-p1-seeds faktisk holder som tre ulike case-typer

Etter at `v15x` viste at første tail-segment fortsatt var blandet i aggregate, tok `v15y` neste naturlige steg:

- behold bare de tre mest informative seedene
- `151` som sterk `p1`-case
- `239` som mulig tradeoff-case
- `271` som sterk `p0`-case
- avgjor om disse faktisk holder som tre ulike lokale case-typer

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `151` holder som `p1_clean_case`
- `239` holder som `tradeoff_case`
- `271` holder som `p0_clean_case`
- case-aggregatet blir derfor perfekt delt:
  - `p1_clean_case = 0.333`
  - `tradeoff_case = 0.333`
  - `p0_clean_case = 0.333`
- diagnosen ender pa `three_case_family_supported`

Dette betyr:

- `p0`-vs-`p1`-usikkerheten er ikke bare stoyende mikrovariasjon
- repoet har na et lite, men ekte, lokalt case-familiebilde
- neste riktige steg er a forklare hva som utloser hvert case, ikke a samle flere aggregate-runder

Viktige filer:

- `relational_universe_v15y_p0_p1_case_duel_lab.py`
- `Documentation/v15y_p0_p1_case_duel_lab.md`
- `Documentation/v15y_p0_p1_case_duel_runs.csv`
- `Documentation/v15y_p0_p1_case_duel_segments.csv`
- `Documentation/v15y_p0_p1_case_duel_duels.csv`
- `Documentation/v15y_p0_p1_case_duel_aggregate.csv`
- `Documentation/v15y_p0_p1_case_duel_diagnosis.csv`
- `Documentation/v15y_p0_p1_case_duel_target_summary.csv`
- `Documentation/v0_15y_operativ_anbefaling.md`

## 0za. v15z forklarte de tre case-typene med tre ulike onset-triggere

Etter at `v15y` viste at `151`, `239` og `271` faktisk holder som tre ulike lokale case-typer, tok `v15z` neste naturlige steg:

- ingen nye simuleringer
- behold den samme smale p0-vs-p1-duellen
- bruk `v15w` for statisk støttebias
- bruk `v15y` for onset-segment og case-duel-data
- avgjor om de tre case-seedene faktisk kan forklares av et lite sett onset-triggere

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- den svake statiske støttefordelen for `p1` holder som bakgrunnsbias
- men den er ikke hele forklaringen
- `151` holder som `p1_compact_radius_trigger`
- `239` holder som `fragmented_fast_tradeoff_trigger`
- `271` holder som `p0_calm_singleton_trigger`
- diagnosen ender pa `three_local_triggers_supported`

Dette betyr:

- de tre case-typene fra `v15y` var ikke bare nyttige etiketter; de kan na forklares mer konkret
- `p1` vinner rent nar den far en kompakt onset med kortere radius og mindre skadesett
- `p1` taper nar den kommer raskt, men fragmentert
- `p0` vinner nar den holder en roligere singleton-lock mens `p1` starter mer splittet
- neste riktige steg er derfor en liten holdout-test av triggerne, ikke en ny bred p0-vs-p1-scan

Viktige filer:

- `relational_universe_v15z_case_trigger_explainer.py`
- `Documentation/v15z_case_trigger_explainer.md`
- `Documentation/v15z_case_trigger_rows.csv`
- `Documentation/v15z_case_trigger_aggregate.csv`
- `Documentation/v15z_case_trigger_diagnosis.csv`
- `Documentation/v15z_case_trigger_target_summary.csv`
- `Documentation/v0_15z_operativ_anbefaling.md`

## 0zb. v15aa viste at triggerhistorien ikke generaliserer rent til nærliggende seeds

Etter at `v15z` ga en klarere forklaring pa `151`, `239` og `271`, tok `v15aa` det smaleste mulige neste steget:

- behold samme basegraf
- behold samme `p0` vs `p1`
- behold samme `band_zero_del`
- test bare to naerliggende holdout-seeds rundt hvert av de tre ankercasene
- avgjor om triggerhistorien bærer lokalt utover de tre opprinnelige seedene

Det viktigste resultatet er klart og negativt:

- artifact-control holder fortsatt rent
- ingen av de tre triggerfamiliene matcher i holdoutene
- alle seks holdout-radene ender som `mixed_trigger`
- familieaggregatet blir derfor:
  - `151`-familien: `not_supported`
  - `239`-familien: `not_supported`
  - `271`-familien: `not_supported`
- diagnosen ender pa `trigger_holdout_not_yet`

Dette betyr:

- `v15z` var nyttig som forklaring av ankercasene
- men forklaringen holder ikke som lokal lov i naerliggende seeds
- repoet bor derfor ikke bruke mer tid pa a generalisere disse triggerne langs samme linje
- neste riktige steg er en ny observabel eller et annet defect-sporsmal, ikke mer trigger-generalisering

Viktige filer:

- `relational_universe_v15aa_case_trigger_holdout.py`
- `Documentation/v15aa_case_trigger_holdout.md`
- `Documentation/v15aa_case_trigger_holdout_runs.csv`
- `Documentation/v15aa_case_trigger_holdout_segments.csv`
- `Documentation/v15aa_case_trigger_holdout_rows.csv`
- `Documentation/v15aa_case_trigger_holdout_aggregate.csv`
- `Documentation/v15aa_case_trigger_holdout_diagnosis.csv`
- `Documentation/v15aa_case_trigger_holdout_target_summary.csv`
- `Documentation/v0_15aa_operativ_anbefaling.md`

## 0zc. v15ab viste at cycle-båndet er diffust, ikke skarpt periodisk

Etter at `v15aa` stoppet videre trigger-generalisering, tok `v15ab` neste smale steg i det sterkeste gjenværende defect-signalet:

- behold samme lokale `add_chord`-bånd ved `t48_g202`
- behold de samme smale holdout-seedene som i `v15u`
- bytt observabel fra "hvem holder best?" til "har retur-signalet en stabil lag/periode?"

Det viktigste resultatet er tydelig:

- artifact-control holder fortsatt rent
- alle tre plasseringene holder fortsatt `cyclic_rate = 1.0`
- men ingen av dem får `stable_single_lag_cycle`
- ingen av dem får heller `few_lag_cycle_family`
- alle tre ender som `diffuse_cycle_family`
- mean dominant lag share er bare omtrent `0.106` til `0.147`
- diagnosen ender pa `cycle_band_is_diffuse`

Dette betyr:

- det lokale `add_chord`-cycle-båndet er fortsatt reelt som recurrence-signal
- men det ser ikke ut til a være drevet av en skarp lokal periode
- høy exact-return-rate kommer i stedet fra bred multi-lag-retur
- repoet bør derfor ikke bruke mer tid pa en periodestory langs denne aksen
- neste riktige steg er en annen observabel enn periodisitet

Viktige filer:

- `relational_universe_v15ab_add_chord_cycle_lag_lab.py`
- `Documentation/v15ab_add_chord_cycle_lag_lab.md`
- `Documentation/v15ab_add_chord_cycle_lag_runs.csv`
- `Documentation/v15ab_add_chord_cycle_lag_aggregate.csv`
- `Documentation/v15ab_add_chord_cycle_lag_diagnosis.csv`
- `Documentation/v15ab_add_chord_cycle_lag_target_summary.csv`
- `Documentation/v0_15ab_operativ_anbefaling.md`

## 0zd. v15ac-v15ad gjorde recurrence-båndet mer fysisk lesbart: stabil kjerne, rolig rand

Etter at `v15ab` viste at cycle-båndet ikke er skarpt periodisk, tok prosjektet to nye smale observabelskift på samme lokale `add_chord`-band ved `t48_g202`:

- behold samme `p0`, `p1`, `p2`
- behold de samme smale holdout-seedene
- bytt først til kjerne/rand-struktur i `v15ac`
- og deretter til randdynamikk i `v15ad`

Det viktigste resultatet i `v15ac` er:

- artifact-control holder fortsatt rent
- alle tre plasseringene holder fortsatt `cyclic_rate = 1.0`
- `core_share_of_union` er høy for alle tre (`~0.855` til `~0.892`)
- `support_core_frac = 1.0` for alle tre
- labelene blir en blanding av `stable_core_variable_shell` og `dominant_static_core`
- diagnosen ender pa `cycle_band_is_core_shell`

Dette betyr:

- recurrence-bandet er bedre forklart som stabil skadekjerne + variabel rand enn som skarp periode

Det viktigste resultatet i `v15ad` er:

- artifact-control holder fortsatt rent
- randen ser ikke bursty ut
- `p0` holder `calm_shell_rate = 1.0`
- `p1` og `p2` holder `calm_shell_rate = 0.667`
- mean shell refresh er lav (`~0.080` til `~0.091`)
- diagnosen ender pa `core_shell_variation_is_calm`

Dette betyr:

- det lokale add_chord-signalet ser ikke bare ut som kjerne + rand
- det ser ut som kjerne + rolig flimrende rand
- dette er et sterkere og mer fysisk lesbart mesoskalasignal enn periodehistorien eller trigger-generaliseringen
- neste riktige steg er derfor randtopologi eller rand-hendelser, ikke mer arbeid pa perioder eller triggere

Viktige filer:

- `relational_universe_v15ac_add_chord_core_shell_lab.py`
- `Documentation/v15ac_add_chord_core_shell_lab.md`
- `Documentation/v15ac_add_chord_core_shell_runs.csv`
- `Documentation/v15ac_add_chord_core_shell_aggregate.csv`
- `Documentation/v15ac_add_chord_core_shell_diagnosis.csv`
- `Documentation/v0_15ac_operativ_anbefaling.md`
- `relational_universe_v15ad_add_chord_boundary_shell_lab.py`
- `Documentation/v15ad_add_chord_boundary_shell_lab.md`
- `Documentation/v15ad_add_chord_boundary_shell_runs.csv`
- `Documentation/v15ad_add_chord_boundary_shell_aggregate.csv`
- `Documentation/v15ad_add_chord_boundary_shell_diagnosis.csv`
- `Documentation/v0_15ad_operativ_anbefaling.md`

## 0ze. v15ae viste at den rolige randen er topologisk fragmentert, ikke ett sammenhengende shell-band

Etter at `v15ac-v15ad` gjorde recurrence-bandet mer fysisk lesbart som stabil kjerne + rolig flimrende rand, tok `v15ae` neste smale observabelskift:

- behold samme `t48_g202`-band med `p0`, `p1`, `p2`
- behold de samme smale holdout-seedene som i `v15ab-v15ad`
- bytt sporsmal fra randtempo til randtopologi
- avgjor om shellen vanligvis holder seg sammenhengende, blir fragmentert, eller bærer lokal cycle-rank

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- alle tre plasseringene holder fortsatt `cyclic_rate = 1.0`
- `p0` og `p1` blir `fragmented_shell_band` i alle seks runene
- `p2` blir `fragmented_shell_band` i fem av seks og `mixed_shell_topology` i ett
- mean shell component count ligger hoyt (`~3.35`, `~3.55`, `~4.18`)
- mean shell connected rate holder seg lav (`~0.090`, `~0.108`, `~0.177`)
- shell loop rate er `0.0` for alle tre
- diagnosen ender pa `cycle_band_has_fragmented_shell_zone`

Dette betyr:

- recurrence-bandet er fortsatt reelt
- men shellen er vanligvis ikke ett sammenhengende band rundt kjernen
- den rolige randvarianten fra `v15ad` ma derfor leses som rolig fragmentert churn, ikke som en stabil lukket randring
- lokal cycle-rank i shellen er ikke det som driver signalet
- neste riktige steg er a lokalisere nar i halevinduet fragmenteringen dannes eller opploses, ikke en bredere scan

Viktige filer:

- `relational_universe_v15ae_add_chord_shell_topology_lab.py`
- `Documentation/v15ae_add_chord_shell_topology_lab.md`
- `Documentation/v15ae_add_chord_shell_topology_runs.csv`
- `Documentation/v15ae_add_chord_shell_topology_snapshots.csv`
- `Documentation/v15ae_add_chord_shell_topology_aggregate.csv`
- `Documentation/v15ae_add_chord_shell_topology_diagnosis.csv`
- `Documentation/v15ae_add_chord_shell_topology_target_summary.csv`
- `Documentation/v0_15ae_operativ_anbefaling.md`

## 0zf. v15af viste at shell-fragmenteringen vanligvis starter tidlig og låser seg i halen

Etter at `v15ae` viste at add_chord-shellen vanligvis er fragmentert, tok `v15af` neste smale steg:

- behold samme `t48_g202`-band med `p0`, `p1`, `p2`
- behold de samme seks smale seedene
- bruk bare de ekte `v15ae`-snapshottene, uten nye simuleringer
- lokaliser nar i halevinduet fragmenteringen starter og om den blir en tidlig lock eller bare senere churn

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `p0` har `early_fragment_lock_rate = 0.833`
- `p1` har `early_fragment_lock_rate = 0.500`, `delayed_fragment_lock_rate = 0.167` og `intermittent_fragment_churn_rate = 0.167`
- `p2` har `early_fragment_lock_rate = 0.667`, `intermittent_fragment_churn_rate = 0.167` og `connected_resistance_churn_rate = 0.167`
- mean first fragment step ligger tett pa tail-start for `p0` og `p2` (`~1537.3`)
- `p1` ligger litt senere (`~1549.3`), som passer med det lille delayed-onset-sporet
- fragmented suffix rate holder seg hoy for alle tre plasseringene
- diagnosen ender pa `fragmentation_is_usually_early_lock`

Dette betyr:

- shell-fragmenteringen i cycle-bandet ser vanligvis ut til a starte tidlig i halevinduet og deretter holde seg som en lokal lock
- dette skjerper `v15ae`: fragmenteringen er ikke bare topologisk til stede, den etablerer seg ofte nesten med en gang i halen
- de viktigste avvikene er na ikke brede familier, men minoritetsspor:
  - et lite delayed-onset-spor i `p1`
  - et lite connected-resistance-spor i `p2`
- neste riktige steg er derfor a forklare disse minoritetsavvikene, ikke a scanne bredere

Viktige filer:

- `relational_universe_v15af_add_chord_shell_fragment_event_lab.py`
- `Documentation/v15af_add_chord_shell_fragment_event_lab.md`
- `Documentation/v15af_add_chord_shell_fragment_runs.csv`
- `Documentation/v15af_add_chord_shell_fragment_segments.csv`
- `Documentation/v15af_add_chord_shell_fragment_aggregate.csv`
- `Documentation/v15af_add_chord_shell_fragment_diagnosis.csv`
- `Documentation/v15af_add_chord_shell_fragment_target_summary.csv`
- `Documentation/v0_15af_operativ_anbefaling.md`

## 0zg. v15ag gjorde minoritetsavvikene lokalt forklarbare

Etter at `v15af` viste at shell-fragmenteringen vanligvis låser tidlig, tok `v15ag` neste smale steg:

- behold bare de seks minoritetsavvikene fra `v15af`
- kjør ingen nye simuleringer
- bruk bare `v15ae`- og `v15af`-dataene
- avgjor om unntakene fortsatt er blandet stoy eller kollapser til et lite lokalt mekanismesett

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- de seks minoritetsrunene kollapser til fire mekanismelabels
- `alternating_to_late_lock` dekker tre av seks unntak
- `two_stage_fragment_lock` forklarer `p1` sitt delayed-onset-case
- `singleton_resistance_case` forklarer `p2` sitt connected-resistance-case
- `near_lock_boundary_case` dekker det siste grensetilfellet
- diagnosen ender pa `minority_exceptions_are_locally_explainable`

Dette betyr:

- minoritetsavvikene i shell-fragmenteringen ser ikke lenger ut som ren reststoy
- de danner et lite lokalt mekanismesett:
  - en liten hovedfamilie med veksling som ender i sen fragment-lock
  - en totrinns delayed-lock
  - en singleton-resistensmekanisme
  - ett boundary-case naer early-lock-familien
- neste riktige steg er derfor en liten holdout-test av akkurat disse unntaksmekanismene, ikke en ny bred scan

Viktige filer:

- `relational_universe_v15ag_shell_exception_explainer.py`
- `Documentation/v15ag_shell_exception_explainer.md`
- `Documentation/v15ag_shell_exception_rows.csv`
- `Documentation/v15ag_shell_exception_aggregate.csv`
- `Documentation/v15ag_shell_exception_diagnosis.csv`
- `Documentation/v15ag_shell_exception_target_summary.csv`
- `Documentation/v0_15ag_operativ_anbefaling.md`

## 0zh. v15ah viste at unntaksmekanismene ikke holder som lokale familier

Etter at `v15ag` gjorde minoritetsavvikene lokalt forklarbare, tok `v15ah` neste riktige steg:

- behold bare de seks unntaksankrene fra `v15ag`
- behold samme `t48_g202`-base og samme observabler
- legg inn to naerliggende holdout-seeds rundt hvert unntaksanker
- avgjor om unntaksmekanismene faktisk replikerer lokalt

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `expected_match_rate = 0.0` for alle seks unntaksankre
- fire av seks ankre har `main_family_revert_rate = 1.0`
- de to gjenværende ankre splitter mellom `early_fragment_lock` og `unresolved_holdout`
- ingen holdouts gaar over i en annen kjent unntaksmekanisme
- diagnosen ender pa `exceptions_mostly_revert_to_main_family`

Dette betyr:

- `v15ag` ga ekte lokal forklaringsverdi for ankerseedene, men mekanismene holder ikke som naerliggende lokale familier
- den viktigste nye kunnskapen er derfor negativ, men sterk:
  - unntakene ser best ut som lokale avvik rundt en robust hovedfamilie `early_fragment_lock`
- prosjektet bor ikke bruke mer tid pa bredere unntaks-ekspansjon langs denne aksen
- hvis sporet skal fortsette, bor neste steg vaere en ny observabel inne i hovedfamilien, ikke mer unntaksjakt

Viktige filer:

- `relational_universe_v15ah_shell_exception_holdout.py`
- `Documentation/v15ah_shell_exception_holdout.md`
- `Documentation/v15ah_shell_exception_holdout_runs.csv`
- `Documentation/v15ah_shell_exception_holdout_aggregate.csv`
- `Documentation/v15ah_shell_exception_holdout_diagnosis.csv`
- `Documentation/v15ah_shell_exception_holdout_target_summary.csv`
- `Documentation/v0_15ah_operativ_anbefaling.md`

## 0zi. v15ai viste at hovedfamilien er bedre lest som coarse fragment-load-band enn som eksakt shell-telling

Etter at `v15ah` viste at unntaksmekanismene ikke holder som naerliggende lokale familier, tok `v15ai` neste riktige steg:

- behold samme lokale `t48_g202` add_chord-band
- behold bare run som faktisk ligger i hovedfamilien `early_fragment_lock`
- bruk ankerrun fra `v15ae-v15af` og holdout-run fra `v15ah` som falt tilbake til hovedfamilien
- bytt observabel fra eksakt shell-komponenttall til coarse band `low = 1..3`, `mid = 4..6`, `high = 7+`

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- ankerrun har `structured_band_rate = 1.0`
- holdout-revert-run har `structured_band_rate = 0.9`
- kombinert `structured_band_rate = 0.955`
- kombinert `band_lock_rate = 0.727`, med bare `band_drift_rate = 0.045`
- `mean_dominant_band_share = 0.687`, mot `mean_dominant_exact_share = 0.365`
- coarse band slar derfor eksakt telling med stor margin: `uplift = 0.322`
- diagnosen ender pa `early_lock_has_structured_band_ladder`

Dette betyr:

- dette ga ekte ny viten inne i hovedfamilien, ikke bare en ny etikett
- `early_fragment_lock` ser mye bedre ut som en strukturert low/mid/high band-stige med litt naboband-drift enn som ett eksakt shell-komponenttall
- hovedfamilien er fortsatt ikke en ren liten liste av defect-arter
- men vi har na en klart bedre mesoskopisk observabel enn eksakt telling
- neste riktige steg er a forklare nar run larser seg inn i `low`, `mid` eller `high`, og hvilke run som bare driver mellom to naboband

Viktige filer:

- `relational_universe_v15ai_early_lock_band_lab.py`
- `Documentation/v15ai_early_lock_band_lab.md`
- `Documentation/v15ai_early_lock_band_runs.csv`
- `Documentation/v15ai_early_lock_band_snapshots.csv`
- `Documentation/v15ai_early_lock_band_aggregate.csv`
- `Documentation/v15ai_early_lock_band_diagnosis.csv`
- `Documentation/v15ai_early_lock_band_target_summary.csv`
- `Documentation/v0_15ai_operativ_anbefaling.md`

## 0zj. v15aj viste at band-onseten er strukturert og placement-skjev

Etter at `v15ai` viste at `early_fragment_lock` er bedre lest som coarse band enn som eksakt shell-telling, tok `v15aj` neste riktige steg:

- behold de ekte `v15ai`-snapshottene
- bruk ingen nye simuleringer
- finn tidligste suffix der runet holder seg innenfor ett band eller et naboband-par
- avgjor om runet gaar rett inn i `low-mid`, senere glir inn i `mid-high`, eller blir igjen i bredere tre-band-churn

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- kombinert `structured_onset_rate = 0.818`
- kombinert `immediate_structured_rate = 0.591`
- kombinert `delayed_structured_rate = 0.227`
- kombinert `persistent_three_band_churn_rate = 0.182`
- `p0` har `immediate_low_mid_ladder_rate = 0.857`
- `p2` har `delayed_mid_high_ladder_rate = 0.375` og `persistent_three_band_churn_rate = 0.250`
- diagnosen ender pa `band_onset_structure_supported`

Dette betyr:

- dette ga ny viten utover `v15ai`: onseten er selv strukturert, ikke bare sluttfordelingen
- `early_fragment_lock` ser ikke flat ut gjennom hele halevinduet
- placement `0` gaar oftest direkte inn i `low-mid`
- placement `2` trenger oftere tid for a komme inn i `mid-high`, eller blir igjen i bredere churn
- neste riktige steg er derfor a forklare inngangstriggerne til disse onset-typene, ikke en ny bred scan

Viktige filer:

- `relational_universe_v15aj_early_lock_band_onset_lab.py`
- `Documentation/v15aj_early_lock_band_onset_lab.md`
- `Documentation/v15aj_early_lock_band_onset_runs.csv`
- `Documentation/v15aj_early_lock_band_onset_aggregate.csv`
- `Documentation/v15aj_early_lock_band_onset_diagnosis.csv`
- `Documentation/v15aj_early_lock_band_onset_target_summary.csv`
- `Documentation/v0_15aj_operativ_anbefaling.md`

## 0zk. v15ak viste at tidlig hale skiller compact low-entry ganske rent, men ikke boundary-sonen

Etter at `v15aj` viste at band-onseten er strukturert, tok `v15ak` neste riktige steg:

- behold de ekte `v15ai`-snapshottene og `v15aj`-onsettypene
- bruk ingen nye simuleringer
- mal enkle tidlige hale-features i de forste 24 snapshottene
- avgjor om disse forklarer immediate `low-mid`, `mid-high`-entry og vedvarende churn

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- immediate low-family har `compact_low_entry_rate = 0.917`
- mid-high-entry-family har `boundary_mixed_rate + heavy_high_pressure_rate = 1.000`
- persistent churn-family har `boundary_mixed_rate = 1.000`
- diagnosen ender pa `entry_trigger_map_partly_supported`

Dette betyr:

- dette ga ny viten: tidlig hale skiller immediate `low-mid` ganske rent fra resten
- immediate `low-mid` ser nesten alltid ut som kompakte low-entry-caser med lav last og rolig switching
- `mid-high`-entry og vedvarende churn lever fortsatt i samme boundary/heavy-sone tidlig i halen
- neste riktige steg er derfor a splitte boundary-sonen, ikke a lete etter nye brede familier

Viktige filer:

- `relational_universe_v15ak_band_entry_trigger_lab.py`
- `Documentation/v15ak_band_entry_trigger_lab.md`
- `Documentation/v15ak_band_entry_trigger_runs.csv`
- `Documentation/v15ak_band_entry_trigger_aggregate.csv`
- `Documentation/v15ak_band_entry_trigger_diagnosis.csv`
- `Documentation/v15ak_band_entry_trigger_target_summary.csv`
- `Documentation/v0_15ak_operativ_anbefaling.md`

## 0zl. v15al viste at boundary-sonen deler seg delvis i high-rise og mid-plateau

Etter at `v15ak` viste at ikke-lave run fortsatt levde i en felles boundary/heavy-sone, tok `v15al` neste riktige steg:

- behold bare `boundary_mixed_trigger`-runene fra `v15ak`
- bruk ingen nye simuleringer
- se litt lenger frem i den tidlige halen, de forste 72 snapshottene
- avgjor om boundary-sonen deler seg i noen fa lokale profiler

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- boundary-sonen deler seg i tre profiler:
  - `late_high_rise_boundary`
  - `mid_plateau_boundary`
  - `residual_boundary`
- `mid_high_entry_family` har `late_high_rise_rate = 0.500`
- `persistent_churn_family` har `mid_plateau_rate = 0.750`
- diagnosen ender pa `boundary_zone_partly_split`

Dette betyr:

- dette ga ny viten, men bare delvis
- boundary-sonen er ikke homogen
- `mid-high`-entry havner oftere i en sen high-rise-gren
- vedvarende churn havner oftere i en roligere mid-plateau-gren
- overlap-caseene er fortsatt viktige, sa dette er ikke en ren lokal lov
- neste riktige steg er a forklare overlap-caseene, ikke a ga bredere med en gang

Viktige filer:

- `relational_universe_v15al_boundary_zone_split_lab.py`
- `Documentation/v15al_boundary_zone_split_lab.md`
- `Documentation/v15al_boundary_zone_split_runs.csv`
- `Documentation/v15al_boundary_zone_split_aggregate.csv`
- `Documentation/v15al_boundary_zone_split_diagnosis.csv`
- `Documentation/v15al_boundary_zone_split_target_summary.csv`
- `Documentation/v0_15al_operativ_anbefaling.md`

## 0zm. v15am gjorde overlap-caseene mer lesbare, men ikke helt løst

Etter at `v15al` delte boundary-sonen i late high-rise, mid-platå og residual, tok `v15am` neste smale steg:

- behold bare de tre overlap-caseene fra `v15al`
- behold de typiske referanselopene for late high-rise og mid-platå
- bruk ingen nye simuleringer
- sammenlign overlap-runene direkte mot disse familieprofilene i samme 72-snapshot-vindu

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `5002161` blir godt forklart som `churn_to_high_rise_crossover`
- `5002240` blir godt forklart som `suppressed_high_rise_plateau`
- `5002220` blir bare delvis forklart som `residual_tilt_to_mid_plateau`
- diagnosen ender pa `overlap_cases_still_partly_mixed`

Dette betyr:

- dette ga ny viten, men i smal form
- overlap-sonen er ikke bare reststoy; to av tre overlap-case blir lokalt mer forklarbare
- residual-caset er fortsatt ikke rent lost, bare tydeligere lokaliseret mot mid-platå-siden
- vi har derfor ikke en liten lokal lov ennå
- neste riktige steg er a bytte observabel inne i overlap-sonen i stedet for a presse denne forklaringen hardere

Viktige filer:

- `relational_universe_v15am_boundary_overlap_explainer.py`
- `Documentation/v15am_boundary_overlap_explainer.md`
- `Documentation/v15am_boundary_overlap_explainer_runs.csv`
- `Documentation/v15am_boundary_overlap_explainer_aggregate.csv`
- `Documentation/v15am_boundary_overlap_explainer_diagnosis.csv`
- `Documentation/v15am_boundary_overlap_explainer_target_summary.csv`
- `Documentation/v0_15am_operativ_anbefaling.md`

## 0zn. v15an viste at overlap-sonen best leses gjennom high-hold, ikke bare familieavstand

Etter at `v15am` gjorde overlap-caseene mer lesbare, men fortsatt ikke helt loste, tok `v15an` neste smale steg:

- behold samme fokuserte run-sett fra `v15am`
- behold de ekte `v15ai`-snapshottene
- bruk ingen nye simuleringer
- mal ikke bare om high-band dukker opp, men om det faktisk holder, glipper eller bare blinker til helt pa slutten

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `5002161` blir skarpt lest som `delayed_high_hold_crossover`
- `5002240` blir skarpt lest som `no_high_hold_plateau`
- `5002220` blir skarpt lest som `late_terminal_high_probe`
- diagnosen ender pa `high_hold_observable_sharpens_overlap_zone`

Dette betyr:

- dette ga ekte ny viten utover `v15am`
- overlap-sonen er bedre forklart av om high-band faktisk holder enn av bare mer generelle familieavstander
- residual-caset ser ikke lenger ut som et nesten-high-rise lop; det ser ut som en sen terminal high-probe
- neste riktige steg er derfor a teste grensen mellom ekte sen high-hold og bare terminal high-probe

Viktige filer:

- `relational_universe_v15an_boundary_high_hold_lab.py`
- `Documentation/v15an_boundary_high_hold_lab.md`
- `Documentation/v15an_boundary_high_hold_runs.csv`
- `Documentation/v15an_boundary_high_hold_aggregate.csv`
- `Documentation/v15an_boundary_high_hold_diagnosis.csv`
- `Documentation/v15an_boundary_high_hold_target_summary.csv`
- `Documentation/v0_15an_operativ_anbefaling.md`

## 0zo. v15ao viste at high-grensen deler seg i fire lesbare haleutfall

Etter at `v15an` viste at overlap-sonen best leses gjennom high-hold, tok `v15ao` neste smale steg:

- behold det fokuserte `v15an`-settet
- legg til ett naerliggende delayed-probe-kontrollop
- bruk ingen nye simuleringer
- avgjor om high-grensen faktisk deler seg i noen fa lesbare haleutfall

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `5002161` blir `established_high_hold`
- `5002220` blir `terminal_high_probe`
- `5002221` blir `failed_early_high_probe`
- `5002240` og mid-platåreferansene blir `no_high_hold_plateau`
- diagnosen ender pa `terminal_probe_boundary_is_structured`

Dette betyr:

- dette ga ekte ny viten utover `v15an`
- residual- og probe-sporene ser ikke lenger ut som generell boundary-mix
- den smale high-grensen deler seg i minst fire lesbare haleutfall:
  - ekte high-hold
  - terminal high-probe
  - mislykket tidlig high-probe
  - ingen high-hold
- neste riktige steg er derfor a forklare hva som bestemmer om sen high starter tidlig nok til a bli hold i stedet for bare terminal probe

Viktige filer:

- `relational_universe_v15ao_terminal_probe_boundary_lab.py`
- `Documentation/v15ao_terminal_probe_boundary_lab.md`
- `Documentation/v15ao_terminal_probe_boundary_runs.csv`
- `Documentation/v15ao_terminal_probe_boundary_aggregate.csv`
- `Documentation/v15ao_terminal_probe_boundary_diagnosis.csv`
- `Documentation/v15ao_terminal_probe_boundary_target_summary.csv`
- `Documentation/v0_15ao_operativ_anbefaling.md`

## 0zp. v15ap viste at de fire haleutfallene allerede kan leses i pre-high launch-vinduet

Etter at `v15ao` viste at high-grensen deler seg i fire lesbare haleutfall, tok `v15ap` neste smale steg:

- behold det fokuserte `v15ao`-settet
- bruk ingen nye simuleringer
- mal bare det lille pre-high-vinduet rett for high enten holder, feiler eller uteblir
- avgjor om de fire haleutfallene allerede kan leses der

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `established_high_hold` leses som `mixed_threshold_launch`
- `terminal_high_probe` leses som `compact_terminal_launch`
- `failed_early_high_probe` leses som `premature_probe_launch`
- `no_high_hold_plateau` leses som `no_launch_plateau`
- diagnosen ender pa `pre_high_launch_map_supported`

Dette betyr:

- dette ga ekte ny viten utover `v15ao`
- forskjellen mellom hold, terminal probe og failed probe ser ut til a vaere synlig allerede i launch-vinduet rett for high-forsoket
- high-grensen er derfor ikke bare en haleeffekt; den har et lite pre-high launch-kart
- neste riktige steg er en liten holdout-test av dette launch-kartet, ikke en bredere scan

Viktige filer:

- `relational_universe_v15ap_pre_high_launch_lab.py`
- `Documentation/v15ap_pre_high_launch_lab.md`
- `Documentation/v15ap_pre_high_launch_runs.csv`
- `Documentation/v15ap_pre_high_launch_aggregate.csv`
- `Documentation/v15ap_pre_high_launch_diagnosis.csv`
- `Documentation/v15ap_pre_high_launch_target_summary.csv`
- `Documentation/v0_15ap_operativ_anbefaling.md`

## 0zq. v15aq viste at impulse-vinduet skiller hold fra sen spike, men ikke failed probe rent nok

Etter at `v15ap` viste at de fire haleutfallene allerede kan leses i pre-high launch-vinduet, tok `v15aq` neste smale steg:

- behold det fokuserte `v15ap`-settet
- bruk ingen nye simuleringer
- mal bare det aller forste post-launch-vinduet etter at high begynner eller nesten begynner
- avgjor om forskjellen mellom hold og probe blir enda skarpere der

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `5002161` og `5002205` blir `sustained_hold_impulse`
- `5002241` blir `rebounding_hold_impulse`
- `5002220` blir `compact_late_spike`
- `5002221` blir bare `soft_failed_impulse`
- diagnosen ender pa `launch_impulse_map_still_mixed`

Dette betyr:

- dette ga noe ny struktur, men mindre ny viten enn `v15ap`
- impulse-vinduet skiller hold fra sen spike ganske godt
- men failed-probe-sporet blir fortsatt ikke rent nok lest i samme observabel
- neste riktige steg er derfor ikke mer press pa impulse-vinduet alene, men en annen liten observabel eller en liten holdout rundt launch-kartet

Viktige filer:

- `relational_universe_v15aq_high_launch_impulse_lab.py`
- `Documentation/v15aq_high_launch_impulse_lab.md`
- `Documentation/v15aq_high_launch_impulse_runs.csv`
- `Documentation/v15aq_high_launch_impulse_aggregate.csv`
- `Documentation/v15aq_high_launch_impulse_diagnosis.csv`
- `Documentation/v15aq_high_launch_impulse_target_summary.csv`
- `Documentation/v0_15aq_operativ_anbefaling.md`

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

## 17. v12h la et eksplisitt kostnadsregnskap over pipeline-valgene

`v12h` tok neste naturlige steg etter `v12g`:

- behold de samme policyene,
- behold `full_basis@0.50` som referanse,
- men la na screeningfasen selv ha en eksplisitt kostnad i arbeidsmodellen.

Det viktigste resultatet er:

- hvis screening er billig eller ukjent, holder `full_basis@0.50` seg som best benchmark
- `spectral_only@0.50` er fortsatt den enkleste same-budget-kandidaten
- hvis screeningkostnaden blir tydelig ikke-neglisjerbar, blir `spectral_plus_dim@0.667` den mest interessante kostnadsnoytrale utfordreren
- derfor er lesningen na betinget av arbeidsmodell, ikke bare av rene oppfolgingskjøringer

Viktige filer:

- `relational_universe_v12h_cost_aware_pipeline.py`
- `Documentation/v12h_cost_aware_pipeline.md`
- `Documentation/v12h_cost_aware_pipeline_summary.csv`
- `Documentation/v0_12h_operativ_anbefaling.md`

## 18. v12i malte faktisk workflow-tid i stedet for a anta screeningkostnad

`v12i` tok neste naturlige steg etter `v12h`:

- behold samme referansepolicyer,
- behold samme aktive regime,
- men maal na virkelig veggklokketid for screening og oppfolging pa den faktiske lokale kodebanen.

Det viktigste resultatet er:

- oppfolgingstiden dominerer nesten fullstendig ved dagens størrelser
- screeningtiden blir praktisk neglisjerbar i total workflow
- `full_basis@0.50` holder seg derfor som maelt arbeidsbenchmark
- `spectral_only@0.50` er fortsatt riktig same-budget-kandidat, men den gir nesten ingen faktisk total tidsgevinst
- `spectral_plus_dim@0.667` beholder hoy kvalitet, men blir tydelig tregere fordi den sender flere baser videre til dyre oppfolgingsbundler

Dette er viktig fordi det strammer inn lesningen av `v12e`-`v12h`:

- de kompakte basisene er fortsatt interessante som struktur og forklaring
- men ved dagens grafstorrelser er det forelopig ikke der den store praktiske arbeidsbesparelsen ligger

Viktige filer:

- `relational_universe_v12i_measured_runtime_pipeline.py`
- `Documentation/v12i_measured_runtime_pipeline.md`
- `Documentation/v12i_measured_runtime_pipeline_followup_timing_summary.csv`
- `Documentation/v12i_measured_runtime_pipeline_summary.csv`
- `Documentation/v0_12i_operativ_anbefaling.md`

## 19. v12j testet om v12i-holder litt opp i størrelse

`v12j` tok neste naturlige steg etter `v12i`:

- behold samme regime,
- behold samme policytrio,
- men flytt workflow-testen til noe større naturlige ensembler.

Det viktigste resultatet er:

- realiserte startstørrelser holder seg fortsatt rent separert
- screeningandelen er fortsatt praktisk neglisjerbar i total workflow
- `spectral_only@0.50` svekkes heller enn styrkes i denne større runden
- `spectral_plus_dim@0.667` er kvalitetsmessig sterkere, men tydelig dyrere
- `random_baseline@0.50` matcher faktisk referansen pa mean best-hit og recall i denne lille større-runden, som er en klar advarsel om at screening-signalet ikke automatisk blir bedre med litt større grafer

Den riktige lesningen er derfor:

- den praktiske flaskehalsen ligger fortsatt i oppfolgingsdynamikken
- kompakte basisrom er fortsatt mer interessante som struktur og forklaring enn som maelt arbeidsbesparelse

Viktige filer:

- `relational_universe_v12j_size_stress_runtime_pipeline.py`
- `Documentation/v12j_size_stress_runtime_pipeline.md`
- `Documentation/v12j_size_stress_runtime_pipeline_target_summary.csv`
- `Documentation/v12j_size_stress_runtime_pipeline_summary.csv`
- `Documentation/v0_12j_operativ_anbefaling.md`

## 20. v12k testet adaptiv oppfølging i stedet for mer pre-screening

`v12k` tok neste naturlige steg etter `v12j`:

- behold samme regime,
- behold samme full-followup som referanse,
- men bruk de første run-seedene pa hver base som adaptiv beslutning om hvem som far full oppfolging.

Det viktigste resultatet er:

- ingen adaptive policyer er naer-match mot `full_followup`
- `probe1_only` er den raske yttergrensen, men mister for mye kvalitet
- `probe2_top_half` er den mest balanserte adaptive kandidaten
- dette betyr at arbeidsgevinst antagelig finnes mer i smartere oppfølgingsstyring enn i ren pre-screening, men at første adaptive runde ikke er sterk nok til a erstatte full oppfolging

Viktige filer:

- `relational_universe_v12k_adaptive_followup_budget.py`
- `Documentation/v12k_adaptive_followup_budget.md`
- `Documentation/v12k_adaptive_followup_budget_target_summary.csv`
- `Documentation/v12k_adaptive_followup_budget_summary.csv`
- `Documentation/v0_12k_operativ_anbefaling.md`

## 21. v12l testet en ekte hybrid mellom screening og adaptiv oppfølging

`v12l` tok neste naturlige steg etter `v12k`:

- behold `band_zero_del` som arbeidsregime,
- behold `full_basis@0.50` som screeningreferanse,
- behold `probe2_top_half` som den mest balanserte adaptive follow-up-kandidaten,
- og kombiner dem i én faktisk workflow.

Det viktigste resultatet er:

- `full_basis__full_followup` holder seg som operativ referanse
- `spectral_only__full_followup` er den nærmeste same-budget-utfordreren på middelverdier
- men den er ikke robust nok split-for-split til å bli ny standard
- `full_basis__probe2_top_half` er den tydeligste reelle tidsutfordreren
- men den taper for mye i `best_hit` og `recall`

Den riktige lesningen er derfor:

- hybridsporet er fortsatt mer lovende enn mer pre-screening
- men den beste retningen videre er dypere adaptiv oppfølging, ikke mer finjustering av screeningbasiser

Viktige filer:

- `relational_universe_v12l_hybrid_screening_followup.py`
- `Documentation/v12l_hybrid_screening_followup.md`
- `Documentation/v12l_hybrid_screening_followup_target_summary.csv`
- `Documentation/v12l_hybrid_screening_followup_summary.csv`
- `Documentation/v0_12l_operativ_anbefaling.md`

## 22. v12m holdt screening fast og gikk dypere i adaptiv oppfølging

`v12m` tok neste naturlige steg etter `v12l`:

- behold `full_basis@0.50` som screeningreferanse,
- behold `full_followup` som kvalitet/nullpunkt,
- og test om en dypere adaptiv family kan hente inn mer kvalitet enn `probe2_top_half` uten å miste hele tidsgevinsten.

Det viktigste resultatet er:

- `probe3_top_half` matcher `full_followup` på mean `best_hit` og `recall`
- samtidig er `probe3_top_half` fortsatt tydelig raskere (`speedup ~= 1.358`)
- pairwise er fortsatt litt svakere enn referansen
- `probe2_top_two_thirds` og `probe3_top_two_thirds` kollapser i praksis til `full_followup` fordi de ender med å forlenge alle screenede baser

Den riktige lesningen er derfor:

- prosjektet har nå den første virkelig sterke adaptive utfordreren
- neste smale steg bør være en binær validering av `probe3_top_half` mot `full_followup`
- og eventuelt en liten beslutningsregelvariant rundt tie-break eller forlengelse, heller enn en ny bred policyfamilie

Viktige filer:

- `relational_universe_v12m_deeper_adaptive_followup.py`
- `Documentation/v12m_deeper_adaptive_followup.md`
- `Documentation/v12m_deeper_adaptive_followup_target_summary.csv`
- `Documentation/v12m_deeper_adaptive_followup_summary.csv`
- `Documentation/v0_12m_operativ_anbefaling.md`

## 23. v12n ga en strengere binær validering av probe3_top_half

`v12n` tok neste smale steg etter `v12m`:

- behold `full_basis@0.50` som fast screening,
- behold `full_followup` som referanse,
- behold `probe3_top_half` som hovedutfordrer,
- og test bare to små regelvarianter rundt den.

Det viktigste resultatet er:

- `probe3_top_half` er fortsatt tydelig raskere enn `full_followup`
- men den holder ikke lenger samme mean `best_hit` og `recall` i den strengere binærrunden
- tie-break-varianten hjelper ikke
- guarded-varianten hjelper heller ikke

Den riktige lesningen er derfor:

- optimismen fra `v12m` må dempes
- `probe3_top_half` er fortsatt en interessant rask utfordrer
- men den er ikke robust nok til å erstatte `full_followup`
- neste reelle forbedring må sannsynligvis komme fra en smartere tidlig beslutningsstatistikk eller et større valideringssett, ikke fra flere nesten-like lokale policyvarianter

Viktige filer:

- `relational_universe_v12n_binary_adaptive_validation.py`
- `Documentation/v12n_binary_adaptive_validation.md`
- `Documentation/v12n_binary_adaptive_validation_target_summary.csv`
- `Documentation/v12n_binary_adaptive_validation_summary.csv`
- `Documentation/v0_12n_operativ_anbefaling.md`

## 24. v13 validerte signalstyrken i stedet for å jage flere policyvarianter

Etter `v12n` tok prosjektet et bevisst steg tilbake fra workflow-optimalisering og spurte:

- hvilke geometriaksjer er faktisk stabile,
- hvilke langsomme driftstørrelser ser robuste ut,
- og er radius-/overlap-signalene sterke nok til å forsvare et større valideringssett?

Det viktigste resultatet er:

- `initial_avg_degree` er fortsatt den klart mest stabile normaliserte startfeature
- `initial_spectral_per_sqrtN` er den tydeligste ikke-trivielle stabile geometriaksen
- `mean_abs_delta_nodes_rel` og `mean_abs_delta_beta1_rel` er fortsatt eksakt null, men må fortsatt leses som mulige regime-/koblingsartefakter
- `mean_abs_delta_spectral_radius_rel` er den mest interessante ikke-trivielle quasi-invariant-kandidaten
- radius-signalet finnes fortsatt, men er ikke sterkt nok til at et større valideringssett er førsteprioritet
- overlap-signalet er enda svakere og bør ikke skaleres opp ennå

Den riktige lesningen er derfor:

- mer data er ikke første svar på alt
- større valideringssett er mer naturlig for stabile kontroller og eventuelle kryssregime-tester av quasi-invarianter
- radius-basisene trenger enten sterkere lokal evidens eller en bedre tverrregime-design før det lønner seg å skalere opp stort

Viktige filer:

- `relational_universe_v13_geometry_signal_validation.py`
- `Documentation/v13_geometry_signal_validation.md`
- `Documentation/v13_geometry_signal_stability_summary.csv`
- `Documentation/v13_quasi_invariant_bootstrap_summary.csv`
- `Documentation/v13_geometry_signal_validation_summary.csv`
- `Documentation/v0_13_operativ_anbefaling.md`

## 25. v13b skilte quasi-invariant-sporet fra radius-basis-sporet

`v13b` tok det neste metodisk riktige steget etter `v13`:

- ikke mer workflow-tuning
- ikke større radiusvalidering ennå
- men en smal kryssregime-test av de mest interessante driftssignalene

Det viktigste resultatet er:

- de eksakte null-driftene holder ikke gjennom hele den lokale regimefamilien
- `nodes`-driften bryter under delete-avvik
- `beta1`-driften bryter tydeligere under triad- og delete-avvik
- derfor skal disse null-driftene nå leses som regime-/koblingsartefakter, ikke som nye bevaringslover

Samtidig er det en positiv del:

- `mean_abs_delta_spectral_radius_rel` holder seg lav og top-3 i alle testede regimer
- dette gjør spektraldriften til den sterkeste ikke-trivielle quasi-invariant-kandidaten prosjektet har akkurat nå
- derfor er større valideringssett nå mest naturlig for målrettet spektral quasi-invariant-testing, ikke for nye radius-basis- eller workflow-runder

Viktige filer:

- `relational_universe_v13b_cross_regime_quasiinvariant_test.py`
- `Documentation/v13b_cross_regime_quasiinvariant_test.md`
- `Documentation/v13b_cross_regime_drift_summary.csv`
- `Documentation/v13b_cross_regime_anchor_delta_summary.csv`
- `Documentation/v0_13b_operativ_anbefaling.md`

## 26. v13c skalerte opp spektralsporet, men dempet anbefalingen

`v13c` tok det naturlige neste steget etter `v13b`:

- behold `band_zero_del` som fast anker
- behold `mean_abs_delta_spectral_radius_rel` som hovedsignal
- behold `dim_proxy` som sekundær kontroll
- skaler opp med litt bredere lokal familie og litt større budsjett

Det viktigste resultatet er:

- spektral relativ drift er fortsatt det sterkeste ikke-trivielle quasi-invariant-sporet
- men signalet er ikke skarpt nok til a sta alene som neste store valideringsmaal
- `dim_proxy` holder seg naer nok i flere regimer til at spektralsporet fortsatt ma leses som lokalt og delvis uavklart
- null-driftene for `nodes` og `beta1` bryter fortsatt off-anchor og skal fortsatt behandles som artefakter, ikke lover

Den riktige lesningen er derfor:

- `v13b` var nyttig som seleksjon av beste ikke-trivielle kandidat
- `v13c` er viktig fordi den demper fristelsen til a skalere opp for tidlig
- storre valideringssett er fortsatt `not_yet` for dette sporet

Viktige filer:

- `relational_universe_v13c_spectral_quasiinvariant_validation.py`
- `Documentation/v13c_spectral_quasiinvariant_validation.md`
- `Documentation/v13c_spectral_validation_focus_summary.csv`
- `Documentation/v13c_spectral_validation_anchor_delta_summary.csv`
- `Documentation/v0_13c_operativ_anbefaling.md`

## 27. v13d gjorde en ren knife-edge-sjekk av spektralsporet

`v13d` tok et enda smalere steg etter `v13c`:

- ikke bredere familie
- ikke større valideringssett
- bare mer lokalt budsjett pa de regimepunktene som fortsatt holdt spektralsporet blandet

Det viktigste resultatet er:

- `band_pdel_0005` er na `strong_local` for spektraldrift mot `dim_proxy`
- `bridge_00075_0000` og `bridge_0010_0000` er bare `good_but_local`
- null-driftene bryter fortsatt off-anchor
- derfor er spektralsporet fortsatt det beste ikke-trivielle sporet, men fortsatt ikke skarpt nok til at storre valideringssett er neste riktige steg

Dette er viktig fordi `v13d` ikke bare repeterer `v13c`; den tester nettopp om mer lokalt diskrimineringsbudsjett losner tvilen. Svaret er forelopig nei.

Viktige filer:

- `relational_universe_v13d_local_spectral_sharpening.py`
- `Documentation/v13d_local_spectral_sharpening.md`
- `Documentation/v13d_spectral_validation_local_summary.csv`
- `Documentation/v13d_spectral_validation_recommendations.csv`
- `Documentation/v0_13d_operativ_anbefaling.md`

## 28. v13e delte triad-korridoren i skarpe og blandede punkt

`v13e` tok neste naturlige steg etter `v13d`:

- dropp delete- og death-avvik
- fokuser bare på triad-korridoren
- legg inn mellompunkter rundt de tidligere triad-kandidatene

Det viktigste resultatet er:

- `bridge_000625_0000` blir `sharp_local`
- `bridge_000875_0000` blir `sharp_local`
- `bridge_0010_0000` er `good_but_local`
- `bridge_00075_0000` er fortsatt `mixed`

Dette er viktig fordi det gjør lesningen mer presis:

- problemet er ikke lenger "hele triad-korridoren er uklar"
- problemet er at ett smalt punkt fortsatt henger igjen som blandet

Viktige filer:

- `relational_universe_v13e_triad_corridor_sharpening.py`
- `Documentation/v13e_triad_corridor_sharpening.md`
- `Documentation/v13e_spectral_validation_corridor_summary.csv`
- `Documentation/v13e_spectral_validation_recommendations.csv`
- `Documentation/v0_13e_operativ_anbefaling.md`

## 29. v13f viste at notch-en ved bridge_00075_0000 ikke holder

`v13f` tok neste naturlige steg etter `v13e`:

- hold modellen fast
- behold bare den smale triad-familien
- legg inn ett finere punkt rett under og ett rett over `bridge_00075_0000`

Det viktigste resultatet er:

- `bridge_00075_0000` blir `sharp_local`
- `bridge_0006875_0000` blir `good_but_local`
- `bridge_0008125_0000` blir `good_but_local`
- `bridge_000875_0000` holder seg `sharp_local`
- notch-diagnosen ender pa `notch_not_supported`

Dette er viktig fordi det endrer lesningen av `v13e`:

- det tidligere blandede punktet ser ikke lenger ut som et ekte lokalt hakk
- den smale triad-korridoren er renere enn `v13e` alene tilsa
- større valideringssett blir derfor `yes_targeted` for akkurat dette spektralsporet

Viktige filer:

- `relational_universe_v13f_triad_notch_test.py`
- `Documentation/v13f_triad_notch_test.md`
- `Documentation/v13f_spectral_validation_local_summary.csv`
- `Documentation/v13f_spectral_validation_notch_summary.csv`
- `Documentation/v13f_spectral_validation_recommendations.csv`
- `Documentation/v0_13f_operativ_anbefaling.md`

## 30. v13g ga en strengere, men mer blandet triad-dom

`v13g` tok neste naturlige steg etter `v13f`:

- behold bare den rensede triad-korridoren
- bruk litt større lokalt budsjett
- test om spektralsporet holder i den smale familien uten notch-fortelling

Det viktigste resultatet er:

- `bridge_0006875_0000` holder som `good_but_local`
- `bridge_00075_0000` holder som `good_but_local`
- `bridge_0008125_0000` faller tilbake til `mixed`
- `bridge_000875_0000` faller ogsa tilbake til `mixed`

Dette er viktig fordi det korrigerer lesningen av `v13f`:

- `v13f` ryddet bort notch-fortellingen, men det betydde ikke at hele korridoren var stabil
- med mer lokalt budsjett spriker korridoren igjen pa oversiden
- større valideringssett skal derfor fortsatt ikke åpnes bredt

Viktige filer:

- `relational_universe_v13g_targeted_triad_validation.py`
- `Documentation/v13g_targeted_triad_validation.md`
- `Documentation/v13g_spectral_validation_corridor_summary.csv`
- `Documentation/v13g_spectral_validation_recommendations.csv`
- `Documentation/v0_13g_operativ_anbefaling.md`

## 31. v13h viste et lokalt gjenopprettet punkt pa oversiden

`v13h` tok neste naturlige steg etter `v13g`:

- behold bare sentrum og oversiden av triad-korridoren
- test finere punkt mellom `bridge_00075_0000` og `bridge_000875_0000`
- avgjor om oversiden degraderer monotont eller om det finnes et lokalt gjenopprettet punkt

Det viktigste resultatet er:

- `bridge_00075_0000` holder som `good_but_local`
- `bridge_00078125_0000` er `mixed`
- `bridge_0008125_0000` er fortsatt `mixed`
- `bridge_00084375_0000` blir `sharp_local`
- `bridge_000875_0000` blir `good_but_local`
- overgangsdiagnosen ender pa `upper_recovery_exists`

Dette er viktig fordi det endrer lesningen av `v13g`:

- oversiden ser ikke ut til a brytes ned jevnt
- det finnes minst ett lokalt gjenopprettet punkt pa oversiden
- men den samlede oversiden er fortsatt ikke ren nok til bredere validering

Viktige filer:

- `relational_universe_v13h_upper_triad_transition.py`
- `Documentation/v13h_upper_triad_transition.md`
- `Documentation/v13h_spectral_validation_transition_summary.csv`
- `Documentation/v13h_spectral_validation_upper_diagnosis.csv`
- `Documentation/v13h_spectral_validation_recommendations.csv`
- `Documentation/v0_13h_operativ_anbefaling.md`

## 32. v13i viste at recovery-punktet ikke holder

`v13i` tok neste naturlige steg etter `v13h`:

- behold bare recovery-punktet og de naermeste nabopunktene
- bruk finere bracketing rundt `bridge_00084375_0000`
- avgjor om det gjenopprettede oversidepunktet er ekte eller bare en lokal fluktuasjon

Det viktigste resultatet er:

- `bridge_0008125_0000` blir `sharp_local`
- `bridge_000828125_0000` blir `sharp_local`
- `bridge_00084375_0000` er bare `good_but_local`
- `bridge_000859375_0000` er `good_but_local`
- `bridge_000875_0000` er `good_but_local`
- recovery-diagnosen ender pa `recovery_not_supported`

Dette er viktig fordi det rydder opp i `v13h`:

- det gjenopprettede punktet ser ikke ut til å vaere en ekte topp
- oversiden har fortsatt struktur, men ikke den toppen vi trodde
- større valideringssett er derfor fortsatt ikke riktig neste steg

Viktige filer:

- `relational_universe_v13i_upper_recovery_refinement.py`
- `Documentation/v13i_upper_recovery_refinement.md`
- `Documentation/v13i_spectral_validation_refinement_summary.csv`
- `Documentation/v13i_spectral_validation_recovery_diagnosis.csv`
- `Documentation/v13i_spectral_validation_recommendations.csv`
- `Documentation/v0_13i_operativ_anbefaling.md`

## 33. Dagens operative lesning

Dagens beste korte lesning er:

- frontier-standard: `band_zero_del`
- aktiv forskningsfase: geometri / invariants / redusert basis / transfer
- screening-benchmark akkurat na: `full_basis`
- beste kompakte screeningpolicy akkurat na: `initial_spectral_per_sqrtN`, men arbeidsflytssignalet er fortsatt for svakt til å gjøre den til ny standard
- naer kompakt strukturkontroll: `initial_spectral_per_sqrtN + initial_dim_proxy`
- mest lovende ikke-trivielle geometrispor ellers: `initial_clustering` og `initial_dim_proxy`
- viktig advarsel: de tidligere eksakte null-driftene for `nodes` og `beta1` skal nå leses som regime-/koblingsartefakter, ikke som nye bevaringslover
- viktig nyansering: radius-transferen ser lokal ut; ved ytre triadpunkt og sterkere delete-avvik blir signalet svakere enn pa de naere regimepunktene
- viktig v13-dom: radius-/basis-signalet er fortsatt lovende, men ikke sterkt nok til at større valideringssett er førsteprioritet
- viktig v13-dom: overlap-/repair-signalet er foreløpig for svakt til å skaleres opp
- viktig v13-dom: `initial_avg_degree` og `initial_spectral_per_sqrtN` er sterke nok til å brukes som stabile kontroller i videre strukturarbeid
- viktig v13b-dom: `mean_abs_delta_spectral_radius_rel` er den mest interessante ikke-trivielle quasi-invariant-kandidaten akkurat nå
- viktig v13c-dom: spektralsporet er fortsatt best, men mer blandet enn `v13b` alene tilsa
- viktig v13c-dom: større valideringssett er fortsatt ikke førstevalg; vent til spektralsporet er skarpere eller bredere testet
- viktig v13d-dom: mer lokalt diskrimineringsbudsjett skjerper ikke hele spektralsporet nok; delete-punktet blir sterkt, men triadpunktene er fortsatt bare lokale
- viktig v13d-dom: større valideringssett er fortsatt `not_yet`
- viktig v13e-dom: triad-korridoren deler seg; to mellompunkter er skarpe, ett er godt men lokalt, og ett punkt er fortsatt blandet
- viktig v13e-dom: større valideringssett er fortsatt `not_yet`, men usikkerheten er nå lokalisert til et smalt triadpunkt
- viktig v13f-dom: det tidligere blandede triadpunktet holder ikke som eget notch under finere bracketing
- viktig v13f-dom: spektralsporet er fortsatt lokalt, men na renere i triad-korridoren enn `v13e` alene viste
- viktig v13f-dom: den lokale rensingen var reell, men bare som mellomsteg
- viktig v13g-dom: den rensede triad-korridoren holder ikke fullt ut under storre lokalt budsjett; oversiden faller tilbake til `mixed`
- viktig v13g-dom: større valideringssett er fortsatt `not_yet`
- viktig v13h-dom: oversiden degraderer ikke monotont; et lokalt gjenopprettet punkt finnes ved `bridge_00084375_0000`
- viktig v13h-dom: spektralsporet er fortsatt `mixed`, men blandingen er na mer strukturert enn i `v13g`
- viktig v13h-dom: større valideringssett er fortsatt `not_yet`
- viktig v13i-dom: det gjenopprettede oversidepunktet holder ikke under finere bracketing
- viktig v13i-dom: oversiden har fortsatt lokal struktur, men ikke en ren recovery-topp
- viktig v13i-dom: større valideringssett er fortsatt `not_yet`
- viktig v13j-dom: det smale bandet mellom `bridge_0008125_0000` og `bridge_000828125_0000` holder som den reneste lokale oversidesonen
- viktig v13j-dom: `bridge_0008203125_0000` kommer inn som nytt `sharp_local` mellompunkt, mens kontrollpunktene over bandet bare er `good_but_local`
- viktig v13j-dom: større valideringssett er fortsatt ikke bredt riktig, men et lite målrettet valideringssett er na `yes_targeted`
- viktig v13k-dom: det samme upper-bandet holder ikke rent nok under større lokalt budsjett
- viktig v13k-dom: bare `bridge_0008203125_0000` forblir `sharp_local`, mens resten av bandet glir tilbake til `good_but_local`
- viktig v13k-dom: større valideringssett gaar derfor tilbake til `not_yet`
- viktig v13l-dom: `bridge_0008203125_0000` holder fortsatt som sterkt punkt, men ikke som et rent løst pivot
- viktig v13l-dom: den nedre fine naboen `bridge_00081640625_0000` er ogsa `sharp_local`, mens `bridge_00082421875_0000` faller til `mixed`
- viktig v13l-dom: området ser derfor asymmetrisk og fortsatt blandet ut, og større valideringssett er fortsatt `not_yet`
- viktig v13m-dom: `bridge_00082421875_0000` holder ikke som et rent enkelt bruddpunkt
- viktig v13m-dom: den øvre fine siden `bridge_000826171875_0000` er `sharp_local`, mens både `bridge_000822265625_0000` og `bridge_00082421875_0000` er `mixed`
- viktig v13m-dom: usikkerheten sitter derfor i en liten lokal drop-sone rundt `0.000822`–`0.000824`, og større valideringssett er fortsatt `not_yet`

## 34. Hva som bor gjores videre

Hvis prosjektet fortsetter lokalt, er det naturlige neste steget ikke mer frontier-tuning, men videre strukturarbeid som tester:

- om de mest stabile startfeatures fortsatt holder som kontroller i nærliggende regimer,
- om den spektrale quasi-invarianten kan gjøres skarpere pa et bredere, men fortsatt kontrollert kryssregime-sett,
- og om radius-signalet kan styrkes metodisk uten å blande det sammen med quasi-invariantsporet.

Etter `v13i` er den oppdaterte anbefalingen:

- fortsett geometri-/invariantsporet heller enn frontier-tuning
- bruk `band_zero_del` som fast arbeidsregime
- bruk `initial_avg_degree` og `initial_spectral_per_sqrtN` som faste strukturkontroller
- behold `spectral_only` og `spectral_plus_clustering` som liten radius-duo, men ikke gjør dem til første mottaker av større valideringssett ennå
- prioriter fortsatt smal lokal avklaring av `mean_abs_delta_spectral_radius_rel`, na spesielt mellom `bridge_0008125_0000` og `bridge_000828125_0000` der signalet ser renest ut
- bruk `v13j` som ny lokal ground truth for oversiden; det smale bandet mellom `bridge_0008125_0000` og `bridge_000828125_0000` er na den reneste sonen
- bruk ikke `v13j` alene som siste sannhet; `v13k` viser at upper-bandet fortsatt er lovende, men blandet under hardere kontroll
- bruk ikke `v13k` alene som siste sannhet heller; `v13l` viser at sentrum fortsatt er sterkt, men at usikkerheten na sitter i den ovre bruddkanten
- bruk ikke `v13l` alene som siste sannhet heller; `v13m` viser at den ovre bruddkanten egentlig er en liten drop-sone, ikke bare ett punkt
- bruk ikke `v13m` alene som siste sannhet heller; `v13n` viser at den nedre drop-kanten heller ikke holder rent som egen knekk
- hold `dim_proxy` som sekundær kontroll i dette sporet
- bruk ikke større valideringssett bredt; `v13g` viser at korridoren fortsatt ikke er ren nok
- bruk heller ikke større valideringssett etter `v13i`; recovery-punktet falt bort under finere bracketing
- bruk heller ikke bred oppskalering etter `v13j`; neste gyldige steg er et lite, målrettet valideringssett rundt dette bandet
- bruk heller ikke bred oppskalering etter `v13k`; targeted-valideringen dempet optimismen igjen
- bruk heller ikke bred oppskalering etter `v13l`; neste gyldige steg er en enda smalere test av den ovre bruddkanten rundt `bridge_00082421875_0000`
- bruk heller ikke bred oppskalering etter `v13m`; neste gyldige steg er en smal test som skiller den nedre drop-kanten fra den øvre, ikke et større valideringssett
- bruk heller ikke bred oppskalering etter `v13n`; den nedre drop-kanten ser mer ut som en smal lokal usikkerhetssone enn en ren overgang
- ikke skaler opp overlap-/repair-validering før signalet er sterkere

## 35. v13j bekreftet et smalt rent upper-band

`v13j` tok neste naturlige steg etter `v13i`:

- behold bare den reneste delen av oversiden
- legg inn ett nytt mellompunkt mellom `bridge_0008125_0000` og `bridge_000828125_0000`
- bruk to kontrollpunkter over bandet
- avgjor om det finnes et ekte lite clean band, ikke bare enkeltpunkter

Det viktigste resultatet er:

- `bridge_0008125_0000` er fortsatt `sharp_local`
- `bridge_0008203125_0000` blir `sharp_local`
- `bridge_000828125_0000` er fortsatt `sharp_local`
- `bridge_0008359375_0000` og `bridge_00084375_0000` er bare `good_but_local`
- banddiagnosen ender pa `clean_band_supported`

Dette er viktig fordi det rydder opp i `v13i`:

- den reneste delen av oversiden er ikke bare to tilfeldige gode punkt
- det finnes et lite sammenhengende lokalt band der spektraldriften er tydelig bedre enn ved kontrollpunktene rett over
- bredere validering er fortsatt ikke riktig, men et lite målrettet valideringssett er na metodisk rimelig

Viktige filer:

- `relational_universe_v13j_upper_clean_band_refinement.py`
- `Documentation/v13j_upper_clean_band_refinement.md`
- `Documentation/v13j_spectral_validation_refinement_summary.csv`
- `Documentation/v13j_spectral_validation_band_diagnosis.csv`
- `Documentation/v13j_spectral_validation_recommendations.csv`
- `Documentation/v0_13j_operativ_anbefaling.md`

## 36. v13k viste at upper-bandet fortsatt er blandet under hardere kontroll

`v13k` tok neste naturlige steg etter `v13j`:

- behold akkurat samme lille upper-band
- behold samme kontrollpunkter
- behold samme målesystem
- bruk bare et større lokalt budsjett

Det viktigste resultatet er:

- `bridge_0008203125_0000` holder som `sharp_local`
- `bridge_0008125_0000` glir tilbake til `good_but_local`
- `bridge_000828125_0000` glir tilbake til `good_but_local`
- kontrollpunktene over bandet er også `good_but_local`
- banddiagnosen ender pa `sampling_ambiguous`

Dette er viktig fordi det korrigerer lesningen av `v13j`:

- `v13j` fant et ekte lovende lokalt band
- men `v13k` viser at bandet ikke er rent nok til å kalles målrettet validert
- større valideringssett er derfor fortsatt ikke riktig neste steg

Viktige filer:

- `relational_universe_v13k_targeted_upper_band_validation.py`
- `Documentation/v13k_targeted_upper_band_validation.md`
- `Documentation/v13k_spectral_validation_refinement_summary.csv`
- `Documentation/v13k_spectral_validation_band_diagnosis.csv`
- `Documentation/v13k_spectral_validation_recommendations.csv`
- `Documentation/v0_13k_operativ_anbefaling.md`

## 37. v13l viste at upper-området fortsatt er asymmetrisk og blandet

`v13l` tok neste naturlige steg etter `v13k`:

- behold bare området rundt `bridge_0008203125_0000`
- legg inn ett finere punkt rett under og ett rett over
- behold de ytre flankepunktene
- avgjor om sentrum faktisk er et løst pivotpunkt

Det viktigste resultatet er:

- `bridge_00081640625_0000` blir `sharp_local`
- `bridge_0008203125_0000` blir fortsatt `sharp_local`
- `bridge_00082421875_0000` faller til `mixed`
- `bridge_000828125_0000` er fortsatt `sharp_local`
- pivotdiagnosen ender pa `sampling_ambiguous`

Dette er viktig fordi det skjerper lesningen av `v13k`:

- sentrumspunktet er fortsatt lovende
- men problemet er ikke bare "for lite budsjett"
- området rundt ser ut til a ha en tydelig ovre bruddkant, ikke en ren symmetrisk topp

Viktige filer:

- `relational_universe_v13l_local_upper_pivot_refinement.py`
- `Documentation/v13l_local_upper_pivot_refinement.md`
- `Documentation/v13l_spectral_validation_refinement_summary.csv`
- `Documentation/v13l_spectral_validation_pivot_diagnosis.csv`
- `Documentation/v13l_spectral_validation_recommendations.csv`
- `Documentation/v0_13l_operativ_anbefaling.md`

## 38. v13m viste at den øvre bruddkanten egentlig er en liten drop-sone

`v13m` tok neste naturlige steg etter `v13l`:

- behold bare området rundt `bridge_00082421875_0000`
- legg inn ett finere punkt rett under og ett rett over
- behold flankepunktene
- avgjor om det blandede punktet er en ekte lokal bruddkant

Det viktigste resultatet er:

- `bridge_0008203125_0000` er fortsatt `sharp_local`
- `bridge_000822265625_0000` blir `mixed`
- `bridge_00082421875_0000` er fortsatt `mixed`
- `bridge_000826171875_0000` blir `sharp_local`
- `bridge_000828125_0000` er fortsatt `sharp_local`
- breakdiagnosen ender pa `sampling_ambiguous`

Dette er viktig fordi det skjerper lesningen av `v13l`:

- den svake sonen er ikke bare ett punkt
- den ser ut som en liten lokal drop-sone mellom to skarpere flankesoner
- større valideringssett er derfor fortsatt ikke riktig neste steg

Viktige filer:

- `relational_universe_v13m_upper_break_edge_test.py`
- `Documentation/v13m_upper_break_edge_test.md`
- `Documentation/v13m_spectral_validation_refinement_summary.csv`
- `Documentation/v13m_spectral_validation_break_diagnosis.csv`
- `Documentation/v13m_spectral_validation_recommendations.csv`
- `Documentation/v0_13m_operativ_anbefaling.md`

## 39. v13n viste at den nedre drop-kanten heller ikke er rent løst

`v13n` tok neste naturlige steg etter `v13m`:

- behold bare den nedre delen av drop-sonen
- legg inn ett finere punkt rett under `bridge_000822265625_0000`
- legg inn ett finere punkt rett over
- behold flankepunktene
- avgjor om den nedre kanten er en egen lokal knekk

Det viktigste resultatet er:

- `bridge_0008203125_0000` er fortsatt `sharp_local`
- `bridge_0008212890625_0000` blir `good_but_local`
- `bridge_000822265625_0000` er fortsatt `mixed`
- `bridge_0008232421875_0000` er `mixed`
- `bridge_00082421875_0000` er fortsatt `mixed`
- breakdiagnosen ender fortsatt pa `sampling_ambiguous`

Dette er viktig fordi det skjerper lesningen av `v13m`:

- den nedre kanten holder ikke som en egen ren overgang
- margin- og delta-signalet peker faktisk bort fra en skarp knekk
- området ser mer ut som et smalt lokalt plateau eller en usikkerhetssone enn som et klart brudd
- større valideringssett er derfor fortsatt ikke riktig neste steg

Viktige filer:

- `relational_universe_v13n_lower_drop_edge_test.py`
- `Documentation/v13n_lower_drop_edge_test.md`
- `Documentation/v13n_spectral_validation_refinement_summary.csv`
- `Documentation/v13n_spectral_validation_break_diagnosis.csv`
- `Documentation/v13n_spectral_validation_recommendations.csv`
- `Documentation/v0_13n_operativ_anbefaling.md`
