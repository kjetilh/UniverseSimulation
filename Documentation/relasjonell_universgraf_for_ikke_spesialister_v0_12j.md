# v0.12j for ikke-spesialister

Denne runden sjekker om den samme praktiske dommen fortsatt holder nar vi flytter arbeidsflyten til noe storre grafer.

- Referansen `full_basis@0.50` bruker omtrent `20.9910` sekunder per split i denne storrelsesrunden.
- `spectral_only@0.50` er fortsatt den enkleste kandidaten, men den holder ikke kvaliteten like godt som referansen i denne større testen.
- `spectral_plus_dim@0.667` er kvalitetssterkere, men tregere fordi den sender flere baser videre til dyre oppfolginger.
