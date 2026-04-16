# v0.15bi operativ anbefaling

- `load_stabilizer_status`: `load_without_stabilization_supported` fordi p2 topper alle små last-akser, mens p1 topper alle små stabiliseringsakser. Det støtter at rare-load-flippen ligger i høy last uten tilsvarende stabilisering.
- `best_load_axis`: `ball2_load` fordi Beste lastakse gir margin 5.000.
- `best_stabilizer_axis`: `full_stabilizer` fordi Beste stabiliseringsakse gir margin 0.511.
- `next_step`: `explain_missing_stabilizer` fordi Neste steg bør forklare hva p2 mangler av stabilisering relativt til p1.

- Les denne runden som en smal p2-vs-p1-grenseforklaring, ikke som en ny bred scan.
