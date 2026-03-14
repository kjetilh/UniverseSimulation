# Feature Lab: Quasi-invariant Study Across Three Regimes

Dette notatet dokumenterer en konkret bruk av `relational_universe_feature_lab.py` for a skille:
- implementerte regler
- malte features
- algebraiske identiteter
- ekte dynamiske invariants
- og kandidater til quasi-invariants

Alle regimer er kjort med baade ra og standardisert SVD-basert analyse. Det er viktig fordi feature-skalaene er veldig ulike, og en ra SVD ellers kan forveksle liten numerisk skala med "nesten bevaring".

## 1. Hva feature-labben faktisk implementerer

Labben har fire eventkanaler:
- `seed`: legger til en ny leaf-node pa en eksisterende vert
- `token`: lar ett token traversere en kant og utlose en lokal rewrite
- `birth`: legger til et nytt token pa en tilfeldig node
- `death`: fjerner et tilfeldig token

Inne i `token_event()` finnes tre rewrite-regler:
- `delete`: sletter den traverserte kanten, eventuelt bare hvis den ikke er bridge
- `triad`: lukker en triangel ved a legge til en ny kant `v-w`
- `swap`: fjerner `v-u` og legger til `v-w`, altsa en lokal edge-swap

Dette betyr at modellen faktisk blander:
- volumtilvekst via `seed`
- action-budsjett via `tokens`
- topologisk omkobling via `swap`
- loop-produksjon via `triad`
- og loop-tapping / strukturbrudd via `delete`

## 2. Features som males, og fysisk lesning

| feature | grafteknisk betydning | fysisk lesning |
| --- | --- | --- |
| `tokens` | antall mobile agenter | action-budsjett eller eksitasjonsinnhold |
| `nodes` | antall noder | volum / antall operative relasjonelle steder |
| `edges` | antall kanter | total relasjonstetthet |
| `components` | antall sammenhengskomponenter | antall operasjonelt frakoblede sektorer |
| `beta1` | `edges - nodes + components` | loop-rang / topologisk ladning |
| `wedges` | antall lengde-2 stier med felles sentrum | lokal forgrening / pre-triangelstruktur |
| `triangles` | antall 3-sykluser | lokal lukking, klynge eller "eksitasjonskjerner" |
| `star3` | antall 3-stjerner | sterk lokal hubbing / gradkonsentrasjon |
| `c4` | antall 4-sykluser | mer utstrakte lukkede sloyer enn triangler |
| `deg_sq_sum` | sum av grad^2 | samlet gradheterogenitet |
| `spectral_radius` | storste egenverdi til adjakensmatrisen | global koblingsstyrke / kollektiv tetthet |
| `clustering` | omtrentlig lokal clustering | hvor triadisk lukket nabolagene er |
| `dim_proxy` | volumvekst-basert dimensjonsproxy | grov, emergent geometrisk dimensjon |

Fysisk viktig poeng: ikke alle disse er gode kandidater til "energi". Noen er ren topologi, noen er lokal motivstruktur, og noen er bare koordinerte beskrivelser av den samme graden eller tettheten.

## 3. Algebraiske identiteter som alltid gjelder

To identiteter er eksakte i alle tre regimer og folger direkte av definisjonene:

1. `beta1 = edges - nodes + components`
2. `deg_sq_sum = 2*wedges + 2*edges`

Konsekvensen er metodologisk viktig:
- hvis SVD finner nesten-nullretninger dominert av `nodes`, `edges`, `components`, `beta1`, er dette ofte bare Betti-identiteten
- hvis den finner nullretninger dominert av `wedges`, `edges`, `deg_sq_sum`, er dette ofte bare grad/wedge-identiteten

Derfor ma disse identitetene faktoriseres ut for man kaller noe en quasi-invariant.

## 4. Regimer og funn

## 4.1 Closed topological sector

Kilder:
- `feature_lab_regimes/closed_topological_sector.csv`
- `feature_lab_regimes/closed_topological_sector_auto.md`
- `feature_lab_regimes/closed_topological_sector_summary.md`

Funn:
- `tokens`, `nodes`, `edges`, `components` og `beta1` er eksakte dynamiske invariants i dette regimet.
- Dette er ikke bare algebra; det folger av at bare bridge-frie edge-swaps er tillatt, mens seed/birth/death er skrudd av.
- Etter at disse invariantene er tatt ut, ser jeg ingen sterk ny quasi-invariant. Motif-sektoren fluktuerer fortsatt.

Lesning:
- spacetime-lignende struktur: svak, siden volumet er fast
- eksitasjons-/energilignende struktur: `tokens` og `beta1`
- motivsektoren fungerer mer som intern geometri enn som bevart ladning

## 4.2 Open balanced regime

Kilder:
- `feature_lab_regimes/open_balanced_regime.csv`
- `feature_lab_regimes/open_balanced_regime_auto.md`
- `feature_lab_regimes/open_balanced_regime_summary.md`

