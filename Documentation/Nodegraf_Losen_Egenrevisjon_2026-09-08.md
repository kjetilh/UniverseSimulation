# Losens egenrevisjon av nodegraf-vurderingen

Skrevet 8. september 2026, **før** Astras motsvar ble lest i sin helhet, av den
grunnen `codex_astra_routes.md` gir: uten en egen posisjon på forhånd blir
«diskusjon» gjenfortelling.

Ærlig forbehold: jeg hadde allerede sett to fragmenter av Astras svar i
stderr-loggen — avsnittet om port 4 og punktlisten til slutt. Delen om port 4
nedenfor er derfor ikke uavhengig. Resten er det.

Merking som i briefen: `[belagt: fil:linje]`, `[vurdering]`, `[usikker]`.

---

## Q1 Er permutasjonsnullen riktig konstruert?

**Fortegnsalgebraen holder.** [belagt: arena/observable_purpose.py:93]
`deltas` regner `O(hi) − O(lo)` per par, så å bytte armetikett innenfor paret er
nøyaktig `−d`. [belagt: stats.py:47] Winsorterskelen er en kvantil av `|d|`, som
fortegnsvending ikke rører, så klipping og fortegnsvending kommuterer — og
[belagt: tests/test_nodegraph.py] `test_winsorising_commutes_with_sign_flipping`
sjekker det på 200 tilfeldige vektorer. Det er denne identiteten hele den raske
nullen hviler på, og den er testet, ikke antatt.

**Men designet er ikke en ren armkontrast.** [belagt: arena/build_substrate.py:188]
`ev = s*7919 + (1 if hi else 0)`: de to armnivåene deler starttilstand, men får
*ulike hendelsesstrømmer*. `d` inneholder derfor både armeffekten og
hendelsesstøy. [vurdering] Det ugyldiggjør ikke testen — under permutasjon
fortegnsvendes støyen sammen med effekten, så nullen absorberer den korrekt —
men det koster styrke, og vurderingen sier det ikke noe sted. Den burde sagt at
en delt hendelsesstrøm (samme `ev` for begge nivåer) ville isolert armen bedre,
og at jeg valgte ulik strøm uten å begrunne det.

**De to nullene er brukt riktig vei.** [belagt: run_experiment.py:120,128]
`null_search_p95` (maks over hele kandidatmengden) gater utvalget der tusenvis
av kandidater ses; `holdout_gate_null_p95` regnes av vinnerens *egne*
holdout-differanser og gater holdout, der én kandidat måles.
[vurdering] Det er riktig fordeling. Å bruke maksimumsnullen på holdout ville
vært konservativt til ubrukelighet; å bruke enkeltnullen på utvalget ville vært
direkte feil.

**Én reell svakhet:** [belagt: run_experiment.py:122] `null_single_p95` beregnes
også på treningssettet og lagres i resultatet, men brukes ikke til noe. Et tall
som ligger i en resultatfil uten en beslutning knyttet til seg inviterer til å
bli lest som en terskel det ikke er.

## Q2 Er holdouten ren?

Sporet, ledd for ledd:
[belagt: run_experiment.py:47] probe-miljøene til enumeratoren tas fra
`pairs_train[:n_probes]`; [belagt: search.py] dedupliseringen bruker bare disse
probene; [belagt: run_experiment.py:97] skåringen kjører mot `"train"`;
[belagt: run_experiment.py:104] vinneren velges fra treningsradene;
[belagt: run_experiment.py:107-108] holdout leses ett sted, for én graf.
`_trim` rangerer på kost og en RNG, ikke på data. **Utvalgsløypa er ren.**

Tre lekkasjer som likevel bør stå skrevet:

1. [belagt: run_experiment.py:213-219] De håndplukkede baselines skåres på
   holdout og skrives til resultatfila. Det er rapportering, ikke utvalg — men
   påstanden «slår beste håndplukkede på holdout» er en *etterpå*-sammenligning,
   ikke en forhåndsregistrert test.
2. [vurdering] Jeg kjørte svak arm tre ganger med ulike søkeseeds og leste
   holdout hver gang. Vinneren som rapporteres er fra den første, forhåndsvalgte
   seeden, og de to andre var stabilitetssjekker — men tre blikk på holdout er
   tre blikk, og vurderingen sier det ikke.
