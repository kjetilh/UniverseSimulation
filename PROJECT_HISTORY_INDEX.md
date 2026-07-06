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

## 0zr. v15ar viste at high-grensen leses skarpere som et horisont-kart

Etter at `v15aq` viste at impulse-vinduet ga litt struktur, men ikke leste failed-probe-sporet rent nok, tok `v15ar` neste smale steg:

- behold det fokuserte `v15ap`-settet
- bruk ingen nye simuleringer
- les high-grensen gjennom nar high starter, hvor sent den siste high-opptredenen kommer, og hvor stor faktisk high-retensjon runet har i dette vinduet
- avgjor om hold, terminal probe, failed probe og no-high-presens skiller lag bedre som horisont-forlop

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `5002161`, `5002205` og `5002241` blir `established_hold_horizon`
- `5002220` blir `terminal_probe_horizon`
- `5002221` blir `failed_probe_horizon`
- `5002240`, `5002272`, `5002273` og `5002307` blir `no_high_presence`
- diagnosen ender pa `horizon_map_supported`

Dette betyr:

- dette ga ekte ny viten utover `v15aq`
- high-grensen er bedre lest som et lite horisont-kart enn som bare launch-impuls
- failed-probe-sporet er na skarpere og mer disiplinert lest
- neste riktige steg er derfor en liten holdout-test av horisont-kartet, ikke en bredere scan

Viktige filer:

- `relational_universe_v15ar_high_retention_horizon_lab.py`
- `Documentation/v15ar_high_retention_horizon_lab.md`
- `Documentation/v15ar_high_retention_horizon_runs.csv`
- `Documentation/v15ar_high_retention_horizon_aggregate.csv`
- `Documentation/v15ar_high_retention_horizon_diagnosis.csv`
- `Documentation/v15ar_high_retention_horizon_target_summary.csv`
- `Documentation/v0_15ar_operativ_anbefaling.md`

## 0zs. v15as viste at bare no-high-presens holder rent i naerliggende horizon-holdouts

Etter at `v15ar` ga ekte ny viten som et lite horisont-kart, tok `v15as` neste naturlige steg:

- behold bare fire representative horisontankre
- behold samme lokale `t48_g202` add_chord-oppsett
- rerun bare to naerliggende seeds rundt hvert anker
- avgjor om horisont-kartet faktisk holder lokalt utover anker-runene

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `no_high_presence` holder rent med `match_rate = 1.000`
- `established_hold_horizon` holder ikke rent; ett holdout blir `mixed_horizon` og ett faller til `no_high_presence`
- `terminal_probe_horizon` faller helt til `no_high_presence`
- `failed_probe_horizon` faller ogsa helt til `no_high_presence`
- diagnosen ender pa `horizon_map_holdout_mixed`

Dette betyr:

- `v15ar` sitt horisont-kart ga ekte ny ankerkunnskap
- men `v15as` viser at bare `no_high_presence` ser lokalt robust ut sa langt
- de andre horizon-familiene ligger pa en skjotere high-grense og kollapser ofte ned til fravaer av high i naerliggende seeds
- neste riktige steg er derfor en enda smalere observabel rundt failed-probe og terminal-probe-grensen, ikke mer bred horisont-ekspansjon

Viktige filer:

- `relational_universe_v15as_horizon_map_holdout.py`
- `Documentation/v15as_horizon_map_holdout.md`
- `Documentation/v15as_horizon_map_holdout_runs.csv`
- `Documentation/v15as_horizon_map_holdout_aggregate.csv`
- `Documentation/v15as_horizon_map_holdout_diagnosis.csv`
- `Documentation/v15as_horizon_map_holdout_target_summary.csv`
- `Documentation/v0_15as_operativ_anbefaling.md`

## 0zt. v15at viste at holdout-kollapsen leses renere som et burst-kart

Etter at `v15as` viste at bare `no_high_presence` holder rent lokalt, tok `v15at` neste smale steg:

- behold samme fire anker-run og aatte holdout-run
- behold samme lokale `t48_g202` add_chord-oppsett
- les boundary-sonen som et lite burst-kart i stedet for bare horisont-etiketter
- avgjor om holdout-kollapsen egentlig er manglende high, fading high eller ekte probe

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- anker-runene deler seg rent i `sustained_hold_burst`, `terminal_compact_burst`, `early_failed_burst` og `no_high_burst`
- holdout-runene er `0.875` `no_high_burst`
- bare ett holdout-run, `5002233`, holder et lite restspor som `fading_late_burst`
- diagnosen ender pa `burst_map_sharpens_holdout_collapse`

Dette betyr:

- burst-observabelen er bedre enn horisont alene for a beskrive holdoutene
- den skjore high-grensen ser mest ut som en no-high-kollaps med ett lite fading-restspor
- neste riktige steg er derfor a forklare akkurat fading-sporet, ikke a presse holdout-kartet bredere

Viktige filer:

- `relational_universe_v15at_high_burst_window_lab.py`
- `Documentation/v15at_high_burst_window_lab.md`
- `Documentation/v15at_high_burst_window_runs.csv`
- `Documentation/v15at_high_burst_window_aggregate.csv`
- `Documentation/v15at_high_burst_window_diagnosis.csv`
- `Documentation/v15at_high_burst_window_target_summary.csv`
- `Documentation/v0_15at_operativ_anbefaling.md`

## 0zu. v15au viste at restsporet er et eget post-peak-fade-forlop

Etter at `v15at` isolerte ett lite `fading_late_burst`-restspor, tok `v15au` neste smale steg:

- behold bare triplet-en `anchor_hold`, `fading_holdout` og `no_high_holdout`
- behold samme lokale placement og seed-familie
- bruk ingen bredere scan
- les bare hva som skjer etter peak-bursten

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `anchor_hold` blir `post_peak_hold`
- `fading_holdout` blir `post_peak_fade`
- `no_high_holdout` blir `no_launch_tail`
- diagnosen ender pa `post_peak_map_supported`

Dette betyr:

- restsporet er ikke bare "mindre hold"
- det er et eget lite mellomforlop der en ekte peak bygges, men high glipper raskt tilbake i mid/lav tail
- boundary-familien er na best lest som rent hold, rent no-high og et lite post-peak-fade-mellomforlop
- neste riktige steg er derfor en minimal holdout rundt `post_peak_fade`

Viktige filer:

- `relational_universe_v15au_post_peak_fade_explainer.py`
- `Documentation/v15au_post_peak_fade_explainer.md`
- `Documentation/v15au_post_peak_fade_runs.csv`
- `Documentation/v15au_post_peak_fade_diagnosis.csv`
- `Documentation/v15au_post_peak_fade_target_summary.csv`
- `Documentation/v0_15au_operativ_anbefaling.md`

## 0zv. v15av viste at post-peak-fade best leses som et singleton-overgangspunkt

Etter at `v15au` viste at restsporet er et ekte `post_peak_fade`-forlop, tok `v15av` neste smale steg:

- behold bare placement `2`
- behold bare den lille overgangen rundt seed `231`
- rerun bare to nye nedre naboer, `215` og `223`
- bruk `239` og `247` bare som ovre kontekst

Det viktigste resultatet er:

- artifact-control holder fortsatt rent
- `231` holder som `post_peak_fade`
- begge nye nedre nabopunkter, `215` og `223`, blir `no_launch_tail`
- `239` holder som `post_peak_hold`
- `247` holder som `no_launch_tail`
- diagnosen ender pa `fade_singleton_not_supported`

Dette betyr:

- `post_peak_fade` er ekte nok som et lokalt forlop
- men det holder ikke som et lite naboband rundt `231`
- det ser best ut som et singleton-aktig overgangspunkt mellom stabilt hold og rent no-launch
- neste riktige steg bor derfor ikke vaere bredere fade-scan, men et nytt defect-sporsmal eller en annen observabel

Viktige filer:

- `relational_universe_v15av_post_peak_fade_holdout.py`
- `Documentation/v15av_post_peak_fade_holdout.md`
- `Documentation/v15av_post_peak_fade_holdout_runs.csv`
- `Documentation/v15av_post_peak_fade_holdout_diagnosis.csv`
- `Documentation/v15av_post_peak_fade_holdout_target_summary.csv`
- `Documentation/v0_15av_operativ_anbefaling.md`

## 0zw. v15aw viste at local_swap ikke generaliserer rent som add_chord pa core-shell-observabelen

Etter at add_chord-sporet rundt hold/no-high-overgangen var presset langt nok, tok `v15aw` et nytt smalt defect-sporsmal:

- legg add_chord-fade-sporet til side
- behold samme operative regime `band_zero_del`
- behold single-defect recurrence-sporet
- bruk den samme core-shell-observabelen som fungerte godt for add_chord
- test bare `local_swap` ved `48` og `96`

Det viktigste resultatet er:

- artifact-control holder rent
- ved `48` er alle 8 run `stable_core_variable_shell`
- ved `96` er bare 1 av 8 run `stable_core_variable_shell`
- `96` er i stedet dominert av `diffuse_shell_recurrence` (`0.625`) og litt `mixed_core_shell` (`0.250`)
- diagnosen ender pa `local_swap_core_shell_mixed`

Dette betyr:

- den nye observabelen generaliserer ikke rent fra add_chord til local_swap
- `local_swap` har fortsatt sterk sen morfologisk retur, men den holder seg mye renere som kjerne+rand ved `48` enn ved `96`
- neste riktige steg er derfor ikke en bred ny defect-scan, men a avgjore om dette er en ekte strukturert size-splitt

Viktige filer:

- `relational_universe_v15aw_local_swap_core_shell_lab.py`
- `Documentation/v15aw_local_swap_core_shell_lab.md`
- `Documentation/v15aw_local_swap_core_shell_runs.csv`
- `Documentation/v15aw_local_swap_core_shell_aggregate.csv`
- `Documentation/v15aw_local_swap_core_shell_diagnosis.csv`
- `Documentation/v15aw_local_swap_core_shell_target_summary.csv`
- `Documentation/v0_15aw_operativ_anbefaling.md`

## 0zx. v15ax viste at local_swap faktisk har en strukturert 48-vs-96 size-splitt

Etter at `v15aw` ga et tydelig 48-vs-96-skille, tok `v15ax` neste lille forklaringsrunde:

- kjor ingen nye simuleringer
- bruk bare `v15aw`-run-radene
- avgjor om 48-vs-96-forskjellen er sterk nok til a kalles ny viten
- kartlegg om det fortsatt finnes sma `96`-lommer som holder core+shell lokalt

Det viktigste resultatet er:

- `48` holder rent som `stable_core_variable_shell` i alle 8 run
- `96` er dominert av `diffuse_shell_recurrence`
- kjerneandelen faller kraftig fra `0.692` til `0.340`
- randandelen stiger fra `0.296` til `0.408`
- det finnes bare en liten `96`-lomme som fortsatt holder `stable_core_variable_shell`
- diagnosen ender pa `local_swap_size_split_supported`

Dette betyr:

- `local_swap` har na en ekte strukturert size-splitt pa denne observabelen
- `48` leses best som ren kjerne+rand-recurrence
- `96` leses best som et mer diffust shell-regime med noen fa resterende core+shell-lommer
- neste riktige steg er derfor a forklare disse `96`-lommene, ikke a scanne bredere

Viktige filer:

- `relational_universe_v15ax_local_swap_size_split_explainer.py`
- `Documentation/v15ax_local_swap_size_split_explainer.md`
- `Documentation/v15ax_local_swap_size_split_aggregate.csv`
- `Documentation/v15ax_local_swap_size_split_placements.csv`
- `Documentation/v15ax_local_swap_size_split_diagnosis.csv`
- `Documentation/v0_15ax_operativ_anbefaling.md`

## 0zy. v15ay viste at 96-lommen best leses som kompakt støtte med dempet rare-turnover

Etter at `v15ax` viste en ekte `48`-vs-`96` size-splitt i local_swap-sporet, tok `v15ay` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `96`-runene fra `v15aw`
- forklar den ene `96`-lommen som fortsatt holder `stable_core_variable_shell`
- sammenlign den med samme placement ved annet growth-seed og noen naere ikke-lommer

Det viktigste resultatet er:

- `artifact_control` arves rent fra `v15aw`
- `growth_seed 101`, `placement 3` holder som `pocket_anchor`
- samme placement ved `growth_seed 202` faller tilbake til `diffuse_shell_recurrence`
- pocket-caset har den mest kompakte relative stotten i `96`-familien (`ball3_over_ball1 = 2.600`)
- pocket-caset holder ogsa lav `rare_share` (`0.149`) og klart hoyere coarse return (`0.785`) enn kontrollene
- diagnosen ender pa `compact_low_rare_pocket_supported`

Dette betyr:

- `96`-lommen ser ikke lenger ut som ren reststoy
- den best leses som et kompakt stottecase med dempet rare-turnover
- placement alene er ikke forklaringen, siden samme placement ved annet growth-seed ikke holder
- neste riktige steg er derfor a forklare seed-flippen inne i placement `3`, ikke a scanne bredere igjen

Viktige filer:

- `relational_universe_v15ay_local_swap_96_pocket_explainer.py`
- `Documentation/v15ay_local_swap_96_pocket_explainer.md`
- `Documentation/v15ay_local_swap_96_pocket_rows.csv`
- `Documentation/v15ay_local_swap_96_pocket_aggregate.csv`
- `Documentation/v15ay_local_swap_96_pocket_diagnosis.csv`
- `Documentation/v0_15ay_operativ_anbefaling.md`

## 0zz. v15az viste at p3-flippen best leses som en kjerneforsterknings-flip, ikke bare en geometri-flip

Etter at `v15ay` viste at `96`-lommen ikke er ren reststoy, tok `v15az` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `target 96`
- fokuser bare pa `placement 3`
- sammenlign `growth_seed 101` og `growth_seed 202` direkte
- bruk noen fa kontroller bare for a holde forklaringen aelig

Det viktigste resultatet er:

- `p3`-casene ligger relativt naert i kompakthetsgeometri (`ball3_over_ball1 = 2.600` vs `2.786`)
- de skiller lag hardt i kjerneforsterkning og haleomfang
- `101/p3` har `core/ball1 = 3.267`, `tail/ball1 = 4.047`, `core/shell = 1.960`
- `202/p3` har bare `core/ball1 = 0.571`, `tail/ball1 = 1.136`, `core/shell = 0.500`
- diagnosen ender pa `p3_seed_flip_is_core_amplification_flip`
- men et ikke-pocket-case, `202/p0`, har enda hoyere core-forsterkning, sa denne aksen er ikke en full global lov

Dette betyr:

- seed-flippen i `p3` leses best som et lokalt skifte mellom ekspandert, vedvarende kjerne og komprimert shell-retur
- placement-geometrien alene er ikke nok til a forklare flippen
- men ren kjerneforsterkning alene er heller ikke en full forklaring globalt
- neste riktige steg er derfor a forklare hva som holder `202/p3` komprimert, ikke a scanne bredere

Viktige filer:

- `relational_universe_v15az_local_swap_p3_seed_flip_explainer.py`
- `Documentation/v15az_local_swap_p3_seed_flip_explainer.md`
- `Documentation/v15az_local_swap_p3_seed_flip_rows.csv`
- `Documentation/v15az_local_swap_p3_seed_flip_summary.csv`
- `Documentation/v15az_local_swap_p3_seed_flip_diagnosis.csv`
- `Documentation/v0_15az_operativ_anbefaling.md`

## 10a. v15ba viste at den diffuse siden av p3-flippen best leses som komprimert shell-retur

Etter at `v15az` viste at `p3`-flippen ikke bare er en geometri-flip, tok `v15ba` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `96`-radene fra `v15aw`
- behold `pocket_anchor` og `p3_diffuse_flip`
- legg til noen fa lokale kontroller for a holde lesningen aelig
- avgjor om `202/p3` best leses som svak pocket eller som en egen komprimert shell-retur

Det viktigste resultatet er:

- `202/p3` holder fortsatt tydelig recurrence (`coarse return = 0.631`)
- men den er sterkt shell-dominert: `shell+rare = 0.778`
- den har lav `core/shell = 0.500`
- den har lav `tail_density = 0.442`
- pocket-caset `101/p3` er langt mindre shell-dominert (`shell+rare = 0.437`) og langt tettere i tailen (`tail_density = 0.698`)
- diagnosen ender pa `compressed_shell_return_supported`

Dette betyr:

- `202/p3` ser ikke best ut som en svak eller mislykket pocket
- den best leses som en komprimert shell-retur: recurrence holder seg i live, men i en liten, rand-/rare-dominert modus
- dette gir ny viten fordi det skiller den diffuse siden av `p3`-flippen fra bare "lavere kjerneforsterkning"
- neste riktige steg er derfor a forklare hvorfor akkurat `growth_seed 202` holder `p3` i denne shell-returen, sammenlignet med andre `growth_seed 202`-caser

Viktige filer:

- `relational_universe_v15ba_local_swap_compressed_shell_explainer.py`
- `Documentation/v15ba_local_swap_compressed_shell_explainer.md`
- `Documentation/v15ba_local_swap_compressed_shell_rows.csv`
- `Documentation/v15ba_local_swap_compressed_shell_summary.csv`
- `Documentation/v15ba_local_swap_compressed_shell_diagnosis.csv`
- `Documentation/v0_15ba_operativ_anbefaling.md`

## 10b. v15bb viste at growth_seed 202 faktisk fyller fire ulike lokale modi

Etter at `v15ba` skilte ut `202/p3` som komprimert shell-retur, tok `v15bb` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `target 96`, `growth_seed 202`
- behold alle fire plasseringer `p0`-`p3`
- avgjor om disse bare er grader av samme diffuse restkategori, eller om de faktisk fyller ulike lokale modi

Det viktigste resultatet er:

- `p0` blir `high_core_mixed_mode`
- `p1` blir `wide_diffuse_retention_mode`
- `p2` blir `dissipative_rare_shell_mode`
- `p3` blir `compressed_shell_return_mode`
- diagnosen ender pa `growth202_mode_map_supported`

Dette betyr:

- `growth_seed 202`-familien kollapser ikke til én diffus restkategori
- den fyller et lite, strukturert moduskart med fire ulike lokale dynamikkroller
- dette er ny viten fordi det gjør `p3`-shell-returen til en del av en intern lokal atlaslesning, ikke bare et enkelt isolert unntak
- neste riktige steg er derfor a forklare hvorfor `p3` velger komprimert shell-retur mens `p1` og `p2` velger andre diffuse modi

Viktige filer:

- `relational_universe_v15bb_local_swap_growth202_mode_map.py`
- `Documentation/v15bb_local_swap_growth202_mode_map.md`
- `Documentation/v15bb_local_swap_growth202_mode_rows.csv`
- `Documentation/v15bb_local_swap_growth202_mode_aggregate.csv`
- `Documentation/v15bb_local_swap_growth202_mode_diagnosis.csv`
- `Documentation/v0_15bb_operativ_anbefaling.md`

## 10c. v15bc viste at p3 skilles fra p1 og p2 langs to ulike akser

Etter at `v15bb` viste et lite internt moduskart i `growth_seed 202`, tok `v15bc` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `p1`, `p2` og `p3`
- sammenlign `p3` direkte mot de to mest informative nabomodusene
- avgjor om `p3` bare er en mellomting, eller om den faktisk skiller seg pa to forskjellige maater

Det viktigste resultatet er:

- `p3_vs_p1` blir `compressed_vs_wide_retention`
- `p3_vs_p2` blir `retained_vs_dissipative_shell`
- diagnosen ender pa `p3_boundary_contrast_supported`

Konkret:

- mot `p1` taper `p3` noe coarse return (`-0.215`), men blir samtidig mer komprimert med mindre tail-union (`-37`) og lavere tail-density (`-0.078`)
- mot `p2` vinner `p3` klart pa retention (`+0.185` coarse gap), har hoyere `core/shell` (`+0.206`) og lavere rare-share (`-0.095`)

Dette betyr:

- `p3` er ikke bare en vag mellomting mellom `p1` og `p2`
- den skiller seg fra `p1` langs en kompresjon-vs-bred-retention-akse
- den skiller seg fra `p2` langs en retention-vs-dissipativ-rare-shell-akse
- neste riktige steg er derfor a lete etter en liten felles triggerakse som avgjor hvilken av disse tre diffuse modusene systemet velger

Viktige filer:

- `relational_universe_v15bc_local_swap_p3_vs_p1_p2_contrast.py`
- `Documentation/v15bc_local_swap_p3_vs_p1_p2_contrast.md`
- `Documentation/v15bc_local_swap_p3_vs_p1_p2_rows.csv`
- `Documentation/v15bc_local_swap_p3_vs_p1_p2_pairs.csv`
- `Documentation/v15bc_local_swap_p3_vs_p1_p2_diagnosis.csv`
- `Documentation/v0_15bc_operativ_anbefaling.md`

## 10d. v15bd viste at growth_seed-202-modiene faktisk kan ordnes av en liten dynamisk triggerakse

Etter at `v15bc` skilte `p3` fra `p1` og `p2` langs to forskjellige akser, tok `v15bd` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `target 96`, `growth_seed 202`
- test et lite sett tolkbare kandidat-akser
- avgjor om én liten akse faktisk ordner `p1 > p3 > p2`

Det viktigste resultatet er:

