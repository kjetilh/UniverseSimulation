# v0.8 fasekart over repair, kausalitet, drift og geometri

## Formål

Dette er første egentlige fasekart over det fokuserte parameterrommet rundt de mest lovende v0.7-punktene. Hvert gridpunkt kombinerer repair-mål, frontdiagnostikk, makrodrift og geometri-proksier i én rad.

## Metode

- lokal kobling: `maximal`
- perturbasjon: `local_swap`
- steg per run: `400`
- seeds per gridpunkt: `3`
- antall gridpunkter: `162`
- `drift_beta1` og `drift_tokens` er her definert som netto endring per event i kontrollgrenen over kjøringen.
- `fit_speed_control` er lineær tilpasning av radius mot event-tid i kontrollgrenen. Den er et grovt frontmål, ikke en streng bound.
- `geometry_score` er eksplisitt heuristisk: den rangerer høyere `dim_proxy`, `clustering` og `spectral_radius`, men uten å påstå at det finnes en unik riktig geometri-signatur.

## Hovedlesning

- repair-vennlig: høy `meeting_fraction`, høy lokal overlap og lav `total_unequal_time`.
- cone-vennlig: lav `mean_final_radius_control` og lav `fit_speed_control`.
- invariant-vennlig: liten absolutt drift i `beta1` og `tokens`.
- geometri-vennlig: høyere `dim_proxy`/`clustering`/`spectral_radius` uten samtidig stor drift.

## Sweet spot-kandidater

| r_birth | r_death | p_swap | p_triad | p_del | score | meeting | overlap | same_desc | unequal | radius | speed | |drift_beta1| | |drift_tokens| | dim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.02 | 0 | 0.02 | 0.01 | 0.01 | 0.786 | 0.333 | 0.532 | 0.533 | 31.1 | 1 | 0.034 | 0.00667 | 0.0383 | 0.91 |
| 0.05 | 0.02 | 0.04 | 0.01 | 0.01 | 0.759 | 0.333 | 0.42 | 0.416 | 25 | 0.333 | 0.0007 | 0.00167 | 0.0567 | 0.95 |
| 0.02 | 0.05 | 0.08 | 0.01 | 0.01 | 0.750 | 0.333 | 0.435 | 0.427 | 31.2 | 1.67 | 0.0607 | 0.00167 | 0.0267 | 1.38 |
| 0.02 | 0.02 | 0.08 | 0.03 | 0 | 0.737 | 0.333 | 0.424 | 0.426 | 29.5 | 1 | 0.051 | 0.0183 | 0.0275 | 1.12 |
| 0.02 | 0 | 0.08 | 0 | 0 | 0.735 | 0.333 | 0.382 | 0.379 | 32.3 | 1 | 0.0374 | 0 | 0.03 | 1.21 |
| 0.08 | 0.05 | 0.02 | 0.01 | 0.01 | 0.719 | 0.333 | 0.478 | 0.477 | 17.8 | 0.667 | 0.0737 | 0.000833 | 0.0783 | 1.01 |
| 0.05 | 0 | 0.08 | 0.03 | 0 | 0.715 | 0.333 | 0.428 | 0.435 | 17.5 | 0.667 | 0.0546 | 0.0233 | 0.0975 | 0.955 |
| 0.02 | 0.05 | 0.04 | 0.03 | 0 | 0.711 | 0.333 | 0.4 | 0.394 | 31.7 | 1.33 | 0.0424 | 0.025 | 0.0408 | 1.32 |

## Repair-vennlige punkter

