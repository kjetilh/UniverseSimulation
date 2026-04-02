# Relasjonell universgraf v0.15b: add_chord collision lab

## Formål

Denne runden tester om to separerte `add_chord`-defects oppfører seg som ren superposisjon av to single-runs, eller om vi ser reelle interaksjonssignaler.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |
| 96 | 96.0 | 96.0 | 96.0 | 1 |
| 192 | 192.0 | 192.0 | 192.0 | 1 |
| 256 | 256.0 | 256.0 | 256.0 | 1 |

## Pair orders

| order | n | mean radius | mean components | mean largest frac | mean shape stability | fit_speed |
| --- | --- | --- | --- | --- | --- | --- |
| ab | 16 | 4.870 | 7.561 | 0.589 | 0.616 | 0.107 |
| ba | 16 | 4.870 | 7.561 | 0.589 | 0.616 | 0.107 |

## Interaction diagnostics

| target | pair | dist | pair-union ab | pair-union ba | order jaccard | control jaccard | comp delta ab | comp delta ba | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 48 | 2-3 | 4 | 0.426 | 0.426 | 1.000 | 1.000 | 0.077 | 0.077 | interaction_supported |
| 48 | 2-3 | 4 | 0.462 | 0.462 | 1.000 | 1.000 | 1.385 | 1.385 | interaction_supported |
| 48 | 3-4 | 3 | 0.435 | 0.435 | 1.000 | 1.000 | 0.154 | 0.154 | interaction_supported |
| 48 | 3-4 | 3 | 0.398 | 0.398 | 1.000 | 1.000 | 0.115 | 0.115 | interaction_supported |
| 96 | 0-5 | 5 | 0.455 | 0.455 | 1.000 | 1.000 | -1.520 | -1.520 | interaction_supported |
| 96 | 0-5 | 5 | 0.357 | 0.357 | 1.000 | 1.000 | 2.200 | 2.200 | interaction_supported |
| 96 | 1-5 | 6 | 0.410 | 0.410 | 1.000 | 1.000 | 0.760 | 0.760 | interaction_supported |
| 96 | 1-5 | 6 | 0.416 | 0.416 | 1.000 | 1.000 | -0.680 | -0.680 | interaction_supported |
| 192 | 3-4 | 7 | 0.323 | 0.323 | 1.000 | 1.000 | -1.520 | -1.520 | interaction_supported |
| 192 | 3-4 | 7 | 0.208 | 0.208 | 1.000 | 1.000 | 2.280 | 2.280 | interaction_supported |
| 192 | 1-2 | 7 | 0.357 | 0.357 | 1.000 | 1.000 | -1.960 | -1.960 | interaction_supported |
| 192 | 1-2 | 7 | 0.350 | 0.350 | 1.000 | 1.000 | -0.400 | -0.400 | interaction_supported |
| 256 | 1-5 | 7 | 0.385 | 0.385 | 1.000 | 1.000 | 4.200 | 4.200 | interaction_supported |
| 256 | 1-5 | 7 | 0.420 | 0.420 | 1.000 | 1.000 | 2.200 | 2.200 | interaction_supported |
| 256 | 0-2 | 6 | 0.360 | 0.360 | 1.000 | 1.000 | -3.200 | -3.200 | interaction_supported |
| 256 | 0-2 | 6 | 0.288 | 0.288 | 1.000 | 1.000 | -3.520 | -3.520 | interaction_supported |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er separert, placement-paret er faktisk lokalt separert, og kontrollgrenene holder seg samkjørte mellom AB/BA.
- `collision_signal`: `collision_signal_present` fordi Parvise defects avviker ofte fra unionen av matched single-runs (`interaction_supported` 1.000) uten sterk ordresensitivitet.
- `next_step`: `follow_collision_family` fordi Neste steg bør være en mer direkte kollisjonsklassifisering: annihilation, pass-through, binding eller secondary split.

## Tolkning

- `near_superposition` betyr at dobbeltdefect-rundet ligner unionen av to matched single-runs.
- `interaction_supported` betyr at begge orders avviker tydelig fra unionen, uten sterk ordresensitivitet.
- `order_sensitive` betyr at selve konstruksjonen av dobbeltdefecten er skjør og ma strammes inn videre.
- `control_divergent` betyr at matched control-grenene ikke er like nok mellom AB/BA til at cross-run union-sammenlikningen er trygg.
