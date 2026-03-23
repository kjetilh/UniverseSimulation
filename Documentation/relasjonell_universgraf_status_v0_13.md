# Relasjonell universgraf status v0.13

## Kort status

Prosjektet er fortsatt forankret i `band_zero_del` som frontier-standard fra `v11e`.

`v13` er ikke en ny frontier-runde. Det er en signalvalidering som spør om geometri- og quasi-invariantsporene fra `v12`-kjeden er sterke nok til at et større valideringssett faktisk vil lære oss noe nytt.

## Live operative konklusjoner

### Frontier

- Live frontier-standard: `band_zero_del`

### Geometri / stabilitet

Det mest robuste i `v13` er:

- `initial_avg_degree` som mest stabil normalisert startfeature
- `initial_spectral_per_sqrtN` som sterkeste ikke-trivielle stabile geometriakse
- `initial_dim_proxy` som fortsatt relevant, men mindre stabil enn de to over

Dette betyr at vi har gode, små kontrollakser for videre strukturarbeid.

### Quasi-invarianter

Det nye i `v13` er ikke en ny bevist lov, men en tydeligere rangering:

- `mean_abs_delta_nodes_rel = 0`
- `mean_abs_delta_beta1_rel = 0`
- `mean_abs_delta_spectral_radius_rel` er den viktigste ikke-trivielle kandidaten

Men den riktige lesningen er fortsatt forsiktig:

- null-driftene kan være regime-/koblingsartefakter
- de bør ikke overselges som ny matematikk før de er testet på tvers av nærliggende regimer

### Redusert basis

`v13` demper optimismen om at mer data alene vil løse radiussporet.

I denne runden er:

- beste lille radius-basis: `spectral_only`
- neste lille radius-kontroll: `spectral_plus_clustering`

Men:

- `q10_skill` for radius er fortsatt negativ
- overlap-signalet er enda svakere

Den operative lesningen er derfor:

- behold de små basisene som strukturspor
- men ikke gjør større valideringssett til førsteprioritet for radius eller overlap akkurat nå

## Hva som ser robust ut

- size-separasjonen er fortsatt ren
- `band_zero_del` er en stabil arbeidsforankring
- stabile startfeatures finnes og kan brukes som kontroller
- `mean_abs_delta_spectral_radius_rel` er verdt å følge videre som ikke-triviell quasi-invariant-kandidat

## Hva som fortsatt er svakt eller betinget

- radius-basisene er fortsatt for ustabile til at større valideringssett er førsteprioritet
- overlap-/repair-signalet er for svakt til å skaleres opp
- null-driftene for `nodes` og `beta1` mangler fortsatt forklaring på tvers av nærliggende regimer

## Neste naturlige steg

Det riktige neste steget etter `v13` er ikke mer workflow-tuning og heller ikke umiddelbart større radiusvalidering.

Det mest naturlige steget er en smal kryssregime-runde som tester:

- om `mean_abs_delta_spectral_radius_rel` holder som quasi-invariant-kandidat utenfor ankerregimet
- om de eksakte null-driftene holder, eller bryter når vi åpner små lokale avvik
- og om de mest stabile startfeatures fortsatt er stabile i samme nærliggende regimefamilie

Kort sagt:

- ja, vi ser tegn til emergent geometri
- ja, vi ser tegn til quasi-invariants
- nei, signalet er ennå ikke sterkt nok til at “mer av det samme” i et større valideringssett er førsteprioritet
