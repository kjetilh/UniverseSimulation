# Operativ anbefaling v0.10e

## Bruk dette videre

### Generator
- Bruk `fast_balanced / deep`.

### Kandidatfront
Flytt sentrum fra `band_best` til:
- `band_zero_del`
- `band_small_triad`

### Sekundær kandidat
- `band_small_death` er fortsatt verdt å beholde som en nær nabo.

### Kandidat som ikke bør være standard lenger
- `band_best` bør nå behandles som referanse, ikke som automatisk standard.

## Praktisk neste oppgave
Bygg en v0.10f / v0.11-runde som:
1. bruker flere growth seeds,
2. bruker flere run seeds,
3. holder generatoren fast,
4. finprøver `p_triad`-aksen rundt `0.00–0.02`,
5. finprøver `p_del`-aksen rundt `0.00–0.01`,
6. eventuelt legger til en liten `p_swap`-akse rundt `0.02`.

## Viktig tolkning
- Ikke kall `band_best` “beste kandidat” lenger uten kvalifikasjon.
- Den operative fronten er nå todelt.
