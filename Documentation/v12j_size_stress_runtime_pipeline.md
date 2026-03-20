# Relasjonell universgraf v0.12j: moderat størrelses-stresstest av målt runtime-pipeline

## Formål

Denne runden tester om v12i-lesningen holder nar vi flytter den samme arbeidsflyten opp til noe storre naturlige ensembler. Maalet er ikke ny frontier eller ny modell, men a se om screeningdelen blir mer relevant eller om oppfolging fortsatt dominerer.

## Metode

- Samme arbeidsregime: `band_zero_del`.
- Samme policyfamilie: `full_basis@0.50`, `spectral_only@0.50`, `spectral_plus_dim@0.667`, pluss `random_baseline@0.50`.
- Samme type måling som v12i: virkelig screeningtid og virkelig oppfolgingstid på lokal kodebane.
- Datasett: `32` baser og `96` underliggende runs i denne storrelsesrunden.
- Screening-splitt: `12`. Timing-lokker per screeningpass: `60`.

## Realiserte startstørrelser

| target | bases | mean_initial_nodes | q10 | q90 | separated_from_prev | mean_actual_radius | sd_actual_radius |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 96 | 8 | 96.0 | 96.0 | 96.0 | 1 | 5.917 | 0.924 |
| 192 | 8 | 192.0 | 192.0 | 192.0 | 1 | 7.083 | 1.884 |
| 320 | 8 | 320.0 | 320.0 | 320.0 | 1 | 7.083 | 1.698 |
| 384 | 8 | 384.0 | 384.0 | 384.0 | 1 | 7.833 | 2.769 |

## Målt oppfølgingstid per størrelse

| target | samples | mean_bundle_seconds | mean_seconds_per_run | mean_steps_per_run | q10_bundle | q90_bundle |
| --- | --- | --- | --- | --- | --- | --- |
| 96 | 1 | 1.2716 | 0.4239 | 480.0 | 1.2716 | 1.2716 |
| 192 | 1 | 2.4455 | 0.8152 | 800.0 | 2.4455 | 2.4455 |
| 320 | 1 | 2.7407 | 0.9136 | 800.0 | 2.7407 | 2.7407 |
| 384 | 1 | 4.0376 | 1.3459 | 800.0 | 4.0376 | 4.0376 |

## Målt pipeline-sammendrag

| rank | policy | budget | total_s | speedup_vs_ref | best_hit | recall | d_best_hit | d_recall | near_match | faster | faster_and_match | screen_share |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | full_basis | 0.500 | 20.9910 | 1.000 | 0.500 | 0.500 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000005 |
| 2 | random_baseline | 0.500 | 20.9909 | 1.000 | 0.500 | 0.500 | 0.000 | 0.000 | 0.500 | 1.000 | 0.500 | 0.000001 |
| 3 | spectral_only | 0.500 | 20.9910 | 1.000 | 0.396 | 0.396 | -0.104 | -0.104 | 0.500 | 1.000 | 0.500 | 0.000002 |
| 4 | spectral_plus_dim | 0.667 | 31.4864 | 0.667 | 0.729 | 0.729 | 0.229 | 0.229 | 0.833 | 0.000 | 0.000 | 0.000002 |

## Operativ lesning

- Referansen `full_basis@0.50` bruker `20.9910` sekunder per split, og screeningdelen utgjor bare `0.000005` av totalen.
- `spectral_only@0.50` gir `speedup_vs_ref=1.000`, men `near_match=0.500` og svakere hit/recall enn referansen.
- `spectral_plus_dim@0.667` gir `speedup_vs_ref=0.667` og `near_match=0.833`.
- `random_baseline@0.50` matcher faktisk `full_basis@0.50` pa mean best-hit og recall i denne lille større-runden, selv om den er svakere pa `near_match`. Det er en tydelig advarsel om at screening-signalet ikke styrker seg automatisk med litt større grafer.
- Denne runden skal leses som en størrelses-stresstest av v12i. Screeningandelen er fortsatt naer null, sa den praktiske flaskehalsen ligger fortsatt i oppfolgingen, ikke i valg av enkel screeningbasis.
