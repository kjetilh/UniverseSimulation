# UniverseSimulation Argumentation Map

Dette dokumentet samler prosjektets argumentasjonskjede i en form som bade mennesker og sprakmodeller kan bruke uten a overtolke.

## Evidensnivaer

All argumentasjon i dette prosjektet bor skilles i fire nivaer:

1. Rapportforankret formalisering
   - det som er eksplisitt formulert i `grundig-research-rapport-16.md`
2. Implementert kode
   - det som faktisk er kjort eller kan kjores i `relational_universe_sim.py`
3. Observerte kjoredata
   - det som kan leses ut av `trajectory.csv` eller nye kjoringer
4. Inferens eller forslag
   - det som virker plausibelt, men ennå ikke er dokumentert i rapport eller kode

Modeller som arbeider med prosjektet ma si hvilket niva en pastand horer til.

## Primitive antagelser

Rapportens minimale antagelser er:

- universet modelleres som en dynamisk graf
- det finnes bare noder og en relasjonstype
- endring skjer gjennom lokale, stokastiske rewrites
- tid er hendelsesbasert, ikke gitt utenfra
- "seeds" er bare operative nar de er koblet til samme komponent
- romtid, partikler og felter skal forklares som emergente storrelser

## Minimal regelkjerne i rapporten

Rapporten foreslar tre lokale regler som formelt utgangspunkt:

- `R_seed`
  - node/leaf birth-death
- `R_slide`
  - lokal edge slide
- `R_tri`
  - triad closure/opening

Poenget er ikke at disse er endelig sannhet, men at et lite regelsett gir et testbart minimumsbilde.

## Hvorfor energi ikke behandles som ett enkelt tall

Rapporten foreslar tre komplementare maater a snakke om energi eller bevaring pa:

- aktivitetsbasert energi
  - total hendelsesrate eller action-kapasitet
- Noether-lignende invariants
  - lineare kombinasjoner av motivtall som faktisk bevares av regelsettet
- monsterenergi
  - en Hamiltonsk-lignende funksjon som styrer sannsynlige makrotilstander

Hovedpoenget er:

- stabilitet krever ikke automatisk en klassisk global energibevaring
- men stabile strukturer blir langt mer plausible hvis visse ladninger eller barrierer er omtrent konservative

## Hva som teller som "partikler" i dette prosjektet

Prosjektet bruker metastabilitet som operasjonell definisjon:

- et monster teller som partikkel-lignende hvis det varer lenge
- det ma kunne overleve sma lokale forstyrrelser
- opplosning ma kreve en kjede av sjeldne hendelser

Dette er en presis og simulerbar definisjon, selv om den ikke i seg selv er kvantemekanikk.

## Hva som ma til for a kunne snakke om emergent romtid

Rapporten legger opp til at dette krever mer enn pen filosofi.

Minstekravene er:

- lokalitetsbundet propagasjon eller effektiv `c_*`
- robuste coarse-grained observabler
- parameterregimer med stasjonare eller metastabile makrostorrelser
- diagnostikker for isotropi, dispersjon og spektral dimensjon

Hvis disse ikke kan males eller stabiliseres, er "emergent spacetime" bare en hypotese.

## Kritiske svakheter som prosjektet ma vaere aapen om

Rapporten gir ogsa sterke advarsler:

- Lorentz-likhet kommer ikke gratis i diskrete grafmodeller
- bounded-degree-mikrostruktur kan vaere for rigid
- korrelasjon er ikke det samme som kvante-entanglement
- coarse-graining ma defineres eksplisitt for a bli testbar fysikk og ikke bare metafor

## Hvordan dagens kode relaterer seg til argumentasjonen

Dagens kode skal leses som et tidlig laboratorium for noen av disse ideene, ikke som en realisering av hele rammen.

Koden kan bidra til a teste:

- om en stor komponent holder seg sammen
- om klustring og loops oppstar
- om visse parametere gir runaway densifisering
- om enkle makrometrikker blir omtrent stabile

Koden kan ikke alene teste:

- DPO-presisjon
- strenge invariants fra rapportens malbilde
- observer-uavhengig emergent geometri
- Lorentz-lik symmetri i sterk forstand

## Testbare hovedsporsmal

Prosjektets sterkeste testbare sporsmal akkurat na er:

1. Finnes det parameterregimer der grafen ikke bare densifiserer ukontrollert?
2. Finnes det langlivede lokale strukturer som kan behandles som metastabile objekter?
3. Kan vi definere observabler som faktisk svarer til rapportens bevarings- og stabilitetsideer?
4. Kan vi lage en tydelig og etterprovbar mapping fra teori til kodeproxy?

## Praktisk regel for modellbruk

Hvis en modell blir spurt om "hva prosjektet viser", bor den som standard svare:

- hva rapporten foreslar
- hva dagens kode kan teste
- hva eksisterende data viser
- hva som fortsatt er apent

Hvis ikke den inndelingen kommer tydelig fram, er svaret for svakt.