- `retention_core_axis = coarse_return + core_to_shell` ordner `p1 > p3 > p2` renest
- den ordnede marginen er `0.390`
- alle de beste aksene er dynamiske
- stotteaksene holder ikke ren ordering
- diagnosen ender pa `retention_core_axis_supported`

Dette betyr:

- growth_seed-202-splittelsen leses ikke best som en enkel geometriakse
- den leses best som en liten dynamisk retention+kjerne-akse
- neste riktige steg er derfor a forklare hva som faktisk driver denne aksen lokalt

Viktige filer:

- `relational_universe_v15bd_local_swap_trigger_axis_lab.py`
- `Documentation/v15bd_local_swap_trigger_axis_lab.md`
- `Documentation/v15bd_local_swap_trigger_axis_placements.csv`
- `Documentation/v15bd_local_swap_trigger_axis_candidates.csv`
- `Documentation/v15bd_local_swap_trigger_axis_diagnosis.csv`
- `Documentation/v0_15bd_operativ_anbefaling.md`

## 10e. v15be viste at triggeraksen er en ekte to-komponentsplitt, ikke ett enkelt maal

Etter at `v15bd` fant en liten, ren triggerakse, tok `v15be` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `v15bd`-akseobservablene
- dekomponer aksedeltaene for `p1_vs_p3`, `p3_vs_p2` og `p1_vs_p2`
- avgjor om aksen drives av én dominerende komponent eller av en liten blanding

Det viktigste resultatet er:

- `p1_vs_p3` blir `core_amplification_dominant`
- `p3_vs_p2` blir `balanced_two_component_gap`
- `p1_vs_p2` blir ogsa `balanced_two_component_gap`
- mean core-share av aksedelta er `0.591` mot coarse-share `0.409`
- diagnosen ender pa `two_component_axis_supported`

Dette betyr:

- aksen fra `v15bd` er ikke bare en pen score
- den bærer faktisk to forskjellige lokale gaptyper
- `p1 > p3` drives mest av kjerneforsterkning (`core_to_shell`)
- `p3 > p2` drives av en mer balansert blanding av retention og kjerneforsterkning
- neste riktige steg er derfor a forklare hvorfor ett gap blir core-dominert mens det andre blir mer balansert

Viktige filer:

- `relational_universe_v15be_local_swap_trigger_axis_component_lab.py`
- `Documentation/v15be_local_swap_trigger_axis_component_lab.md`
- `Documentation/v15be_local_swap_trigger_axis_pairs.csv`
- `Documentation/v15be_local_swap_trigger_axis_aggregate.csv`
- `Documentation/v0_15be_operativ_anbefaling.md`

## 10f. v15bf viste at de to nabogapene inne i triggeraksen heller ikke er samme type overgang

Etter at `v15be` viste at triggeraksen er en liten to-komponentsplitt, tok `v15bf` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `v15bd`- og `v15be`-observablene
- sammenlign `p1_vs_p3` direkte mot `p3_vs_p2`
- avgjor om de to nabogapene bare er svakere/sterkere versjoner av samme overgang

Det viktigste resultatet er:

- `p1_vs_p3` blir `core_shape_separation`
- `p3_vs_p2` blir `retention_plus_shell_drag`
- `p1_vs_p2` blir fortsatt bare `mixed_gap_family`
- diagnosen ender pa `neighbor_gap_asymmetry_supported`

Dette betyr:

- growth_seed-202-splittelsen har mer lokal struktur enn bare én pen akse
- øvre nabogap leses best som sterkere kjerneform-separasjon
- nedre nabogap leses best som en blandet overgang der taperen baade mister retention og tar pa seg tyngre shell-byrde
- neste riktige steg er derfor a forklare shell-drag-siden av den balanserte overgangen

Viktige filer:

- `relational_universe_v15bf_local_swap_gap_asymmetry_explainer.py`
- `Documentation/v15bf_local_swap_gap_asymmetry_explainer.md`
- `Documentation/v15bf_local_swap_gap_asymmetry_rows.csv`
- `Documentation/v15bf_local_swap_gap_asymmetry_diagnosis.csv`
- `Documentation/v0_15bf_operativ_anbefaling.md`

## 10g. v15bg viste at shell-drag-siden av p3 > p2 nesten helt er rare-last, ikke bredere shell

Etter at `v15bf` skilte ut `p3 > p2` som en egen `retention_plus_shell_drag`-overgang, tok `v15bg` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `target 96`, `growth_seed 202`
- dekomponer shell-draget i ordinær shell-share vs rare-share
- avgjor om taperen egentlig bare har mer shell, eller om den spesielt blåses opp av rare-last

Det viktigste resultatet er:

- `p2` og `p3` har nesten lik shell-share (`0.442` vs `0.444`)
- men `p2` har klart hoyere rare-share (`0.429` vs `0.333`)
- rare-andelen dekker i praksis hele shell-draget (`rare_fraction_of_shell_drag ~= 1.031`)
- diagnosen ender pa `rare_loaded_shell_drag_supported`

Dette betyr:

- den balanserte `p3 > p2`-overgangen er ikke best lest som bredere ordinær shell
- den leses best som en overgang der taperen bærer tung rare-last samtidig som retentionen er svakere
- neste riktige steg er derfor a forklare hva som trigger rare-last i den dissipative `p2`-retningen

Viktige filer:

- `relational_universe_v15bg_local_swap_shell_drag_decomposition.py`
- `Documentation/v15bg_local_swap_shell_drag_decomposition.md`
- `Documentation/v15bg_local_swap_shell_drag_placements.csv`
- `Documentation/v15bg_local_swap_shell_drag_rows.csv`
- `Documentation/v15bg_local_swap_shell_drag_diagnosis.csv`
- `Documentation/v0_15bg_operativ_anbefaling.md`

## 10h. v15bh viste at p2 faktisk har en liten lokal rare-load-trigger, men ikke en full rare-rangering

Etter at `v15bg` viste at `p3 > p2` best leses som retention pluss rare-loaded shell-drag, tok `v15bh` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `p1`, `p2` og `p3` i `target 96`, `growth_seed 202`
- test et lite sett støtte-/last-akser
- avgjor om `p2` kan leses som en egen rare-load-retning uten a late som hele `p1/p2/p3`-rekkefolgen er løst

Det viktigste resultatet er:

- flere sma akser setter `p2` tydelig overst
- beste kandidater er `ball2_load`, `ball3_load` og `ball1_load`
- alle holder `p2_top = 1`
- ingen av dem gjenskaper samtidig hele rare-rangeringen `p2 > p3 > p1`
- diagnosen ender pa `p2_rare_load_trigger_supported`

Dette betyr:

- `p2` ser ikke bare ut som den svakeste diffuse modusen i ettertid
- den ser ut til a ha en liten lokal støtte-/last-trigger som peker mot rare-load-inflasjon
- men vi skal ikke late som denne triggeren allerede forklarer hvorfor `p3` fortsatt holder bedre enn `p1`
- neste riktige steg er derfor a forklare hvorfor `p2` glir over i rare-load mens `p1` ikke gjør det, selv om begge er relativt tunge lokalt

Viktige filer:

- `relational_universe_v15bh_local_swap_rare_load_trigger_lab.py`
- `Documentation/v15bh_local_swap_rare_load_trigger_lab.md`
- `Documentation/v15bh_local_swap_rare_load_trigger_placements.csv`
- `Documentation/v15bh_local_swap_rare_load_trigger_axes.csv`
- `Documentation/v15bh_local_swap_rare_load_trigger_diagnosis.csv`
- `Documentation/v0_15bh_operativ_anbefaling.md`

## 10i. v15bi viste at p2 vs p1 best leses som load-vs-stabilizer-flip

Etter at `v15bh` viste en liten lokal p2-trigger uten å løse hele rare-rangeringen, tok `v15bi` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `p1`, `p2` og `p3` i `target 96`, `growth_seed 202`
- del kandidataksene i to familier: last og stabilisering
- avgjor om `p2` og `p1` faktisk skiller lag som høy last vs sterk stabilisering

Det viktigste resultatet er:

- `p2` topper alle sma last-akser
- `p1` topper alle sma stabiliseringsakser
- beste lastakse er `ball2_load`
- beste stabiliseringsakse er `full_stabilizer = coarse_return + core_share + shell2_over_shell1`
- diagnosen ender pa `load_without_stabilization_supported`

Dette betyr:

- `p2` glir ikke bare mot rare-load fordi den er "mer diffus"
- den ser ut til a være den tyngste lokale lastretningen uten tilsvarende stabiliseringsbuffer
- `p1` holder seg ute av rare-load ikke fordi lasten er lav, men fordi stabiliseringspakken er tydelig sterkere
- neste riktige steg er derfor a forklare hva `p2` konkret mangler av stabilisering relativt til `p1`

Viktige filer:

- `relational_universe_v15bi_local_swap_load_stabilizer_flip.py`
- `Documentation/v15bi_local_swap_load_stabilizer_flip.md`
- `Documentation/v15bi_local_swap_load_stabilizer_placements.csv`
- `Documentation/v15bi_local_swap_load_stabilizer_axes.csv`
- `Documentation/v15bi_local_swap_load_stabilizer_diagnosis.csv`
- `Documentation/v0_15bi_operativ_anbefaling.md`

## 10j. v15bj viste at p2 sitt stabiliseringsunderskudd er retention-led

Etter at `v15bi` skilte `p2` og `p1` som høy last uten nok buffer vs last med buffer, tok `v15bj` neste smale steg:

- kjor ingen nye simuleringer
- behold bare `p1`-vs-`p2`-stabiliseringssiden
- dekomponer `full_stabilizer`
- avgjor om underskuddet primært ligger i retention, i core-stotte eller i shell-lagdeling

Det viktigste resultatet er:

- retention-gapet er `0.400`
- core-gapet er `0.213`
- shell-lag-gapen er `0.100`
- retention dekker `0.561` av total stabiliseringsgap
- core dekker `0.298`
- shell-lagdeling dekker `0.140`
- diagnosen ender pa `retention_led_stabilizer_deficit_supported`

Dette betyr:

- `p2` mangler ikke stabilisering likt pa alle fronter
- underskuddet er klart retention-led
- core-stotte er en tydelig sekundarkomponent
- shell-lagdeling spiller en mindre, men ikke null, rolle

Viktige filer:

- `relational_universe_v15bj_local_swap_stabilizer_component_lab.py`
- `Documentation/v15bj_local_swap_stabilizer_component_lab.md`
- `Documentation/v15bj_local_swap_stabilizer_components.csv`
- `Documentation/v15bj_local_swap_stabilizer_diagnosis.csv`
- `Documentation/v0_15bj_operativ_anbefaling.md`

## 10k. v15bk samlet local_swap-retningene i et lite load-stabilizer-moduskart

Etter at `v15bj` viste at `p2` sitt stabiliseringsunderskudd er retention-led, tok `v15bk` neste naturlige syntesesteg:

- kjor ingen nye simuleringer
- behold beste lokale lastakse fra `v15bi`
- behold beste lokale stabiliseringsakse fra `v15bi`/`v15bj`
- sentrer dem lokalt og se om `p1`, `p2` og `p3` fyller ulike modi

Det viktigste resultatet er:

- `p1` blir `buffered_heavy_load`
- `p2` blir `rare_load_risk`
- `p3` blir `low_load_diffuse`
- diagnosen ender pa `load_stabilizer_mode_map_supported`

Dette betyr:

- growth_seed-202-kartet leses na ikke bare som tre etiketter
- det leses som tre ulike lokale roller
- `p1` bærer tung last men har nok buffer
- `p2` bærer tung last uten nok buffer og er derfor den klare rare-load-risikoen
- `p3` er lettere lastet og mer diffust

Viktige filer:

- `relational_universe_v15bk_local_swap_load_stabilizer_mode_map.py`
- `Documentation/v15bk_local_swap_load_stabilizer_mode_map.md`
- `Documentation/v15bk_local_swap_load_stabilizer_mode_rows.csv`
- `Documentation/v15bk_local_swap_load_stabilizer_mode_diagnosis.csv`
- `Documentation/v0_15bk_operativ_anbefaling.md`

## 10l. v15bl viste at spektral drift skjerpes igjen nar vi condition-er pa lokale carrier-familier

Etter at `v15bk` samlet `local_swap`-retningene i et lite lokalt moduskart, tok `v15bl` neste naturlige steg tilbake mot quasi-invariant-sporet:

- behold bare den stabile anchor-regimen
- behold bare de lokale carrier-familiene som faktisk overlevde i defect-sporet
- rerun et lite `add_chord`-band og et lite `local_swap`-moduskart
- mal de samme relative driftmetrikkene som i `v12`/`v13`, spesielt spektral drift mot dim-drift

Det viktigste resultatet er:

- artifact-control holder rent
- `nodes` og `beta1` holder fortsatt lavest drift, men bare som sanity-metrikker
- i add_chord-bandet blir spektral drift skarpere i `cycle_band_p2` enn i pooled add_chord-familie
- i local_swap-moduskartet blir spektral drift skarpere i `low_load_diffuse` enn i pooled local_swap-familie
- diagnosen ender pa `shared_family_level_spectral_candidate`

Dette betyr:

- repoet har fortsatt ikke en ny global quasi-invariant-lov
- men spektral relativ drift ser bedre ut nar vi condition-er pa lokale carrier-familier enn nar vi blander alt sammen
- den beste nye lesningen er derfor familiespesifikk eller carrier-spesifikk sharpening
- neste riktige steg er en liten carrier-first sammenlikning, ikke en ny bred global invariant-scan

Viktige filer:

- `relational_universe_v15bl_conditional_quasi_invariant_lab.py`
- `Documentation/v15bl_conditional_quasi_invariant_lab.md`
- `Documentation/v15bl_conditional_quasi_invariant_target_summary.csv`
- `Documentation/v15bl_conditional_quasi_invariant_rows.csv`
- `Documentation/v15bl_conditional_quasi_invariant_aggregate.csv`
- `Documentation/v15bl_conditional_quasi_invariant_diagnosis.csv`
- `Documentation/v0_15bl_operativ_anbefaling.md`

## 10m. v15bm viste at carrier-first cross-family-splittelsen ikke holder rent pa holdout-seeds

Etter at `v15bl` fant et delt familiespesifikt spektralt delsignal i bade add_chord og local_swap, tok `v15bm` neste naturlige steg:

- behold bare de to spektrale vinnerlommene fra `v15bl`
- legg ved naerliggende dim-fargede kontroller i hver familie
- bruk friske holdout-seeds
- avgjor om dette holder som en carrier-first cross-family-splittelse

Det viktigste resultatet er:

- artifact-control holder rent
- `cycle_band_p2` holder spectral rank `1`
- `low_load_diffuse` holder spectral rank `1`
- men kontrollene `cycle_band_p1` og `buffered_heavy_load` holder ogsa spectral rank `1`
- candidate-poolen ser derfor ikke skarpere ut enn kontroll-poolen
- diagnosen ender pa `carrier_first_holdout_not_yet`

Dette betyr:

- `v15bl` var ekte ny viten
- men den beste lesningen er fortsatt familiespesifikk sharpening, ikke en ren cross-family carrier-lov
- neste riktige steg bor derfor holde seg innen den sterkeste familien, ikke presse videre pa delt cross-family-portabilitet for tidlig

Viktige filer:

- `relational_universe_v15bm_carrier_first_spectral_holdout.py`
- `Documentation/v15bm_carrier_first_spectral_holdout.md`
- `Documentation/v15bm_carrier_first_spectral_target_summary.csv`
- `Documentation/v15bm_carrier_first_spectral_rows.csv`
- `Documentation/v15bm_carrier_first_spectral_aggregate.csv`
- `Documentation/v15bm_carrier_first_spectral_diagnosis.csv`
- `Documentation/v0_15bm_operativ_anbefaling.md`

## 10n. v15bn viste at add_chord har en svak liten skalahypotese, men ikke mer enn det

Etter at `v15bm` svekket den delte carrier-first-lesningen, tok `v15bn` neste naturlige steg innen den sterkeste add_chord-familien:

- behold bare `growth_seed 202`
- bruk `48/p2` som anker, siden det var den sterkeste spektrale add_chord-lommen i `v15bl`
- mal alle `96`-plasseringene mot dette ankeret med samme coarse-geometri- og relative-drift-observabler
- avgjor om en liten `48 -> 96`-skalaovergang faktisk ser gjenkjennelig ut

Det viktigste resultatet er:

- artifact-control holder rent
- `96/p3` blir beste `96`-kandidat
- `96/p3` holder spectral rank `1`
- men combined-distance-gapet til `96/p1` er bare `0.019`
- diagnosen ender derfor pa `small_scale_jump_match_weak`

Dette betyr:

- repoet har en legitim liten add_chord-skalahypotese
- men bare som svak kandidat, ikke som etablert skalaovergang
- neste riktige steg er en ren holdout-tie-break mot den naermeste `96`-rivalen

Viktige filer:

- `relational_universe_v15bn_add_chord_scale_jump_family_map.py`
- `Documentation/v15bn_add_chord_scale_jump_family_map.md`
- `Documentation/v15bn_add_chord_scale_jump_target_summary.csv`
- `Documentation/v15bn_add_chord_scale_jump_rows.csv`
- `Documentation/v15bn_add_chord_scale_jump_aggregate.csv`
- `Documentation/v15bn_add_chord_scale_jump_match_rows.csv`
- `Documentation/v15bn_add_chord_scale_jump_diagnosis.csv`
- `Documentation/v0_15bn_operativ_anbefaling.md`

## 10o. v15bo viste at den lille add_chord-skalaovergangen ikke holder rent pa holdout

Etter at `v15bn` bare ga en svak ranking-vinner, tok `v15bo` den riktige tie-break-runden:

- behold bare `48/p2` som anker
- bruk `96/p3` som kandidat
- bruk `96/p1` som naermeste kontrollrival
- rerun pa friske holdout-seeds
- avgjor om kandidaten faktisk holder bedre enn kontrollen

Det viktigste resultatet er:

- artifact-control holder rent
- `96/p3` beholder spectral rank `1`
- men `96/p1` blir likevel den naermeste profilen til ankeret pa combined coarse+spectral-likhet
- diagnosen ender pa `scale_jump_pair_not_yet`

Dette betyr:

- `48/p2 -> 96/p3` holder ikke som en ren liten add_chord-skalaovergang
- den mest interessante delen av resultatet er derfor ikke en ny positiv claim, men at skalabruddet tydeligvis er strukturert nok til a forklares

Viktige filer:

- `relational_universe_v15bo_add_chord_scale_jump_holdout.py`
- `Documentation/v15bo_add_chord_scale_jump_holdout.md`
- `Documentation/v15bo_add_chord_scale_jump_holdout_target_summary.csv`
- `Documentation/v15bo_add_chord_scale_jump_holdout_rows.csv`
- `Documentation/v15bo_add_chord_scale_jump_holdout_aggregate.csv`
- `Documentation/v15bo_add_chord_scale_jump_holdout_comparison.csv`
- `Documentation/v15bo_add_chord_scale_jump_holdout_diagnosis.csv`
- `Documentation/v0_15bo_operativ_anbefaling.md`

## 10p. v15bp viste at add_chord-skalabruddet splitter mellom spectral-hold og geometry-hold

Etter det negative holdout-resultatet i `v15bo` tok `v15bp` en ren forklaringsrunde:

- bruk bare `v15bo`-aggregatene
- sammenlikn `96/p3` og `96/p1` direkte mot `48/p2`
- avgjor om bruddet sitter i spectral-rang, coarse geometri eller begge

Det viktigste resultatet er:

- `96/p3` leses best som `spectral_without_geometry_hold`
- `96/p1` leses best som `geometry_without_spectral_hold`
- diagnosen ender pa `split_scale_break_supported`

Dette betyr:

- skalabruddet er ikke bare et tomt nei
- `96/p3` holder den spektrale siden bedre, men mister for mye coarse geometri
- `96/p1` holder coarse geometri bedre, men mister spectral-rangen
- dermed har repoet fortsatt ikke en liten ren scale-transfer-familie, men en strukturert delt breaking av kravene

Viktige filer:

- `relational_universe_v15bp_add_chord_scale_break_explainer.py`
- `Documentation/v15bp_add_chord_scale_break_explainer.md`
- `Documentation/v15bp_add_chord_scale_break_rows.csv`
- `Documentation/v15bp_add_chord_scale_break_diagnosis.csv`
- `Documentation/v0_15bp_operativ_anbefaling.md`

## 10q. v15bq viste at en rikere add_chord-coarse-geometri heller ikke redder den lille scale-transfer-hypotesen

Etter at `v15bp` hadde forklart add_chord-skalabruddet som en delt spectral-vs-geometry-breaking, tok `v15bq` neste naturlige steg:

- behold akkurat den samme lille `48/p2 -> 96/p3`-hypotesen
- behold `96/p1` som naermeste kontroll
- bytt ut den enkle share-pakken med shell-dynamikk og shell-topologi som alternativ coarse-geometri
- avgjor om den beste `96`-kandidaten kanskje likevel ligner ankeret pa den mer strukturelle observabelen

Det viktigste resultatet er:

- artifact-control holder rent
- `96/p3` taper ogsa pa alternativ coarse-geometri
- `96/p1` blir fortsatt naermest ankeret
- alt-gapet ender pa `-0.100`
- diagnosen ender pa `alt_coarse_bridge_not_yet`

