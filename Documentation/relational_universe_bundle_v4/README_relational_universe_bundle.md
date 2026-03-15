# README: Relasjonell universgraf-bundle

Dette er en ren Markdown-pakke som samler:

1. en arbeidsavhandling for modellen,
2. Codex-prompter for videre utvikling,
3. de to simulatorene som allerede er laget.

## Filer

- `relasjonell_universgraf_avhandling.md`  
  Hoveddokumentet. Inneholder hele modellskissen så langt, energi- og invariantanalysen, simulatorfortolkning og ordliste.

- `codex_meta_prompt_for_prompt_generation.md`  
  En meta-prompt du kan gi Codex når du vil at Codex selv skal skrive gode prompts for andre kodeassistenter.

- `codex_prompt_simulator_bruk_og_tolkning.md`  
  En direkte prompt for å få en kodeassistent til å bruke simulatorene faglig riktig og forklare hva målingene betyr.

- `codex_prompt_refaktorering_rule_engine.md`  
  En direkte prompt for refaktorering av simulatorene til en regelmotor med eksplisitte feature-deltaer og invariantanalyse.

- `codex_prompt_invariantanalyse.md`  
  Ekstra prompt for å få Codex til å implementere nullroms-/stoikiometri-analysen matematisk og programmessig.

- `relational_universe_sim.py`  
  Minimal simulator.

- `relational_universe_sim_energy.py`  
  Simulator med energi- og kontinuitetsdiagnostikk.

## Anbefalt leserekkefølge

1. `relasjonell_universgraf_avhandling.md`
2. `codex_prompt_simulator_bruk_og_tolkning.md`
3. `codex_prompt_refaktorering_rule_engine.md`

## Rask start

### Lukket topologisk test
```bash
python relational_universe_sim_energy.py \
  --closed \
  --check-exact \
  --w-tokens 1 \
  --w-beta1 1 \
  --w-stress 0 \
  --out closed_energy.csv
```

### Åpent metastabilt regime
```bash
python relational_universe_sim_energy.py \
  --steps 200000 \
  --p-triad 0.10 \
  --p-del 0.10 \
  --w-tokens 1 \
  --w-beta1 1 \
  --w-stress 0 \
  --out open_energy.csv
```

### Lokal kontinuitetstest
```bash
python relational_universe_sim_energy.py \
  --steps 50000 \
  --local-radius 3 \
  --out local_tokens.csv
```

## Hva du leter etter

- **Eksakt invariant:** en størrelse som ikke endres event-for-event i et lukket regime.
- **Quasi-invariant:** liten drift i åpne, metastabile regimer.
- **Metastabil struktur:** store komponenter, loop-rikdom, moderat clustering, lav eller kontrollert drift.
- **Dårlig regelklasse:** regler som sprenger opp komponenten, skaper ukontrollert drift eller ødelegger alle enkle invariants.

## Viktig metodisk poeng

Målet er ikke å "bevise" vår fysikk direkte. Målet er å finne ut hvilke mikroskopiske rewrite-klasser som i det hele tatt er kompatible med:

- robust struktur,
- energilignende bevaring,
- emergent geometri,
- og senere kanskje relativistiske eller feltlignende makrolover.
