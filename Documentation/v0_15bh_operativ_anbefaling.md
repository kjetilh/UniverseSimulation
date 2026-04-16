# v0.15bh operativ anbefaling

- `rare_load_trigger_status`: `p2_rare_load_trigger_supported` fordi Flere små støtte-/last-akser setter p2 tydelig øverst, men ingen av dem løser samtidig p3 > p1. Det støtter en lokal p2-trigger uten å late som hele rare-rangeringen er løst.
- `best_axis`: `ball2_load` fordi Beste kandidatakse gir p2-margin 5.000.
- `next_step`: `explain_p2_trigger_without_overclaim` fordi Neste steg bør forklare p2-triggeren lokalt, ikke åpne en bredere scan.

- Les denne runden som en smal rare-load-triggerlab, ikke som en ny bred scan.
