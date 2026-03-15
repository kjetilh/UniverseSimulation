# Perturbasjonslab: closed_chord_v05

## Formål

Dette v0.5-steget undersøker om den lokale relasjonsdynamikken faktisk gir en operasjonell causal cone.
Metoden er å kjøre to kopla replikater med samme stokastiske instruksjonsstrøm og én lokal forskjell i bare den ene.

## Viktig metodisk oppgradering

Tidligere laboratorier brukte et globalt bro-kriterium (`avoid_disconnect`) for å hindre frakobling.
Det kriteriet er ikke strengt lokalt. Denne perturbasjonslaben bruker derfor som standard en renere, lokal regelklasse.

## Kjøringsparametre

- label: closed_chord_v05
- steps: 8000
- seed: 123
- initial_cycle: 10
- initial_tokens: 4
- r_seed: 0.04
- r_token: 1.0
- p_triad: 0.0
- p_del: 0.0
- p_swap: 0.08
- perturbation: add_chord
- center_token_index: 0
- log_every: 50

## Startperturbasjon

```json
{
  "delta_core": {
    "beta1": 1,
    "components": 0,
    "nodes": 0,
    "tokens": 0
  },
  "support": [
    0,
    1,
    2
  ],
  "type": "add_chord",
  "u": 1,
  "v": 0,
  "w": 2
}
```

## Hovedfunn fra denne kjøringen

| metric | value |
| --- | --- |
| final_time | 2008.561102 |
| final_edge_diff_count | 163 |
| final_damaged_nodes_count | 83 |
| final_token_hamming | 4 |
| final_radius_control | 11 |
| final_radius_perturbed | 9 |
| max_radius_control | 13 |
| max_radius_perturbed | 12 |
| final_core_l1 | 1.0 |
| final_regime_l1 | 90.23155 |
| final_delta_beta1 | 1.0 |
| fit_speed_control | 0.005159 |
| fit_speed_perturbed | 0.003066 |
| max_ratio_speed_control | 0.249057 |
| max_ratio_speed_perturbed | 0.249057 |

## Tolking

- `radius_control` og `radius_perturbed` måler hvor langt den observerbare forskjellsmengden strekker seg fra perturbasjonens støtte i de to grenene.
- Hvis disse radiusene vokser langsomt og omtrent lineært i eventtid, har vi en praktisk kandidat til en emergent causal cone.
- Hvis de derimot hopper momentant til store verdier uten lokal mekanisme, er lokaliteten brutt eller målingen dårlig definert.

## Front-hastigheter

- control: max(r/t) = 0.249057, lineær fit-slope = 0.00515939
- perturbed: max(r/t) = 0.249057, lineær fit-slope = 0.00306598

Disse tallene er ikke fundamentale konstanter. De er laboratorie-estimater for effektiv spredningshastighet i denne regelklassen og dette parameterregimet.

## Første treff per radius (control-geometri)

| radius | first_hit_time_control | first_hit_step_control |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 12.0454 | 50 |
| 2 | 12.0454 | 50 |
| 3 | 12.0454 | 50 |
| 4 | 157.476 | 600 |
| 5 | 345.74 | 1350 |
| 6 | 372.595 | 1450 |
| 7 | 542.713 | 2150 |
| 8 | 906.798 | 3600 |

## Event-konsistens mellom grenene

| metric | value |
| --- | --- |
| same_micro_event | 7788 |
| different_micro_event | 212 |
| same_token_index | 425 |
| different_token_index | 7575 |

## Hva som er etablert i dette steget

1. Prosjektet har nå en eksplisitt perturbasjonsmetodikk basert på shared noise / kopla replikater.
2. Lokalitet er renset metodisk ved å flytte analysen til en strengt lokal regelklasse.
3. Causal-cone-spørsmålet er nå flyttet fra metafor til målbart objekt: radius som funksjon av eventtid og makrofeature-drift.

## Begrensninger

- Denne laben holder token-antallet fast. Dermed er shared-SSA-koblingen eksakt fordi den totale raten er den samme i begge grener.
- Hvis token birth/death skal inn igjen, må vi bygge maksimal kobling eller uniformisering for å beholde metodisk kontroll.
- `radius_control` er definert relativt til kontrollgrenenes øyeblikksgeometri; det er operasjonelt nyttig, men ikke eneste mulige definisjon.

## Neste naturlige steg etter denne laben

- Utvid koblingen til birth/death-regimer med uniformisering eller maksimal Poisson-kobling.
- Legg til multikjøringsstatistikk og konfidensintervaller for front-hastighet.
- Knytt causal-cone-estimatet til relativitetsdiskusjonen: når blir denne hastigheten universell over eksitasjoner og regimer?

## Referanser

- D. T. Gillespie, *Exact stochastic simulation of coupled chemical reactions* (1977).
- P. Arrighi og G. Dowek, *Causal graph dynamics* (2013).
- P. Arrighi og S. Martiel, *Quantum causal graph dynamics* (2017).
- B. Martin, *Damage spreading and μ-sensitivity on cellular automata* (2007).
- E. H. Lieb og D. W. Robinson, *The finite group velocity of quantum spin systems* (1972).

_Rå logg: `/mnt/data/perturbation_closed_chord_log.csv`_

_Rå eventdata: `/mnt/data/perturbation_closed_chord_events.csv`_
