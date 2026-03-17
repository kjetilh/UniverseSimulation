# Status v0.10e

## Hovedstatus

v0.10e er en fokusert lokal robusthetstest rundt `band_best` under anbefalt generatorregime `fast_balanced / deep`.

## Viktigste funn

- Generatornivåene 48, 96, 192 og 256 ble realisert rent i denne runden.
- `band_best` holder seg **ikke** som lokal vinner.
- `band_zero_del` er sterkest på rå mean composite og bootstrap-vinnersannsynlighet.
- `band_small_triad` er sterkest på den lokale fokusscoren som kombinerer score, skala-stabilitet og mindre negativ `quasi_large`.
- Prosjektets lokale sentrum bør derfor flyttes til en **to-kandidat-front**:
  - `band_zero_del`
  - `band_small_triad`

## Metodisk vurdering

Dette er et godt tegn. Når generatorartefakter er redusert og man bare gjør en lokal kandidatperturbasjon,
endrer rangeringen seg på en måte som er både forståelig og informativ.

## Neste steg

Bygg v0.10f / v0.11 rundt denne fronten, ikke rundt `band_best` alene.
