# Operativ anbefaling v0.15dt

- `input_scope`: `combined_v15dq_v15dr_v15ds_no_new_dynamics` fordi Seed count=16; class counts=multi_active_p0_p2:4;single_active_p2:4;no_active:3;single_active_p1:3;multi_active_p0_p1:1;single_active_p0:1.
- `class_stratification`: `repeated_classes_trainable_singletons_ood` fordi Train classes=multi_active_p0_p2;no_active;single_active_p1;single_active_p2; singletons behandles som OOD/unknown.
- `feature_selection`: `posthoc_family_diverse_candidate` fordi Selected 8 pre-run morphology features. Dette er kandidatdesign, ikke validert selector.
- `leave_one_out_result`: `ood_guard_ok_but_class_prediction_weak` fordi Repeated LOO accuracy=0.214; singleton OOD abstain accuracy=1.000.
- `next_step`: `improve_class_profiles_or_add_one_atlas_round` fordi OOD-abstention fungerer, men repeated-class prediksjon er for svak; mer atlas eller bedre profiler trengs.

- Ikke kall dette validert selector uten fresh holdout.
- Hvis status er holdout-worthy, neste runde maa skrive selector-spec foer dynamikk.
- Hvis OOD-vakten feiler, ikke bruk mer runtime paa samme selector.
- Ikke oppgrader til invariant/Lorentz/partikkel/entanglement-claim.
