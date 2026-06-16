# v0.15dj forklart for ikke-spesialister

Vi har sett at samme type forstyrrelse (`add_chord`) kan gi langtrekkende respons, men hvilken plassering som virker flytter seg naar basegrafen byttes.

`v15dj` bruker derfor ikke mer simulasjonstid. I stedet spoer den: kan vi se paa den lokale geometrien rundt en mulig plassering foer vi kjorer dynamikken, og bruke det til aa velge bedre kandidater?

Det forelopige svaret er: kanskje, men bare som en svak prior. Regler som velger plasseringer med lav lokal support-volume treffer minst en aktiv plassering i begge basegrafene vi har. Men datasettet er lite, og regelen bommer paa noe av den positive strukturen.

Neste steg er derfor ikke aa paastaa at vi har funnet en regel. Neste steg er aa la denne billige regelen velge kandidater paa en ny basegraf foer vi kjorer dynamikk, og se om den faktisk hjelper der.
