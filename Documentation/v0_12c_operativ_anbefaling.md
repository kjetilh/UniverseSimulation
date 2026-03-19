# v0.12c operativ anbefaling

Fortsett radius-/surrogatesporet med `spectral_plus_dim` som første arbeidsbasis. Den topper off-anchor transfer med mean skill `0.132` og worst-case `-0.023`.
Behold `spectral_only` som nær kontroll. Hvis disse to holder seg tette i senere runder, har vi trolig et lite plateau av enkle surrogate-baser heller enn én unik vinner.
Behandle samtidig `bridge_0015_0000`-enden som en lokal grensekontroll: når alle basisene blir svakt negative der, er det et tegn på at radius-transferen fortsatt er lokal og ikke bør overselges.
Hold analysen smal: bruk `final_radius_control` som hovedmål og ikke anta at overlap/repair følger med før repoet faktisk viser det.
