# Caregiver workflows

Revision R0.1 | 2026-10-23 | Owner Faisal Farouq

## Task control

**Artifact:** ASTRO-A-04

**Objective:** Specify observable consent-led workflows for engagement, medication, observations and staff communication.

**Required inputs:** Fictional profile fixtures, consent scope, approved recipient, deterministic policies and record schema.

**Known values and provisional assumptions:** All data simulated; four communication priorities are non-clinical; five interaction presets.

**Unknowns:** Approved recipient identity, retention period, final accessibility review and endpoint details.

**Calculations:** Retry example: initial attempt at 0 s, retries at 5 s, 15 s and 35 s; after 3 retries show delivery unconfirmed and offer manual contact. Intervals are software test values, not an emergency-response commitment.

**Output file:** caregiver_workflows/04_caregiver_workflows.md

**Implementation steps:** 1. Load allowed fixture. 2. Confirm consent and mode. 3. Run the four flows below. 4. Exercise corrections/declines/offline behavior. 5. Record audit and source IDs.

**Acceptance test:** ASTRO-V-10 to 19 and 21; each decline and failure has an auditable truthful outcome.

**Stop conditions:** Real data, recipient outside allowlist, clinical advice, approval mismatch, capture consent withdrawn or corrupted audit.

**Result:** PASS - workflow specification ready for software implementation; no execution claimed

**Next dependency:** G1 fixture and recipient policy approval

**Physical authorization and supervision:** Scripted adult actors on laptop; participant work needs an approved protocol.

**Budget effect:** Within B-06 and B-12 allowances; no spend committed.

**Revision:** R0.1

**Date:** 2026-10-23

**Accountable owner:** Faisal Farouq

## Specification

Start each session with the research role and SIMULATED banner. Select a fictional profile and identify the actor role. Ask separately for preference memory, note storage, microphone/camera use and report transmission. A user can decline an activity or withdraw capture consent. If free text appears to contain real personal/health information, pause entry and ask the operator to replace it with fictional fixture data; heuristic detection alone is not a privacy guarantee.

Companionship flow: offer a consented game, story, music/relaxation or feelings check-in; accept a selection through speech, touch or communication board. Ask for clarification when uncertain. A sensitive concern yields a short supportive response and an offer to contact the approved caregiver. Record a note only after the actor confirms the wording. Child preset uses age-appropriate curated content and guardian-controlled settings; older-adult preset offers slower speech and repetition; rehabilitation preset uses seated verbal/visual activities unless a separate motion script is approved; limited-speech/mobility preset provides large targets, captions and a manual board. No preset authorizes clinical or person-contact motion.

Medication flow: a deterministic reminder displays the exact original instructions for fictional Demo Medication A, instruction version and source. Ask taken, skipped, postponed or no response. Record it as a patient statement, never confirmed ingestion. Postponed does not change the prescribed schedule and the robot supplies no catch-up or double-dose guidance. A scripted skipped/missed response prepares a report. Show recipient and complete contents, then require explicit send confirmation. No confirmation means no outbound message; retain the pending draft. Human-authorized record changes create a new version and preserve the original.

Observation flow: receive only an allowed simulator fixture or actor-entered simulated value. Validate metric type, units, source, observed time and actor; record both observed and recorded time. Show trends as descriptive values, with missing/stale flags and no diagnostic label. A deliberately artificial threshold crossing says: 'This simulated reading crossed the demonstration review rule. I cannot determine what it means. Would you like to contact your approved caregiver?' Show the exact trigger. The fixture uses an intentionally non-clinical test threshold and is never a clinical limit.

Staff communication flow: choose routine summary, caregiver attention requested, immediate human contact requested or system assistance required. Assemble facts, actor statements, robot observations and unknowns as separate fields. Preview exact recipient, time window, simulated readings, medication responses, concerns and robot status. Approval binds to report hash, version and recipient. Altered drafts return to preview. Send only to an allowlisted mock receiver; audit every attempt and use the same idempotency key on retry. Show queued, attempted, endpoint received and separately human reviewed. Timeout displays unconfirmed delivery and a manual call option. No state implies emergency dispatch.

Corrections append a superseding record with reason, actor, before/after version and audit event. Unauthorized reads and changes are denied and audited. Local mock mappings use Observation-like value/time/source records, Provenance-like origin/revision records and AuditEvent-like access events. These borrow structure from HL7 R4 references SRC-06 to 08; they do not claim FHIR conformance or connectivity.
