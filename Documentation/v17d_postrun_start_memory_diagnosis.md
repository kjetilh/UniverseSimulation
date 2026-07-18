# v17d postrun start-memory diagnosis

Status: `v17d_start_sensitive_features_contract_but_endpoint_separation_persists`.

## Input boundary

This is a descriptive postrun aggregation of the frozen v17d CSV files. It reruns no chain and computes no source spectrum or observed-effect statistic.

- endpoint input SHA-256: `d985ff4fcf6b4a7dcfc89fb3a2317c78af8a372cfff2ed649c698cc971297481`
- pairwise input SHA-256: `54d0993184752c0d6b8d5dac1b01ee714dfead130b5e99c8e62f9a79203c3eef`
- residual-profile input SHA-256: `3cb0772765d4208c0e9ed002988687f5e9f1f17e906e8b9a60a7bf834a1ddcfb`

## Diagnosis

The early-to-late gap contracts for source-edge fraction and concrete-conflict fraction in `12/12` source-feature cells. Candidate-rank gap contracts in `3/6` sources. This is directional finite movement, not convergence.

Direct cross-start endpoint distance contracts in `5/6` sources, but the late/early ratios span `0.987676` to `1.005646`. The state-level separation is therefore effectively flat over the observed windows even while selected coarse features move toward each other.

All `6/6` sources have one exact residual-component profile digest across both starts, both seeds and both windows, with flexible-edge Jaccard `1.0`. This rules out a changing residual-SCC partition as the explanation for the observed start memory. It does not prove that the length-2-to-4 proposal state graph is connected.

## Next decision

One bounded effect-blind scale extension is justified because traversal, resource, seed agreement, time-window distance agreement, residual profiles and proposal-node overlap passed while start memory remained and the start-sensitive feature gaps moved directionally. The next gate must checkpoint a substantially longer chain and test whether direct cross-start distance responds to scale. If it remains flat, stop scaling this kernel and change the move class. Source effects remain closed.

## Claim limit

This diagnosis does not establish convergence, slow mixing, hidden disconnection, a canonical measure or any physical effect. It only separates observed feature contraction from persistent endpoint separation in the finite v17d data.
