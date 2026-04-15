# Relasjonell universgraf v0.15an: boundary high-hold lab

## Formal

Denne runden kjorer ingen nye simuleringer. Den bruker ekte `v15ai`-snapshotter og det fokuserte run-settet fra `v15am` for a lese overlap-sonen gjennom hvor stabilt high-band holder etter forste opptreden.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Reference high-hold profiles

| role | seed | start idx | span | hold rate | relapses | regains | last12 high | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| typical_late_high_rise | 5002205 | 35 | 37 | 0.973 | 1 | 1 | 1.000 | stable_high_hold_reference |
| typical_late_high_rise | 5002241 | 42 | 30 | 0.733 | 3 | 3 | 0.917 | rebounding_high_hold_reference |
| typical_mid_plateau | 5002272 | 72 | 0 | 0.000 | 0 | 0 | 0.000 | no_high_hold_reference |
| typical_mid_plateau | 5002273 | 72 | 0 | 0.000 | 0 | 0 | 0.000 | no_high_hold_reference |
| typical_mid_plateau | 5002307 | 72 | 0 | 0.000 | 0 | 0 | 0.000 | no_high_hold_reference |

## Overlap high-hold cases

| seed | prior explanation | start idx | span | hold rate | relapses | regains | last12 high | high-hold label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5002161 | churn_to_high_rise_crossover | 40 | 32 | 0.875 | 3 | 3 | 0.833 | delayed_high_hold_crossover |
| 5002220 | residual_tilt_to_mid_plateau | 69 | 3 | 1.000 | 0 | 0 | 0.250 | late_terminal_high_probe |
| 5002240 | suppressed_high_rise_plateau | 72 | 0 | 0.000 | 0 | 0 | 0.000 | no_high_hold_plateau |

## Overlap aggregate

| label | n | rate | mean start idx | mean span | mean hold rate | mean relapses |
| --- | --- | --- | --- | --- | --- | --- |
| delayed_high_hold_crossover | 1 | 0.333 | 40.0 | 32.0 | 0.875 | 3.000 |
| late_terminal_high_probe | 1 | 0.333 | 69.0 | 3.0 | 1.000 | 0.000 |
| no_high_hold_plateau | 1 | 0.333 | 72.0 | 0.0 | 0.000 | 0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er fortsatt rent separert; denne runden bruker bare ekte v15ai- og v15am-data.
- `high_hold_status`: `high_hold_observable_sharpens_overlap_zone` fordi Overlap-sonen blir skarpere lest av high-hold-observabelen: ett lop faar reell sen high-hold, ett blir igjen uten high-hold, og residual-caset reduseres til en sen terminal high-probe.
- `next_step`: `probe_terminal_probe_boundary` fordi Neste steg bor teste hva som skiller ekte sen high-hold fra bare terminal high-probe, ikke presse generell overlap-forklaring videre.

## Tolkning

- Dette er fortsatt en liten overlap-runde, ikke en ny scan.
- Les high-hold-labelene som en observabel for haleatferd, ikke som nye defect-arter.
- Hvis denne observabelen virker, betyr det at overlap-sonen best forklares av forskjellen mellom ekte sen high-hold og sen, men bare terminal, high-opptreden.
