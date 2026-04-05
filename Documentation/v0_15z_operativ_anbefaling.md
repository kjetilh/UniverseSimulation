# v0.15z operativ anbefaling

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle p0/p1-runene matcher ønsket add_chord-perturbasjon.
- `support_bias`: `p1_denser_support__p0_wider_expansion` fordi P1 sitter i litt tettere lokal støtte, mens p0 har litt større relativ videre ekspansjon. Dette er bakgrunnsbias, ikke hele forklaringen.
- `trigger_snapshot`: `p1_compact=1;tradeoff=1;p0_calm=1;mixed=0` fordi Dette oppsummerer hvordan de tre case-seedene brytes ned i onset-trigger-typer.
- `case_trigger_status`: `three_local_triggers_supported` fordi De tre utvalgte case-seedene kan forklares av tre ulike onset-triggere: kompakt p1-lock, fragmentert tradeoff og rolig p0-singleton-lock.
- `next_step`: `targeted_trigger_holdout` fordi Neste steg bør teste om disse triggerne holder på noen få nærliggende holdout-seeds, ikke åpne en ny bred scan.

- Les denne runden som en forklaring av tre lokale case-seeds, ikke som bred trigger-validering.
