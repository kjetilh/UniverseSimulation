# Ordliste v0.10b

- **Nominal target size**: størrelsen generatoren blir bedt om å lage.
- **Realized initial size**: størrelsen grafen faktisk har når growth-fasen er ferdig.
- **Growth-regime**: reglene som brukes til å bygge startgrafene før selve kandidatdynamikken testes.
- **Burn-in**: en innledende vekst-/naturliggjøringsfase før måling.
- **Adaptive calibration**: enkel kontrollsløyfe som prøver å stoppe generatoren når grafen ligger i ønsket størrelsesbånd.
- **Naturalness-proxy**: en operasjonell score som sier hvor mye en generator ligner de tidligere, mer troverdige naturlige strukturene.
- **Finite-size artefakt**: et mønster som ser ut som fysikk, men egentlig skyldes at systemene er for små eller dårlig separert.
- **Deep-variant**: en growth-variant med lengre naturliggjøring / hold-fase enn light-variant.
- **Band-best**: kandidaten som hittil har kommet best ut i flere strenge tester.
