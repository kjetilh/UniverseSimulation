# Relasjonell universgraf v0.15h: representative collision traces

## Formål

Denne runden følger noen få representative v15g-traces lenger i tid. Målet er å se om de tidlige genealogy-chainene fortsatt bærer informasjon på lang horisont, eller om de kollapser til en felles senfase.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Representative traces

| trace | pair | offset | expected prefix | prefix chain | full chain | tail | final comps | tail dual |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pair23_merge_hold_split | 2-3 | 0 | merge_hold_split | merge_hold_split | merge_hold_split | rebound_merge_tail | 1.000 | 0.310 |
| pair23_compress_split_rebind | 2-3 | 11 | compress_split_rebind | compress_split_rebind | compress_split_rebind | mixed_tail | 1.000 | 0.316 |
| pair23_split_persistent_dual | 2-3 | 5 | split_persistent_dual | split_persistent_dual | split_persistent_dual | mixed_tail | 1.000 | 0.000 |
| pair34_split_persistent_dual | 3-4 | 5 | split_persistent_dual | split_persistent_dual | split_persistent_dual | rebound_merge_tail | 1.000 | 0.456 |

## Operativ lesning

- `artifact_control`: `clean` fordi Order-control holder seg samkjørt og matched controls forblir stabile gjennom den lengre horisonten.
- `trace_signal`: `long_horizon_family_difference` fordi Representative tracene holder ikke én felles senfase; tail-behavior skiller seg på tvers av tracene (mixed_tail, rebound_merge_tail).
- `next_step`: `follow_trace_genealogies` fordi Neste steg bør følge noen få representative traces enda mer direkte, ikke starte ny bred pair-scan.

## Tolkning

- Disse trace-kjedene er fortsatt diagnostiske arbeidskategorier, ikke partikkelbevis.
- Langhorisont-runden brukes her til å teste om tidlige chain-navn holder eller vaskes ut senere.
- Hvis flere traces ender likt sent, er det en nyttig negativ innsikt, ikke et nederlag.
