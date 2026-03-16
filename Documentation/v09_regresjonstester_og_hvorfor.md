# v0.9 regresjonstester og hvorfor de finnes

Følgende regresjonstester ble lagt til i [tests/test_v09_regression.py](/Users/kjetil/Build/Digipomps/HAVEN/UniverseSimulation/tests/test_v09_regression.py):

- `compute_steps_for_state` må være monotont stigende i `N` innenfor klammegrensene.
- bootstrap-rutinene må tåle at en metric er konstant uten å krasje.
- `burnin_sensitivity` må regne riktig på et syntetisk, håndregnet eksempel.
- `radius_alpha` må bli omtrent `0` når radius er konstant på tvers av størrelser.
- `radius_alpha` må bli omtrent `1` når radius er proporsjonal med `N`.

Dette er viktig fordi v0.9 nå bruker skala- og tail-diagnostikk som en aktiv del av kandidatvurderingen. Hvis disse hjelpefunksjonene glipper, kan hele den numeriske tolkningen gli uten at simulatoren selv nødvendigvis kaster en feil.

Disse testene er derfor ikke “ekstra pynt”. De beskytter selve overgangen fra rå simulering til skalaanalyse.
