# Relasjonell universgraf status v0.13b

## Kort status

`v13b` gjør én ting klart:

- radius-/basis-sporet er fortsatt for svakt til å være første mottaker av større valideringssett
- men spektral quasi-invariant-sporet er nå sterkt nok til å fortjene målrettet videre validering

Prosjektet er fortsatt forankret i `band_zero_del` som frontier-standard fra `v11e`.

## Live operative konklusjoner

### Frontier

- Live frontier-standard: `band_zero_del`

### Hva v13b faktisk endret

`v13` sa at større valideringssett ikke var førsteprioritet.

`v13b` gjør den lesningen mer presis:

- ikke større valideringssett for radius-basis ennå
- ikke større valideringssett for overlap-/repair-sporet
- men ja til målrettet større validering av den relative spektraldriften

### Null-drifter

De tidligere mest fristende “perfekte” signalene holder ikke gjennom hele den lokale regimefamilien:

- `mean_abs_delta_nodes_rel` bryter under delete-avvik
- `mean_abs_delta_beta1_rel` bryter tydeligere under triad- og delete-avvik

Disse skal derfor nå leses som:

- regime-/koblingsartefakter
- ikke som nye bevaringslover

### Ikke-triviell quasi-invariant

Det sterkeste ikke-trivielle signalet etter `v13b` er:

- `mean_abs_delta_spectral_radius_rel`

Det som gjør den interessant er at den:

- holder seg lav
- ligger top-3 i alle testede lokale regimer
- og ikke kollapser når vi åpner små triad-, delete- og death-avvik

## Hva som ser robust ut

- `band_zero_del` er fortsatt stabil arbeidsforankring
- `initial_avg_degree` og `initial_spectral_per_sqrtN` er fortsatt gode kontrollakser
- spektral relativ drift er nå beste ikke-trivielle quasi-invariant-kandidat

## Hva som fortsatt er svakt eller betinget

- radius-basisene er fortsatt for ustabile til at større validering er førsteprioritet
- overlap-/repair-signalet er fortsatt for svakt til å skaleres opp
- clustering-drift er numerisk skjør og skal ikke leses hardt uten ekstra normaliseringskontroll

## Neste naturlige steg

Det riktige neste steget er en smal `v13c` eller tilsvarende som gjør én ting:

- skaler opp valideringen av `mean_abs_delta_spectral_radius_rel`

Det bør gjøres med:

- litt bredere, men fortsatt lokal regimefamilie
- samme rene size-separasjon
- og eksplisitt sammenligning mot `dim_proxy` som sekundær kontroll

Kort sagt:

- emergent geometri: ja, forsiktig men reelt
- quasi-invariants: ja, nå med ett klart ikke-trivielt hovedspor
- større valideringssett: ja, men målrettet mot spektral quasi-invariant, ikke bredt over alt
