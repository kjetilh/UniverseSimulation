# v0.15ce operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `target768_plateau_holdout`: `target768_plateau_weak_holdout` fordi Target-768 map holder delvis (0.750), men ikke rent nok til mekanismeforklaring.
- `observed_plateau_members`: `observed` fordi add_chord_p1;add_chord_p2;add_chord_p3;local_swap_p1;local_swap_p2
- `retained_full_near_pairs`: `observed` fordi add_chord_p2::local_swap_p2
- `next_step`: `target768_second_holdout_or_mechanism` fordi Neste steg bor vaere en enda smalere holdout eller en mekanismeobservabel, ikke mer family-label-tuning.

- Les dette som holdout av target-768 plateauet, ikke som en ny bred scale scan.
