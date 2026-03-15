
# Codex-prompt: bruk feature-labben til å teste quasi-invarianter

Du skal arbeide på et lite forskningsprosjekt om en relasjonell universmodell der:
- universet er en dynamisk graf,
- det finnes bare én relasjonstype,
- lokale “units of action” er stokastiske rewrite-hendelser,
- spacetime og partikkel-lignende strukturer er emergente makromønstre.

Bruk filen `relational_universe_feature_lab.py` som hovedinstrument.

## Oppgave
1. Les koden og identifiser:
   - hvilke regler som faktisk implementeres,
   - hvilke features som måles,
   - hvilke algebraiske identiteter som alltid gjelder.
2. Skriv en kort teknisk forklaring i Markdown av hva hver feature betyr fysisk.
3. Kjør minst tre regimer:
   - lukket topologisk sektor,
   - åpent balansert regime,
   - et mer aggressivt regime med høyere triadic closure og delete.
4. For hvert regime:
   - lagre CSV,
   - generer Markdown-oppsummering,
   - identifiser eksakte invariants,
   - identifiser kandidater til quasi-invariants,
   - skill eksplisitt mellom algebraiske identiteter og dynamiske resultater.
5. Gi en avsluttende vurdering:
   - hvilke features ser ut til å være “spacetime-lignende”,
   - hvilke ser ut til å være “eksitasjons-/energilignende”,
   - og hvilke bare er redundante beskrivelser av samme struktur.

## Viktige krav
- Ikke kall noe en bevaringslov før du har sjekket om det bare følger av definisjonene.
- Vær eksplisitt om skalaeffekter i SVD-analysen.
- Kjør både rå og standardisert analyse dersom du utvider koden.
- Dokumenter alle funn i Markdown, ikke i løse kommentarer.

## Leveranser
- oppdatert Markdown-notat,
- eventuelle CSV-filer,
- og konkrete forslag til hvilke features som bør inngå i et redusert basisrom.
