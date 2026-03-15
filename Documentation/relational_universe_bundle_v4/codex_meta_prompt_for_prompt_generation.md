# Codex meta-prompt: generer gode prompts for kodeassistenter

Kopier teksten under og gi den til Codex når du vil at Codex skal skrive nye, høykvalitets prompts for kodeassistenter som skal arbeide videre med simulatorene.

---

Du skal skrive **prompter for kodeassistenter** som skal arbeide på et forskningsprosjekt om en relasjonell universgraf. Kodeassistentene skal ikke finne på en ny ontologi; de skal arbeide innenfor en spesifisert modell og være matematisk disiplinerte.

## Modellens faste premisser

- Universet modelleres som en dynamisk urettet graf.
- Det finnes bare én node-type og én relasjonstype.
- "Units of action" modelleres teknisk som lokale hendelser eller tokens som bærer hendelser.
- Tid er emergent og representeres operasjonelt gjennom asynkron hendelsesdynamikk.
- Spacetime er emergent, ikke fundamental bakgrunn.
- Partikler tolkes som metastabile klustre eller loops.
- Entanglement tolkes som korrelasjon / felles constraint-struktur, ikke som en superluminal kanal.
- Seeds kan oppstå kontinuerlig, men er operasjonelt relevante bare når de kobles inn i en komponent.
- Matematisk analyse skal bruke feature-vektorer, lokale rewrite-regler, endringsvektorer og invariantanalyse.

## Programvarekontekst

Det finnes to Python-filer:

- `relational_universe_sim.py`
- `relational_universe_sim_energy.py`

Det finnes også dokumentasjon i Markdown som beskriver:

- ontologien,
- energi-kandidater,
- invariantanalysen,
- og ønsket videre refaktorering.

## Hvordan promptene du skriver skal være

Hver prompt du produserer skal:

1. være skrevet for en dyktig kodeassistent,
2. være eksplisitt om mål, ikke bare vag om ønsket retning,
3. skille klart mellom:
   - fysisk tolkning,
   - matematisk definisjon,
   - programmeringsoppgave,
4. bevare modellens ontologiske begrensninger,
5. forby at kodeassistenten smugler inn:
   - bakgrunnsrom,
   - nye relasjonstyper,
   - udokumenterte ekstra partikkeltyper,
   - "quantum magic" uten matematisk representasjon,
6. kreve:
   - type hints,
   - docstrings,
   - reproducerbarhet via seed,
   - enhetstester eller minst verifiserbare invariantsjekker,
   - klar CLI eller README-oppdatering,
7. kreve at assistenten forklarer **hva målingene betyr**, ikke bare hvordan de beregnes.

## Standardstruktur for promptene du lager

Hver prompt skal inneholde disse seksjonene:

1. **Mål**
2. **Eksisterende filer**
3. **Faglige premisser som ikke må brytes**
4. **Konkrete utviklingsoppgaver**
5. **Vitenskapelig betydning**
6. **Akseptansekriterier**
7. **Ikke-mål / hva som ikke skal gjøres**
8. **Format på svaret**

## Tone

- presis,
- teknisk,
- profesjonell,
- uten hype,
- uten å late som om modellen allerede er en etablert fysisk teori.

## Oppgave nå

Skriv en ny prompt for en kodeassistent som skal: **[SETT INN DIN KONKRETE OPPGAVE HER]**

Sørg for at prompten er direkte brukbar uten videre redigering.
