# v17f postrun reverse-closure diagnosis

Status: `v17f_reverse_support_failure_is_bounded_search_asymmetry`.

This diagnosis is descriptive and was not preregistered. It replays the frozen v17f trace without computing source spectra or observed effects.

## Failure localization

Exact trace replay passed `24/24`. V17f recorded `11` reverse-unsupported length-5 auxiliaries across `9/24` chains, out of `720` valid length-5 auxiliaries (`0.015278`). All were rejected and changed no state.

All other frozen movement floors passed in `24/24` chains. Resource passed `24/24`, with maximum formal chain runtime `22.681378` seconds.

Failure reasons under the frozen 20,000-state guide: reverse_first_search_budget_exhausted=7; reverse_suffix_missing_from_bounded_support=4.

The explicit reverse path was structurally valid in `11/11` cases, and the frozen witness search exhausted its budget in `11/11`. A diagnostic 10x search cap recovered reverse support for `9/11` failed auxiliaries. This does not alter the frozen v17f failure or qualify a larger search budget.

## Interpretation

The expanded Metropolis kernel remained probability-safe because q_reverse=0 auxiliaries were rejected. The stricter preregistered movement gate nevertheless failed because the bounded raw auxiliary support was not reverse-closed. The failure is in proposal-support qualification, not assignment integrity, length-5 availability, aggregate movement, or resource use.

## Smallest next repair

Define the length-5 proposal support as the existing generated auxiliary post-filtered by explicit reverse support under the same frozen 20,000-state law. Unsupported pairs become proposal dead ends before entering the valid-proposal count. This preserves the generation probability for retained auxiliaries, makes support reverse-closed by construction, and should permit exact replay of accepted v17f state trajectories. Preregister the repair and require exact endpoint/accepted-transition parity with v17f plus zero runtime reverse-unsupported events before any matched-work start-memory gate.

This diagnosis does not establish connectivity, convergence, source effects, Bell correlations, entanglement, Lorentz symmetry, spacetime or a universe model.
