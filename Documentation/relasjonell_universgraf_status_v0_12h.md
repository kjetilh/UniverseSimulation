# Relasjonell universgraf status v0.12h

## Kort status

Prosjektet er ikke lenger i en aktiv frontier-tuningfase. Den siste rene frontier-avklaringen er fortsatt `v11e`, der `band_zero_del` vant tydelig over den siste smale bridge-utfordreren.

Etter dette har arbeidet flyttet seg til en strukturfase:

- finn en liten geometrisk eller invariant-lignende basis,
- test om den transfererer,
- test om den er nyttig for screening og billigere arbeidsflyter,
- og skill hele tiden mellom dynamikk, scoringartefakter og rene arbeidskostnadsmodeller.

## Live operative konklusjoner

### Frontier

- Live frontier-standard: `band_zero_del`
- Dette bygger fortsatt på `v11e`, ikke på eldre bridge-runder.

### Geometri / struktur

Det mest robuste så langt er ikke en ny bevaringslov, men et mønster:

- `initial_avg_degree`, `initial_spectral_per_sqrtN` og `initial_dim_proxy` er nyttige normaliserte startfeatures.
- Radius-transferen er lokal, ikke global.
- En liten basis kan være nyttig, men ingen liten basis har vunnet alle oppgaver samtidig.

### Screening / arbeidsflyt

Etter `v12e`-`v12h` er bildet:

- screening-benchmark: `full_basis`
- beste enkle same-budget-kandidat: `spectral_only@0.50`
- mest interessante kostnadsnøytrale utfordrer når screening ikke er gratis: `spectral_plus_dim@0.667`

Dette er en betinget arbeidskonklusjon, ikke ny fysikk.

## Hva som ser robust ut

- Generator-/størrelseskrisen ser ryddet bort i den aktive kjeden.
- `band_zero_del` er en stabil arbeidsforankring.
- `full_basis` holder seg som beste praktiske benchmark for screening.
- Kompakte policyer er relevante nok til å være verdt videre testing.

## Hva som fortsatt er svakt eller betinget

- `spectral_only` er nyttig, men ikke en klar universell vinner.
- `spectral_plus_dim` er viktig som strukturkontroll og blir mer interessant under eksplisitt kostnadsmodell, men er ikke generelt best.
- De eksakte null-driftene i tidligere struktur-runder skal fortsatt ikke overselges som ny matematikk uten forklaring.
- Radius-signalene er foreløpig lokale og regimebundne.

## Riktig lesning av v12h

`v12h` sier ikke at vi nå har funnet den beste billige policyen én gang for alle.

Det den faktisk sier er:

- Hvis screening er billig eller ukjent, behold `full_basis@0.50`.
- Hvis vi bare vil ha en enkel policy uten å endre oppfølgingsbudsjettet, er `spectral_only@0.50` den riktige kandidaten.
- Hvis vi modellerer screening som reelt kostbar, blir `spectral_plus_dim@0.667` en interessant kostnadsnøytral utfordrer.

Dette er derfor et arbeidsregnskap, ikke en ny dynamisk lov.

## Neste naturlige steg

Det neste naturlige steget er ikke ny bred frontier-scan.

Det riktige neste steget er en mer direkte arbeidsflyt-test som måler faktisk praktisk kostnad:

- sammenlign `full_basis@0.50`
- mot `spectral_only@0.50`
- og `spectral_plus_dim@0.667`
- med enten en valgt kostnadsmodell eller virkelig veggklokketid / faktisk oppfølgingsarbeid

Målet bør være å finne ut om enkelheten i den kompakte policyen gir ekte praktisk gevinst, eller bare en ryddigere forklaring.
