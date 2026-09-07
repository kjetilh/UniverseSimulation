# WP-F2 rapport

Status: DELVIS UTFØRT / M BLOKKERT PÅ REGELAVKLARING. R er ferdig (16/16); M er ikke startet (0/16). Codex måler; G1-verifikasjon hos spesifikasjonsforfatter gjenstår.

## Frosne parametre og metode

`WP-F2_frozen.json` SHA-256: `8b220334d2fbe55054d92c215fec608f378fd8ec2a9ddcbf3e6e54cc09990c42`.
Params er hentet fra `v16b.run → v16a.anchor_params`, fordi `frozen_spec` ikke inneholder Params. Alle terskler, seed og operasjonelle estimatorvalg ble frosset før piloten.
Modus M seed-policy: `pending`. Legacy er uendret v16a-projeksjon av de samme deskriptorene; i M inkluderer den deklarerte grafskrivinger som mark-adapteren ikke utfører. Kernel-ordenen bruker adapterens faktiske skrivesett. DAG.add er uendret.
Tau måles i Gillespie-tid, ikke hendelsesnummer. R bruker alle forfarpar til samme sene hendelsesutvalg som V. R-avstander hentes fra siste 512-stegs øyeblikksgraf; manglende noder/frakoblede par telles separat. Bootstrap er eksakt over de 256 trekkene av fire historier, ikke over hendelser.
Markvekter normaliseres innen hvert token, slik at tokenklokkene ikke endres. RRG er en tilfeldig regulær kontroll; ingen enkelt realisasjon sertifiseres som uendeligdimensjonal.

## Kjøretid

```json
{
  "pilot_seconds": 506.63647287501954,
  "projected_32_histories_seconds": 16212.367132000625,
  "projected_hours": 4.503435314444618,
  "selected_steps": 8192,
  "estimated_selected_seconds": 8106.183566000313,
  "caveat": "single lat3/R history; mode, token growth, analysis and machine load may change runtime"
}
```

## Målte tall

|modus|orden|underlag|n|α [95% KI]|γ [95% KI]|tverrbinding|kantdrift|
|---|---|---|---|---|---|---|---|
|R|kernel|ring|4|1.7012 [1.4150, 2.0841]|0.3059 [0.2737, 0.3907]|0.5743|0.2007|
|R|kernel|lat2|4|nan [nan, nan]|0.3506 [0.2626, 0.4381]|0.5953|0.1414|
|R|kernel|lat3|4|nan [nan, nan]|0.4121 [0.3322, 0.4252]|0.6763|0.1002|
|R|kernel|rrg|4|nan [nan, nan]|0.5000 [0.5000, 0.6159]|0.5105|0.1960|
|R|legacy|ring|4|1.1520 [1.1375, 1.2224]|0.2585 [0.2585, 0.2585]|0.2741|0.2007|
|R|legacy|lat2|4|nan [nan, nan]|0.3614 [0.3000, 0.4170]|0.1297|0.1414|
|R|legacy|lat3|4|nan [nan, nan]|0.4381 [0.4381, 0.4381]|0.1127|0.1002|
|R|legacy|rrg|4|nan [nan, nan]|0.4352 [0.4352, 0.4381]|0.1341|0.1960|

De fire WP-F0-tallene med KI er bevart i `WP-F2_aggregate.csv`; per-historie-tall står i `WP-F2_per_history.csv`. Hendelseslogger og øyeblikksgrafer er separate CSV-er per historie.

## Uendrede terskler

|modus|orden|evaluerbar|rekkefølge|separasjon|mekanisme|F2|
|---|---|---|---|---|---|---|
|M|kernel|False|False|False|False|False|
|M|legacy|False|False|False|False|False|
|R|kernel|False|False|False|False|False|
|R|legacy|False|False|False|False|False|

## Utfall, begrensninger og neste beslutning

WP-F2 samlet er ikke fullført: M mangler. G4-grenen som avhenger av M kan ikke velges. R består ikke det frosne mekanismekravet (detaljer under). Ingen WP-F3 er kjørt.

## Blokkert / gjenstående

Commit og uavhengig G1-kontroll er ikke bekreftet i denne automatisk genererte rapporten. Ingen push, publisering eller RAG-sync inngår, i henhold til denne arbeidsordren. Ingen fysikkpåstander. Fire historier gir grov usikkerhetsoppløsning. Avvik fra WP-F0 ved 8× kjørelengde er observasjoner, ikke automatisk kodefeil.

## Verifisert delresultat 7. september 2026

R-batchen tok 728.617 s (12.14 min), etter piloten på 506.636 s.
Pilotens 32-historiersanslag var 4.503 timer; derfor ble STEPS halvert til 8192
før batchen. Det konservative halverte anslaget var 2.252 timer.
`WP-F2_runtime_estimate.json` og den før-start skrevne hjerteslaglinjen er bevis.
Piloten har 16384 steg og er holdt utenfor alle batchaggregater og KI.

16 R-historier og den separate piloten er kontrollert fra lagrede CSV-er med
uendret `DependencyDAG.add` og `analyze`: **17/17 bestått**. Hendelsesnummer,
klokker, forgjengersett, antall kanter, høyde, sammenlignbare par, kildehash og
512-stegs øyeblikksbilder stemmer. Se `WP-F2_verification.csv`, som også lagrer
SHA-256 for alle fem rå-/analyseartefakter per historie.

