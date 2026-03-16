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

| r_birth | r_death | p_swap | p_triad | p_del | repair | causal | quasi | geom | composite | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.08 | 0.02 | 0.02 | 0 | 0 | 0.766 | 0.571 | 0.936 | 0.852 | 0.768 | mixed |
| 0.05 | 0 | 0.02 | 0.02 | 0 | 0.807 | 0.724 | 0.781 | 0.708 | 0.761 | repair_cone_candidate |
| 0.08 | 0 | 0.06 | 0 | 0 | 0.824 | 0.476 | 0.924 | 0.832 | 0.758 | mixed |
| 0.02 | 0.02 | 0.02 | 0 | 0 | 0.552 | 0.707 | 1.000 | 0.895 | 0.749 | macro_stable_weak_repair |
| 0.02 | 0 | 0.02 | 0 | 0 | 0.581 | 0.612 | 0.988 | 0.877 | 0.729 | macro_stable_weak_repair |

## Toppkandidater fra refined rerun

| r_birth | r_death | p_swap | p_triad | repair | causal | quasi | geom | composite | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.09 | 0.02 | 0.02 | 0 | 0.914 | 0.868 | 0.953 | 0.922 | 0.912 | spacetime_candidate |
| 0.07 | 0.01 | 0.02 | 0 | 0.892 | 0.689 | 0.991 | 0.923 | 0.867 | spacetime_candidate |
| 0.08 | 0.03 | 0.02 | 0 | 0.875 | 0.716 | 0.954 | 0.954 | 0.867 | spacetime_candidate |
| 0.09 | 0.03 | 0.02 | 0 | 0.914 | 0.731 | 0.895 | 0.894 | 0.860 | mixed |
| 0.09 | 0.02 | 0.02 | 0 | 0.774 | 0.891 | 0.836 | 0.959 | 0.853 | spacetime_candidate |

## Hva dette innebærer

Det innebærer at prosjektet nå har gått fra "finnes det noen interessante effekter?" til "hvilke regimer er beste kandidater for en mer fysisk tolkning?"

Det er et viktig skifte. Vi er fortsatt ikke ved en fysisk teori, men vi har nå et mer presist regimevalg for de neste undersøkelsene.
