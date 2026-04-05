# v0.15x operativ anbefaling

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert i denne første-tail-segment-runden.
- `duel_family_snapshot`: `p1_early=0.000;p1_soft=0.000;tradeoff=0.000;p0_calm=0.000` fordi Dette oppsummerer hvordan p0 og p1 skiller lag i første tail-segment på de samme små holdout-seedene.
- `first_segment_status`: `first_segment_still_mixed` fordi Første tail-segment gjør forskjellen mer konkret, men ikke rent nok til én enkel mekanisme.
- `next_step`: `stay_tiny` fordi Neste steg bør være en enda mindre forklaringsrunde på én eller to seed-caser.

- Les denne runden som en første-tail-segment-test for `p0` vs `p1`, ikke som bredere band-mapping.
