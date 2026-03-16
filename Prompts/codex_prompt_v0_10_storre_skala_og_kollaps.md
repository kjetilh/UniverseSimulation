# Codex-prompt: v0.10 større skala og skaleringskollaps

Du jobber på prosjektet "relasjonell universgraf". Bruk eksisterende filer i arbeidsmappen, særlig:

- `relational_universe_v09b_asymptotic_refinement.py`
- `relational_universe_v09_scale_and_natural_ensembles.py`
- `relational_universe_v08b_natural_ensemble_robustness.py`
- `relational_universe_local_max_coupling_lab.py`

## Oppgave

Bygg v0.10 som en større og strengere asymptotikk-test.

## Mål

1. Utvid naturlige ensembler til minst ett høyere størrelsesnivå enn v0.9b, for eksempel 256 og gjerne 384 hvis runtime tillater det.
2. Gi toppkandidatene flere growth seeds enn v0.9b.
3. Implementer eksplisitte skaleringsdiagnostikker:
   - data collapse-forsøk for radius/front,
   - bedre modellvalg mellom log, sqrt, og power-law,
   - usikkerhet på lokale eksponenter.
4. Skill tydelig mellom:
   - pre-asymptotiske transiente mønstre,
   - og mer stabile storskala-regimer.
5. Bevar hele prosjektets dokumentasjonsstil:
   - markdown-dokumenter,
   - csv-utdata,
   - en ikke-spesialist-forklaring,
   - en ny bundle-zip.

## Viktig

- Ikke omskriv ontologien. Hold deg til samme modellfamilie.
- Ikke lag nye primitive objekter.
- Ikke “fiks” resultatene. Hvis den nåværende toppkandidaten svekkes, dokumenter det ærlig.
- Lag kode som er enkel å kjøre fra kommandolinje.
- Skriv korte kommentarer i kode der de faktisk hjelper.
- Legg inn regresjonstester eller sanity-checks der det er rimelig.

## Ønskede artefakter

- `relational_universe_v10_*.py`
- `relasjonell_universgraf_v0_10_*.md`
- `prosjektoversikt_v0_10.md`
- `relasjonell_universgraf_for_ikke_spesialister_v0_10.md`
- `ordliste_v0_10.md`
- relevante csv-filer
- ny `README_*.md`
- ny bundle-zip
