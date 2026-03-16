# Relasjonell universgraf – status v0.7

## Hva som er nytt
- Lokal maksimal kobling av endelige overgangskjerner innen hver event-familie.
- Meeting- og survival-analyse.
- Egen faseprobe som forberedelse til v0.8.

## Hva som er løst
- Vi har nå skilt klart mellom:
  - familywise uniformisering,
  - familywise akseptkobling,
  - og lokal kobling av konkrete hendelser.
- Vi kan derfor si mer presist om hva som er ekte dynamisk divergens og hva som skyldes grov koblingsmetode.

## Viktigste funn i hovedregimet
- Meeting fraction: rank = 0.000, maximal = 0.000
- Mean local overlap: rank = 0.050, maximal = 0.082
- Mean same-descriptor rate: rank = 0.033, maximal = 0.079
- Mean shared token fraction final: rank = 0.064, maximal = 0.216
- Mean unequal time: rank = 41.468, maximal = 39.344

## Tolkning
v0.7 viser ikke at repair allerede er sterk eller vanlig. Men det viser at bedre lokal kobling eksponerer mer felles struktur enn v0.6-lignende rank-baseline gjorde. Det betyr at prosjektet nå har en mer pålitelig måler for hvor mye av divergensen som faktisk er fysisk i modellen.

## Hvor prosjektet står
Prosjektet er nå på et punkt der følgende kan undersøkes i samme ramme:
1. begrenset spredning,
2. repair / meeting,
3. quasi-invariants,
4. og geometri-proksier.

## Neste riktige steg
- v0.8 fasekart over parameterrommet
- koble repair-regimer til energi- og dimensjonsdiskusjonen
- undersøke om repair-vennlige regimer også er de mest spacetime-lignende