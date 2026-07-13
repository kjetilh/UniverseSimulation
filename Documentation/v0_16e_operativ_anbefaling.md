# Operativ anbefaling v0.16e

Status: `pass_to_v16f_cross_map_relation_gate`.

- Behold clock-map-resultatet avgrenset til faktisk simuleringstid, target 1536 og de frosne 128/64/32-opplosningene.
- Ved full pass: test relasjonen mellom clock-map og causal-depth-map paa nye data; ikke kall dem samme geometri ennaa.
- Ved null-ekvivalens: behold clock-map som kontroll og stopp denne observabelretningen uten refit.
- Clock-map er scheduler-order-dependent selv om det er relabel-invariant; ikke presenter det som observer-uavhengig tid.
- Ikke promoter signalet til Lorentz-symmetri, proper time, spacetime eller continuum.
