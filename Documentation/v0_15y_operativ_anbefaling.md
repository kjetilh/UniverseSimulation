# v0.15y operativ anbefaling

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert i denne case-runden.
- `case_snapshot`: `p1_clean=1;tradeoff=1;p0_clean=1;mixed=0` fordi Dette oppsummerer de tre utvalgte seed-casene etter onset-metrikkene.
- `case_family_status`: `three_case_family_supported` fordi De tre valgte seed-casene holder faktisk som tre ulike lokale case-typer: p1-clean, tradeoff og p0-clean.
- `next_step`: `explain_case_triggers` fordi Neste steg bør forklare hva som utløser hvert case, ikke samle flere aggregate-runder.

- Les denne runden som en case-duel-runde på tre seed-caser, ikke som bredere lokal scanning.
