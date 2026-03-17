# v0.10e regresjonstester og hvorfor de finnes

- `base_separation`: beskytter mot at v0.10e begynner å bruke ikke-separerte startnivåer som om de var reelle skalanivåer.
- `band_best_is_not_top_mean_composite`: beskytter mot at den nye bundle-v12-dommen forsvinner uten at vi oppdager det.
- `pairwise_table_is_consistent`: beskytter bootstrap-sammendraget mot asymmetriske eller inkonsistente sannsynlighetstabeller.
- `focused_score_regenerates`: beskytter kandidat-CSV-en mot intern inkonsistens mellom delscore-feltene og `focused_score`.
