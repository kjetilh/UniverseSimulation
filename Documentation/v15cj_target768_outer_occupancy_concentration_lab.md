# Relasjonell universgraf v0.15cj: target-768 outer occupancy concentration lab

## Formal

Denne runden tester om p2 skiller seg fra p0 gjennom mer konsentrert outer-occupancy selv om outer-genealogien forble reseeded i `v15ci`.

## Startstorrelse

| target | mean initial | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 768 | 768.0 | 768.0 | 768.0 | 1 |

## Outer occupancy summary

| profile | outer union | active | entropy | top1 | top3 | top5 | core mass | rare mass | outer dist |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p0 | 137.500 | 0.750 | 0.931 | 0.029 | 0.075 | 0.116 | 0.276 | 0.143 | 5.750 |
| add_chord_p2 | 192.500 | 1.000 | 0.927 | 0.019 | 0.055 | 0.090 | 0.272 | 0.131 | 9.337 |
| local_swap_p0 | 106.000 | 0.992 | 0.906 | 0.058 | 0.174 | 0.268 | 0.326 | 0.219 | 5.882 |
| local_swap_p2 | 117.500 | 0.882 | 0.884 | 0.164 | 0.266 | 0.343 | 0.229 | 0.236 | 9.888 |

## P2 versus P0

| compare | entropy gap | top3 gap | top5 gap | core mass gap | rare mass gap | union gap | distance gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| add_chord_p2_minus_p0 | -0.004 | -0.019 | -0.025 | -0.004 | -0.012 | 55.000 | 3.587 |
| local_swap_p2_minus_p0 | -0.022 | 0.092 | 0.076 | -0.098 | 0.017 | 11.500 | 4.006 |

## Cross-carrier P2 contrast

| compare | entropy gap swap-add | top3 gap add-swap | top5 gap add-swap | core mass gap add-swap | rare mass gap swap-add | union gap swap-add | distance gap swap-add |
| --- | --- | --- | --- | --- | --- | --- | --- |
| local_swap_p2_minus_add_chord_p2 | -0.043 | -0.211 | -0.253 | 0.044 | 0.105 | -75.000 | 0.551 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `shared_p2_outer_concentration`: `shared_p2_outer_concentration_weak` fordi Outer-occupancy peker svakt mot en delt p2-konsentrasjon (scores add=1/5, swap=3/5), men ikke rent nok ennå.
- `carrier_alignment`: `mixed` fordi Carrier-alignment her betyr bare at p2-vs-p0-gapen peker samme vei i begge carrierne, ikke at alle detaljer er like.
- `next_step`: `flux_or_feeder_observable` fordi Neste steg bor vaere en flux- eller feeder-observabel, ikke mer ren occupancy-oppsummering.

## Tolkning

- Dette er en ny p2-observabel innen samme target-768-spor, ikke et nytt skalahopp.
- Positivt signal her betyr at p2 holder outer-halen på færre og tyngre noder, ikke at vi har funnet en partikkel.
