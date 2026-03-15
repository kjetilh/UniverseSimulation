# Codex-prompt – bygg maksimal kobling / uniformisering for birth-death-regimer

Du skal lage neste versjon av perturbasjonslaben slik at den også kan håndtere token birth/death uten å miste metodisk kontroll over koplingen mellom replikaene.

## Problem
Dagens perturbasjonslab virker eksakt i token-lukkede sektorer fordi begge grener har samme totale rate:
R = r_seed + K * r_token.

Når birth/death aktiveres, kan K divergere mellom grenene.
Da holder ikke den nåværende shared-SSA-koblingen lenger.

## Mål
Implementer minst én av følgende strategier:
1. uniformisering med felles dominerende Poisson-klokke,
2. maksimal coupling av hendelseskanaler,
3. en annen presis og godt dokumentert koplingskonstruksjon.

## Krav
- Dokumenter matematisk hva som er eksakt og hva som bare er approksimativt.
- Skill tydelig mellom:
  - shared-noise coupling,
  - maximal coupling,
  - approximate synchronization.
- Behold eksisterende token-lukket modus som referanse.

## Analysekrav
Når den nye koplingen er implementert:
- kjør sammenlikninger mellom lukket og birth/death-aktiv sektor
- mål hvordan causal radius, beta1-drift og regime_L1 endrer seg
- lag markdown-rapport med tolkning

## Leveranser
- ny python-modul eller utvidet eksisterende modul
- README i markdown
- ett teknisk notat som forklarer koplingsmetoden
- eksempelkjøringer med CSV og markdown-oppsummering
