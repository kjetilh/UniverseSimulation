# Relasjonell universgraf v0.15g: collision genealogy lab

## Formål

Denne runden holder samme add_chord-kollisjonsoppsett som v15b-v15f, men lar genealogy, event-kjeder og komponentbaner være hovedproduktet i stedet for de gamle coarse window-etikettene.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Pair availability audit

| growth | pair | available | min dist |
| --- | --- | --- | --- |
| 101 | 2-3 | 1 | 4 |
| 101 | 3-4 | 1 | 1 |
| 202 | 2-3 | 0 | -1 |
| 202 | 3-4 | 1 | 3 |

## Aggregate genealogy signals

| pair | included | ambiguous | split | merge | birth | death | mean lifetime | max comps | dual duration | dominant chain | hetero | old mixed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2-3 | 6 | 0 | 30.167 | 33.500 | 34.500 | 30.500 | 19.885 | 8.833 | 226.333 | split_persistent_dual | 0.000 | 0.500 |
| 3-4 | 6 | 0 | 23.167 | 28.000 | 38.333 | 31.833 | 21.664 | 8.000 | 120.333 | split_persistent_dual | 0.000 | 0.500 |

## Event-chain frequencies

| pair | chain | n | rate |
| --- | --- | --- | --- |
| 2-3 | compress_split_rebind | 2 | 0.333 |
| 2-3 | merge_hold_split | 2 | 0.333 |
| 2-3 | split_persistent_dual | 2 | 0.333 |
| 2-3 | split_fragment | 0 | 0.000 |
| 2-3 | heterogeneous | 0 | 0.000 |
| 3-4 | compress_split_rebind | 2 | 0.333 |
| 3-4 | merge_hold_split | 0 | 0.000 |
| 3-4 | split_persistent_dual | 4 | 0.667 |
| 3-4 | split_fragment | 0 | 0.000 |
| 3-4 | heterogeneous | 0 | 0.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstørrelsene er separert, begge pair-familiene finnes på den delte 101-basen, og order-control holder seg samkjørt.
- `genealogy_signal`: `partially_structured` fordi Genealogy-sporingen reduserer noe usikkerhet, men pair-familiene kollapser fortsatt ikke rent til én liten chain-familie (`2-3` split_persistent_dual, `3-4` split_persistent_dual).
- `next_step`: `follow_representative_traces` fordi Neste steg bør være å følge noen få representative runs lenger i tid med de samme observablene.

## Tolkning

- `split`, `merge`, `birth` og `death` er genealogy-hendelser i den lokale damagesonen, ikke partikkelbevis.
- `compress_split_rebind`, `merge_hold_split`, `split_persistent_dual` og `split_fragment` er diagnostiske chain-navn, ikke fysiske arter.
- De gamle `window_class`-etikettene beholdes bare som downstream-sammenlikning.
