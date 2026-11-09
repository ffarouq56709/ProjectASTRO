# Requirements and phase allocation

Revision R0.1 | 2026-10-23 | Owner Faisal Farouq

## Task control

**Artifact:** ASTRO-A-03

**Objective:** Create testable uniquely identified requirements separated by Year 1, later phases and exclusions.

**Required inputs:** Owner brief, architecture and test IDs.

**Known values and provisional assumptions:** 64 requirements; every row maps to a planned verification ID and evidence status.

**Unknowns:** Owner acceptance, approved tolerances and specialized implementation limits.

**Calculations:** Coverage = mapped requirements / total requirements = 64/64 = 100 percent planned mapping; executed verification coverage = 0/64 = 0 percent.

**Output file:** requirements/03_requirement_matrix.md

**Implementation steps:** 1. Review each shall statement. 2. Accept or revise phase. 3. Freeze accepted revision. 4. Add new IDs for new scope; never recycle IDs. 5. Link executed runs without overwriting failures.

**Acceptance test:** No duplicate IDs, missing phase or missing verification mapping; no unexecuted performance PASS.

**Stop conditions:** Excluded capability is enabled, a safety limit is guessed, or a requirement loses source/evidence traceability.

**Result:** PASS - specification mapping complete; all requirements unvalidated

**Next dependency:** G0 owner acceptance then detailed verification planning

**Physical authorization and supervision:** Document review only.

**Budget effect:** No change; scope additions require cost/mass impact review.

**Revision:** R0.1

**Date:** 2026-10-23

**Accountable owner:** Faisal Farouq

## Specification

The authoritative requirement records are requirements/requirements.csv and the Requirements workbook tab. Phase values are Year 1, Later and Excluded. Excluded rows are enforceable negative requirements; they still require verification. Later rows define a gate for future work and do not expand the first-year commitment.

Height acceptance of 1.829 m +/-0.020 m is a proposed build tolerance for owner acceptance, not an alteration of the target. Mass <=55 kg remains a target. Crossing 55 kg triggers rework even though the major-review threshold is >65 kg. Speed is reported as a target-achievement result alongside step completion; a slower safe trial cannot be described as meeting the speed target.

Requirement status BLOCKED - NOT TESTED means implementation or evidence is missing. It does not mean the documentation is incomplete or that failure has been observed. A planned test, plausible calculation or budget allocation cannot close a physical requirement. Each release must preserve the accepted requirement revision, actual configuration and authorized reviewer disposition.
