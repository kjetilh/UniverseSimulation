# Relasjonell universgraf – status v0.8 fasekart

## Hva som er nytt
- Vi har nå ett samlet parameterkart som rangerer repair, radius/front, makrodrift og geometri-proksier samtidig.
- Kartet bruker maksimal lokal kobling som standard og ligger derfor på toppen av v0.7-metodikken.

## Kort dom
1. sweet spot-kandidat: r_birth=0.02, r_death=0, p_swap=0.02, p_triad=0.01, p_del=0.01, sweet_score=0.786
2. sweet spot-kandidat: r_birth=0.05, r_death=0.02, p_swap=0.04, p_triad=0.01, p_del=0.01, sweet_score=0.759
3. sweet spot-kandidat: r_birth=0.02, r_death=0.05, p_swap=0.08, p_triad=0.01, p_del=0.01, sweet_score=0.750

## Hva som ser mest lovende ut
- Repair-vennlig: r_birth=0.02, r_death=0, p_swap=0.02, p_triad=0.01, p_del=0.01
- Invariant-vennlig: r_birth=0.02, r_death=0.05, p_swap=0.02, p_triad=0, p_del=0

## Hva som fortsatt mangler
- Mer presis statistikk på de beste punktene.
- Skalering med flere seeds og lengre runs.
- Eventuelt v0.7+-arbeid med enda skarpere lokal kobling i åpne familier hvis repair fortsatt ser skjør ut.
