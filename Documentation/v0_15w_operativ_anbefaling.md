# v0.15w operativ anbefaling

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert i denne støttekontrasten.
- `support_snapshot`: `degree_gap=0.667;ball1_gap=2.000;expansion_gap=-0.106` fordi Positiv degree/ball1-gap betyr tettere lokal støtte for p1. Negativ expansion-gap betyr at p0 har litt større relativ videre ekspansjon.
- `duel_snapshot`: `tradeoff_rate=0.167;p0_calm_rate=0.000;p1_clean_rate=0.333` fordi Dette oppsummerer hvordan p0 og p1 skiller lag på samme seed_delta i de smale holdout-duellene.
- `p0_p1_contrast`: `contrast_still_mixed` fordi Støttekontrasten gjør p0-vs-p1 mer konkret, men ikke ren nok til å gi én enkel forklaring ennå.
- `next_step`: `stay_local` fordi Neste steg bør være en enda mindre forklaringsrunde på unike noder eller første tail-segment.

- Les denne runden som en liten p0-vs-p1-forklaringsrunde, ikke som bredere cycle-mapping.
