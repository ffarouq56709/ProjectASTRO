# Ranked feature backlog

Revision R0.1 | 2026-10-23 | Owner Faisal Farouq

## Task control

**Artifact:** ASTRO-A-08

**Objective:** Rank useful additions without silently expanding the first-year scope.

**Required inputs:** Capability brief, dependency readiness and ordinal benefit/risk/cost/time judgments.

**Known values and provisional assumptions:** 22 features scored on benefit, risk, cost and time from 1 to 5; dependencies can block any rank.

**Unknowns:** User-study benefit, actual effort, license costs, endpoint access and qualified reviewers.

**Calculations:** Score=2*benefit+(6-risk)+(6-cost)+(6-time), maximum 25. Example consent dashboard=2*5+5+5+5=25. Score is an editorial planning heuristic, not quantified safety or ROI.

**Output file:** requirements/08_feature_backlog.md

**Implementation steps:** 1. Review score definitions. 2. Resolve dependencies before selection. 3. Implement Year 1 core. 4. Re-score additions after evidence. 5. Approve scope changes through new requirements.

**Acceptance test:** All ideas requested in brief represented or grouped explicitly; ranking reproducible; no later feature presented as committed.

**Stop conditions:** New feature changes clinical scope, real-data policy, physical risk or cap without review.

**Result:** PASS - ranked planning backlog; benefits and effort unvalidated

**Next dependency:** G1 core software backlog selection

**Physical authorization and supervision:** Physical additions need their own reviewed motion/fixture gates.

**Budget effect:** No spend approved; relative cost ratings are not price quotes.

**Revision:** R0.1

**Date:** 2026-10-23

**Accountable owner:** Faisal Farouq

## Specification

The complete ranked backlog is requirements/feature_backlog.csv and the Backlog workbook tab. Benefit 1 means low expected caregiver value and 5 high. Risk 1 means low incremental risk and 5 high; cost and development time use the same low-to-high ordinal scale. The score supports discussion; mandatory safety, privacy and accessibility controls are implemented as requirements even if a numerical rank changes. Ties use stable feature IDs. Changing a score in the workbook recomputes score and numerical rank; sort the table by rank after editing, because row order is a baseline snapshot.

Consent, accessibility, human-contact controls, summaries, daily check-ins, privacy mode, curated engagement, maintenance reminders and approved telepresence are first-year software work. Basic appointment reminders and static wayfinding use fictional schedules and do not imply public navigation. The manual board provides a non-speech fallback.

Teach-back is limited to exact approved material and cannot certify understanding. Multilingual interaction needs reviewed translations. Family media requires consent and moderation. Room control requires approved interfaces and bounded permissions. Delivery, laundry and meal requests are communication relays before physical transport. Rehabilitation games require qualified clinician-authored motions and a separate motion release. Cart/trolley/cargo alternatives are evaluated for heavier loads before biped payload growth. A counterbalanced or detachable supported module is a Year 1 design option rather than an extra promised robot arm.
