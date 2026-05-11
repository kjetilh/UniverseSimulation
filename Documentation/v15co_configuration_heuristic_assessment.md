# Relasjonell universgraf v0.15co: configuration heuristic assessment

## Formal

Denne runden kjorer ingen ny universdynamikk. Den svarer paa et metodisk spoersmaal:

Kan egenskaper vi kjenner fra vaart univers, som Lorentz-likhet, invarianter, globale regler og entanglement, brukes som heuristikk for valg av konfigurasjoner i repoet?

Kort svar: ja, men bare som en svak og falsifiserbar prioriteringsheuristikk etter oversettelse til repo-observabler. Ordene kan ikke brukes direkte som konklusjoner.

## Verified current state

- `band_zero_del` er fortsatt arbeidsregime fra `v11e`; dette er regimevalg, ikke fysikkbevis.
- Lorentz-/spacetime-sporet er fortsatt `not_yet`: `v14`, `v14b` og `v14c` viser rene nok kontroller til aa ta signalet alvorlig, men fortsatt mode-dependence, placement-sensitivity og uavklart lokal anisotropi.
- Defect-/interaction-sporet er fortsatt den sterkeste positive retningen: `v15b` viser ikke-triviell pair-vs-single non-superposition, og `v15g` viser delvis strukturerte genealogy/event-chain-moenstre.
- Quasi-invariant-sporet er interessant, men betinget: `v12`/`v13` peker paa spektral relativ drift som beste ikke-trivielle kandidat, mens `v15bl` skjerper dette etter carrier/family-conditioning. Dette er ikke en global lov.
- Global-budget/global-regel-spraak skal holdes nede: `v15cl` finner ikke ren inner-gate eller global-budget-kobling.
- Skala er fortsatt en hard sperre for store paastander: `v15cn` holder target-768 p2-lommen live, men target 1024 stoetter ikke p2 under samme absolute step budget.

## Heuristic axes

| axis_id | current_status | selector_role | priority | confidence |
| --- | --- | --- | --- | --- |
| A0_artifact_hygiene | mandatory_clean_gate | hard_gate | must_pass | high |
| A1_defect_nonseparability | strongest_active_signal_but_mesoscale | positive_search_axis | high | medium_high |
| A2_conditional_quasi_invariant | weak_to_moderate_positive_selector | secondary_positive_axis | medium | medium |
| A3_lorentz_like | not_yet | negative_filter_or_diagnostic_only | medium_low | medium_high_negative |
| A4_global_rules | not_yet | instrumentation_axis | medium_low | medium_negative |
| A5_scale_robustness | unresolved_budget_caveat | holdout_gate | high_for_claims | medium |
| A6_local_isotropy_geometry | not_explained | risk_penalty | medium | medium |

## Candidate rules

| rule_id | rule_name | rule_type | then_decision |
| --- | --- | --- | --- |
| R0 | hygiene_before_physics | hard_gate | reject or rerun before interpretation |
| R1 | nonseparability_is_search_signal | positive_prioritization | prioritize as defect/interaction candidate |
| R2 | conditioned_invariant_before_global_invariant | positive_but_capped | use as local carrier heuristic; require cross-family and scale holdout before law language |
| R3 | lorentz_not_positive_selector_yet | negative_filter | do not upgrade to Lorentz-like; use as anisotropy diagnostic |
| R4 | global_rule_language_requires_derivation_or_holdout | language_guardrail | report as diagnostic or sanity metric only |
| R5 | scale_before_universe_like_claim | claim_gate | keep as live pocket but run budget-scaled or intermediate-scale holdout before stronger interpretation |

## Decision table

| candidate_direction | decision | next_use |
| --- | --- | --- |
| target768_p2_horizon_local_swap | retain_as_contrast_anchor_not_final_target | compare against target1024 scaled-budget or intermediate target |
| target768_p2_horizon_add_chord | retain_as_carrier_contrast | do not overfit; use beside local_swap to test carrier dependence |
| target1024_p2_same_absolute_budget | do_not_discard_until_budget_scaled | run scaled-budget 1024 or one intermediate scale |
| lorentz_front_speed_as_selector | do_not_use_as_positive_selector | keep as diagnostic after stronger mesoscale signal appears |
| entanglement_like_wording | forbidden_as_claim | rename to pair_non_superposition unless a formal Bell-like measurement framework exists |

## Physics anchors and repo translations

| anchor | external_source | url | usable_repo_translation | strict_caveat |
| --- | --- | --- | --- | --- |
| Relativity / Lorentz-like behavior | Einstein 1905, On the Electrodynamics of Moving Bodies | https://en.wikisource.org/wiki/On_the_Electrodynamics_of_Moving_Bodies_(1920_edition) | frame/mode/placement robustness of propagation observables | repo does not have coordinates, clocks, metric tensor, or demonstrated invariant signal speed |
| Symmetry -> conservation / invariant laws | Noether 1918, Invariante Variationsprobleme | https://eudml.org/doc/59024 | look for quantities with low drift that also predict or compress dynamics across families | zero drift in nodes/beta1 is not a law unless it survives off-regime and has a derivation |
| Gauge/symmetry interpretation of conservation | Stanford Encyclopedia of Philosophy, Gauge Theories in Physics, section on Noether theorem | https://plato.stanford.edu/entries/gauge-theories/ | treat invariance claims as requiring both formal structure and empirical/dynamical relevance | current repo has graph dynamics, not a Lagrangian field theory |
| Entanglement / nonseparability | Bell 1964, On the Einstein Podolsky Rosen paradox | https://journals.aps.org/ppf/abstract/10.1103/PhysicsPhysiqueFizika.1.195 | only a weak proxy is available: non-superposition of paired local defects versus matched single controls | collision non-superposition is not quantum entanglement; there is no Bell test, Hilbert space, or measurement-setting formalism here |

## Interpretation

Det er mulig aa lage en heuristikk, men bare hvis vi skiller mellom inspirasjon og evidens:

- Lorentz-likhet er forelopig en negativ filter-/diagnostikkakse, ikke en positiv selector.
- Invariant-spraak er forelopig en conditional quasi-invariant-akse: spektral drift kan prioritere carrier/family-runder, men ikke etablere globale lover.
- Globale regler maa behandles som instrumentering, ikke som konklusjon, inntil en observabel overlever skala, carrier og kontrollfamilier.
- Entanglement er ikke en tillatt paastand i dagens repo. Den naermeste repo-lokale proxyen er pair non-superposition under matched single controls.
- Defect non-superposition og genealogy er den beste positive signalaksen akkurat naa, men den sier "real mesoscale interaction", ikke "partikkel".

## Next natural step

Neste dynamiske steg boer vaere en liten scale/budget-runde, ikke et nytt bredt soek:

`target1024_scaled_budget_p2_horizon` eller ett mellomtarget mellom `768` og `1024`.

Grunnen er at `v15cn` gir den viktigste claim-gaten: hvis p2 bare finnes ved target 768 under dagens absolutte budsjett, kan vi ikke bruke den som universe-like selector. Hvis den kommer tilbake ved skalanormalisert budsjett eller mellomskala, blir p2-lommen mye mer interessant som testbenk for conditional quasi-invariant og defect-interaction observabler.

## Evidence discipline

Denne rapporten introduserer ingen nye runtime-resultater. CSV-ene er syntese-/beslutningstabeller basert paa eksisterende repo-filer og eksterne begrepsankere. De skal ikke leses som maalinger fra en ny simulering.
