
# README: v0.4 redusert basis og regelbetingede ΔF-matriser

Denne pakken er neste presise steg etter v0.3 feature-lab.

## Hovedidé
Vi går fra generell feature-utforskning til en stram analyse av:

- redusert feature-basis,
- eksakte lineære invariants,
- kontekstbetingede motivendringer,
- og standardiserte regelbetingede ΔF-matriser.

## Viktigste nye filer

- `relational_universe_rule_delta_lab.py`  
  Instrumentert simulator og analyseverktøy for v0.4.

- `relasjonell_universgraf_v0_4_redusert_basis_og_regelbetingede_deltaF.md`  
  Teoretisk og metodologisk dokumentasjon av steget.

- `rule_delta_closed_summary.md`  
  Representative resultater i lukket topologisk sektor.

- `rule_delta_open_summary.md`  
  Representative resultater i åpen topologisk sektor.

## Hovedresultater
1. `edges` og `deg_sq_sum` er fjernet fra basisen fordi de er algebraisk avledbare.
2. I lukket topologisk sektor er `tokens` og `beta1` de ikke-trivielle invariantsene i én fast sammenhengende komponent.
3. I åpen topologisk sektor gjenstår bare `tokens` som eksakt lineær invariant i kjernebasis.
4. Kontekstformler for `wedges`, `triangles` og `star3` er verifisert med null residual i representative kjøringer.

## Anbefalt leserekkefølge
1. Les `relasjonell_universgraf_v0_4_redusert_basis_og_regelbetingede_deltaF.md`
2. Se `rule_delta_closed_summary.md`
3. Se `rule_delta_open_summary.md`
4. Kjør deretter `relational_universe_rule_delta_lab.py` med egne parametre

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

## Viktig metodologisk poeng
Dette steget er laget for å forhindre tre vanlige feil:

- å forveksle grafidentiteter med dynamiske lover,
- å forveksle lineære invariants med generelle energibegreper,
- å forveksle empirisk treghet med eksakt bevaring.

## Naturlig neste steg
Neste riktige steg er en perturbasjonslab for kausal spredning og effektiv propagasjonshastighet.
