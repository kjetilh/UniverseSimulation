# Codex-prompt: verifiser matematisk og numerisk konsistens

## Formål
Du skal kontrollere konsistens i den aktive simulatorpakken, ikke lete etter pene narrativer.

## Modellkjerne
Universet er en dynamisk graf med stokastiske lokale omskrivninger. Koblingslaboratoriene sammenligner to nesten like grener for å måle om forskjeller forblir lokale eller sprer seg.

## Viktigste filer
- `relational_universe_local_max_coupling_lab.py`
- `relational_universe_v08_phase_atlas.py`
- `relational_universe_v08b_natural_ensemble_robustness.py`
- `relational_universe_v08b_verify.py`
- `tests/test_v08b_regression.py`

## Hva du må kontrollere
- at marginalsannsynlighetene fortsatt er riktige under kobling,
- at bootstrap-intervaller omslutter sine punktestimater,
- at CSV-strukturer er bakoverkompatible der prosjektet forventer det,
- at naturlige ensemblefamilier faktisk er større enn leketøy-baselinen,
- at påståtte quasi-invarianter ikke bare er algebraiske identiteter i forkledning.

## Tolkning av scorefamilier
- `repair`: numerisk lesning av lokal event-overlap, ikke et bevis på global kontraksjon.
- `causal`: operasjonell skadefront-kontroll, ikke en bevist lyshastighet.
- `quasi`: små drifter i utvalgte størrelser, men bare dynamisk interessante hvis de ikke følger trivielle identiteter.
- `geom`: stabile geometri-proksier; fortsatt bare proxyer.

## Metodiske begrensninger
- Resultatene er seed- og ensembleavhengige.
- Bootstrap over få ensemblefamilier har begrenset oppløsning.
- Små grafer kan gi pene, men villedende mønstre.
- Fravær av kollaps er ikke det samme som bevis for emergent fysikk.

## Arbeidsstil
- Rapporter funn som eksplisitte sjekker med pass/fail.
- Skill strengt mellom algebraiske fakta, numeriske observasjoner og fortolkning.
- Når du tviler, vis tall eller kodebaner i stedet for å generalisere.
