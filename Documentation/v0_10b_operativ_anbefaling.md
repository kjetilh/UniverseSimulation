# Operativ anbefaling videre

## Anbefalt standard nå

### Ensemble-regime
Bruk `fast_balanced` i deep-variant.

### Kandidater
Bruk et smalt sett:
- `band_best`
- `macro_stable`
- én kontrollkandidat, for eksempel `balanced_pdel`

### Hva som ikke bør gjøres
- Ikke kall noe “asymptotisk” hvis realiserte startstørrelser ikke er reelt separert.
- Ikke tolk ekstreme eksponenter fysisk før generatorproblemet er kontrollert.
- Ikke bland generator-score og dynamisk kandidat-score.

## Neste Codex/ChatGPT-oppgave
Bygg v0.10e / v0.11 med:
1. flere growth seeds,
2. flere run seeds,
3. `fast_balanced/deep`,
4. smal kandidatportefølje,
5. tydelig bootstrap og plotting av reelle startstørrelser.
