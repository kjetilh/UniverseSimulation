# Relasjonell universgraf v0.8b – forklaring uten professorspråk

## Hvor er vi i prosjektet?

Vi prøver å finne ut om et univers bygget av noder, relasjoner, tilfeldige hendelser og lokale regler kan begynne å vise noe som ligner stabil geometri, bevaringslover og begrenset spredning av påvirkning.

Tidligere fant vi et lovende område i parameterrommet. Men Codex pekte på et viktig problem: kanskje så disse regimene bare bra ut fordi vi startet fra veldig enkle små testgrafer.

v0.8b er svaret på akkurat det problemet.

## Hva gjorde vi nå?

Vi lot modellen selv vokse frem større og mer naturlige starttilstander. Så tok vi nesten like universer, ga dem en liten lokal forskjell, og målte hvor godt de beholdt felles struktur over tid.

Vi testet også hva som skjer når vi skrur litt på `p_del`, altså hvor mye relasjoner får lov til å bli slettet direkte.

## Hva fant vi?

Det viktigste er at de beste regimene **ikke falt fra hverandre** når vi sluttet å bruke bare små leketøy-starttilstander. Den foreløpig sterkeste kandidaten i denne runden hadde parametere `(r_birth, r_death, p_swap, p_triad, p_del)=(0.02, 0.00, 0.02, 0.00, 0.01)`.

Det betyr ikke at modellen er 'riktig'. Men det betyr at prosjektet blir mer troverdig, fordi de lovende områdene ser ut til å overleve strengere tester.

## Hvorfor er dette viktig?

I tidlig forskning er det lett å lure seg selv med små, pene eksempler. Når en idé fortsatt ser lovende ut på større og mer naturlige starttilstander, er det et tegn på at man kanskje har funnet en ekte struktur i modellen – ikke bare en effekt av hvordan man startet simuleringen.

## Hva betyr det i praksis?

- Vi begynner å få et smalere område av regler som virker verdt å studere videre.
- Vi får bedre grunnlag for å spørre om modellen kan gi noe som ligner spacetime og relativitet.
- Vi ser at litt sletting av relasjoner kan tåles noen steder, men for mye ser ofte ut til å skade stabiliteten.

## Hva er neste steg?

Neste naturlige steg er å gjøre startensemblet enda bredere og større, og samtidig måle usikkerheten i kausalfronten mer direkte. Da kan vi begynne å spørre om de lovende regimene virkelig danner en robust 'fysisk' klasse og ikke bare et smalt numerisk vindu.
