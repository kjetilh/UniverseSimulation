# Codex-prompt: bruk og tolkning av simulatorene

Kopier teksten under og gi den til Codex eller en annen kodeassistent.

---

Du skal arbeide videre på et forskningsprosjekt om en relasjonell universgraf. Prosjektet er spekulativt, men skal behandles med matematisk og programmatisk disiplin.

## Mål

Bruk de eksisterende simulatorene til å:

1. forklare presist hva de modellerer,
2. forklare hva hver sentrale observabel betyr fysisk og matematisk,
3. lage en praktisk arbeidsflyt for parameterstudier,
4. identifisere hvilke regimer som ser:
   - stabile,
   - metastabile,
   - driftende,
   - eller degenererende ut,
5. foreslå små, kontrollerte utvidelser som **ikke** bryter modellens grunnpremisser.

## Eksisterende filer

- `relational_universe_sim.py`
- `relational_universe_sim_energy.py`
- `relasjonell_universgraf_avhandling.md`

## Faglige premisser som ikke må brytes

- Grafen har én node-type og én relasjonstype.
- Du skal ikke innføre et bakgrunnsrom.
- Du skal ikke innføre nye felt eller partikler som ekstra primitiver.
- Spacetime skal forstås som emergent makrostruktur.
- Entanglement skal behandles som korrelasjon / constraint, ikke som fri signaleringskanal.
- Energi skal behandles som en tilstandsfunksjonal eller invariant-kandidat, ikke bare som rå hendelsesrate.
- Feature-settet \((K,N,M,C,\beta_1)\) er den første analysen, ikke den endelige sannheten.

## Konkrete utviklingsoppgaver

1. Les begge simulatorene og skriv en strukturert teknisk forklaring av:
   - state,
   - eventtyper,
   - scheduler,
   - målefunksjoner,
   - energifunksjonaler,
   - kontinuitetsdiagnostikk.

2. Lag en kort README-seksjon med anbefalte eksperimenter:
   - lukket topologisk test,
   - åpent metastabilt regime,
   - lokal kontinuitetstest.

3. Implementer eller foreslå et enkelt analyseverktøy som:
   - leser CSV-utdata,
   - plotter \(E(t)\), \(\beta_1(t)\), \(K(t)\), \(N(t)\), \(M(t)\),
   - estimerer drift,
   - markerer perioder med metastabilitet.

4. Forklar presist hva følgende observabler betyr:
   - `beta1`
   - `E_tokens`
   - `E_total`
   - `clustering`
   - `eff_dim`
   - `region_residual`

5. Beskriv hvilke utfall som ville telle som:
   - tegn på stabilitetslag,
   - tegn på quasi-konservering,
   - tegn på at regelklassen er fysisk lite lovende.

6. Foreslå 3 små, lokale modifikasjoner av reglene som kan testes uten å forlate ontologien.

## Vitenskapelig betydning

Oppgaven handler ikke bare om kode. Den handler om å gjøre det mulig å avgjøre hvilke mikroskopiske rewrite-klasser som kan støtte:

- store stabile komponenter,
- loop-bårne invariants,
- lokal kontinuitet,
- og senere kanskje et emergent spacetime-regime.

## Akseptansekriterier

Svaret ditt må inneholde:

- en konsis, men presis systemforklaring,
- en tabell over observabler og deres tolkning,
- konkrete kommandoeksempler,
- en plan for parameter sweep,
- minst ett forslag til analysekode eller analysemodul,
- eksplisitt advarsel mot overtolkning.

## Ikke-mål

- Ikke presenter modellen som etablert fysikk.
- Ikke introduser nye primitive objekter uten å begrunne det.
- Ikke bruk ord som "kvante", "gravitasjon" eller "felt" som pynt uten å knytte dem til konkrete observabler eller regler.

## Format på svaret

Svar i følgende struktur:

1. Oversikt
2. Hva simulatorene faktisk gjør
3. Hvordan kjøre meningsfulle eksperimenter
4. Hvordan lese utdata
5. Forslag til forbedringer
6. Risikoer og feiltolkninger
