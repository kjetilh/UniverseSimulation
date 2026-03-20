# v0.12h operativ anbefaling

Behold `full_basis@0.50` som standardbenchmark hvis screeningkostnaden er liten eller ukjent.
Behold `spectral_only@0.50` som den viktigste enkle same-budget-kandidaten.
Hvis vi senere kan ansla at screeningkostnaden faktisk er ikke-neglisjerbar, bor vi teste `spectral_plus_dim@0.667` som kostnadsnoytral utfordrer mot referansen.
Det neste naturlige steget er derfor en eksplisitt arbeidsflyt med valgt kostnadsmodell eller virkelig veggklokketid: maal faktisk tid/kostnad for `full_basis@0.50` mot `spectral_only@0.50` og `spectral_plus_dim@0.667`.
