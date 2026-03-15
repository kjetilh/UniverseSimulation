
# README for feature-rom og quasi-invariant-pakken

Denne pakken er neste steg etter de opprinnelige simulatorene.

## Hovedfil
- `relational_universe_feature_lab.py`

Denne filen:
- simulerer lokal grafdynamikk,
- måler et utvidet feature-rom,
- lagrer tidsserier til CSV,
- og kan skrive Markdown-oppsummeringer med quasi-invariantanalyse.

## Dokumentasjon
- `relasjonell_universgraf_feature_rom_og_quasiinvarianter_v0_3.md`

Dette dokumentet forklarer:
- hvorfor feature-rommet ble utvidet,
- hvilke algebraiske identiteter som alltid gjelder,
- hvilke invariants som er dynamiske,
- og hvordan empiriske quasi-invarianter bør tolkes.

## Eksempelkøringer
- `feature_closed_summary.md`
- `feature_open_summary.md`
- `closed_reduced_analysis.md`
- `open_reduced_analysis.md`

Disse filene dokumenterer representative testregimer.

## Codex-prompter
- `codex_prompt_feature_lab_bruk_og_quasiinvarianter.md`
- `codex_prompt_refaktorering_reduced_basis_og_standardisert_analyse.md`

## Anbefalt arbeidsflyt
1. Les v0.3-dokumentet.
2. Kjør `relational_universe_feature_lab.py` i et lukket regime.
3. Kjør deretter et åpent balansert regime.
4. Sammenlikn rå og reduserte analyser.
5. Bruk Codex-promptene til å refaktorere og videreutvikle analysepipen.

## Viktig metodologisk advarsel
En lineær kombinasjon av features som ser nesten konstant ut, er ikke nødvendigvis en fysisk bevaringslov.
Den kan være:
- en definisjonell identitet,
- en artefakt av skala i dataene,
- eller en ekte dynamisk quasi-invariant.

Hele poenget med dette steget er å skille disse tre fra hverandre.
