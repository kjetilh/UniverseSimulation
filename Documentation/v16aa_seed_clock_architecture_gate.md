# UniverseSimulation v16aa: seed-clock architecture gate

Dato: 2026-07-12

## Konklusjon

Gaten velger `exposure_matched_local` med fast lokal per-host-rate `0.000503953815` som kandidat for en fresh dynamisk holdout.

Dette er ikke en ny anchor og ikke dynamisk validering. Raten er fittet til eksisterende v15dx token-time exposure for aa bevare seed-budsjettet i foerste orden. Kandidaten maa fryses og testes paa fresh growth seeds foer den kan erstatte dagens globale klokke.

## Rekonstruksjon

- Anchor-runs: `24`.
- Observerte events: `81936`.
- Observerte seed-events: `39`.
- Rekonstruert total kontinuerlig tid: `967.614417`.
- Rekonstruert token-time integral: `76801.832942`.
- Time-weighted effektivt tokenantall: `79.372353`.
- Median initial K: `16.000000`.
- Forventet global-clock seed exposure: `38.704577` mot `39` observerte seeds.

Tokenantallet rekonstrueres foer hvert logget `dt`; birth oeker K etter intervallet og death reduserer K. Dermed kan en kontrafaktisk fast lokal hazard beregnes som `rho_seed * integral K(t) dt` uten aa finne paa nye dynamiske resultater.

## Kandidater

| candidate | local_rate_per_host | bounded_local | retains_node_growth | aggregate_ratio_vs_current | min_run_ratio_vs_current | max_run_ratio_vs_current | selection_pass | evidence_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| current_global | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.000000 | architecture_control_or_rejected_candidate |
| naive_local_per_token | 0.040000 | 1.000000 | 1.000000 | 79.372353 | 61.733819 | 98.570196 | 0.000000 | architecture_control_or_rejected_candidate |
| initial_median_local | 0.002500 | 1.000000 | 1.000000 | 4.960772 | 3.858364 | 6.160637 | 0.000000 | architecture_control_or_rejected_candidate |
| exposure_matched_local | 0.000504 | 1.000000 | 1.000000 | 1.000000 | 0.777775 | 1.241871 | 1.000000 | fit_candidate_requires_fresh_holdout |
| preparation_only | 0.000000 | 1.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | architecture_control_or_rejected_candidate |
| explicit_global_background | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.000000 | architecture_control_or_rejected_candidate |

Den naive lokale kandidaten gjenbruker `0.04` som rate per token og gir derfor en omtrent K-ganger stoerre seed-exposure. Initial-K-kalibreringen undervurderer at K vokser kraftig under runnet. Exposure-matching bruker i stedet en fast rate bestemt av time-weighted K; den er lokal etter fit fordi raten ikke leser K under dynamikken.

`preparation_only` er en viktig kontroll, men kan ikke vaere hovedkandidat dersom fysisk nodevekst skal beholdes. `explicit_global_background` er koherent bare for en betinget lokal subdynamikk; den gir ikke whole-system intrinsic causality.

## Remote-context gate

| candidate | context | base_intensity | remote_intensity | absolute_difference | remote_invariant | bounded_local |
| --- | --- | --- | --- | --- | --- | --- |
| current_global | token_host | 0.040000 | 0.020000 | 0.020000 | 0.000000 | 0.000000 |
| current_global | node_host_no_tokens | 0.010000 | 0.008000 | 0.002000 | 0.000000 | 0.000000 |
| naive_local_per_token | token_host | 0.040000 | 0.040000 | 0.000000 | 1.000000 | 1.000000 |
| naive_local_per_token | node_host_no_tokens | 0.040000 | 0.040000 | 0.000000 | 1.000000 | 1.000000 |
| initial_median_local | token_host | 0.002500 | 0.002500 | 0.000000 | 1.000000 | 1.000000 |
| initial_median_local | node_host_no_tokens | 0.002500 | 0.002500 | 0.000000 | 1.000000 | 1.000000 |
| exposure_matched_local | token_host | 0.000504 | 0.000504 | 0.000000 | 1.000000 | 1.000000 |
| exposure_matched_local | node_host_no_tokens | 0.000504 | 0.000504 | 0.000000 | 1.000000 | 1.000000 |
| preparation_only | token_host | 0.000000 | 0.000000 | 0.000000 | 1.000000 | 1.000000 |
| preparation_only | node_host_no_tokens | 0.000000 | 0.000000 | 0.000000 | 1.000000 | 1.000000 |
| explicit_global_background | token_host | 0.040000 | 0.020000 | 0.020000 | 0.000000 | 0.000000 |
| explicit_global_background | node_host_no_tokens | 0.010000 | 0.008000 | 0.002000 | 0.000000 | 0.000000 |

## Relabel gate

| candidate | graph_count | trials | max_abs_error | failures | relabel_pass |
| --- | --- | --- | --- | --- | --- |
| current_global | 992.000000 | 1984.000000 | 0.000000 | 0.000000 | 1.000000 |
| naive_local_per_token | 992.000000 | 1984.000000 | 0.000000 | 0.000000 | 1.000000 |
| initial_median_local | 992.000000 | 1984.000000 | 0.000000 | 0.000000 | 1.000000 |
| exposure_matched_local | 992.000000 | 1984.000000 | 0.000000 | 0.000000 | 1.000000 |
| preparation_only | 992.000000 | 1984.000000 | 0.000000 | 0.000000 | 1.000000 |
| explicit_global_background | 992.000000 | 1984.000000 | 0.000000 | 0.000000 | 1.000000 |

## Gate-evaluering

| gate | status | observed | required | decision |
| --- | --- | --- | --- | --- |
| input_integrity | pass | runs=24;events=81936 | runs=24;events=81936 | continue |
| global_clock_reconstruction | pass | 1.007633 | observed/expected in [0.5,1.5] | continue |
| selected_remote_invariance | pass | 0.000000 | <=1e-12 | continue |
| selected_relabel_covariance | pass | 0.000000 | <=1e-12 | continue |
| unique_architecture_candidate | pass | exposure_matched_local | exactly one | freeze_for_fresh_holdout |
| fresh_validation | not_run | none | fresh growth seeds; no refit | do_not_start_v16b |
| v16aa_overall | candidate_selected_not_validated | exposure_matched_local | fresh holdout before architecture adoption | run_fresh_seed_clock_holdout |

## Evidensstatus

- Lokaliteten og relabel-egenskapen til en fast per-host-rate er eksakte arkitekturfakta.
- Ratevalget er fittet paa v15dx og har ingen fresh evidens.
- Exposure-ratio er en foersteordens kontrafaktisk beregning paa eksisterende trajectories; den inkluderer ikke feedback fra ekstra seed-noder til senere birth/move/swap-hazards.
- Resultatet sier ingenting direkte om Lorentz-likhet, spacetime eller universell geometri.

## Neste gate

Kjoer en fresh, matched scheduler-holdout paa growth seeds som ikke inngikk i fittet:

- current_global som baseline
- preparation_only som mekanismekontroll
- `exposure_matched_local` med frosset `rho_seed=0.000503953815`
- separate RNG/ID-allokatorer og samme eventbudsjett
- primaert seed-exposure, nodevekst, tokenvekst, total tid og family-rate shock
- ingen refit etter fresh resultater

Bare dersom den lokale kandidaten unngaar katastrofal vekst og holder seed-/family-budsjettet innen frosne toleranser, rerunnes v16a-locality-gaten og v16b event-DAG kan vurderes.
