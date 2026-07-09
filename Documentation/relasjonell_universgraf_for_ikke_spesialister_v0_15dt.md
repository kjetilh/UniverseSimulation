# Relasjonell universgraf for ikke-spesialister v0.15dt

Denne runden bruker ikke ny simulasjon. Den ser paa de klassene vi allerede har funnet, og spoer om det finnes en forsiktig maate aa kjenne dem igjen foer simulasjonen starter.

Det viktigste kravet er at systemet maa kunne si `unknown` naar en startgraf ikke ligner nok paa de repeterte klassene.

- Hovedlesning: `ood_guard_ok_but_class_prediction_weak`.
- Neste steg: `improve_class_profiles_or_add_one_atlas_round` fordi OOD-abstention fungerer, men repeated-class prediksjon er for svak; mer atlas eller bedre profiler trengs.

Hvis denne typen kandidat skal bli nyttig, maa den overleve en fresh holdout. Uten det er den bare et godt kartnotat.
