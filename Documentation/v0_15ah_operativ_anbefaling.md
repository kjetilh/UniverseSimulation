# v0.15ah operativ anbefaling

- `artifact_control`: `clean` fordi Startstørrelsene er rent separert og alle holdout-radene matcher ønsket add_chord-perturbasjon.
- `exception_holdout_status`: `exceptions_mostly_revert_to_main_family` fordi De fleste nærliggende holdouts faller tilbake til `early_fragment_lock`, så hovedkunnskapen er at unntakene er lokale avvik rundt en sterk hovedfamilie.
- `next_step`: `stop_exception_expansion` fordi Neste steg bør ikke være bredere unntaks-scan; vi bør heller bruke dette som støtte for at early-lock-familien er den robuste live-lesningen.

- Les denne runden som en smal holdout-test av unntaksmekanismene, ikke som en ny bred defect-scan.
