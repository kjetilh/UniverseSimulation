# Ordliste v0.9b

## alpha_all
Helningen når vi ser hvordan radius vokser med størrelse over alle målte skalaer.

## alpha_large
Samme type helning, men bare på de største størrelsene. Denne er viktigere når vi vil vite hvordan systemet faktisk oppfører seg asymptotisk.

## alpha_jump
Forskjellen mellom `alpha_large` og `alpha_all`. Stor positiv verdi er et faresignal.

## linear_margin
Et mål på om radius ser mer sublineær enn lineær ut.

## finite-size-artefakt
Et mønster som ser ekte og stabilt ut på små eller moderate størrelser, men som ikke holder når systemet blir større.

## burn-in
En innledende utviklingsfase der systemet får “modne” før selve testen starter.

## natural ensemble
Et startsystem som er vokst frem av modellens egen dynamikk, i stedet for at vi tegner det for hånd.

## quasi-invariant
En størrelse som ikke er helt bevart, men som ofte driver sakte nok til å fungere som en nyttig stabilitetsmarkør.

## causal front
Den omtrentlige fronten for hvor langt en lokal forstyrrelse har rukket å spre seg.

## asymptotic score
En samlescore brukt i v0.9b for å rangere kandidater etter hvor gode de ser ut på stor skala.
