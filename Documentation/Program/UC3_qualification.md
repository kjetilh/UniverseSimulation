# UC3 — kvalifisering før data

Dato: 2026-09-11. Plan og formål: [UC3_plan.md](UC3_plan.md).
Denne filen dokumenterer instrumentering, ikke kandidatutfall.

## Verifiserte instrumenter

- Ny kjerne: 11 tester bestått, inkludert uttømmende 285 graf/posisjonstilstander
  og 1 120 lovlige overganger for enkle grafer med 1–4 noder (198 slide,
  410 bud, 102 collapse, 410 cut). Lokalitet, invers, enhetsbevaring,
  samlokaliserte enheter, feil uten delvis mutasjon, komponenter, ommerking,
  nye ID-er og adskillelse fra observasjon kontrolleres.
- Ny observatør: 16 tester bestått. Syntetiske, ikke-fysiske testhistorier
  kontrollerer grov bølgeretur med utskiftede deler, frosset struktur, ren
  akkresjon, ommerking, rekkefølge, uobserverte komponenter og lik avstand
  på den deklarerte eksponeringsklokken. De erstatter ikke dynamiske referanser.
- Root kjørte et separat, lovlig **to-perioders positivt fixture**: 64 endringer,
  32 buds og 32 collapses, 16 sluttnoder, to bevarte enheter og primærskår 1.
  Dette er kodekvalifisering, ikke den fulle registrerte kalibreringen.
- Det eksakte antallet tillatte nullord med 16 buds/16 collapses og observert
  høyde minst 8 ved firestegspunkter er 3 631 908. Sampleren bruker heltalls-
  fullføringsantall; kandidatdata brukes ikke til å velge nullbetingelsen.

## Separat fler-enhetsstresstest

Konstruert fixture, ikke kandidatmåling: noder 0…12; to adskilte seks-sykluser
på 0…5 og 6…11, og isolert node 12. Enhetsplasseringer `[0,2,6,8,12,0]`.
Hvert frø bruker `random.Random(seed)` og 1 000 `attempt_step` med vektene
4:1:2:1, uten stopp ved absorpsjon. Ingen kandidatendepunkter beregnes.

| Frø | Endringer | Blokkerte forsøk |
| --- | ---: | ---: |
| 3400 | 44 | 956 |
| 3401 | 53 | 947 |
| 3402 | 52 | 948 |
| 3403 | 14 | 986 |
| 3404 | 65 | 935 |
| 3405 | 63 | 937 |
| 3406 | 80 | 920 |
| 3407 | 116 | 884 |

Sum: **8 000 forsøk, 487 endringer, 7 513 blokkerte, ingen invariantfeil**.
Fordelingen av endringer var slide 209, bud 99, collapse 54 og cut 125.
Kontrollert for hvert forsøk: enheter består, komponenter fusjoneres ikke,
hopp bruker gamle kanter med bare det deklarerte fødselsunntaket, nye ID-er
gjenbrukes ikke, og E−2N+antall_kutt er uendret. Mange blokkerte forsøk viser
en reell mulighet for aktivitetsstans i loven; de er ikke et metastabilitetsfunn.

## Uavhengige innvendinger som endret planen før frys

1. Like fødsels-/kollapsklasser ville gitt automatisk ikke-negativ nodedrift.
   Vektene er valgt før kandidatdata slik at begge driftfortegn er mulige.
2. Globalt tick-lag ville blandet uavhengige etterkommeruniverser og favorisert
   små grafer. Observatøren bruker nå komponenteksponering og initialskalert lag.
3. Ubegrensede Dyck-nullord hadde ofte for liten ekskursjon. Nullordene er nå
   betinget på observert amplitude før sampling. Hver referansegren er fortsatt
   lovlig, men kontrollene kvalifiserer bare det sammensatte instrumentet.
4. Et komponentbrudd kan gi størrelsesfall uten nodesletting. Vinduer får derfor
   egne tellinger av brudd, buds, collapses og kutt samt faktiske forsøksgrenser.

## Runner og endelig regresjon før frys

Runneren besto **19 tester** med bittesmå midlertidige protokoller, ikke de
registrerte forskningskjøringene. De dekker eksakt Dyck-enumerasjon til n=5,
uniforme betingede grenvekter, komponentklokker ved brudd og fremmede hendelser,
observer av/på med samme RNG-bane, budsjetter/sensur, overstyringsvern og
manipulerte hendelser, snapshots, summer, protokoller og referansegater.
Verifikasjonen regenererer alle fem evidensfiler; en endret hash i JSON er
ikke nok til å få en manipulert fil godkjent. Kandidatens kalibrering verifiseres
rekursivt før start og ved replay.

Root kjørte dessuten 32 eksisterende UC1/UC2-regresjoner sammen med de 46 nye:
**78 målrettede tester bestått**. Den separate stresstestens 8 000 forsøk
ble uavhengig reprodusert av root med nøyaktig samme summer og en ekstra
rekonstruksjon av forventede kant-/enhetsendringer etter hvert forsøk.

```sh
python3 -B -m unittest tests.test_local_change_candidate tests.test_local_change_runner tests.test_units_of_change_conformance tests.test_local_growth_candidate tests.test_local_growth_observer tests.test_local_growth_runner
```

Plan, protokoll, kjerne, observatør og runner fryses i en pushet commit før
full måling. Resultatfilene registrerer SHA-256 for alle kjøringsavhengigheter
og planen; senere tolkning skrives i en separat rapport. Ingen full
Documentation-suite ble kjørt.
