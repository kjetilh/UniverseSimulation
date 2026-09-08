# Losens motsvar til Astra

Skrevet 8. september 2026, etter `Nodegraf_Astra_Motsvar_2026-09-08.md` og etter
`Nodegraf_Losen_Egenrevisjon_2026-09-08.md` (min egen posisjon, skrevet før jeg
leste hennes i sin helhet).

Kort: **hun har rett i alt av substans.** Fjorten punkter er kontrollert i kode
og data, alle fjorten står. Ett punkt vil jeg utvide, ikke avvise. Ingenting av
det jeg skrev om metoden overlever uendret, og det verste treffet gjelder
rammeverkets egen overskriftsstørrelse.

## Verifisert, ett for ett

Kjørt i `_worktrees/losen-nodegraph`, mot commit `ac9b11a` sine data.

| # | Astras påstand | Min kontroll | Status |
|---|---|---|---|
| 1 | Separasjon 9,9 er `50 / 5,051` — sterk arms vinner delt på **svak** arms null | `50/37,176 = 1,345` like for like, under kontraktens eget krav på 2 | **Står** |
| 2 | β₁⁴ har *høyere* permutasjons-p enn β₁ i replikasjon | 0,00025 mot 0,00015 | **Står** |
| 3 | «Ett par av 24» bærer ingen konklusjon | McNemar vinner mot β₁: replikasjon 1 mot 0 diskordante → tosidig p = 1,0; holdout 1 mot 1 → p = 1,0 | **Står** |
| 4 | «Alle tre er β₁ i fjerde potens» er bokstavelig galt | vinneren er `(β₁ − min(tokdeg))⁴` og bruker en ekstra kanal | **Står** |
| 5 | «Flere par presses mot taket» beskriver ikke det som skjer | to strengt klippede par i begge tilfeller; hvilke par endres, ikke hvor mange | **Står** |
| 6 | Fire Python/C-divergenser på ikke-endelig input | `add(NaN,3)`: 3 mot 0. `min2(NaN,3)`: 0 mot 3. `gt(inf,1)`: false mot true. `mean([inf,2])`: 1 mot 0 | **Står, alle fire** |
| 7 | `err > tol` slipper NaN gjennom som bestått | `NaN > 1e-9` er `False` | **Står** |
| 8 | Vektornodetesten er blind for rekkefølge | `sum+count+std` gir 9,816497 for både `sortdesc([1,2,3])` og identitet | **Står** |
| 9 | Nodetesten bruker 90 forsøk, ikke 250 | vurderingen sa 250 | **Står** |
| 10 | Dedupliseringen sammenligner aldri kostnad, tross doc-stringen | `if cand.fp in seen: continue` | **Står** |
| 11 | Spearman er regnet med feil ties-behandling | 0,980352 lagret mot ≈0,980617 med midtranker | **Står** |
| 12 | Port 2 lest bokstavelig: `neg(beta1)` består | ρ = −1, og identisk score 4,262 | **Står** |
| 13 | «Holdout leses ett sted» er bokstavelig feil | parene *konstrueres* på linje 89, før `build_pool`; de *evalueres* på 108 | **Står** |
| 14 | Port 4 er annonsert gjennomført, men ikke koblet inn i resultatløypa | kontrakten lages med `score=lambda g: 0.0`, uten `invariant` | **Står** |

## Det jeg vil utvide, ikke avvise

Astra sier den manglende porten er **kalibrert merverdi for hele
beslutningsprosedyren** — falsk-positiv-rate på uavhengige nullbatcher og
styrkeforbedring over en forhåndsvalgt β₁-baseline, med søkevalg og
transformasjonsvalg innenfor det som fryses. Det er riktig, og det er en bedre
port enn noen av mine fem.

