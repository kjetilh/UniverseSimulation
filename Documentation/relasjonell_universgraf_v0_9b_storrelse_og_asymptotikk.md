# Relasjonell universgraf v0.9b – størrelse og asymptotikk

## Hva som er nytt i forhold til v0.9

v0.9b utvider samme metodiske oppsett til større naturlige ensembler og skiller eksplisitt mellom rå målinger og skalaekstrapolasjon.

- Tail-analyse bruker bare gruppenivåer med målskala >= 96.
- Ekstrapolasjonene i denne runden er rapportert ved nominell størrelse 256.

## Rå observasjon vs ekstrapolasjon

- Rå observasjon: run- og group-CSV-ene viser hva som faktisk ble målt ved de konkrete ensemble-størrelsene.
- Ekstrapolasjon: asymptotic-summary-CSV-en viser tail-fits og projiserte verdier. Disse er modellbaserte lesninger av dataene, ikke direkte observasjoner.

## Kandidater

| candidate | mean composite | CI low | tail radius α | tail overlap slope | tail quasi slope | pred radius@256 |
| --- | --- | --- | --- | --- | --- | --- |
| balanced_pdel | 0.696 | 0.633 | 0.217 | 0.011 | 0.266 | 4.37 |
| band_best | 0.682 | 0.582 | 0.041 | 0.051 | 0.177 | 3.28 |
| triad_runner | 0.518 | 0.383 | 0.645 | 0.096 | 0.042 | 7.13 |

## Foreløpig beste asymptotiske kandidat

- kandidat: `balanced_pdel`
- mean composite: 0.696
- tail radius α: 0.217
- tail overlap slope: 0.011
- tail quasi slope: 0.266
- predikert radius ved 256: 4.37

## Tolkning

En lovende kandidat i v0.9b bør kombinere akseptabel composite med en lav tail-radius-eksponent og ikke for negativ tail-slope i overlap og quasi. Dette er fortsatt en asymptotisk lesning av begrensede data, ikke et bevis på en endelig storklassesfase.