Dette betyr:

- add_chord-sporet har na blitt testet baade med enkel share-geometri og rikere shell-geometri
- ingen av dem gir en ren liten `48 -> 96` scale-bridge
- derfor bor vi ikke bruke mer budsjett pa akkurat denne add_chord-skalaovergangen na

Viktige filer:

- `relational_universe_v15bq_add_chord_alt_coarse_geometry_lab.py`
- `Documentation/v15bq_add_chord_alt_coarse_geometry_lab.md`
- `Documentation/v15bq_add_chord_alt_coarse_geometry_target_summary.csv`
- `Documentation/v15bq_add_chord_alt_coarse_geometry_rows.csv`
- `Documentation/v15bq_add_chord_alt_coarse_geometry_aggregate.csv`
- `Documentation/v15bq_add_chord_alt_coarse_geometry_comparison.csv`
- `Documentation/v15bq_add_chord_alt_coarse_geometry_diagnosis.csv`
- `Documentation/v0_15bq_operativ_anbefaling.md`

## 10r. v15br viste at local_swap low_load_diffuse holder pa holdout som bade modus og spectral lomme

Etter det hardere negative resultatet for add_chord i `v15bq` pivoterte `v15br` til det andre carrier-sporet:

- behold bare `target 96`, `growth_seed 202`
- bruk de tre lokale retningene `p1`, `p2`, `p3`
- rerun `local_swap` pa friske holdout-seeds
- mal baade moduskartet fra `v15bk` og spectral-vs-dim-sporet fra `v15bl`
- avgjor om `low_load_diffuse` faktisk holder som bade modus og spectral lomme

Det viktigste resultatet er:

- artifact-control holder rent
- `p1` holder som `buffered_heavy_load`
- `p2` holder som `rare_load_risk`
- `p3` holder som `low_load_diffuse`
- alle tre holder spectral rank `1`
- men `p3` holder samtidig den forventede modusen og spectral-rangen i samme lomme
- diagnosen ender pa `mode_plus_spectral_pocket_supported`

Dette betyr:

- `local_swap` er forelopig et sterkere carrier-spor enn add_chord for videre geometri-/quasi-invariant-arbeid
- spesielt er `96/p3` na en bedre kandidat for videre coarse carrier-geometri enn `48/p2 -> 96/p3` var som liten add_chord-skalaovergang
- neste riktige steg er derfor en direkte carrier-geometri-sammenlikning mellom add_chord og local_swap

Viktige filer:

- `relational_universe_v15br_local_swap_mode_spectral_holdout.py`
- `Documentation/v15br_local_swap_mode_spectral_holdout.md`
- `Documentation/v15br_local_swap_mode_spectral_holdout_target_summary.csv`
- `Documentation/v15br_local_swap_mode_spectral_holdout_rows.csv`
- `Documentation/v15br_local_swap_mode_spectral_holdout_aggregate.csv`
- `Documentation/v15br_local_swap_mode_spectral_holdout_diagnosis.csv`
- `Documentation/v0_15br_operativ_anbefaling.md`

## 10s. v15bs viste at add_chord og local_swap ligger naermere hverandre ved samme locus enn historiene deres hver for seg tilsier

Etter at `v15bq` svekket add_chord-sporet og `v15br` styrket local_swap-sporet, tok `v15bs` det naturlige sammenlikningssteget:

- behold samme base
- behold samme target `96`, growth_seed `202` og placement `3`
- rerun `add_chord` og `local_swap` pa de samme holdout-seedene
- avgjor om carrier-fordelen splitter rent mellom geometri og spectral renhet ved akkurat samme locus

Det viktigste resultatet er:

- artifact-control holder rent
- begge perturbasjoner holder spectral rank `1`
- add_chord holder litt sterkere coarse return og litt sterkere kjerneandel
- local_swap holder litt lavere spectral drift og litt bedre dim-minus-spectral-margin
- men alle gapene er sma
- diagnosen ender pa `carrier_compare_still_mixed`

Dette betyr:

- vi bor ikke overtolke `add_chord` og `local_swap` som to rent komplementaere carrier-typer ved samme locus
- den sterke forskjellen mellom dem sitter mer i hvilke lommer som holder hver for seg enn i en enkel lokal side-ved-side-duell
- neste riktige steg bor derfor bruke en ny carrier-observabel, ikke mer av samme `p3`-sammenlikning

Viktige filer:

- `relational_universe_v15bs_add_chord_vs_local_swap_p3_carrier_compare.py`
- `Documentation/v15bs_add_chord_vs_local_swap_p3_carrier_compare.md`
- `Documentation/v15bs_add_chord_vs_local_swap_p3_target_summary.csv`
- `Documentation/v15bs_add_chord_vs_local_swap_p3_rows.csv`
- `Documentation/v15bs_add_chord_vs_local_swap_p3_aggregate.csv`
- `Documentation/v15bs_add_chord_vs_local_swap_p3_compare.csv`
- `Documentation/v15bs_add_chord_vs_local_swap_p3_diagnosis.csv`
- `Documentation/v0_15bs_operativ_anbefaling.md`

## 10t. v15bt viste at timingteksturen heller ikke splitter carrierne rent ved samme locus

Etter at `v15bs` viste at de statiske carrier-snittene fortsatt var blandede, tok `v15bt` neste naturlige observabelsteg:

- behold samme base, target `96`, growth_seed `202` og placement `3`
- behold de samme holdout-seedene
- sammenlikn add_chord og local_swap i hvordan de gaar inn i sin sene fragmenterte hale
- mal first-fragment-step, suffix-lock, attachment i forste fragmentsegment og state-switching

Det viktigste resultatet er:

- artifact-control holder rent
- begge carrierne gaar tidlig inn i fragment-lock
- add_chord er `anchored_early_fragment_lock` i `0.500` av runene
- local_swap er `anchored_early_fragment_lock` i `0.333`
- resten hos local_swap er mest `looser_early_fragment_lock`
- men gapene er sma, og diagnosen ender pa `carrier_timing_still_mixed`

Dette betyr:

- timingteksturen er ikke den observabelen som renser same-locus-duellen
- vi bor derfor ikke bruke mer budsjett pa flere sma timingvarianter av samme sammenlikning

Viktige filer:

- `relational_universe_v15bt_same_locus_carrier_timing_lab.py`
- `Documentation/v15bt_same_locus_carrier_timing_lab.md`
- `Documentation/v15bt_same_locus_carrier_timing_target_summary.csv`
- `Documentation/v15bt_same_locus_carrier_timing_runs.csv`
- `Documentation/v15bt_same_locus_carrier_timing_segments.csv`
- `Documentation/v15bt_same_locus_carrier_timing_aggregate.csv`
- `Documentation/v15bt_same_locus_carrier_timing_compare.csv`
- `Documentation/v15bt_same_locus_carrier_timing_diagnosis.csv`
- `Documentation/v0_15bt_operativ_anbefaling.md`

## 10u. v15bu viste at occupancy-spekteret heller ikke splitter same-locus-duellen

Etter det blandede timingresultatet i `v15bt` tok `v15bu` en helt annen observabelklasse:

- behold samme base, samme `96/p3`-locus og samme holdout-seeds
- mal tail-union, normalisert occupancy-entropi og top-k-masseandeler
- avgjor om add_chord og local_swap egentlig skiller lag i konsentrasjonsgeometri selv om de ser like ut i andre snitt

Det viktigste resultatet er:

- artifact-control holder rent
- haleunionen er naer (`91.3` vs `95.0`)
- entropien er naer (`0.974` vs `0.970`)
- top3-masseandelen er nesten identisk (`0.0493` vs `0.0487`)
- diagnosen ender pa `occupancy_spectrum_still_mixed`

Dette betyr:

- heller ikke occupancy-spekteret gir en ren same-locus-splittelse
- dermed er same-locus-duellen mellom add_chord og local_swap na testet med minst tre observabelklasser:
  - statiske carrier-snitt
  - timingtekstur
  - occupancy-konsentrasjon
- den riktige neste retningen er derfor a forlate akkurat denne duellformen og lete etter ny familiestruktur eller et nytt skalahopp

Viktige filer:

- `relational_universe_v15bu_same_locus_carrier_occupancy_spectrum_lab.py`
- `Documentation/v15bu_same_locus_carrier_occupancy_spectrum_lab.md`
- `Documentation/v15bu_same_locus_carrier_occupancy_target_summary.csv`
- `Documentation/v15bu_same_locus_carrier_occupancy_runs.csv`
- `Documentation/v15bu_same_locus_carrier_occupancy_aggregate.csv`
- `Documentation/v15bu_same_locus_carrier_occupancy_compare.csv`
- `Documentation/v15bu_same_locus_carrier_occupancy_diagnosis.csv`
- `Documentation/v0_15bu_operativ_anbefaling.md`

## 10v. v15bv fant svak familiestruktur, men ingen felles feature-symmetri

Etter at `v15bs`, `v15bt` og `v15bu` viste at add_chord/local_swap ikke lar seg splitte rent ved samme `96/p3`-locus, tok `v15bv` et smalt skritt ut av samme-locus-duellen:

- behold target `96` og growth_seed `202`
- test placements `0..3`
- sammenlikn `add_chord` og `local_swap`
- bruk nye holdout-seeds
- mål support-geometri, core/shell/rare carrier-geometri, recurrence og relativ spectral/dim-drift
- let etter repeterte family-labels og feature-level near-symmetry-par

Det viktigste resultatet er:

- artifact-control holder rent
- seks av åtte profiler faller i en bred `geometry_core_family`
- `add_chord_p1` skiller seg ut som `expanded_shell_family`
- `local_swap_p3` skiller seg ut som `spectral_core_family`
- beste pairwise-par er support-only near-symmetries ved samme placement, ikke felles support+carrier-symmetrier
- diagnosen ender på `family_structure_without_symmetry_supported`

Dette betyr:

- samme-locus-duellen var for smal, men det finnes en repeterbar geometry-core-plateau-struktur ved target `96`
- symmetry-signalet er ikke sterkt: ingen par er nærme både i support- og carrier-feature-rom
- `symmetry` i denne runden er bare feature-level avstand, ikke automorfi eller fysisk symmetri
- neste riktige smale steg er en holdout av familieinndelingen på friske seeds; hvis den ikke holder, bør prosjektet ta et nytt skalahopp i stedet for mer terskelfiksing ved target `96`

Viktige filer:

- `relational_universe_v15bv_family_structure_symmetry_lab.py`
- `Documentation/v15bv_family_structure_symmetry_lab.md`
- `Documentation/v15bv_family_structure_symmetry_target_summary.csv`
- `Documentation/v15bv_family_structure_symmetry_rows.csv`
- `Documentation/v15bv_family_structure_symmetry_aggregate.csv`
- `Documentation/v15bv_family_structure_symmetry_family_summary.csv`
- `Documentation/v15bv_family_structure_symmetry_pairwise.csv`
- `Documentation/v15bv_family_structure_symmetry_diagnosis.csv`
- `Documentation/v0_15bv_operativ_anbefaling.md`

## 10w. v15bw viste at target-96 family-map ikke replikerer rent

Etter `v15bv` tok `v15bw` den nødvendige holdouten:

- behold target `96`, growth_seed `202`, placements `0..3`
- behold `add_chord` og `local_swap`
- bruk nye seeds
- bruk samme support-/carrier-/recurrence-/spectral-observabler
- behandle `v15bv` sin family-map som en falsifiserbar forventning

Det viktigste resultatet er:

- artifact-control holder rent
- total match-rate mot `v15bv` er bare `0.375`
- forventet geometry-core-retention er `0.500`
- outlier-retention er `0.000`
- observerte geometry-core-medlemmer blir `add_chord_p1`, `add_chord_p2`, `local_swap_p1`, `local_swap_p2`, `local_swap_p3`
- det finnes to full feature-level near-symmetry-kandidater i holdouten, men de redder ikke family-map-en
- diagnosen ender på `family_structure_not_replicated`

Dette betyr:

- `v15bv` ga et nyttig signal, men ikke en stabil target-96 family-map
- mer terskelfiksing ved target `96` ville sannsynligvis overfitte
- neste riktige steg er et nytt skalahopp med samme observabler, ikke et bredere target-96-søk

Viktige filer:

- `relational_universe_v15bw_family_structure_holdout.py`
- `Documentation/v15bw_family_structure_holdout_lab.md`
- `Documentation/v15bw_family_structure_holdout_target_summary.csv`
- `Documentation/v15bw_family_structure_holdout_rows.csv`
- `Documentation/v15bw_family_structure_holdout_aggregate.csv`
- `Documentation/v15bw_family_structure_holdout_summary.csv`
- `Documentation/v15bw_family_structure_holdout_pairwise.csv`
- `Documentation/v15bw_family_structure_holdout_diagnosis.csv`
- `Documentation/v0_15bw_operativ_anbefaling.md`

## 10x. v15bx viste et mer ordnet target-192 plateau

Etter at `v15bw` svekket target-96 family-map-en, tok `v15bx` det smale skalahoppet:

- flytt fra target `96` til target `192`
- behold growth_seed `202`
- behold placements `0..3`
- behold `add_chord` og `local_swap`
- behold samme observabler og samme feature-level near-symmetry-apparat
- bruk family-labels bare som sonder, ikke som etablert struktur

Det viktigste resultatet er:

- artifact-control holder rent
- seks av åtte profiler faller i `spectral_diffuse_rare_family`
- de seks er `add_chord_p0`, `add_chord_p1`, `add_chord_p3`, `local_swap_p0`, `local_swap_p1`, `local_swap_p3`
- begge p2-profiler blir `mixed_family`
- dette gir en ny tverr-perturbasjonssplitt: p2 skiller seg ut ved target `192`
- det finnes ingen full support+carrier near-symmetry-kandidater, bare support-only nærhet
- diagnosen ender på `scale_jump_family_plateau_supported`

Dette betyr:

- skalahoppet ga faktisk ny viten: target `192` ser mer ordnet ut enn target `96` i denne observabelpakken
- plateauet er spectral/diffuse/rare-preget, ikke geometry-core-preget slik `v15bv` antydet ved target `96`
- p2-avviket er nå mer interessant enn individuelle add_chord/local_swap-avvikere
- neste riktige steg er en holdout av target-192 plateauet på friske seeds før noen ny større tolkning

Viktige filer:

- `relational_universe_v15bx_scale_jump_family_probe.py`
- `Documentation/v15bx_scale_jump_family_probe_lab.md`
- `Documentation/v15bx_scale_jump_family_probe_target_summary.csv`
- `Documentation/v15bx_scale_jump_family_probe_rows.csv`
- `Documentation/v15bx_scale_jump_family_probe_aggregate.csv`
- `Documentation/v15bx_scale_jump_family_probe_family_summary.csv`
- `Documentation/v15bx_scale_jump_family_probe_pairwise.csv`
- `Documentation/v15bx_scale_jump_family_probe_diagnosis.csv`
- `Documentation/v0_15bx_operativ_anbefaling.md`

## 10y. v15by svekket p2-splittelsen, men styrket bredt target-192 plateau

Etter `v15bx` tok `v15by` den nødvendige target-192 holdouten:

- behold target `192` og growth_seed `202`
- behold placements `0..3`
- behold `add_chord` og `local_swap`
- bruk friske seeds
- test forventningen fra `v15bx`: seks `spectral_diffuse_rare_family`-profiler og to p2-profiler som `mixed_family`

Det viktigste resultatet er:

- artifact-control holder rent
- eksakt match-rate mot `v15bx` er `0.625`
- forventet plateau-retention er `0.833`
- p2-outlier-retention er `0.000`
- observert plateau er bredere enn forventet: syv av åtte profiler blir `spectral_diffuse_rare_family`
- bare `local_swap_p1` faller ut som `mixed_family`
- det finnes ett full feature-level near-symmetry-par: `add_chord_p3` / `local_swap_p3`
- diagnosen ender på `target192_plateau_weak_holdout`

Dette betyr:

- `v15bx` sin rene p2-splittelse holder ikke
- men target `192` ser fortsatt mer ordnet ut enn target `96`: det brede spectral/diffuse/rare-plateauet blir snarere bredere enn borte
- mer target-192 label-tuning er derfor ikke riktig
- neste steg bør enten være target `384` med samme observabler eller en mekanismeobservabel som forklarer hvorfor target `192` blir så spectral/diffuse/rare

Viktige filer:

- `relational_universe_v15by_target192_plateau_holdout.py`
- `Documentation/v15by_target192_plateau_holdout_lab.md`
- `Documentation/v15by_target192_plateau_holdout_target_summary.csv`
- `Documentation/v15by_target192_plateau_holdout_rows.csv`
- `Documentation/v15by_target192_plateau_holdout_aggregate.csv`
- `Documentation/v15by_target192_plateau_holdout_summary.csv`
- `Documentation/v15by_target192_plateau_holdout_pairwise.csv`
- `Documentation/v15by_target192_plateau_holdout_diagnosis.csv`
- `Documentation/v0_15by_operativ_anbefaling.md`

## 10z. v15bz fant nytt target-384 familiesignal og to near-symmetry-kandidater

Etter at `v15by` gjorde target-192-bildet bredere, men fortsatt litt uklart, tok `v15bz` neste skalahopp:

- flytt til target `384`
- behold growth_seed `202`
- behold placements `0..3`
- behold `add_chord` og `local_swap`
- behold samme family-observabler og feature-level near-symmetry-apparat

Det viktigste resultatet er:

- artifact-control holder rent
- `spectral_diffuse_rare_family` samler fire profiler
- `rare_diffuse_family` samler begge p2-profiler
- `add_chord_p3` blir `spectral_core_family`
- `local_swap_p1` blir `mixed_family`
- det finnes to full feature-level near-symmetry-kandidater
- diagnosen ender på `target384_family_plus_symmetry_candidate`

Dette betyr:

- target `384` gir faktisk ny struktur, ikke bare mer av den uklare target-192-bredden
- p2 ser igjen særpreget ut, nå som en delt `rare_diffuse_family`
- dette er fortsatt bare feature-level struktur, men sterkt nok til at neste naturlige steg er en holdout av de konkrete target-384 kandidatene

Viktige filer:

- `relational_universe_v15bz_target384_family_probe.py`
- `Documentation/v15bz_target384_family_probe_lab.md`
- `Documentation/v15bz_target384_family_probe_target_summary.csv`
- `Documentation/v15bz_target384_family_probe_rows.csv`
- `Documentation/v15bz_target384_family_probe_aggregate.csv`
- `Documentation/v15bz_target384_family_probe_family_summary.csv`
- `Documentation/v15bz_target384_family_probe_pairwise.csv`
- `Documentation/v15bz_target384_family_probe_diagnosis.csv`
- `Documentation/v0_15bz_operativ_anbefaling.md`

## 10aa. v15ca viste at radial occupancy ikke forklarer p1/p2-grensen rent

Etter at target-192 holdouten fortsatt var litt uklar, tok `v15ca` den andre halvdelen av arbeidet: en ny mekanismeobservabel.

Oppsett:

- behold target `192`
- behold growth_seed `202`
- behold bare placements `1` og `2`
- behold `add_chord` og `local_swap`
- mal radial occupancy-fordeling rundt support, occupancy-deltakelse, shell4+-masse og rare-masse

Det viktigste resultatet er:

- artifact-control holder rent
- etter korrigert avstandsmåling er weighted mean distance tolkbar
- p2 ligger ikke konsistent lenger ute enn p1
- shell4+- og rare-massegap peker heller ikke mot en ren p2-uteovergang
- diagnosen ender på `radial_diffuse_boundary_not_yet`

Dette betyr:

- den brede spectral/diffuse/rare-lesningen ved target `192` er ikke forklart av denne enkle radial occupancy-aksen
- det er derfor ikke riktig å presse mer target-192 mekanisme-tuning langs samme akse
- neste steg bør heller gå til target-384-holdout eller en annen mekanismeobservabel enn radial occupancy

Viktige filer:

- `relational_universe_v15ca_target192_radial_occupancy_mechanism_lab.py`
- `Documentation/v15ca_target192_radial_occupancy_mechanism_lab.md`
- `Documentation/v15ca_target192_radial_occupancy_target_summary.csv`
- `Documentation/v15ca_target192_radial_occupancy_rows.csv`
- `Documentation/v15ca_target192_radial_occupancy_aggregate.csv`
- `Documentation/v15ca_target192_radial_occupancy_compare.csv`
- `Documentation/v15ca_target192_radial_occupancy_diagnosis.csv`
- `Documentation/v0_15ca_operativ_anbefaling.md`

## 10ab. v15cb viste at den konkrete target-384-mappen ikke holder rent pa holdout

Etter at `v15bz` fant et lovende target-384-kart, tok `v15cb` den smale holdouten:

- behold target `384`
- behold growth_seed `202`
- behold placements `0..3`
- behold `add_chord` og `local_swap`
- bruk friske seeds
- test både family-map-en og de to full feature-level near-symmetry-kandidatene fra `v15bz`

Det viktigste resultatet er:

- artifact-control holder rent
- total match-rate mot `v15bz` er `0.500`
- spectral_diffuse_rare-kvartetten holder delvis (`0.750`)
- rare_diffuse-paret holder delvis (`0.500`)
- ingen av de to full near-symmetry-kandidatene holder som full near-symmetry i holdouten
- observert quartet blir `add_chord_p0`, `add_chord_p1`, `add_chord_p2`, `local_swap_p3`
- diagnosen ender på `target384_candidates_not_replicated`

