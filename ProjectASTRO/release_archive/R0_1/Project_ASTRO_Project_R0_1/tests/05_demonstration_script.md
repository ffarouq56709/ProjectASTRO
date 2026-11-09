# First year demonstration script

Revision R0.1 | 2026-10-23 | Owner Faisal Farouq

## Task control

**Artifact:** ASTRO-A-05

**Objective:** Define a reproducible demonstration with separate software, walking and stationary-handling evidence.

**Required inputs:** Accepted test plan, passed prior gates, fictional fixtures, approved recipient and calibrated logging.

**Known values and provisional assumptions:** Two three-step trials; 10 supported 2 kg repetitions; software first; no public hazardous first integration.

**Unknowns:** Actual trial speed, step geometry, tether-load criterion, stop limits and facility configuration.

**Calculations:** Handling example: 0.10 m lift at 0.02 m/s takes 5 s upward; down takes 5 s; 5 s top and bottom dwell gives 20 s/cycle, 200 s for 10 cycles. Proposed timing only.

**Output file:** tests/05_demonstration_script.md

**Implementation steps:** 1. Execute software segment. 2. Review physical permits. 3. Execute walking independently. 4. Reset and mechanically secure for handling. 5. Export evidence and limitations.

**Acceptance test:** All segment criteria below met with complete raw logs; any omitted segment means partial demonstration only.

**Stop conditions:** Any unreviewed gate, barrier entry, arrest catch, unexpected motion, limit trip, communication misstatement, payload release or loss of synchronized evidence.

**Result:** REWORK - script defined; physical and software prerequisites absent

**Next dependency:** G1 software demonstration then G5 to G8

**Physical authorization and supervision:** All powered work requires named test director, authorized operator, stop operator and qualified support/rigging review.

**Budget effect:** No commitments; separate segments avoid added integration scope.

**Revision:** R0.1

**Date:** 2026-10-23

**Accountable owner:** Faisal Farouq

## Specification

Preflight: record run ID, requirement revision, software/model/configuration hashes, operator names and actual date/time. Confirm all data are fictional. Load profile SIM-001 and local test recipient RECIPIENT-UNASSIGNED only as a non-sendable placeholder until the owner names a consenting recipient. Demonstrate the manual human-contact button. State that this is a research prototype and no patient or emergency service is involved.

Segment A on laptop: choose the older-adult preset; show large text/captions and privacy control. Play one short word game; start a feelings check-in and confirm an actor note. In separate scripted branches show the child, adult, rehabilitation and limited-speech/mobility presets. Insert simulated heart rate, oxygen saturation, temperature, activity/rest and patient-reported entries. Show trend, source, unit and time, then correct a deliberately inaccurate fictional entry and show both versions and access history.

Segment B on laptop: display fictional medication instructions exactly as entered; record a skipped dose and decline one send. Show that no message left the outbox. Create a new exact-preview approval and send to the approved mock recipient. Demonstrate endpoint receipt and separately a human review action. Disable the endpoint, show bounded retries and unconfirmed delivery, and offer manual contact. Cross an artificial simulation review rule and show non-diagnostic explanation. Start and end an approved audio/video test call with visible capture state. Export the human-readable shift report and audit trail.

Segment C in the cleared test area after all motion gates: operator verifies support rig, stop function, interlock, thermal baseline, charge state and log synchronization. With no test payload attached, perform one approved three-step sequence, settle, stop and inspect. Reset, then perform the second sequence. Count distinct alternating swing/landing events using foot contact and video. Record pelvis displacement and time, peak/RMS joint loads, temperature, current and tether load. No arrest catch, external propulsion or operator stabilization counts as a successful gait trial. Tether pretension/support limits must be accepted before the run; report any sustained weight assistance. Target speed is assessed on the defined first-toe-off to third stable landing interval with its distance convention fixed in the protocol. Startup/settling timing must be reported separately.

Segment D in a separately secured stationary fixture: disable walking and verify support/payload interlocks. Use a captured 2.00 kg inert object over a guarded catch tray. Proposed motion is 0.10 m vertical travel at <=0.02 m/s and <=0.30 m horizontal reach, with reviewed self-weight, grip and force limits. Execute 10 complete up/dwell/down/dwell cycles. Record each repetition and every stop. No walking occurs with the object. A stopped repetition is retained as an attempt; do not erase it or count it as complete. The full test is rerun only after a reviewed cause and disposition.

Closeout: remove drive enable, secure gravity loads, export raw logs, hashes, configuration, event video and approved-recipient receipt. Record each criterion as PASS, REWORK or BLOCKED with evidence. State measured outcomes and remaining limitations aloud. If physical gates are unavailable, present the software segment and simulation visualization with a clear partial-completion label; the Year 1 physical goals remain unmet.
