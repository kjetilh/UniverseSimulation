# WP-F2 rapport

Forsøk 2 følger amendment 1. Forsøk 1 er bevart separat i sin helhet.

Original frys SHA-256: `8b220334d2fbe55054d92c215fec608f378fd8ec2a9ddcbf3e6e54cc09990c42`.
Forsøk 2 frys SHA-256: `bb2805971fe744433353d61cb9577cddb170e3c450436ee15f6e688ab4065896`.

Metode: τ = 0,25·2^(k/4) til T/2; hendelser ved t≥T/2. Begge helninger bruker median V≥8 og τ≤T/4, minst seks punkter. γ bruker middelavstand; R90 og R90-γ rapporteres diagnostisk. KI er eksakt bootstrap over 256 trekk av fire historier. Udefinerte historier beholdes. Alle v7/v16-kilder og den opprinnelige laben er uendret. Separat wrapper erstatter bare M-seed-lese-/skrivesettet; M-dynamikken bruker den opprinnelige MarkAdapter med seed-policy mark. Ingen R-dynamikk kjøres.

## Forsøk 2 — R

|orden|underlag|n|α [95% KI]|γ middel [95% KI]|γ R90|minste fit-punkter α/γ|
|---|---|---|---|---|---|---|
|kernel|ring|4|1.621158 [1.377219, 1.868694]|0.331278 [0.280660, 0.392217]|0.353052|7/7|
|kernel|lat2|4|2.053882 [1.882598, 2.324796]|0.460400 [0.427132, 0.464781]|0.397631|6/6|
|kernel|lat3|4|2.755761 [2.667896, 2.792386]|0.455726 [0.452883, 0.467821]|0.338829|6/6|
|kernel|rrg|4|1.756612 [1.738640, 1.810818]|0.629536 [0.576845, 0.637790]|0.388132|6/6|
|legacy|ring|4|1.162586 [1.085637, 1.285781]|0.364755 [0.350275, 0.395276]|0.414473|6/6|
|legacy|lat2|4|nan [nan, nan]|nan [nan, nan]|nan|5/5|
|legacy|lat3|4|nan [nan, nan]|nan [nan, nan]|nan|3/3|
|legacy|rrg|4|nan [nan, nan]|nan [nan, nan]|nan|5/5|

Alle kurver, parantall, avstandssummer, WP-F0-observabler, drift og tverrbindinger er lagret i forsøk 2-CSV-ene.

## Forsøk 2 — M

|orden|underlag|n|α [95% KI]|γ middel [95% KI]|γ R90|minste fit-punkter α/γ|
|---|---|---|---|---|---|---|
|kernel|ring|4|1.667715 [1.572883, 1.945987]|0.368336 [0.320182, 0.415745]|0.373417|7/7|
|kernel|lat2|4|2.225544 [2.101663, 2.295005]|0.497491 [0.416634, 0.556155]|0.514944|7/7|
|kernel|lat3|4|2.868109 [2.800182, 3.128140]|0.404375 [0.393264, 0.433237]|0.326408|7/7|
|kernel|rrg|4|1.939058 [1.738640, 2.154625]|0.626861 [0.608568, 0.632705]|0.413581|6/6|
|legacy|ring|4|1.190327 [1.148943, 1.338890]|0.411130 [0.377005, 0.428754]|0.444118|6/6|
|legacy|lat2|4|nan [nan, nan]|nan [nan, nan]|nan|5/5|
|legacy|lat3|4|nan [nan, nan]|nan [nan, nan]|nan|3/3|
|legacy|rrg|4|nan [nan, nan]|nan [nan, nan]|nan|4/4|

Alle kurver, parantall, avstandssummer, WP-F0-observabler, drift og tverrbindinger er lagret i forsøk 2-CSV-ene.

## Forsøk 1 — R (bevart)

Full original rapport: [WP-F2_attempt1_report.md](WP-F2_attempt1_report.md). Tallene under bruker det gamle gridet og γ på R90.

|orden|underlag|α|γ R90|
|---|---|---|---|
|kernel|ring|1.701186|0.305889|
|kernel|lat2|nan|0.350591|
|kernel|lat3|nan|0.412062|
|kernel|rrg|nan|0.500000|
|legacy|ring|1.152003|0.258496|
|legacy|lat2|nan|0.361441|
|legacy|lat3|nan|0.438082|
|legacy|rrg|nan|0.435168|

## Uendrede porter / G4

|modus|orden|rekkefølge|separasjon|γ-spenn|mekanisme|F2|
|---|---|---|---|---|---|---|
|R|kernel|fail|fail|0.129122|fail|fail|
|R|legacy|not_evaluable|not_evaluable|nan|not_evaluable|not_evaluable|
|M|kernel|fail|fail|0.129155|fail|fail|
|M|legacy|not_evaluable|not_evaluable|nan|not_evaluable|not_evaluable|

