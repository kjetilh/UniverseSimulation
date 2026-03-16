# v0.8b – hovedfunn og implikasjoner

## Kort konklusjon

v0.8b styrker prosjektet metodisk. Det mest lovende området i parameterrommet overlevde overgangen fra små leketøytilstander til større, modellvokste startensembler. Samtidig flyttet den mest robuste kandidaten seg.

## Det viktigste skiftet fra v0.8 til v0.8b

I v0.8 kom et regime nær
`(r_birth, r_death, p_swap, p_triad, p_del) = (0.08, 0.02, 0.02, 0.00, 0.00)`
ut som vinner i den aktuelle slicen.

I v0.8b, når vi rangerer etter **bootstrap-lower-bound på naturlig composite score**, er den sterkeste kandidaten i stedet

`(0.02, 0.00, 0.02, 0.00, 0.01)`

med

- mean natural composite ≈ **0.730**
- bootstrap lower bound ≈ **0.688**
- mean natural radius ≈ **2.867**
- mean natural overlap ≈ **0.660**

Dette betyr at kandidatbåndet ikke kollapset, men at optimum ble mer sensitivt for større og mer naturlige starttilstander enn v0.8 alene kunne vise.

## Det kanskje viktigste resultatet

Det finnes **ingen enkelt parameterkombinasjon som dominerer alle naturlige ensembler samtidig**.

De tre naturlige ensemble-vinnerne var:

| Ensemble | Beste punkt |
| --- | --- |
| natural24 | (0.02, 0.05, 0.02, 0.00, 0.00) |
| natural48 | (0.02, 0.02, 0.02, 0.02, 0.00) |
| natural_jitter | (0.08, 0.02, 0.02, 0.00, 0.00) |

Det innebærer at prosjektet nå bør tenke mer i termer av et **robust kandidatbånd** enn et enkelt “magisk” punkt.

## Hva p_del ser ut til å gjøre

`p_del` er ikke bare “skadelig”. I flere linjer er en liten positiv verdi kompatibel med bedre eller minst like god robusthet enn `p_del = 0`.

Samtidig er effekten tydelig **ikke monotont positiv**:
- for enkelte kandidater hjelper `p_del ≈ 0.01`,
- for andre synker robustheten igjen når `p_del` blir større,
- og høyere `p_del` trekker ofte radius opp eller gjør ensembleavhengigheten større.

Den foreløpige lesningen er derfor:
> litt lokal sletting kan fungere som en form for dynamisk avlastning eller re-organisering, men for mye sletting skader den makroskopiske stabiliteten.

## Hvor “naturlige” starttilstandene faktisk var

Gjennomsnitt over kandidater i v0.8b:

| Ensemble | Mean initial nodes | Mean initial tokens | Mean initial beta1 | Mean initial triangles |
| --- | ---: | ---: | ---: | ---: |
| natural24 | 33.2 | 4.6 | 2.0 | 0.6 |
| natural48 | 53.0 | 13.2 | 9.6 | 7.0 |
| natural_jitter | 40.8 | 9.0 | 6.0 | 3.8 |

Dette er vesentlig rikere starttilstander enn de tidlige syklene, og det gjør v0.8b til en reell robusthetstest snarere enn bare en kosmetisk variant av v0.8.

## Hva dette innebærer

1. **Prosjektet er fortsatt lovende.** Kandidatområdet blir smalere når testene skjerpes.
2. **Prosjektet er ikke ferdig modent.** Resultatene er fortsatt ensemblefølsomme.
3. **Det riktige neste steget er skalaanalyse.** Vi må teste de beste regimene på enda større, mer varierte naturlige ensembler og måle hvordan radius, overlap og quasi-invariants skalerer.

## Arbeidshypotese etter v0.8b

Den mest fruktbare hypotesen nå er ikke at én parameterkombinasjon “er universet”, men at det finnes et lite bånd av regimer med disse trekkene:

- lav `p_swap`,
- svært lav eller lav `p_triad`,
- lav til moderat `p_del`,
- lav eller moderat `r_death`,
- og `r_birth` som ikke er for høy i de mest robuste naturlige ensembletestene.

Det er dette båndet v0.9 bør presse hardest.
