# WP-F2 / WP-H: metodeavklaringer før batchen

Skrevet 7. september 2026 før første batch. Dette er ikke en resultatrapport.

## Uavklart: seed i modus M

WP-F2 krever frossen graf i M og uendret exposure_matched_local-adapter.
Koden `v7.apply_seed_descriptor` legger til en node og en kant, mens arbeidsordren
bare erstatter delete/triad/swap med mark. Den lokale seed-raten er positiv:
0.0005039538147742117 per vert. Derfor kan disse kravene ikke alle oppfylles uten
et valg som arbeidsordren ikke angir.

Kjetil er spurt om seed også skal skrive mark på vertsnoden, eller om seed skal
beholdes med eksplisitt rapportering av drift. Ingen av alternativene er valgt
på Kjetils vegne. `WP-F2_frozen.json` har `M_seed_policy: pending`; R-piloten er
uavhengig av dette. M kan ikke kjøres med pending. Avklaringen skal lagres som
`WP-F2_M_seed_resolution.json`, med policy, Kjetils ordlyd, tidspunkt og
frozen_sha256, uten å overskrive den opprinnelige forhåndsregistreringen.

## Parametre og miljø

`v16b.frozen_spec` inneholder lokal seed-rate, men ingen Params. Parameterkilden
er derfor nøyaktig den som brukes av `v16b.run`: `v16a.anchor_params()`.
Den gir r_birth=0.02, p_swap=0.02, r_death=p_del=p_triad=0, r_token=1;
hele objektet er lagret i frozen-filen. Ingen egne regelparametre er valgt.
De fire historiene bruker to v16b-seed med 17 starttokens og to med 26,
balansert og likt mellom underlag og modi. Plasseringen er uniform med tilbakelegging.

Systemets python3 er 3.13.2. `.codex_pydeps` har NumPy 2.0.2 for Python 3.9,
og `/usr/bin/python3` kan importere det, men kan ikke parse eksisterende v16a-
f-strenger (krever Python >=3.12). Det eksisterende `/opt/homebrew/bin/python3.11`
har NumPy 2.4.0, SciPy 1.16.3 og NetworkX 3.6.1, men kan heller ikke parse v16a.
Dynamikk kjøres med python3.13 og eksisterende ren Python NetworkX via PYTHONPATH;
analyse med Python 3.11. Ingen pakker er installert og ingen v7/v16-filer er endret.

## Kontroller og kilder

F2 sin eksakte maksimumsberegning for inkluderende intervall bruker at et
intervall ikke krymper når endepunktene forlenges til rot og sluk. Dette er
kontrollert mot direkte opptelling av alle par for alle DAG-er med opptil fem
hendelser, og mot en uavhengig mengdebasert implementasjon på tilfeldige DAG-er.
Fortidsvolum og R90 er kontrollert mot direkte opptelling av alle forfarpar i en
kjede som går på en ring. Manglende eksponenttilpasning blir NaN, aldri bestått.

H sin returprobabilitet er kontrollert mot binomialformelen på en ring,
inkludert eksakt null på odde tidspunkt. Derfor er partall 4…64 frosset før
måling for både universgraf og kontroller; alle returer 1…64 lagres. 10%-gitteret
omkobler distinkte opprinnelige kanter, avrundet ned til nærmeste partall.

NetworkX-dokumentasjonen er kontrollert 7. september 2026:

- [double_edge_swap](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.swap.double_edge_swap.html)
  bevarer gradene, men garanterer ikke sammenheng. H bevarer frakoblede nuller
  og rapporterer uendelige avstander; de forkastes ikke betinget på resultat.
- [random_regular_graph](https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.random_regular_graph.html)
  brukes for den tilfeldige 3-regulære kontrollen. En enkelt endelig graf er
  ikke et bevis på asymptotisk ekspansjon eller uendelig dimensjon.

Loop-detektoren er kjørt ved forberedelses-milepælen: S1, S2, S4, S5 og S7
utløst; S3 og S6 ikke utløst. Full rårapport står i
`.program_logs/WP-F2_loop_check.log`. Signaturene er rapportert, ikke godkjent bort.

## Publisering og eksisterende arbeid

Den konkrete arbeidsordren sier to separate commits og ingen push, samt at
closure-policyen ikke inngår. Derfor skal ikke denne kjøringen betegnes som
publisert. Ingen deploy eller RAG-sync utføres. Git index-tilgang er kontrollert
med vellykket `git add` av den allerede sporede, uendrede arbeidsordren; ingen
uvedkommende filer ble staged. Eksisterende endringer i .gitignore, loop-detektor,
verify-filer og andre uregistrerte dokumenter er beholdt.

## Observert målebegrensning under R-batchen

Lat2/R-seed 1153087013 og 1153087049 har endelig Gillespie-tid henholdsvis
56.7069 og 62.0833. Frosset tau-grid er derfor 1,2,4,8. Kernel-ordenens
medianvolumer er henholdsvis [1,2,6,18] og [1,2,6,16]. Bare tau=8 oppfyller
V>=8. Minst to punkter trengs for en helning, så alpha er udefinert, ikke null.
Legacy-ordenens alpha er også udefinert i begge. Batchen fortsetter med uendrede
regler. Manglende fit kan ikke oversettes til et bevis på fravær av geometri.
Ingen tau-punkter legges til etter at dette er sett.

## Korreksjon av Git-forhåndskontrollen

Faktisk staging av nye filer feilet med .git/index.lock: Operation not permitted.
Den tidlige kommandoen på uendret sporfil var en no-op og kunne ikke bevise
skrivetilgang. Ingen commits er opprettet. Arbeidsordrens stoppregel er aktiv.
