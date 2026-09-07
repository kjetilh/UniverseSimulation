# WP-F2 → WP-H: fortsettelse

7. september 2026. Arbeidskatalog er UniverseSimulation, aktiv gren master.
Original brukerordre: fullfør WP-F2, deretter WP-H. Kjøretidsanslag skal stå i
hjerteslaget før alle historier startes. Arbeidsordren sier ingen push og ingen
publisering/RAG-sync i denne pakken. To separate commits når pakkene er ferdige.

## Frosset kjøring

WP-F2 frozen SHA-256: `8b220334d2fbe55054d92c215fec608f378fd8ec2a9ddcbf3e6e54cc09990c42`.
R-pilot med 16384 steg tok 506.636 s, totalanslag 4.503 h. Den pålagte
halveringen til 8192 er derfor brukt. Konservativt justert anslag: 2.252 h.
Tidsanslaget er skrevet før R_BATCH_START i `.program_logs/WP-F2.heartbeat`.
Målt pilot er lagret under WP-F2_pilot_R_lat3_1152067013_* og teller ikke i
batchen med halvert lengde. Alle frø, terskler og analysevalg er i frozen-filen.

R-batchen kjører sekvensielt, 16 historier, i en separat prosess startet fra
Codex. Logg: `.program_logs/WP-F2_R_batch.log`. Siste hjerteslag og eksisterende
*_summary.csv er grunnsannhet. Ikke start duplikater mens prosessen kjører.
En fullført historie har summary, curves, events, snapshots og metadata.

## Avklaring som fortsatt kreves

Kjetil er spurt via asynkront spørsmål: skal M også gjøre seed til mark på
vertsnoden, eller beholde seed og oppgi at grafen ikke er frossen? Ingen svar
foreligger når dette skrives. Ingen M-historie er kjørt. Standardverdien i
frozen-filen er `pending`, som hindrer M-kjøring. Ikke tolk forhåndsvalgt
UI-alternativ eller ventetid som svar. Se WP-F2_method_notes.md for bevis fra v7.

Ved eksplisitt svar: lagre WP-F2_M_seed_resolution.json med policy (`mark` eller
`unchanged`), frozen_sha256, nøyaktig svar og tid. Ikke endre original frozen-fil.
Svar `unchanged` krever at frossen-M-gaten tydelig merkes som avvikende kontroll,
fordi seed endrer grafen. Alle vitenskapelige konklusjoner avgrenses til faktisk
målte parametre; ikke kopier arbeidsordrens brede regelfamilie-dom som bevis.

## Kommandoer

Dynamikk: `PYTHONPATH=/opt/homebrew/lib/python3.11/site-packages python3`.
Analyse: `/opt/homebrew/bin/python3.11` uten PYTHONPATH-overstyring.
Ingen avhengigheter er installert. v16a trenger Python >=3.12, mens installert
NumPy/SciPy virker i 3.11. Den opprinnelige .codex_pydeps er for Python 3.9.

Etter M-avklaring og avsluttet R-prosess kan `Tools/influence_order_lab.py --batch`
fortsette. Den hopper over ferdige R-historier og kjører M-historiene. Bruk
ovennevnte dynamikkmiljø. --aggregate gjenoppbygger tabeller og rapport.
Rapportens automatisk genererte del sier at commit/G1 gjenstår til en separat
verifikasjonskvittering er skrevet.

WP-H er implementert og forhåndsregistrert, men ikke kjørt. Etter ferdig F2,
verifikasjon og egen F2-commit: kjør Tools/state_graph_dimension_lab.py --replay
med dynamikkmiljøet, deretter --analyze med 3.11. Replay kontrollerer alle
originale v16b-deskriptorer/tider og node/tokenantall; ingen ny dynamikk.
Skriv også H-kjøretidsanslaget til WP-H.heartbeat før hele H-kjøringen.

