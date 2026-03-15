# Codex-prompt – bruk og utvidelse av perturbasjonslaben

Du skal arbeide på filen `relational_universe_perturbation_lab.py`.

## Mål
Utvid og bruk simulatoren som et forskningsverktøy for å studere:
1. kausal spredning av lokale perturbasjoner,
2. forskjellen mellom lukket og åpen topologisk sektor,
3. forskjellen mellom invariant-bevarende og charge-injiserende perturbasjoner.

## Viktige metodiske krav
- Behold den strengt lokale regelklassen som standard.
- Ikke gjeninnfør globale bridge-tester i standardløpet.
- Behold shared-noise-koblingen mellom replikaene i token-lukkede regimer.
- Gjør all ny analyse reproduserbar fra kommandolinjen.

## Deloppgaver
1. Legg til batch-modus:
   - flere seeds
   - flere perturbasjonstyper
   - flere regimer
   - samlet CSV og samlet markdown-oppsummering

2. Legg til plotting:
   - radius_control vs tid
   - radius_control vs steg
   - edge_diff_count vs tid
   - regime_L1 vs tid

3. Legg til flere skade-mål:
   - Jaccard-avstand mellom kantmengdene
   - første-treff-kurver per radius
   - empirisk front-envelope

4. Lag en egen analysefunksjon som sammenlikner:
   - `local_swap`
   - `add_chord`
   med identiske øvrige parametre

5. Skriv ut en kort tolkning på slutten av hver batch:
   - er spredningen mest ballistisk,
   - mest lokal scrambling,
   - eller blandet?

## Leveranser
- oppdatert python-kode
- én README i markdown
- ett eksempel på batch-kjøring
- ett eksempel på tolkning av resultatene
