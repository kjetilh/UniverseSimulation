# Codex-prompt – v0.8 faseatlas og videreutvikling

Du arbeider i et forskningsprosjekt om en relasjonell universgraf. Prosjektet har nå nådd v0.8 og har følgende kodebase som utgangspunkt:

- `relational_universe_local_max_coupling_lab.py` (v0.7-kjernelab)
- `relational_universe_v08_phase_atlas.py` (v0.8 faseatlas)
- diverse CSV/Markdown-rapporter fra v0.7 og v0.8

## Kontekst
Modellen representerer universet som en dynamisk graf med:
- noder
- én relasjonstype (udirekte kanter)
- stokastiske lokale `units of action`
- ingen bakgrunnsgeometri
- spacetime, partikler og felter tolkes som emergente mønstre

v0.7 etablerte lokal maksimal kobling mellom to nærliggende universgrener.
v0.8 skanner et kandidatrom og rangerer regimer etter fire mål:
1. repair / overlap
2. bounded causal spread
3. quasi-invariants
4. geometry robustness

## Oppgave
Forbedre v0.8 uten å bryte den eksisterende semantikken.

### Krav
1. Bevar de eksisterende parameterne og filformatene så langt det er rimelig.
2. Legg til støtte for bootstrap confidence intervals for aggregate metrics per gridpunkt.
3. Legg til mulighet for finere scan i et lokalt nabolag rundt de beste coarse-punktene.
4. Legg til Pareto-rangering med eksport av frontier til egen CSV.
5. Ikke introduser skjulte globale koordinater eller ikke-lokale regler.
6. Dokumenter endringene i klar Markdown.

### Leveranser
- oppdatert Python-kode
- en kort README
- ett eksempel på kommandoer
- en Markdown-oppsummering av hva endringen metodisk betyr

### Viktig
- vær eksplisitt om hvilke deler som er eksakte og hvilke som er heuristiske
- ikke bland sammen 'geometrirobusthet' med ekte geometri; kall det fortsatt proxy eller robustness
- ikke påstå at en fasegrense er skarp hvis dataene bare støtter en crossover eller et heuristisk regimeskille
