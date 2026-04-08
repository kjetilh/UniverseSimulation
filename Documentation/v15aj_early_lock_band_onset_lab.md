# Relasjonell universgraf v0.15aj: early-lock band onset lab

## Formal

Denne runden bruker `v15ai`-snapshottene til a finne nar run faktisk finner en strukturert `low-mid` eller `mid-high` ladder-suffix, og hvilke run som blir igjen i bredere tre-band-churn.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Source groups

| group | n | structured onset | immediate structured | delayed structured | three-band churn | immediate low-mid | delayed mid-high | onset step | post switches |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| anchor_main_family | 12 | 0.750 | 0.583 | 0.167 | 0.250 | 0.500 | 0.167 | 1593.8 | 9.8 |
| holdout_revert | 10 | 0.900 | 0.600 | 0.300 | 0.100 | 0.500 | 0.300 | 1685.3 | 6.0 |
| combined | 22 | 0.818 | 0.591 | 0.227 | 0.182 | 0.500 | 0.227 | 1639.6 | 7.9 |

## Per placement

| placement | n | structured | immediate low-mid | delayed mid-high | three-band churn | onset step | post dominant share |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 7 | 0.857 | 0.857 | 0.000 | 0.143 | 1536.0 | 0.678 |
| 1 | 7 | 0.857 | 0.429 | 0.286 | 0.143 | 1649.3 | 0.738 |
| 2 | 8 | 0.750 | 0.250 | 0.375 | 0.250 | 1733.3 | 0.849 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er rent separert, og denne runden bygger bare pa ekte `v15ai`-data.
- `band_onset_status`: `band_onset_structure_supported` fordi De fleste run finner en strukturert ladder-suffix, men onseten er ikke flat: placement 0 gaar oftest rett inn i `low-mid`, mens placement 2 oftere glir senere inn i `mid-high` eller blir igjen i bredere churn.
- `placement_skew`: `descriptive` fordi `p0` har immediate low-mid-rate 0.857, `p1` har delayed mid-high-rate 0.286, og `p2` har delayed mid-high-rate 0.375 med mer churn.
- `next_step`: `probe_band_entry_triggers` fordi Neste steg bor forklare hva i tidlig hale som avgjor om et run gaar direkte inn i `low-mid`, senere inn i `mid-high`, eller blir igjen i tre-band-churn.

## Tolkning

- Dette er fortsatt en smal observabelrunde inne i hovedfamilien, ikke en ny defect-scan.
- En strukturert ladder-suffix betyr her at resten av halen holder seg innenfor ett band eller et naboband-par.
- Hvis dette holder, peker neste steg mot lokale triggerforhold ved selve overgangen inn i `low-mid` eller `mid-high`.
