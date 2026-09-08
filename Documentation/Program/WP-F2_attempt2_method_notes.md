# WP-F2 forsøk 2 / WP-H — kjøringsnotater

8. september 2026. Arbeidsordre: WP-F2_amendment_1.md, R → M → gater → WP-H.
Ingen nye avhengigheter, ingen v7/v16-endringer, ingen endring av original frys.

## Implementasjon og tolkning

Tools/influence_order_attempt2.py er en separat wrapper rundt den opprinnelige
Tools/influence_order_lab.py. Originalfilen er beholdt bit-for-bit, slik at
originale kildehash og WP-H-forhåndsregistrering fremdeles validerer. Wrapperen
bruker MarkAdapter og run_history uendret, men erstatter kernel_access under
M-kjøringen med amendmentets eksakte seed-lese-/skrivesett. Andre deskriptorer
bruker originalt uttrekk. Legacy beholder sin deklarerte, delvis kontrafaktiske
v16a-projeksjon, slik opprinnelig frys angir.

Det gamle run_history skriver også gammelt-grid-diagnostikk for M; disse filene
er ikke brukt i forsøk 2-gatene. Bare *_attempt2_summary.csv inngår. R sine
opprinnelige logger, grafer, metadata, kurver og sammendrag er ikke overskrevet.
Full forsøk 1-rapport og tabeller er kopiert til WP-F2_attempt1_* før analysen.

«Samme punktkrav» er før nye tall tolket som samme utvalg for begge helninger:
median V≥8, τ≤T/4, minst seks finite positive punkter. R90-helning er kun
supplerende diagnostikk på dette samme vinduet. Manglende historier beholdes
som NaN og gjør gruppe-KI udefinert. De fjernes ikke fra bootstrap.

Kurvene teller alle kvalifiserte forfarpar. Eksakte heltallshistogrammer
akkumuleres etter første τ-vindu som inkluderer paret. Middelavstand er
avstandssum / antall par med definert avstand. Manglende noder i R-øyeblikksgraf
er fortsatt udefinerte; ingen settes til avstand null. R90 beregnes med
opprinnelig lineær interpolasjon. Tester sammenligner med direkte paropptelling.

En syntaksfeil i første utkast til tau_grid ble funnet av py_compile og rettet
før tester, frys eller reanalyse. Ingen resultatbasert tuning.

## Miljø og kjøring

Dynamikk/replay: PYTHONPATH=/opt/homebrew/lib/python3.11/site-packages python3.
Analyse: /opt/homebrew/bin/python3.11 uten PYTHONPATH-overstyring.
Dette er de eksisterende miljøene dokumentert i WP-F2_method_notes.md.

F2: --prepare, --reanalyze-R, --run-M, --gates på den nye wrapperen, i denne
rekkefølgen. Verifikasjon: Tools/verify_wp_f2_artifacts.py (ressurssett → original
DAG.analyze), deretter Tools/verify_wp_f2_attempt2.py (alle V-kurver fra tidsmasker,
uendret DAG-statistikk, seed-støtte, uavhengig OLS og alle bevarte kildehash).

H: Tools/run_wp_h_package.py --replay og --analyze kaller den frosne H-koden.
Wrapperen endrer bare status/ledger og kjøretidsanslag. Analysepiloten er samme
første sluttgraf, holdt utenfor gateaggregatene; ingen ny dynamikk. H-evidence
kontrolleres av Tools/verify_wp_h_artifacts.py.

## Kildekontroll for H-null

NetworkX double_edge_swap-dokumentasjonen ble kontrollert på nettet 8. september:
[offisiell dokumentasjon](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.swap.double_edge_swap.html).
Den bevarer nodegrader, teller vellykkede byttinger og garanterer ikke sammenheng.
H beholder derfor eventuelle frakoblede nuller og rapporterer uendelige avstander.
Ingen påstand om uniform nullmiksing eller asymptotisk dimensjon følger av dette.

## Publisering og stoppregel

Arbeidskopien hadde eksisterende endringer ved start; disse er bevart. Den aktive
grenen er losen/nodegraph-vurdering-20260908. Amendmentet krever rapport og stopp
ved faktisk .git-blokkering, med integrator som committer. Målt resultat er ikke
lik en fullført publiseringsrunde. Ingen push, deploy, live-revisjon eller
RAG-status skal antas fra lokale målinger eller tester.
