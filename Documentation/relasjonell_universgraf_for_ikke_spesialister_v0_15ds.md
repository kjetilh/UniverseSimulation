# Relasjonell universgraf for ikke-spesialister v0.15ds

Denne runden lager et kart over hvilke lokale plasseringer som faktisk blir aktive i nye startgrafer.

Poenget er ikke aa forutsi alt ennaa. Poenget er aa finne ut om landskapet har noen faa gjentagende typer, eller om nye typer fortsatt dukker opp.

- Hovedlesning: `class_frequency_atlas_stabilizing`.
- Neste steg: `stratify_next_selector_by_repeated_classes` fordi Atlaset viser repeterte klasser med begrenset novelty; neste selector bor vaere OOD-first og klasse-stratifisert.

Dette er nyttig fordi en god selector trenger et stabilt klassekart. Hvis kartet stadig faar nye klasser, er det for tidlig aa snakke som om vi har en regel.
