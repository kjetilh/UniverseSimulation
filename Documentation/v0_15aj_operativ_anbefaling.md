# v0.15aj operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsen er rent separert, og denne runden bygger bare pa ekte `v15ai`-data.
- `band_onset_status`: `band_onset_structure_supported` fordi De fleste run finner en strukturert ladder-suffix, men onseten er ikke flat: placement 0 gaar oftest rett inn i `low-mid`, mens placement 2 oftere glir senere inn i `mid-high` eller blir igjen i bredere churn.
- `placement_skew`: `descriptive` fordi `p0` har immediate low-mid-rate 0.857, `p1` har delayed mid-high-rate 0.286, og `p2` har delayed mid-high-rate 0.375 med mer churn.
- `next_step`: `probe_band_entry_triggers` fordi Neste steg bor forklare hva i tidlig hale som avgjor om et run gaar direkte inn i `low-mid`, senere inn i `mid-high`, eller blir igjen i tre-band-churn.

- Les denne runden som en onset-lesning av `v15ai`-bandene, ikke som en ny defect-familieinndeling.
