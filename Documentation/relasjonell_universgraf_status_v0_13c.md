# Relasjonell universgraf status v0.13c

## Kort status

`v13c` bekrefter at spektral relativ drift fortsatt er det sterkeste ikke-trivielle quasi-invariant-sporet vi har, men runden demper samtidig optimismen fra `v13b`.

Prosjektet er fortsatt forankret i `band_zero_del` som frontier-standard fra `v11e`.

## Live operative konklusjoner

### Frontier

- Live frontier-standard: `band_zero_del`

### Stabile kontroller

De mest nyttige stabile kontrollaksene i `v13c` er fortsatt:

- `initial_avg_degree`
- `initial_spectral_per_sqrtN`
- `initial_dim_proxy`

Dette betyr at geometri-/invariantsporet fortsatt har et lite, brukbart sett kontroller for videre lokal testing.

### Null-drifter

`v13c` bekrefter det `v13b` allerede antydet:

- `mean_abs_delta_nodes_rel` er ikke en generell lov
- `mean_abs_delta_beta1_rel` er ikke en generell lov

De skal derfor fortsatt leses som:

- regime-/koblingsartefakter
- ikke som nye bevaringslover

### Spektral quasi-invariant

Det sterkeste ikke-trivielle sporet i `v13c` er fortsatt:

- `mean_abs_delta_spectral_radius_rel`

Men den riktige lesningen er nå mer forsiktig enn i `v13b`:

- spektraldriften holder seg lav i hele den lokale familien
- den slår ofte `dim_proxy`
- men ikke så rent og ensidig at den alene rettferdiggjør et større valideringssett allerede nå

### Dim-kontroll

`dim_proxy` holder seg naer nok i flere regimer til at spektralsporet fortsatt ma leses som:

- lovende
- lokalt robust
- men fortsatt delvis uavklart

## Hva som ser robust ut

- `band_zero_del` er fortsatt stabil arbeidsforankring
- size-separasjonen er fortsatt ren
- `initial_avg_degree` og `initial_spectral_per_sqrtN` er fortsatt gode strukturkontroller
- spektral relativ drift er fortsatt beste ikke-trivielle quasi-invariant-kandidat

## Hva som fortsatt er svakt eller betinget

- null-driftene bryter fortsatt off-anchor
- spektralsporet er fortsatt ikke skarpt nok til a sta alene som neste store valideringsmal
- radius-/basis-sporet er fortsatt svakere enn quasi-invariantsporet
- overlap-/repair-sporet er fortsatt for svakt til a skaleres opp

## Neste naturlige steg

Det riktige neste steget etter `v13c` er ikke et stort nytt valideringssett.

Det riktige neste steget er en ny, smal lokal runde som:

- holder `band_zero_del` som anker
- tester spektral relativ drift mot et litt bredere, men fortsatt kontrollert kryssregime-sett
- bruker `dim_proxy` som sekundær kontroll
- og prover a gjore spektralsporet skarpere før vi bruker mer budsjett pa storre validering

Kort sagt:

- emergent geometri: ja, fortsatt forsiktig men reelt
- quasi-invariants: ja, med spektraldrift som beste ikke-trivielle kandidat
- større valideringssett: fortsatt `not_yet`
