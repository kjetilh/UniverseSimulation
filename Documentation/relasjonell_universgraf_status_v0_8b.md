# Statusnotat v0.8b

## Kort status

v0.8b er fullført som en lokal p_del-refinement og ensemble-robusthetstest rundt v0.8-kandidatbåndet.

## Hva som er nytt i forhold til v0.8

- `p_del` er nå åpnet lokalt i kandidatregionen.
- vurderingen skjer ikke lenger bare på små sykler, men også på større, modellgenererte startensembler.
- kandidatene evalueres med bootstrap-intervaller for naturlig composite score.

## Foreløpig hoveddom

Prosjektet går fortsatt i en lovende retning. Beste kandidat i denne runden hadde natural mean composite ≈ 0.718 og bootstrap lower bound ≈ 0.659.

## Metodisk betydning

Det er viktigere at kandidatbåndet overlevde strengere testing enn nøyaktig hvilket punkt som kom øverst akkurat her. Det betyr at modellen foreløpig blir mer selektiv når kravene skjerpes, ikke mindre meningsfull.

## Neste steg

v0.9 bør utvide naturlige ensembler videre og legge på mer eksplisitt skalaanalyse: større grafer, flere burn-in-regimer, og bedre måling av hvordan kausalradius og quasi-invariants skalerer med startstørrelse.
