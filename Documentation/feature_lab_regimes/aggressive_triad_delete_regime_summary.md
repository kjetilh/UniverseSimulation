# Aggressive Triad/Delete Regime

Kilder:
- CSV: `aggressive_triad_delete_regime.csv`
- Autoanalyse: `aggressive_triad_delete_regime_auto.md`

## Regime

- steps: 10000
- initial_cycle: 10
- initial_tokens: 6
- r_seed = 0.03
- r_birth = 0.01
- r_death = 0.01
- p_triad = 0.18
- p_del = 0.14
- p_swap = 0.10
- avoid_disconnect = False

Dette er bevisst et hardere regime: hoy triadic closure, hoy delete og moderat swap. Her forventer man ikke metastabil stillhet, men kraftig omorganisering og mulig fragmentering.

## Eksakte algebraiske identiteter

- `beta1 = edges - nodes + components`
- `deg_sq_sum = 2*wedges + 2*edges`

I dette regimet blir de algebraiske identitetene enda viktigere, fordi dynamikken ellers er sa voldsom at rene skalaeffekter lett kan mistolkes som bevaring.

## Eksakte dynamiske invariants

Ingen ikke-trivielle dynamiske invariants ble observert. Alle topologiske tellestorrelsene endrer seg.

## Kandidater til quasi-invariants

Ra SVD peker pa `clustering` som tredje kandidat med liten drift. Det er metodologisk farlig a lese dette som en quasi-invariant, fordi:
- `clustering` er bundet til intervallet [0,1]
- variasjonsrommet er derfor mye mindre enn for `edges`, `c4` eller `deg_sq_sum`
- standardisert SVD fjerner denne dominansen

Nar feature-skalaene standardiseres, forsvinner `clustering` ut av toppkandidatene. De standardiserte nullretningene er igjen dominert av kombinasjoner av:
- `edges`
- `beta1`
- `wedges`
- `deg_sq_sum`

Det er altsa hovedsakelig algebraisk redundans, ikke en ny fysisk bevaringslov.

## Dynamiske resultater som ikke er identiteter

- `tokens` kollapser fra 6 til 1
- `nodes` gaar fra 10 til 289
- `edges` gaar fra 10 til 645
- `components` gaar fra 1 til 17
- `dim_proxy` gaar fra ca. 0.79 til 2.23
- `clustering` holder seg lav, rundt 0.15-0.18

Dette er ikke et rolig metastabilt spacetime-regime. Det er et aggressivt omkoblings- og vekstregime der lokal lukking og sletting sameksisterer med sterk komponentdannelse.

## Tolkning

Dette regimet er mest nyttig som stress-test for analysepipen. Det viser eksplisitt hvorfor man ma kjore bade ra og standardisert SVD. Uten standardisering ville man lett ha kalt `clustering` en quasi-invariant bare fordi den lever pa en liten og bundet skala.
