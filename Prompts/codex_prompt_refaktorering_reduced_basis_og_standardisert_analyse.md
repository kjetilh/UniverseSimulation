
# Codex-prompt: refaktorer feature-labben til et forskningsverktøy

Du skal refaktorere `relational_universe_feature_lab.py` til en renere forskningskodebase.

## Mål
Lag en struktur som skiller mellom:
1. grafdynamikk,
2. feature-ekstraksjon,
3. invariantanalyse,
4. rapportgenerering.

## Krav til refaktorering

### A. Del opp i moduler
Foreslå og implementer en modulstruktur omtrent slik:
- `graph_core.py`
- `rules.py`
- `features.py`
- `analysis.py`
- `reporting.py`
- `main.py`

### B. Regelobjekter
Hver regel skal være et objekt eller en klasse med:
- navn,
- lokal matching-logikk,
- `apply(state)`-metode,
- og en metode som returnerer estimerte eller eksakte `ΔF` for et valgt feature-set.

### C. Analyze-only modus
Legg til støtte for å:
- lese en eksisterende CSV,
- kjøre quasi-invariantanalyse uten ny simulering,
- skrive en Markdown-rapport.

### D. Standardisert analyse
Utvid analysen slik at den kan kjøres i minst to modi:
- rå inkrementer,
- z-skalerte eller annen standardisert inkrementanalyse.

Rapporten skal forklare forskjellen.

### E. Redusert basis
Implementer eksplisitt støtte for et redusert feature-rom der trivielle identiteter kan kvotienteres ut, for eksempel:
- fjern redundansen mellom `(nodes, edges, beta1, components)`,
- fjern redundansen mellom `(wedges, edges, deg_sq_sum)`.

### F. Testbarhet
Lag små enhetstester eller sanity checks for:
- `beta1 = edges - nodes + components`,
- `deg_sq_sum = 2*wedges + 2*edges`,
- og for at `strict edge-swap` faktisk bevarer `edges` eksakt.

## Stil
- Skriv ryddig Python med type hints.
- Bruk docstrings.
- Ikke innfør tunge avhengigheter uten god grunn.
- All dokumentasjon skal være i Markdown.

## Leveranser
- refaktorert kode,
- en kort teknisk designrapport i Markdown,
- et eksempel på analyze-only kjøring,
- og en kort note om hvilke deler som er rent algebraiske, og hvilke som er dynamiske.
