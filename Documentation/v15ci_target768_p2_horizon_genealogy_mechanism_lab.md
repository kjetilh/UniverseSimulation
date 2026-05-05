# Relasjonell universgraf v0.15ci: target-768 p2 horizon genealogy mechanism lab

## Formal

Denne runden tester om den delte p2-horisonten ved target `768` best leses som en vedvarende ytre grein eller som gjentatt outer re-seeding.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 768 | 768.0 | 768.0 | 768.0 | 1 |

## Profile summary

| profile | dominant mech | persistent | reseeded | mixed | probe | active | dominant presence | dominant mass | lateborn mass | turnover | reactivation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | reseeded_outer_horizon | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.184 | 0.477 | 2.291 | 0.000 |
| add_chord_p2 | reseeded_outer_horizon | 0.250 | 0.750 | 0.000 | 0.000 | 1.000 | 0.733 | 0.529 | 0.490 | 0.981 | 0.000 |
| local_swap_p0 | reseeded_outer_horizon | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 0.202 | 0.466 | 1.891 | 0.000 |
| local_swap_p2 | reseeded_outer_horizon | 0.000 | 1.000 | 0.000 | 0.000 | 1.000 | 0.994 | 0.490 | 0.433 | 1.324 | 0.000 |

## P2 versus P0

| compare | active gap | persistent gap | reseeded gap | dominant presence gap | dominant mass gap | lateborn gap | turnover gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p2_minus_p0 | 0.000 | 0.250 | -0.250 | -0.267 | 0.345 | 0.013 | -1.310 |
| local_swap_p2_minus_p0 | 0.000 | 0.000 | 0.000 | -0.006 | 0.288 | -0.033 | -0.568 |

## Cross-carrier P2 contrast

| compare | active gap | persistent gap | reseeded gap | dominant presence gap | dominant mass gap | lateborn gap | turnover gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| local_swap_p2_minus_add_chord_p2 | 0.000 | -0.250 | 0.250 | 0.262 | -0.039 | -0.057 | 0.343 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `shared_p2_horizon_mechanism`: `shared_p2_horizon_mechanism_not_yet` fordi Outer-genealogien er ikke sterk nok til aa gi en ren delt p2-mekanismefortelling ennå.
- `carrier_alignment`: `aligned` fordi Dominant mekanikk ved p2 er add_chord=reseeded_outer_horizon, local_swap=reseeded_outer_horizon.
- `next_step`: `new_p2_observable` fordi Neste steg bor vaere en annen p2-observabel, ikke mer av samme genealogiklasse.

## Tolkning

- Dette er en smal mekanismerunde rundt p2-lommen ved target `768`, ikke et nytt bredt target-sok.
- Positivt signal her betyr bare at outer-genealogien bærer repeterbar informasjon om hvordan horisonten holdes oppe.
- Ingen av disse labelene skal leses som partikler eller universell geometri.
