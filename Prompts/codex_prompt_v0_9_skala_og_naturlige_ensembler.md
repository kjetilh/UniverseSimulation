# Codex-prompt: utvid v0.8b med større naturlige ensembler og skalaanalyse

Du jobber videre på prosjektet "relasjonell universgraf". Les først følgende filer i repoet / arbeidsmappen:

- `relational_universe_local_max_coupling_lab.py`
- `relational_universe_v08_phase_atlas.py`
- `relational_universe_v08b_natural_ensemble_robustness.py`
- `relasjonell_universgraf_v0_8_faseatlas_og_regimevalg.md`
- `relasjonell_universgraf_v0_8b_naturlige_ensembler_og_bootstrap.md`

## Oppgave

Bygg v0.9 som en skala- og ensembleutvidelse av v0.8b.

### Mål
1. Utvid naturlige startensembler til større størrelser, for eksempel mål rundt 64, 96 og 128 noder.
2. Innfør minst to forskjellige burn-in-regimer for å teste om kandidatbåndet er robust mot hvordan de naturlige starttilstandene blir generert.
3. Mål hvordan disse størrelsene påvirker:
   - local overlap
   - final radius
   - edge difference count
   - beta1-drift
   - spectral radius-drift
4. Lag bootstrap- eller jackknife-intervaller for skaleringsmålene.
5. Produser:
   - ny Python-kode
   - CSV-filer
   - en teknisk `.md`-rapport
   - en lay `.md`-forklaring

### Krav
- Ikke bryt kompatibilitet med eksisterende run-level kolonnenavn hvis du kan unngå det.
- Hold all dokumentasjon i Markdown.
- Vær eksplisitt på hvilke resultater som er rå observasjoner og hvilke som er fortolkninger.
- Unngå å introdusere "magiske" samlescorer uten forklaring; hvis du lager nye scorer, dokumenter formelen tydelig.
- Kommenter kode nøkternt og presist.
