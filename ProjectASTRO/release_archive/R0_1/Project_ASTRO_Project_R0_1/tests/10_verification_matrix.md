# Verification and evidence matrix

Revision R0.1 | 2026-10-23 | Owner Faisal Farouq

## Task control

**Artifact:** ASTRO-A-10

**Objective:** Connect every requirement to a reproducible acceptance method and honest evidence status.

**Required inputs:** Requirement baseline, 26 test specifications, qualified approved limits and test equipment later.

**Known values and provisional assumptions:** All 64 requirements mapped; 26 verification protocols planned; zero system verification runs executed.

**Unknowns:** Calibration records, actual software/hardware, run results, environmental conditions and reviewers.

**Calculations:** Planned traceability 64/64=100 percent; executed system verification 0/26=0 percent. Authoring QA is separate and cannot improve either physical result.

**Output file:** tests/10_verification_matrix.md

**Implementation steps:** 1. Approve protocol and limits. 2. Record configuration/calibration. 3. Run only authorized stage. 4. Capture failures and raw logs. 5. Review result. 6. Invalidate affected evidence when configuration changes.

**Acceptance test:** A PASS has a unique run, exact requirement/config revision, calibrated evidence and reviewer disposition; no pending test is represented as passed.

**Stop conditions:** Missing prerequisite, invalid calibration, lost logs/time sync, altered configuration, safety trip or fabricated evidence.

**Result:** REWORK - verification plan complete at baseline level; all system evidence missing

**Next dependency:** G1 software tests and G2 detailed physical test procedures

**Physical authorization and supervision:** Planned procedures do not authorize hazardous execution.

**Budget effect:** Test facility, review and instrument access remain unquoted allowances.

**Revision:** R0.1

**Date:** 2026-10-23

**Accountable owner:** Faisal Farouq

## Specification

The verification matrix in tests/verification_matrix.csv and the Verification workbook tab includes method, pass criterion, prerequisites and the reason each test is blocked. The requirement list in each verification record is generated from the requirement-to-test mapping to avoid stale cross references. Excluded functions have denial tests. Later-phase items have configuration and claim inspections rather than invented execution results.

Before executing a physical protocol, add numeric trip limits, sampling rates, equipment/fixture ratings, calibration validity, test location, operators, exclusion geometry, emergency procedure and an independently approved stop-time budget. Those values are intentionally not guessed in this baseline. Absence of any required value blocks enable. A provisional geometry angle is not an approved software limit.

Evidence record schema: evidence_id; test_id; requirement_ids; actual date/time and time-zone/UTC; actor/operator; reviewer; run result; requirement revision; hardware configuration; software and model hashes; signed limit-set hash; calibration references; environment; raw-log paths and SHA-256 hashes; deviations; stop events; limitations and disposition. Never prepopulate a future run as passed. Document-only QA records describe authoring consistency and rendering, and are explicitly outside robot verification.

Gait evidence must disclose tether loading. A visually plausible animation, simulation with ideal actuators, externally supported stepping motion or footage without synchronized logs cannot establish the full physical goal. Simulator mass/inertia/friction sweeps and failure injections support engineering decisions but do not validate the actual prototype. Handling and walking get different configuration IDs and test permits.
