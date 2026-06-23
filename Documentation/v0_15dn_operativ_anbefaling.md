# Operativ anbefaling v0.15dn

## Kortversjon

v15dn flytter add_chord/1024-problemet fra single-winner selector til aktivt-sett-landskap.
Dette er riktig retning fordi v15dm viste at samme base kan ha mer enn en aktiv placement.

## Status

- Landskap: `multi_active_base_conditioned_landscape`.
- Set-regel: `posthoc_full_coverage_nontrivial_but_false_positive_set_rule`.
- Neste steg: `treat_as_observable_design_not_selector; require_fresh_holdout_if_used`.

## Praktisk anbefaling

- Beste ikke-trivielle screen akkurat naa er `local_ball3_beta1`/`low`/`top_k=2` med coverage `1.000` og burden `0.667`.
- Ikke kjor fresh holdout foer vi har bestemt om denne regelen skal fryses uten videre justering.
- Unngaa aa refitte genealogy-intensity eller dynamiske responser inn i selector-claim; de er response/audit, ikke pre-run.
- Hvis vi bruker ny dynamikk, boer den teste en frossen aktivt-sett-regel paa minst to nye growth seeds.
