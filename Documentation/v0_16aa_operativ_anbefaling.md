# Operativ anbefaling v0.16aa

Status: `candidate_selected_not_validated`.

- Frys `exposure_matched_local` med `rho_seed=0.000503953815`.
- Behold `current_global` som baseline og `preparation_only` som mekanismekontroll.
- Kjoer en fresh matched scheduler-holdout uten refit.
- Ikke endre core anchor eller start v16b event-DAG foer holdouten og ny locality-gate passerer.
- Ikke les den in-sample exposure-matchen som dynamisk eller fysisk validering.
