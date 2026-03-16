# Relasjonell universgraf v0.10 – større skala og skaleringskollaps

v0.10 løfter skalaen videre enn v0.9b og prøver samtidig en mer eksplisitt kollaps-lesning av radiusfronten.

- inkluderer 384-nivå: nei

| candidate | composite | alpha_large | collapse_cv_tail | best model | stable tail |
| --- | --- | --- | --- | --- | --- |
| macro_stable | 0.641 | -3.753 | 0.003 | linear | 0 |
| band_best | 0.654 | -5.439 | 0.183 | linear | 0 |

Beste kandidat i denne runden er `macro_stable`.
Den har alpha_large ≈ -3.753, collapse_cv_tail ≈ 0.003 og beste radiusmodell `linear`.

## Tolkning

Pre-asymptotiske mønstre viser seg typisk som store hopp i lokale eksponenter og svak kollaps i tailen. Et mer stabilt storskala-regime bør derimot få mindre tail-spredning og et mer konsistent modellvalg.
