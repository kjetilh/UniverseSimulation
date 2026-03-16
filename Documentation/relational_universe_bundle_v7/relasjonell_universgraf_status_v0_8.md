# Statusnotat v0.8

## Hvor vi er nå

Prosjektet har nå et eksplisitt faseatlas over en valgt, lovende slice av parameterrommet.
Det betyr at vi ikke lenger bare følger intuisjon fra enkeltkjøringer; vi har begynt å rangere regimer systematisk etter flere mål samtidig.

## Hva v0.8 la til

- et coarse grid over kandidatrommet fra v0.7
- fire scorefamilier: repair, causal, quasi og geom
- composite-score og Paretofront
- og en liten refined rerun-runde for de mest lovende coarse-punktene

## Foreløpig konklusjon

Det mest lovende området ligger fortsatt i svakt til moderat åpne regimer med:
- moderat `r_birth`
- liten eller moderat `r_death`
- lav til moderat `p_swap`
- og svært liten `p_triad`

Det er nå mindre sannsynlig at de beste kandidatene ligger i enten helt lukkede eller tydelig mer åpne regimer.

## Toppkandidater fra coarse-scanet

| r_birth | r_death | p_swap | p_triad | repair | causal | quasi | geom | composite | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.02 | 0.02 | 0.02 | 0 | 0.910 | 0.648 | 0.994 | 0.875 | 0.854 | mixed |
| 0.02 | 0.05 | 0.02 | 0 | 0.619 | 0.814 | 0.989 | 0.980 | 0.814 | macro_stable_weak_repair |
| 0.08 | 0.02 | 0.02 | 0 | 0.825 | 0.535 | 0.960 | 0.900 | 0.795 | mixed |
| 0.02 | 0 | 0.02 | 0 | 0.707 | 0.504 | 0.988 | 0.928 | 0.757 | mixed |
| 0.02 | 0.02 | 0.02 | 0.02 | 0.846 | 0.709 | 0.788 | 0.566 | 0.744 | repair_cone_candidate |

## Toppkandidater fra refined rerun

| r_birth | r_death | p_swap | p_triad | repair | causal | quasi | geom | composite | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.08 | 0.02 | 0.02 | 0 | 1.000 | 0.790 | 0.967 | 0.956 | 0.932 | repair_cone_candidate |
| 0.02 | 0.05 | 0.02 | 0 | 0.191 | 0.730 | 0.993 | 0.800 | 0.608 | mixed |
| 0.02 | 0 | 0.02 | 0 | 0.226 | 0.552 | 0.985 | 0.933 | 0.601 | mixed |
| 0.02 | 0.02 | 0.02 | 0 | 0.173 | 0.447 | 1.000 | 0.964 | 0.565 | macro_stable_weak_repair |
| 0.02 | 0.02 | 0.02 | 0.02 | 0.062 | 0.619 | 0.542 | 0.577 | 0.401 | drift_dominant |

## Hva dette innebærer

Det innebærer at prosjektet nå har gått fra "finnes det noen interessante effekter?" til "hvilke regimer er beste kandidater for en mer fysisk tolkning?"

Det er et viktig skifte. Vi er fortsatt ikke ved en fysisk teori, men vi har nå et mer presist regimevalg for de neste undersøkelsene.