| r_birth | r_death | p_swap | p_triad | p_del | score | meeting | overlap | same_desc | unequal | radius | speed | |drift_beta1| | |drift_tokens| | dim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.02 | 0 | 0.02 | 0.01 | 0.01 | 0.960 | 0.333 | 0.532 | 0.533 | 31.1 | 1 | 0.034 | 0.00667 | 0.0383 | 0.91 |
| 0.08 | 0.05 | 0.02 | 0.01 | 0.01 | 0.937 | 0.333 | 0.478 | 0.477 | 17.8 | 0.667 | 0.0737 | 0.000833 | 0.0783 | 1.01 |
| 0.05 | 0 | 0.08 | 0.03 | 0 | 0.892 | 0.333 | 0.428 | 0.435 | 17.5 | 0.667 | 0.0546 | 0.0233 | 0.0975 | 0.955 |
| 0.05 | 0 | 0.08 | 0.01 | 0.01 | 0.881 | 0.333 | 0.407 | 0.421 | 14.2 | 1 | 0.0842 | 0.000833 | 0.0642 | 0.956 |
| 0.05 | 0.02 | 0.04 | 0.01 | 0.01 | 0.862 | 0.333 | 0.42 | 0.416 | 25 | 0.333 | 0.0007 | 0.00167 | 0.0567 | 0.95 |
| 0.02 | 0.05 | 0.08 | 0.01 | 0.01 | 0.862 | 0.333 | 0.435 | 0.427 | 31.2 | 1.67 | 0.0607 | 0.00167 | 0.0267 | 1.38 |
| 0.02 | 0.02 | 0.08 | 0.03 | 0 | 0.859 | 0.333 | 0.424 | 0.426 | 29.5 | 1 | 0.051 | 0.0183 | 0.0275 | 1.12 |
| 0.02 | 0.05 | 0.04 | 0.03 | 0 | 0.827 | 0.333 | 0.4 | 0.394 | 31.7 | 1.33 | 0.0424 | 0.025 | 0.0408 | 1.32 |

## Cone-vennlige punkter

| r_birth | r_death | p_swap | p_triad | p_del | score | meeting | overlap | same_desc | unequal | radius | speed | |drift_beta1| | |drift_tokens| | dim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.05 | 0.02 | 0.04 | 0.01 | 0.01 | 0.974 | 0.333 | 0.42 | 0.416 | 25 | 0.333 | 0.0007 | 0.00167 | 0.0567 | 0.95 |
| 0.05 | 0 | 0.08 | 0.03 | 0 | 0.830 | 0.333 | 0.428 | 0.435 | 17.5 | 0.667 | 0.0546 | 0.0233 | 0.0975 | 0.955 |
| 0.08 | 0 | 0.02 | 0.03 | 0 | 0.823 | 0 | 0.312 | 0.308 | 16.5 | 1 | 0.0346 | 0.0225 | 0.128 | 0.852 |
| 0.02 | 0 | 0.02 | 0.01 | 0.01 | 0.791 | 0.333 | 0.532 | 0.533 | 31.1 | 1 | 0.034 | 0.00667 | 0.0383 | 0.91 |
| 0.08 | 0.05 | 0.02 | 0.01 | 0.01 | 0.789 | 0.333 | 0.478 | 0.477 | 17.8 | 0.667 | 0.0737 | 0.000833 | 0.0783 | 1.01 |
| 0.05 | 0.02 | 0.02 | 0.01 | 0.01 | 0.786 | 0 | 0.225 | 0.23 | 32.7 | 1 | 0.0347 | 0 | 0.0608 | 0.896 |
| 0.02 | 0 | 0.08 | 0 | 0 | 0.782 | 0.333 | 0.382 | 0.379 | 32.3 | 1 | 0.0374 | 0 | 0.03 | 1.21 |
| 0.02 | 0.02 | 0.08 | 0.03 | 0 | 0.760 | 0.333 | 0.424 | 0.426 | 29.5 | 1 | 0.051 | 0.0183 | 0.0275 | 1.12 |

## Invariant-vennlige punkter

