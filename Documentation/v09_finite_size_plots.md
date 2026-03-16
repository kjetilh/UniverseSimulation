# v0.9 finite-size plottingrapport

## Figurene

- `v09_composite_vs_size.png`: viser om composite-score holder seg oppe eller kollapser når de naturlige starttilstandene blir større.
- `v09_radius_vs_size_linear.png`: viser rå radiusvekst uten skaletransformasjon.
- `v09_radius_vs_size_loglog.png`: er den relevante figuren for sublineær skadeutbredelse, fordi en svakere enn lineær log-log-helning støtter ideen om begrenset frontvekst.
- `v09_overlap_vs_logsize.png`: viser om repair/overlap holder seg stabilt eller synker med størrelse.
- `v09_quasi_vs_logsize.png`: viser om quasi-score forvitrer med log-størrelse.

## Kort tolkning per figur

- Composite-figuren bør leses sammen med kandidatrangeringen. Den nåværende toppkandidaten er `balanced_pdel` med mean composite ≈ 0.703.
- Radius log-log-figuren støtter en tentativ sublineær lesning hvis man fokuserer på toppkandidaten: radius α ≈ 0.068 og øvre bootstrapgrense ≈ 0.631. Dette er fortsatt et numerisk hint, ikke et bevis.
- Overlap-figuren styrker hypotesen bare dersom kurvene ikke faller bratt med størrelse. For toppkandidaten er overlap-slope ≈ 0.217.
- Quasi-figuren svekker hypotesen hvis quasi-score synker raskt med log-størrelse. For toppkandidaten er quasi-slope ≈ -0.324.

## Filer

- `v09_composite_vs_size.png`
- `v09_radius_vs_size_linear.png`
- `v09_radius_vs_size_loglog.png`
- `v09_overlap_vs_logsize.png`
- `v09_quasi_vs_logsize.png`
