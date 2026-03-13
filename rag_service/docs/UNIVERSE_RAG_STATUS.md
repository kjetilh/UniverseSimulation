# UniverseSimulation RAG Status

Dette dokumentet beskriver hvor prosjektet faktisk er na, og hva den nye `rag_service`-pakken skal hjelpe med.

## Status na

Per 2026-03-13 har repoet fire sentrale deler:

- `Documentation/grundig-research-rapport-16.md`
  - den formelle og konseptuelle hovedrapporten
- `relational_universe_sim.py`
  - en kjorbar toy-simulator av en dynamisk, urettet graf
- `trajectory.csv`
  - en eksisterende baseline-kjoring fra simulatoren
- `rag_service/`
  - den nye prosjektspesifikke RAG-tjenesten med docs, prompts og cases

## Hva som er levert med denne RAG-en

Denne RAG-en etablerer et eget korpus for:

- prosjektstatus
- teori og argumentasjon
- verktøybruk
- modellinstruksjoner og promptprofiler

Det viktigste er at den gir sprakmodeller et eksplisitt skille mellom:

- rapportens formelle ramme
- dagens implementerte toy-modell
- observerte resultater i `trajectory.csv`
- forslag til videre arbeid

## Hva rapporten spesifiserer

Rapporten formaliserer et mye strengere malbilde enn dagens kode:

- mikrotilstander som enkle, urettede grafer
- lokalitet via grafavstand
- CTMC/SSA-semantikk
- et minimalt regelsett:
  - `R_seed`
  - `R_slide`
  - `R_tri`
- energibegreper som aktivitetsrate, invariants og monsterenergi
- metastabilitet som definisjon av emergente "partikler"
- et testprogram for kausale kjegler, Lorentz-likhet og coarse-graining

## Hva dagens kode faktisk implementerer

Dagens simulator er en toy-approximation, ikke en direkte DPO-implementasjon av rapporten.

Det som faktisk finnes i `relational_universe_sim.py`:

- en enkel urettet graf med adjacency-sets
- mobile tokens som traversal-mekanisme
- lokale rewrites via:
  - sletting av traversert kant
  - triadic closure
  - lokal rewire
  - seed attachment
- kontinuerlig tid via en Gillespie-lignende SSA
- enkel logging av:
  - `nodes`
  - `edges`
  - `tokens`
  - `avg_degree`
  - `clustering`
  - `eff_dim`

Det som ikke finnes enn:

- eksplisitt DPO-rule-engine
- egen logging av `R_seed`, `R_slide`, `R_tri` som distinkte hendelsestyper
- logging av invariants som `|E|-|V|` eller `beta_1`
- kausal-kjeglemaaling
- spektral dimensjon fra random walk
- systematisk sweep over parameterrom

## Hva baseline-dataene tyder pa

`trajectory.csv` inneholder 400 loggpunkter fra en lang kjoring opp til 200000 hendelser.

Fra filen:

- noder: `30 -> 838`
- kanter: `87 -> 7096`
- gjennomsnittlig grad: `5.8 -> 16.94`
- clustering holder seg omtrent i intervallet `0.25 - 0.41`
- `eff_dim` blir etter hvert endelig og ligger ved siste punkt rundt `1.14`

Dette tyder pa:

- en stor sammenhengende komponent vedvarer
- systemet densifiserer tydelig under default-parametrene
- dagens modell viser lokal klustring, men ikke grunnlag for sterke paastander om emergent romtid

## Hvorfor vi trenger denne RAG-en

For dette prosjektet er det lett for en modell a blande sammen:

- hva rapporten argumenterer for i prinsippet
- hva dagens toy-kode faktisk kan teste
- hva baseline-kjoringen faktisk viser

RAG-en er laget for a redusere akkurat den forvirringen.

## Viktigste gap akkurat na

Det viktigste gapet er ikke manglende ideer, men manglende kobling mellom ide og maaling:

1. Rapporten beskriver observabler og testprogram mye rikere enn koden gjor.
2. Koden gir bare en grov approximation av regelsettet.
3. Eksisterende resultater er enkeltskjoringer, ikke robuste eksperimentserier.
4. Det finnes forelopig lite maskinlesbar dokumentasjon om hvordan verktøyene bor brukes.

## Narmeste neste steg

De mest realistiske neste stegene er:

1. logg regeltyper og bevaringskandidater eksplisitt i simulatoren
2. bygg et lite sweep-oppsett for parameterregimer
3. legg til diagnostikker for runaway densifisering vs metastabile klustre
4. etabler en tydelig mapping mellom rapportens begreper og kodens faktiske proxies
5. bruk denne RAG-en som kildegrunnlag for videre design og evaluering