3. [vurdering] **Den alvorligste.** Arenaens utforming — armnivåene 0,03 mot
   0,09 og 20 000 hendelser — ble valgt etter utforskende kjøringer på seedene
   1000–1007, som *er* treningsseeds. Det er ikke en lekkasje inn i
   kandidatutvalget, men det er en lekkasje inn i arenavalget, og
   replikasjonssettet (seed 501000+) er det eneste tallet som er fritt for den.

## Q4 Er konformanstesten sterk nok til å bære ordet «sertifisert»?

Nei, og det er allerede belagt med en feil jeg fant selv:
[belagt: Documentation/Nodegraf_Vurdering_2026-09-08.md, del 5 punkt 7] C-backenden
ga 11,6 % feil svar ved 400 000 elementer mens den bestod prøven, fordi
`random_env` aldri trakk vektorer over 128. Prøven trekker nå 4 096 og 20 000.

Det som *fortsatt* ikke dekkes, med konkrete verdier:
[belagt: compile_c.py, `random_env`] ingen ekstremmagnituder (1e308 — som er
nøyaktig der `** 2` mot `*` divergerte og måtte fanges av en egen totalitetstest
i stedet), ingen denormaler (1e-320), ingen NaN/inf inn, og ingen vektorer der
alle elementer er like (som setter `sd = 0` og `MAD = 0` samtidig).
[vurdering] «Sertifisert» bør erstattes med «bestått prøve X med Y trekninger».
Ordet lover en egenskap; testen gir en observasjon.

## Q5 Er den positive referansen god nok?

Nei. [belagt: _cache/experiment.json] Den er `winner_train_score = 50,0` — som er
`SCORE_CAP` [belagt: stats.py:36]. En referanse som treffer taket sier bare «minst
50». Separasjonen 9,9 er derfor en **nedre grense**, ikke en måling, og
vurderingen presenterer den som et tall. Dessuten er den tatt fra n = 8 par mot
svak arms n = 24, og fra en arm som ved nærmere ettersyn er et regimeskifte
(`dn` ≈ −15 000 noder), ikke en gradsforskjell.

[vurdering] Det burde vært en armstyrke justert slik at referansen lander midt i
skalaen, med samme n som søkearmen, og en kalibreringskurve over flere
armstyrker i stedet for ett punkt. Da måler man hvor instrumentet metter, ikke
bare at det gjør det.

## Q6 Er portene de riktige?

**Porten som mangler: en nullarm.** Kjør hele løypa med `lo` og `hi` satt til
*samme* parameterverdi, bare ulike hendelsesseeds. Finner den noe, er feilen i
datagenerering, mellomlagring eller paring — ikke i statistikken. Permutasjonsnullen
tester bare statistikken; en nullarm tester rørledningen. Den er billig (15 s) og
mangler.

**Porten jeg ville strøket: port 3** (språkmodell mot enumerator per krone).
[vurdering] Den svarer ikke på om rammeverket er verdt å bygge; den er et eget
spørsmål som kan stilles når som helst senere. Å ha den blant portene gir
inntrykk av at verdien avhenger av at en modell viser seg nyttig, og det gjør den
ikke.

**Porten jeg ville omskrevet: port 2** (Spearman < 0,9 mot enhver enkelt kanal).
[vurdering] Den forutsetter at et nyttig funn må være ukorrelert med noe kjent.
Det er feil krav: en reell styrkegevinst kan godt være sterkt korrelert med en
kjent størrelse. Kravet burde vært dokumentert merverdi *utover* baselinen ved
kontrollert feilrate, ikke lav korrelasjon.

---

## Det jeg forventer at Astra treffer meg på

Skrevet nå, så det kan sjekkes etterpå:

1. At port 4 er annonsert som gjennomført, men at mekanismen ikke er koblet inn
   i hovedeksperimentets resultatløype. (Fragmentet jeg allerede så.)
2. At `transform_only` bare tester identisk fortegnsvektor og derfor er både for
   snever og for løs.
3. At taket på 50 gjør separasjonstallet meningsløst som måling.
4. At «21 mot 20 fortegn» er ett par og bør omtales deskriptivt, ikke som en
   etablert merverdi.
