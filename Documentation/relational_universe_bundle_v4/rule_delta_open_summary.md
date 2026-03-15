# Redusert basis og regelbetingede ΔF-matriser

Dette dokumentet er v0.4-steget i prosjektet. Målet er å erstatte diffuse quasi-invariant-utsagn med en presis analyse av:

1. hvilken feature-basis som er algebraisk uavhengig,
2. hvilke lineære invariants som følger av den valgte regelklassen,
3. hvilke kontekstbetingede motivendringer som kan beregnes eksakt, og
4. hvilke resterende features som må behandles som empiriske makrovariabler.

## Kjøringsparametre

- steps: 4000
- seed: 17
- r_seed: 0.05
- r_token: 1.0
- r_birth: 0.0
- r_death: 0.0
- p_triad: 0.1
- p_del: 0.1
- p_swap: 0.06
- avoid_disconnect: True
- relocate_tokens: True

## Redusert feature-basis

Vi bruker følgende reduserte basis:

`tokens, nodes, components, beta1, wedges, triangles, star3, c4, spectral_radius, clustering, dim_proxy`

Følgende størrelser er eksplisitt tatt ut av basisen fordi de er algebraisk avledbare:

- `edges = beta1 + nodes - components`
- `deg_sq_sum = 2*edges + 2*wedges = 2*(beta1 + nodes - components) + 2*wedges`

# Symbolsk invariantklassifikasjon i kjernebasis

Kjernebasis er `F_core = (tokens, nodes, components, beta1)`.
Her betyr `beta1 = edges - nodes + components` grafens første Betti-tall (uavhengige sykluser).

## Primitive regler og eksakte lineære inkrementer

| regel | Δtokens | Δnodes | Δcomponents | Δbeta1 | merknad |
| --- | ---: | ---: | ---: | ---: | --- |
| seed | 0 | 1 | 0 | 0 | Ny bladnode festes til eksisterende komponent. |
| birth | 1 | 0 | 0 | 0 | Token fødes på eksisterende node. |
| death | -1 | 0 | 0 | 0 | Token dør. |
| triad | 0 | 0 | 0 | 1 | Ny kant legges inn mellom to tidligere ikke-adjiserte noder i samme komponent. |
| delete | 0 | 0 | 0 | -1 | Ikke-bro-kant fjernes i samme komponent. |
| swap | 0 | 0 | 0 | 0 | En kant fjernes og en annen legges inn; lineært ingen endring i kjernebasis. |
| move | 0 | 0 | 0 | 0 | Ren traversering uten topologisk omskriving. |

## Nullrom og eksakte lineære invariants

En lineær kombinasjon `I = c·F_core` er eksakt invariant dersom `ΔF_rule · c = 0` for alle regler i den valgte regelklassen.

### Regelsett: `closed_topological`

Regler: seed, swap

Invariantrommets dimensjon: 3

- -1.0·tokens
- +1.0·components
- +1.0·beta1

### Regelsett: `open_topological`

Regler: seed, triad, delete, swap

Invariantrommets dimensjon: 2

- -1.0·components
- +1.0·tokens

### Regelsett: `fully_open_linear`

Regler: seed, triad, delete, swap, birth, death

Invariantrommets dimensjon: 1

- -1.0·components

## Tolkning

- I `closed_topological` er `tokens`, `components` og `beta1` eksakte lineære invariants i kjernebasis.
- Hvis man i tillegg arbeider i én fast sammenhengende komponent (`components = 1`), reduseres de ikke-trivielle invariantene til `tokens` og `beta1`.
- I `open_topological` bryter `triad/delete` den eksakte bevaringen av `beta1`, men `tokens` består som invariant så lenge token-birth/death er slått av.
- I `fully_open_linear` er det i praksis bare `components` som gjenstår; i en fast sammenhengende komponent forsvinner dermed alle ikke-trivielle lineære invariants i kjernebasis.

Dette er den presise lineære klassifikasjonen som tidligere lå implisitt i diskusjonen.

## Kontekstbetingede eksakte formler i den reduserte motivsektoren

Disse formlene gjelder for features som kan uttrykkes rent kombinatorisk ved lokale grad- og nabostrukturer.
De er ikke antagelser; de er identiteter for de primitive reglene slik de er implementert i simulatoren.

| regel | lokal kontekst | Δwedges | Δtriangles | Δstar3 |
| --- | --- | --- | --- | --- |
| seed | hostgrad h | h | 0 | C(h,2) |
| triad | grader d_v,d_w og felles naboer c | d_v + d_w | c | C(d_v,2)+C(d_w,2) |
| delete | grader d_v,d_u og felles naboer c | -[(d_v-1)+(d_u-1)] | -c | -[C(d_v-1,2)+C(d_u-1,2)] |
| swap | d_u,d_w,c_del,c_add | -(d_u-1)+d_w | -c_del + c_add | -C(d_u-1,2)+C(d_w,2) |

Merk at `c4`, `spectral_radius`, `clustering` og `dim_proxy` ikke har like enkle lokale lukkede formler i denne implementasjonen.
De må derfor analyseres empirisk som regimevariabler eller quasi-invariant-kandidater.

