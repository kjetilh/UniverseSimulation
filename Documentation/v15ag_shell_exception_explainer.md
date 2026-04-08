# Relasjonell universgraf v0.15ag: shell exception explainer

## Formal

Denne runden kjorer ingen nye simuleringer. Den forklarer bare minoritetsavvikene fra `v15af` for a se om de kollapser til et lite lokalt mekanismesett.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Exception runs

| placement | seed | timing | mechanism | prefix steps | longest connected | final fragment | suffix frag | switches | exact return |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 239 | intermittent_fragment_churn | alternating_to_late_lock | 0.0 | 120.0 | 576.0 | 0.757 | 6.000 | 0.899 |
| 1 | 151 | intermittent_fragment_churn | alternating_to_late_lock | 48.0 | 128.0 | 344.0 | 0.714 | 7.000 | 0.977 |
| 1 | 179 | delayed_fragment_lock | two_stage_fragment_lock | 32.0 | 40.0 | 536.0 | 0.960 | 3.000 | 0.938 |
| 1 | 211 | mixed_fragment_timing | near_lock_boundary_case | 0.0 | 144.0 | 632.0 | 0.823 | 4.000 | 0.860 |
| 2 | 151 | connected_resistance_churn | singleton_resistance_case | 8.0 | 280.0 | 80.0 | 0.252 | 15.000 | 0.984 |
| 2 | 211 | intermittent_fragment_churn | alternating_to_late_lock | 0.0 | 184.0 | 120.0 | 0.694 | 6.000 | 1.000 |

## Exception aggregate

| mechanism | n | rate | mean prefix | mean final fragment | mean suffix frag | mean switches |
| --- | --- | --- | --- | --- | --- | --- |
| alternating_to_late_lock | 3 | 0.500 | 16.0 | 346.7 | 0.722 | 6.333 |
| near_lock_boundary_case | 1 | 0.167 | 0.0 | 632.0 | 0.823 | 4.000 |
| singleton_resistance_case | 1 | 0.167 | 8.0 | 80.0 | 0.252 | 15.000 |
| two_stage_fragment_lock | 1 | 0.167 | 32.0 | 536.0 | 0.960 | 3.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er fortsatt rent separert; denne runden forklarer bare de ekte minoritetsavvikene fra v15af.
- `exception_mechanism_status`: `minority_exceptions_are_locally_explainable` fordi Minoritetsavvikene kollapser til et lite lokalt sett: totrinns fragment-lock, singleton-resistens, en boundary-case og en liten gruppe alternating-to-late-lock spor.
- `next_step`: `target_exception_holdout` fordi Neste steg bor teste om akkurat disse unntaksmekanismene holder pa noen fa nye naerliggende seeds, ikke scanne bredere.

## Tolkning

- Dette er en ren unntaksforklaring inne i `v15af`, ikke en ny scan.
- Les mekanismene som lokale forklaringskategorier, ikke som nye defect-arter.
