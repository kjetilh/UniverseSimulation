# WP-H rapport

Status: 12/12 grafer målt; ingen fysikkpåstand.

## Frosset metode og kjøretid

`WP-H_frozen.json` SHA-256: `dfe12effe77675174e04ea07c3afba669c46d5474c8c6b599ac72d7d61570b59`.
Analyse så langt: 37.107 s. Replaytid står i `WP-H_replay_runtime.json`.
64 rotnoder, r=1…10, lokal volumhelning på 3…6 og 6…10. Ikke-lat vandring: returnsannsynligheten regnes eksakt ved matrisepropagasjon; d_s tilpasses ved partall t=4…64. Partallsvalget ble frosset før måling på grunn av null retur ved odde tider på bipartitte positive kontroller. Ingen korreksjon for endelig graf eller stasjonært gulv. Gate bruker median over de 64 roteksponentene.
Nullene har nøyaktig samme merkede gradsekvens etter 10E vellykkede byttinger. Åtte nullreplikater gir grov 95%-intervalloppløsning; uniform miksing er ikke dokumentert. Positivt 2D-gitter er åpent og nær kvadratisk med eksakt N; den omkoblede kontrollen omkobler 10% av distinkte opprinnelige kanter, avrundet ned til partall, med faktisk drift i rådata.

## Replayintegritet

Alle 2048 deskriptorer og klokkeinkrementer per historie må samsvare med original v16b-logg. Initialt og endelig node-/tokenantall er kontrollert mot v16b_run_summary.csv; se `WP-H_replay_audit.csv`. Ingen ny dynamikk utover den samme replayen.

## Forhåndsregistrert gate

|graf|median d_s|null 95% lav|null 95% høy|under|over|
|---|---|---|---|---|---|
|2801_41011_current_global|1.97374|2.71773|3.11880|True|False|
|2801_41011_exposure_matched_local|1.85385|2.75224|3.07581|True|False|
|2801_41047_current_global|1.89365|2.75757|3.20100|True|False|
|2801_41047_exposure_matched_local|2.08660|2.90523|3.20711|True|False|
|2801_41081_current_global|1.92054|2.89052|3.19859|True|False|
|2801_41081_exposure_matched_local|2.18794|2.89214|3.23914|True|False|
|2903_41011_current_global|1.88915|2.86596|3.14261|True|False|
|2903_41011_exposure_matched_local|1.74599|2.83905|3.08113|True|False|
|2903_41047_current_global|1.91086|2.53937|3.23778|True|False|
|2903_41047_exposure_matched_local|1.74762|2.87602|3.22121|True|False|
|2903_41081_current_global|1.94638|2.96301|3.24165|True|False|
|2903_41081_exposure_matched_local|1.78154|2.90224|3.33480|True|False|

Terskel: minst 10 av 12 i samme retning. Under: 12/12; over: 0/12. Utfall: bestått.

## Begrensning, neste beslutning og lesning G

Grafene skilles fra disse gradbevarende nullene på det frosne tidsvinduet. Lesning G får støtte fra grafavlesningen, men en stabil dimensjon over større skalaer er ikke etablert.

## Blokkert / gjenstående

Commit og uavhengig G1-verifikasjon gjenstår til de er særskilt bekreftet. Ingen push/publisering/RAG-sync i denne arbeidsordren. Fullstendige observabler, ballvolumer, returkurver og alle grafrealisereringer er lagret som WP-H CSV-er.

## Verifisert resultat og målte referanser

Replay 12/12 bestått: 24 576/24 576 deskriptorer og klokkeinkrementer
samsvarer med original v16b, og alle start-/sluttantall stemmer. Replaytid
107,019 s; analyse av 144 grafer 37,112 s. Den separate målepiloten er holdt
utenfor alle gateaggregater. Se runtime-estimat og faktiske runtime-JSON-er.

144/144 grafer og 9216 rotmålinger er kontrollert fra lagrede artefakter:
gradsekvens, alle kulevolumer, uavhengig OLS av lagrede returkurver,
analytiske ringreturer, gater og referanser. Verifikasjon står i
WP-H_verification.csv, kilde-/testkvittering i WP-H_execution_sources.json.

**Registrert gate: bestått, 12/12 under nullens 95%-intervall (krav ≥10/12).**
Universgrafenes rotmedian-d_s er 1,745992–2,187936 (median 1,902256).
Både ring og 2D-gitter ligger under de tilhørende nullintervallene i 12/12
sammenligninger. Primærmålet har dermed målte positive referanser og nuller
som det faktisk skiller, i henhold til referansekravet i AGENTS.md.

