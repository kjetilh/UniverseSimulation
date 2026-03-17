# Operativ anbefaling v0.10f

## Behold fast

- Generator: `fast_balanced / deep`
- Størrelsesnivåer: `48, 96, 192, 256`

## Flytt sentrum

Fronten bør nå defineres som:

- `band_zero_del`
- `frontier_diag_mid`

## Nedgrader

- `band_small_triad` fra medvinner til kontroll-/referansekandidat
- `band_best` forblir historisk referanse

## Praktisk neste oppgave

Lag en v0.11 frontier resolution round som:

1. holder generatoren fast,
2. bruker flere growth seeds og flere run seeds,
3. finprøver området mellom `band_zero_del` og `frontier_diag_mid`,
4. tester en liten `p_swap`-akse for zero-del-familien,
5. og rapporterer to ulike vinnerbegreper eksplisitt:
   - rå `mean_composite`-vinner
   - asymptotisk/focused-score-vinner

## Viktig tolkning

Ikke kall `band_small_triad` del av fronten lenger.
Ikke kall `band_zero_del` eneste vinner uten kvalifikasjon.
Det riktige bildet nå er en spenning mellom rå ytelse og asymptotisk disiplin.
