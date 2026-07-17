# Bell-teoremet, Bell-ulikheter og observerte kvantekorrelasjoner

## Formaal

Dette notatet skiller tre ting som ofte omtales som om de var det samme:

1. Bell-teoremet er en logisk inkompatibilitet mellom en bestemt klasse lokale
   kausale modeller og alle kvanteprediksjonene.
2. Bell-ulikheter er konkrete, testbare grenser som følger av antakelsene i den
   modellklassen.
3. Observerte kvantekorrelasjoner er endelige eksperimentdata med statistisk
   usikkerhet, systematiske feilkilder og eksplisitte analysevalg.

Skillet er viktig for `UniverseSimulation`: en korrelasjon, stabil struktur
eller ikke-triviell lokal interaksjon i en graf er ikke i seg selv en
Bell-korrelasjon, et bevis paa entanglement eller et brudd paa lokal kausalitet.

## 1. Bell-teoremet

Bell-teoremet handler ikke bare om hvorvidt skjulte variable finnes. Det viser
at ingen teori i en bestemt lokal-kausal modellklasse kan reprodusere alle
kvanteprediksjonene.

En vanlig formulering bruker:

- to adskilte maalesider, Alice og Bob
- lokale innstillinger `x` og `y`
- lokale utfall `a` og `b`
- en mulig felles underliggende tilstand `lambda`

Bell-lokal faktorisering skrives

```text
P(a,b | x,y,lambda) = P(a | x,lambda) P(b | y,lambda).
```

Sammen med blant annet frihet/maaleuavhengighet for innstillingsvalgene, og
korrekt definisjon av forsokspopulasjonen, gir denne faktoriseringen observerbare
begrensninger. Kvanteteori predikerer fordelinger som kan bryte disse
begrensningene.

Teoremet sier derfor ikke uten videre at naturen sender et kontrollerbart signal
raskere enn lyset. Kvanteprediksjonene og eksperimentene respekterer
no-signalling i de observerte marginalfordelingene. Teoremet tvinger i stedet
frem en revisjon av minst en antakelse i den Bell-lokale modellklassen.

Ordene `lokal realisme` brukes ofte som kortform, men de kan skjule hvilke
antakelser som faktisk testes. I presis argumentasjon boer lokal kausalitet,
maaleuavhengighet, utfallsdefinisjon, utvalgsregel og eventuell
deteksjonsantakelse oppgis separat.

## 2. Bell-ulikheter

En Bell-ulikhet er en matematisk konsekvens av Bell-antakelsene, formulert i
observerbare sannsynligheter eller korrelasjoner. Ulikheten er dermed
eksperimentets nullgrense, ikke selve teoremet.

CHSH-ulikheten er et standardeksempel. Med to binare innstillinger paa hver side
og binare utfall defineres

```text
S = E(0,0) + E(0,1) + E(1,0) - E(1,1).
```

Bell-lokale modeller oppfyller

```text
|S| <= 2.
```

Kvanteteori tillater opptil Tsirelson-grensen `2*sqrt(2)` for egnede tilstander
og maalinger. En observert `S > 2` er likevel ikke alene en komplett konklusjon.
Forsoket maa ogsaa ha en gyldig trial-definisjon, kontroll paa postseleksjon,
tilstrekkelig deteksjon, relevante avstands-/timingbetingelser og en statistisk
analyse som passer dataenes avhengighetsstruktur.

Det finnes mange Bell-ulikheter. Valg av ulikhet avhenger blant annet av antall
innstillinger, utfall, parter og hvilke eksperimentelle smutthull analysen skal
taalere. Et brudd paa en bestemt ulikhet avviser den tilsvarende lokale
nullklassen under de oppgitte antakelsene; det beviser ikke enhver detalj i
kvantemekanikkens ontologi.

## 3. Observerte kvantekorrelasjoner

Observerte korrelasjoner er de faktiske registrerte tellingene: valgte
innstillinger, lokale utfall, tidsstempel, heralding/deteksjon og den
preregistrerte regelen for hvilke hendelser som er trials. Fra disse estimeres
`E(x,y)`, `S` eller en annen Bell-statistikk.

Det evidensielle utsagnet er statistisk: hvor usannsynlige er dataene under en
klart definert Bell-lokal nullmodell, gitt analyseprotokollen? Hensen et al.
rapporterte i 2015 en loophole-free test med 245 trials, `S = 2.42 +/- 0.20` og
`p <= 0.039`. Senere fotonforsok rapporterte langt sterkere statistisk evidens
og kombinerte raske innstillingsvalg med hoey deteksjonseffektivitet.

