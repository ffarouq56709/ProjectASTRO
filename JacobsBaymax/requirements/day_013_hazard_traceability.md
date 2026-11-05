# Day 13 · Hazard-to-test traceability

**R0.3 working audit · 2026-11-04 · Owner: Faisal Farouq**

Result: **PASS — document traceability only.** Owner time: **2 hours**, recorded at the owner's instruction. Prepared by Codex as a documentation assistant; no independent engineering or safety review is claimed.

## What is complete

- Audited the 20 original hazards against 64 requirements and 26 verification protocols.
- Promoted all 15 Day 10 scenarios to permanent IDs, giving 35 working hazards.
- Reconciled requirement/hazard links in both directions and added an explicit `Hazard IDs` column to the working verification matrix.
- Checked 103 hazard/requirement pairs and 76 hazard/verification pairs in both directions: **358 directed checks**, with no missing IDs or reverse links. All 64 requirement/verification pairs also agree in both directions.
- Added `blocks gate` and the basis for each hold. All **31 P0 hazards** name existing gates. G0's accepted documentation/software/analysis scope is unaffected.
- Saved 33 changed link fields from the original rows in `day_013_link_changes.csv`. These include missing reverse links, supporting tests reached through requirements, and links to the new scenarios.

The main output is [day_013_hazard_traceability.csv](day_013_hazard_traceability.csv), one row per hazard. Its direct-test column distinguishes the original scenario/baseline tests from supporting tests added through requirement links. A link means the protocol contributes evidence; it does not establish that the method is sufficient or has passed.

## Permanent IDs

| Day 10 | Permanent hazard | Scenario |
|---|---|---|
| MP-01 | JB-H-21 | Knee pinch |
| MP-02 | JB-H-22 | Ankle pinch |
| MP-03 | JB-H-23 | Hip/inner-thigh pinch |
| MP-04 | JB-H-24 | Foot lands on a person |
| MP-05 | JB-H-25 | Swinging leg strikes a person |
| MP-06 | JB-H-26 | Runaway joint |
| MP-07 | JB-H-27 | Shoulder-pin pinch or arm drop |
| MP-08 | JB-H-28 | Shell collision/cracking/pinch |
| MP-09 | JB-H-29 | Cable snag or sensor/power-line damage |
| MP-10 | JB-H-30 | Object falls from handling tray |
| MP-11 | JB-H-31 | Handling actuator/tray pinch |
| MP-12 | JB-H-32 | Separate handling stand overturns |
| MP-13 | JB-H-33 | Handling load drops on power loss |
| MP-14 | JB-H-34 | Person uses arms/tray/stand for support |
| MP-15 | JB-H-35 | Walking while loaded or docked |

Parent hazard IDs and original MP IDs remain in the working register, so these details can be traced to Day 10 without editing its historical files.

## Working files and protocol coverage

- [Hazards](../risk_records/hazards_R0_3.csv): 35 rows, parent/source IDs, gate holds and priority basis.
- [Requirements](requirements_R0_3.csv): 64 existing requirements with reconciled links. Requirement text is retained for the Day 14 wording review; this is not a newly accepted requirements baseline.
- [Verification matrix](../tests/verification_matrix_R0_3.csv): 26 existing protocols with reverse hazard links and a separate `Day 13 coverage to implement` field.

The coverage field calls out foot/swing exclusion (JB-V-06), shoulder-pin retention and cable routing (JB-V-07), sensor disconnect and handling power-off retention (JB-V-08), joint/handling limits (JB-V-09), stand stability and tray protection (JB-V-22), dock/payload/support interlocks (JB-V-23), and preflight/no-contact checks (JB-V-25). These are review and implementation tasks. Qualified reviewers must establish acceptance criteria before the relevant tests.

The 15 new scenarios receive conservative **P0 planning holds** while awaiting assessment. This is a release priority, not an assessed severity or risk score. Their severity, and every hazard's likelihood and residual risk, remain **UNASSESSED**. The original 20 severity/priority entries are retained as inherited baseline values. Day 10 numbers and control ideas remain unverified source screens.

Gate holds apply to the relevant configuration and release scope. A listed gate cannot be released for that scope until the hazard has an authorized evidence-based disposition. This file grants no gate release, purchase, fabrication or powered-test authority. The original `gates.csv` is a historical R0.1 record; the later Day 7 evidence records the restricted G0 release.

## Carry forward to Day 14

1. Reconcile the existing Day 8 wording issues with the accepted Day 6/7 configuration and scope.
2. Update the retained $10,000 wording in JB-R-009, JB-V-03, G3 and the Day 12 assumption register against **D-01's accepted $15,000 working cap**. The $25,000 tier (D-10) is still proposed.
3. Obtain the owner's disposition of D-07 before adopting JB-R-065–073 or adding proposed JB-V-27. They are excluded from this audit's accepted-ID set.
4. Keep specialist assignments, acceptance criteria and hazard dispositions open until supported by actual evidence.

All 26 verification protocols remain **BLOCKED / NONE — NOT EXECUTED**. Day 13 ran no robot test or simulation and released no gate.

## Reproduce the document checks

From the project root:

```sh
python3 JacobsBaymax/requirements/day_013_trace_hazards.py --check
```

Omit `--check` to regenerate the five working CSVs and the evidence JSON. Inputs and outputs have SHA-256 hashes in [the evidence record](../evidence/day_013_hazard_traceability_review.json). The script checks saved-output consistency, ID existence, reverse links, P0 gate references and retained unexecuted/unassessed status. It does not execute any JB-V protocol.
