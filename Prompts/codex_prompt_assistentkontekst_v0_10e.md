# Assistentkontekst v0.10e

## Prosjektstatus
Prosjektet modellerer universet som en dynamisk relasjonell graf.
Spacetime, partikler og felt behandles som emergente mønstre i samme underliggende relasjonstype.

## Aktiv metodisk status
- Generatorproblemet fra v0.9b/v0.10 er behandlet i v0.10b–v0.10d.
- Anbefalt generator er nå `fast_balanced / deep`.
- v0.10e gjorde en lokal robusthetstest rundt `band_best`.

## Viktigste nye funn i v0.10e
- `band_best` holdt seg ikke som lokal vinner.
- `band_zero_del` er sterkest på rå mean composite og bootstrap-vinnersannsynlighet.
- `band_small_triad` er sterkest på lokal fokusscore som belønner score + skala-stabilitet.
- `band_small_death` er en relevant sekundær nabo.
- Den operative fronten er nå todelt: `band_zero_del` og `band_small_triad`.

## Ting som ikke må glippe
- Skill mellom generatorfunn og dynamiske kandidatfunn.
- Skill mellom rå mean composite og mer strukturelle/asymptotiske indikatorer.
- Ikke kall `band_best` standardkandidat uten kvalifikasjon.
- Ikke kall noe asymptotisk hvis startnivåene ikke er reelt separert.
