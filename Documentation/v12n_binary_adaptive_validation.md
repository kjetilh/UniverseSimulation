# Relasjonell universgraf v0.12n: binær validering av probe3_top_half

## Formål

Denne runden er bevisst smal. Vi holder screening fast ved `full_basis@0.50` og sammenligner bare `full_followup`, `probe3_top_half` og to små beslutningsregelvarianter.

## Metode

- Regime holdes fast ved `band_zero_del`.
- Screening holdes fast ved `full_basis@0.50`.
- Adaptive policyer bygger alle på `probe_runs=3`.
- Datasett: `24` baser. Screeningsplitt: `40`. Timing-lokker per screeningpass: `300`.

## Realiserte startstørrelser

| target | bases | mean_initial_nodes | q10 | q90 | separated_from_prev | mean_actual_radius | sd_actual_radius |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 6 | 48.0 | 48.0 | 48.0 | 1 | 4.472 | 0.565 |
| 96 | 6 | 96.0 | 96.0 | 96.0 | 1 | 5.194 | 1.684 |
| 192 | 6 | 192.0 | 192.0 | 192.0 | 1 | 8.028 | 1.781 |
| 256 | 6 | 256.0 | 256.0 | 256.0 | 1 | 7.028 | 2.026 |

## Policy-sammendrag

| rank | policy | best_hit | recall | pairwise | total_s | speedup | d_best_hit | d_recall | d_pairwise | near_match | faster_and_match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | full_followup | 0.669 | 0.669 | 0.644 | 26.874 | 1.000 | 0.000 | 0.000 | 0.000 | 1.000 | 1.000 |
| 2 | probe3_top_half | 0.650 | 0.650 | 0.590 | 19.835 | 1.356 | -0.019 | -0.019 | -0.054 | 0.925 | 0.925 |
| 3 | probe3_top_half_screen_tiebreak | 0.650 | 0.650 | 0.590 | 19.835 | 1.356 | -0.019 | -0.019 | -0.054 | 0.925 | 0.925 |
| 4 | probe3_guarded_half | 0.650 | 0.650 | 0.590 | 20.470 | 1.320 | -0.019 | -0.019 | -0.054 | 0.925 | 0.925 |

## Operativ lesning

- `full_followup` er referansen med `total_s=26.874`.
- `probe3_top_half` er hovedutfordreren: `speedup=1.356`, `best_hit=0.650`, `recall=0.650`, `pairwise=0.590`.
- `probe3_top_half_screen_tiebreak` tester om skjermscore kan brukes som sekundær beslutningsregel: `speedup=1.356`, `pairwise=0.590`.
- `probe3_guarded_half` tester om små partielle forskjeller bør utløse bredere forlengelse: `speedup=1.320`, `best_hit=0.650`, `recall=0.650`.
- Den viktige repo-lojale lesningen her er at `probe3_top_half` fortsatt er raskere, men ikke lenger matcher referansen på hit/recall i denne direkte valideringen.
- Siden tie-break- og guarded-varianten ikke hjelper, ser det forelopig ikke ut som om små lokale beslutningsregel-justeringer er nok til a lukke gapet.

