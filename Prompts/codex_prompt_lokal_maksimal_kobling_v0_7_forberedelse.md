# Codex-prompt: forbered v0.7 med mer lokal maksimal kobling

Du skal refaktorere `relational_universe_uniformized_coupling_lab.py` for å forberede v0.7.

## Mål
Forbedre koblingen innen hver event-familie slik at den ikke bare er familywise korrekt, men også mer lokalt maksimal eller nær-maksimal.

## Krav
1. Behold den overordnede familywise uniformization-konstruksjonen.
2. For hver familie (`seed`, `token`, `birth`, `death`), isoler lokale overgangskjerner.
3. Implementer eller skisser en bedre coupling for:
   - vektet valg av token
   - valg av nabo
   - valg av kandidat ved triad/swap
4. Logg nye mål på coupling-kvalitet:
   - probability of exact local match
   - divergence source by family
   - shared-ID retention rate
5. Skriv all dokumentasjon i Markdown.

## Viktig analyse
Skill mellom:
- maksimal kobling av Bernoulli-aksept
- maksimal kobling av kategoriske valg
- full maksimal kobling av hele lokale overgangskjernen

Du må eksplisitt si hva som er oppnådd og hva som fortsatt er heuristisk.

## Leveranse
- refaktorert Python-kode
- Markdown-notat som forklarer algoritmen
- testkjøringer som sammenligner gammel og ny coupling
