# Relasjonell universgraf v0.12k: adaptiv styring av oppfølgingsbudsjettet

## Formål

Denne runden flytter fokus bort fra pre-screening og inn i selve oppfolgingsarbeidet. Sporsmalet er om noen fa tidlige run-seeds per base kan brukes til a avgjore hvilke baser som faktisk fortjener full oppfolging.

## Metode

- Samme regime: `band_zero_del`.
- Samme dynamiske utfallsmal: full-bundle `mean_final_radius_control` per base.
- Hver policy far se de forste `probe_runs` run-seedene for alle baser.
- Noen policyer stopper der; andre fullforer alle run-seeds for en top-fraksjon av basene innen hver størrelse.
- Datasett: `24` baser og `144` timed single-run rows.

## Realiserte startstørrelser

| target | bases | mean_initial_nodes | q10 | q90 | separated_from_prev | mean_actual_radius | sd_actual_radius |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 6 | 48.0 | 48.0 | 48.0 | 1 | 4.472 | 0.565 |
| 96 | 6 | 96.0 | 96.0 | 96.0 | 1 | 5.194 | 1.684 |
| 192 | 6 | 192.0 | 192.0 | 192.0 | 1 | 8.028 | 1.781 |
| 256 | 6 | 256.0 | 256.0 | 256.0 | 1 | 7.028 | 2.026 |

## Adaptive policy-sammendrag

| rank | policy | probe_runs | extend_frac | best_hit | recall | pairwise | run_frac | time_frac | speedup | near_match | faster_and_match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | full_followup | 6 | 1.00 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1 | 1 |
| 2 | probe1_only | 1 | 0.00 | 0.500 | 0.500 | 0.674 | 0.167 | 0.159 | 6.279 | 0 | 0 |
| 3 | probe2_only | 2 | 0.00 | 0.500 | 0.500 | 0.678 | 0.333 | 0.335 | 2.983 | 0 | 0 |
| 4 | probe1_top_quarter | 1 | 0.25 | 0.500 | 0.750 | 0.778 | 0.444 | 0.438 | 2.283 | 0 | 0 |
| 5 | probe1_top_half | 1 | 0.50 | 0.500 | 0.750 | 0.795 | 0.583 | 0.586 | 1.706 | 0 | 0 |
| 6 | probe2_top_half | 2 | 0.50 | 0.750 | 0.750 | 0.840 | 0.667 | 0.677 | 1.477 | 0 | 0 |

## Operativ lesning

- Referansen `full_followup` bruker all oppfolgingskostnad (`time_frac=1.0`) og gir `best_hit=1.000`, `recall=1.000`.
- `probe1_only` er den raskeste policyen: `time_frac=0.159`, men den faller til `best_hit=0.500`, `recall=0.500`.
- `probe1_top_half` er den mest aggressive adaptive kandidaten i denne runden: `time_frac=0.586`, `best_hit=0.500`, `recall=0.750`.
- `probe2_top_half` er den mest balanserte kandidaten: `time_frac=0.677`, `best_hit=0.750`, `recall=0.750`.
- Den viktigste operative dommen er at ingen adaptive policyer er nær-match mot full oppfolging i denne runden. Adaptiv follow-up ser derfor lovende ut, men er ennå ikke en drop-in erstatning.