Dette betyr:

- target `384` ga et ekte interessant førstesignal i `v15bz`, men ikke en ren og stabil kandidatmap
- det er derfor ikke riktig å presse videre på akkurat disse target-384-labelene
- neste steg bør være ny observabel eller ny skalaavgjørelse, ikke enda en family-holdout av samme map

Viktige filer:

- `relational_universe_v15cb_target384_candidate_holdout.py`
- `Documentation/v15cb_target384_candidate_holdout_lab.md`
- `Documentation/v15cb_target384_candidate_holdout_target_summary.csv`
- `Documentation/v15cb_target384_candidate_holdout_rows.csv`
- `Documentation/v15cb_target384_candidate_holdout_aggregate.csv`
- `Documentation/v15cb_target384_candidate_holdout_summary.csv`
- `Documentation/v15cb_target384_candidate_holdout_symmetry_summary.csv`
- `Documentation/v15cb_target384_candidate_holdout_diagnosis.csv`
- `Documentation/v0_15cb_operativ_anbefaling.md`

## 10ac. v15cc viste at shell-turnover ikke redder target-384-familiene

Etter at `v15cb` svekket troen pa det konkrete target-384-kartet, prover `v15cc` en ny observabel i stedet for mer labeltuning:

- behold target `384`
- behold growth_seed `202`
- behold placements `0..3`
- behold `add_chord` og `local_swap`
- maal tidsopplost shell-turnover rundt support i tail-fasen

Det viktigste resultatet er:

- artifact-control holder rent
- quartet-majoriteten blir bare `2/4`
- p2-paret samler seg ikke i én turnover-familie
- quartet->p2-turnover-avstand er ikke storre enn quartet-intern avstand
- diagnosen ender pa `turnover_structure_not_yet`

Dette betyr:

- target `384` fikk ikke en ren ny familiestruktur bare ved a bytte til turnover-observabel
- det er derfor riktig a ga til ny skalaavgjorelse heller enn mer target-384 tuning pa samme nivå

Viktige filer:

- `relational_universe_v15cc_target384_shell_turnover_observable.py`
- `Documentation/v15cc_target384_shell_turnover_observable.md`
- `Documentation/v15cc_target384_shell_turnover_target_summary.csv`
- `Documentation/v15cc_target384_shell_turnover_rows.csv`
- `Documentation/v15cc_target384_shell_turnover_aggregate.csv`
- `Documentation/v15cc_target384_shell_turnover_pairwise.csv`
- `Documentation/v15cc_target384_shell_turnover_summary.csv`
- `Documentation/v15cc_target384_shell_turnover_diagnosis.csv`
- `Documentation/v0_15cc_operativ_anbefaling.md`

## 10ad. v15cd fant et sterkere target-768-plateau

Etter at `v15cc` ga et negativt observabelsvar, tok `v15cd` neste skalahopp:

- behold growth_seed `202`
- behold placements `0..3`
- behold `add_chord` og `local_swap`
- behold samme family-/symmetry-observabler som i de tidligere scale-jump-rundene
- test target `768` smalt, med friske seeds

Det viktigste resultatet er:

- artifact-control holder rent
- sju av atte profiler faller i `rare_diffuse_family`
- `add_chord_p0` blir eneste `spectral_diffuse_rare_family`-outlier
- det finnes to full feature-level near-symmetry-kandidater:
  - `add_chord_p1` / `add_chord_p2`
  - `add_chord_p2` / `local_swap_p2`
- diagnosen ender pa `target768_family_plateau_supported`

Dette betyr:

- target `768` er sa langt den mest lovende nye skalaen i denne observable-stakken
- men signalet ma holdes ut før det kan brukes som mekanismeinngang

Viktige filer:

- `relational_universe_v15cd_target768_family_probe.py`
- `Documentation/v15cd_target768_family_probe_lab.md`
- `Documentation/v15cd_target768_family_probe_target_summary.csv`
- `Documentation/v15cd_target768_family_probe_rows.csv`
- `Documentation/v15cd_target768_family_probe_aggregate.csv`
- `Documentation/v15cd_target768_family_probe_family_summary.csv`
- `Documentation/v15cd_target768_family_probe_pairwise.csv`
- `Documentation/v15cd_target768_family_probe_diagnosis.csv`
- `Documentation/v0_15cd_operativ_anbefaling.md`

## 10ae. v15ce viste at target-768-plateauet holder bare delvis pa holdout

Etter det positive `v15cd`-signalet tok `v15ce` den smale falsifiseringen:

- behold target `768`
- behold growth_seed `202`
- behold placements `0..3`
- behold `add_chord` og `local_swap`
- bruk friske seeds
- test baade 7-profils `rare_diffuse`-plateauet, `add_chord_p0`-outlieren og de to full near-symmetry-parene

Det viktigste resultatet er:

- artifact-control holder rent
- total match-rate mot `v15cd` er `0.750`
- plateau-retention er `0.714`
- outlier-retention er `1.000`
- full near-symmetry-retention er `0.500`
- `add_chord_p2` / `local_swap_p2` holder som full near-symmetry, mens `add_chord_p1` / `add_chord_p2` glir til support-only
- `local_swap_p0` og `local_swap_p3` glir ut av plateauet og blir `spectral_diffuse_rare_family`
- diagnosen ender pa `target768_plateau_weak_holdout`

Dette betyr:

- target `768` er mer lovende enn target `384`, men fortsatt ikke rent nok til en bred mekanismefortelling
- det riktige neste steget er smalere: enten mekanisme rundt den stabile resten eller en enda smalere holdout, ikke mer family-label-tuning over hele kartet

Viktige filer:

- `relational_universe_v15ce_target768_plateau_holdout.py`
- `Documentation/v15ce_target768_plateau_holdout_lab.md`
- `Documentation/v15ce_target768_plateau_holdout_target_summary.csv`
- `Documentation/v15ce_target768_plateau_holdout_rows.csv`
- `Documentation/v15ce_target768_plateau_holdout_aggregate.csv`
- `Documentation/v15ce_target768_plateau_holdout_summary.csv`
- `Documentation/v15ce_target768_plateau_holdout_pairwise.csv`
- `Documentation/v15ce_target768_plateau_holdout_symmetry_summary.csv`
- `Documentation/v15ce_target768_plateau_holdout_diagnosis.csv`
- `Documentation/v0_15ce_operativ_anbefaling.md`

## 10af. v15cf viste at en grov support-locus-lesning ved target-768 fortsatt er for svak

Etter at `v15ce` pekte pa den stabile resten ved `768`, tok `v15cf` neste smale mekanismesteg:

- behold target `768`
- behold growth_seed `202`
- behold bare placements `0` og `2`
- behold `add_chord` og `local_swap`
- maal radial occupancy, occupancy-spekter og core/rare-fordeling samtidig

Det viktigste resultatet er:

- artifact-control holder rent
- p2 ligger lenger ute enn p0 i weighted distance i begge carrierne
- men rare/core- og occupancy-entropi-signalet er ikke konsistent nok til en ren locus-lesning
- support-core-fraksjonen splitter ikke i det hele tatt
- carrier-gapet er mindre ved p2 enn ved p0 pa noen metrikker, men ikke med sterk nok total struktur
- diagnosen ender pa `support_locus_split_not_yet`

Dette betyr:

- target `768` er fortsatt den mest interessante skalaen i denne observable-stakken
- men p0/p2-splittelsen kan ikke ennå leses som en ren support-locus-mekanisme
- neste riktige steg er en ny, enda smalere target-768-observabel rundt p2-lommen eller spectral-outlieren, ikke mer grov locus- eller family-tuning

Viktige filer:

- `relational_universe_v15cf_target768_support_locus_mechanism_lab.py`
- `Documentation/v15cf_target768_support_locus_mechanism_lab.md`
- `Documentation/v15cf_target768_support_locus_target_summary.csv`
- `Documentation/v15cf_target768_support_locus_runs.csv`
- `Documentation/v15cf_target768_support_locus_aggregate.csv`
- `Documentation/v15cf_target768_support_locus_locus_summary.csv`
- `Documentation/v15cf_target768_support_locus_compare.csv`
- `Documentation/v15cf_target768_support_locus_diagnosis.csv`
- `Documentation/v0_15cf_operativ_anbefaling.md`

## 10ag. v15cg viste at far-shell-horisonten gir et svakt, men ekte p2-signal ved target-768

Etter at `v15cf` ikke klarte a lese target-768-resten som en grov support-locus-splitt, tok `v15cg` neste smale observabelsteg:

- behold target `768`
- behold growth_seed `202`
- behold bare placements `0` og `2`
- behold `add_chord` og `local_swap`
- maal om shell4+-tung, langtrekkende skade faktisk holder ut gjennom halen som en far-shell-horisont

Det viktigste resultatet er:

- artifact-control holder rent
- p0-kontrollene bygger ingen faktisk far-shell-horisont
- `local_swap_p2` viser den sterkeste p2-horisonten
- `add_chord_p2` viser ogsa noe p2-horisont, men ikke sterkt nok til en ren carrier-robust lesning
- diagnosen ender pa `far_shell_horizon_weak`

Dette betyr:

- target `768` har mer struktur i p2-lommen enn `v15cf` kunne fange
- men repoet kan fortsatt ikke lese dette som en ren carrieruavhengig lov
- neste riktige steg er derfor en smal holdout av den sterkeste p2-lommen, ikke bred ny family-tuning

Viktige filer:

- `relational_universe_v15cg_target768_far_shell_horizon_lab.py`
- `Documentation/v15cg_target768_far_shell_horizon_lab.md`
- `Documentation/v15cg_target768_far_shell_horizon_target_summary.csv`
- `Documentation/v15cg_target768_far_shell_horizon_runs.csv`
- `Documentation/v15cg_target768_far_shell_horizon_aggregate.csv`
- `Documentation/v15cg_target768_far_shell_horizon_compare.csv`
- `Documentation/v15cg_target768_far_shell_horizon_diagnosis.csv`
- `Documentation/v0_15cg_operativ_anbefaling.md`

## 10ah. v15ch holdt ut p2-horisonten og oppgraderte den til en delt p2-kandidat

Etter at `v15cg` fant den sterkeste resten i `local_swap_p2`, tok `v15ch` neste smale falsifisering:

- behold target `768`
- behold growth_seed `202`
- behold bare `local_swap_p0`, `local_swap_p2` og `add_chord_p2`
- bruk friske run-seeds
- bruk et lite nabolag av horisont-terskler (`loose`, `baseline`, `tight`)

Det viktigste resultatet er:

- artifact-control holder rent
- `local_swap_p2` holder i baseline og `3/3` terskelkonfigurasjoner mot p0-kontrollen
- p0-kontrollen holder seg ren (`baseline no-horizon = 1.000`)
- `add_chord_p2` holder samtidig i alle `3/3` terskelkonfigurasjoner og er faktisk litt sterkere enn `local_swap_p2`
- diagnosen ender pa `local_swap_p2_horizon_holdout_supported`, men carrier-scope leses som `shared_p2_candidate`

Dette betyr:

- `v15cg` traff ikke bare et skjort local_swap-spesifikt cutoff
- den riktige lesningen er smalere og samtidig sterkere: target `768` har na en delt feature-level p2-lomme pa tvers av carrier
- dette er fortsatt ikke en partikkelpaastand eller en universell geometri
- neste riktige steg er derfor en delt p2-mekanismeobservabel, ikke mer bred target-768 family-tuning

Viktige filer:

- `relational_universe_v15ch_target768_local_swap_p2_horizon_holdout.py`
- `Documentation/v15ch_target768_local_swap_p2_horizon_holdout_lab.md`
- `Documentation/v15ch_target768_local_swap_p2_horizon_target_summary.csv`
- `Documentation/v15ch_target768_local_swap_p2_horizon_runs.csv`
- `Documentation/v15ch_target768_local_swap_p2_horizon_threshold_rows.csv`
- `Documentation/v15ch_target768_local_swap_p2_horizon_aggregate.csv`
- `Documentation/v15ch_target768_local_swap_p2_horizon_compare.csv`
- `Documentation/v15ch_target768_local_swap_p2_horizon_robustness.csv`
- `Documentation/v15ch_target768_local_swap_p2_horizon_diagnosis.csv`
- `Documentation/v0_15ch_operativ_anbefaling.md`

## 10ai. v15ci viste at outer-genealogi alene er for generisk til aa forklare p2-lommen

Etter at `v15ch` holdt ut p2-horisonten som delt feature-level kandidat, tok `v15ci` den mest direkte mekanikkerunden:

- behold target `768`
- behold growth_seed `202`
- behold bare placements `0` og `2`
- behold `add_chord` og `local_swap`
- spor genealogi bare for outer `shell4+`-delen i halen

Det viktigste resultatet er:

- artifact-control holder rent
- alle fire profiler leses som `reseeded_outer_horizon`
- p2 har lavere turnover og høyere dominant mass enn p0
- men selve outer-genealogien skiller ikke p2 fra p0 rent nok
- diagnosen ender pa `shared_p2_horizon_mechanism_not_yet`

Dette betyr:

- outer-aktivitet er reell, men for generisk som mekanikkforklaring alene
- p2-lommen finnes fortsatt, men den ligger ikke rent i en enkel genealogiklasse
- neste riktige steg er derfor en annen p2-observabel, ikke mer av samme genealogiklasse

Viktige filer:

- `relational_universe_v15ci_target768_p2_horizon_genealogy_mechanism_lab.py`
- `Documentation/v15ci_target768_p2_horizon_genealogy_mechanism_lab.md`
- `Documentation/v15ci_target768_p2_horizon_genealogy_target_summary.csv`
- `Documentation/v15ci_target768_p2_horizon_genealogy_runs.csv`
- `Documentation/v15ci_target768_p2_horizon_genealogy_component_rows.csv`
- `Documentation/v15ci_target768_p2_horizon_genealogy_event_rows.csv`
- `Documentation/v15ci_target768_p2_horizon_genealogy_aggregate.csv`
- `Documentation/v15ci_target768_p2_horizon_genealogy_compare.csv`
- `Documentation/v15ci_target768_p2_horizon_genealogy_diagnosis.csv`
- `Documentation/v0_15ci_operativ_anbefaling.md`

## 10aj. v15cj ga bare et svakt outer-occupancy-signal for p2

Etter at `v15ci` viste at outer-genealogi er for grov, tok `v15cj` neste smale akseskifte:

- behold target `768`
- behold growth_seed `202`
- behold bare placements `0` og `2`
- behold `add_chord` og `local_swap`
- maal hvor konsentrert outer-occupancy er i halen

Det viktigste resultatet er:

- artifact-control holder rent
- `local_swap_p2` er tydelig mer konsentrert enn `local_swap_p0`
- `add_chord_p2` holder derimot ikke samme klare konsentrasjonsgap mot `add_chord_p0`
- diagnosen ender pa `shared_p2_outer_concentration_weak`

Dette betyr:

- konsentrasjon kan vaere en del av p2-historien, men ikke som ren delt carrier-lov
- den riktige neste testen bor vaere mer mekanisk enn enda en ny ren tail-oppsummering

Viktige filer:

- `relational_universe_v15cj_target768_outer_occupancy_concentration_lab.py`
- `Documentation/v15cj_target768_outer_occupancy_concentration_lab.md`
- `Documentation/v15cj_target768_outer_occupancy_target_summary.csv`
- `Documentation/v15cj_target768_outer_occupancy_runs.csv`
- `Documentation/v15cj_target768_outer_occupancy_aggregate.csv`
- `Documentation/v15cj_target768_outer_occupancy_compare.csv`
- `Documentation/v15cj_target768_outer_occupancy_diagnosis.csv`
- `Documentation/v0_15cj_operativ_anbefaling.md`

## 10ak. v15ck viste at outer-feeder-flux heller ikke holder rent som delt p2-mekanisme

Etter at `v15cj` pekte mot en mulig, men svak konsentrasjonsfortelling, tok `v15ck` neste smale mekanikkerunde:

- behold target `768`
- behold growth_seed `202`
- behold bare placements `0` og `2`
- behold `add_chord` og `local_swap`
- maal om ny outer-masse mates gjennom fa inner-shell-3 feeder-soner

Det viktigste resultatet er:

- artifact-control holder rent
- `add_chord_p2` viser litt mer concentrated-feeder-rate enn `add_chord_p0`, men med langt lavere birth-intensity
- `local_swap_p2` ser derimot mer self-propagating ut enn mer feeder-konsentrert enn `local_swap_p0`
- diagnosen ender pa `feeder_flux_not_yet`

Dette betyr:

- de rimeligste outer-tail-mekanismene ved target `768` er na testet uten a gi en ren delt p2-forklaring
- p2-lommen er fortsatt reell nok til videre arbeid
- men neste riktige steg bor flytte mekanismeaksen innover mot trigger-/gate- eller boundary-observabler rundt shell2/3 eller supportnaer lansering

Viktige filer:

- `relational_universe_v15ck_target768_outer_feeder_flux_lab.py`
- `Documentation/v15ck_target768_outer_feeder_flux_lab.md`
- `Documentation/v15ck_target768_outer_feeder_target_summary.csv`
- `Documentation/v15ck_target768_outer_feeder_runs.csv`
- `Documentation/v15ck_target768_outer_feeder_snapshot_rows.csv`
- `Documentation/v15ck_target768_outer_feeder_aggregate.csv`
- `Documentation/v15ck_target768_outer_feeder_compare.csv`
- `Documentation/v15ck_target768_outer_feeder_diagnosis.csv`
- `Documentation/v0_15ck_operativ_anbefaling.md`

## 10al. v15cl viste at shell2/3-gate og global-budget-kobling ikke forklarer p2-horisonten rent

Etter at `v15ck` viste at outer-feeder-flux ikke holdt som delt p2-mekanisme, tok `v15cl` neste indre mekanikksteg:

- behold target `768`
- behold growth_seed `202`
- behold bare placements `0` og `2`
- behold `add_chord` og `local_swap`
- maal shell2/3-gate, outer-horizon, shell23/outer-kompensasjon og globale driftbudsjett i samme run

Det viktigste resultatet er:

- artifact-control holder rent
- p2-horisonten dukker fortsatt opp i denne nye seed-runden
- `local_swap_p2` er sterkest (`established_far_shell_rate = 0.750`)
- `add_chord_p2` holder svakere (`0.250`)
- men shell2/3-gate skiller ikke p2 fra p0 rent
- p2 har lavere pre-gate peak, lavere gate release og lavere opposite shell23/outer motion enn p0 i begge carrierne
- p2 har lavere spektral drift enn p0, men ikke med nok shell-redistribusjonsstruktur til aa kalle dette global-budget-kobling
- diagnosene ender pa `inner_gate_not_yet` og `global_budget_coupling_not_yet`

Dette betyr:

- p2-lommen ved target `768` er fortsatt reell nok til videre smal testing
- men den bor ikke forklares som global invariant-kobling basert paa denne observabelen
- neste riktige steg er enten en renere lokal trigger-observabel eller en forsiktig p2-horizon holdout/skala-test

Viktige filer:

- `relational_universe_v15cl_target768_inner_gate_global_budget_lab.py`
- `Documentation/v15cl_target768_inner_gate_global_budget_lab.md`
- `Documentation/v15cl_target768_inner_gate_global_budget_target_summary.csv`
- `Documentation/v15cl_target768_inner_gate_global_budget_runs.csv`
- `Documentation/v15cl_target768_inner_gate_global_budget_snapshot_rows.csv`
- `Documentation/v15cl_target768_inner_gate_global_budget_aggregate.csv`
- `Documentation/v15cl_target768_inner_gate_global_budget_compare.csv`
- `Documentation/v15cl_target768_inner_gate_global_budget_diagnosis.csv`
- `Documentation/v0_15cl_operativ_anbefaling.md`

## 10am. v15cm viste at p2-horisonten ikke starter som en ren tidlig lokal trigger

Etter at `v15cl` avviste en ren shell2/3-gate og global-budget-forklaring, tok `v15cm` den mest lokale gjenværende mekanismelesningen:

- behold target `768`
- behold growth_seed `202`
- behold placements `0` og `2`
- behold `add_chord` og `local_swap`
- bruk samme seed-deltaer som `v15cl` for direkte sammenligning
- maal tidlig supportnaer launch, supportgeometri, first shell/outer-hit, tidlig radiusvekst og downstream far-shell-horisont

Det viktigste resultatet er:

- artifact-control holder rent
- p2-horisonten dukker fortsatt opp: `local_swap_p2 = 0.750`, `add_chord_p2 = 0.250`
- men p2 er ikke tidligere, raskere eller sterkere enn p0 i tidlig launch
- `add_chord_p2` har first-outer-gap `+512.0` mot p0, lavere early radius slope og lavere early peak damage
- `local_swap_p2` har first-outer-gap `+234.0` mot p0, lavere early radius slope og lavere early peak damage
- static support geometry forklarer heller ikke p2 rent
- diagnosene ender pa `local_trigger_not_yet` og `support_geometry_not_explanatory`

Dette betyr:

- target-768 p2-lommen er fortsatt reell nok til videre testing
- men den bor ikke forklares som en enkel lokal trigger uten ny observabel
- etter outer-tail, inner-gate/global-budget og local-trigger negative mekanismesvar er neste riktige steg en smal `p2_horizon_scale_holdout`

