# v0.15bn operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsene er rent separert og alle add_chord-runs matcher onsket perturbasjon.
- `anchor_profile`: `cycle_band_p2` fordi Ankeret er target 48, placement 2, siden det var den sterkeste spektrale lommen i v15bl innen add_chord-bandet.
- `scale_jump_match`: `small_scale_jump_match_weak` fordi Beste 96-match er p3, men combined distance-gapet til neste kandidat er bare 0.019.
- `next_step`: `holdout_with_one_control` fordi Neste steg bor teste ankerparet mot en enkel 96-kontroll for a se om dette er ekte eller bare svak lokal konkurranse.

- Les denne runden som en liten add_chord-skalaovergang, ikke som en ny generell geometri-lov.
