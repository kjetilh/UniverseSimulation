# Relasjonell universgraf v0.15i: tail transition lab

## Formål

Denne runden analyserer bare de representative v15h-tracene. Målet er å gjøre senfase-overgangene mer presise enn `mixed_tail` og `rebound_merge_tail`.

## Startstørrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Trace-tail overganger

| trace | prefix chain | v15h tail | v15i tail | major events | topology changes | quiet suffix |
| --- | --- | --- | --- | --- | --- | --- |
| pair23_merge_hold_split | merge_hold_split | rebound_merge_tail | merge_rebound_lock | 18.000 | 16.000 | 56.000 |
| pair23_compress_split_rebind | compress_split_rebind | mixed_tail | fragmenting_lock | 10.000 | 10.000 | 92.000 |
| pair23_split_persistent_dual | split_persistent_dual | mixed_tail | quiet_singleton_lock | 0.000 | 0.000 | 314.000 |
| pair34_split_persistent_dual | split_persistent_dual | rebound_merge_tail | fragmenting_lock | 15.000 | 14.000 | 148.000 |

## Aggregate tail labels

| tail label | n traces | rate | mean events | mean changes | mean quiet suffix |
| --- | --- | --- | --- | --- | --- |
| fragmenting_lock | 2 | 0.500 | 12.500 | 12.000 | 120.000 |
| merge_rebound_lock | 1 | 0.250 | 18.000 | 16.000 | 56.000 |
| quiet_singleton_lock | 1 | 0.250 | 0.000 | 0.000 | 314.000 |

## Operativ lesning

- `artifact_control`: `clean` fordi Tail-overgangene er order-stabile i denne runden.
- `tail_signal`: `tail_families_sharpened` fordi v15h sine grove tail-typer brytes videre ned i minst tre repeterbare overganger (fragmenting_lock, merge_rebound_lock, quiet_singleton_lock).
- `next_step`: `trace_event_explanations` fordi Neste steg bør forklare disse overgangene med eksplisitte hendelseskjeder, ikke ny bred pair-scan.

## Tolkning

- Dette er fortsatt trace-diagnostikk, ikke bevis på partikler eller universelle defect-arter.
- Poenget er å se om senfasen kan deles opp i noen få repeterbare overgangstyper.
- Hvis vi får flere slike typer enn i v15h, betyr det at collision-sporet blir mer forklarbart uten å bli oversolgt.
