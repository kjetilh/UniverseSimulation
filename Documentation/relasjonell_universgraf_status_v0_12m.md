# Relasjonell universgraf status v0.12m

## Kort status

Prosjektet er fortsatt i struktur- og arbeidsflytfasen.
`band_zero_del` er fortsatt frontier-standarden fra `v11e`.

`v12m` er første runde der en dypere adaptiv oppfølgingspolicy faktisk matcher referansen på hovedmålene, samtidig som den er raskere.

## Live operative konklusjoner

### Frontier

- Live frontier-standard: `band_zero_del`
- Dette bygger fortsatt på `v11e`.

### Geometri / struktur

Det viktigste struktursignalet er fortsatt:

- små geometriske basisrom bærer noe nyttig informasjon,
- radius-transferen er lokal,
- og oppfølgingen er fortsatt den operative flaskehalsen.

### Adaptiv oppfølging

`v12m` viser:

- `full_followup` er fortsatt referansen
- `probe2_top_half` er ikke lenger den beste adaptive utfordreren
- `probe3_top_half` er den nye sterke adaptive kandidaten

Det som gjør `probe3_top_half` viktig er:

- `mean_best_hit ~= 0.669`
- `mean_recall ~= 0.669`
- dette matcher `full_followup`
- samtidig er `speedup_vs_ref ~= 1.358`

Det som fortsatt holder igjen en full overgang er:

- `pairwise` er litt svakere enn referansen

## Viktige kontrollfunn

- `probe2_top_two_thirds` og `probe3_top_two_thirds` er ikke ekte vinnere her.
- I denne settingen kollapser de metodisk til `full_followup`, fordi to screenede baser per størrelse og `extend_frac=0.667` betyr at begge blir forlenget.

Dette er viktig, fordi det forteller oss at neste steg ikke bør være “større extend-fraksjon”, men smartere beslutningsregel.

## Riktig lesning

`v12m` sier ikke at arbeidsproblemet er løst én gang for alle.

Det den faktisk sier er:

- vi har nå den første adaptive policyen som matcher referansen på mean hit/recall
- tidsgevinsten er fortsatt reell
- den siste viktige usikkerheten er om den lille pairwise-svikten er akseptabel eller kan forbedres

## Neste naturlige steg

Det neste naturlige steget er en smal valideringsrunde:

- sammenlign bare `full_followup` mot `probe3_top_half`
- og test eventuelt en liten variant med smartere tie-break eller forlengelsesregel

Målet bør være å avklare om `probe3_top_half` kan oppgraderes fra sterk utfordrer til ny operativ arbeidsregel.
