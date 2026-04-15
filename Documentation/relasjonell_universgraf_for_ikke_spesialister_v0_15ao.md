# Relasjonell universgraf for ikke-spesialister v0.15ao

Denne runden sa pa en veldig liten grense inne i haleatferden: nar high-band dukker opp, blir det da vaerende, dør det ut igjen, eller kommer det bare for sent?

Det viktigste vi fant er:

- seed `5002161`: `established_high_hold`
- seed `5002220`: `terminal_high_probe`
- seed `5002240`: `no_high_hold_plateau`
- seed `5002221`: `failed_early_high_probe`

Den operative dommen er `terminal_probe_boundary_is_structured`: Den smale high-grensen deler seg na i fire lesbare utfall: ekte high-hold, terminal high-probe, mislykket tidlig high-probe og ingen high-hold.

Det nye her er at vi na kan skille mellom sen ekte high-hold, sen terminal probe og tidlig mislykket probe i stedet for a lese alt som samme slags boundary-uklarhet.