## Hendelsesfordeling

| event | count |
| --- | --- |
| delete | 253 |
| move | 3202 |
| seed | 74 |
| swap | 164 |
| triad | 307 |

## Empirisk regelbetinget middelmatrise i redusert basis

Tabellen under viser middelverdien av `ΔF` per hendelsestype i den reduserte basisen.

| event | tokens | nodes | components | beta1 | wedges | triangles | star3 | c4 | spectral_radius | clustering | dim_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| delete | 0 | 0 | 0 | -1 | -8.221 | -1.269 | -20.29 | -2.779 | -0.09832 | -0.0245 | 0.01601 |
| move | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -0.001358 |
| seed | 0 | 1 | 0 | 0 | 4.189 | 0 | 9.905 | 0 | 0.01916 | -0.01458 | 0.03761 |
| swap | 0 | 0 | 0 | 0 | -0.5183 | -0.6341 | -1.774 | -0.1341 | -0.018 | -0.01532 | 0.02183 |
| triad | 0 | 0 | 0 | 1 | 7.977 | 1.544 | 18.89 | 2.707 | 0.09869 | 0.03274 | -0.003821 |

## Standardisert middelmatrise

Her er de samme radene etter standardisering per feature med global standardavviksskala over hendelsesmatrisen.
Dette gjør det mulig å sammenlikne hvilke regler som dominerer hvilke features uavhengig av enhetsstørrelse.

| event | tokens | nodes | components | beta1 | wedges | triangles | star3 | c4 | spectral_radius | clustering | dim_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| delete | 0 | 0 | 0 | -2.674 | -2.362 | -1.817 | -1.805 | -1.788 | -1.711 | -0.8727 | 0.1068 |
| move | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | -0.009066 |
| seed | 0 | 7.421 | 0 | 0 | 1.204 | 0 | 0.8812 | 0 | 0.3335 | -0.5194 | 0.251 |
| swap | 0 | 0 | 0 | 0 | -0.1489 | -0.9082 | -0.1579 | -0.08633 | -0.3132 | -0.5458 | 0.1457 |
| triad | 0 | 0 | 0 | 2.674 | 2.292 | 2.211 | 1.681 | 1.742 | 1.717 | 1.166 | -0.0255 |

## Nullrom fra teoretiske kjernematriser

### closed_topological

Regler: seed, swap

Invariantbasis:

- -1.000·tokens
- +1.000·components
- +1.000·beta1

### open_topological

Regler: seed, triad, delete, swap

Invariantbasis:

- -1.000·components
- +1.000·tokens

### fully_open_linear

Regler: seed, triad, delete, swap, birth, death

Invariantbasis:

- -1.000·components

## Empirisk kjernematrise for aktive regler i denne kjøringen

| regel | tokens | nodes | components | beta1 |
| --- | --- | --- | --- | --- |
| seed | 0 | 1 | 0 | 0 |
| triad | 0 | 0 | 0 | 1 |
| delete | 0 | 0 | 0 | -1 |
| swap | 0 | 0 | 0 | 0 |

Empirisk nullromsbasis i kjernebasis:

- -1.000·components
- +1.000·tokens

## Residualtest for kontekstbetingede motivformler

Hvis residualene her er null (opp til flyttallsavrunding), bekrefter simulatoren de eksakte lokale formlene for `wedges`, `triangles` og `star3`.

| event | feature | n | mean_abs_residual | max_abs_residual |
| --- | --- | --- | --- | --- |
| seed | wedges | 74 | 0 | 0 |
| seed | triangles | 74 | 0 | 0 |
| seed | star3 | 74 | 0 | 0 |
| triad | wedges | 307 | 0 | 0 |
| triad | triangles | 307 | 0 | 0 |
| triad | star3 | 307 | 0 | 0 |
| delete | wedges | 253 | 0 | 0 |
| delete | triangles | 253 | 0 | 0 |
| delete | star3 | 253 | 0 | 0 |
| swap | wedges | 164 | 0 | 0 |
| swap | triangles | 164 | 0 | 0 |
| swap | star3 | 164 | 0 | 0 |

## Metodologisk status

Dette steget etablerer et presist skille mellom tre nivåer:

1. **Grafidentiteter**: størrelser som ikke bør behandles som uavhengige observabler.
2. **Regelstyrte invariants**: nullrom til de primitive `ΔF`-radene i valgt regelklasse.
3. **Regimevariabler**: `c4`, `spectral_radius`, `clustering`, `dim_proxy` og lignende, som må analyseres empirisk og eventuelt som quasi-invarianter.

Denne sondringen er nødvendig før man kan gå videre til mer modne spørsmål om emergent geometri, effektiv energi og dimensjon.

## Videre arbeid

- Legg til flere lokale motivfeatures og sjekk om de er uavhengige etter identitetsreduksjon.
- Bygg en eksplisitt `Rule`-abstraksjon med analytiske `delta_core`- og `delta_motif`-metoder.
- Koble dette til perturbasjonstester for maksimal propagasjonshastighet og senere til spektral/volumetrisk dimensjon.

_CSV med rå hendelsesdata: `/mnt/data/rule_delta_open_events.csv`_
