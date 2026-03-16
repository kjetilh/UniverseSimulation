# v0.9b – hovedfunn og implikasjoner

## Hovedfunn

1. `band_best` ble beste asymptotiske kandidat i v0.9b.
2. `balanced_pdel`, som vant i v0.9, svekkes tydelig når finite-size-risiko måles direkte.
3. `macro_stable` holder seg som en seriøs, men svakere kontrollkandidat.
4. Lokal refinering styrker `band_best` ytterligere.

## Hva det innebærer

Dette innebærer at prosjektet ikke bare finner gode kandidater.
Det begynner også å oppdage når gode kandidater **slutter** å være gode under strengere tester.

Det er en mye viktigere egenskap enn å maksimere én totalscore.

## Hva som er metodisk nytt

v0.9b innfører et klarere skille mellom:

- all-skala-indikatorer,
- stor-skala-indikatorer,
- og tegn på finite-size-artefakter.

## Prosjektmessig betydning

Hvis `band_best` også holder i en v0.10-runde med større skala og flere growth seeds, blir det et mye sterkere signal om at prosjektet faktisk har isolert et interessant arbeidsregime.
