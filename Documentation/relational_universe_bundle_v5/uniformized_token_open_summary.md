# Uniformized coupling lab: token_open_moderate

## Formål

Dette v0.6-steget utvider kausalitetslaben til åpne regimer der token-antallet kan endre seg.
I v0.5 var en eksakt felles Gillespie-klokke bare ren når token-antallet var identisk og konstant i begge grener.
I v0.6 bruker vi i stedet en dominerende felles potensial-hendelsesprosess og familywise thinning.

## Kjøringsparametre

- steps: 10000
- seed: 7
- initial_cycle: 8
- initial_tokens: 4
- r_seed: 0.04
- r_token: 1.0
- r_birth: 0.01
- r_death: 0.009
- p_triad: 0.0
- p_del: 0.0
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
    3,
    4,
    5
  ],
  "type": "local_swap"
}
```

## Hovedfunn fra kjøringen

| metric | value |
| --- | --- |
| final_t | 161.1893702914851 |
| final_radius_control | 4 |
| final_radius_perturbed | 3 |
| max_radius_control | 5 |
| max_radius_perturbed | 7 |
| final_edge_diff_count | 28 |
| final_damaged_nodes_count | 19 |
| final_delta_tokens | 33.0 |
| final_delta_beta1 | 0.0 |
| final_core_l1 | 33.0 |
| final_regime_l1 | 60.55516671145679 |
| fit_speed_control | 0.0019861109149297805 |
| both_accept_total | 8935 |
| one_sided_total | 1065 |
| null_total | 0 |

## Kvalitet på koblingen

- totale potensial-hendelser: 10000
- begge aksepterte: 8935
- ensidige aksepter: 1065
- dobbelt-null: 0

| family | potential | both_accept | one_sided | null |
| --- | --- | --- | --- | --- |
| seed | 11 | 11 | 0 | 0 |
| token | 9718 | 8698 | 1020 | 0 |
| birth | 245 | 200 | 45 | 0 |
| death | 26 | 26 | 0 | 0 |

## Front-hastigheter

- control: max(r/t) = 0.22106, lineær fit-slope = 0.00198611
- perturbed: max(r/t) = 0.22106, lineær fit-slope = 0.0071567

## Første treff per radius

| radius | first_hit_time_control |
| --- | --- |
| 0 | 0 |
| 1 | 12.4055 |
| 2 | 12.4055 |
| 3 | 18.0947 |
| 4 | 18.0947 |
| 5 | 53.4792 |
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

_Rå logg: `/mnt/data/uniformized_token_open_log.csv`_

_Rå eventdata: `/mnt/data/uniformized_token_open_events.csv`_
