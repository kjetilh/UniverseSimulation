# v0.9b regresjonstester og hvorfor de finnes

v0.9b innfører nye indikatorer som er ment a fange finite-size-risiko direkte. Derfor beskytter testene mer enn bare filformat:

- `alpha_jump = alpha_large - alpha_all`
- `linear_margin = rmse_linear - min(rmse_log, rmse_sqrt)`
- lagret `asymptotic_score` må faktisk gi en konsistent rangering
- størrelseprofilene må ha forventet antall målskalaer
- fravær av nok størrelsesdata må håndteres ryddig
- CSV-regenerering skal ikke endre kolonnenavn unødvendig

Den viktigste sanity-checken er sammenligningen mellom `band_best` og `balanced_pdel`: hvis `band_best` ikke lenger slår `balanced_pdel` på `alpha_jump` og `linear_margin`, har den sentrale v0.9b-konklusjonen i praksis blitt brutt.
