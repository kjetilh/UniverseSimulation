# v0.12f operativ anbefaling

Bruk `full_basis` som budsjettbenchmark og `spectral_only` som kompakt arbeidspolicy. Hvis vi trenger den sterkeste offline screeningkurven, holder `full_basis` seg som referanse.
Hvis vi trenger en enklere policy, er `spectral_only` fortsatt den riktige lille kandidaten. Den ma leses mot budsjett-tallene: `budget_to_match_full_basis_hit50 = 0.500` og `budget_to_match_full_basis_recall50 = 0.667`.
Denne anbefalingen er bevisst forsiktig. `spectral_only` slar `spectral_plus_dim` i denne policy-oppgaven, men curve-wide ligger den fortsatt naert random-baseline og bor derfor behandles som en lovende, men ikke endelig screeningregel.
Neste naturlige steg er a teste denne kompakte policyen i en enda mer direkte kandidatpipeline: behold bare topp-fraksjonen og mael faktisk hvor mange oppfolgingskjoringer vi unngar ved samme eller nesten samme treffrate.
