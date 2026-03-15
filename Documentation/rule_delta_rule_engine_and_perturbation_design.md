# Teknisk design: rule-engine og perturbasjonslab v0.4

## Formål

Dette notatet beskriver den faktiske v0.4-refaktoren som nå ligger i kodebasen. Målet har vært å gjøre overgangen fra invariantanalyse til lokal kausal spredning metodisk presis.

## Modulstruktur

- `rule_delta_lab/graph_core.py`
  Felles graf- og state-primitiver.
- `rule_delta_lab/features.py`
  Feature-ekstraksjon, redusert basis og algebraiske identiteter.
- `rule_delta_lab/rules.py`
  Primitive regelobjekter og lokal kontekst.
- `rule_delta_lab/analysis.py`
  Nullromsanalyse, residualtester og Markdown-rapportering for rule-delta-labben.
- `rule_delta_lab/simulator.py`
  Gillespie-lignende scheduler som bevarer eksisterende `relational_universe_rule_delta_lab.py`-CLI.
- `rule_delta_lab/perturbation.py`
  Kopla kjøringer med delt RNG-strøm og måling av spredningsfront.

## Regelkontrakt

Hver primitiv regel er nå et objekt med:

- `candidate_contexts(state, traversal)`
- `applies(state, context)`
- `apply(state, context, rng)`
- `delta_core(context)`
- `delta_motif(context)`

Det skiller tre ting som tidligere lå blandet sammen:

1. lokal matching,
2. eksakte analytiske deltaformler,
3. og faktisk state-mutasjon.

## Hva som er eksakt

### Algebraiske identiteter

- `beta1 = edges - nodes + components`
- `deg_sq_sum = 2*wedges + 2*edges`

Disse er definisjonelle og skal ikke tolkes som bevaringslover.

### Eksakte regelstyrte deltaer i kjernebasis

- `seed`: `Δ(nodes)=+1`
- `birth`: `Δ(tokens)=+1`
- `death`: `Δ(tokens)=-1`
- `triad`: `Δ(beta1)=+1`
- `delete`: `Δ(beta1)=-1`
- `swap`: null i kjernebasis

### Eksakte lokale motivformler

- `seed`: `Δwedges = h`, `Δtriangles = 0`, `Δstar3 = C(h,2)`
- `triad`: `Δwedges = d_v + d_w`, `Δtriangles = c`, `Δstar3 = C(d_v,2)+C(d_w,2)`
- `delete`: `Δwedges = -[(d_v-1)+(d_u-1)]`, `Δtriangles = -c`, `Δstar3 = -[C(d_v-1,2)+C(d_u-1,2)]`
- `swap`: `Δwedges = -(d_u-1)+d_w`, `Δtriangles = -c_del + (c_add - 1)`, `Δstar3 = -C(d_u-1,2)+C(d_w,2)`

`swap`-formelen er viktig: `-1`-leddet i trekantdeltaet er reelt og kommer av at den nye kanten ser destinasjonsnoden som felles nabo før gammel kant er fjernet.

## Hva som er numerisk

Følgende er ikke lukket under enkle lokale formler i denne implementasjonen og behandles derfor som regimevariabler:

- `c4`
- `spectral_radius`
- `clustering`
- `dim_proxy`

Disse må evalueres empirisk per kjøring og per regime.

## Perturbasjonslab

Perturbasjonslabben gjør tre ting:

1. bygger to trajektorier fra samme warmup-tilstand,
2. bruker samme semantiske RNG-strøm for begge,
3. setter inn én ekstra lokal regel bare i den ene trajektorien.

Deretter måles forskjellen som:

- antall differensnoder,
- histogram over differensnoder per grafdistanse fra initial support,
- `spread_radius`,
- feature-differanser i redusert basis,
- og løpende estimater `c_star_event` og `c_star_time`.

## Representative filer

- `rule_delta_closed_summary.md`
- `rule_delta_open_summary.md`
- `rule_delta_perturbation_summary.md`
- `rule_delta_closed_events.csv`
- `rule_delta_open_events.csv`
- `rule_delta_perturbation_events.csv`

## Tydelig skille mellom nivåer

### Teorem/identitet

Dette er de algebraiske identitetene og de eksakte lokale deltaformlene.

### Numerisk observasjon

Dette er regimeavhengige tabeller, spredningskurver og målte nullrom i en konkret kjøring.

### Spekulativ fortolkning

Dette er påstander om emergent spacetime, causal cones og energilignende makrovariabler. Slike tolkninger må bygge på flere kjøringer og kryssregime-stabilitet, ikke på én enkelt rapport.
