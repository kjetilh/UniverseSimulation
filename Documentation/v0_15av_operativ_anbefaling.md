# v0.15av operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle run i denne runden matcher onsket add_chord-perturbasjon.
- `fade_holdout_status`: `fade_singleton_not_supported` fordi Begge nye nedre nabopunktene faller til `no_launch_tail`, sa fading-sporet ser best ut som et singleton-aktig overgangspunkt mellom hold og no-launch.
- `next_step`: `stop_fade_expansion` fordi Neste steg bor ikke vaere bredere fade-scan; dette er bedre lest som et lokalt overgangspunkt.

- Les denne runden som en minimal fade-holdout, ikke som en ny bred defect-scan.
