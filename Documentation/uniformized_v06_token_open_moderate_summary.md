# Uniformized coupling lab: codex_v06_token_open_moderate

## Formål

Dette v0.6-steget utvider kausalitetslaben til åpne regimer der token-antallet kan endre seg.
I v0.5 var en eksakt felles Gillespie-klokke bare ren når token-antallet var identisk og konstant i begge grener.
I v0.6 bruker vi i stedet en dominerende felles potensial-hendelsesprosess og familywise thinning.

## Kjøringsparametre

- steps: 3000
- seed: 321
- initial_cycle: 10
- initial_tokens: 4
- r_seed: 0.04
- r_token: 1.0
- r_birth: 0.05
- r_death: 0.05
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
    2,
    3,
    4
  ],
  "type": "local_swap"
}
```

## Hovedfunn fra kjøringen

| metric | value |
| --- | --- |
| final_t | 41.54183224459296 |
| final_radius_control | 3 |
| final_radius_perturbed | 4 |
| max_radius_control | 4 |
| max_radius_perturbed | 5 |
| final_edge_diff_count | 8 |
| final_damaged_nodes_count | 10 |
| final_delta_tokens | 5.0 |
| final_delta_beta1 | 0.0 |
| final_core_l1 | 5.0 |
| final_regime_l1 | 8.385110648305394 |
| fit_speed_control | -0.014655249091075146 |
| both_accept_total | 2887 |
| one_sided_total | 113 |
| null_total | 0 |

## Kvalitet på koblingen

- totale potensial-hendelser: 3000
- begge aksepterte: 2887
- ensidige aksepter: 113
- dobbelt-null: 0

| family | potential | both_accept | one_sided | null |
| --- | --- | --- | --- | --- |
| seed | 0 | 0 | 0 | 0 |
| token | 2664 | 2572 | 92 | 0 |
| birth | 290 | 269 | 21 | 0 |
| death | 46 | 46 | 0 | 0 |

## Front-hastigheter

- control: max(r/t) = 0.313834, lineær fit-slope = -0.0146552
- perturbed: max(r/t) = 0.337299, lineær fit-slope = -0.0173155

## Første treff per radius

| radius | first_hit_time_control |
| --- | --- |
| 0 | 0 |
| 1 | 6.37281 |
| 2 | 6.37281 |
| 3 | 9.98886 |
| 4 | 25.9002 |
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

_Rå logg: `Documentation/uniformized_v06_token_open_moderate_log.csv`_

_Rå eventdata: `Documentation/uniformized_v06_token_open_moderate_events.csv`_
