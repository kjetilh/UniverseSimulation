# v0.15al operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsen er rent separert, og denne runden bygger bare pa ekte `v15ai`, `v15aj` og `v15ak`-data.
- `boundary_split_status`: `boundary_zone_partly_split` fordi Boundary-sonen er ikke ren, men den deler seg i to nyttige grener: `mid-high` havner oftere i late high-rise, mens vedvarende churn oftere blir i en mid-plateau-gren.
- `family_split_note`: `descriptive` fordi `mid_high_entry_family` har late-high-rise-rate 0.500, mens `persistent_churn_family` har mid-plateau-rate 0.750.
- `next_step`: `explain_overlap_cases` fordi Neste steg bor forklare overlap-caseene: ett churn-run som ogsa blir high-rise, og ett mid-high-run som blir mid-plateau.

- Les denne runden som en smal splitting av boundary-sonen fra `v15ak`, ikke som nye defect-arter.
