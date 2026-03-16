# v0.10b ensemble calibration

Dette dokumentet kalibrerer den naturlige ensemble-generatoren før videre asymptotisk tolkning.
Målet er å skille tydelig mellom nominell størrelse, realisert initial størrelse og senere dynamisk utvikling.

## Hovedpoeng

- `baseline` = gammel generatorlogikk med fast burn-in og ekstra burn-in.
- `adaptive` = samme mikrodynamikk, men med en enkel, dokumentert størrelses-kalibrering som stopper på et in-band snapshot hvis mulig.
- Et størrelsesnivå regnes bare som operativt separert hvis 10–90% intervallene ikke overlapper med nabonivået.

## Oppsummering av realiserte størrelser

| method | burnin | target | mean_realized | sd | q10 | q90 | hit_rate | abs_rel_err |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| adaptive | deep | 24 | 26.0 | 0.0 | 26.0 | 26.0 | 1.00 | 0.083 |
| adaptive | deep | 48 | 45.0 | 0.0 | 45.0 | 45.0 | 1.00 | 0.062 |
| adaptive | deep | 96 | 87.0 | 0.0 | 87.0 | 87.0 | 1.00 | 0.094 |
| adaptive | light | 24 | 24.0 | 0.0 | 24.0 | 24.0 | 1.00 | 0.000 |
| adaptive | light | 48 | 45.0 | 0.0 | 45.0 | 45.0 | 1.00 | 0.062 |
| adaptive | light | 96 | 87.0 | 0.0 | 87.0 | 87.0 | 1.00 | 0.094 |
| baseline | deep | 24 | 35.0 | 0.0 | 35.0 | 35.0 | 0.00 | 0.458 |
| baseline | deep | 48 | 54.0 | 0.0 | 54.0 | 54.0 | 0.00 | 0.125 |
| baseline | deep | 96 | 73.0 | 0.0 | 73.0 | 73.0 | 0.00 | 0.240 |
| baseline | light | 24 | 27.0 | 0.0 | 27.0 | 27.0 | 0.00 | 0.125 |
| baseline | light | 48 | 45.0 | 0.0 | 45.0 | 45.0 | 1.00 | 0.062 |
| baseline | light | 96 | 60.0 | 0.0 | 60.0 | 60.0 | 0.00 | 0.375 |

## Overlapp mellom nabonivåer

| method | burnin | A | B | gap_q90_to_q10 | overlap_fraction | strictly_separated |
| --- | --- | --- | --- | --- | --- | --- |
| adaptive | deep | 24 | 48 | 19.0 | 0.00 | 1 |
| adaptive | deep | 48 | 96 | 42.0 | 0.00 | 1 |
| adaptive | light | 24 | 48 | 21.0 | 0.00 | 1 |
| adaptive | light | 48 | 96 | 42.0 | 0.00 | 1 |
| baseline | deep | 24 | 48 | 19.0 | 0.00 | 1 |
| baseline | deep | 48 | 96 | 19.0 | 0.00 | 1 |
| baseline | light | 24 | 48 | 18.0 | 0.00 | 1 |
| baseline | light | 48 | 96 | 15.0 | 0.00 | 1 |

## Grei operativ lesning

- `adaptive` / `deep`: brukbare nominelle nivåer = 24,48,96 (count=3)
- `adaptive` / `light`: brukbare nominelle nivåer = 24,48,96 (count=3)
- `baseline` / `deep`: brukbare nominelle nivåer = 24,48,96 (count=3)
- `baseline` / `light`: brukbare nominelle nivåer = 24,48,96 (count=3)

## Tolkning

Hvis et nominelt nivå realiserer omtrent samme nodeantall som et nabonivå, er det et generatorproblem, ikke et asymptotisk funn.
Negative eller ekstreme eksponenter under slike forhold må tolkes som metodiske artefakter inntil generatoren er reparert eller byttet ut.

