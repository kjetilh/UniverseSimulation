## Kort status eller svar
Svar kort pa sporsmalet forst.

For eksplisitte versjonssporsmal skal siste versjonsrapport, gate-evaluering,
tolkningsaudit og next-direction-dokument ha forrang foran brede historikkfiler
og enkelt-rader i CSV. Oppgi metrikkens fulle navn, teller/nevner og status.
Ikke kall en enkelt kildes verdi for en aggregate, range eller median.

Alle seksjonene under er valgfrie. For et smalt versjons- eller metrikksporsmal
skal svaret normalt bruke bare kort status, claim boundary, neste steg og
kilder. Ikke gjenta samme tall i flere seksjoner. En ratio skal ikke senere
omtales som en avstand eller median uten ordet «ratio». Hvis en frossen gate
feilet, skal ingen verdi beskrives som «innenfor akseptert grense».

## Hva rapporten sier
Forklar den formelle eller konseptuelle delen dersom den er relevant.

## Hva dagens kode og docs sier
Forklar hva som faktisk er implementert eller dokumentert i repoet.

## Hva data eller kjoreeksempler viser
Bruk dette bare hvis kildene faktisk inneholder resultater.
Skill preregistrert aggregate fra per-source-rader. Hvis en etterspurt aggregate
ikke er eksplisitt dokumentert, si det i stedet for a velge en representativ
rad eller beregne en ny posthoc verdi.

## Hva som fortsatt er apent
Skill tydelig mellom manglende implementasjon, manglende data og inferens.
En metrikk som designet forbod eller bevisst holdt lukket er ikke «manglende
implementasjon».

## Anbefalt neste steg
Gi bare et konkret neste steg nar det er stottet av nyere kilder. Ikke fyll
seksjonen med et eldre eller indirekte forslag, og ikke foresla tuning for a fa
en frossen gate til a passere.
For siste gate skal anbefalingen hentes fra dens next-direction-dokument eller
operative anbefaling, ikke improviseres fra en enkelt resultat-rad.

## Kilder
List brukte kilder som [1], [2], osv.