Seks unittest-tester består (tre for estimatorene, tre for runtimekontrakten),
pluss den uttømmende små-DAG-testen. Runtime-testen bruker syntetisk ring,
ikke universets historier. Reproduksjonskommandoer står i `WP-F2_resume.md`.
Kildehashene i både F2 og den forberedte H-forhåndsregistreringen er uendret.

### R: terskel for terskel

| orden | α rekkefølge | α separasjon | γ-spenn over ring/lat2/lat3 | mekanisme ≤ 0,10 | samlet F2-R |
|---|---|---|---|---|---|
| kernel | kan ikke evalueres | kan ikke evalueres | 0,1061728873 | ikke bestått | ikke bestått |
| legacy | kan ikke evalueres | kan ikke evalueres | 0,1795859283 | ikke bestått | ikke bestått |

Den maskinelle `WP-F2_gates.csv` setter boolske gateflagg til false når
forutsetninger mangler; `WP-F2_threshold_audit.csv` skiller uttrykkelig mellom
`not_evaluable`, `not_run` og `fail` for hver terskel. Tabellen over er den
terskelvise dommen. Kernel-ordenens γ-medianer er 0,305889, 0,350591 og 0,412062.
De etablerer ikke én felles diffusiv eller ballistisk lov. Grensen 0,10 er ikke
endret selv om overskridelsen er liten.

α er udefinert i **5/16 kernel-historier** og **7/16 legacy-historier**,
fordi bare ett tau-punkt når median V≥8. Disse historiene er ikke fjernet fra
bootstrap; deres gruppe-KI er udefinert. Se `WP-F2_unavailable_fits.csv` og
hver histories kurvefil. Ringens kernel-α er 1,7012 [1,4150; 2,0841], men et
enkelt underlag kan ikke avgjøre rekkefølge eller nullseparasjon.

Kernel-ordenens mediane kantdrift (symmetrisk differanse delt på initialt E)
er 0,2007 / 0,1414 / 0,1002 / 0,1960 for ring/lat2/lat3/rrg. Kernel-ordenens
medianer for tverrbindingsandel er 0,5743 / 0,5953 / 0,6763 / 0,5105.
Legacy-ordenens lenker per hendelse er 1,074 / 1,050 / 1,045 / 1,052,
altså fortsatt tynne. Tverrbindingsandelen er ikke identisk med WP-F0s 8,5%:
her er underlagene andre og historiene fire ganger lengre etter halveringen.
Uendret v16a-uttrekk og eksakt syntetisk trace-paritet er kontrollert; tallforskjell
alene behandles ikke som bevis for kodefeil.

Ved hver histories største tau-vindu mangler grafavstand for samlet 89 av
8 933 865 kernel-par og 70 av 2 002 045 legacy-par (nye noder siden siste
øyeblikksbilde). Disse er talt som udefinerte og utelatt fra R90. Ingen manglende
avstand er satt til null. Alle antall finnes i kurvefilene.

### Hva som fortsatt blokkerer

M er ikke kjørt. Arbeidsordren krever frossen geometri, mens uendret `seed`
legger til node og kant og ikke er blant de tre hendelsene med angitt
mark-erstatning. Kjetil er spurt om denne regelen. Ingen svar er mottatt når
rapporten skrives; `M_seed_policy` er `pending`. Det er en reell forskjell i
forsøket, ikke et tillatelsesspørsmål utløst av en skill. Se
`WP-F2_method_notes.md`. WP-H er forberedt og kontrollert på analytisk ring,
men replay/null-kjøringen er ikke startet fordi F2 skal komme først.

G4: R består ikke, M er ukjent; ingen av de tre fullstendige M/R-grenene kan
adjudiseres. Dette dokumenterer ikke fravær av geometri i hele regelfamilien.
**Lesning G er fortsatt uavklart samlet; R-kalibreringen gir ikke den påkrevde
dokumentasjonen ved dette N/T.** Neste beslutning er M sin seed-semantikk,
ikke justering av tau-grid, epsilon eller terskler etter resultatene.

Loop-detektoren er kjørt: S1, S2, S4, S5 og S7 utløst; S3 og S6 ikke utløst.
Dette er bevart i metode-notatet og råloggen. Uavhengig G1-kvittering gjenstår.
Ingen push, deploy eller RAG-sync er utført, i samsvar med denne arbeidsordren.

## Integrasjonsstatus

Delarbeidet lagres i egen WP-F2-commit med den bestilte tittelen. Committen
inneholder fullført R, pilot, frosset oppsett, tester og en uttrykkelig åpen M.
Dette er ikke en erklæring om fullført WP-F2. Commit-hash identifiseres fra
Git-historien; ingen push utføres. WP-H-forberedelsene holdes i egen commit.

## Endelig integrasjonskvittering: BLOKKERT

Det faktiske staging-forsøket feilet med exit 128:
`fatal: Unable to create .git/index.lock: Operation not permitted`.
Ingen filer ble staged; ingen commit eller push ble gjort. Tidligere test av
`git add` på en allerede sporet, uendret fil var en no-op og beviste ikke
skrivetilgang. Den tidligere planen om to commits er derfor ikke utført.

Arbeidsordrens eksplisitte regel gjelder: «Kan din sandbox ikke skrive .git:
si det i rapporten og stopp — integratoren committer.» Det gjøres ikke et nytt
forsøk eller en omgåelse. R-evidence og begge forberedte verktøy ligger på disk.
M avventer dessuten Kjetils seed-avklaring; WP-H er fortsatt ikke kjørt.
En integrator må stage egne filer eksplisitt og bevare skillet mellom faktisk
måling og uutført arbeid. WP-F2_integration_files.json lister F2-filene.
