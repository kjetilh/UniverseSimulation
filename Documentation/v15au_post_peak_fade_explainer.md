# Relasjonell universgraf v0.15au: post-peak fade explainer

## Formal

Denne runden forklarer bare den lille `anchor_hold` / `fading_holdout` / `no_high_holdout`-triplet-en etter at burst-peaken faktisk er etablert.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Cases

| case | run seed | expected burst | peak start | peak rate | post high | post mid | first low after peak | post-peak label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| anchor_hold | 5002241 | sustained_hold_burst | 61 | 1.000 | 1.000 | 0.000 | -1 | post_peak_hold |
| fading_holdout | 5002233 | fading_late_burst | 51 | 1.000 | 0.154 | 0.769 | 7 | post_peak_fade |
| no_high_holdout | 5002249 | no_high_burst | 0 | 0.000 | 0.000 | 0.000 | 0 | no_launch_tail |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle run i denne runden matcher onsket add_chord-perturbasjon.
- `post_peak_status`: `post_peak_map_supported` fordi Det lille triplet-caset deler seg rent i post-peak hold, post-peak fade og ingen launch-tail.
- `next_step`: `holdout_post_peak_fade` fordi Neste steg bor teste om `post_peak_fade` holder pa noen fa naerliggende seeds rundt fading-caset.

## Tolkning

- Dette er en ren forklaringsrunde for fading-sporet, ikke en ny bred seed-scan.
- Les dette som lokal mekanikk etter peak, ikke som nye defect-arter.
