# Uniformized coupling lab: full_open_moderate

## Formål

Dette v0.6-steget utvider kausalitetslaben til åpne regimer der token-antallet kan endre seg.
I v0.5 var en eksakt felles Gillespie-klokke bare ren når token-antallet var identisk og konstant i begge grener.
I v0.6 bruker vi i stedet en dominerende felles potensial-hendelsesprosess og familywise thinning.

## Kjøringsparametre

- steps: 10000
- seed: 9
- initial_cycle: 8
- initial_tokens: 4
- r_seed: 0.04
- r_token: 1.0
- r_birth: 0.01
- r_death: 0.009
- p_triad: 0.05
- p_del: 0.03
- p_swap: 0.08
- min_tokens: 1
- perturbation: local_swap
- center_token_index: 0

## Startperturbasjon

```json
{
  "delta_core": {
    "beta1": 0,
    "components": 0,
    "nodes": 0,
    "tokens": 0
  },
  "support": [
    0,
    1,
    7
  ],
  "type": "local_swap"
}
```

## Hovedfunn fra kjøringen

| metric | value |
| --- | --- |
| final_t | 105.83603119038649 |
| final_radius_control | 2 |
| final_radius_perturbed | 2 |
| max_radius_control | 3 |
| max_radius_perturbed | 3 |
| final_edge_diff_count | 45 |
| final_damaged_nodes_count | 14 |
| final_delta_tokens | 119.0 |
| final_delta_beta1 | -1.0 |
| final_core_l1 | 120.0 |
| final_regime_l1 | 351.6246142550703 |
| fit_speed_control | -0.010218178179624981 |
| both_accept_total | 7852 |
| one_sided_total | 2148 |
| null_total | 0 |

## Kvalitet på koblingen

- totale potensial-hendelser: 10000
- begge aksepterte: 7852
- ensidige aksepter: 2148
- dobbelt-null: 0

| family | potential | both_accept | one_sided | null |
| --- | --- | --- | --- | --- |
| seed | 6 | 6 | 0 | 0 |
| token | 9475 | 7448 | 2027 | 0 |
| birth | 508 | 388 | 120 | 0 |
| death | 11 | 10 | 1 | 0 |

## Front-hastigheter

- control: max(r/t) = 0.258889, lineær fit-slope = -0.0102182
- perturbed: max(r/t) = 0.388334, lineær fit-slope = -0.0109391

## Første treff per radius

| radius | first_hit_time_control |
| --- | --- |
| 0 | 0 |
| 1 | 7.72532 |
| 2 | 7.72532 |
| 3 | 13.5288 |
| 4 | NA |
| 5 | NA |
| 6 | NA |
| 7 | NA |
| 8 | NA |

## Tolkning

Familywise uniformization gjør det mulig å beholde én delt potensial-klokke selv når totalratene i de to grenene er ulike.
Dermed kan vi skille mellom virkelig kausal spredning og ren klokke-deskronisering.

I åpne regimer er det fortsatt mulig at forskjeller i tokens, noder eller topologi vokser raskt.
Poenget i v0.6 er ikke å bevise universell causal cone én gang for alle, men å gjøre testen metodisk legitim i de regimene der v0.5 ikke lenger var tilstrekkelig.

## Hva som er nytt i dette steget

1. Token birth/death er nå eksplisitt inne i perturbasjonslaben.
2. Eventtid er koblet via en dominerende felles potensial-hendelsesstrøm.
3. Familywise thinning og felles uniforms gir maksimal samsvar på aksept-beslutningen for hver valgt familie.
4. Node- og token-id-er bevares over grenene når hendelser deles, slik at divergens kan måles meningsfullt.

## Begrensninger

- Koblingen er eksakt på familywise-rate-nivå, men ikke nødvendigvis maksimal for hele den lokale overgangskjernen.
- Rank-kobling for lokale valg er enkel og robust, men ikke den eneste mulige eller nødvendigvis optimale koblingen.
- Vi må senere undersøke om front-hastighet blir robust under andre lokale koblingsvalg.

## Neste naturlige steg

- Bygg en mer finmasket maksimal kobling for lokale overganger innen hver familie.
- Studer om det finnes en stabil overgrense for front-hastighet over et større parameterrom.
- Koble v0.6-laben til dimensjons- og energidiskusjonen: er det de samme regimene som gir quasi-invariants, stabil geometri og begrenset spredning?

_Rå logg: `/mnt/data/uniformized_full_open_log.csv`_

_Rå eventdata: `/mnt/data/uniformized_full_open_events.csv`_
