# UC1 / UC2 explicit provenance — not a graph database

Declared as-of date: 2026-09-10.

This is an explicit file-based index, not a graph database or an inference engine. Statuses and relations are declarations from the manifest, not verified scientific conclusions. SHA-256 identifies whole-file source bytes; anchors are unverified citation hints. Only listed sources were read.

## Nodes

| ID | Kind | Status | Repository-relative source | Anchor | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| uc1-evidence | data | measured | Documentation/Program/UC1&#95;measurements.json |  | 9c0461cb1ab9a7f8d52c4dee5980683c9b3f6199f2466c58537522f1aa904844 |
| uc1-protocol | protocol | verified | Documentation/Program/UC1&#95;preregistration.json |  | b0ba3861ee1df93aa102d2b0857945988a0e951caa11239e23cbc06f3bfa128a |
| uc1-report | report | measured | Documentation/Program/UC1&#95;report.md |  | c4ac7ee2bb1af894157bb874b3a9d1184da1e0d6e6563f1d235eed3727499515 |
| uc2-calibration | data | measured | Documentation/Program/UC2&#95;calibration.json |  | 760c7411880d645d659f45a5ef0bf365a882d14db611e249052ee067ba2d5718 |
| uc2-candidate | result | measured | Documentation/Program/UC2&#95;candidate.json |  | dc94435b538ba0d73802d8dc92cf31e05bda900e30f6a6c9c94037fec81ecb67 |
| uc2-events | data | measured | Documentation/Program/UC2&#95;candidate&#95;events.csv |  | beb239398135d5f1236d0964127d2739ba26dfb6d056d0f741081eb467c1034c |
| uc2-kernel | code | verified | Tools/local&#95;change&#95;candidate.py |  | c4f63b6fea5835bd06fb25e6586e094508e2e2e006fda91fe2c88bb7eb218c44 |
| uc2-limits | limitation | verified | Documentation/Program/UC2&#95;model&#95;contract.md | hva-kandidaten-kan-svare-pa | 7af789c9bcc407df0016aef306b6adbeed6c85800a642ab9a398bbada0ea9caf |
| uc2-protocol | protocol | verified | Documentation/Program/UC2&#95;preregistration.json |  | 56de517f878efb184485373af87c801732be7a4b5651c0d427b4a7f4396349ed |
| uc2-report | report | measured | Documentation/Program/UC2&#95;report.md |  | 41fae61d385d27832bc69ef0d57046a2ecfa5e820d4ded887d4a51d601df5f34 |
| uc2-rule | user&#95;rule | verified | Documentation/Program/UC2&#95;model&#95;contract.md | brukerens-presisering-og-var-avgrensning | 7af789c9bcc407df0016aef306b6adbeed6c85800a642ab9a398bbada0ea9caf |
| uc2-runner | code | verified | Tools/run&#95;local&#95;change&#95;candidate.py |  | d55a2f02332ca5232bf810ed1f3cbc1b5fd989fd7c3158d3b2d1f4d31cf3f586 |
| uc2-tests | test | verified | tests/test&#95;local&#95;change&#95;candidate.py |  | 746d44ee4615bdc9b55a8976650a4010139a64eb75f396db755cc04858b3f744 |
| uc2-witness | data | measured | Documentation/Program/UC2&#95;witness.csv |  | 1b2ea1e0eb31557f353886a02bd10df918694e5bcc9718cd81eb090a0fa314c2 |

## Declared edges

| Source | Relation | Target |
| --- | --- | --- |
| uc1-evidence | derived&#95;from | uc1-protocol |
| uc1-report | reports | uc1-evidence |
| uc2-calibration | calibrates | uc2-runner |
| uc2-candidate | derived&#95;from | uc2-events |
| uc2-candidate | derived&#95;from | uc2-protocol |
| uc2-candidate | executed&#95;with | uc2-kernel |
| uc2-kernel | implements | uc2-rule |
| uc2-protocol | assumes | uc2-rule |
| uc2-protocol | limited&#95;by | uc2-limits |
| uc2-report | limited&#95;by | uc2-limits |
| uc2-report | reports | uc2-calibration |
| uc2-report | reports | uc2-candidate |
| uc2-runner | executed&#95;with | uc2-kernel |
| uc2-runner | implements | uc2-protocol |
| uc2-tests | tests | uc2-kernel |
| uc2-witness | derived&#95;from | uc2-events |
