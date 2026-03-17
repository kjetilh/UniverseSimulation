# Relasjonell universgraf v0.10f – forklart for ikke-spesialister

## Hva vi prøver å gjøre

Vi prøver ikke å bevise hele universet i kode. Vi prøver å se om en veldig enkel idé kan gi opphav til noe som minner om fysikk:

- alt består av relasjoner,
- små lokale hendelser endrer disse relasjonene,
- og store, stabile mønstre kan da kanskje oppføre seg som rom, tid og partikkel-lignende ting.

## Hva som var spørsmålet i denne runden

Vi hadde to kandidater som så lovende ut i forrige runde:

- en variant vi kalte `band_zero_del`
- og en variant vi kalte `band_small_triad`

Nå ville vi se om begge fortsatt var gode når testen ble litt strengere.

## Hva vi fant

Det skjedde noe interessant:

- `band_small_triad` holdt **ikke** stand.
- En tredje kandidat, `frontier_diag_mid`, kom inn og viste seg å være bedre enn `band_small_triad` på den typen mål som handler om roligere og mer skalerbar oppførsel.
- Samtidig er `band_zero_del` fortsatt best på ren “rå ytelse”.

## Oversatt til enkelt språk

Vi har nå to forskjellige typer vinnere:

1. **Den som presterer best her og nå**: `band_zero_del`
2. **Den som ser mest lovende ut når systemet blir større og oppfører seg mer ryddig**: `frontier_diag_mid`

Det er faktisk nyttig. Det betyr at prosjektet ikke bare følger gamle spor av vane. Når vi tester hardere, får vi et tydeligere bilde.

## Hva det betyr videre

Vi skal nå ikke lenger bruke like mye tid på `band_small_triad`.
Neste runde bør heller finne ut hvilken av disse to som virkelig er best:

- `band_zero_del`
- `frontier_diag_mid`

Det er et mer presist og mer interessant spørsmål enn vi hadde før.
