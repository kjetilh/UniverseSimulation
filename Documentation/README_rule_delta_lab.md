
# README: v0.4 regelmotor, redusert basis og perturbasjonslab

Denne pakken er neste presise steg etter v0.3 feature-lab.

## Hovedidé
Vi går fra generell feature-utforskning til en stram analyse av:

- eksplisitte regelobjekter,
- redusert feature-basis,
- eksakte lineære invariants,
- kontekstbetingede motivendringer,
- og standardiserte regelbetingede ΔF-matriser.

## Viktigste nye filer

- `relational_universe_rule_delta_lab.py`  
  Bevarer eksisterende CLI og peker nå på den refaktorerte regelmotoren.

- `relational_universe_perturbation_lab.py`  
  Ny CLI for kopla kjøringer med delt RNG-strøm og lokal perturbasjon.

- `rule_delta_lab/`  
  Modulær implementasjon av grafkjerne, features, regler, analyse og perturbasjon.

- `relasjonell_universgraf_v0_4_redusert_basis_og_regelbetingede_deltaF.md`  
  Teoretisk og metodologisk dokumentasjon av steget.

- `rule_delta_closed_summary.md`  
  Representative resultater i lukket topologisk sektor.

- `rule_delta_open_summary.md`  
  Representative resultater i åpen topologisk sektor.

- `rule_delta_perturbation_summary.md`  
  Representative resultater for kausal spredning i kopla kjøringer.

- `rule_delta_rule_engine_and_perturbation_design.md`  
  Kort teknisk designnotat for refaktoren.

## Hovedresultater
1. `edges` og `deg_sq_sum` er fjernet fra basisen fordi de er algebraisk avledbare.
2. I lukket topologisk sektor er `tokens` og `beta1` de ikke-trivielle invariantsene i én fast sammenhengende komponent.
3. I åpen topologisk sektor gjenstår bare `tokens` som eksakt lineær invariant i kjernebasis.
4. Kontekstformler for `wedges`, `triangles` og `star3` er verifisert med null residual i representative kjøringer.
5. Primitive regler er nå egne objekter med `delta_core(...)`, `delta_motif(...)`, `applies(...)` og `apply(...)`.
6. En ny perturbasjonslab måler spredning i grafdistanse, hendelsestid og redusert feature-vektor under delt RNG-strøm.
7. `swap`-regelen bruker den presise trekantformelen `Δtriangles = -c_del + (c_add - 1)`.

## Anbefalt leserekkefølge
1. Les `relasjonell_universgraf_v0_4_redusert_basis_og_regelbetingede_deltaF.md`
2. Les `rule_delta_rule_engine_and_perturbation_design.md`
3. Se `rule_delta_closed_summary.md`
4. Se `rule_delta_open_summary.md`
5. Se `rule_delta_perturbation_summary.md`
6. Kjør deretter CLI-ene selv

## Eksempelkommandoer

Lukket topologisk sektor:
```bash
python relational_universe_rule_delta_lab.py \
  --closed-topological \
  --steps 6000 \
  --seed 17 \
  --out-csv rule_delta_closed_events.csv \
  --out-md rule_delta_closed_summary.md
```

Åpen topologisk sektor:
```bash
python relational_universe_rule_delta_lab.py \
  --open-topological \
  --steps 4000 \
  --seed 17 \
  --out-csv rule_delta_open_events.csv \
  --out-md rule_delta_open_summary.md
```

Perturbasjonslab:
```bash
python relational_universe_perturbation_lab.py \
  --steps 1000 \
  --warmup-steps 250 \
  --seed 19 \
  --avoid-disconnect \
  --relocate-tokens \
  --out-csv rule_delta_perturbation_events.csv \
  --out-md rule_delta_perturbation_summary.md
```

## Viktig metodologisk poeng
Dette steget er laget for å forhindre tre vanlige feil:

- å forveksle grafidentiteter med dynamiske lover,
- å forveksle lineære invariants med generelle energibegreper,
- å forveksle empirisk treghet med eksakt bevaring,
- og å forveksle divergens mellom to kjøringer med ulik ekstern støy.

## Naturlig neste steg
Neste riktige steg er parameter-sweeps og regimekart for perturbasjonsfront, ikke flere ad hoc-fortolkninger av enkeltruns.
