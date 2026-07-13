# Operativ anbefaling v0.16f

Status: `pass_to_v16g_clock_depth_boundary_mechanism_gate`.

- Ikke slaa sammen clock- og depth-kartene til en felles geometri paa grunnlag av v16f.
- Ved full pass: test om event-family og lokal rate forklarer hvor clock-grenser kutter depth-komponenter.
- Ikke legg til et tredje kart eller oek target foer mekanismen er testet.
- Behold edge-internaliserings-phi som diagnostikk; den var ikke primary og skal ikke oppgraderes post hoc.
- Ikke presenter simulation clock som proper time eller resultatet som Lorentz-, spacetime- eller continuum-evidens.
