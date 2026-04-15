# Relasjonell universgraf v0.15az: local_swap p3 seed-flip explainer

## Formål

Denne runden forklarer hvorfor `placement 3` ved `target 96` holder som en liten core+shell-lomme ved `growth_seed 101`, men ikke ved `growth_seed 202`.

## Case rows

| role | growth_seed | placement | label | support | ball3/ball1 | core/ball1 | tail/ball1 | core/shell | rare share | coarse return |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| context_control | 101 | 0 | diffuse_shell_recurrence | 9,15,58 | 3.727 | 2.818 | 4.382 | 0.795 | 0.205 | 0.677 |
| context_control | 101 | 1 | mixed_core_shell | 0,1,12 | 3.000 | 2.188 | 3.358 | 0.897 | 0.149 | 0.615 |
| context_control | 101 | 2 | diffuse_shell_recurrence | 0,1,70 | 3.083 | 1.167 | 2.528 | 0.400 | 0.329 | 0.446 |
| p3_pocket_anchor | 101 | 3 | stable_core_variable_shell | 4,5,16 | 2.600 | 3.267 | 4.047 | 1.960 | 0.149 | 0.785 |
| high_amplification_nonpocket | 202 | 0 | mixed_core_shell | 8,10,64 | 4.091 | 4.364 | 5.705 | 1.548 | 0.151 | 0.585 |
| context_control | 202 | 1 | diffuse_shell_recurrence | 6,7,18 | 2.722 | 1.389 | 2.108 | 0.893 | 0.274 | 0.846 |
| context_control | 202 | 2 | diffuse_shell_recurrence | 6,7,8 | 2.571 | 0.476 | 1.238 | 0.294 | 0.429 | 0.446 |
| p3_diffuse_flip | 202 | 3 | diffuse_shell_recurrence | 0,13,39 | 2.786 | 0.571 | 1.136 | 0.500 | 0.333 | 0.631 |

## Role summary

| role | n | stable core+shell | diffuse shell | mean ball3/ball1 | mean core/ball1 | mean tail/ball1 | mean core/shell | mean rare share | mean coarse return |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| p3_pocket_anchor | 1 | 1.000 | 0.000 | 2.600 | 3.267 | 4.047 | 1.960 | 0.149 | 0.785 |
| p3_diffuse_flip | 1 | 0.000 | 1.000 | 2.786 | 0.571 | 1.136 | 0.500 | 0.333 | 0.631 |
| high_amplification_nonpocket | 1 | 0.000 | 0.000 | 4.091 | 4.364 | 5.705 | 1.548 | 0.151 | 0.585 |
| context_control | 5 | 0.000 | 0.800 | 3.021 | 1.607 | 2.723 | 0.656 | 0.277 | 0.606 |

## Operativ lesning

- `seed_flip_status`: `p3_seed_flip_is_core_amplification_flip` fordi De to p3-casene ligger relativt naert i kompakthetsgeometri, men skiller lag hardt i hvor mye støtteområdet faktisk blåses opp til stor, vedvarende kjerne og hale.
- `amplification_scope`: `amplification_not_sufficient_globally` fordi Det finnes minst ett ikke-pocket-case med enda høyere core-forsterkning, så forsterkning alene er ikke en full forklaring.
- `next_step`: `explain_why_202_p3_stays_compressed` fordi Neste steg bør forklare hva som holder `202/p3` komprimert, siden placement-geometrien alene ikke gjør jobben.

## Tolkning

- Dette er en ren forklaringsrunde pa toppen av v15aw-v15ay, ikke en ny simulering.
- Les dette som en forklaring av seed-flippen inne i `p3`, ikke som en ny generell lov for local_swap.