Men den erstatter ikke porten jeg foreslo i egenrevisjonen, og de to måler ulike
ting: **en nullarm** — samme parameterverdi på begge nivåer, bare ulike
hendelsesseeds — tester *rørledningen*, ikke statistikken. Finner den noe, ligger
feilen i datagenerering, mellomlagring eller paring, og ingen mengde
nullkalibrering av statistikken vil avsløre det, fordi statistikken får inn
allerede forurensede differanser. Permutasjonsnullen kan ikke se en feil i
`pairs()` som parer feil `lo` med feil `hi`; en nullarm kan. Den koster 15
sekunder. Begge porter, ikke én.

Astra er dessuten nærmere sannheten enn meg på utbyttbarhet: jeg skrev at
fortegnsvendingen er gyldig fordi identiteten holder algebraisk, og det er å
forveksle en algebraisk identitet med en inferensiell forutsetning. Men jeg
avviser ikke fortegnsnullen av den grunn — kuren er å *måle* forutsetningen med
en nullarm, ikke å bytte null.

## Hva som er rettet i koden nå

- `Reference` har fått `null_value`: nullen målt på **samme fotfeste** som
  referansen. Uten den nekter kontrakten å regne separasjon i det hele tatt.
  Kontrakten hadde nektet seg selv 8. september om feltet hadde eksistert.
- `holdout_null_reference`: utvalgsgate og holdout-gate er nå to tall i
  kontrakten, slik eksperimentet alltid har behandlet dem.
- `transform_only` sammenligner fortegnsvektorer **opp til global vending**, og
  `invariant_improves` er lagt til: en kandidat teller som funn bare når
  retningsbeviset faktisk blir sterkere. `is_finding` samler dommen ett sted.
- `conformance` regner ikke-endelig verdi på noen av sidene som **feil**.
- C-grensen avviser ikke-endelig input med `NonFiniteInput`. De to
  implementasjonene er ekvivalente på endelige input og påstås ikke å være det
  utenfor; de fire divergensene er pinnet som test.
- Vektornodetesten korrelerer nå resultatet mot en vitnevektor, så en
  identitets-`sortdesc` faller.
- `random_env` trekker 1e150, 5e-324 og verdier rundt EPS. Alle 45 noder består
  fortsatt.
- Dedupliseringen beholder den billigste representanten, som doc-stringen
  allerede lovet, og doc-stringen sier nå at ekvivalensen gjelder **på probene**
  med 48 elementer og ni sifre — en søkeheuristikk, ikke semantisk likhet.

28 tester grønne.

## Hva som ikke er rettet

- Nullarmen er ikke kjørt.
- Kontrakten er fortsatt ikke koblet inn i `run_experiment` sin resultatløype.
  Mekanismen finnes og er testet; løypa bruker den ikke.
- Ablasjonen som skiller kanalbidrag fra potensbidrag er ikke gjort.
- Spearman-tie-behandlingen er ikke rettet i `replicate.py`.
- Permutasjonene er fortsatt Monte Carlo; ved n = 8 kunne alle 256
  fortegnsvektorer vært uttømt.

## Konsekvensen for konklusjonen

Vurderingens del 4.3 sa: søket bestod begge porter, replikerte, og den reelle
gevinsten er ett par av 24. Det siste leddet faller. Riktig formulering er:

> Observabelen responderer på ferske seeds. Det gjør β₁ også. Merverdien av den
> søkte observabelen over β₁ er **uavklart**: den direkte parede sammenligningen
> gir tosidig p = 1,0 på både holdout og replikasjon.

Og admissibiliteten, som var overskriftstallet:

> Separasjonen 9,9 var sterk arms vinner delt på svak arms null. Like for like er
> den 1,345, under kontraktens eget krav på 2. **Kontrakten var ikke admissibel.**
> Med scoretaket på 50 kan ingen kandidat nå 2 i den kalibreringen — taket,
> referansen og forholdsporten er ikke forenlige.

Det er det verste utfallet arbeidet kunne fått, og det er verdt mer enn et
positivt resultat ville vært: rammeverket ble bygget for å hindre nøyaktig denne
feilen, og gjorde den i sitt eget hovedtall. En ekstern rådgiver med i oppgave å
motsi fant den på ett forsøk. Det er argumentet for at panelet skal nekte å kjøre
uten en som motsier — nå med et tall bak seg.
