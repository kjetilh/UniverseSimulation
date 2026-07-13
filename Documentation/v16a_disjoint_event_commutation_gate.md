# UniverseSimulation v16a: disjoint-event commutation og local-clock gate

Dato: 2026-07-12

## Konklusjon

Gaten ender som `fail_architecture_revision_required`.

Transformasjonsdelen bestod: `7123450` deklarert disjunkte eventpar ble testet, med `0` kommutasjonsfeil og `0` relabel-feil. Dette er et eksakt resultat innen den endelige censusen, ikke en dynamisk ensembleobservasjon.

Scheduler-delen feilet: seed-intensiteten for samme lokale `seed_tid`-descriptor endret seg fra `0.040000` til `0.020000` da ett fjernt token ble lagt til. Den aktive seed-klokken er `r_seed / K` per token, og avhenger derfor av globalt tokenantall. Dagens anchor kan ikke beskrives som bare bounded-support lokale klokker.

Operativt betyr dette: ikke gaa til v16b paa uendret anchor. Redesign seed-klokken eller deklarer den globale seed-scheduleren som en eksplisitt fysisk bakgrunnsstruktur, og rerun v16a.

## Census

- Connected unlabeled graph-atlas graphs: `992`.
- States inklusive alle 1-/2-token placements og fixtures: `33385`.
- Observerte eventtyper: `seed:59999;birth:59999;death:53222;stuck:1;move:189272;delete:183759;triad:231514;swap:231514`.
- Deklarert disjunkte eventpar: `7123450` over `11` aktive-anchor pair-kind-klasser.
- Runtime: `448.433` sekunder.

Graph-atlas-delen bruker alle sammenhengende umerkede grafer med 4--7 noder. Tokenplasseringene er uttommende, men ikke kvotientert videre under grafautomorfier; dette gir redundant dekning heller enn manglende dekning. `seed_node`/`birth_node` og `stuck` dekkes av egne fixtures.

## Hva som ble holdt fast

- Concrete descriptors og event-spesifikke ID-er ble pre-drawn foer rekkefolgen ble variert.
- `e1;e2` og `e2;e1` brukte samme initialtilstand og samme ID-allokering.
- Terminaltilstander ble sammenlignet eksakt og deretter opp til node-isomorfi med token-ID-er bevart.
- Hvert disjunkt par ble ogsaa transportert gjennom en deterministisk node-relabeling.
- Overlappende read/write-support ble logisk ekskludert og kunne ikke bidra til pass.

## Event-support

| event_kind | anchor_active | action_read | action_write | selection_read | bounded_local_clock |
| --- | --- | --- | --- | --- | --- |
| seed | 1.000000 | host node; host token entry for seed_tid | new node; host/new adjacency | global token count or global node count | 0.000000 |
| birth | 1.000000 | host node; parent token entry | new token entry | parent degree | 1.000000 |
| death | 0.000000 | target token entry | target token removal | host degree plus global min_tokens guard | 0.000000 |
| stuck | 1.000000 | token entry; host adjacency | none | host degree | 1.000000 |
| move | 1.000000 | token entry; traversed edge | token location | radius-2 neighborhood | 1.000000 |
| delete | 0.000000 | token; traversed edge; source adjacency | token; edge; optional source node/tokens | radius-2 neighborhood | 1.000000 |
| triad | 0.000000 | token; path v-u-w; absent v-w | token; edge v-w | radius-2 neighborhood | 1.000000 |
| swap | 1.000000 | token; path v-u-w; absent v-w | token; remove v-u; add v-w | radius-2 neighborhood | 1.000000 |

## Kommutasjon