Dette er sterk empirisk evidens mot den testede Bell-lokale modellklassen. Det er
ikke det samme som:

- et direkte bilde av en skjult fysisk mekanisme
- et signal som kan brukes til raskere-enn-lys-kommunikasjon
- et bevis for at bare en bestemt kvantefortolkning er mulig
- et bevis for at enhver observert korrelasjon skyldes entanglement

Kvanteteori forutsier baade selve korrelasjonene og no-signalling-marginalene.
Bell-eksperimentene tester kombinasjonen av fordelinger og kausal struktur, ikke
bare om to dataserier samvarierer.

## 4. Logisk forhold mellom de tre nivaaene

```text
Bell-antakelser
    -> matematisk teorem
    -> observerbar Bell-ulikhet
    -> preregistrert eksperiment og endelige tellinger
    -> statistisk avvisning eller manglende avvisning av lokal null
```

Teoremet avgrenser modellklassen. Ulikheten gjoer avgrensningen maalbar.
Eksperimentet avgjoer hvor godt virkelige data stemmer med grensen. Ingen av
trinnene kan erstattes av det neste: en utledning er ikke et eksperiment, og en
korrelasjon uten riktig kausal/testmessig struktur er ikke et Bell-brudd.

## 5. Claim boundary for UniverseSimulation

Repoet har per v17a ingen Bell-test og ingen etablert entanglement-observabel.
Dagens finite grafsimuleringer har blant annet vist lokale struktur- og
defektsignaler, ikke-triviell kollisjonsinteraksjon og flere negative eller
betingede invariant-/Lorentz-resultater. Disse kan motivere nye observabler,
men de oppfyller ikke Bell-protokollen.

En fremtidig Bell-inspirert gate maatte minst preregistrere:

- en kildehendelse som produserer to lokalt avlesbare delsystemer
- to eller flere lokalt valgte innstillinger per side
- binare eller ellers eksplisitt avgrensede lokale utfall
- en kausal/DAG-basert ikke-innflytelsesbetingelse mellom fjern innstilling og
  lokalt utfall; en grafavstand alene er ikke fysisk spacelike separation
- en innstillingsgenerator som er uavhengig av kildevariablene under nullen
- alle trials, tap og ugyldige utfall uten resultatavhengig postseleksjon
- en frosset Bell-statistikk, nullmodell og sekvensielt gyldig test
- no-signalling-audit av marginalene som separat kontroll

Selv om en intern modell skulle bryte en Bell-ulikhet, ville den foerste
konklusjonen vaere begrenset: modellens genererte fordelinger ligger utenfor den
preregistrerte lokale nullklassen. Det ville ikke alene vise at modellen
beskriver vaart univers, at dens grafavstand er spacetime, eller at dens interne
objekter er fysiske partikler.

## 6. Operativ konsekvens

Den naavaerende forskningsgaten skal ikke hoppe direkte til en Bell-test.
`v17a` kvalifiserte lokal proposal-reversibilitetsalgebra, men ikke tilstrekkelig
finite movement. Neste riktige gate er derfor `v17b`: kvalifiser en mer effektiv,
fortsatt target-uavhengig residual-cycle constructor foer effect-, invariant-,
Lorentz- eller Bell-lignende paastander gjenapnes.

Bell-sporet boer beholdes som et senere, selvstendig evidensprogram. Det trenger
andre datatyper og strengere kausal instrumentering enn dagens struktur- og
sampler-gater.

## Primaerkilder

- J. S. Bell, *On the Einstein Podolsky Rosen paradox* (1964):
  <https://cds.cern.ch/record/111654>
- J. F. Clauser, M. A. Horne, A. Shimony og R. A. Holt, *Proposed Experiment to
  Test Local Hidden-Variable Theories* (1969):
  <https://doi.org/10.1103/PhysRevLett.23.880>
- B. Hensen et al., *Loophole-free Bell inequality violation using electron
  spins separated by 1.3 kilometres* (2015):
  <https://www.nature.com/articles/nature15759>
- L. K. Shalm et al., *Strong Loophole-Free Test of Local Realism* (2015):
  <https://www.nist.gov/publications/strong-loophole-free-test-local-realism>
- M. Giustina et al., *Significant-Loophole-Free Test of Bell's Theorem with
  Entangled Photons* (2015):
  <https://www.nist.gov/publications/significant-loophole-free-test-bells-theorem-entangled-photons>

