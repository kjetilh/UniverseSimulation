# v0.8 refined rerun – kandidatkontroll

Denne rerun-runden bruker flere seeds og lengre horisont på et lite utvalg av coarse-vinnerne.

Refined-vinner: `(r_birth, r_death, p_swap, p_triad)=(0.08, 0.02, 0.02, 0.00)`, composite ≈ 0.932.

| r_birth | r_death | p_swap | p_triad | repair | causal | quasi | geom | composite | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.08 | 0.02 | 0.02 | 0 | 1.000 | 0.790 | 0.967 | 0.956 | 0.932 | repair_cone_candidate |
| 0.02 | 0.05 | 0.02 | 0 | 0.191 | 0.730 | 0.993 | 0.800 | 0.608 | mixed |
| 0.02 | 0 | 0.02 | 0 | 0.226 | 0.552 | 0.985 | 0.933 | 0.601 | mixed |
| 0.02 | 0.02 | 0.02 | 0 | 0.173 | 0.447 | 1.000 | 0.964 | 0.565 | macro_stable_weak_repair |
| 0.02 | 0.02 | 0.02 | 0.02 | 0.062 | 0.619 | 0.542 | 0.577 | 0.401 | drift_dominant |
| 0.08 | 0 | 0.02 | 0.02 | 0.278 | 0.388 | 0.000 | 0.000 | 0.194 | drift_dominant |
