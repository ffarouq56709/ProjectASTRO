# Revision history

R0.1 | 2026-10-23 | Owner Faisal Farouq

Initial provisional baseline from owner brief. Twelve connected artifacts, 64 requirements, 26 planned verification protocols, 20 preliminary risks and no executed system tests. Cap unchanged at USD 10000; illustrative commercial-actuation route USD 15899. No procurement, physical fabrication, professional approval or clinical validation.

R0.3 | 2026-10-28 | Owner Faisal Farouq

Day 6 rewritten with load, gait, drive, cost and mass screens (architecture/day_006_joint_load_screen.py). Kept 10 leg joints with no hip yaw. Owner reference photo added (cad_specifications/reference). Recommended hip-roll axes 0.30 m apart under wide shells, 3:1 stage on hip roll and 2:1 on knee. Arms pinned during gait; hands fixed. Handling drive changed to a bought guided linear actuator on a separate stand. Mass projection 48.5 kg + 6.5 kg reserve; bulky shell flagged as +1.6 kg risk. Actuator line screened at USD 2,841-3,481 from dated listings (not quotes). R0.2 Day 6 records archived in revision_history/day_006_revised_proposal_R0_2.zip. Working decision log added (decision_log_R0_3.csv); R0.1 decisions.csv unchanged. 365-day website plan rewritten to R0.3. No hardware, simulation, test, purchase or gate release.

R0.3 owner decisions | 2026-10-28 | Owner Faisal Farouq

Owner accepted the Day 6 R0.3 recommendations: D-03 Option A with 0.30 m hip-roll axes, 3:1 hip roll and 2:1 knee; D-04 bought actuator on a separate stand; D-01 USD 10,000 working cap until quotes (final Day 193). Day 6 PASS (document). Day 7 REWORK: D-02, D-05 open; D-06 awaiting confirmation; G0 BLOCKED.

G0 | 2026-10-28 | Owner Faisal Farouq

Owner accepted the R0.2 mission wording for all five Day 1 charter differences (D-06). Day 1 PASS. Day 7 PASS; G0 released for documentation, software and analysis only. D-02 deferred with dates; D-05 restricted to mock receiver.

Caregiver link proposal | 2026-11-04 | Owner Faisal Farouq

Added fictional patient SIM-002 (78, manual wheelchair, type 2 diabetes label; glucose in mg/dL; Demo Medications B and C; care-team notify values 70/250 mg/dL marked fictional) in simulated_patient_data/fictional_fixture_SIM-002.json; SIM-001 unchanged. New caregiver_workflows/05_caregiver_link_and_grounding.md: two-way mock caregiver line with verbatim replies, four record types, read-back before saving statements, eight anti-hallucination layers and grounding rules R1-R9. Prototype software/prototypes/grounding_check.py run on SIM-002: 17/17 cases as expected (desk prototype on fixture data, not a system test). Proposed JB-R-065 to 073 and JB-V-27 (grounding and record integrity) for owner decision D-07 on Day 14. Plan Days 17, 18, 29, 31, 34, 58, 62 and 67 updated. Mock receiver only (D-05).

D-01 update | 2026-11-04 | Owner Faisal Farouq

Owner raised the working cap from USD 10,000 to USD 15,000 (at least this much available). Website budget page and Day 193 updated. Days 5-7 records unchanged as history. Reserve recommendation: keep about USD 3,000 uncommitted until written quotes.

D-02, D-08, D-09 | 2026-11-04 | Owner Faisal Farouq

D-02: owner has outside contacts; outreach starts now. D-08: tethered walking stays a Year 1 must-have. D-09 proposed: caregiver feedback sessions on fictional scenarios only, ethics check first.

Budget tiers | 2026-11-04 | Owner Faisal Farouq

Added budget/budget_tiers_R0_4.md, .pdf and .csv: 55 part lines across five tiers (USD 15k to 50k) plus a beyond-50k list. Mid-estimate totals: 13,879 / 17,554 / 21,960 / 30,004 / 42,849. Listing prices checked 2026-11-04 for RobStride, Jetson Orin Nano Super, VectorNav VN-100, OptiTrack, RAZE gantry; all other lines are estimates. D-10 proposed: target the USD 25k tier.