Viktige filer:

- `relational_universe_v15cm_target768_local_trigger_lab.py`
- `Documentation/v15cm_target768_local_trigger_lab.md`
- `Documentation/v15cm_target768_local_trigger_target_summary.csv`
- `Documentation/v15cm_target768_local_trigger_runs.csv`
- `Documentation/v15cm_target768_local_trigger_snapshot_rows.csv`
- `Documentation/v15cm_target768_local_trigger_aggregate.csv`
- `Documentation/v15cm_target768_local_trigger_compare.csv`
- `Documentation/v15cm_target768_local_trigger_diagnosis.csv`
- `Documentation/v0_15cm_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cm.md`

## 10an. v15cn viste at p2-horisonten ikke skalerer rent til target 1024 under samme budsjett

Etter at `v15cm` avviste en enkel lokal triggerforklaring, tok `v15cn` den neste smale skala-testen:

- behold `band_zero_del`
- behold growth_seed `202`
- behold `add_chord` og `local_swap`
- behold bare placements `0` og `2`
- inkluder fresh target-768 anchor
- legg til target `1024` som moderat skala-holdout
- bruk samme absolute step budget (`2560`) for begge targets

Det viktigste resultatet er:

- artifact-control holder rent
- startstorrelser er rene og separerte: target `768` og `1024`
- fresh target-768 anchor replikerer delvis
- ved target `768` er `local_swap_p2` stottet (`support_score = 5`, `established_far_shell_rate = 0.500`)
- ved target `768` er `add_chord_p2` svakere (`support_score = 3`, `established_far_shell_rate = 0.500`)
- ved target `1024` stottes ingen p2-carrier
- `add_chord_p2` ved target `1024` har `established_far_shell_rate = 0.000` og `support_score = 0`
- `local_swap_p2` ved target `1024` har `established_far_shell_rate = 0.000` og `support_score = 0`
- diagnosen ender pa `target768_specific_under_current_budget`

Dette betyr:

- target-768 p2-lommen er fortsatt reell nok til videre arbeid
- men signalet skalerer ikke automatisk til target `1024` under samme absolute step budget
- dette er ikke et endelig skala-avslag, fordi fravaer ved `1024` kan skyldes utilstrekkelig tidsbudsjett
- neste riktige steg er `target1024_budget_extension_or_intermediate_scale`

Viktige filer:

- `relational_universe_v15cn_p2_horizon_scale_holdout.py`
- `Documentation/v15cn_p2_horizon_scale_holdout_lab.md`
- `Documentation/v15cn_p2_horizon_scale_holdout_target_summary.csv`
- `Documentation/v15cn_p2_horizon_scale_holdout_runs.csv`
- `Documentation/v15cn_p2_horizon_scale_holdout_aggregate.csv`
- `Documentation/v15cn_p2_horizon_scale_holdout_compare.csv`
- `Documentation/v15cn_p2_horizon_scale_holdout_scale_summary.csv`
- `Documentation/v15cn_p2_horizon_scale_holdout_diagnosis.csv`
- `Documentation/v0_15cn_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cn.md`

## 10ao. v15co gjorde univers-inspirerte valgheuristikker eksplisitte

Etter at `v15cn` viste at p2-horisonten ikke automatisk skalerer til target `1024` under samme absolute step budget, tok `v15co` et metodisk syntesesteg i stedet for aa kjoere enda en dynamisk runde:

- oversett univers-inspirerte egenskaper til repo-lokale observabler
- skill eksplisitt mellom inspirasjon, heuristikk og faktisk simulasjonsevidens
- lag hard gate for artifact hygiene
- ranger defect non-superposition/genealogy som beste positive signalakse
- behold conditional spectral quasi-invariant som sekundar, begrenset akse
- hold Lorentz som diagnostikk/negativt filter, ikke positiv selector
- hold globale regler som instrumentering, ikke lovspraak
- forby entanglement-claims utover en svak pair-non-superposition-proxy

Det viktigste resultatet er en beslutningspolicy, ikke nye runtime-tall:

- `configuration_heuristic = possible_but_weak`
- `hard_gate = artifact_hygiene_first`
- `best_positive_axis = defect_nonseparability_and_genealogy`
- `conditional_invariant_axis = spectral_candidate_capped`
- `lorentz_axis = diagnostic_only_not_selector`
- `entanglement_axis = proxy_only`
- `scale_gate = target1024_budget_extension_or_intermediate_scale`

Dette betyr:

- det er mulig aa bruke trekk fra vaart univers som soekeheuristikk, men bare etter streng repo-lokal oversettelse
- Lorentz-likhet, globale invarianter og entanglement skal ikke brukes som direkte positive claims i dagens repo
- target-768 p2-lommen er fortsatt live, men den maa gjennom budsjett-/skalagater foer den kan bli en sterkere universe-like selector
- neste naturlige dynamiske steg er `target1024_scaled_budget_p2_horizon_or_intermediate_target`

Viktige filer:

- `relational_universe_v15co_configuration_heuristic_assessment.py`
- `Documentation/v15co_configuration_heuristic_assessment.md`
- `Documentation/v15co_configuration_heuristic_axes.csv`
- `Documentation/v15co_configuration_candidate_rules.csv`
- `Documentation/v15co_configuration_decision_table.csv`
- `Documentation/v15co_configuration_physics_anchor_notes.csv`
- `Documentation/v0_15co_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15co.md`

## 10ap. v15cp viste at target-1024 p2 ikke bare manglet skalert budsjett

Etter at `v15co` gjorde budsjett-/skalagaten eksplisitt, tok `v15cp` den smaleste dynamiske oppfolgingen:

- behold target `1024`
- behold growth_seed `202`
- behold `add_chord` og `local_swap`
- behold bare placements `0` og `2`
- behold samme seed-deltaer som `v15cn`
- endre bare step budget fra same-absolute `2560` til skalert `3414`

Det viktigste resultatet er:

- artifact-control holder rent
- target `1024` p2 gjenopplives ikke av skalert budsjett
- `add_chord_p2` har fortsatt `established_far_shell_rate = 0.000`, `support_score = 0`, `candidate_supported = 0`
- `local_swap_p2` har fortsatt `established_far_shell_rate = 0.000`, `support_score = 0`, `candidate_supported = 0`
- den tydeligste budsjettresponsen gaar i stedet til `add_chord_p0`: horizon-span oker fra `33.500` til `86.000`
- samlet horizon-span-delta mot `v15cn` er p0=`52.500`, p2=`0.000`
- diagnosen ender pa `scaled_budget_p2_not_supported` og `p0_budget_response_without_p2`

Dette betyr:

- `1024`-negativen i `v15cn` kan ikke enkelt forklares med bare skalanormalisert tidsbudsjett
- target-768 p2-lommen er fortsatt interessant som lokal lomme/kontrast, men svekket som skala-selector
- neste naturlige valg er enten ett mellomtarget eller aa nedgradere p2 som skala-selector
- ikke oppgrader global invariant-, Lorentz- eller entanglement-sprak fra dette

Viktige filer:

- `relational_universe_v15cp_target1024_scaled_budget_p2_horizon.py`
- `Documentation/v15cp_target1024_scaled_budget_p2_horizon_lab.md`
- `Documentation/v15cp_target1024_scaled_budget_target_summary.csv`
- `Documentation/v15cp_target1024_scaled_budget_runs.csv`
- `Documentation/v15cp_target1024_scaled_budget_aggregate.csv`
- `Documentation/v15cp_target1024_scaled_budget_compare.csv`
- `Documentation/v15cp_target1024_scaled_budget_budget_compare.csv`
- `Documentation/v15cp_target1024_scaled_budget_diagnosis.csv`
- `Documentation/v0_15cp_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cp.md`

## 10aq. v15cq gjorde midpoint-testen og svekket p2 som skala-selector

Etter at `v15cp` viste at skalert target-1024-budsjett ikke gjenopplivet p2, tok `v15cq` den minste mellomskala-avgjorelsen:

- behold `band_zero_del`
- behold growth_seed `202`
- test bare target `896`, midt mellom `768` og `1024`
- behold `add_chord` og `local_swap`
- behold placements `0` og `2`
- behold seed-deltaene fra `v15cn`/`v15cp`
- skaler step budget fra target 768: `2560 -> 2987`

Det viktigste resultatet er:

- artifact-control holder rent
- target 896 gir ikke p2-support etter kriteriene i noen carrier
- `add_chord_p2` har noe far-shell-aktivitet (`established_far_shell_rate = 0.500`, horizon `49.500`), men `add_chord_p0` er like etablert og har lengre horizon (`75.000`)
- dermed blir `add_chord_p2_minus_p0` bare support-score `1` og `candidate_supported = 0`
- `local_swap_p2` etableres ikke ved target 896 (`established = 0.000`, horizon `0.000`, support-score `1`)
- scale-ladderen er dermed: target 768 local_swap-p2 supported, target 896 partial/not-supported, target 1024 not-supported
- diagnosen ender pa `intermediate_p2_partial_not_supported`

Dette betyr:

- p2 er svekket som skala-selector
- p2 kan fortsatt beholdes som target-768 lokal lomme/kontrast
- hvis man vil vaere ekstra konservativ, kan midpoint replikeres med litt mer seed-budget
- ellers er neste riktige steg aa nedgradere p2-scale-sporet og lete etter ny observabel/retning
- dette gir fortsatt ingen grunn til aa oppgradere global invariant-, Lorentz- eller entanglement-sprak

Viktige filer:

- `relational_universe_v15cq_intermediate_scale_p2_horizon.py`
- `Documentation/v15cq_intermediate_scale_p2_horizon_lab.md`
- `Documentation/v15cq_intermediate_scale_target_summary.csv`
- `Documentation/v15cq_intermediate_scale_runs.csv`
- `Documentation/v15cq_intermediate_scale_aggregate.csv`
- `Documentation/v15cq_intermediate_scale_compare.csv`
- `Documentation/v15cq_intermediate_scale_ladder.csv`
- `Documentation/v15cq_intermediate_scale_diagnosis.csv`
- `Documentation/v0_15cq_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cq.md`

## 10ar. v15cr pensjonerte p2 som primar skala-selector og valgte p0-holdout som neste retning

Etter `v15cq` var p2-bildet tydelig nok til at neste steg burde vaere en beslutningsvurdering, ikke enda en p2-run:

- target `768`: local_swap-p2 er stottet, add_chord-p2 er delvis
- target `896`: add_chord-p2 er aktiv, men ikke sterkere enn p0; local_swap-p2 faller bort
- target `1024`: p2 er ikke stottet, heller ikke med skalert budsjett

`v15cr` kjorer ingen ny dynamikk. Den sammenlikner rimelige nestevalg:

- replikere midpoint-p2
- gi target-1024 enda mer p2-budsjett
- pensjonere p2 som skala-selector
- folge den nye add_chord-p0 skalaresponsen
- gaa tilbake til conditional quasi-invariant
- gjenapne Lorentz/global-regel-spor
- gjore bred skala-sweep

Det viktigste resultatet er:

- `p2_scale_selector = retire_as_primary_selector`
- `p2_status = keep_as_target768_local_contrast`
- `new_best_candidate = add_chord_p0_scale_response`
- `next_step = v15cs_add_chord_p0_scale_response_holdout`

Begrunnelsen er at `add_chord_p0` var kontrollprofilen som faktisk fikk sterkere far-shell-horisont med skala:

- target `768`: horizon `2.000`
- target `896`: horizon `75.000`
- target `1024`: horizon `86.000`

Dette betyr ikke at p0 er en lov, partikkel eller invariant. Det betyr bare at den marginale informasjonsverdien na er bedre i en fresh-seed p0-holdout enn i mer p2-budsjett.

Viktige filer:

- `Documentation/v15cr_next_direction_assessment.md`
- `Documentation/v15cr_next_direction_decision_matrix.csv`
- `Documentation/v0_15cr_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cr.md`

## 10as. v15cs viste at p0-responsen er target-spesifikk, ikke 896/1024-skalerende

Etter at `v15cr` valgte `add_chord_p0_scale_response` som beste neste kandidat, tok `v15cs` en fresh-seed holdout:

- behold `band_zero_del`
- behold growth_seed `202`
- test targets `896` og `1024`
- bruk budsjetter skalert fra target 768: `2987` og `3414`
- primarprofil: `add_chord_p0`
- kontroller: `add_chord_p2` og `local_swap_p0`
- friske seed-deltaer: `6203` og `6269`

Det viktigste resultatet er target-spesifikt:

- artifact-control holder rent
- ved target `896` holder `add_chord_p0` sterkt:
  - `established_far_shell_rate = 1.000`
  - `mean_high_horizon_span = 136.000`
  - `p0_response_score = 6`
  - kontroller er svakere
- ved target `1024` kollapser `add_chord_p0`:
  - `established_far_shell_rate = 0.000`
  - `mean_high_horizon_span = 0.000`
  - `p0_response_score = 0`
- ved target `1024` er det i stedet `add_chord_p2` som etablerer far-shell-horizon:
  - `established_far_shell_rate = 0.500`
  - `mean_high_horizon_span = 82.500`

Dette betyr:

- p0-responsen fra `v15cq` er ikke en enkel 896/1024-skalerende kandidat
- men 896-p0 ser reell nok ut til aa vaere en target-spesifikk lomme
- 1024-p2 dukker opp paa friske seeds selv om tidligere p2-scale-linje var negativ; dette peker mer mot target-/placement-spesifikk carrier-veksling enn mot en enkel p0- eller p2-lov
- diagnosen ender pa `p0_scale_response_target_specific`
- neste steg boer enten bracket/replikere p0-responsen rundt 896/1024 eller skifte fra label-budget til response-fingerprint-syntese

Viktige filer:

- `relational_universe_v15cs_add_chord_p0_scale_response_holdout.py`
- `Documentation/v15cs_add_chord_p0_scale_response_holdout.md`
- `Documentation/v15cs_add_chord_p0_scale_response_target_summary.csv`
- `Documentation/v15cs_add_chord_p0_scale_response_runs.csv`
- `Documentation/v15cs_add_chord_p0_scale_response_aggregate.csv`
- `Documentation/v15cs_add_chord_p0_scale_response_control_compare.csv`
- `Documentation/v15cs_add_chord_p0_scale_response_summary.csv`
- `Documentation/v15cs_add_chord_p0_scale_response_historical_compare.csv`
- `Documentation/v15cs_add_chord_p0_scale_response_diagnosis.csv`
- `Documentation/v0_15cs_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cs.md`

## 10at. v15ct viste at response-fingerprint er mer informativt enn p0/p2-label akkurat naa

Etter at `v15cs` gjorde p0-responsen target-spesifikk, tok `v15ct` en synteserunde uten ny dynamikk:

- les eksisterende CSV-er fra `v15cn`, `v15cp`, `v15cq` og `v15cs`
- klassifiser hver profile/target/seed-scope etter response fingerprint heller enn etter p0/p2-label
- sammenlign old-vs-fresh seed scopes ved target `896` og `1024`
- skriv eksplisitte beslutningsrader for p0-label, p2-label, carrier-signal, seed-stabilitet og neste steg

Det viktigste resultatet er at labelen ikke er stabil nok:

- 4/6 old-vs-fresh scaled-profile-sammenligninger skifter response-class
- `add_chord_p0` er sterk ved target `896` paa friske seeds, men kollapser ved `1024`
- `add_chord_p2` er ikke target-768-supported, er delvis ved `896`, absent/diffuse ved gammel `1024`, men aktiv ved frisk `1024`
- `p0_label_stability = not_stable`
- `p2_label_stability = not_stable`

Carrier-lesningen er likevel ikke død:

- `add_chord` har 8 persistent-far-shell-observasjoner mot 2 for `local_swap`
- men hvilken placement/seed-lomme som svarer skifter
- diagnosen blir derfor `add_chord_placement_sensitive_live`
- dette er et dynamisk responsmønster, ikke en invariant-, partikkel- eller Lorentz-paastand

Neste naturlige dynamiske steg er:

- `v15cu_add_chord_placement_response_map`
- smalt kart over add_chord placements ved target `896` og `1024`
- maal: teste om responsen ligger i et lite placement-landskap foer vi bruker mer budsjett paa p0/p2-labeler

Viktige filer:

- `relational_universe_v15ct_response_fingerprint_synthesis.py`
- `Documentation/v15ct_response_fingerprint_synthesis.md`
- `Documentation/v15ct_response_fingerprints.csv`
- `Documentation/v15ct_response_class_summary.csv`
- `Documentation/v15ct_response_seed_stability.csv`
- `Documentation/v15ct_response_decisions.csv`
- `Documentation/v0_15ct_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15ct.md`

## 10au. v15cu viste at add_chord-responsen er et placement-landskap, ikke en p0/p2-label

Etter at `v15ct` pekte paa `add_chord_placement_sensitive_live`, kjorer `v15cu` en smal dynamisk placement-map:

- behold `band_zero_del`
- behold growth_seed `202`
- test targets `896` og `1024`
- bruk budsjetter skalert fra target 768: `2987` og `3414`
- perturbation: `add_chord` only
- placements: `p0`, `p1`, `p2`, `p3`
- friske seed-deltaer: `7307` og `7351`

Artifact-kontroll er ren:

- startstorrelser er separert
- alle requested `add_chord`-perturbations matcher faktisk perturbasjon

Det viktigste resultatet er at responsen ikke følger p0/p2-labelene:

- ved target `896`:
  - `p1` er `strong_persistent_far_shell`, score `6`, horizon `75.000`
  - `p2` er `moderate_persistent_far_shell`, score `6`, horizon `57.500`
  - `p0` og `p3` har `no_horizon`
- ved target `1024`:
  - `p3` er dominant `strong_persistent_far_shell`, score `6`, established `1.000`, horizon `172.000`
  - `p1` er ogsaa `strong_persistent_far_shell`, score `6`, horizon `86.000`
  - `p0` og `p2` har `no_horizon`

Dette gir ny viten:

- `p0` faller ut ved begge target paa nye seed-deltaer
- `p1` er den eneste placementen som er strong persistent ved begge target
- `p2` er en 896-lomme, ikke en stabil 1024-lomme
- `p3` dukker opp som sterk 1024-lomme
- beste placement skifter fra p1 ved 896 til p3 ved 1024

Diagnosen blir:

- `add_chord_carrier = add_chord_carrier_live`
- `placement_landscape = target_specific_placement_switch`
- `target_stability = placement_classes_shift_across_targets`
- neste steg: `mechanism_probe_for_winning_placements`

Dette betyr ikke at p1 eller p3 er partikler, invarianter eller Lorentz-struktur. Det betyr at p0/p2 er feil primar leseakse akkurat naa. Den bedre hypotesen er at `add_chord` skaper et target- og supportavhengig responslandskap som maa forklares mekanistisk.

Viktige filer:

- `relational_universe_v15cu_add_chord_placement_response_map.py`
- `Documentation/v15cu_add_chord_placement_response_map.md`
- `Documentation/v15cu_add_chord_placement_response_target_summary.csv`
- `Documentation/v15cu_add_chord_placement_response_runs.csv`
- `Documentation/v15cu_add_chord_placement_response_aggregate.csv`
- `Documentation/v15cu_add_chord_placement_response_compare.csv`
- `Documentation/v15cu_add_chord_placement_response_target_patterns.csv`
- `Documentation/v15cu_add_chord_placement_response_stability.csv`
- `Documentation/v15cu_add_chord_placement_response_diagnosis.csv`
- `Documentation/v0_15cu_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cu.md`

## 10av. v15cv bekreftet p1/p3-landskapet, men ikke en enkel support/launch-mekanisme

Etter at `v15cu` viste et add_chord-placement-landskap, kjorer `v15cv` en mekanismeprobe:

- rerun bare p1 og p3 fra `v15cu`
- behold targets `896` og `1024`
- behold growth_seed `202`
- behold seed-deltaer `7307` og `7351`
- legg til supportgeometri, supporttopologi og tidlig-launch snapshots
- ikke legg til mer p0/p2-labelbudget

Artifact-kontroll er ren:

- startstorrelser er separert
- alle requested `add_chord`-perturbations matcher faktisk perturbasjon

Det viktigste resultatet er todelt.

Forst: selve placement-landskapet holder:

- p1 er `strong_persistent_far_shell` ved target `896`
  - `established = 0.500`
  - horizon `75.000`
- p1 er ogsaa `strong_persistent_far_shell` ved target `1024`
  - `established = 0.500`
  - horizon `86.000`
- p3 er `no_horizon` ved target `896`
- p3 er `strong_persistent_far_shell` ved target `1024`
  - `established = 1.000`
  - horizon `172.000`

Deretter: de enkle mekanismeforklaringene holder ikke:

- `early_launch_axis = early_launch_not_sufficient`
- p3 1024-vs-896 early-launch score er `0/6`
- `support_geometry_axis = support_geometry_not_sufficient`
- p3 1024-vs-896 support-geometry score er `0/5`

Dette er nyttig negativ viten:

- P1 ser ut som en stabil bro over 896/1024.
- P3 ser ut som en target-spesifikk 1024-lomme.
- Men hverken tidlig outer launch eller enkle statiske supportgeometri-tall forklarer hvorfor p3 bare blir dominant ved 1024.
- Mekanismen maa sannsynligvis ligge i per-run genealogisk utvikling, seed-split eller senere komponentdynamikk, ikke i bare initial support-lokalitet.

