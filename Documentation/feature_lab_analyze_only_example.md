# Feature Lab Analyze-only Example

Dette er et konkret eksempel på analyze-only bruk av den refaktorerte feature-labben.

## Kommando

```bash
python3 relational_universe_feature_lab.py \
  --mode analyze \
  --input-csv Documentation/feature_lab_regimes/open_balanced_regime.csv \
  --summary-md Documentation/feature_lab_examples/analyze_only_open_balanced.md \
  --analysis-mode both \
  --feature-basis reduced
```

## Hva den gjør

- leser en eksisterende trajectory-CSV
- kjører quasi-invariantanalyse uten ny simulering
- skriver en Markdown-rapport

## Generert rapport

- `Documentation/feature_lab_examples/analyze_only_open_balanced.md`

Denne modusen er nyttig når man:
- vil sammenligne rå og standardisert analyse på samme datasett
- vil teste ulike feature-baser uten å generere nye kjøringer
- eller vil la ChatGPT/Codex analysere allerede eksisterende regimesett
