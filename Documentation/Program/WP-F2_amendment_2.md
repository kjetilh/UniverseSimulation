# WP-F2 tillegg 2 — 8. september 2026: α bærer dimensjon, og gaten min leser den feil

Gjelder `WP-F2_influence_order_calibration.md` og `WP-F2_amendment_1.md`.
Skrevet av Claude (spec-forfatter) etter forsøk 2, modus R. Tallene under er
lest fra `WP-F2_attempt2_per_history.csv` og
`WP-F2_R_*_attempt2_curves.csv`, ikke fra rapportsammendrag.

Ledgeren teller dette som forsøk 3 på samme fingeravtrykk. Grunnen står her.

## 1. Hovedfunnet fra forsøk 2

Med amendment 1s tettere τ-grid er α endelig målbar i alle 16 historier
(6–9 fit-punkter mot 1–2 i forsøk 1). Kernel-leseordenen:

| underlag | kjent d | α målt [95 % KI] | forhåndssagt α = 1 + d_s/2 | innenfor KI |
|---|---|---|---|---|
| ring | 1 | 1,621 [1,377; 1,869] | 1,50 | ja |
| lat2 | 2 | 2,054 [1,883; 2,325] | 2,00 | ja |
| lat3 | 3 | 2,756 [2,668; 2,792] | 2,50 | nei (0,26 for høy) |
| rrg | ∞ | 1,757 [1,739; 1,811] | ∞ | nei — se del 2 |

**Rekkefølgen holder for de tre endelige underlagene, KI-ene er disjunkte, og
to av tre treffer et tall som ble skrevet ned 6. september før noe var målt**
(`Geometribevarende_orden_2026-09-06.md`, del 4: |J⁻(e,τ)| ∝ τ^{1+d_s/2}).
Det er en prediksjon, ikke en tilpasning. Separasjonen ring/lat2 er knapp
(1,869 mot 1,883) og skal ikke omtales som robust.

Legacy-ordenen (v16a-projeksjonen) gir α = nan for lat2, lat3 og rrg: for få
punkter når V ≥ 8. Kontrasten er poenget — den gamle ordenen kan ikke måle
dette i det hele tatt der den nye kan.

γ på middelavstand: ring 0,331, lat2 0,460, lat3 0,456, rrg 0,630. lat2 og
lat3 ligger på diffusivt ½ innenfor målefeil; ring lavere; rrg klart raskere.

## 2. Feilen i gaten: rrg har ingen eksponent å ordne

Gaten krevde `α(ring) < α(lat2) < α(lat3) < α(rrg)`. Målt α(rrg) = 1,76,
altså mellom ring og lat2. Det leses lett som «ordenen bærer ikke dimensjon».
Det er feil lesning, og grunnen er min.

På en ekspander vokser fortidsvolumet **eksponentielt**, ikke som en potens.
Å tilpasse en rett linje i log–log til en eksponentiell kurve gir et endelig
tall, og det tallet betyr ingenting. Kontrollen, over fit-vinduet, per historie:

| underlag | R² potenslov (ln V mot ln τ) | R² eksponentiell (ln V mot τ) | foretrekker |
|---|---|---|---|
| ring | 0,99531 | 0,97701 | potens, 4/4 |
| lat2 | 0,99711 | 0,98710 | potens, 4/4 |
| lat3 | 0,99923 | 0,97798 | potens, 4/4 |
| rrg | 0,98727 | 0,99675 | **eksponentiell, 4/4** |

**16 av 16 historier faller på riktig side, uten unntak.** Ekspanderen er
separert fra de tre endelige underlagene — men av *funksjonsform*, ikke av
eksponentverdi. Instrumentet skiller altså «har dimensjon» fra «har ikke
dimensjon» skarpere enn gaten min var i stand til å lese.

Dette er tredje gang på samme pakke at spesifikasjonen, ikke målingen, er
feilen (τ-grid, seed i M, nå funksjonsform). Fellesnevneren er verdt å skrive
ned: **jeg har hver gang antatt at alle referansene deler en egenskap uten å
måle at de gjør det.** Det er nøyaktig den tredje nektelsen i
`Tools/nodegraph/purpose.py` — «statistikken skiller ikke sine egne to
referanser → bytt statistikk, ikke terskel». Nodegraf-rammeverket, skrevet
dagen etter denne gaten, avviser denne gaten.

## 3. Rettelse — frosset her, før M analyseres

Gate F2 erstattes av to ledd som begge må holde, per modus:

**F2a — formskille.** For hver historie tilpasses både potenslov og
eksponentiell over fit-vinduet. Krav: alle ring/lat2/lat3-historier
foretrekker potens, alle rrg-historier foretrekker eksponentiell.
*Målt for R/kernel: 16/16. Bestått.*

**F2b — eksponentordning, kun blant underlag som består potensleddet i F2a.**
α(ring) < α(lat2) < α(lat3), disjunkte 95 %-KI mellom nabopar.
*Målt for R/kernel: rekkefølge ja; KI disjunkte, ring/lat2 med 0,014. Bestått, knapt.*

**Mekanismeleddet (γ innenfor 0,10 for ring/lat2/lat3) står uendret og feiler:
spennet er 0,129.** Det skal ikke lempes på. lat2 og lat3 er enige (0,460 mot
0,456); ring alene ligger lavt (0,331). Forklaringen er ikke etablert, og en
ring er det underlaget der «avstand» har minst rom å variere i. Rapporter det
som ikke bestått, med den observasjonen ved siden av.

Ingen terskelverdi er endret. F2a er ikke en ny terskel som gjør det lettere å
bestå; den er et krav som ikke fantes, og rrg måtte bestå det for å bli lest
i det hele tatt.

## 4. Hva som gjenstår

1. Analyser modus M med samme grid og F2a/F2b. M er den avgjørende: R har
   10–20 % kantdrift, så «underlaget» beveger seg under målingen.
2. Kjør WP-H.
3. Først når M er inne: G4-adjudikasjon for lesning G.

## 5. Hva som allerede kan sies, og hva som ikke kan

Kan sies: **innflytelsesordenen bærer underlagets dimensjon når underlaget har
en**, målt på tre kjente underlag, med en eksponent som ble forutsagt før
måling, og med ekspanderen separert på funksjonsform. Den gamle
konflikt-DAG-projeksjonen kan ikke måle det samme.

Kan ikke sies: at det relasjonelle universet har en dimensjon. Ingen
univershistorie er målt med dette instrumentet. Kalibreringen er ikke ferdig
før M er lest, og WP-F3 er ikke spesifisert. Ingen fysikkpåstand.
