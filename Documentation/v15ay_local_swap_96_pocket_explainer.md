# Relasjonell universgraf v0.15ay: local_swap 96-pocket explainer

## Formål

Denne runden forklarer den ene `96`-lommen i v15aw som fortsatt holder `stable_core_variable_shell`, og sammenligner den med noen få nære ikke-lommer.

## Case rows

| role | growth_seed | placement | label | support | mean degree | ball3/ball1 | core share | shell share | rare share | coarse return |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| background_nonpocket | 101 | 0 | diffuse_shell_recurrence | 9,15,58 | 4.667 | 3.727 | 0.352 | 0.443 | 0.205 | 0.677 |
| compact_nonpocket_control | 101 | 1 | mixed_core_shell | 0,1,12 | 5.667 | 3.000 | 0.402 | 0.448 | 0.149 | 0.615 |
| background_nonpocket | 101 | 2 | diffuse_shell_recurrence | 0,1,70 | 4.333 | 3.083 | 0.192 | 0.479 | 0.329 | 0.446 |
| pocket_anchor | 101 | 3 | stable_core_variable_shell | 4,5,16 | 5.667 | 2.600 | 0.563 | 0.287 | 0.149 | 0.785 |
| high_core_nonpocket_control | 202 | 0 | mixed_core_shell | 8,10,64 | 4.667 | 4.091 | 0.516 | 0.333 | 0.151 | 0.585 |
| background_nonpocket | 202 | 1 | diffuse_shell_recurrence | 6,7,18 | 6.667 | 2.722 | 0.342 | 0.384 | 0.274 | 0.846 |
| background_nonpocket | 202 | 2 | diffuse_shell_recurrence | 6,7,8 | 7.667 | 2.571 | 0.130 | 0.442 | 0.429 | 0.446 |
| same_placement_diffuse_control | 202 | 3 | diffuse_shell_recurrence | 0,13,39 | 5.333 | 2.786 | 0.222 | 0.444 | 0.333 | 0.631 |

## Role summary

| role | n | stable core+shell | diffuse shell | mean degree | mean ball3/ball1 | mean core share | mean rare share | mean coarse return |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pocket_anchor | 1 | 1.000 | 0.000 | 5.667 | 2.600 | 0.563 | 0.149 | 0.785 |
| same_placement_diffuse_control | 1 | 0.000 | 1.000 | 5.333 | 2.786 | 0.222 | 0.333 | 0.631 |
| compact_nonpocket_control | 1 | 0.000 | 0.000 | 5.667 | 3.000 | 0.402 | 0.149 | 0.615 |
| high_core_nonpocket_control | 1 | 0.000 | 0.000 | 4.667 | 4.091 | 0.516 | 0.151 | 0.585 |
| background_nonpocket | 4 | 0.000 | 1.000 | 5.833 | 3.026 | 0.254 | 0.309 | 0.604 |

## Operativ lesning

- `pocket_status`: `compact_low_rare_pocket_supported` fordi 96-lommen ser best ut som et kompakt støttecase med dempet rare-turnover. Samme placement ved growth_seed 202 holder ikke, så placement alene er ikke forklaringen.
- `placement_sufficiency`: `placement_not_sufficient` fordi Placement 3 gir ikke pocket automatisk; growth_seed 202 faller tilbake til diffuse_shell_recurrence.
- `next_step`: `explain_seed_flip_within_p3` fordi Neste steg bør sammenligne growth_seed 101 og 202 direkte innen placement 3, siden det er der pocketen faktisk lever eller dør.

## Tolkning

- Dette er en ren forklaringsrunde pa toppen av v15aw og v15ax, ikke en ny simulering.
- Les dette som en forklaring av den ene `96`-lommen, ikke som en ny stor law for local_swap.
