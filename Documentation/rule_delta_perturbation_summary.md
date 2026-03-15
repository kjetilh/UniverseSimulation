# Perturbation Lab

## Metode

To simuleringer startes fra samme warmup-tilstand og drives deretter av samme semantiske RNG-strøm.
En ekstra lokal omskriving settes inn bare i den perturberte kopien før den kopla kjøringen starter.

## Eksakte antagelser

- Samme event-indeks bruker samme RNG-nøkler i begge kjøringer.
- Perturbasjonen er lokal og følger en eksisterende primitiv regel.
- `spread_radius` måles som største grafdistanse fra perturbasjonens initiale support til de noder som fortsatt er forskjellige.

## Kjøringsparametre

- steps: 1000
- warmup_steps: 250
- seed: 19
- perturbation: auto
- actual_perturbation: triad
- support_nodes: 4, 6, 12

## Numeriske observasjoner

- max_spread_radius: 4
- final_spread_radius: 3
- final_c_star_event: 1
- final_c_star_time: 4.12986

### Første treff per radius

- radius 0: event 1
- radius 1: event 3
- radius 2: event 50
- radius 3: event 102
- radius 4: event 557

### Tolkning

#### Teorem/identitet

- Den delte RNG-strømmen betyr at observerte avvik skyldes tilstandsavhengighet etter perturbasjonen, ikke ulik ekstern støy.

#### Numerisk observasjon

- `c_star_event` og `c_star_time` er empiriske overkanter i denne kjøringen, ikke universelle konstanter.

#### Spekulativ fortolkning

- Hvis `spread_radius` vokser lineært over mange kjøringer og regimer, kan dette tolkes som en effektiv causal-cone-lignende front i universgrafen.

_CSV med rå perturbasjonsdata: `Documentation/rule_delta_perturbation_events.csv`_
