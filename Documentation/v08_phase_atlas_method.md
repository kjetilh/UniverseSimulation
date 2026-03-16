# Metodenotat – v0.8 atlasoppgradering

## Hva som er nytt metodisk

- Coarse-atlaset bruker nå bootstrap confidence intervals per gridpunkt.
- Refined-runden er nå en ekte lokal neighborhood-scan rundt coarse-vinnere, ikke bare en rerun av nøyaktig samme punkter.
- En liten `p_del`-akse er åpnet i refinement-runden for å teste robusthet mot svak sletting.
- Paretofront eksporteres til egne CSV-filer for videre plotting og analyse.
- Run-level caching gjør at tidligere punkt/seed-kombinasjoner kan gjenbrukes.

## Hva dette betyr

Atlaset er fortsatt heuristisk, men det er mindre skjørt enn i forrige runde. Vi får nå både et bedre bilde av hvilke punkter som er gode, og hvor robuste de er mot små parameterbevegelser.

Den beste refined-kandidaten i denne runden lå ved `r_birth=0.09`, `r_death=0.02`, `p_swap=0.02`, `p_triad=0`, `p_del=0.02`.

## Hva som fortsatt ikke er løst

- Bootstrap over få seeds er bare en første robusthetsindikator.
- Atlaset er fortsatt et slice, ikke hele parameterrommet.
- Geometrirobusthet er fortsatt proxy-språk, ikke en etablert emergent geometri.