Neste naturlige steg:

- `add_genealogy_to_p1_p3_seed_splits`
- bruk p1/p3, targets `896/1024`, seed-deltaer `7307/7351`
- spor komponentgenealogi og event chains per run
- maal: forklare hvorfor noen p1/p3-runs etablerer far-shell horizon og andre ikke

Dette betyr fortsatt ikke partikler, Lorentz-likhet eller global invariant. Det er en smal mekanismeavklaring for add_chord placement-landskapet.

Viktige filer:

- `relational_universe_v15cv_add_chord_winning_placement_mechanism_probe.py`
- `Documentation/v15cv_add_chord_winning_placement_mechanism_probe.md`
- `Documentation/v15cv_add_chord_winning_placement_target_summary.csv`
- `Documentation/v15cv_add_chord_winning_placement_support_geometry.csv`
- `Documentation/v15cv_add_chord_winning_placement_snapshot_rows.csv`
- `Documentation/v15cv_add_chord_winning_placement_runs.csv`
- `Documentation/v15cv_add_chord_winning_placement_aggregate.csv`
- `Documentation/v15cv_add_chord_winning_placement_compare.csv`
- `Documentation/v15cv_add_chord_winning_placement_diagnosis.csv`
- `Documentation/v0_15cv_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cv.md`

## 10aw. v15cw fant en begrenset p1/1024 genealogy-separasjon

Etter at `v15cv` bekreftet p1/p3-landskapet, men ikke fant en enkel support- eller early-launch-mekanisme, kjorer `v15cw` en genealogy-runde:

- behold targets `896` og `1024`
- behold placements `p1` og `p3`
- behold growth_seed `202`
- behold seed-deltaer `7307` og `7351`
- bruk component trajectories og event logs som primaerdata
- la far-shell horizon vaere downstream outcome

Artifact-kontroll er ren:

- startstorrelser er separert
- alle requested `add_chord`-perturbations matcher faktisk perturbasjon

Landskapet reproduseres:

- `p1_bridge=1`
- `p3_switch=1`
- diagnosen er `p1_bridge_p3_switch_reproduced`

Per-run resultater:

- `896/p1/7307`: `established_far_shell_horizon`, `split_persistent_dual`
- `896/p1/7351`: `no_far_shell_horizon`, `split_persistent_dual`
- `896/p3/7307`: `no_far_shell_horizon`, `split_persistent_dual`
- `896/p3/7351`: `no_far_shell_horizon`, `split_persistent_dual`
- `1024/p1/7307`: `no_far_shell_horizon`, `birth_death_churn`
- `1024/p1/7351`: `established_far_shell_horizon`, `split_fragment`
- `1024/p3/7307`: `established_far_shell_horizon`, `split_persistent_dual`
- `1024/p3/7351`: `established_far_shell_horizon`, `split_persistent_dual`

Det viktige er begrenset, men ekte:

- `1024/p1` har disjunkte genealogy patterns for no-horizon og horizon.
- `birth_death_churn` gir no-horizon i denne lille n.
- `split_fragment` gir horizon i denne lille n.
- Men `split_persistent_dual` er blandet globalt: samme pattern opptrer baade med og uten horizon.

Diagnosen blir derfor:

- `genealogy_axis = genealogy_separates_limited_seed_splits`
- ikke en generell genealogy-lov
- neste steg: `holdout_p1_1024_genealogy_split_axis`

Dette betyr:

- Genealogi er mer informativ enn de naive supportgeometri-/early-launch-observablene fra `v15cv`.
- Men funnet maa holdes smalt: det er en konkret `1024/p1` seed-split-hypotese, ikke en generell add_chord-mekanisme.
- Ikke oppgrader til partikkel-, Lorentz-, invariant- eller universell geometry-claim.

Viktige filer:

- `relational_universe_v15cw_add_chord_p1_p3_genealogy_seed_split.py`
- `Documentation/v15cw_add_chord_p1_p3_genealogy_seed_split.md`
- `Documentation/v15cw_add_chord_p1_p3_genealogy_target_summary.csv`
- `Documentation/v15cw_add_chord_p1_p3_genealogy_component_trajectories.csv`
- `Documentation/v15cw_add_chord_p1_p3_genealogy_event_log.csv`
- `Documentation/v15cw_add_chord_p1_p3_genealogy_runs.csv`
- `Documentation/v15cw_add_chord_p1_p3_genealogy_aggregate.csv`
- `Documentation/v15cw_add_chord_p1_p3_genealogy_chain_summary.csv`
- `Documentation/v15cw_add_chord_p1_p3_genealogy_diagnosis.csv`
- `Documentation/v0_15cw_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cw.md`

## 10ax. v15cx svekket den konkrete p1/1024 genealogy-mappingen paa holdout

Etter at `v15cw` fant en liten, ren `1024/p1` seed-splitt, tok `v15cx` den riktige holdouten foer generalisering:

- behold target `1024`
- behold placement `p1`
- behold growth_seed `202`
- bruk fire nye seed-deltaer: `7411`, `7477`, `7541`, `7603`
- test bare den konkrete v15cw-kalibreringen:
- `birth_death_churn -> no_far_shell_horizon`
- `split_fragment -> established_far_shell_horizon`
- behold component trajectories og event logs som primaerdata
- la far-shell horizon vaere downstream outcome

Artifact-kontroll er ren:

- startstorrelse er ren og separert
- alle requested `add_chord`-perturbations matcher faktisk perturbasjon

Holdout-resultatet er ikke positivt for den kategoriske mappingen:

- `7411`: `established_far_shell_horizon`, `split_persistent_dual`
- `7477`: `mixed_far_shell_horizon`, `split_persistent_dual`
- `7541`: `established_far_shell_horizon`, `split_persistent_dual`
- `7603`: `established_far_shell_horizon`, `split_persistent_dual`

Aggregert:

- `established_far_shell_rate = 0.750`
- `mean_high_horizon_span = 126.000`
- `genealogy_patterns = split_persistent_dual:4`
- `known_mapping_n = 0`
- `pattern_separates_outcome = 0`
- `mean_churn_event_count = 1381.000`
- `mean_max_component_count = 42.750`
- `mean_max_total_defect_mass = 235.250`

Diagnosen blir derfor:

- `p1_1024_specific_genealogy_axis_not_reproduced`
- den konkrete `birth_death_churn`/`split_fragment`-mappingen fra `v15cw` skal ikke brukes som selector
- `split_persistent_dual` er ikke en ren klasse, men det ser ut som et bredere high-intensity genealogy-regime med sterkere horizon-tilboyelighet i denne holdouten

Dette betyr:

- Genealogy er fortsatt nyttig, men de grove event-chain labels er for grove som mekanismeforklaring.
- Neste riktige steg er en kontinuerlig genealogy-intensitetsobservabel: churn, split-timing, post-split dual-duration, max mass og event-rate mot horizon.
- Ikke oppgrader dette til partikkel-, Lorentz-, invariant- eller universell geometry-claim.

Viktige filer:

- `relational_universe_v15cx_p1_1024_genealogy_holdout.py`
- `Documentation/v15cx_p1_1024_genealogy_holdout.md`
- `Documentation/v15cx_p1_1024_genealogy_holdout_target_summary.csv`
- `Documentation/v15cx_p1_1024_genealogy_holdout_component_trajectories.csv`
- `Documentation/v15cx_p1_1024_genealogy_holdout_event_log.csv`
- `Documentation/v15cx_p1_1024_genealogy_holdout_runs.csv`
- `Documentation/v15cx_p1_1024_genealogy_holdout_aggregate.csv`
- `Documentation/v15cx_p1_1024_genealogy_holdout_chain_summary.csv`
- `Documentation/v15cx_p1_1024_genealogy_holdout_diagnosis.csv`
- `Documentation/v0_15cx_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cx.md`

## 10ay. v15cy fant at kontinuerlig genealogy-intensitet er bedre enn grove labels

Etter at `v15cx` svekket den konkrete `birth_death_churn`/`split_fragment`-mappingen, tok `v15cy` det riktige billige steget foer ny dynamikk:

- ingen ny dynamisk kjøring
- les `v15cw` og `v15cx` sine run-level genealogy-tabeller
- bygg kontinuerlige genealogy-features uten aa bruke horizon som input
- evaluer mot downstream `far_shell_horizon_label` og `high_horizon_span`
- sammenlign med de grove event-chain labels

Score-inputene er genealogy-/event-/mass-felter:

- `churn_per_step`
- `split_per_step`
- `birth_death_per_step`
- `max_component_count_per_target`
- `max_total_defect_mass_fraction`
- `mean_total_defect_mass_fraction`
- `post_split_dual_fraction`
- `first_split_earliness`

Hovedresultatet:

- coarse event-chain labels er ikke nok
- kontinuerlig intensity-index er lovende, men fortsatt post-hoc og liten n

Scope-resultater:

- `all_runs`: intensity AUC `0.800`, Spearman mot horizon-span `0.521`
- `v15cw_all`: intensity AUC `0.750`, Spearman `0.443`
- `p1_1024_all`: intensity AUC `0.875`, Spearman `0.638`
- `p1_1024_holdout_only`: intensity AUC `1.000`, Spearman `0.949`

Top-metrikker:

- globalt er `max_component_count_per_target` sterkest: AUC `0.943`, Spearman `0.783`
- for `p1/1024` er `compress_per_step` sterkest: AUC `1.000`, Spearman `0.893`
- i holdout-only er intensity-index/churn/birth-death alle AUC `1.000`, men dette er bare fire runs

Diagnosen blir:

- `continuous_genealogy_intensity_promising_small_n`
- dette er sterkere enn grove genealogy labels
- men fordi scoren er post-hoc, maa den fryses foer ny dynamikk

Neste riktige steg:

- `pre_register_continuous_intensity_holdout`
- frys intensity-score/top-metrikker
- test paa nye dynamiske runs foer scorevekter eller observabler endres
- ikke oppgrader til partikkel-, Lorentz-, invariant- eller entanglement-claim

Viktige filer:

- `relational_universe_v15cy_continuous_genealogy_intensity_synthesis.py`
- `Documentation/v15cy_continuous_genealogy_intensity_synthesis.md`
- `Documentation/v15cy_continuous_genealogy_intensity_runs.csv`
- `Documentation/v15cy_continuous_genealogy_intensity_metric_scores.csv`
- `Documentation/v15cy_continuous_genealogy_intensity_scope_summary.csv`
- `Documentation/v15cy_continuous_genealogy_intensity_top_metrics.csv`
- `Documentation/v15cy_continuous_genealogy_intensity_diagnosis.csv`
- `Documentation/v0_15cy_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cy.md`

## 10az. v15cz gjorde pre-registered holdout, men selector-testen ble ubalansert

Etter `v15cy` var det riktige steget aa ikke justere mer paa scoren, men aa fryse den og teste paa ny dynamikk:

- behold `1024:p1/add_chord` som smal holdout-lomme
- bruk `growth_seed = 202`
- kjor 24 nye seed-deltaer
- fit score-spec bare paa kalibreringsdata fra `v15cw`/`v15cx`
- skriv holdout-score blindt foer horizon-label/fasitering
- ekskluder `mixed` fra primaer AUC og rapporter den separat

Den frosne `genealogy_intensity_index` bruker fortsatt bare pre-horizon genealogy-/event-/mass-felter:

- `churn_per_step`
- `split_per_step`
- `birth_death_per_step`
- `max_component_count_per_target`
- `max_total_defect_mass_fraction`
- `mean_total_defect_mass_fraction`
- `post_split_dual_fraction`
- `first_split_earliness`

Hovedresultatet er todelt:

- artifact-control holder rent
- `1024:p1` viser seg mye sterkere som far-shell-horizon-lomme enn tidligere antatt

Holdout-labelene ble:

- `established_far_shell_horizon`: 22
- `no_far_shell_horizon`: 1
- `mixed_far_shell_horizon`: 1

Primaerscoren bestod den smale retningssjekken:

- decisive runs: 23
- AUC: `1.000`
- exact one-sided p: `0.043`
- den ene no-horizon-runnen fikk lavest score

Men dette er ikke en balansert confirmatory selector-validering:

- negativklassen har bare ett decisive eksempel
- diagnosen blir derfor `pre_registered_intensity_inconclusive_balance`
- riktig tolkning er "lovende frossen score under ubalansert holdout", ikke "validert selector"

En viktig korreksjon fra holdouten er at den post-hoc sterkeste enkeltmetrikken fra `v15cy` ikke holdt:

- `compress_per_step` faller til AUC `0.114`
- dette svekker en ren kompresjonsforklaring
- de mer sammensatte intensitets-/churn-/birth-death-signalene er fortsatt mer interessante, men krever balansert kontrast

Neste riktige steg:

- ikke refit `v15cz`-scoren paa holdouten
- ikke oppgrader til invariant-, Lorentz-, entanglement- eller partikkelclaim
- hvis scoren skal testes videre, pre-registrer en kontrast-/balanseringsrunde mot svakere/negative placements
- hvis ikke, rapporter `v15cz` som en ubalansert men informativ positiv retningssjekk for `1024:p1`

Viktige filer:

- `relational_universe_v15cz_pre_registered_continuous_intensity_holdout.py`
- `Documentation/v15cz_pre_registered_continuous_intensity_holdout.md`
- `Documentation/v15cz_pre_registered_continuous_intensity_holdout_score_spec.csv`
- `Documentation/v15cz_pre_registered_continuous_intensity_holdout_calibration_manifest.csv`
- `Documentation/v15cz_pre_registered_continuous_intensity_holdout_target_summary.csv`
- `Documentation/v15cz_pre_registered_continuous_intensity_holdout_component_trajectories.csv`
- `Documentation/v15cz_pre_registered_continuous_intensity_holdout_event_log.csv`
- `Documentation/v15cz_pre_registered_continuous_intensity_holdout_blind_scores.csv`
- `Documentation/v15cz_pre_registered_continuous_intensity_holdout_runs.csv`
- `Documentation/v15cz_pre_registered_continuous_intensity_holdout_metric_scores.csv`
- `Documentation/v15cz_pre_registered_continuous_intensity_holdout_scope_summary.csv`
- `Documentation/v15cz_pre_registered_continuous_intensity_holdout_diagnosis.csv`
- `Documentation/v0_15cz_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15cz.md`

## 10ba. v15da balanserte selector-testen og felte frozen genealogy-intensity som selector

Etter `v15cz` var primaerproblemet ikke mer p1-budsjett, men mangel paa negative/weak-control outcomes.
Raadgiverpanelet ble derfor brukt til aa velge neste smale runde:

- Claude CLI ble forsokt, men svarte `Not logged in`
- to remote Codex-subagenter anbefalte fresh frozen-score placement-kontrast
- lokale modeller ble ikke brukt, for aa unngaa aa forstyrre laptop-jobber

Designet ble:

- target `1024`
- `growth_seed = 202`
- perturbasjon `add_chord`
- placements `p0`, `p1`, `p2`
- 12 friske seed-deltaer per placement: `9341/9391/9433/9479/9533/9587/9631/9677/9733/9781/9833/9887`
- samme scaled budget som v15cz
- v15cz `genealogy_intensity_index` score-spec lastet fra artefakt og brukt uten refit
- primaer outcome er `established_far_shell_horizon` vs `no_far_shell_horizon`; `mixed` og `failed` er ikke-decisive

Artifact-control holder rent:

- startstorrelse er ren
- requested perturbation matcher faktisk `add_chord`
- score-spec er frosset fra v15cz

Kontrasten balanserer testen godt nok:

- decisive rows: `34`
- established: `11`
- no_horizon: `23`
- mixed: `1`
- failed: `1`

Placement-resultatet er det viktigste:

- `p1`: `10/12 established`, `1 no_horizon`, `1 mixed`, mean horizon `144.417`, mean score `0.678`
- `p2`: `0/12 established`, `12 no_horizon`, mean horizon `0.000`, mean score `0.343`
- `p0`: `1 established`, `10 no_horizon`, `1 failed`, mean horizon `13.917`, mean score `0.618`

Dette skjerper bildet:

- `p1/1024` replikerer som en robust far-shell-horizon-lomme
- `p2/1024` er en ren negativ placement-kontroll i denne runden
- `p0/1024` er ikke bare svak; den er en falsk-positiv intensity-kontroll, fordi den ofte scorer hoyt uten horizon

Primaerscoren feiler derfor som selector under raadgiverkriteriene:

- `genealogy_intensity_index` AUC: `0.711`
- exact rank-DP one-sided p: `0.025`
- median established-minus-no delta: `0.282`
- p-verdien og deltaen er positive, men AUC er under terskel og falsk-positive p0-runs gjor scoren utilstrekkelig som selector

Diagnosen blir:

- `frozen_intensity_placement_contrast_failed`

Operativ konsekvens:

- ikke refit v15cz-scoren paa v15da
- ikke oppgrader til partikkel-, Lorentz-, entanglement-, invariant- eller universell-geometri-claim
- genealogy-intensity bor nedgraderes fra selector til deskriptiv observabel
- neste naturlige observabel bor skille `p0` false-positive intensity fra `p1` horizon, sannsynligvis timing/phase/band-entry eller support-to-far-shell routing

Viktige filer:

- `relational_universe_v15da_frozen_intensity_placement_contrast.py`
- `Documentation/v15da_frozen_intensity_placement_contrast.md`
- `Documentation/v15da_frozen_intensity_placement_contrast_target_summary.csv`
- `Documentation/v15da_frozen_intensity_placement_contrast_component_trajectories.csv`
- `Documentation/v15da_frozen_intensity_placement_contrast_event_log.csv`
- `Documentation/v15da_frozen_intensity_placement_contrast_blind_scores.csv`
- `Documentation/v15da_frozen_intensity_placement_contrast_runs.csv`
- `Documentation/v15da_frozen_intensity_placement_contrast_placement_summary.csv`
- `Documentation/v15da_frozen_intensity_placement_contrast_matched_seed_compare.csv`
- `Documentation/v15da_frozen_intensity_placement_contrast_metric_scores.csv`
- `Documentation/v15da_frozen_intensity_placement_contrast_scope_summary.csv`
- `Documentation/v15da_frozen_intensity_placement_contrast_diagnosis.csv`
- `Documentation/v15da_advisor_panel_notes.csv`
- `Documentation/v0_15da_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15da.md`

## 10bb. v15db viste at routing forklarer p0-falskpositiver, men ikke som tidlig selector

Etter `v15da` var den viktigste mekanistiske spenningen:

- p1 etablerer far-shell horizon robust
- p2 er en ren negativ kontroll
- p0 kan ha hoy frozen genealogy-intensity uten horizon

`v15db` tok derfor et no-new-dynamics steg:

- les bare `v15da` run-tabellen og komponenttrajectory-tabellen
- ikke refit v15cz-score
- test candidate-observabler som kan skille p0 high-score no-horizon fra p1 established
- skill eksplisitt mellom early/pre-entry features og downstream routing/retention

Hovedfunn:

- p0 high-score no-horizon false positives har median `genealogy_intensity_index = 0.816`
- p1 established har median `genealogy_intensity_index = 0.768`
- baseline-intensity er derfor direkte misledende for akkurat denne kontrasten

Downstream routing skiller derimot rent:

- `tail_route_index`: AUC `1.000` for p1 established vs p0 high-score no-horizon
- `entry_timing_index`: AUC `1.000` for samme kontrast
- `intensity_without_route_pressure`: AUC `1.000` for samme kontrast naar lavere er bedre for established

Men dette er ikke nok som predictor:

- `tail_route_index` og `entry_timing_index` bruker downstream/entry-nare informasjon
- de forklarer false positives, men er ikke legitim pre-horizon selector

Beste early/pre-entry kandidat er bare moderat:

- `component_early_far8_mass_fraction` AUC `0.720` for p1 established vs p0 false-positive
- samme feature har AUC `0.783` for established vs no-horizon
- `phase_entry_index` ligger lavere (`0.700` for p1-vs-p0 false-positive)

Diagnosen blir:

- `downstream_routing_separates_but_not_pre_entry`

Operativ konsekvens:

- genealogy-intensity forblir deskriptiv, ikke selector
- downstream routing/entry forklarer p0-falskpositivene
- neste riktige steg er aa instrumentere en tidligere route-entry/retention precursor
- ikke bruk tail/first-high downstream-felter som om de var pre-horizon predictors
- ikke oppgrader til partikkel-, Lorentz-, entanglement-, invariant- eller universell-geometri-claim

Viktige filer:

- `relational_universe_v15db_routing_phase_observable_synthesis.py`
- `Documentation/v15db_routing_phase_observable_synthesis.md`
- `Documentation/v15db_routing_phase_run_features.csv`
- `Documentation/v15db_routing_phase_group_summary.csv`
- `Documentation/v15db_routing_phase_metric_scores.csv`
- `Documentation/v15db_routing_phase_false_positive_cases.csv`
- `Documentation/v15db_routing_phase_diagnosis.csv`
- `Documentation/v0_15db_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15db.md`

## 10bc. v15dc testet strengere pre-horizon routing og fant bare svakt/moderat signal

`v15db` forklarte p0-falskpositivene med downstream routing, men det var ikke godt nok som predictor.

`v15dc` tok derfor en strengere no-new-dynamics runde:

