# Operativ anbefaling v0.15cj

- `artifact_control`: `clean` fordi Startstorrelsen er ren og alle requested perturbations matcher faktisk perturbasjon.
- `shared_p2_outer_concentration`: `shared_p2_outer_concentration_weak` fordi Outer-occupancy peker svakt mot en delt p2-konsentrasjon (scores add=1/5, swap=3/5), men ikke rent nok ennå.
- `carrier_alignment`: `mixed` fordi Carrier-alignment her betyr bare at p2-vs-p0-gapen peker samme vei i begge carrierne, ikke at alle detaljer er like.
- `next_step`: `flux_or_feeder_observable` fordi Neste steg bor vaere en flux- eller feeder-observabel, ikke mer ren occupancy-oppsummering.

- Les dette som en smal outer-occupancy-observabel ved target 768, ikke som bred fysikktolkning.
