# Operativ anbefaling v0.16b

Status: `pass_to_v16c_coarse_graining_pilot`.

- Behold event-DAG-resultatet avgrenset til deklarert read/write-support og samplede historikker.
- Ved full pass: gaa til en liten, preregistrert tre-skala v16c coarse-graining-pilot.
- Ved eksakt DAG-pass men stabilitetsfail: raffiner bare den svake coarse-observabelen; ikke endre event-support.
- Ved replay/relabel-fail: reparer minste manglende supportavhengighet og rerun v16b.
- Ikke promoter event-DAG til spacetime, Lorentz-symmetri eller universell kausal orden.