- les bare `v15da` run-tabellen og komponenttrajectory-tabellen
- bruk ingen nye simuleringer
- ikke refit v15cz-score
- sensurer etablerte runs foer `first_high_step`
- bruk `early_step_limit` for no-high-runs
- hold downstream tail/retention som evaluering, ikke som feature

Hovedresultat:

- diagnosen er `pre_horizon_route_precursor_weak`
- beste censored feature er `pre_far8_slope_per_100`
- `pre_far8_slope_per_100` har AUC `0.780` for p1 established vs p0 high-score no-horizon
- samme feature har AUC `0.794` for established vs no-horizon
- dette er nyttig, men ikke sterkt nok for en selector-claim

Gruppeavlesning:

- p1 established median `pre_route_coherence_index = 0.339`
- p0 high-score no-horizon median `pre_route_coherence_index = 0.125`
- p1 established median `pre_mean_far8_fraction = 0.166`
- p0 high-score no-horizon median `pre_mean_far8_fraction = 0.066`

Viktig negativ kontroll:

- baseline `genealogy_intensity_index` har fortsatt AUC `0.280` for p1 established vs p0 false positives
- `pre_route_coherence_index` er bedre, men fortsatt bare `0.620`
- eksisterende komponentproxyer gir altsaa ikke en ren pre-horizon selector

Operativ konsekvens:

- downstream routing forklarer false positives, men maa ikke brukes som predictor
- censored komponentproxyer gir bare svakt/moderat tidlig signal
- neste riktige steg er direkte per-snapshot route-entry/retention logging
- ikke press eksisterende pre-horizon komponentproxyer videre uten ny instrumentering
- ikke oppgrader til partikkel-, Lorentz-, entanglement-, invariant- eller universell-geometri-claim

Viktige filer:

- `relational_universe_v15dc_pre_horizon_routing_precursor_lab.py`
- `Documentation/v15dc_pre_horizon_routing_precursor.md`
- `Documentation/v15dc_pre_horizon_run_features.csv`
- `Documentation/v15dc_pre_horizon_group_summary.csv`
- `Documentation/v15dc_pre_horizon_metric_scores.csv`
- `Documentation/v15dc_pre_horizon_false_positive_cases.csv`
- `Documentation/v15dc_pre_horizon_diagnosis.csv`
- `Documentation/v0_15dc_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dc.md`

## 10bd. v15dd logget route-entry direkte og forklarte p0-falskpositivene mekanistisk

`v15dc` viste at eksisterende sensurerte komponentproxyer bare gir svakt/moderat pre-horizon-signal.

`v15dd` tok derfor det neste instrumenteringssteget:

- rerun samme smale v15da-scope
- target `1024`
- `add_chord`
- placements `p0,p1,p2`
- seed-deltaer `9341..9887`
- frossen v15da/v15cz genealogy-score gjenbrukes kun som sammenligningskolonne, ikke refittes
- primarproduktet er `v15dd_direct_route_snapshot_log.csv`

Per snapshot logger v15dd:

- route phase: `near_field`, `outer_probe`, `mid_route`, `high_route`
- high/mid/outer flags
- `outer_pressure_without_high`
- contiguous high-run id og lengde
- `sustained_high3_flag`
- retention-window
- dropout og reentry etter sustained entry
- mid-to-high transitions

Hovedfunn:

- diagnosen er `direct_route_entry_retention_separates_false_positives`
- p1 established er `sustained_high_retention:10`
- p0 high-score/no-horizon false positives er `outer_pressure_no_high_entry:5`
- median direct retention er p1 `0.978` og p0 false-positive `0.000`
- median outer-pressure-without-high er p1 `0.088` og p0 false-positive `0.937`

Metrikker:

- `first_sustained_high3_earliness`: AUC `1.000` for p1 established vs p0 false-positive
- `direct_retention_rate_after_entry`: AUC `1.000`
- `last12_high_rate_direct`: AUC `1.000`
- `sustained_high3_rate`: AUC `1.000`
- `direct_high_rate`: AUC `1.000`
- `outer_pressure_without_high_rate`: AUC `1.000` for samme kontrast naar lavere er bedre
- baseline `genealogy_intensity_index`: AUC `0.280`

Tolkning:

- dette er sterk mekanistisk separasjon av false positives
- p0 kan ha hoy genealogy-intensity og mye outer pressure uten aa konvertere til sustained high-route entry
- p1-established-runs gaar faktisk inn i high-route og holder retention
- direct-route-feltene er outcome-naere og maa ikke brukes som om de var en pre-entry selector

Operativ konsekvens:

- neste riktige steg er aa avlede tidligere pre-entry features fra snapshot-loggen
- ny selector-kandidat maa fryses foer ny kjøring
- direct route outcome skal brukes som fasit/instrumentering, ikke som predictor
- ikke oppgrader til partikkel-, Lorentz-, entanglement-, invariant- eller universell-geometri-claim

Viktige filer:

- `relational_universe_v15dd_direct_route_entry_retention_lab.py`
- `Documentation/v15dd_direct_route_entry_retention.md`
- `Documentation/v15dd_direct_route_target_summary.csv`
- `Documentation/v15dd_direct_route_snapshot_log.csv`
- `Documentation/v15dd_direct_route_run_summary.csv`
- `Documentation/v15dd_direct_route_group_summary.csv`
- `Documentation/v15dd_direct_route_label_crosstab.csv`
- `Documentation/v15dd_direct_route_metric_scores.csv`
- `Documentation/v15dd_direct_route_diagnosis.csv`
- `Documentation/v0_15dd_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dd.md`

## 10be. v15de testet route-prefix som strict pre-entry selector og fant ikke signalet

`v15dd` forklarte p0-falskpositivene mekanistisk, men route-entry-feltene var outcome-naere.

`v15de` gjorde derfor en no-new-dynamics syntese:

- leser bare `v15dd_direct_route_snapshot_log.csv` og `v15dd_direct_route_run_summary.csv`
- ingen ny simulasjonsdynamikk
- faste tidlige vinduer: `64`, `96`, `128`, `256`, `512`, `640`
- tidligste p1-established sustained high3-entry i v15dd er step `104`
- derfor er bare vinduer `<=96` strict pre-entry
- senere vinduer rapporteres som entry-risk, ikke som selector-claim

Hovedfunn:

- diagnosen er `pre_entry_feature_not_found`
- beste strict pre-entry feature er `w96_mean_outer_share`
- `w96_mean_outer_share` har AUC `0.560` for p1-established vs p0 high-score/no-horizon false positives
- samme feature har AUC `0.617` for established vs no-horizon
- beste strict `64`-vindu er `w64_component_count_slope_per_100`, AUC `0.550` mot p0 false positives
- baseline `genealogy_intensity_index` er fortsatt ikke selector i denne kontrasten, AUC `0.280`

Entry-risk-funn:

- senere vinduer blir mer informative, men er for naer entry/outcome
- beste entry-risk feature er `w640_ready_both_rate`
- `w640_ready_both_rate` har AUC `0.800` mot p0 false positives og `0.834` for established vs no-horizon
- `w512_positive_distance_margin_rate` og `w640_positive_distance_margin_rate` har ogsaa AUC `0.800` mot p0 false positives

Tolkning:

- route-loggen forklarer false positives, men gir ikke en legitim tidlig selector under strict pre-entry-vindu
- bedre route-prefix squeezing er trolig avtagende avkastning
- neste riktige retning er en ikke-route pre-entry observabel
- mest plausible kandidatomraader er support-geometri, lokal gate/topologi, eller annen pre-entry struktur som ikke er direkte route-entry/retention
- ikke bruk entry-risk-vinduene som evidence for invariant, Lorentz-likhet, entanglement, partikler eller universell geometri

Viktige filer:

- `relational_universe_v15de_pre_entry_feature_synthesis.py`
- `Documentation/v15de_pre_entry_feature_synthesis.md`
- `Documentation/v15de_pre_entry_run_features.csv`
- `Documentation/v15de_pre_entry_metric_scores.csv`
- `Documentation/v15de_pre_entry_window_summary.csv`
- `Documentation/v15de_pre_entry_diagnosis.csv`
- `Documentation/v0_15de_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15de.md`

## 10bf. v15df fant en lovende strict ikke-route pre-entry observabel, men statisk support er en confound

`v15de` fant ikke en legitim strict pre-entry selector i route-prefix-loggen.

`v15df` gjorde derfor neste smale observabelsyntese uten ny dynamikk:

- leser `v15da_frozen_intensity_placement_contrast_component_trajectories.csv`
- leser `v15dd_direct_route_run_summary.csv` for labels, analysis groups og statisk supportgeometri
- bruker strict vinduer `<=32`, `<=64`, `<=96`
- route-entry/retention-felt brukes ikke som kandidatfeatures
- downstream horizon/direct-route labels brukes bare som evalueringsfasit

Primarfunn:

- diagnosen er `pre_entry_support_topology_promising`
- primarresultatet styres av strict dynamisk komponent/topologi, ikke statisk support
- beste strict dynamiske ikke-route metric er `w32_mean_boundary_per_mass`
- `w32_mean_boundary_per_mass` har AUC `0.960` for p1-established vs p0 high-score/no-horizon false positives
- samme metric har AUC `0.864` for established vs no-horizon
- ved `<=64` faller samme boundary/mass-signal til AUC `0.880` mot p0 false positives
- ved `<=96` faller det til AUC `0.800` mot p0 false positives

Confound-vakt:

- beste statiske supportmetric er `static_mean_support_degree`
- `static_mean_support_degree` har AUC `1.000` mot p0 false positives og AUC `0.957` established-vs-no
- dette er statisk support-/placement-informasjon
- derfor skal det rapporteres som placement-confound/audit, ikke som dynamisk selector

Gruppeavlesning:

- p1-established median `w96_gate_tension = 0.205`
- p0 high-score/no-horizon median `w96_gate_tension = 0.156`
- p1-established median `w96_trapped_core = 0.968`
- p0 high-score/no-horizon median `w96_trapped_core = 0.694`
- baseline `genealogy_intensity_index` har fortsatt AUC `0.280` mot p0 false positives

Tolkning:

- dette er det sterkeste repo-lokale pre-entry observabelsporet etter at route-prefix feilet
- men signalet kan delvis vaere statisk placement/support-geometri
- neste steg maa derfor fryse `w32_mean_boundary_per_mass` og rapportere statisk support som eksplisitt confound/audit
- ikke oppgrader dette til invariant, Lorentz-likhet, entanglement, partikler eller universell geometri

Viktige filer:

- `relational_universe_v15df_pre_entry_support_topology_synthesis.py`
- `Documentation/v15df_pre_entry_support_topology_synthesis.md`
- `Documentation/v15df_pre_entry_support_topology_run_features.csv`
- `Documentation/v15df_pre_entry_support_topology_family_summary.csv`
- `Documentation/v15df_pre_entry_support_topology_group_summary.csv`
- `Documentation/v15df_pre_entry_support_topology_metric_scores.csv`
- `Documentation/v15df_pre_entry_support_topology_diagnosis.csv`
- `Documentation/v0_15df_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15df.md`

## 10bg. v15dg holdt ut boundary/mass-kandidaten paa friske seeds

`v15df` fant en lovende strict pre-entry ikke-route observabel, men statisk supportgeometri var en confound.

`v15dg` gjorde derfor en pre-registrert fresh holdout:

- target `1024`
- growth seed `202`
- perturbation `add_chord`
- placements `p0,p1,p2`
- fresh seed-deltaer `10091,10133,10177,10223,10271,10331,10391,10453`
- primarmetric frosset til `w32_mean_boundary_per_mass`
- retning frosset til `higher_is_established`
- route-entry/retention brukes ikke som feature
- statisk `static_mean_support_degree` rapporteres bare som support-/placement-audit

Artifact og balanse:

- artifact-control er `clean`
- labels: `established_far_shell_horizon:7`, `no_far_shell_horizon:15`, `mixed_far_shell_horizon:2`
- p1-established: `7`
- p0 high-score/no-horizon false positives: `8`
- p2 no-horizon: `6`

Primarfunn:

- diagnosen er `boundary_mass_holdout_supported`
- `w32_mean_boundary_per_mass` har AUC `0.821` for p1-established vs p0 high-score/no-horizon false positives
- samme metric har AUC `0.857` for established vs no-horizon
- p1 median boundary/mass er `13.500`
- p0 false-positive median boundary/mass er `11.125`
- median p1-p0false delta er `2.375`
- p2 no-horizon median boundary/mass er `8.500`

Audit og begrensning:

- `static_mean_support_degree` har AUC `1.000` mot p0 false positives
- dette er placement-/support-informasjon og maa ikke behandles som dynamisk selector
- baseline `genealogy_intensity_index` har AUC `0.679` mot p0 false positives
- boundary/mass er dermed bedre enn genealogy-intensity i denne holdouten, men support-confound er fortsatt live

Tolkning:

- dette er den sterkeste repo-lokale stotten saa langt for en strict pre-entry dynamisk observabel
- det er fortsatt bare en lokal, placement-betinget defect/response-observabel
- ikke oppgrader til invariant, Lorentz-likhet, entanglement, partikler eller universell geometri
- neste riktige steg er samme frosne boundary/mass-metric paa ny growth seed eller naboskala, med statisk supportgeometri eksplisitt rapportert som confound/audit

Viktige filer:

- `relational_universe_v15dg_boundary_mass_holdout.py`
- `Documentation/v15dg_boundary_mass_holdout.md`
- `Documentation/v15dg_boundary_mass_target_summary.csv`
- `Documentation/v15dg_boundary_mass_component_trajectories.csv`
- `Documentation/v15dg_boundary_mass_event_log.csv`
- `Documentation/v15dg_boundary_mass_blind_scores.csv`
- `Documentation/v15dg_boundary_mass_run_features.csv`
- `Documentation/v15dg_boundary_mass_group_summary.csv`
- `Documentation/v15dg_boundary_mass_matched_seed_compare.csv`
- `Documentation/v15dg_boundary_mass_metric_scores.csv`
- `Documentation/v15dg_boundary_mass_diagnosis.csv`
- `Documentation/v0_15dg_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dg.md`

## 10bh. v15dh viste at boundary/mass ikke transferer som p1-anchor over growth seed

`v15dg` gjorde `w32_mean_boundary_per_mass` til den sterkeste lokale pre-entry-kandidaten saa langt, men den testen laa fortsatt paa growth seed `202`.

`v15dh` holdt alt annet fast og flyttet bare base/growth seed:

- target `1024`
- growth seed `303`
- perturbation `add_chord`
- placements `p0,p1,p2`
- fresh seed-deltaer `11003,11057,11113,11171,11239,11311,11383,11447`
- primarmetric fortsatt frosset til `w32_mean_boundary_per_mass`
- retning fortsatt `higher_is_established`
- route-entry/retention brukes ikke som feature
- statisk `static_mean_support_degree` rapporteres bare som support-/placement-audit

Artifact og balanse:

- artifact-control er `clean`
- labels: `established_far_shell_horizon:8`, `no_far_shell_horizon:15`, `mixed_far_shell_horizon:1`
- p1-established: `0`
- p1 no-horizon: `8`
- p0 established: `4`
- p2 established: `4`

Primarfunn:

- diagnosen er `boundary_mass_not_growth_seed_transferable_under_original_anchor`
- growth-seed-303 endrer placement-landskapet: p1 er ikke lenger positiv anchor
- `w32_mean_boundary_per_mass` har AUC `0.463` for established vs no-horizon
- den opprinnelige p1-vs-p0-false-positive-kontrasten finnes ikke paa denne growth seed-en

Audit og begrensning:

- `static_mean_support_degree` har AUC `0.217` established-vs-no
- supportgeometrien er fortsatt viktig som audit, men retningen fra v15dg transferer ikke som selector
- baseline `genealogy_intensity_index` har AUC `0.858` established-vs-no
- genealogy-intensity korrelerer overall her, men er ikke primary og skal ikke refittes til claim

Tolkning:

- v15dg sin boundary/mass-kandidat maa nedgraderes fra mulig generell pre-entry selector til base-/placement-betinget observabel
- `p1/1024` er ikke growth-seed-general
- dette svekker universaliserende spraak og styrker behovet for aa forstaa base/support-signaturer
- neste riktige steg er no-new-dynamics syntese av v15dg/v15dh for aa sammenligne base/support-signaturer og placement-respons foer mer label-budget brukes

Viktige filer:

- `relational_universe_v15dh_boundary_mass_growth_seed_holdout.py`
- `Documentation/v15dh_boundary_mass_growth_seed_holdout.md`
- `Documentation/v15dh_boundary_mass_target_summary.csv`
- `Documentation/v15dh_boundary_mass_component_trajectories.csv`
- `Documentation/v15dh_boundary_mass_event_log.csv`
- `Documentation/v15dh_boundary_mass_blind_scores.csv`
- `Documentation/v15dh_boundary_mass_run_features.csv`
- `Documentation/v15dh_boundary_mass_group_summary.csv`
- `Documentation/v15dh_boundary_mass_matched_seed_compare.csv`
- `Documentation/v15dh_boundary_mass_metric_scores.csv`
- `Documentation/v15dh_boundary_mass_diagnosis.csv`
- `Documentation/v0_15dh_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dh.md`

## 10bi. v15di viste at neste steg maa kondisjonere paa base/support foer mer dynamikk

`v15di` var en no-new-dynamics syntese av `v15dg` og `v15dh`.

Den sammenlignet growth seed `202` og `303` med samme target `1024`, perturbation `add_chord`, placements `p0,p1,p2`, og frossen boundary/mass-lesning.

Hovedfunn:

- artifact-control er `clean`
- placement-landskapet er ikke growth-seed-stabilt
- p1 established-rate endres `0.875 -> 0.000`
- p0 established-rate endres `0.000 -> 0.500`
- p2 established-rate endres `0.000 -> 0.500`

Support-signaturer endres samtidig:

- p0: `13,72,343 -> 3,4,827`
- p1: `1,58,537 -> 12,13,22`
- p2: `6,8,9 -> 25,177,430`

Metric-audit:

- `w32_mean_boundary_per_mass` AUC er `0.857` paa seed 202, `0.463` paa seed 303, og `0.563` samlet
- `static_mean_support_degree` AUC er `0.967` paa seed 202, `0.217` paa seed 303, og `0.517` samlet
- `genealogy_intensity_index` er deskriptivt interessant (`0.858` paa seed 303, `0.769` samlet), men ikke primary og skal ikke refittes til claim

Tolkning:

- v15dg sin positive boundary/mass-lesning var reell i seed-202-landskapet, men ikke growth-seed-general
- fixed placement-labels er ikke nok; support-/base-signatur maa inn foer neste dynamikkvalg
- dette svekker enhver retning mot universell selector akkurat naa
- neste riktige steg er en billig support-/base-kondisjonert pre-run audit/selector som predikerer plausible placements foer mer dynamikk brukes

Viktige filer:

- `relational_universe_v15di_growth_seed_signature_synthesis.py`
- `Documentation/v15di_growth_seed_signature_synthesis.md`
- `Documentation/v15di_growth_seed_placement_summary.csv`
- `Documentation/v15di_growth_seed_support_delta.csv`
- `Documentation/v15di_growth_seed_outcome_matrix.csv`
- `Documentation/v15di_growth_seed_metric_audit.csv`
- `Documentation/v15di_growth_seed_diagnosis.csv`
- `Documentation/v0_15di_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15di.md`

## 10bj. v15dj gjorde support-kondisjonert pre-run audit foer mer dynamikk

`v15dj` fulgte v15di sin anbefaling uten aa lage nye dynamiske resultater.

Den leste `Documentation/v15di_growth_seed_placement_summary.csv` og testet om billige support-/base-features kunne brukes som pre-run prior for hvilke `1024/add_chord` placements som er verdt aa teste paa en ny growth seed.

Aktive placements ble definert bare for audit-scoring som `established_rate >= 0.50`:

- growth seed `202`: p1 aktiv (`0.875`)
- growth seed `303`: p0 aktiv (`0.500`)
- growth seed `303`: p2 aktiv (`0.500`)

Hovedfunn:

- en liten klasse `low local support volume/gap`-regler treffer minst en aktiv placement i begge kjente growth seeds
- `low_ball2_minus_ball1`, `low_ball3_minus_ball1`, `low_ball3_minus_ball2`, `low_static_support_ball_2` og `low_static_support_ball_3` har alle `top1_hit_rate = 1.000`
- men total top1-capture er bare `2/3` aktive placements (`0.667`)
- seed-303 har baade p0 og p2 aktive, mens low-volume-reglene typisk peker paa p2 og mister p0

Tolkning:

- supportgeometri er nyttig som pre-run prior, ikke som validert selector
- dette er en scout-kandidat, ikke en universell supportlov
- det gir likevel en bedre neste dynamikkrunde enn blind fixed-placement label-budget
- neste riktige steg er en pre-registrert fresh growth-seed holdout der support-rangering velger top1/top2 pluss kontrast foer dynamikken kjores

Viktige filer:

- `relational_universe_v15dj_support_conditioned_pre_run_audit.py`
- `Documentation/v15dj_support_conditioned_pre_run_audit.md`
- `Documentation/v15dj_support_conditioned_placement_features.csv`
- `Documentation/v15dj_support_conditioned_rule_predictions.csv`
- `Documentation/v15dj_support_conditioned_rule_scores.csv`
- `Documentation/v15dj_support_conditioned_diagnosis.csv`
- `Documentation/v0_15dj_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dj.md`