| r_birth | r_death | p_swap | p_triad | p_del | score | meeting | overlap | same_desc | unequal | radius | speed | |drift_beta1| | |drift_tokens| | dim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.02 | 0.05 | 0.02 | 0 | 0 | 0.983 | 0 | 0.223 | 0.226 | 85.7 | 3 | 0.0423 | 0 | 0.0125 | 1.18 |
| 0.02 | 0.05 | 0.02 | 0.01 | 0.01 | 0.980 | 0 | 0.251 | 0.231 | 47.1 | 2.33 | 0.0334 | 0 | 0.0133 | 1.09 |
| 0.02 | 0.05 | 0.08 | 0 | 0 | 0.971 | 0 | 0.177 | 0.183 | 70.3 | 2.67 | 0.0396 | 0 | 0.0158 | 1.42 |
| 0.02 | 0.05 | 0.04 | 0 | 0 | 0.963 | 0 | 0.182 | 0.195 | 56.4 | 2 | 0.0331 | 0 | 0.0183 | 1.37 |
| 0.02 | 0.05 | 0.02 | 0 | 0.01 | 0.962 | 0 | 0.279 | 0.278 | 57.3 | 2 | 0.0372 | 0.00167 | 0.0108 | 1.21 |
| 0.02 | 0.02 | 0.02 | 0 | 0.01 | 0.942 | 0 | 0.211 | 0.207 | 47.5 | 2.67 | 0.057 | 0.00167 | 0.0167 | 0.926 |
| 0.02 | 0.05 | 0.08 | 0 | 0.01 | 0.937 | 0 | 0.0944 | 0.0946 | 61.4 | 2.67 | 0.0356 | 0.0025 | 0.0142 | 0.857 |
| 0.02 | 0.05 | 0.02 | 0.01 | 0 | 0.932 | 0 | 0.251 | 0.258 | 57 | 2.33 | 0.0391 | 0.00417 | 0.0075 | 1.2 |

## Geometri-vennlige punkter

| r_birth | r_death | p_swap | p_triad | p_del | score | meeting | overlap | same_desc | unequal | radius | speed | |drift_beta1| | |drift_tokens| | dim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.02 | 0.05 | 0.02 | 0.03 | 0 | 0.790 | 0 | 0.246 | 0.245 | 65.4 | 2 | 0.026 | 0.0308 | 0.0267 | 1.18 |
| 0.02 | 0 | 0.04 | 0.03 | 0 | 0.741 | 0 | 0.156 | 0.153 | 40.5 | 1.67 | 0.0388 | 0.0225 | 0.0575 | 1.09 |
| 0.02 | 0.05 | 0.04 | 0.03 | 0 | 0.725 | 0.333 | 0.4 | 0.394 | 31.7 | 1.33 | 0.0424 | 0.025 | 0.0408 | 1.32 |
| 0.02 | 0 | 0.02 | 0.03 | 0 | 0.717 | 0 | 0.244 | 0.262 | 38 | 1.67 | 0.0434 | 0.0217 | 0.0375 | 1.03 |
| 0.08 | 0 | 0.02 | 0.03 | 0 | 0.708 | 0 | 0.312 | 0.308 | 16.5 | 1 | 0.0346 | 0.0225 | 0.128 | 0.852 |
| 0.02 | 0.02 | 0.04 | 0.03 | 0 | 0.690 | 0 | 0.243 | 0.244 | 42.2 | 2 | 0.0486 | 0.0192 | 0.0417 | 1.17 |
| 0.08 | 0.02 | 0.02 | 0.03 | 0 | 0.666 | 0 | 0.332 | 0.356 | 16.8 | 1.67 | 0.109 | 0.02 | 0.137 | 0.968 |
| 0.08 | 0.02 | 0.02 | 0.03 | 0.01 | 0.665 | 0 | 0.209 | 0.211 | 16.6 | 2 | 0.121 | 0.0158 | 0.13 | 0.866 |

## Vurdering

Det beste kompromisset i denne scanningen ligger ved `r_birth=0.02`, `r_death=0`, `p_swap=0.02`, `p_triad=0.01`, `p_del=0.01`.

Dette er ikke et bevis på et unikt optimalt regime, men et praktisk sweet spot for neste runde: punktet kombinerer høyere repair-score enn de fleste konkurrenter med moderat radius, lavere drift og relativt strukturerte geometri-proksier.

## Hva som er data, og hva som er tolkning

- Data: alle tall i CSV-en og tabellene over.
- Tolkning: at et punkt er `repair-vennlig`, `cone-vennlig`, `invariant-vennlig` eller `geometri-vennlig` er en operasjonell merkelapp basert på scorene over.
- Spekulasjon: at et slikt sweet spot faktisk er en kandidat for emergent spacetime. Det krever mer presis skalering, flere seeds og helst strengere lokale koblinger i åpne familier.

_CSV: `Documentation/v08_phase_map.csv`_
