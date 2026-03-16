# Codex-prompt – plotting og heatmaps for v0.8

Bruk `relational_universe_v08_phase_atlas.py` og de tilhørende CSV-filene til å lage en brukerorientert analysepakke.

## Oppgave
Lag et lite plotting-verktøy som:
1. leser coarse- og refined-CSV-ene
2. lager heatmaps for composite-score, repair-score, causal-score, quasi-score og geom-score
3. markerer Paretofront-punkter tydelig
4. genererer en Markdown-rapport som forklarer hvordan figurene skal tolkes

## Tekniske krav
- bruk kun Python-standardbibliotek + `matplotlib` + `numpy`
- ingen seaborn
- ingen subplots i samme figur; én figur per score
- filnavn skal være konsistente og lett gjenbrukbare
- rapporten skal være nøktern: skill klart mellom observasjon, tolkning og spekulasjon

## Viktige forklaringer i rapporten
- hvorfor dette ikke er et fullstendig fasekart over hele parameterrommet
- hvorfor `p_del = 0`-slicen ble brukt i v0.8
- hvorfor Paretofront er nyttig når flere mål konkurrerer
