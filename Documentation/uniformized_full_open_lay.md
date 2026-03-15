# Hvor vi er nå – forklart enkelt

## Hva problemet var

I forrige steg kunne vi sammenligne to nesten like universgrener bare så lenge de hadde like mange action-bærere (tokens).
Men så snart en gren fikk flere eller færre tokens enn den andre, begynte de å 'gå på ulike klokker'.
Da ble det uklart om forskjeller spredte seg fordi modellen hadde ekte kausalitet, eller bare fordi vi sammenlignet to systemer som ikke lenger fikk hendelser samtidig.

## Hva vi har gjort nå

Vi bygde derfor en ny metode med en felles overordnet klokke.
Ved hver mulig hendelse trekker vi først hvilken type hendelse som kunne skje, og så avgjør vi om den faktisk skjer i den ene grenen, den andre, begge eller ingen.

Det gjør at begge universgrenene fortsatt lever under samme overordnede 'vær', selv når de lokalt utvikler seg litt forskjellig.

## Hvorfor dette er viktig

Nå kan vi teste om en liten lokal forskjell sprer seg utover gradvis, også i mer realistiske og åpne regimer der antall action-bærere kan vokse og krympe.

## Hva en representativ kjøring viste

- skadefronten endte på radius 2 i kontrollgeometrien
- forskjellen i kantstruktur endte på 45 kanter
- antall tokens mellom grenene skilte seg til slutt med 119.0
- den estimerte effektive front-hastigheten i kontrollgrenen var omtrent -0.01022

Dette er fortsatt ikke en fysisk lov. Det er en laboratoriemåling inne i modellen.
Men det er et viktig steg fordi testen nå er mye renere enn før.

## Hva dette betyr i praksis

Vi er nå kommet til et punkt der prosjektet ikke bare spør om modellen kan lage stabile mønstre, men også om den kan lage en innebygd grense for hvor fort påvirkning sprer seg.

Hvis det holder seg gjennom flere tester, er det et signal om at noe relativitet-lignende kan vokse frem av modellen i stedet for å bli lagt inn utenfra.

## Hva som kommer etterpå

- forbedre selve koblingen slik at den blir enda skarpere
- kartlegge hvilke parameterregimer som gir best tegn til lyskjegle-lignende oppførsel
- koble dette til energidiskusjonen og til spørsmålet om hvordan romdimensjoner kan dukke opp
