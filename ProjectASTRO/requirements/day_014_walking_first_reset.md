# Day 14 — walking-first reset review

Revision: R0.3  
Actual work date: 2026-11-05  
Accountable owner: Faisal Farouq  
Document status: project planning record; not an engineering, safety, procurement, legal or ethics review  
Owner time recorded: 2.0 hours  
Document result: **REWORK — owner decisions accepted; contact outreach not yet sent**

## Outcome

The owner accepted D-11 through D-15 on 2026-11-05. The milestone ladder, commercial-battery boundary, deterministic/template-first care architecture, public-name boundary and USD 25,000 planning tier are now project decisions.

The owner will contact the required people personally. No outreach message, contact name, communication channel, appointment or reply is recorded yet. Day 20 procurement remains blocked until an exact quote and purchase authorization exist. Powered work remains blocked until the applicable permit, reviewed limits and named second-person stop operator exist.

This record does not authorize a purchase, a battery, fabrication, energization or motion.

## D-11 through D-15

| ID | Recommendation reviewed | Current status | Next owner action |
|---|---|---|---|
| D-11 | Use the early milestone ladder: one joint Day 26, one-leg disposition Day 63, two legs hanging Day 81; retain formal standing and gait stages on Days 266–294. | ACCEPTED — owner 2026-11-05 | Preserve every formal gate and evidence requirement |
| D-12 | Do not build a custom battery pack. Use a documented commercial pack with matched BMS and charger after electrical and regeneration review. | ACCEPTED — owner 2026-11-05 | Identify the electrical reviewer; no battery purchase is authorized |
| D-13 | Keep the safety-relevant care path deterministic and template-first. Prefer local fictional-data evaluation; block cloud use until privacy, terms, grounding, latency and failure evidence are reviewed. | ACCEPTED — owner 2026-11-05 | Run the bounded Days 71–77 evaluation; cloud remains disabled meanwhile |
| D-14 | Use “Jacobs Caregiver Research Robot” publicly; retain Project ASTRO as an internal repository codename and avoid public character likeness or implied affiliation pending IP/legal review. | ACCEPTED — owner 2026-11-05 | Apply the boundary to future public material |
| D-15 | Use USD 25,000 as the recommended planning tier while USD 15,000 remains the current working cap; authorize only exact quoted purchases. | ACCEPTED — owner 2026-11-05 | Plan against USD 25,000; authorize each exact purchase separately |

The authoritative wording and accepted status are recorded in `revision_history/decision_log_R0_3.csv` from the owner’s explicit message.

## Early walking milestone evidence

| Milestone | Target | Minimum evidence before a GO disposition |
|---|---:|---|
| One joint on bench | Day 26 | Signed Day 19 permit; reviewed current/speed/travel limits; named second-person stop operator; both directions and both stop paths timestamped; no limit increase inferred from the result |
| One-leg rig | Day 63 | Five identities/configurations; five-node timing; supported pose, compliance, thermal and fault evidence; raw logs and hashes; floor contact and standing explicitly NOT TESTED |
| Two legs hanging | Day 81 | Ten-node timing; bounded synchronized trajectories; support load; phase/tracking/thermal evidence; support independent of motor torque; no standing or gait claim |
| Formal tethered standing | Day 266 | Reviewer-controlled S9 disposition from executed evidence and failed/stopped-run index |
| Weight shift | Day 273 | Reviewer-controlled S10 disposition from bilateral contact and stability evidence |
| One step | Day 280 | Reviewer-controlled S11 disposition from a controlled single-step trial |
| Three steps | Days 287 and 294 | First three-step disposition followed by a second trial and G6 disposition; target speed remains 0.10–0.15 m/s |

Early development milestones do not release G2–G5, standing or gait permits.

## Procurement boundary

Day 20 remains **BLOCKED**. No bench-actuator purchase is authorized because the following exact fields are absent:

- seller and quote date;
- RobStride 04 hardware and firmware revision;
- quantity and included cables/connectors;
- landed amount including freight, tax and tariff;
- warranty and return terms;
- owner’s written authorization for that exact line; and
- Day 19 permit readiness for later powered work.

The USD 319 value is a listing screen, not a landed quote or authorization. The requested 11-unit RFQ on Day 16 is an information request, not an order.

## Contact scheduling targets

| Needed for | Roles | What the request must ask for | Current evidence |
|---|---|---|---|
| Day 19 | Controls/safety reviewer; second-person stop operator | Bench-permit review, competence evidence, available date, scope and cost | OWNER WILL CONTACT — not yet scheduled |
| Day 24 | Electrical reviewer | Protected bench-supply and wiring review, inspection date, scope and cost | OWNER WILL CONTACT — not yet scheduled |
| Day 28 | Controls/safety and electrical reviewers; mechanical reviewer if fixture changed | First powered-evidence disposition and revised limits | OWNER WILL CONTACT — not yet scheduled |
| Day 35 | Mechanical/robotics and controls reviewers | Actuator GO / CONDITIONAL / NO-GO review for one-leg use | OWNER WILL CONTACT — not yet scheduled |
| Day 47 | Mechanical reviewer; rigging/facility provider; fabricator as applicable | Marked one-leg drawings, support/load-path comments and release conditions | OWNER WILL CONTACT — not yet scheduled |
| Day 56 | Mechanical, electrical and controls/safety reviewers; stop operator | Powered one-leg permit review and test-session availability | OWNER WILL CONTACT — not yet scheduled |

The owner’s commitment to contact them personally is recorded. It does not yet establish identity, competence, availability, appointment, cost or approval.

## Day 14 completion checks

- PASS: D-11 through D-15 each has a recommendation, status, owner action and decide-by day.
- PASS: the owner explicitly accepted D-11 through D-15 on 2026-11-05.
- PASS: no purchase is authorized without an exact item and amount; Day 20 is explicitly blocked.
- PASS: every powered milestone still requires a permit, reviewed limits and a second person.
- REWORK: the owner will perform outreach, but no scheduling request, appointment or reply is recorded yet.

## Sources

- `requirements/day_013_hazard_traceability.csv`
- `revision_history/decision_log_R0_3.csv`
- `requirements/contact_schedule.csv`
- `requirements/day_004_responsibility_matrix.csv`
- `Website/source/plan_w01_06.py`
- `Website/source/plan_w07_12.py`

