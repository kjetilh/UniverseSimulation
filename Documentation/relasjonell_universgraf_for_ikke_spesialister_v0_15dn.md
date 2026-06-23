# Relasjonell universgraf for ikke-spesialister v0.15dn

Denne runden handler om en ganske jordna metodefeil vi vil unngaa:
naar vi tester tre mulige lokale inngrep i samme graf, kan det hende at mer enn ett av dem er aktivt.
Da blir det feil aa late som oppgaven alltid er aa finne en enkelt vinner.

v15dn bruker derfor gamle resultater og spoer: kan vi, foer dynamikken kjoeres, se nok i lokal grafmorfologi til aa foreslaa et lite sett av aktive kandidater?
Det er nyttig bare hvis settet er mindre enn aa velge alt.

## Hva vi ikke paastaar

- Vi paastaar ikke at dette er partikler.
- Vi paastaar ikke Lorentz-likhet eller romtid.
- Vi paastaar ikke en invariant.
- Vi bruker dette som strengere instrumentering for aa se om signalet er reproduserbart.

## Hva som teller som fremgang

Fremgang her er ikke et stort ord, men en bedre beslutning:
enten finner vi en liten frossen regel som fortjener fresh holdout,
eller saa laerer vi at dagens pre-run morfologi ikke er nok og maa byttes ut.

## Operativ diagnose

- `input_scope`: `no_new_dynamics_synthesis`.
- `landscape_state`: `multi_active_base_conditioned_landscape`.
- `placement_selector_language`: `single_winner_selector_deprioritized`.
- `metric_screen`: `posthoc_metric_audit_only`.
- `set_rule_screen`: `posthoc_full_coverage_nontrivial_but_false_positive_set_rule`.
- `next_step`: `treat_as_observable_design_not_selector; require_fresh_holdout_if_used`.
