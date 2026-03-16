# Relasjonell universgraf v0.9 – enkel forklaring

## Hva er nytt her?

I stedet for bare å spørre hvilke regler som ser bra ut på moderate testgrafer, spør vi nå om de samme reglene fortsatt holder formen når startuniversene blir mye større.

Størrelsene i denne runden er målområder, ikke eksakte fasitsvar. Derfor er det de realiserte startstørrelsene i CSV-filene som teller analytisk.

Vi måler ikke dette med én ny totalscore. Vi ser direkte på fem ting: lokal likhet mellom grenene, hvor langt forskjellen sprer seg, hvor mange kanter som er forskjellige til slutt, og hvor mye to sentrale strukturmål driver.

## Hva ser mest lovende ut akkurat nå?

- Høyest lokal overlap i denne runden kom fra `v08b_top_3` i `moderate` ved mål 128 noder.
- Lavest slutt-radius kom fra `v08b_top_1` i `moderate` ved mål 96 noder.
- Den flatteste enkeltslope-estimatet kom på metrikken `abs_drift_beta1_per_step` for `v08b_top_3` i `moderate`.

## Hvordan dette bør tolkes

Hvis de beste kandidatene fortsatt ser rimelig stabile ut når grafen blir mye større, er det et bedre tegn enn at de bare var pene på små leketøy-eksempler. Hvis de derimot forverres raskt med størrelse, er det en advarsel om at vi kanskje bare har funnet et småskala-fenomen.

Dette steget sier derfor mer om prosjektets modenhet enn om endelig fysikk. Vi prøver å finne ut om de samme mønstrene overlever når vi slutter å holde universet kunstig lite.
