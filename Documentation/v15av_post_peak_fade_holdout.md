# Relasjonell universgraf v0.15av: post-peak fade holdout

## Formal

Denne runden tester bare den nederste lokale nabosonen rundt fading-caset ved seed `231` i placement `2`.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Cases

| role | case | seed delta | post high | post mid | last12 high | post-peak label |
| --- | --- | --- | --- | --- | --- | --- |
| lower_holdout | lower_215 | 215 | 0.000 | 0.000 | 0.000 | no_launch_tail |
| lower_holdout | lower_223 | 223 | 0.000 | 0.000 | 0.000 | no_launch_tail |
| anchor_fade | anchor_231 | 231 | 0.154 | 0.769 | 0.083 | post_peak_fade |
| upper_context | upper_239 | 239 | 1.000 | 0.000 | 0.917 | post_peak_hold |
| upper_context | upper_247 | 247 | 0.000 | 0.000 | 0.000 | no_launch_tail |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle run i denne runden matcher onsket add_chord-perturbasjon.
- `fade_holdout_status`: `fade_singleton_not_supported` fordi Begge nye nedre nabopunktene faller til `no_launch_tail`, sa fading-sporet ser best ut som et singleton-aktig overgangspunkt mellom hold og no-launch.
- `next_step`: `stop_fade_expansion` fordi Neste steg bor ikke vaere bredere fade-scan; dette er bedre lest som et lokalt overgangspunkt.

## Tolkning

- Dette er en minimal holdout rundt fading-caset, ikke en ny bred scan.
- Les dette som lokal overgangsstruktur, ikke som nye defect-arter.
