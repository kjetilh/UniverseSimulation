# Codex-prompt – v0.8b med p_del-akse og finere lokal scan

Utvid v0.8-faseatlaset med en liten `p_del`-akse og en lokal refinementsløyfe.

## Oppgave
1. Start fra dagens coarse-vinnere i `relational_universe_v08_phase_atlas.py`.
2. Definer en lokal scan der:
   - `p_del ∈ {0.00, 0.01, 0.02}`
   - `p_triad` finjusteres i små steg rundt v0.8-vinnerne
   - `p_swap` finjusteres i små steg rundt v0.8-vinnerne
   - `r_birth` og `r_death` finjusteres i små steg rundt v0.8-vinnerne
3. Hold fortsatt `local_coupling = maximal`.
4. Rapporter om de lovende regimene er robuste når slettingsakse åpnes litt.

## Krav
- skill eksplisitt mellom coarse og local refinement
- legg inn enkel caching slik at tidligere kjørte gridpunkter ikke regnes om unødvendig
- eksporter både run-level og aggregate CSV
- skriv en Markdown-rapport som sier tydelig om v0.8-kandidatene overlever når `p_del` åpnes, eller om de kollapser
