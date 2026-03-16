# v0.9 verifikasjon

## Hva som ble sjekket

- at run-, group- og candidate-CSV-ene har de forventede kolonnene,
- at kandidatfilen faktisk er sortert etter nedre bootstrapgrense på composite,
- at group-rows dekker både `light` og `deep` burn-in og minst tre målstørrelser.

## Resultat

- Run CSV kolonner: pass
- Group CSV kolonner: pass
- Candidate CSV kolonner: pass
- Kandidatrangering: pass
- Group coverage: pass

## Detaljer

- Beste kandidat i filen er `balanced_pdel` med CI low ≈ 0.622.
- Observerte target-nivåer: [24, 48, 96]
- Observerte burn-in labels: ['deep', 'light']

Merk at denne verifikasjonen er en output-kontroll. De egentlige regresjonstestene ligger i en egen testfil.
