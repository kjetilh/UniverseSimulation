# Operativ anbefaling v0.15do

## Kortversjon

v15do fant flere post-hoc aktivt-sett-type-screens som kan forklare v15dn sine falske positive,
men nettopp mangfoldet av perfekte regler viser at datasettet er underbestemt.
Dette er en kandidatgenerator, ikke en selector.

## Beste screen

- Regel: `delta_return_t2` / `p0_ge_p1` -> true=`p0_p2`.
- Exact-set-match: `1.000`.
- Precision: `1.000`.
- Burden: `0.500`.

## Neste steg

- Hvis vi bruker dynamisk budsjett: velg og frys en enkel regel eksakt, og test paa minst to nye growth seeds.
- Hvis vi vil vaere mer konservative: legg til en pre-run guard som begrunner valgt metrikfamilie, ikke bare en terskel.
- Ikke refit terskler etter holdout; da mister runden verdi.

## Diagnose

- `input_scope`: `no_new_dynamics_synthesis`.
- `type_scope`: `observed_two_type_landscape_only`.
- `multiplicity_guard`: `underdetermined`.
- `type_discriminator_screen`: `many_posthoc_exact_type_discriminators_found_underdetermined`.
- `next_step`: `choose_one_pre_registered_guard_then_v15dp_two_seed_holdout`.