Tabellen viser median over grafreplikater; råverdier for hver graf, alle
volumkurver og returkurver står i de tilhørende CSV-ene.

|type|n|median rot-d_s|d_s fra middelkurve|d_vol 3–6|d_vol 6–10|diameter|medianavstand|
|---|---|---|---|---|---|---|---|
|universe|12|1.902256|1.826507|2.811242|2.363580|25.500000|10.000000|
|null|96|3.028560|0.567598|3.427391|1.524222|inf|8.000000|
|ring|12|0.968025|0.968025|0.892694|0.938847|512.000000|256.250000|
|lat2|12|1.806560|1.696595|1.661862|1.689667|62.500000|21.000000|
|lat2_rewired|12|3.123241|3.017519|2.924702|2.779532|16.000000|8.000000|

Den omkoblede 2D-kontrollen har rotmedian-d_s 3,054478–3,209964, mot
1,702474–1,855189 for det åpne gitteret. Dette er en endelig endring på t≤64,
ikke en måling av uendelig dimensjon.

### Avgjørende begrensning: frakoblede nuller og aggregering

Alle 12 universgrafer er sammenhengende, mens **alle 96 nullgrafer er
frakoblede**. Nullene er beholdt som forhåndsregistrert, har nøyaktig samme
gradsekvens og har uendelig global diameter. Antall komponenter og frakoblede
par står per graf i rådata og i WP-H_aggregation_sensitivity.csv. Nullene
representerer ikke en sammenhengsbetinget null. 10E byttinger er heller ikke
et bevis for uniform miksing.

Den forhåndsregistrerte gaten bruker medianen av de 64 roteksponentene.
Det alternative, allerede lagrede målet fra **gjennomsnittlig returkurve**
gir motsatt retning: universets verdi er over hver av sine åtte nullers
verdier i alle 12 grupper, 96/96 par. For det registrerte rotmedian-målet er
universet under hver null, også 96/96. Disse fortegnene er invariant ved
strengt voksende transformasjon av det respektive ferdigberegnede målet.
Dette er en etterkontroll av aggregasjonsfølsomhet, ikke en ny gate, et nytt
forsøk eller 96 uavhengige hypotesetester. Historiene deler dessuten bare to
vekstgrunnlag, så ingen binomial signifikans beregnes fra disse tellingene.

Dommen «lavere dimensjon» er derfor ikke robust på tvers av de to
aggregeringsvalgene. Den spesifikke registrerte nullseparasjonen består,
men gir ikke en aggregeringsuavhengig eller asymptotisk spektraldimensjon.
Det er heller ikke et bevis for stabil dimensjon fra én endelig skala.

**Lesning G får støtte fra den registrerte nullseparasjonen i WP-H, men
stabil geometri er fortsatt ikke dokumentert; WP-H opphever ikke F2-feilen.**
Neste beslutning er å vurdere sammenhengsbetinget null og aggregasjonsvalg
før en eventuell ny forhåndsregistrering. Ingen slik omkjøring er gjort her.

## Endelig integrasjonsstatus — BLOKKERT

Målingene og den beskrevne verifikasjonen er ferdige. Foreskrevet staging av
171 eksplisitte F2-filer feilet 2026-09-08T22:22:51.147581+00:00, exit 128:

`fatal: Unable to create '/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/.git/index.lock': Operation not permitted`

Denne kjøringen opprettet ingen commits og gjorde ingen push. HEAD observert
før forsøket var `b9ec9092f40a0c1a797cb7651dd5af5443ba8840` på `program/wp-f2-f3-20260908`; tidligere deldata ble committet av
en parallell prosess. Det er ikke en commit-kvittering for sluttresultatet.

Amendment 1, punkt 5 krever rapport og stopp ved .git-blokkering; integratoren
committer. Ingen omgåelse eller nytt staging-forsøk er gjort. Full closure er
**publication_blocked**: sluttcommit/push mangler, arkivet er ikke bygd eller
deployet fra en slik commit, live manifest-revisjon er ikke verifisert, og
RAG-sync samt reell token-scoped auth-/sitasjons-/rate-limit-/ferskhetskontroll
er ikke utført. Ingen av disse stegene er utledet fra lokale tester.

Eksakte separate statuser: `WP-F2_H_closure_status.json`. Integrasjonsfillister:
`WP-F2_attempt2_integration_files.json` og `WP-H_integration_files.json`.
Arbeidskopiens øvrige endringer og den parallelle prosessens dokumentasjon er
bevart. Ingen forskningsprosess fra denne kjøringen står igjen i bakgrunnen.