Funn:
- `components` holder seg eksakt lik 1 i denne kjøringen. Det er en dynamisk observasjon, ikke en identitet.
- `nodes`, `edges`, `beta1`, `triangles` og `c4` drifter sterkt oppover.
- `clustering` blir hoy, mens `dim_proxy` faller. Det peker mot tett lokal klynging heller enn et tynt spacetime-lignende nettverk.
- SVD-kandidatene etter standardisering kollapser tilbake til identitetssektoren `edges/beta1/wedges/deg_sq_sum`.

Konklusjon:
- dette regimet gir ingen robust ny ikke-triviell quasi-invariant utover observerbar sammenheng (`components = 1`) i denne kjøringen
- det viktigste dynamiske resultatet er en sammenhengende, men kraftig kondenserende lokal struktur

## 4.3 Aggressive triad/delete regime

Kilder:
- `feature_lab_regimes/aggressive_triad_delete_regime.csv`
- `feature_lab_regimes/aggressive_triad_delete_regime_auto.md`
- `feature_lab_regimes/aggressive_triad_delete_regime_summary.md`

Funn:
- ingen ikke-trivielle dynamiske invariants overlever
- `tokens` kollapser, `components` vokser, `nodes` og `edges` eksploderer
- ra SVD lofter `clustering` som kandidat, men standardisert SVD fjerner denne dominansen

Dette er et textbook-eksempel pa skalaeffekt:
- `clustering` lever pa [0,1]
- `edges`, `c4`, `deg_sq_sum` lever pa store, voksende skalaer
- ra SVD kan derfor mistolke lav absolutt variasjon som bevaring
- standardisering viser at den egentlige nesten-nullsektoren igjen er dominert av algebraiske avhengigheter

Konklusjon:
- ingen robust ny quasi-invariant
- regime egner seg som stress-test og som advarsel mot a lese bounded features som bevarte storrelser

## 5. Hva som ser spacetime-lignende ut

Best kandidater:
- `nodes`: grovt volum
- `components`: operasjonell sammenheng eller fragmentering
- `dim_proxy`: emergent geometrisk vekst/tynning
- `spectral_radius`: global koblingsstyrke
- `wedges` og `c4`: mellomskala struktur som sier noe om lokal kontra utstrakt geometri

Disse er ikke bevaringslover. De er geometri- og strukturdiagnostikker.

## 6. Hva som ser eksitasjons- eller energilignende ut

Best kandidater:
- `tokens`: naermest et action-budsjett
- `beta1`: topologisk loop-ladning
- `triangles`: lokal lukket eksitasjon eller kondensasjonskjerne

Disse er de mest naturlige nar man vil snakke om "eksitasjon", "ladning" eller "energi-lignende" storrelser. Men bare `tokens` og `beta1` oppforer seg som eksakte invariants i den lukkede sektoren.

## 7. Hva som er redundant eller avledet

Disse bor ikke behandles som uavhengige basisretninger:
- `beta1`, hvis `nodes`, `edges` og `components` allerede er med
- `deg_sq_sum`, hvis `wedges` og `edges` allerede er med
- hele familier av linearkombinasjoner som bare er omskrivinger av de to identitetene over

I tillegg bor `clustering` brukes med forsiktighet:
- den er nyttig som diagnose
- men den er bounded og skala-sensitiv
- og bor ikke brukes alene som quasi-invariantkandidat

## 8. Forslag til redusert basisrom

Et praktisk redusert basisrom for videre arbeid er:

`tokens, nodes, edges, components, wedges, triangles, c4, spectral_radius, dim_proxy`

Begrunnelse:
- beholder action-budsjett (`tokens`)
- beholder volum og sammenheng (`nodes`, `edges`, `components`)
- beholder lokal og mellomskala geometri (`wedges`, `triangles`, `c4`)
- beholder globale/geometriske diagnostikker (`spectral_radius`, `dim_proxy`)
- dropper eksplisitt redundante koordinater (`beta1`, `deg_sq_sum`)

Mulig enda strammere basis hvis man vil ha minimalitet:

`tokens, nodes, edges, components, triangles, c4, spectral_radius, dim_proxy`

Da mister man den eksplisitte "open-triad"-tellingen `wedges`, men fjerner samtidig en feature som ofte korrelerer sterkt med gradmomenter og tetthet.

## 9. Sluttvurdering

Feature-labben er allerede nyttig nok til a teste quasi-invarianter, men hovedfunnet i disse tre regimene er negativt og derfor metodologisk verdifullt:

- de sterkeste nullretningene er som oftest algebraiske identiteter
- den lukkede sektoren gir ekte dynamiske invariants, men fa ikke-trivielle quasi-invarianter utover dem
- det apne balanserte regimet gir strukturvekst og sammenheng, ikke en ny bevaringslov
- det aggressive regimet viser tydelig hvorfor ra SVD alene er utilstrekkelig

Det riktige neste steget er derfor ikke a lete etter stadig flere features, men a:
- faktorisere ut identitetssektoren eksplisitt
- jobbe videre i et redusert basisrom
- og deretter teste om noen kombinasjoner forblir metastabilt stille pa tvers av flere ikke-trivielle regimer
