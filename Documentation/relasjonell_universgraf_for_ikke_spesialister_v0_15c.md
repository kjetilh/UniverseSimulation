# Relasjonell universgraf v0.15c for ikke-spesialister

Denne runden prøvde ikke bare å se om to defects påvirker hverandre, men hvilken type påvirkning det ligner mest på.

Hoveddommen er `mixed_collision_family`.

Det betyr: Kollisjonsklassene splitter seg fortsatt (`secondary_split_like` 0.250, `binding_like` 0.188, `annihilation_like` 0.000, `pass_through_like` 0.000).

Neste anbefaling er: Neste steg bør være en enda smalere interaksjonstest med flere snapshots og eksplisitt komponentsporing rundt møtet.
