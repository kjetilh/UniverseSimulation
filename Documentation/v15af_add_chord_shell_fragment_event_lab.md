# Relasjonell universgraf v0.15af: add_chord shell fragment event lab

## Formal

Denne runden kjorer ingen nye simuleringer. Den bruker de ekte `v15ae`-snapshottene for a lokalisere nar shell-fragmentering starter og om den holder tidlig eller kommer senere gjennom mindre lokale hendelser.

## Startstorrelser

| target | mean initial nodes | q10 | q90 | separated |
| --- | --- | --- | --- | --- |
| 48 | 48.0 | 48.0 | 48.0 | 1 |

## Fragment timing summary

| placement | n | early lock | delayed lock | intermittent churn | connected resistance | mean first frag step | mean prefix steps | mean suffix frag | mean switches |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6 | 0.833 | 0.000 | 0.167 | 0.000 | 1537.3 | 1.3 | 0.912 | 5.500 |
| 1 | 6 | 0.500 | 0.167 | 0.167 | 0.000 | 1549.3 | 13.3 | 0.904 | 4.333 |
| 2 | 6 | 0.667 | 0.000 | 0.167 | 0.167 | 1537.3 | 1.3 | 0.823 | 3.833 |

## Operativ lesning

- `artifact_control`: `clean` fordi Startstorrelsene er fortsatt rent separert; denne runden bruker bare de ekte v15ae-snapshottene og legger ikke inn ny simulasjonsstoy.
- `fragment_timing_status`: `fragmentation_is_usually_early_lock` fordi Shell-fragmenteringen ser oftest ut til a starte tidlig i halevinduet og deretter holde seg som en lokal lock med minoritetsavvik.
- `next_step`: `inspect_minor_exceptions` fordi Neste steg bor forklare minoritetsavvikene, spesielt forsinket onset i `p1` og connected-resistance-caset i `p2`.

## Tolkning

- Dette er en ren analyse av `v15ae`-snapshottene, ikke en ny bred defect-run.
- Les dette som timing i shell-fragmenteringen, ikke som en ny generell defect-lov.
