# Operativ anbefaling v0.15cz

- `artifact_control`: `clean` fordi Startstorrelse er ren og alle requested add_chord-perturbations matcher faktisk perturbasjon.
- `pre_registration_control`: `frozen_score_applied` fordi Score-spec er fit paa v15cw/v15cx calibration rows og brukt uten refit paa v15cz holdout.
- `primary_test`: `pre_registered_intensity_inconclusive_balance` fordi Ikke nok balansert decisive data for confirmatory test: decisive=23, established=22, no_horizon=1, mixed=1; AUC=1.000, p=0.043.
- `next_step`: `run_pre_registered_extension_or_report_inconclusive` fordi Forleng bare etter den pre-registrerte balanse-regelen; ikke endre score eller metric.

- Score ble frosset fra v15cw/v15cx foer v15cz-holdout-evaluering.
- Ikke refit score, normalisering eller metric etter aa ha sett holdout-resultatet.
- Ikke oppgrader dette til partikler, global invariant, Lorentz-likhet eller entanglement.
