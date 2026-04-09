# Relasjonell universgraf v0.15ak: band entry trigger lab

## Formal

Denne runden tester om enkle tidlige hale-features kan forklare onset-typene fra `v15aj`, spesielt skillet mellom immediate `low-mid`, senere `mid-high`, og vedvarende tre-band-churn.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Source groups

| group | n | compact low | mid-loaded low-mid | boundary mixed | heavy high | early low | early mid | early high | switches |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| anchor_main_family | 12 | 0.500 | 0.000 | 0.417 | 0.083 | 0.694 | 0.250 | 0.056 | 2.583 |
| holdout_revert | 10 | 0.500 | 0.100 | 0.300 | 0.100 | 0.608 | 0.337 | 0.054 | 2.900 |
| combined | 22 | 0.500 | 0.045 | 0.364 | 0.091 | 0.655 | 0.290 | 0.055 | 2.727 |

## Per onset family

| onset family | n | compact low | mid-loaded low-mid | boundary mixed | heavy high | mean comp | largest frac | switches |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| immediate_low_family | 12 | 0.917 | 0.083 | 0.000 | 0.000 | 2.458 | 0.514 | 1.167 |
| mid_high_entry_family | 6 | 0.000 | 0.000 | 0.667 | 0.333 | 4.549 | 0.271 | 5.167 |
| persistent_churn_family | 4 | 0.000 | 0.000 | 1.000 | 0.000 | 3.542 | 0.310 | 3.750 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er rent separert, og denne runden bygger bare pa ekte `v15ai`- og `v15aj`-data.
- `entry_trigger_status`: `entry_trigger_map_partly_supported` fordi Tidlig hale skiller immediate `low-mid` ganske rent fra resten: disse runene er nesten alltid kompakte low-entry-caser, mens `mid-high` og vedvarende churn for det meste lever i en boundary/heavy-trigger-sone.
- `family_split_note`: `descriptive` fordi Immediate low-family har compact-low-rate 0.917, mid-high-family har boundary/heavy-rate 1.000, og churn-family har boundary-rate 1.000.
- `next_step`: `split_boundary_zone` fordi Neste steg bor forklare hva som deler boundary-zonen i faktisk `mid-high`-entry mot vedvarende tre-band-churn.

## Tolkning

- Dette er fortsatt en smal forklaringsrunde inne i samme hovedfamilie og samme halevindu.
- `compact_low_entry_trigger` betyr tidlig lav last, lavt komponentnivaa og rolig switching.
- `boundary_mixed_trigger` betyr at runet starter i en blandet grensesone der tidlig hale ikke ennå skiller rent mellom `mid-high`-entry og vedvarende churn.
