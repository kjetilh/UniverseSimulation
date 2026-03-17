# Prosjektoversikt v0.10f

## Kort versjon

Vi bygger og tester en relasjonell universmodell der:

- noder og relasjoner er fundamentale,
- dynamikken er lokal og stokastisk,
- spacetime og partikkel-lignende mønstre skal oppstå emergent,
- og simulatorene brukes til å identifisere stabile, skalerbare dynamiske regimer.

## Hva vi har funnet fram til nå

1. Tidlige brede søk fant lovende regimer, men mange resultater var blandet med generator- og finite-size-problemer.
2. v0.10b–v0.10d løste generatorproblemet nok til at større naturlige ensembler faktisk kunne realiseres.
3. v0.10e snevret inn fronten til `band_zero_del` og `band_small_triad`.
4. v0.10f viste at denne todelingen ikke holder. `band_small_triad` faller ut, og `frontier_diag_mid` tar over som asymptotisk sterk nabo.

## Nåværende operative bilde

- `band_zero_del` er best på rå komposittscore.
- `frontier_diag_mid` er best på focused/asymptotisk score.
- `band_small_triad` bør nå behandles som kontroll, ikke som medvinner.

## Neste naturlige steg

En v0.11 frontier resolution round mellom `band_zero_del` og `frontier_diag_mid`, med:

- flere seeds,
- finere lokal akse i `(p_triad, p_del)`,
- liten `p_swap`-sensitivitet,
- og eksplisitt skille mellom rå dynamisk ytelse og asymptotisk disiplin.