G4 og referansekvalifikasjon må leses sammen: ikke-evaluerbar α er manglende instrumentgrunnlag, ikke null eksponent eller et påvist fravær av geometri. De målte kalibreringsreferansene må skilles før endepunktet kan brukes som hypotesegate (AGENTS.md). Ingen terskel er endret. Naboforskjellenes fortegn står i gatefilen som transform-invariant rekkefølgekontroll. Fire historier gir grov KI-oppløsning; dette er en endelig kalibrering. Ingen WP-F3 kjøres.

## Status og avslutning

Målinger og integrasjon har separate statuser. Commit/push, offentlig arkiv, live-revisjon, RAG-sync og autentisert ferskhets-/sitasjonskontroll er ikke bekreftet. Ved faktisk .git-blokkering gjelder amendmentets stoppregel; integratoren committer. Uavhengig G1-kvittering gjenstår. Ingen fysikkpåstand.

## Verifisert resultat — amendment 1, forsøk 2

R 16/16 reanalysert på 67,782 s. M 16/16 kjørt og analysert på 1201,465 s
(20,024 min), 8192 steg per historie. Original pilot/halvering står i forsøk 1.
Ingen ny R-dynamikk. Alle 32 kernel-historier har minst seks fit-punkter; begge
primære kalibreringsgater er dermed evaluerbare med amendmentets målevindu.

**G4: M feiler. Den bestilte F2-kalibreringen består ikke for det testede
regeloppsettet ved disse N/T. R feiler også.** Ingen WP-F3 er startet.
Både R og M har α-fortegnene +,+,− for ring→lat2→lat3→rrg. Ring/lat2/lat3 har
stigende α med disjunkte nabointervaller i begge modi, men kravet omfatter
også rrg. Rrg-leddet bryter den forhåndsregistrerte rekkefølgen. Ingen ny
formtest, ingen nye porter og ingen endret γ-grense er brukt i denne kjøringen.
R sitt γ-spenn er 0,129122101194; M sitt er 0,129154885821; begge er over 0,10.

M har målt kantdrift og andel berørte opprinnelige kanter lik null i alle
16 historier, og samme antall noder ved start og slutt. Seed-hendelser leser
bare den angitte verten og eventuelt tokenet, og skriver bare mark:host.
Legacy er fortsatt tynn: tallene er i aggregatet. Legacy sine manglende
seks-punktsfit er «ikke evaluerbar», ikke en målt negativ eksponent.

Middelavstands-γ for R er 0,331278 / 0,460400 / 0,455726 / 0,629536.
Under-½-helningen for ring forsvinner altså ikke ved å erstatte R90 med
middelavstand. Dette utelukker heltalls-R90 som hele forklaringen, men
identifiserer ikke tokenfangst som årsak; målevindu og endelig størrelse er
fortsatt begrensninger. R90 på samme vindu er lagret som diagnostikk.

Referansekravet i AGENTS.md gjelder: endepunktet består ikke sin fulle
kalibrering mot de målte kjente underlagene. Derfor kvalifiserer denne
runden ikke α som en generell hypotesegate for universets geometri. Den
brede formuleringen «nei for regelfamilien» i hovedspec-en kan ikke gjøres
til et bevis for alle skalaer eller alle geometrier fra disse dataene.
**Lesning G står ikke dokumentert av F2-kalibreringen ved dette N/T.**
WP-H gir den separat bestilte grafavlesningen; den endrer ikke F2-portene.

Verifikasjon: 33/33 lagrede historier inklusive separat gammel pilot er
gjenskapt fra lese-/skrivesett med uendret DependencyDAG.add og analyze.
32/32 forsøk 2-historier består uavhengig kontroll av samtlige V-punkter,
fit-vindu, OLS-helninger, uendret DAG-statistikk og M sin seed-/driftkontrakt.
Fem analysetester, fire runtime-tester og uttømmende små-DAG-selvtest består.
Se WP-F2_attempt2_verification.csv, WP-F2_verification.csv og
WP-F2_attempt2_checks.json. Alle opprinnelige kilder, original frys og R-data
bevarer hashene fra før forsøket.

En parallell prosess committet foreløpige data som 3ab0fd5 og la inn
WP-F2_amendment_2.md og en ledger med attempts=3 mens M kjørte. Den prosessens
commit-tittel er ikke en fullført konklusjon fra denne kjøringen. Denne
rapportens portutfall gjelder amendment 1, forsøk 2, slik brukeren bestilte.
Amendment 2 er ikke utført her. Den eksterne dokumentasjonen er bevart.

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
