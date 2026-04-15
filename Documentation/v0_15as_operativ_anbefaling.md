# v0.15as operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle holdout-runene matcher onsket add_chord-perturbasjon.
- `horizon_holdout_status`: `horizon_map_holdout_mixed` fordi Horisont-kartet gir fortsatt nyttig struktur pa holdouts, men holder ikke rent nok som lokalt lovmessig kart ennå.
- `next_step`: `tighten_failed_probe_horizon` fordi Neste steg bor vaere en enda smalere observabel eller holdout rundt failed-probe og terminal-probe-grensen.

- Les denne runden som en smal holdout-test av horisont-kartet, ikke som en ny bred defect-scan.
