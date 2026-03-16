# Relasjonell universgraf – status v0.7

## Hva som er nytt
- Lokal maksimal kobling av endelige overgangskjerner innen hver event-familie.
- Meeting- og survival-analyse for å måle repair, ikke bare divergence.
- Direkte sammenligning mellom rank-baseline og maksimal lokal kobling.

## Hva som nå er løst
- Vi skiller nå klart mellom:
  - familywise maksimal kobling av aksept/rejekt,
  - lokal maksimal kobling av konkrete hendelser,
  - og full likhet av hele tilstanden.

## Hovedfunn
- `rank`:
  - meeting fraction ≈ 0.000
  - mean local overlap ≈ 0.050
  - same-descriptor rate ≈ 0.033
  - mean unequal time ≈ 41.468
- `maximal`:
  - meeting fraction ≈ 0.000
  - mean local overlap ≈ 0.082
  - same-descriptor rate ≈ 0.079
  - mean unequal time ≈ 39.344

## Tolkning
Hvis maksimal lokal kobling forbedrer meeting og reduserer unequal time uten å endre marginals, betyr det at v0.6 var metodisk korrekt, men konservativ i hvor mye lokal repair den kunne avdekke.

## Hvor prosjektet står
Prosjektet er nå i stand til å teste tre ting på en disiplinert måte:
1. om en liten forskjell sprer seg med begrenset radius,
2. om noen regimer også reparerer forskjellen,
3. og om de regimene overlapper med regimer som ser geometri-lignende ut.

## Neste naturlige steg
- v0.8: fasekart over parameterrommet med meeting, front-hastighet og quasi-invariants i samme kart.
- koble disse regimene til energi- og dimensjonsdiskusjonen.
