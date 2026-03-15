# Relasjonell universgraf – status v0.6

## Hva som er nytt
- Åpne regimer med state-dependent `birth` og `death` er nå eksplisitt inne i kausalitetslaben.
- To grener kan fortsatt sammenlignes under én felles potensial-klokke via familywise uniformization.
- Koden støtter nå persistent node- og token-ID, slik at divergens kan spores mer presist.

## Hva som er løst
- Vi har fjernet den viktigste metodiske svakheten i v0.5 for åpne regimer: ulik totalrate mellom grenene.
- Vi kan nå skille mellom:
  - ekte dynamisk divergens,
  - feature-drift,
  - og ren klokke-deskronisering.

## Viktigste funn
- Token-open moderate regimer gir i snitt:
  - max radius ≈ 5.20
  - both-accept fraction ≈ 0.873
  - one-sided fraction ≈ 0.127
- Fullt åpne moderate regimer gir i snitt:
  - max radius ≈ 3.15
  - both-accept fraction ≈ 0.585
  - one-sided fraction ≈ 0.415

## Tolkning
- Litt åpenhet ser ut til å være fruktbart.
- For mye åpenhet ser ut til å drive forskjellen over i token- og feature-drift raskere enn i pen, geometrisk frontutbredelse.

## Hvor prosjektet står
Prosjektet er nå i en fase der det faktisk går an å:
1. sammenligne regimer systematisk,
2. snakke mer presist om emergent causal cone,
3. og forberede en seriøs overgang til fasekart og parameterrom.

## Neste steg
- v0.7: maksimal lokal kobling innen hver familie
- parameterfasekart
- kobling til energi- og dimensjonsspørsmålet
