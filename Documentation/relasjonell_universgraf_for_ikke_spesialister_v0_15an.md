# Relasjonell universgraf for ikke-spesialister v0.15an

Denne runden spurte ikke bare om high-band dukker opp, men om det faktisk holder seg etter at det har dukket opp.

Det viktigste vi fant er:

- seed `5002161`: `delayed_high_hold_crossover`
- seed `5002240`: `no_high_hold_plateau`
- seed `5002220`: `late_terminal_high_probe`

Den operative dommen er `high_hold_observable_sharpens_overlap_zone`: Overlap-sonen blir skarpere lest av high-hold-observabelen: ett lop faar reell sen high-hold, ett blir igjen uten high-hold, og residual-caset reduseres til en sen terminal high-probe.

Dette gir mer nytte enn bare en ny etikett, fordi residual-caset na leses som en sen terminal high-probe i stedet for et nesten-high-rise lop.
