# Relasjonell universgraf v0.15y: p0-vs-p1 case duel lab

## Formål

Denne runden tester om de tre mest informative p0/p1-seedene faktisk holder som tre ulike lokale case-typer.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Case aggregate

| case | n | rate | exact gap | first gap | component gap | largest gap | adjacent-jaccard gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| p0_clean_case | 1 | 0.333 | -0.240 | 24.0 | 0.250 | -0.024 | nan |
| p1_clean_case | 1 | 0.333 | 0.101 | -40.0 | 0.000 | 0.000 | 0.022 |
| tradeoff_case | 1 | 0.333 | -0.147 | -16.0 | 1.000 | -0.023 | 0.012 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert i denne case-runden.
- `case_snapshot`: `p1_clean=1;tradeoff=1;p0_clean=1;mixed=0` fordi Dette oppsummerer de tre utvalgte seed-casene etter onset-metrikkene.
- `case_family_status`: `three_case_family_supported` fordi De tre valgte seed-casene holder faktisk som tre ulike lokale case-typer: p1-clean, tradeoff og p0-clean.
- `next_step`: `explain_case_triggers` fordi Neste steg bør forklare hva som utløser hvert case, ikke samle flere aggregate-runder.

## Tolkning

- Dette er en ren case-duel-runde på tre utvalgte seeds, ikke en ny sweep.
- Les dette som lokal case-typologi, ikke som generell defect-lov.
