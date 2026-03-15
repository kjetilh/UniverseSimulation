# v0.6 Uniformized Coupling: Codex Assessment

## Scope

Dette notatet bruker den aktive v0.6-laben i [relational_universe_uniformized_coupling_lab.py](/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/relational_universe_uniformized_coupling_lab.py) og de to representative kjøringene:

- `codex_v06_token_open_moderate`
- `codex_v06_full_open_moderate`

Rå headline-metrics for disse kjøringene ligger i [uniformized_v06_codex_raw_results.csv](/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/Documentation/uniformized_v06_codex_raw_results.csv).

## Hva koden faktisk implementerer

### Family-rater

De fire event-familiene er:

- `seed`
- `token`
- `birth`
- `death`

De lokale family-ratene er definert i [relational_universe_uniformized_coupling_lab.py](/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/relational_universe_uniformized_coupling_lab.py#L472):

- `lambda_seed = r_seed`
- `lambda_token = r_token * K`
- `lambda_birth = r_birth * sum_t (1 + birth_degree_bias * max(deg(node_t)-1, 0))`
- `lambda_death = r_death * sum_t death_weight(t)` når `K > min_tokens`, ellers `0`

der `death_weight(t) = death_inverse_degree_scale / (1 + deg(node_t))`.

### Dominerende family-klokke

I [coupled_step](/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/relational_universe_uniformized_coupling_lab.py#L626) beregnes for hver familie

- `mu_f = max(lambda_f^control, lambda_f^perturbed)`

og total dominerende rate

- `M = sum_f mu_f`

Deretter trekkes `dt ~ Exp(M)` og en familie `f` med sannsynlighet `mu_f / M`.

### Thinning-regelen

Når familie `f` er valgt, brukes én felles uniform `U`:

- kontroll aksepterer hvis `U < lambda_f^control / mu_f`
- perturbert aksepterer hvis `U < lambda_f^perturbed / mu_f`

Dette er familywise thinning. Det er den sentrale v0.6-konstruksjonen.

### Lokal kobling innen hver familie

Når en familie er akseptert, brukes felles uniforms og rank/vekt-kobling:

- `seed`: felles `u_anchor` velger vertsnode, og delt `new_node_id` brukes når grenene begge aksepterer.
- `token`: felles `u_token`, `u_neighbor`, `u_rule` og `u_candidate` styrer tokenvalg, traversering og lokal `delete`/`triad`/`swap`.
- `birth`: felles `u_host` og delt `new_token_id`; verts-token velges ved samme uniform mot hver grens egne vekter.
- `death`: felles `u_token`; token som dør velges ved samme uniform mot hver grens egne death-vekter.

Dette gir høy samvariasjon, men er ikke full maksimal kobling av hele lokale overgangskjernen.

## Hva som er eksakt og hva som er heuristisk

### Matematisk eksakt

- Familywise marginal correctness er eksakt: hver gren ser riktig family-rate etter uniformization + thinning.
- Den delte potensial-klokken er eksakt for den dominerende family-prosessen.
- Bernoulli-aksept per valgt familie er maksimal gitt `mu_f = max(lambda_f^A, lambda_f^B)`.
- Delt node-ID og token-ID ved felles `seed` og `birth` gjør at identitet ikke driver kunstig divergens når begge grener aksepterer samme familie.

### Heuristisk eller bare praktisk kobling

- Koblingen av vektede tokenvalg i `birth` og `death` er ikke maksimal; den er en delt-uniform-kobling.
- Koblingen av nabovalg og kandidatvalg i `token`-familien er heller ikke maksimal; den er rank-koblet.
- Hele den lokale overgangskjernen er derfor ikke maksimalt koblet, bare familywise korrekt og lokalt samkjørt.
- `fit_speed_control` er en deskriptiv lineær fit av radius mot eventtid, ikke en bevist fysisk hastighetsgrense.

## Hva målene betyr

Målene under kommer fra [damage_snapshot](/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/relational_universe_uniformized_coupling_lab.py#L765) og [summarize_coupling](/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/relational_universe_uniformized_coupling_lab.py#L837).

- `radius_control`: maksimal grafavstand i kontrollgeometrien fra perturbasjonens støtte til skademengden. Dette er hovedmålet for geometrisk spredning.
- `delta_tokens`: forskjell i token-antall mellom grenene. Dette er åpenhets- og populasjonsdrift, ikke geometri.
- `core_l1`: absolutt differanse over `(tokens, nodes, components, beta1)`. Dette måler grov topologisk og populasjonsmessig drift.
- `regime_l1`: absolutt differanse over høyere strukturmål som `wedges`, `triangles`, `c4`, `spectral_radius`, `clustering`, `dim_proxy`. Dette er struktur- og eksitasjonsdrift mer enn ren støtte-radius.
- `both_accept_total`: antall potensial-hendelser der begge grener faktisk aksepterte valgt familie. Dette er et mål på hvor sterkt grenene fortsatt drives av felles støy.
- `one_sided_total`: antall potensial-hendelser der bare én gren aksepterte. Dette er et direkte mål på hvor åpent og divergerende regimet er under familywise kobling.

## Representative kjøringer

### A. Token-open moderate

Kjøring:

```bash
python3 relational_universe_uniformized_coupling_lab.py \
  --label codex_v06_token_open_moderate \
  --steps 3000 \
  --seed 321 \
  --initial-cycle 10 \
  --initial-tokens 4 \
  --token-open-moderate \
  --perturbation local_swap \
  --log-every 50 \
  --out-log-csv Documentation/uniformized_v06_token_open_moderate_log.csv \
  --out-events-csv Documentation/uniformized_v06_token_open_moderate_events.csv \
  --out-summary-md Documentation/uniformized_v06_token_open_moderate_summary.md \
  --out-lay-md Documentation/uniformized_v06_token_open_moderate_lay.md \
  --out-json Documentation/uniformized_v06_token_open_moderate_report.json
```

Hovedtall:

- `final_radius_control = 3`
- `max_radius_control = 4`
- `final_delta_tokens = 5`
- `final_core_l1 = 5`
- `final_regime_l1 = 8.385`
- `both_accept_total = 2887`
- `one_sided_total = 113`
- `both_accept_frac = 0.962`
- `one_sided_frac = 0.0377`

Lesning:

- Koblingskvaliteten er høy; nesten alle potensial-hendelser aksepteres i begge grener.
- Det finnes fortsatt åpenhet nok til at `delta_tokens` driver.
- Geometrisk spredning er lesbar, men denne ene seeden gir negativ lineær fit på slutten fordi radius ikke vokser monotont gjennom hele runen. Det er en deskriptiv effekt, ikke et motbevis mot lokalitet.

### B. Full-open moderate

Kjøring:

```bash
python3 relational_universe_uniformized_coupling_lab.py \
  --label codex_v06_full_open_moderate \
  --steps 3000 \
  --seed 321 \
  --initial-cycle 10 \
  --initial-tokens 4 \
  --full-open-moderate \
  --perturbation local_swap \
  --log-every 50 \
  --out-log-csv Documentation/uniformized_v06_full_open_moderate_log.csv \
  --out-events-csv Documentation/uniformized_v06_full_open_moderate_events.csv \
  --out-summary-md Documentation/uniformized_v06_full_open_moderate_summary.md \
  --out-lay-md Documentation/uniformized_v06_full_open_moderate_lay.md \
  --out-json Documentation/uniformized_v06_full_open_moderate_report.json
```

Hovedtall:

- `final_radius_control = 1`
- `max_radius_control = 5`
- `final_delta_tokens = 3`
- `final_core_l1 = 6`
- `final_regime_l1 = 0`
- `both_accept_total = 2816`
- `one_sided_total = 184`
- `both_accept_frac = 0.939`
- `one_sided_frac = 0.0613`

Lesning:

- Regimet er mer åpent enn token-open moderate, men radiusen blir mindre stabil som sluttmål.
- Mer av divergensen går inn i ensidige aksepter og core-drift enn i en pen, vedvarende front.
- Denne seeden ser derfor mer ut som lokal scrambling og populasjonsdrift enn som ren spacetime-lignende frontutbredelse.

## Sammenlikning mot bundle-v5 sin multikjøring

Bundle-v5 sin aggregatoppsummering i [uniformized_coupling_multirun_summary.md](/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/Documentation/uniformized_coupling_multirun_summary.md) er viktigere enn én enkelt seed:

- `token_open_moderate`: mean final radius `3.650`, mean max radius `5.200`, mean both-accept fraction `0.873`, mean one-sided fraction `0.127`
- `full_open_moderate`: mean final radius `0.550`, mean max radius `3.150`, mean both-accept fraction `0.585`, mean one-sided fraction `0.415`

Det er den riktige grunnen til at `token_open_moderate` bør regnes som bedre kandidat for videre spacetime-testing, ikke bare den enkelte Codex-kjøringen.

## Vurdering

### Er dette en god kandidat for videre spacetime-testing?

Ja, men bare i den moderate token-open sektoren.

Begrunnelse:

- Familywise-koblingen er matematisk mye renere enn v0.5 i åpne regimer.
- `token_open_moderate` holder høy `both_accept` og moderat `one_sided`, som betyr at grenene fortsatt deler mye struktur samtidig som regimet er genuint åpent.
- Bundle-v5 sine multirun-data viser tydelig større og mer lesbar radiusutbredelse i `token_open_moderate` enn i `full_open_moderate`.

`full_open_moderate` er derimot svakere som første spacetime-kandidat fordi:

- ensidige aksepter blir langt vanligere,
- token- og core-drift tar mer plass,
- og radiusen blir mindre stabil som lesbar geometri.

## Forbedringer gjort i koden denne runden

Jeg gjorde to praktiske forbedringer som var verdt å beholde:

- CLI-aliasene `--token-open-moderate` og `--full-open-moderate` er lagt til i [relational_universe_uniformized_coupling_lab.py](/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/relational_universe_uniformized_coupling_lab.py), fordi promptene og bundle-teksten brukte disse navnene mens parseren opprinnelig bare hadde `--token-open-topologically-closed` og `--full-open`.
- Begge v0.6-skriptene oppretter nå parent-kataloger for output-filer automatisk, og scan-scriptet skriver også aggregert CSV via `--out-aggregate-csv`.

Dette er ikke teoretiske endringer, men de gjør v0.6-verktøyene konsistente med dokumentasjonen og enklere å bruke reproduserbart.

## Neste eksperiment

Det neste riktige eksperimentet er nå:

1. Kjør et eksplisitt parameter-scan rundt `token_open_moderate` med [relational_universe_uniformized_scan.py](/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/relational_universe_uniformized_scan.py).
2. Ranger regimer etter kombinasjonen:
   - høy `both_accept_frac`
   - moderat `one_sided_frac`
   - ikke-triviell `max_radius_control`
   - kontrollert drift i `delta_tokens` og `delta_beta1`
3. Gå deretter til v0.7-prompten og forbedre lokal maksimal kobling innen familiene, spesielt for vektede valg i `birth` og `death` og for lokale valg i `token`-familien.

Kort sagt:

- v0.6 gjør åpen-regime-testen metodisk legitim
- `token_open_moderate` er den beste nåværende spacetime-kandidaten
- v0.7 bør fokusere på bedre lokal maksimal kobling, ikke ny ontologi
