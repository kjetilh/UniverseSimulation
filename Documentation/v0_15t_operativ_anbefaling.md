# v0.15t operativ anbefaling

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle smale holdout-profiler matcher ønsket add_chord-perturbasjon.
- `cycle_center_status`: `shifted_center_p1` fordi Plassering 1 holder høyere cycle-rate og høyere exact-return over de smale holdout-seedene enn plassering 2.
- `pairwise_seed_duels`: `p1_wins=4;p2_wins=2;ties=0` fordi Dette teller bare smale head-to-head-dueller på samme seed_delta, med 0.01 som liten likevektsterskel.
- `next_step`: `probe_p1_microcenter` fordi Neste steg bør være en enda smalere mikrotest rundt p1 som lokalt cycle-sentrum.

- Les denne runden som en smal holdout-test inne i det lokale add_chord-båndet, ikke som en ny bred cycle-scan.
