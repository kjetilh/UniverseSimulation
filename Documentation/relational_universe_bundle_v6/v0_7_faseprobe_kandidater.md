# v0.7 faseprobe – kandidater før v0.8

Dette notatet trekker ut de mest lovende parameterpunktene fra faseproben.

## Mest lovende overlap-/repair-kandidater

| r_birth | r_death | p_swap | p_triad | p_del | mean_overlap | same_descriptor | unequal_time | shared_token_frac | final_radius |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.05 | 0.00 | 0.04 | 0.00 | 0.00 | 0.199 | 0.198 | 29.734 | 0.436 | 2.333 |
| 0.05 | 0.00 | 0.04 | 0.03 | 0.00 | 0.185 | 0.186 | 22.837 | 0.493 | 1.500 |
| 0.05 | 0.05 | 0.04 | 0.00 | 0.00 | 0.181 | 0.195 | 31.551 | 0.373 | 2.167 |

## Første tolkning
Det ser ut som om et regime med:
- moderat `birth`,
- svak eller moderat `death`,
- lav til moderat `swap`,
- og svært liten `triad`

gir de beste tegnene til å kombinere:
- høy lokal overlap,
- moderat eller lav unequal time,
- og relativt liten slutt-radius.

## Hva dette innebærer
Dette er fortsatt ikke et ferdig fasekart, men det er nok til å styre v0.8. I stedet for å skanne hele parameterrommet blindt, kan vi starte der disse indikatorene allerede ser lovende ut.