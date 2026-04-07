# Relasjonell universgraf v0.15ab: add_chord cycle lag lab

## Formål

Denne runden spør om det lokale add_chord-cycle-båndet ser periodisk ut med en stabil return-lag, eller om høy retur-rate kommer fra bred multi-lag-retur.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Lag summary

| placement | n | cyclic rate | stable single lag | few lag | diffuse lag | mean exact | mean dominant share | mean dominant lag |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6 | 1.000 | 0.000 | 0.000 | 1.000 | 0.859 | 0.111 | 40.0 |
| 1 | 6 | 1.000 | 0.000 | 0.000 | 1.000 | 0.846 | 0.106 | 40.0 |
| 2 | 6 | 1.000 | 0.000 | 0.000 | 1.000 | 0.752 | 0.147 | 45.3 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle smale cycle-lag-profiler matcher ønsket add_chord-perturbasjon.
- `lag_cycle_status`: `cycle_band_is_diffuse` fordi Høy return-rate ser hovedsakelig ut til å komme fra bred multi-lag-retur, ikke en skarp lokal periode.
- `next_step`: `stop_period_story` fordi Neste steg bør være en annen observabel enn periodisitet.

## Tolkning

- Dette er en ny observabel inne i samme lokale add_chord-band, ikke en ny placement-scan.
- Les dette som periodisitetsdiagnostikk for local recurrence, ikke som bevis for en generell defect-lov.
