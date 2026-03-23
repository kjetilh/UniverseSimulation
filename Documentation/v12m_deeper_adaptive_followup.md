# Relasjonell universgraf v0.12m: dypere adaptiv oppfølging under fast screening

## Formål

Denne runden holder screeningdelen fast ved `full_basis@0.50` og tester bare en dypere familie av adaptive oppfolgingspolicyer. Maalet er a se om vi kan komme naermere referansen uten a gi fra oss hele tidsgevinsten.

## Metode

- Regime holdes fast ved `band_zero_del`.
- Screening holdes fast ved `full_basis@0.50`.
- Bare adaptive follow-up-policyer varieres.
- Datasett: `24` baser. Screeningsplitt: `40`. Timing-lokker per screeningpass: `300`.

## Realiserte startstørrelser

| target | bases | mean_initial_nodes | q10 | q90 | separated_from_prev | mean_actual_radius | sd_actual_radius |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 6 | 48.0 | 48.0 | 48.0 | 1 | 4.472 | 0.565 |
| 96 | 6 | 96.0 | 96.0 | 96.0 | 1 | 5.194 | 1.684 |
| 192 | 6 | 192.0 | 192.0 | 192.0 | 1 | 8.028 | 1.781 |
| 256 | 6 | 256.0 | 256.0 | 256.0 | 1 | 7.028 | 2.026 |

## Adaptive policy-sammendrag under fast screening

| rank | policy | probe_runs | extend_frac | best_hit | recall | pairwise | total_s | speedup | d_best_hit | d_recall | near_match | faster_and_match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | probe3_top_half | 3 | 0.500 | 0.669 | 0.669 | 0.640 | 20.349 | 1.358 | 0.000 | 0.000 | 1.000 | 1.000 |
| 2 | full_followup | 6 | 1.000 | 0.669 | 0.669 | 0.667 | 27.592 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 |
| 3 | probe2_top_two_thirds | 2 | 0.667 | 0.669 | 0.669 | 0.667 | 27.592 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 |
| 4 | probe3_top_two_thirds | 3 | 0.667 | 0.669 | 0.669 | 0.667 | 27.592 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 |
| 5 | probe4_top_half | 4 | 0.500 | 0.662 | 0.662 | 0.641 | 23.107 | 1.195 | -0.006 | -0.006 | 0.975 | 0.975 |
| 6 | probe2_top_half | 2 | 0.500 | 0.613 | 0.613 | 0.621 | 18.402 | 1.506 | -0.056 | -0.056 | 0.775 | 0.775 |

## Operativ lesning

- Referansen `full_followup` bruker `27.592` sekunder og setter nullpunktet for hit/recall.
- `probe2_top_half` er arven fra `v12k`/`v12l`: `speedup=1.506`, `best_hit=0.613`, `recall=0.613`.
- `probe3_top_half` tester mer informasjon per base uten a utvide feltet: `speedup=1.358`, `best_hit=0.669`, `recall=0.669`.
- `probe2_top_two_thirds` tester bredere adaptiv oppfolging: `speedup=1.000`, `best_hit=0.669`, `recall=0.669`.
- `probe3_top_two_thirds` er den mest informative adaptive utfordreren i denne familien: `speedup=1.000`, `best_hit=0.669`, `recall=0.669`.
- `probe2_top_two_thirds` og `probe3_top_two_thirds` kollapser i praksis til `full_followup` i denne settingen, fordi `0.667` med bare to screenede baser per størrelse betyr at begge blir forlenget. De er derfor nyttige som metodisk kontroll, ikke som ekte adaptive vinnere.
- Den viktigste nye lesningen er at `probe3_top_half` faktisk matcher referansen på mean `best_hit` og `recall`, samtidig som den er klart raskere. Pairwise er fortsatt litt svakere, så dette er den første sterke adaptive utfordreren, ikke en endelig ny standard.

