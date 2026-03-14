# Feature Lab Refactor Design

Dette notatet beskriver refaktoreringen av `relational_universe_feature_lab.py` fra en monolitt til en liten forskningskodebase.

## Mål

Refaktoreringen skiller eksplisitt mellom:
- grafdynamikk
- feature-ekstraksjon
- invariantanalyse
- rapportgenerering

Dette gir renere kode, enklere testing og bedre støtte for analyze-only arbeidsflyt.

## Modulstruktur

Ny pakke:

- `feature_lab/graph_core.py`
- `feature_lab/rules.py`
- `feature_lab/features.py`
- `feature_lab/analysis.py`
- `feature_lab/reporting.py`
- `feature_lab/main.py`

Eksisterende inngangspunkt:

- `relational_universe_feature_lab.py`

Denne filen er nå bare en tynn wrapper rundt `feature_lab.main`.

## Ansvarsdeling

### `graph_core.py`

Inneholder:
- `UGraph`
- `State`
- bootstrap-logikk
- generelle grafhjelpere som `count_components`, `beta1_cycle_rank`, `is_bridge`

Dette er den minst domenespesifikke delen og inneholder ingen analyse- eller rapportlogikk.

### `rules.py`

Inneholder:
- `SimulationParameters`
- eksplisitte regelklasser
- `FeatureLabSimulator`

Regelklassene er:
- `SeedAttachRule`
- `TokenBirthRule`
- `TokenDeathRule`
- `DeleteTraversedEdgeRule`
- `TriadicClosureRule`
- `StrictEdgeSwapRule`

Hver regel har:
- `name`
- `find_matches(...)`
- `apply(state, match, rng)`
- `delta_features(...)`

`delta_features(...)` er implementert som eksakt feature-differanse mellom kopi av tilstanden før og etter regelapplikasjon for valgt feature-set. Dermed trenger vi ikke hardkode symbolsk `ΔF` for alle features for å få en korrekt forskningspipeline.

### `features.py`

Inneholder:
- hele feature-rommet
- redusert basis
- algebraiske identiteter
- deterministisk feature-måling

Viktig valg:
- `beta1` og `deg_sq_sum` er beholdt i full basis
- redusert basis fjerner disse fordi de er algebraisk redundante gitt de øvrige koordinatene

### `analysis.py`

Inneholder:
- CSV-innlasting
- quasi-invariantanalyse
- rå og standardisert SVD
- drift-statistikk
- identitetsresidualer
- strukturerte analyseobjekter (`AnalysisReport`, `SVDResult`, osv.)

### `reporting.py`

Inneholder:
- Markdown-tabeller
- rendring av analyse- og kjøringsrapporter
- analyze-only eksempelnotat

### `main.py`

Inneholder:
- CLI-parser
- `simulate`-modus
- `analyze`-modus
- kobling mellom simulering, analyse og rapportering

## Analyze-only modus

Ny arbeidsflyt:

```bash
python3 relational_universe_feature_lab.py \
  --mode analyze \
  --input-csv Documentation/feature_lab_regimes/open_balanced_regime.csv \
  --summary-md Documentation/feature_lab_examples/analyze_only_open_balanced.md \
  --analysis-mode both \
  --feature-basis reduced
```

Dette lar oss kjøre quasi-invariantanalyse på eksisterende data uten å simulere på nytt.

## Rå vs standardisert analyse

Begge analyser er nå førsteordens borgere i koden:

- `raw`: SVD på rå inkrementer og rå hastigheter
- `standardized`: SVD på z-skalerte features og deres inkrementer/hastigheter
- `both`: begge i samme rapport

Metodisk poeng:
- rå analyse er nyttig når man vil se faktisk størrelse i systemets naturlige koordinater
- standardisert analyse er nødvendig for å avsløre skalaartefakter

## Redusert basis

Redusert basis er implementert som en eksplisitt feature-basis:

- full basis: inkluderer `beta1` og `deg_sq_sum`
- redusert basis: fjerner `beta1` og `deg_sq_sum`

Dette kvotienterer ut:
- redundansen mellom `nodes`, `edges`, `beta1`, `components`
- redundansen mellom `wedges`, `edges`, `deg_sq_sum`

Det er et første, pragmatisk steg. Senere kan man gjøre dette mer formelt som en lineær kvotient av feature-rommet.

## Testbarhet

Det er lagt inn små sanity checks i:

- `tests/test_feature_lab_sanity.py`

Disse sjekker:
- `beta1 = edges - nodes + components`
- `deg_sq_sum = 2*wedges + 2*edges`
- at `StrictEdgeSwapRule` bevarer `edges` eksakt

## Designvalg som bevisst ikke er tatt ennå

- Ingen tunge eksterne avhengigheter er lagt til.
- `numpy` brukes fortsatt bare opportunistisk i analysefasen.
- Reglenes `ΔF` er foreløpig beregnet ved eksakt differanse på tilstandskopier, ikke ved håndkodede symbolformler for hvert feature.

Dette er en god balanse mellom forskningsnøyaktighet og kodeenkelhet i nåværende fase.
