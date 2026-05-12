# Relasjonell universgraf for ikke-spesialister v0.15cr

Vi testet om p2-moensteret var en god peker mot noe som skalerer til storre grafer. Det ser det forelopig ikke ut til aa vaere.

P2 var interessant ved storrelse 768. Men ved 896 er signalet bare delvis og ikke sterkere enn kontrollen, og ved 1024 dukker det ikke opp igjen selv med mer tid.

Det mest interessante nye sporet er faktisk en kontroll: `add_chord_p0`. Den var nesten svak ved 768, men fikk lang far-shell-horisont ved 896 og 1024. Det kan vaere et lite artefakt, men det er mer lovende aa teste enn aa bruke mer tid paa p2.

Neste smale steg boer derfor vaere aa teste `add_chord_p0` med friske seeds ved 896 og 1024. Hvis det holder, har vi en ny skala-respons-kandidat. Hvis det faller sammen, bor vi slutte aa jakte paa dette p2/p0-sporet og heller lage en bedre observabel.
