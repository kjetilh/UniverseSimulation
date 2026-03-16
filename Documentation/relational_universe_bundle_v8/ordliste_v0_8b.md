# Ordliste v0.8b

## Kandidatbånd
Et lite område i parameterrommet der flere nærliggende parameterkombinasjoner ser lovende ut. Dette er sterkere enn ett pent datapunkt, men svakere enn en ferdig teori.

## Ensemble
En samling starttilstander som brukes for å teste om en effekt er robust og ikke bare skyldes én spesiell initialtilstand.

## Naturlig startensemble
Et ensemble der startgrafene ikke er hånddesignet direkte, men er vokst frem av modellens egen dynamikk.

## Burn-in
En innledende evolusjonsfase før selve testen begynner, brukt for å la systemet utvikle mer naturlig struktur.

## Bootstrap-intervall
Et usikkerhetsintervall laget ved å trekke om observasjoner med tilbakelegging mange ganger. Her brukes det som et robusthetsmål, ikke som et endelig statistisk sannhetsstempel.

## Composite score
En samlescore som kombinerer flere delmål. I dette prosjektet er den bare en operativ rangering, ikke en fundamental fysisk størrelse.

## Repair
Hvor godt to nesten like universgrener klarer å beholde eller gjenfinne felles struktur etter en lokal perturbasjon.

## Causal
Hvor begrenset spredningen av forskjellen mellom to grener ser ut til å være, målt med blant annet radius og edge-differanse.

## Quasi-invariant
En størrelse som ikke er eksakt bevart, men som driver sakte nok til å fungere omtrent som en bevart størrelse i et gitt regime.

## Geometrirobusthet
Hvor lite geometri-proksier som spektralradius, clustering og dimensjonsproxy divergerer mellom to nesten like grener.

## beta1
Grafens første Betti-tall eller cycle rank. I denne sammenhengen fungerer det som et mål på hvor mange uavhengige loops grafen inneholder.

## p_del
Sannsynlighetsandel for en lokal slettegren i token-dynamikken. Intuitivt: hvor ofte relasjoner får lov til å brytes direkte.

## p_swap
Sannsynlighetsandel for en lokal omkoblingsgren som flytter en relasjon uten å endre antall kanter like enkelt som sletting/oppretting gjør.

## p_triad
Sannsynlighetsandel for triadisk lukking, altså en lokal regel som bygger en ny relasjon og dermed kan øke clustering og loopdannelse.

## Radius
I perturbasjonslaben: hvor langt ut den observerte forskjellen mellom to grener har spredt seg fra perturbasjonens støtte.