Tester bestått:
- python3 Tools/influence_order_lab.py --self-test
- /opt/homebrew/bin/python3.11 -m unittest tests.test_influence_order_lab -v (3)
- PYTHONPATH=... python3 -m unittest tests.test_influence_order_runtime -v (3)
- /opt/homebrew/bin/python3.11 Tools/state_graph_dimension_lab.py --self-test

Hvert eksisterende source_hash er kontrollert uendret. Nye testfiler er skrevet
etter freeze og endrer ikke de frosne verktøyene. En flyttalls-likhet i den første
F2 selvtesten ble rettet til toleranse før freeze; begge råberegningene var like
innen avrunding. Ingen estimator eller terskel er tunet etter data.

## Eierskap og integrasjon

Egne filer: Tools/influence_order_lab.py, Tools/state_graph_dimension_lab.py,
tests/test_influence_order_lab.py, tests/test_influence_order_runtime.py,
WP-F2_* og WP-H_* opprettet nå, og de to egne radene i attempt_ledger.csv.
WP-F2_influence_order_calibration.md er eksisterende arbeidsordre og er uendret.
Andre eksisterende endringer må ikke stages. Les git status og diff.

Git index-tilgang virket; ingen commit er gjort ennå. Ikke bruk `.git`-blokkering
som forklaring uten en faktisk feil. Stoppregelen krever rapport og stopp dersom
commit senere blokkeres. `.program_logs` er ignorert; bevar viktig evidence som
CSV/JSON og sporbar rapport, ikke stol bare på ignorerte logger.

Loop-detektoren flagget S1,S2,S4,S5,S7 og ikke S3,S6. Full rapport er i
.program_logs/WP-F2_loop_check.log. Ingen falsk påstand om full godkjenning.

## Oppdatert stoppunkt

R-prosessen er avsluttet normalt 21:26:24Z. Alle 16 R-historier er ferdige,
pluss separat pilot. 17/17 bestått artefaktverifikasjon. Originale kildehash
stemmer. R feiler mekanismeterskel (gamma-spenn 0.1061728873); alpha mangler
for 5 kernel-historier og 7 legacy-historier. M og H er fortsatt ikke kjørt.
R-batchens boolske gatefil suppleres av WP-F2_threshold_audit.csv, som skiller
manglende grunnlag fra negativ terskel. Ikke aggregér på nytt uten å bevare
rapportens manuelle avslutning; --aggregate overskriver den genererte rapporten.
Delarbeidene lagres i to separate commits, med blokkeringen synlig i rapportene.
Det innebærer ikke at WP-F2 eller WP-H er ferdig. Avsluttende commit-hasher
finnes i git log og hjerteslag, ikke i de selvrefererende rapportfilene.

Ny verifikator: Tools/verify_wp_f2_artifacts.py (ingen dynamikk) gjenskaper DAG
fra alle lagrede ressurssett og kryssjekker uendrede v16b analyze-observabler.
Den har produsert WP-F2_verification.csv med hasher for 17*5 artefakter.

## SISTE STATUS — GIT BLOKKERT, INGEN COMMITS

Faktisk git add av 101 eksplisitte egne filer feilet med exit 128:
.git/index.lock: Operation not permitted. Ingen staging eller commits fant sted.
Tidligere avsnitt om planlagte commits er planer, ikke utførte handlinger.
Tidlig git add av uendret sporfil var en no-op, ikke en valid skrivetilgangstest.
Stoppregelen i arbeidsordren er fulgt. Integratoren committer.

WP-F2_integration_files.json er eksplisitt filliste for F2. Den inkluderer nå
seg selv. Ledger har kun F2-raden endret; H-raden skal først oppdateres i H sin
separate commit. H-forberedte filer er Tools/state_graph_dimension_lab.py,
Documentation/Program/WP-H_frozen.json og Documentation/Program/WP-H_report.md.
De er ikke utførte H-målinger. Ingen ekstra tillatelse til push er gitt.

Før videre M-dynamikk kreves fortsatt eksplisitt seed-avklaring fra Kjetil.
Ingen svar har kommet i denne økten. R-batchen er avsluttet; det går ingen
forskningsprosess videre i bakgrunnen.
