# v17j interpretation audit

Formal status: `v17j_anchor_independent_compound_cycle_qualified`.

The two-cycle block is anchor-independent at proposal time: it sees the current assignment and candidate graph, not the paired evaluation start. Exact balance is a property of retained sampled auxiliary paths, not proof that the finite chains mixed or connected the whole component. The net-change filter is symmetric and rejected paths remain self-loops; no conditioned proposal normalization was introduced. Source effects and physics remain untested.
