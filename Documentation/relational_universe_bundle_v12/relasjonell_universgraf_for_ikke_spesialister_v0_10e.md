# Relasjonell universgraf v0.10e – forklart uten professor-språk

## Hva gjorde vi nå?

Vi tok den modellen som tidligere så mest lovende ut, og testet noen veldig like varianter av den.
Poenget var å se om den gamle favoritten virkelig var best, eller om en nesten lik variant faktisk fungerer bedre.

## Hvorfor var dette viktig?

Tidligere fant vi ut at noen av de store startuniversene våre egentlig ikke var så store som vi trodde.
Det kunne lure oss til å tro at en modell var god eller dårlig bare på grunn av hvordan startgrafene ble laget.

Derfor gjorde vi først generatoren bedre. Så gjorde vi denne testen.

## Hva fant vi?

To ting er spesielt viktige:

1. Startstørrelsene i denne runden ble faktisk det de skulle være: 48, 96, 192 og 256.
2. Den gamle favoritten `band_best` var **ikke** best når vi sammenlignet den med noen veldig like naboer.

I stedet dukket det opp to nye sterke kandidater:

- `band_zero_del`
- `band_small_triad`

Den første ser best ut hvis man bare spør: “Hvilken kandidat scorer høyest totalt?”
Den andre ser best ut hvis man også bryr seg om hvor jevnt og stabilt ting utvikler seg når størrelsen øker.

## Hva betyr det?

Det betyr at prosjektet fortsatt ser lovende ut, men på en mer moden måte.
Vi får ikke bare “samme vinner hver gang”. Når vi gjør testen strengere, blir kandidatene sortert mer presist.

Det er ofte et godt tegn i et forskningsprosjekt.

## Hva betyr det ikke?

Det betyr ikke at vi har en ferdig teori om universet.
Det betyr heller ikke at en av disse kandidatene “må” være riktig.

Det betyr bare at prosjektet nå har et **mer presist sentrum** enn før.

## Hva blir neste steg?

Neste steg bør være å ta de to nye toppkandidatene og teste dem enda grundigere,
med flere kjøringer og noen få ekstra nesten-like varianter rundt dem.
