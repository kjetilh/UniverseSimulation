# Instruksjoner: å peke nodegraph mot et nytt problem

For deg som skal bruke dette, ikke lese om det. Formålet står i `PURPOSE.md`,
vurderingen av om det er verdt noe i
`../../Documentation/Nodegraf_Vurdering_2026-09-08.md`.

Kjør `python3 examples/minimal_purpose.py` først. Den er hele arbeidsflyten på
under 130 linjer med planta effekt, så du ser maskineriet svare riktig på et
spørsmål der fasiten er kjent, før du peker det mot noe der den ikke er det.

## Når dette er riktig verktøy

- Du skal **gate på et tall** — en observabel, en metrikk, en terskel — og
  tallet skal bety noe etterpå.
- Du leter etter et uttrykk i et rom av uttrykk: en observabel, en
  feature, et Goal-predikat, en billigere formel for noe du regner ofte.
- Du har, eller kan lage, en **paret** oppstilling: to armer som deler alt
  annet enn det du varierer.

## Når det ikke er det

- Du har ingen billig, eksakt, total scorefunksjon. Da er ikke problemet at du
  mangler et søkerammeverk. Bygg scorefunksjonen først, eller la det være.
- Du kan ikke lage en positiv referanse — en oppstilling der du *vet* effekten
  er til stede. Uten den vet du ikke om instrumentet ditt kan måle noe som
  helst, og et negativt resultat betyr ingenting.
- Du trenger bare å regne ut noe én gang. Da skriv en funksjon.

## De tre nektelsene

`purpose.py` nekter, mekanisk, i tre tilfeller. Ikke omgå dem — de er hver
enkelt kjøpt og betalt av en feil som allerede er gjort.

1. **Ingen målt nullreferanse** → runden er instrumentering, ikke en test.
2. **Ingen målt positiv referanse** → ingenting viser at statistikken
   responderer når effekten *er* til stede. (v17 gikk elleve runder uten.)
3. **Statistikken skiller ikke sine egne to referanser** → formålet er ikke
   målbart med den statistikken. Bytt statistikk, ikke terskel.

Og etter et funn: `transform_only`. Har kandidaten samme fortegnsvektor som
referansen, bærer den ingen retningsinformasjon referansen ikke hadde, uansett
hvor mye bedre den vektede scoren ser ut.

## Seks steg

Kopier `examples/minimal_purpose.py` og bytt ut de fem merkede blokkene.

1. **Kanaler.** Hva har en kandidat lov til å se på, med typer.
   `(("x", VEC), ("n", REAL))`. Alt som ikke står her, kan ikke lekke inn.
   Legg inn minst én *nuisance-kanal* som du vet ikke bærer noe — den skal
   score som støy, og gjør den ikke det, er oppstillingen feil.
2. **Paret data.** For hver seed: én `lo` og én `hi` som deler alt annet. Deler
   de ikke starttilstand, måler du start-familien, ikke armen. Det er nøyaktig
   feilen `v17_program_closure.md` del 2 beskriver.
3. **Splittene.** `TRAIN` velger. `HOLDOUT` leses av én funksjon, for én
   allerede valgt graf. Et replikasjonssett på helt ferske seeds er det som
   faktisk avgjør; se `replicate.py`.
4. **Referansene, begge målt.**
   - null: `stats.null_references_np(alle_deltas)`. Bruk `null_search_p95` for
     utvalg (den kontrollerer at et søk over tusenvis alltid finner en vinner)
     og `null_single_p95` for holdout.
   - positiv: kjør *samme søk* på en arm der effekten er stor og kjent.
5. **Invariant-følgesvenn.** Sett `contract.invariant` til fortegnstesten og
   `contract.reference_graph` til den beste håndplukkede kandidaten. Uten den
   leser du en omparametrisering som et funn.
6. **Kompilér vinneren.** `compile_c.certify(graph)` gir deg ingenting hvis den
   er uenig med referansetolken. Er utdatatypen `vec`, eller mangler en node
   C-implementasjon, sier den det i stedet for å gjette.

## Fallgruvene som allerede har kostet noe

| | målt |
|---|---|
| Kodegenerering til Python gir ingen gevinst | 0,99× |
| Marshalling per kall spiser gevinsten | 2,45× mot 251× |
| Blind nivå-for-nivå enumerering er uframkommelig | drept etter 170 s før dybde 2 |
| Median/MAD er degenerert ved lav n | nullreferansen traff taket ved n = 8 |
| Effektstørrelse uten √n har nesten ingen styrke | mot små, konsistente responser |
| Monotone omskrivninger klatrer «gratis» i den vektede scoren | 2,64 → 3,44 uten ett eneste fortegnsskifte |

De to siste ble begge oppdaget **fordi nullen ble målt**. Hadde den vært
antatt, hadde de passert.

## Kommandoer

```bash
python3 tests/test_nodegraph.py          # 21 tester
python3 examples/minimal_purpose.py      # hele arbeidsflyten, planta effekt
python3 run_experiment.py --depth 3 --only weak
python3 replicate.py                     # forhåndsvalgt vinner, ferske seeds
python3 demo_compile.py                  # komposittnode → C → sertifisering
```

## Grenser du skal si fra om, ikke jobbe rundt

- C-backenden returnerer en skalar. En `vec`-verdi kompileres ikke.
- Alle 45 nodene har C-implementasjon. Legger du til en node uten, blir grafen
  ukompilerbar, og `compile_c` sier hvilken node det gjelder.
- Ingenting her er en fysikkpåstand. Skal et resultat inn i v-serien, gjelder
  `AGENTS.md` sin runde-avslutning i tillegg, og da er det en egen beslutning.
