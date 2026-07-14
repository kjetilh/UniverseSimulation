# v16n pre-result runtime audit

Date: 2026-07-15.

The first frozen v16n execution was interrupted before any attempt-ceiling result, qualification row, interval spectrum, or scientific result was produced.

Observed sequence:

- all six deterministic calibration histories completed their history and metadata phase;
- the first ceiling (`240`) then ran without producing a completed ceiling result;
- the process remained healthy at `100%` of one CPU core;
- a one-second macOS process sample showed that `576/765` sampled main-frame observations were in Python's linear `list.index` implementation;
- the traceback on interruption identified `candidates.index(first_index)` inside `coarse_rewire`.

The selected edge index already has a fixed position inside its immutable color bucket. Replacing the linear lookup with a precomputed index-to-position array leaves random draws, candidate pairs, seeds, acceptance rules, stopping rules, invariants, and outputs semantically unchanged. It changes only lookup complexity from linear to constant time.

Because no ceiling result existed and no spectrum computation is present in v16n, this repair cannot be conditioned on an observed effect or qualification outcome. The script must nevertheless be hash-frozen again before the formal calibration is restarted. The scientific specification digest is expected to remain unchanged; the preregistered script hash must change.
