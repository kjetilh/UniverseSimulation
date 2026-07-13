# v0.16aa for ikke-spesialister

Den gamle seed-klokken velger ett sted i hele grafen og fordeler en fast total rate mellom alle tokens. Derfor avhenger en lokal hendelse av hvor mange tokens som finnes langt borte.

Vi fant en fast rate per token som er genuint lokal og som, beregnet paa gamle tidsforloep, ville gitt omtrent samme totale antall seed-hendelser. Men raten er tilpasset gamle data og maa testes paa nye grafer foer den kan tas i bruk.

Neste test sammenligner den gamle globale klokken, ingen seed-hendelser etter preparering, og den nye lokale kandidaten paa helt nye startgrafer.
