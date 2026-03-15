# Redusert basis og regelbetingede ΔF-matriser

Dette dokumentet er v0.4-steget i prosjektet. Målet er å erstatte diffuse quasi-invariant-utsagn med en presis analyse av:

1. hvilken feature-basis som er algebraisk uavhengig,
2. hvilke lineære invariants som følger av den valgte regelklassen,
3. hvilke kontekstbetingede motivendringer som kan beregnes eksakt, og
4. hvilke resterende features som må behandles som empiriske makrovariabler.

## Kjøringsparametre

- steps: 6000
- seed: 17
- r_seed: 0.05
- r_token: 1.0
- r_birth: 0.0
- r_death: 0.0
- p_triad: 0.0
- p_del: 0.0
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
| move | 5870 |
| seed | 67 |
| swap | 63 |

## Empirisk regelbetinget middelmatrise i redusert basis

Tabellen under viser middelverdien av `ΔF` per hendelsestype i den reduserte basisen.

| event | tokens | nodes | components | beta1 | wedges | triangles | star3 | c4 | spectral_radius | clustering | dim_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| move | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0005489 |
| seed | 0 | 1 | 0 | 0 | 3.97 | 0 | 12.3 | 0 | 0.02944 | -0.001436 | 0.0183 |
| swap | 0 | 0 | 0 | 0 | -0.746 | 0 | -4.778 | 0 | -0.0006093 | 0.001527 | -0.02164 |

## Standardisert middelmatrise

Her er de samme radene etter standardisering per feature med global standardavviksskala over hendelsesmatrisen.
Dette gjør det mulig å sammenlikne hvilke regler som dominerer hvilke features uavhengig av enhetsstørrelse.

| event | tokens | nodes | components | beta1 | wedges | triangles | star3 | c4 | spectral_radius | clustering | dim_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| move | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.003636 |
| seed | 0 | 9.516 | 0 | 0 | 5.314 | 0 | 3.258 | 0 | 1.303 | -0.2349 | 0.1212 |
| swap | 0 | 0 | 0 | 0 | -0.9986 | 0 | -1.266 | 0 | -0.02697 | 0.2498 | -0.1433 |

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
| swap | 0 | 0 | 0 | 0 |

Empirisk nullromsbasis i kjernebasis:

- -1.000·tokens
- +1.000·components
- +1.000·beta1

## Residualtest for kontekstbetingede motivformler

Hvis residualene her er null (opp til flyttallsavrunding), bekrefter simulatoren de eksakte lokale formlene for `wedges`, `triangles` og `star3`.

| event | feature | n | mean_abs_residual | max_abs_residual |
| --- | --- | --- | --- | --- |
| seed | wedges | 67 | 0 | 0 |
| seed | triangles | 67 | 0 | 0 |
| seed | star3 | 67 | 0 | 0 |
| triad | wedges | 0 | nan | nan |
| triad | triangles | 0 | nan | nan |
| triad | star3 | 0 | nan | nan |
| delete | wedges | 0 | nan | nan |
| delete | triangles | 0 | nan | nan |
| delete | star3 | 0 | nan | nan |
| swap | wedges | 63 | 0 | 0 |
| swap | triangles | 63 | 0 | 0 |
| swap | star3 | 63 | 0 | 0 |

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

_CSV med rå hendelsesdata: `/mnt/data/rule_delta_closed_events.csv`_