## 10bk. v15dk falsifiserte low-volume support-rank som fresh selector

`v15dk` gjorde den pre-registrerte fresh growth-seed-holdouten som v15dj anbefalte.

Disiplinen var:

- target `1024`
- growth seed `404`
- perturbation `add_chord`
- placements `p0,p1,p2`
- 8 friske seed-deltaer per placement
- support-ranking skrevet til `v15dk_support_rank_pre_run_ranking.csv` foer dynamikk-loop

Pre-run ranking:

- rank 1: p0, support `3,27,434`, `support_ball2_minus_ball1 = 35`, `support_ball_3 = 107`
- rank 2: p2, support `5,159,1003`, `support_ball2_minus_ball1 = 40`, `support_ball_3 = 112`
- rank 3: p1, support `12,14,465`, `support_ball2_minus_ball1 = 56`, `support_ball_3 = 175`

Dynamisk resultat:

- p0: `no_far_shell_horizon:8`, established-rate `0.000`
- p2: `no_far_shell_horizon:8`, established-rate `0.000`
- p1: `established_far_shell_horizon:4; mixed_far_shell_horizon:1; no_far_shell_horizon:3`, established-rate `0.500`

Hovedfunn:

- top1 capture = `0.000`
- top2 capture = `0.000`
- support-rank-status = `support_rank_not_supported`
- `w32_mean_boundary_per_mass` er svak som audit (`AUC = 0.526` established-vs-no)

Tolkning:

- v15dj sin low local support volume/gap-regel skal pensjoneres som selector-kandidat
- p1/1024 er ikke universell, men den kan reaktiveres paa ny base etter aa ha feilet paa growth seed 303
- add_chord-landskapet er fortsatt live, men enkelt statisk support-volume forklarer ikke placement-switchene
- neste retning bor vaere ny observabeldesign eller skala-/landskapsanalyse, ikke mer blind low-volume support-rank holdout

Viktige filer:

- `relational_universe_v15dk_pre_registered_support_rank_holdout.py`
- `Documentation/v15dk_pre_registered_support_rank_holdout.md`
- `Documentation/v15dk_support_rank_pre_run_ranking.csv`
- `Documentation/v15dk_support_rank_placement_summary.csv`
- `Documentation/v15dk_support_rank_evaluation.csv`
- `Documentation/v15dk_support_rank_metric_scores.csv`
- `Documentation/v15dk_support_rank_diagnosis.csv`
- `Documentation/v0_15dk_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dk.md`

## 10bl. v15dl fant en svak return-probability-morfologi-scout etter support-rank-feilen

`v15dl` var en no-new-dynamics syntese etter v15dk.

Den gjorde ikke nye defect-runs. Den leste eksisterende `1024/add_chord/p0,p1,p2`-resultater fra:

- v15dg: growth seed `202`
- v15dh: growth seed `303`
- v15dk: growth seed `404`

I tillegg rekonstruerte den basegrafene og add_chord-proben for hvert `(growth_seed, placement)` og la til billige pre-run morfologiobservabler:

- lokal volumvekst rundt support
- shortcut/local-efficiency-endring
- return-probability og spectral-dimension proxy
- enkel Forman-style curvature rundt support/chord-endepunkt

Landskapsresultatet er konkret:

- seed 202: aktiv `p1`, established-rate `0.875`
- seed 303: aktive `p0;p2`, begge established-rate `0.500`
- seed 404: aktiv `p1`, established-rate `0.500`

Hovedfunn:

- artifact-control er clean
- v15dk sin low-volume support-rank er fortsatt pensjonert
- beste nye placement-level post-hoc metric er `delta_return_t2`, AUC `0.900`
- beste regel er `delta_return_t2`/high, men bare som `weak_posthoc_top2_scout`
- top1 capture = `0.750`
- top2 capture = `0.750`

Tolkning:

- return-probability-endring er mer interessant enn den pensjonerte low-support-rankingen
- men dette er fortsatt post-hoc og svakt, ikke en validert selector
- hvis vi bruker mer dynamisk budsjett, maa `delta_return_t2`/high fryses foer en liten v15dm-holdout
- dette er ikke evidens for Lorentz-likhet, global invariant, entanglement, partikler eller universell emergent geometri

Viktige filer:

- `relational_universe_v15dl_base_landscape_morphology_synthesis.py`
- `Documentation/v15dl_base_landscape_morphology_synthesis.md`
- `Documentation/v15dl_base_landscape_target_summary.csv`
- `Documentation/v15dl_base_landscape_morphology_features.csv`
- `Documentation/v15dl_base_landscape_placement_summary.csv`
- `Documentation/v15dl_base_landscape_seed_summary.csv`
- `Documentation/v15dl_base_landscape_metric_scores.csv`
- `Documentation/v15dl_base_landscape_rule_scores.csv`
- `Documentation/v15dl_base_landscape_diagnosis.csv`
- `Documentation/v0_15dl_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dl.md`

## 10bm. v15dm testet return-probability-scouten paa fresh seed og fikk bare partial capture

`v15dm` var en liten pre-registrert fresh holdout av v15dl sin beste morfologi-scout.

Disiplinen var:

- target `1024`
- growth seed `505`
- perturbation `add_chord`
- placements `p0,p1,p2`
- 4 friske seed-deltaer per placement
- pre-run ranking skrevet til `v15dm_frozen_return_pre_run_ranking.csv` foer dynamikk-loop
- frossen rank-metric: `delta_return_t2`, high-is-better, med `delta_return_t4` som tiebreak

Pre-run ranking:

- rank 1: p0, support `5,98,599`, `delta_return_t2 = -0.020`
- rank 2: p1, support `7,8,9`, `delta_return_t2 = -0.025`
- rank 3: p2, support `13,14,263`, `delta_return_t2 = -0.033`

Dynamisk resultat:

- p0: `established_far_shell_horizon:3; no_far_shell_horizon:1`, established-rate `0.750`
- p1: `established_far_shell_horizon:1; no_far_shell_horizon:3`, established-rate `0.250`
- p2: `established_far_shell_horizon:3; no_far_shell_horizon:1`, established-rate `0.750`

Hovedfunn:

- active placements = `p0;p2`
- top1 capture = `0.500`
- top2 capture = `0.500`
- return-scout-status = `return_scout_weak_partial_capture`
- `w32_mean_boundary_per_mass` er svak/feilrettet som audit (`AUC = 0.300` established-vs-no)
- genealogy-intensity er deskriptivt sterkt i denne lille runden (`AUC = 1.000`), men er ikke pre-run selector og skal ikke refittes til claim

Tolkning:

- `delta_return_t2` er mer interessant enn low-support-rank, men overlever ikke som ren selector
- viktigere lærdom er at flere placements kan vaere aktive paa samme base
- neste retning bor vaere multi-active/base-landscape observabeldesign, ikke mer top1-rangering eller post-hoc refit av `delta_return_t2`
- dette er ikke evidens for Lorentz-likhet, global invariant, entanglement, partikler eller universell emergent geometri

Viktige filer:

- `relational_universe_v15dm_frozen_return_probability_holdout.py`
- `Documentation/v15dm_frozen_return_probability_holdout.md`
- `Documentation/v15dm_frozen_return_pre_run_ranking.csv`
- `Documentation/v15dm_frozen_return_placement_summary.csv`
- `Documentation/v15dm_frozen_return_evaluation.csv`
- `Documentation/v15dm_frozen_return_metric_scores.csv`
- `Documentation/v15dm_frozen_return_diagnosis.csv`
- `Documentation/v0_15dm_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dm.md`

## 10bn. v15dn flyttet add_chord-sporet fra single-winner til aktivt-sett-landskap

`v15dn` var en no-new-dynamics syntese etter v15dm.
Den brukte eksisterende dynamikk fra v15dl og v15dm, og innforte en mer passende responsform:
ikke "hvilken placement vinner?", men "hvilket lite sett av placements er aktivt paa denne basegrafen?"

Scope:

- target `1024`
- perturbation `add_chord`
- placements `p0,p1,p2`
- growth seeds `202/303/404/505`
- ingen ny dynamikk
- eksisterende dynamiske labels brukes bare som responsekolonner

Seed-landskap:

- seed 202: aktivt sett `p1`
- seed 303: aktivt sett `p0;p2`
- seed 404: aktivt sett `p1`
- seed 505: aktivt sett `p0;p2`

Hovedfunn:

- single-winner-framing er feil modell for dette sporet, fordi flere placements kan vaere aktive paa samme base
- beste placement-level post-hoc audit er `delta_return_t4`/high med AUC `0.861`
- `delta_return_t2` blir dermed ikke reddet som selector; return-observabler er fortsatt audit/observabeldesign
- beste ikke-trivielle aktivt-sett-screen er `local_ball3_beta1`/low/top2
- denne screenen har coverage `1.000`, precision `0.750`, burden `0.667`, exact-set-match `0.500`
- den har falske positive `p0` paa single-active seeds `202` og `404`

Tolkning:

- v15dn gir ny viten fordi problemet bor modelleres som et base-betinget aktivt-sett-landskap
- v15dn gir ikke en validert selector, fordi den beste full-coverage-regelen fortsatt har falske positive og er post-hoc
- en eventuell neste dynamiske runde maa fryse en aktivt-sett-regel foer run og teste minst to nye growth seeds
- alternativt bor vi bygge en ny pre-run observabel som spesielt prover aa skille `p1`-only seeds fra `p0;p2` seeds foer mer dynamikk
- dette er ikke evidens for Lorentz-likhet, global invariant, entanglement, partikler eller universell emergent geometri

Viktige filer:

- `relational_universe_v15dn_multi_active_landscape_synthesis.py`
- `Documentation/v15dn_multi_active_landscape_synthesis.md`
- `Documentation/v15dn_multi_active_landscape_placement_rows.csv`
- `Documentation/v15dn_multi_active_landscape_seed_summary.csv`
- `Documentation/v15dn_multi_active_landscape_set_rule_scores.csv`
- `Documentation/v15dn_multi_active_landscape_metric_scores.csv`
- `Documentation/v15dn_multi_active_landscape_diagnosis.csv`
- `Documentation/v0_15dn_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dn.md`

## 10bo. v15do fant mange perfekte aktivt-sett-type-screens, som betyr underbestemmelse

`v15do` var en no-new-dynamics syntese etter v15dn.
Den brukte v15dn sine placement-rader og laget seed-level pre-run kontraster for aa teste om de to observerte aktivt-sett-landskapene kunne skilles:

- `p1_only`: seeds `202` og `404`
- `p0_p2`: seeds `303` og `505`

Scope:

- target `1024`
- perturbation `add_chord`
- placements `p0,p1,p2`
- growth seeds `202/303/404/505`
- ingen ny dynamikk
- response er aktivt sett fra eksisterende v15dn/v15dl/v15dm-rader

Hovedfunn:

- det finnes perfekte kompakte post-hoc type-regler paa de fire eksisterende seedene
- best sorterte comparison-regel er `delta_return_t2/p0_ge_p1 -> p0_p2 else p1_only`
- denne regelen har exact-set-match `1.000`, coverage `1.000`, precision `1.000`, burden `0.500`
- men det finnes `110` perfekte kompakte regler over `17` metrikker
- dette er ikke robusthet; det er underbestemmelse fra for lite n og for stort feature-rom

Tolkning:

- v15do gir nyttig ny viten ved aa vise at aktivt-sett-type kan beskrives mer kompakt enn v15dn sin top2-screen
- samtidig svekker v15do selector-claimet, fordi altfor mange post-hoc regler forklarer de samme fire seedene
- neste dynamiske runde maa velge og fryse en enkel type-guard foer run, helst paa minst to nye growth seeds
- ikke refit `delta_return_t2`, `local_ball3_beta1` eller terskler etter holdout
- dette er ikke evidens for Lorentz-likhet, global invariant, entanglement, partikler eller universell emergent geometri

Viktige filer:

- `relational_universe_v15do_active_set_type_discriminator_synthesis.py`
- `Documentation/v15do_active_set_type_discriminator_synthesis.md`
- `Documentation/v15do_active_set_type_seed_features.csv`
- `Documentation/v15do_active_set_type_comparison_rules.csv`
- `Documentation/v15do_active_set_type_threshold_rules.csv`
- `Documentation/v15do_active_set_type_diagnosis.csv`
- `Documentation/v0_15do_operativ_anbefaling.md`

## 10bp. v15dp pensjonerte den beste v15do-guarden paa fresh seeds

`v15dp` tok den anbefalte holdout-runden etter v15do:

- velg en enkelt type-guard foer dynamikk
- skriv pre-run guard/morfologi til CSV foer run-loop
- test paa minst to nye growth seeds
- ikke refit terskler eller metrikker etter outcome

Frossen guard:

- `delta_return_t2/p0_ge_p1 -> p0_p2 else p1_only`
- kilde: beste sorterte v15do post-hoc comparison-regel
- target `1024`
- perturbation `add_chord`
- placements `p0,p1,p2`
- growth seeds `606/707`
- seed-deltaer `15007/15061/15121/15187`

Pre-run:

- seed `606`: `delta_return_t2(p0)=-0.011`, `delta_return_t2(p1)=-0.010`, predikert `p1_only`
- seed `707`: `delta_return_t2(p0)=-0.092`, `delta_return_t2(p1)=-0.021`, predikert `p1_only`

Faktisk dynamikk:

- seed `606`: ingen aktive placements; p0/p1/p2 alle `0.000` established-rate
- seed `707`: `p0_only`; p0 established-rate `0.750`, p1/p2 `0.000`
- samlet run-labels: `established_far_shell_horizon:3`, `mixed_far_shell_horizon:1`, `no_far_shell_horizon:20`

Score:

- type accuracy `0.000`
- exact-set-match `0.000`
- coverage `0.000`
- precision `0.000`
- guard-status `guard_inconclusive_unobserved_active_set_type`

Tolkning:

- dette er ikke bare svak selector-ytelse; fresh seeds introduserer aktivt-sett-typer utenfor v15do sitt to-type-rom (`none`, `p0_only`)
- den konkrete v15do-guarden skal pensjoneres som selector-kandidat
- ikke refit `delta_return_t2/p0_ge_p1` etter outcome
- neste interessante steg er aktivt-sett-taksonomi/landskapsstruktur over flere seeds, ikke mer single-guard-refinement
- dette er fortsatt lokal defect/response-struktur, ikke evidens for Lorentz-likhet, global invariant, entanglement, partikler eller universell emergent geometri

Viktige filer:

- `relational_universe_v15dp_active_set_type_guard_holdout.py`
- `Documentation/v15dp_active_set_type_guard_holdout.md`
- `Documentation/v15dp_active_set_type_guard_pre_run_guard.csv`
- `Documentation/v15dp_active_set_type_guard_pre_run_morphology.csv`
- `Documentation/v15dp_active_set_type_guard_placement_summary.csv`
- `Documentation/v15dp_active_set_type_guard_seed_evaluation.csv`
- `Documentation/v15dp_active_set_type_guard_evaluation.csv`
- `Documentation/v15dp_active_set_type_guard_diagnosis.csv`
- `Documentation/v0_15dp_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dp.md`

## 10bq. v15dq gjorde type-rommet eksplisitt foer mer dynamikk

`v15dq` tok neste smarte steg etter v15dp:

- ingen ny dynamikk
- les v15dn og v15dp placement/morphology CSV-er
- samle alle kjente `1024/add_chord/p0,p1,p2` growth-seed-landskap
- formaliser aktivt-sett-taksonomien foer nye selector-forsok
- sjekk pre-run contrasts med lekkasjevakt, altsaa uten outcome-felter som features

Hvorfor dette var smart:

- v15dp feilet ikke bare som guard; den viste at v15do sitt to-type-rom var for smalt
- aa refitte `delta_return_t2/p0_ge_p1` ville optimalisert en regel for feil taksonomi
- en no-new-dynamics syntese er billigere og mer epistemisk ryddig enn aa bruke mer runtime foer vi vet hvilke responsklasser som finnes

Observert taksonomi over seks seeds:

- `single_active_p1`: seeds `202/404`
- `multi_active_p0_p2`: seeds `303/505`
- `no_active`: seed `606`
- `single_active_p0`: seed `707`

Hovedresultat:

- gammel v15do two-type-space dekker bare `4/6` seeds
- nye v15dp-klasser dekker `2/6` seeds
- repeated classes er `single_active_p1` og `multi_active_p0_p2`
- singleton classes er `no_active` og `single_active_p0`

Pre-run contrast audit etter lekkasjevakt:

- `65` rene repeated-pair contrasts finnes i dagens tiny sample
- return-probability-familien har `33`
- curvature/shortcut har `11`
- local-volume/topology har `8`
- support-volume/topology har `9`
- shortcut/reach har `4`

Tolkning:

- contrastene er leads, ikke validerte selectors
- singleton-klassene er taksonomisk viktige, men kan ikke laere en robust mapper alene
- neste dynamiske budsjett bor brukes paa taxonomy-mapping eller flere fresh seeds for klassefrekvens
- ikke refit v15do/v15dp-guarden
- ikke oppgrader til Lorentz-likhet, global invariant, entanglement, partikler eller universell emergent geometri

Viktige filer:

- `relational_universe_v15dq_active_set_taxonomy_synthesis.py`
- `Documentation/v15dq_active_set_taxonomy_synthesis.md`
- `Documentation/v15dq_active_set_taxonomy_placement_rows.csv`
- `Documentation/v15dq_active_set_taxonomy_seed_summary.csv`
- `Documentation/v15dq_active_set_taxonomy_class_summary.csv`
- `Documentation/v15dq_active_set_taxonomy_seed_features.csv`
- `Documentation/v15dq_active_set_taxonomy_pairwise_type_contrasts.csv`
- `Documentation/v15dq_active_set_taxonomy_feature_family_summary.csv`
- `Documentation/v15dq_active_set_taxonomy_diagnosis.csv`
- `Documentation/v0_15dq_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dq.md`

## 10br. v15dr viste at repeated-class mapperen ikke holder

`v15dr` tok neste naturlige steg etter v15dq:

- bruk v15dq sine repeated-class contrasts som treningsgrunnlag
- bygg en liten deterministic taxonomy-mapper foer ny dynamikk
- la mapperen svare `unknown` hvis fresh morphology faller utenfor known repeated-class envelope
- kjor fresh holdout paa target `1024`, `add_chord`, placements `p0,p1,p2`
- bruk growth seeds `808/909/1001/1103` og seed-deltaer `17011/17053/17107/17167`
- evaluer active-set type etter dynamikk uten refit

Hvorfor dette var smart:

- v15dq viste at to-type-rommet var for smalt, men repeated classes fantes fortsatt
- en mapper med eksplisitt `unknown` er strengere enn en ny single-feature guard
- hvis mapperen traff known classes eller abstained paa OOD, kunne vi ha testet en mer moden configuration heuristic

Pre-run mapper:

- seed `808`: predikerte `multi_active_p0_p2`
- seed `909`: predikerte `single_active_p1`
- seed `1001`: predikerte `multi_active_p0_p2`
- seed `1103`: predikerte `multi_active_p0_p2`

Faktisk fresh taxonomy:

- seed `808`: `single_active_p2`
- seed `909`: `no_active`
- seed `1001`: `single_active_p2`
- seed `1103`: `multi_active_p0_p1`

Hovedresultat:

- alle fire fresh seeds var OOD relativt til repeated-class-rommet fra v15dq
- mapperen abstained ikke paa noen av dem
- `overall_exact_set_match_rate = 0.000`
- `ood_abstain_accuracy = 0.000`
- `coverage_fraction = 0.750`, men bare med mange falske positive (`precision_fraction = 0.429`)
- diagnosen er `taxonomy_mapper_not_supported`

Tolkning:

- det var riktig aa teste mapperen, men den feilet rent som selector
- v15dr utvider taksonomien med `single_active_p2` og `multi_active_p0_p1`
- neste gevinst bor komme fra klassefrekvens-/landskapsatlas eller OOD-foerst design
- ikke refit samme repeated-class mapper etter outcome
- ikke oppgrader til Lorentz-likhet, global invariant, entanglement, partikler eller universell emergent geometri

Viktige filer:

- `relational_universe_v15dr_active_set_taxonomy_mapper_holdout.py`
- `Documentation/v15dr_active_set_taxonomy_mapper_holdout.md`
- `Documentation/v15dr_active_set_taxonomy_mapper_spec.csv`
- `Documentation/v15dr_active_set_taxonomy_mapper_pre_run_mapper.csv`
- `Documentation/v15dr_active_set_taxonomy_mapper_pre_run_morphology.csv`
- `Documentation/v15dr_active_set_taxonomy_mapper_run_features.csv`
- `Documentation/v15dr_active_set_taxonomy_mapper_placement_summary.csv`
- `Documentation/v15dr_active_set_taxonomy_mapper_seed_evaluation.csv`
- `Documentation/v15dr_active_set_taxonomy_mapper_evaluation.csv`
- `Documentation/v15dr_active_set_taxonomy_mapper_diagnosis.csv`
- `Documentation/v0_15dr_operativ_anbefaling.md`
- `Documentation/relasjonell_universgraf_for_ikke_spesialister_v0_15dr.md`

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
