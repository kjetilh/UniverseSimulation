# UniverseSimulation

UniverseSimulation er et arbeidsrepo for a teste hypoteser om et bakgrunnslost, relasjonelt univers der:

- noder og en relasjonstype er de primitive byggesteinene
- lokale stokastiske rewrite-hendelser er "units of action"
- tid, romtid, partikler og bevaringslover skal forklares som emergente storrelser

Det som finnes i repoet na:

- `Documentation/grundig-research-rapport-16.md`: den matematiske og konseptuelle hovedrapporten
- `relational_universe_sim.py`: en kjørbar toy-simulator som approximerer deler av rammeverket med en dynamisk urettet graf
- `trajectory.csv`: en eksisterende baseline-kjoring fra simulatoren
- `rag_service/`: en prosjektspesifikk RAG-tjeneste for statusdokumentasjon, argumentasjon, verktøybruk og promptprofiler

## Kjor simulatoren

```bash
python3 relational_universe_sim.py --steps 2000 --log-every 500 --out ''
```

For flere parametre:

```bash
python3 relational_universe_sim.py --help
```

## Hva RAG-en er til for

`rag_service/` er laget for a gi språkmodeller og research-klienter et bedre faktagrunnlag om:

- hvor prosjektet faktisk er na
- hva forskningsrapporten hevder
- hvordan dagens verktøy brukes
- hvilke antagelser, argumenter og testprogram prosjektet bygger pa

Se `rag_service/docs/README.md` for oversikt.
