
# Codex-prompt: v0.4 rule-delta-lab og videre utvidelse

Du arbeider i et forskningsprosjekt om en relasjonell universgraf. 
Eksisterende filer inkluderer:

- `relational_universe_sim.py`
- `relational_universe_sim_energy.py`
- `relational_universe_feature_lab.py`
- `relational_universe_rule_delta_lab.py`

## Kontekst
Prosjektet modellerer universet som en dynamisk graf med:
- noder,
- én relasjonstype,
- lokale stokastiske units of action,
- emergent spacetime som makroregime,
- partikkel-/feltlignende strukturer som stabile eller metastabile mønstre.

I v0.4 er følgende allerede etablert:
- redusert feature-basis,
- kjernebasis `F_core = (tokens, nodes, components, beta1)`,
- symbolsk invariantklassifikasjon via nullrom,
- kontekstbetingede eksakte formler for `wedges`, `triangles` og `star3`,
- empiriske standardiserte regelbetingede ΔF-matriser.

## Oppgave
Utvid kodebasen på en forskningsmessig ryddig måte.

### Del A: refaktorering
1. Innfør en eksplisitt `Rule`-abstraksjon.
2. Hver regel skal kunne rapportere:
   - `delta_core(context)`
   - `delta_motif(context)`
   - `applies(state, context)`
   - `apply(state, rng)`
3. Skill klart mellom:
   - grafidentiteter,
   - eksakte lineære invariants,
   - og empiriske regimevariabler.

### Del B: perturbasjonslab
Bygg et nytt verktøy som:
1. kjører to kopla simuleringer med identisk RNG-strøm,
2. introduserer én lokal perturbasjon i bare én av dem,
3. måler forskjellen som funksjon av:
   - grafdistanse,
   - hendelsestid,
   - og endring i redusert feature-vektor,
4. estimerer en effektiv propagasjonsfront / causal cone.

### Del C: analyse
Produser Markdown-filer som dokumenterer:
- metode,
- eksakte antagelser,
- representative kjøringer,
- tolkning av resultatene,
- og hva som fortsatt er åpent.

## Strenge krav
- Ikke ødelegg eksisterende CLI-er.
- Ikke innfør nye ontologiske primitiver uten å dokumentere hvorfor.
- Bruk bare lokale regler; ingen skjult global geometri.
- Skriv lesbar, testbar Python.
- Lag minst én enkel enhetstest for hver ny analytisk deltaformel.
- Når du dokumenterer, skill tydelig mellom:
  - teorem/identitet,
  - numerisk observasjon,
  - og spekulativ fortolkning.

## Suksesskriterium
Resultatet skal gjøre det mulig å gå videre fra invariantanalyse til en presis studie av lokal kausal spredning i universgrafen.
