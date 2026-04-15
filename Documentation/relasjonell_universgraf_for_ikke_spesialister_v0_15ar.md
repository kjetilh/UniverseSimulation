# Relasjonell universgraf for ikke-spesialister v0.15ar

Denne runden sa pa hvor langt high faktisk lever etter at det begynner, i stedet for bare hvordan starten eller impulsen ser ut.

Det viktigste vi fant er:

- seed `5002161`: `established_hold_horizon`
- seed `5002220`: `terminal_probe_horizon`
- seed `5002221`: `failed_probe_horizon`
- seed `5002240`: `no_high_presence`

Den operative dommen er `horizon_map_supported`: High-grensen blir na rent lest som et lite horisont-kart: ekte hold-horisont, terminal probe-horisont, failed probe-horisont og ingen high-presens.

Det nye her er at high-grensen kan leses gjennom hvor langt high faktisk lever: holder helt ut, bare blinker til på slutten, glipper tidlig, eller dukker aldri opp.
