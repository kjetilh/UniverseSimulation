# Relasjonell universgraf for ikke-spesialister v0.15ap

Denne runden sa pa de siste fa stegene for high-band for a se om ulike haleutfall faktisk starter forskjellig allerede like for selve high-forsoket.

Det viktigste vi fant er:

- seed `5002161`: `mixed_threshold_launch`
- seed `5002220`: `compact_terminal_launch`
- seed `5002221`: `premature_probe_launch`
- seed `5002240`: `no_launch_plateau`

Den operative dommen er `pre_high_launch_map_supported`: Pre-high-vinduet deler de fire haleutfallene i et lite launch-kart: blandet threshold-launch, kompakt terminal launch, prematur probe-launch og ingen launch.

Det nye her er at forskjellen mellom ekte hold, terminal probe og mislykket probe ser ut til a finnes allerede i launch-vinduet, ikke bare i halen etterpa.
