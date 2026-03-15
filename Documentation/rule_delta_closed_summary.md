# Rule-delta lab v0.4

## Metode

Denne rapporten skiller eksplisitt mellom:

1. algebraiske identiteter i feature-rommet,
2. eksakte lineære invariants som følger av primitive regler,
3. og numeriske observasjoner i en konkret kjøring.

## Kjøringsparametre

- steps: 1200
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

## Algebraiske identiteter

- `beta1 = edges - nodes + components`
- `deg_sq_sum = 2*wedges + 2*edges`

Herfra følger at `edges` og `deg_sq_sum` ikke skal behandles som uavhengige dynamiske observabler i den reduserte basisen.

## Teorem og identiteter

### Primitive regler og eksakte lineære inkrementer i kjernebasis

| regel | Δtokens | Δnodes | Δcomponents | Δbeta1 | merknad |
| --- | --- | --- | --- | --- | --- |
| seed | 0 | 1 | 0 | 0 | Ny bladnode festes til eksisterende komponent. |
| birth | 1 | 0 | 0 | 0 | Token fødes på eksisterende node. |
| death | -1 | 0 | 0 | 0 | Token dør. |
| triad | 0 | 0 | 0 | 1 | Ny intern kant opprettes i samme komponent. |
| delete | 0 | 0 | 0 | -1 | Ikke-bro-kant fjernes i samme komponent. |
| swap | 0 | 0 | 0 | 0 | En kant fjernes og en annen legges inn lokalt. |
| move | 0 | 0 | 0 | 0 | Ren traversering uten omskriving. |

En lineær kombinasjon `I = c·F_core` er eksakt invariant dersom `ΔF_rule · c = 0` for alle regler i den valgte regelklassen.

### Regelsett: `closed_topological`

Regler: seed, swap

Invariantrommets dimensjon: 3

- -1.000·tokens
- +1.000·components
- +1.000·beta1

### Regelsett: `open_topological`

Regler: seed, triad, delete, swap

Invariantrommets dimensjon: 2

- -1.000·components
- +1.000·tokens

### Regelsett: `fully_open_linear`

Regler: seed, triad, delete, swap, birth, death

Invariantrommets dimensjon: 1

- -1.000·components

### Eksakte motivformler

Formlene under er lokale identiteter for dagens implementasjon. De er ikke numeriske estimater.

| regel | Δwedges | Δtriangles | Δstar3 |
| --- | --- | --- | --- |
| seed | h | 0 | C(h,2) |
| triad | d_v + d_w | c | C(d_v,2) + C(d_w,2) |
| delete | -[(d_v-1)+(d_u-1)] | -c | -[C(d_v-1,2)+C(d_u-1,2)] |
| swap | -(d_u-1)+d_w | -c_del + (c_add - 1) | -C(d_u-1,2)+C(d_w,2) |

Merk spesielt at `swap` gir `Δtriangles = -c_del + (c_add - 1)`. `-1`-leddet kommer av at den nye kanten `(source, target)` deler destinasjonsnoden som felles nabo før den gamle kanten fjernes.

## Numeriske observasjoner

### Hendelsesfordeling

| event | count |
| --- | --- |
| move | 1152 |
| seed | 14 |
| swap | 34 |

### Empirisk middelmatrise i redusert basis

| event | tokens | nodes | components | beta1 | wedges | triangles | star3 | c4 | spectral_radius | clustering | dim_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| move | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| seed | 0 | 1 | 0 | 0 | 2.5 | 0 | 2.5 | 0 | 0.05012 | -0.001488 | 0.05242 |
| swap | 0 | 0 | 0 | 0 | -0.02941 | 0 | 0 | 0 | -0.0005624 | 0.0006127 | -0.004675 |

### Standardisert middelmatrise

Denne tabellen er z-skalert per feature over hele hendelsesmatrisen. Den skal brukes til å kontrollere for rene skalaeffekter.

| event | tokens | nodes | components | beta1 | wedges | triangles | star3 | c4 | spectral_radius | clustering | dim_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| move | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| seed | 0 | 9.313 | 0 | 0 | 6.048 | 0 | 3.627 | 0 | 2.187 | -0.09669 | 4.522 |
| swap | 0 | 0 | 0 | 0 | -0.07115 | 0 | 0 | 0 | -0.02454 | 0.03981 | -0.4033 |

### Empirisk kjernebasis for aktive regler

| regel | tokens | nodes | components | beta1 |
| --- | --- | --- | --- | --- |
| seed | 0 | 1 | 0 | 0 |
| swap | 0 | 0 | 0 | 0 |

Empirisk nullromsbasis:

- -1.000·tokens
- +1.000·components
- +1.000·beta1

### Residualtest for eksakte motivformler

| event | feature | n | mean_abs_residual | max_abs_residual |
| --- | --- | --- | --- | --- |
| seed | wedges | 14 | 0 | 0 |
| seed | triangles | 14 | 0 | 0 |
| seed | star3 | 14 | 0 | 0 |
| triad | wedges | 0 | nan | nan |
| triad | triangles | 0 | nan | nan |
| triad | star3 | 0 | nan | nan |
| delete | wedges | 0 | nan | nan |
| delete | triangles | 0 | nan | nan |
| delete | star3 | 0 | nan | nan |
| swap | wedges | 34 | 0 | 0 |
| swap | triangles | 34 | 0 | 0 |
| swap | star3 | 34 | 0 | 0 |

## Tolkning

### Teorem/identitet

- Redusert basis kvotienterer ut de to innebygde grafidentitetene.
- Nullrommene i kjernebasis er eksakte utsagn om primitive regelklasser, ikke data-tilpassede observasjoner.

### Numerisk observasjon

- De empiriske middelmatrisene viser hvilke features som faktisk driver i denne konkrete parameterkonteksten.
- Standardisert analyse skiller stor absolutt skala fra robust strukturell dominans.

### Spekulativ fortolkning

- `c4`, `spectral_radius`, `clustering` og `dim_proxy` er fortsatt regimevariabler. De kan bli quasi-invarianter i bestemte regimer, men det følger ikke av reglene alene.

## Videre arbeid

- Knytt regelobjektene til en eksplisitt perturbasjonslab med kopla kjøringer.
- Mål causal-cone-lignende spredning i grafdistanse og hendelsestid.

_CSV med rå hendelsesdata: `Documentation/rule_delta_closed_events.csv`_
