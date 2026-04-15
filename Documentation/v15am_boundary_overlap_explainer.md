# Relasjonell universgraf v0.15am: boundary overlap explainer

## Formal

Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter og ekte `v15al`-boundary-labels for a forklare de tre overlap-caseene som ble igjen mellom late high-rise og mid-platå.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Reference profiles

| role | seed | placement | first high>=3 | last12 high | last12 mid | longest high | longest mid | peak comp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| typical_late_high_rise | 5002205 | 2 | 35.0 | 1.000 | 0.000 | 31.0 | 5.0 | 10.0 |
| typical_late_high_rise | 5002241 | 2 | 42.0 | 0.917 | 0.083 | 11.0 | 13.0 | 8.0 |
| typical_mid_plateau | 5002272 | 1 | 72.0 | 0.000 | 0.667 | 0.0 | 10.0 | 5.0 |
| typical_mid_plateau | 5002273 | 2 | 72.0 | 0.000 | 1.000 | 1.0 | 30.0 | 7.0 |
| typical_mid_plateau | 5002307 | 0 | 72.0 | 0.000 | 1.000 | 0.0 | 22.0 | 5.0 |

## Overlap cases

| seed | onset family | boundary label | nearest | d high | d plateau | margin | explanation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5002161 | persistent_churn_family | late_high_rise_boundary | typical_late_high_rise | 0.100 | 0.690 | 0.591 | churn_to_high_rise_crossover |
| 5002220 | mid_high_entry_family | residual_boundary | typical_mid_plateau | 0.498 | 0.258 | 0.240 | residual_tilt_to_mid_plateau |
| 5002240 | mid_high_entry_family | mid_plateau_boundary | typical_mid_plateau | 0.592 | 0.192 | 0.400 | suppressed_high_rise_plateau |

## Overlap aggregate

| explanation | n | rate | mean first high>=3 | mean last12 high | mean last12 mid | mean margin |
| --- | --- | --- | --- | --- | --- | --- |
| churn_to_high_rise_crossover | 1 | 0.333 | 40.0 | 0.833 | 0.167 | 0.591 |
| residual_tilt_to_mid_plateau | 1 | 0.333 | 69.0 | 0.250 | 0.750 | 0.240 |
| suppressed_high_rise_plateau | 1 | 0.333 | 72.0 | 0.000 | 1.000 | 0.400 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er fortsatt rent separert; denne runden bruker bare ekte v15ai- og v15al-data.
- `overlap_explainer_status`: `overlap_cases_still_partly_mixed` fordi Overlap-caseene er mer lesbare enn i v15al, men kollapser ikke til et lite lokalt forklaringssett ennå.
- `next_step`: `change_overlap_observable` fordi Neste steg bor bytte observabel inne i overlap-sonen, ikke presse denne forklaringen hardere.

## Tolkning

- Dette er fortsatt en liten forklaringsrunde inne i boundary-sonen, ikke en ny scan.
- Les forklaringene som lokale overgangstyper, ikke som nye defect-arter eller lokale lover.
- Hvis overlap-caseene er lokalt forklarbare, betyr det at `v15al` sin rest-ambiguitet er mer strukturert enn bare blandet stoy.
