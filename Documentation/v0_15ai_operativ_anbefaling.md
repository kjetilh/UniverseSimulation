# v0.15ai operativ anbefaling

- `artifact_control`: `clean` fordi Startstorrelsen er rent separert og alle run i denne runden matcher onsket add_chord-perturbasjon.
- `coarse_band_status`: `early_lock_has_structured_band_ladder` fordi Hovedfamilien er mye bedre lest som coarse low/mid/high-band med litt naboband-drift enn som ett eksakt shell-komponenttall, og dette holder ogsa pa holdout-run som falt tilbake til hovedfamilien.
- `band_mode_note`: `descriptive` fordi Ankerrun domineres mest av `mid`, mens holdout-revert-rundene domineres mest av `low`.
- `next_step`: `probe_band_onset_and_switching` fordi Neste steg bor forklare nar run larser seg inn i low, mid eller high band, og hvilke run som bare driver mellom to naboband.

- Les denne runden som en observabeltest inne i `early_fragment_lock`, ikke som en ny defect-familie-scan.
