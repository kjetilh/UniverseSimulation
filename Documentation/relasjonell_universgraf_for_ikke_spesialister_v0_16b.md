# v0.16b for ikke-spesialister

Vi gjorde hver faktisk hendelse til et punkt i en avhengighetsgraf. En pil betyr at en senere hendelse leser eller endrer noe en tidligere hendelse brukte eller endret.

Den viktigste proeven stokker om hendelser som grafen sier er uavhengige, men respekterer alle pilene. Dersom mange slike rekkefolger ender i eksakt samme graf og tokenplassering, er mye av den opprinnelige sekvensen bare en representasjonsrekkefolge, ikke en fysisk avhengighet.

Statusen i denne runden er `pass_to_v16c_coarse_graining_pilot`. Selv ved pass er dette en kontrollert kausal arkitektur i modellen, ikke et bevis for romtid eller relativitet.
