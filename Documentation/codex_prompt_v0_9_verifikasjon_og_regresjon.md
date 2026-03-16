# Codex-prompt: verifikasjon og regresjonstester for v0.9

Du skal styrke påliteligheten i v0.9-koden.

Oppgaver:
1. legg inn regresjonstester for at `compute_steps_for_state` er monotont stigende i `N` innenfor klammegrensene,
2. test at bootstrap-rutinene ikke krasjer når én metric er konstant,
3. test at burn-in-sensitivitet beregnes riktig på syntetiske group-rows,
4. test at radius_alpha blir ~0 når radius er konstant på tvers av størrelser,
5. test at radius_alpha blir ~1 når radius er proporsjonal med N.

Krav:
- skriv testene i en egen Python-fil,
- legg ved kort markdown-notat om hva som ble testet og hvorfor det er viktig.
