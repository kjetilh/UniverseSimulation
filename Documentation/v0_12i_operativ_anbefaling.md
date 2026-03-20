# v0.12i operativ anbefaling

Behold `full_basis@0.50` som operativ arbeidsbenchmark til en kompakt policy faktisk viser bedre eller lik kvalitet med maelt raskere total arbeidsflyt.
Behold `spectral_only@0.50` som den viktigste enkle kandidaten. Den er fortsatt den naturlige same-budget-sammenlikningen, med `speedup_vs_ref=1.000` og `near_match=0.467`.
Behold `spectral_plus_dim@0.667` som kostnadssensitiv utfordrer bare hvis den maelte workflow-raten faktisk er konkurransedyktig. I denne runden er `speedup_vs_ref=0.750` og `near_match=0.833`.
Neste naturlige steg etter v12i er en liten størrelses-stresstest: sjekk om denne arbeidsdommen holder når vi flytter samme pipeline litt opp i startstørrelse, ikke ved ny frontier-tuning.

