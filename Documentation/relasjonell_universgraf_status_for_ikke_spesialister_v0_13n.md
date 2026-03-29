# Relasjonell universgraf: status for ikke-spesialister v0.13n

## Kort fortalt

Vi leter fortsatt etter tegn til en enkel, stabil geometri i simuleringen som kan gjøre det lettere å forstå eller styre dynamikken.

Det mest interessante sporet akkurat nå er ikke en ny frontier-vinner, men en mulig "nesten-bevart" spektral størrelse:

- hvor lite den spektrale radiusen driver under dynamikken
- sammenlignet med hvor mye en annen kontrollstørrelse (`dim_proxy`) driver

## Hva `v13m` og `v13n` prøvde å avklare

De to rundene testet et veldig smalt område i triad-parameteren der vi har sett både lovende og uklare resultater.

- `v13m` viste at usikkerheten ikke satt i bare ett punkt, men i en liten lokal drop-sone.
- `v13n` testet så den nedre kanten av denne sonen direkte.

## Hva `v13n` faktisk fant

`v13n` ga ikke støtte til at den nedre kanten er en ren lokal overgang.

Det vi ser nå er:

- ett sterkt punkt litt lavere nede
- ett "ganske bra" punkt rett over det
- og deretter en liten sone som fortsatt er blandet og ustabil nok til at vi ikke bør overselge den

## Hva det betyr

Dette er nyttig selv om det ikke er en stor seier.

Det betyr at:

- spektralsporet fortsatt ser ekte ut
- men det er fortsatt lokalt og skjørt
- og vi bør fortsatt ikke bruke et større valideringssett før området er renere avklart

## Ærlig status nå

- Frontier-standard er fortsatt `band_zero_del`.
- Geometri-/invariantsporet lever fortsatt.
- De "for pene" null-driftene for `nodes` og `beta1` skal fortsatt ikke tolkes som nye matematiske lover.
- Den beste ikke-trivielle kandidaten er fortsatt lav spektral drift, men bare som et lokalt og foreløpig signal.

## Praktisk lesning

Vi har altså ikke funnet en ny stor lov ennå.
Men vi har heller ikke mistet sporet.

Prosjektet står nå i en fase der vi prøver å skille:

- ekte lokal struktur
- fra lokal variasjon og samplingstøy

Det er en treg fase, men den er metodisk riktig hvis vi vil unngå å bygge videre på et falskt signal.
