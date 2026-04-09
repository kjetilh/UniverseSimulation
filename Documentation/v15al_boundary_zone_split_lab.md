# Relasjonell universgraf v0.15al: boundary zone split lab

## Formal

Denne runden prover a dele boundary-sonen fra `v15ak` i noen fa senere tidlige-hale profiler, for a se om `mid-high`-entry og vedvarende churn skiller lag bedre der.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Per onset family

| onset family | n | late high-rise | mid plateau | residual | peak high | high last24 | comp72 | switches72 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mid_high_entry_family | 4 | 0.500 | 0.250 | 0.250 | 0.240 | 0.479 | 5.000 | 14.500 |
| persistent_churn_family | 4 | 0.250 | 0.750 | 0.000 | 0.111 | 0.208 | 4.295 | 11.750 |

## Per boundary label

| boundary label | n | high last24 | mid last24 | low last24 | comp72 | largest72 | switches72 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| late_high_rise_boundary | 3 | 0.861 | 0.139 | 0.000 | 5.819 | 0.200 | 17.000 |
| mid_plateau_boundary | 4 | 0.010 | 0.865 | 0.125 | 4.000 | 0.284 | 10.000 |
| residual_boundary | 1 | 0.125 | 0.667 | 0.208 | 3.722 | 0.330 | 14.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er rent separert, og denne runden bygger bare pa ekte `v15ai`, `v15aj` og `v15ak`-data.
- `boundary_split_status`: `boundary_zone_partly_split` fordi Boundary-sonen er ikke ren, men den deler seg i to nyttige grener: `mid-high` havner oftere i late high-rise, mens vedvarende churn oftere blir i en mid-plateau-gren.
- `family_split_note`: `descriptive` fordi `mid_high_entry_family` har late-high-rise-rate 0.500, mens `persistent_churn_family` har mid-plateau-rate 0.750.
- `next_step`: `explain_overlap_cases` fordi Neste steg bor forklare overlap-caseene: ett churn-run som ogsa blir high-rise, og ett mid-high-run som blir mid-plateau.

## Tolkning

- Dette er fortsatt en smal oppfolging av boundary-sonen, ikke en ny bred familie-scan.
- `late_high_rise_boundary` betyr at hoy-band-trykk bygger seg opp tydelig i de forste 72 hale-snapshottene.
- `mid_plateau_boundary` betyr at runet holder seg mest pa et roligere mid-platå uten tydelig high-rise i denne fasen.