| left_kind | right_kind | declared_disjoint | isomorphic_commutation | relabel_pass | failures |
| --- | --- | --- | --- | --- | --- |
| birth | birth | 166467.000000 | 166467.000000 | 166467.000000 | 0.000000 |
| birth | death | 106444.000000 | 106444.000000 | 106444.000000 | 0.000000 |
| birth | delete | 323630.000000 | 323630.000000 | 323630.000000 | 0.000000 |
| birth | move | 335912.000000 | 335912.000000 | 335912.000000 | 0.000000 |
| birth | seed | 452932.000000 | 452932.000000 | 452932.000000 | 0.000000 |
| birth | stuck | 2.000000 | 2.000000 | 2.000000 | 0.000000 |
| birth | swap | 411048.000000 | 411048.000000 | 411048.000000 | 0.000000 |
| birth | triad | 411048.000000 | 411048.000000 | 411048.000000 | 0.000000 |
| death | death | 26611.000000 | 26611.000000 | 26611.000000 | 0.000000 |
| death | delete | 161815.000000 | 161815.000000 | 161815.000000 | 0.000000 |
| death | move | 167956.000000 | 167956.000000 | 167956.000000 | 0.000000 |
| death | seed | 106444.000000 | 106444.000000 | 106444.000000 | 0.000000 |
| death | swap | 205524.000000 | 205524.000000 | 205524.000000 | 0.000000 |
| death | triad | 205524.000000 | 205524.000000 | 205524.000000 | 0.000000 |
| delete | delete | 103625.000000 | 103625.000000 | 103625.000000 | 0.000000 |
| delete | move | 488748.000000 | 488748.000000 | 488748.000000 | 0.000000 |
| delete | seed | 202014.000000 | 202014.000000 | 202014.000000 | 0.000000 |
| delete | swap | 154296.000000 | 154296.000000 | 154296.000000 | 0.000000 |
| delete | triad | 263316.000000 | 263316.000000 | 263316.000000 | 0.000000 |
| move | move | 281932.000000 | 281932.000000 | 281932.000000 | 0.000000 |
| move | seed | 335912.000000 | 335912.000000 | 335912.000000 | 0.000000 |
| move | swap | 585588.000000 | 585588.000000 | 585588.000000 | 0.000000 |
| move | triad | 663558.000000 | 663558.000000 | 663558.000000 | 0.000000 |
| seed | seed | 79380.000000 | 79380.000000 | 79380.000000 | 0.000000 |
| seed | stuck | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| seed | swap | 203128.000000 | 203128.000000 | 203128.000000 | 0.000000 |
| seed | triad | 255108.000000 | 255108.000000 | 255108.000000 | 0.000000 |
| swap | swap | 38840.000000 | 38840.000000 | 38840.000000 | 0.000000 |
| swap | triad | 198420.000000 | 198420.000000 | 198420.000000 | 0.000000 |
| triad | triad | 188228.000000 | 188228.000000 | 188228.000000 | 0.000000 |

## Hazard-faktorisering

| event_kind | anchor_active | runtime_formula_samples | formula_max_abs_error | formula_exact | bounded_local_clock | status |
| --- | --- | --- | --- | --- | --- | --- |
| seed | 1.000000 | 59999.000000 | 0.000000 | 1.000000 | 0.000000 | fail_active_global_dependency |
| birth | 1.000000 | 59999.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |
| death | 0.000000 | 53222.000000 | 0.000000 | 1.000000 | 0.000000 | inactive_anchor_global_guard |
| stuck | 1.000000 | 1.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |
| move | 1.000000 | 189272.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |
| delete | 0.000000 | 183759.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |
| triad | 0.000000 | 231514.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |
| swap | 1.000000 | 231514.000000 | 0.000000 | 1.000000 | 1.000000 | pass_bounded_local |

Den numeriske formelauditen passerer for alle eventtyper. Det redder ikke seed-lokaliteten: den bekrefter nettopp den eksakte globale normaliseringen `r_seed/K` (eller `r_seed/N` uten tokens).

## Remote-context kontroll

| event_kind | base_intensity | remote_intensity | absolute_difference | remote_invariant | interpretation |
| --- | --- | --- | --- | --- | --- |
| seed | 0.040000 | 0.020000 | 0.020000 | 0.000000 | global_normalization_detected |
| birth | 0.020000 | 0.020000 | 0.000000 | 1.000000 | bounded_local_intensity |
| death | 0.000000 | 0.015000 | 0.015000 | 0.000000 | global_min_tokens_guard_detected |
| move | 0.400000 | 0.400000 | 0.000000 | 1.000000 | bounded_local_intensity |
| delete | 0.200000 | 0.200000 | 0.000000 | 1.000000 | bounded_local_intensity |
| triad | 0.200000 | 0.200000 | 0.000000 | 1.000000 | bounded_local_intensity |
| swap | 0.200000 | 0.200000 | 0.000000 | 1.000000 | bounded_local_intensity |

## Evidensstatus

- Kommutasjonspasset gjelder konkrete transformasjoner under det deklarerte action-support-skjemaet.
- Det er ikke bevis for Lorentz-invarians, diffeomorfisme-invarians eller emergent spacetime.
- Local-clock-feilen er sterkere enn en observabel-null: den er en eksakt arkitekturdiagnose for aktiv seed-scheduling.
- Feilen beviser ikke at relasjonelle universmodeller er umulige. Den krever at dagens anchor endres foer intrinsic causal claims kan testes rent.

## Beslutning

`v16b` er blokkert. Neste smale steg er en seed-clock design gate med minst to eksplisitte alternativer:

1. lokal per-token seed-hazard, slik at total seed-rate skalerer med antall lokale klokker
2. en eksplisitt global seed-prosess som merkes som bakgrunnstid og derfor ikke brukes som grunnlag for observer-uavhengig lokal kausalitet

Alternativ 1 endrer dynamikken og krever ny anchor-kalibrering senere. Alternativ 2 endrer forskningspaastanden. Ingen av dem skal skjules som en liten implementasjonsdetalj.
