# UC3R — post-hoc observation of structural remnants, 2026-11-04

Population: all 16 archived UC3 candidate worlds; no simulated continuation,
replacements, parameter search, effect gate or new physics. Existing overall
outcomes were known. This extraction rule is written before inspecting new
episode-level outcomes; it does not turn old data into preregistered data.

1. Replay successful edits in order from initial states; blocked attempts do
   not advance physical time. Track exact undirected edge instances by endpoint
   pair AND creation tick (0 for initial edges); removal/recreation resets it.
   A slide changes the pair, i.e. does not count as literal survival.
2. Follow each original persistent unit's current connected component. A change
   is seen only if its source is in the pre-event component of the tag. A split
   counts once and the tag follows only its own descendant. Measure the 2-core
   after each seen edit, not just saved frames. All initial graphs are trees.
3. First episode per tag: hold its running record of 2-core node count K
   (strictly larger replaces the peak; earliest tie retained). After a peak
   K>=4, take the first later seen edit with 2*K_now<=K_peak as the loss.
   Loss may be a split, ordinary cut, collapse or other edit; report separately.
   R is the set of peak 2-core edge *instances* still present anywhere in
   the tag's post-loss component; they need not still belong to its 2-core.
   Distinguish initial edges from instances created after the tree start.
4. For the next **16** seen successful edits (loss edit excluded), record
   each bud and its pre-event source–anchor edge. Hit only if that exact
   edge instance belongs to R. At each bud also record its conditional
   opportunity: incident R instances at the source / all incident edges.
   This follows UC3's uniform neighbor choice; it is a bookkeeping comparator,
   not a measured matched null or a counterfactual law. Keep no peak, no loss,
   empty R, no bud, no hit and short/terminal exposure in the accounting.
5. Separately record renewed core growth: K_now >= K_loss+2 in follow-up.
   Joint witness: a hit and a same-or-later such core observation within
   that window. Preserve exact world, tag, peak/loss/hit/growth ticks, anchor,
   edge birth tick and core sizes. Do not require return to the original shape.
   Report any hit on a post-initial edge separately. These definitions exclude
   inheritance by wholesale rewiring and do not measure a growth advantage.
6. Unit traces and buds can overlap. Count worlds with each observation;
   present tag counts explicitly as correlated coverage. Distinct physical
   hit buds are unique (run_id,tick); never treat tag copies as replicates.
   If displaying O−E, also give the positive/tied/negative world counts;
   no hypothesis verdict from sign or weighted value. Include every world
   by start size and an inspectable chronological witness if one exists.
7. Check input SHA-256 against the archived UC3 manifest and replay totals/
   final state against archived summaries. Independent extraction and small
   offline fixtures test the observer; no drawn stochastic trajectories.
   The old fan references do not qualify this new measure. No causal gate,
   accumulation claim, or extrapolation beyond these logs.

Work ownership: root integrates, checks provenance, writes interpretation
and handles closure. Separate workers own the extractor, independent replay,
and public/RAG source-list adapters respectively; no shared Git mutations.
