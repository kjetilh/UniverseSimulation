# Relasjonell universgraf v0.15ca: target-192 radial occupancy mechanism lab

## Formal

Denne runden bruker en ny observabelklasse: radial occupancy-fordeling rundt perturbasjonssupport.
Sporsmalet er om p1/p2-grensen ved target 192 faktisk ser ut som en radial/rare/distributed overgang.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 192 | 192.0 | 192.0 | 192.0 | 1 |

## Aggregert radial occupancy

| profile | coarse | occ entropy | participation | mean dist | shell4+ | rare mass | spectral rel |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p1 | 0.810 | 0.954 | 97.683 | 4.340 | 0.578 | 0.049 | 0.020 |
| add_chord_p2 | 0.829 | 0.953 | 106.097 | 3.906 | 0.456 | 0.041 | 0.020 |
| local_swap_p1 | 0.913 | 0.953 | 112.220 | 5.177 | 0.685 | 0.048 | 0.022 |
| local_swap_p2 | 0.930 | 0.965 | 129.752 | 5.075 | 0.636 | 0.024 | 0.022 |

## P2 minus P1

| perturbation | mean dist gap | shell4+ gap | shell entropy gap | participation gap | rare mass gap | spectral rel gap |
| --- | --- | --- | --- | --- | --- | --- |
| add_chord | -0.434 | -0.122 | 0.098 | 8.414 | -0.008 | -0.000 |
| local_swap | -0.103 | -0.049 | 0.062 | 17.532 | -0.024 | -0.001 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `radial_mechanism`: `radial_diffuse_boundary_not_yet` fordi Den nye radial occupancy-observabelen forklarer ikke p1/p2-grensen rent.
- `next_step`: `target384_or_new_mechanism` fordi Neste steg bor vaere target 384 eller en annen mekanismeobservabel, ikke mer av samme p1/p2-runde.

## Tolkning

- Dette er en mekanismeobservabel, ikke en ny family-label-runde.
- Positivt signal her betyr at p2 virkelig ligger lenger ute og mer distribuert enn p1, ikke bare at labelene er forskjellige.
