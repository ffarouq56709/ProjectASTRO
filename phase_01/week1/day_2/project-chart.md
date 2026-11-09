# Project ASTRO Caregiver-Support Robot — Project Charter v1.0

| Field | Value |
|---|---|
| Day | 2 |
| Phase | Phase 1 — Requirements, access, and risk |
| Week | 1 |
| Revision | v1.0 |
| Date | 2026-10-23 |
| Owner | Faisal Farouq |
| Units | SI units: millimeters (mm), kilograms (kg), seconds (s), meters per second (m/s), newtons (N), and newton-meters (N·m) |
| Hardware required today | None |
| Previous accepted inputs | [Day 1 accepted input summary](#day-1-accepted-input-summary) |

## 1. Required tools and inputs

Tools needed today:

- Text editor
- Day 1 requirements table
- Project calendar
- Version-control or revision-history system

Parts and materials needed today:

- No hardware
- No fabrication materials
- No physical shop access

## 2. Project purpose

The Project ASTRO project will create a 1,829 mm-tall ASTRO-style caregiver-support robotics prototype.

The project will explore:

- Slow tethered bipedal walking
- Friendly human interaction
- Consent-based health-data collection
- Caregiver or medical-team notification
- Controlled object handling
- Removable plastic body panels

The prototype may support caregivers and medical professionals, but it will not replace them. It will not independently diagnose, treat, or prevent a medical condition.

## 3. First-year demonstration target

The first-year prototype will demonstrate the following capabilities as separate controlled tests:

1. A 1,829 mm-tall robot completes two successful sequences of three consecutive tethered steps.
2. The target walking speed is between 0.10 m/s and 0.15 m/s.
3. The robot receives simulated or properly consented measurements from approved external health sensors.
4. Every health reading includes its source, value, units, timestamp, and whether the data is simulated or real.
5. The robot recognizes a scripted concerning event and asks whether assistance is needed.
6. After confirmation, the robot sends a structured test report to an approved test recipient.
7. While stationary and mechanically supported, the robot lifts a 2 kg test object.
8. The robot uses removable plastic panels to create its external ASTRO-style body.
9. The robot records test evidence and clearly communicates its limitations.

Walking while carrying the payload is not included in the first-year demonstration.

## 4. Requirement-status definitions

### PROVISIONAL TARGET

A value selected for planning and early engineering. It has not yet been proven through completed analysis or physical testing.

### VALIDATED

A requirement supported by completed calculations, simulations, inspections, or physical testing and accepted at the appropriate project gate.

### REWORK

The requirement is properly defined, but the current design does not satisfy it.

### BLOCKED

Necessary information, authorization, evidence, equipment, funding, or ownership is missing.

Unless explicitly marked **VALIDATED**, every numerical value in this revision is a **PROVISIONAL TARGET**.

## 5. Shall-requirements

| ID | Shall-requirement | Owner | Verification method | Current status |
|---|---|---|---|---|
| SYS-001 | The robot shall have an overall sole-to-crown height of 1,829 ± 10 mm. | Faisal Farouq | Measure the master CAD model and later measure the completed robot from the standing surface to its crown. | PROVISIONAL TARGET |
| SYS-002 | The robot shall have a target operating mass of 55 kg or less. Design work shall stop for review if the projected mass exceeds 65 kg. | Faisal Farouq | Compare the CAD mass report, purchased-component masses, body-panel masses, and final scale measurement. | PROVISIONAL TARGET |
| SYS-003 | The lower body shall contain 10 active joints: hip pitch, hip roll, knee pitch, ankle pitch, and ankle roll on each leg. | Faisal Farouq | Inspect the joint register, CAD assembly, simulation model, control configuration, and completed robot. | PROVISIONAL TARGET |
| WALK-001 | The robot shall complete three consecutive tethered steps twice at a target speed of 0.10–0.15 m/s inside a cleared test area. | Faisal Farouq | Review synchronized test video and telemetry produced during an authorized walking test. | PROVISIONAL TARGET |
| BUD-001 | Total project spending shall remain between USD 6,350 and USD 10,000, including contingency. | Faisal Farouq | Compare approved purchases, invoices, estimates, and the final cost ledger with the gated project budget. | PROVISIONAL TARGET |
| ACCESS-001 | Restricted fabrication, plastic forming, high-energy wiring, battery handling, lifting, energization, load testing, and walking tests shall be performed only by a named person or vendor authorized to perform that work. | Faisal Farouq | Inspect the authorization record, work order, and returned fabrication or test evidence for every gated task. | REQUIRED CONTROL |
| HEALTH-001 | The robot shall receive simulated or consented heart-rate, oxygen-saturation, temperature, or activity data from approved external sensors. | Faisal Farouq | Demonstrate receipt of the sensor ID, measured value, units, timestamp, and simulated-or-real-data label. | PROVISIONAL TARGET |
| HEALTH-002 | The robot shall not convert a sensor reading into an independent medical diagnosis or treatment recommendation. | Faisal Farouq | Review all displayed messages, generated reports, spoken responses, and demonstration scripts. | REQUIRED CONTROL |
| ALERT-001 | After a confirmed scripted alert, the robot shall send a structured test report to an approved recipient within 60 seconds. | Faisal Farouq | Compare the confirmation timestamp with the receiving-system timestamp during a controlled test. | PROVISIONAL TARGET |
| PRIV-001 | The system shall obtain recorded consent before collecting or transmitting identifiable health information. | Faisal Farouq | Verify the consent record, approved-recipient list, communication configuration, and transmission log before testing. | REQUIRED CONTROL |
| LIFT-001 | While stationary and mechanically supported, the robot shall lift a 2 kg test object from approximately 500 mm to 1,000 mm above the floor for 10 supervised repetitions. | Faisal Farouq | Record the payload mass, lift height, actuator telemetry, support configuration, and post-test inspection. | PROVISIONAL TARGET |
| BODY-001 | The external body shall use approximately 28 removable plastic panels with a combined target mass of 8 kg or less, nominal panel gaps of 3 mm, and at least 12 mm of clearance from moving mechanisms. | Faisal Farouq | Review the panel schedule, CAD clearance analysis, panel measurements, individual panel masses, and completed installation. | PROVISIONAL TARGET |
| CLAIM-001 | The first-year prototype shall not claim to diagnose disease, recommend treatment, replace a caregiver or clinician, guarantee emergency response, lift a person, walk untethered in public, or walk while carrying a heavy payload. | Faisal Farouq | Review the charter, user interface, reports, demonstration script, video captions, and published project description. | REQUIRED CONTROL |

## 6. Named project parameters

| Parameter | Symbol | Provisional value | Units |
|---|---:|---:|---|
| Overall robot height | `H_TOTAL` | 1,829 | mm |
| Target operating mass | `M_TARGET` | 55 | kg |
| Mass design-stop limit | `M_STOP` | 65 | kg |
| Active lower-body joints | `N_LEG_DOF` | 10 | joints |
| Consecutive steps required | `N_STEPS` | 3 | steps |
| Successful walking sequences | `N_SEQUENCES` | 2 | sequences |
| Minimum walking speed | `V_WALK_MIN` | 0.10 | m/s |
| Maximum walking speed | `V_WALK_MAX` | 0.15 | m/s |
| Required stationary payload | `M_PAYLOAD` | 2 | kg |
| Stretch payload | `M_PAYLOAD_STRETCH` | 5 | kg |
| Maximum alert-delivery time | `T_ALERT_MAX` | 60 | s |
| Approximate plastic-panel count | `N_PANELS` | 28 | panels |
| Maximum combined panel mass | `M_PANELS_MAX` | 8 | kg |
| Minimum moving-part clearance | `C_PANEL_MIN` | 12 | mm |
| Nominal panel gap | `G_PANEL` | 3 | mm |
| Lower budget target | `COST_LOW` | 6,350 | USD |
| Maximum budget | `COST_HIGH` | 10,000 | USD |

## 7. Access boundary

Faisal Farouq is the accountable project owner.

Project ownership does not automatically provide authorization to use equipment or perform restricted physical work.

Faisal Farouq may complete:

- Requirements development
- Research and documentation
- CAD design
- MuJoCo simulation
- Motor and gearbox calculations
- Structural calculations
- Electrical design
- Software development
- Test planning
- Budget tracking
- Supplier communication
- Inspection of returned parts
- Low-energy fitting of properly prepared parts when permitted

The following activities remain gated:

- Cutting, drilling, machining, or powered trimming
- Heating, bending, or vacuum-forming plastic
- Welding or structural metal fabrication
- High-energy electrical assembly
- Battery construction or modification
- Lifting or supporting the assembled robot
- Energizing high-power actuators
- Structural proof testing
- Payload testing
- Walking tests

Every gated task requires:

1. A named authorized executor
2. Released drawings or work instructions
3. Applicable facility or vendor procedures
4. Defined acceptance measurements
5. Returned photographs, measurements, inspection records, or test data

Jacobs Makerspace access by itself does not prove authorization to use a particular tool.

## 8. Excluded first-year claims

The first-year prototype will not claim that it:

- Diagnoses a disease or medical emergency
- Recommends medication or treatment changes
- Replaces a caregiver, nurse, physician, or emergency service
- Guarantees that an alert reaches or is reviewed by medical personnel
- Safely lifts, catches, transfers, or physically supports a person
- Operates untethered around members of the public
- Walks while carrying the test payload
- Autonomously responds to a real emergency
- Has validated a value that remains marked as a provisional target

## 9. Assumptions

1. Caregiver reporting will initially use simulated events and an approved test recipient.
2. Identifiable health data will remain disabled until consent, privacy, security, and institutional requirements are accepted in writing.
3. Commercial external sensors will provide the initial health measurements.
4. Lower-body walking remains the primary hardware objective.
5. The 2 kg lifting test will be stationary, mechanically supported, and separate from walking.
6. The 5 kg payload is a stretch goal requiring separate structural, actuator, budget, and safety approval.
7. The plastic body panels will not carry primary structural loads.
8. The object-handling mechanism may be simplified, counterbalanced, or tested as a separate module if the complete robot cannot meet its mass or budget limits.

## 10. Open questions

- Who will review and accept the structural calculations?
- Who will review the fall-protection and tethering plan?
- Which approved external sensors will be used?
- Where will caregiver test alerts be sent?
- What privacy and consent rules apply to the planned health-data demonstration?
- What arm mechanism can lift 2 kg without violating the mass limit?
- Who is authorized to fabricate the structural frame?
- Who is authorized to manufacture the plastic panels?
- Does the USD 10,000 limit include external sensors and communication services?
- Can the 55 kg mass target be maintained after adding the arms and plastic panels?

These questions do not block completion of the Day 2 charter. They must be resolved before the affected design, purchasing, fabrication, or testing gate.

## 11. Day 1 accepted input summary

Day 1 established the following accepted planning inputs:

- ASTRO-style caregiver-support research prototype
- 1,829 mm overall height target
- 55 kg operating-mass target
- 65 kg mass design-stop limit
- 10 active lower-body joints
- Three consecutive tethered steps
- Target walking speed of 0.10–0.15 m/s
- USD 6,350–10,000 gated budget
- Remote engineering by default
- Authorized execution for restricted physical work
- Health observation and reporting without diagnosis
- Stationary 2 kg payload requirement
- 5 kg payload retained as a future stretch goal
- Removable plastic body panels instead of an inflatable exterior

This section is the traceable internal link to the previous accepted project inputs.

## 12. Day 2 comparison and completion decision

### Required comparison

| Acceptance item | Required value | Charter value | Result |
|---|---:|---:|---|
| Overall height | 1,829 mm | 1,829 ± 10 mm | PASS |
| Consecutive steps | 3 | 3 | PASS |
| Walking speed | 0.10–0.15 m/s | 0.10–0.15 m/s | PASS |
| Active lower-body joints | 10 | 10 | PASS |
| Owner assigned | Required | Faisal Farouq | PASS |
| Verification methods assigned | Required | Assigned to every requirement | PASS |
| Provisional values identified | Required | All unvalidated values marked | PASS |

### Day 2 status

**PASS — artifact completeness only.**

Every required category has:

- A measurable requirement
- A named owner
- A verification method
- A status
- A numerical value or explicit control condition

This PASS does not authorize:

- Hardware purchasing
- Fabrication
- Tool use
- Battery work
- Robot energization
- Structural load testing
- Medical use
- Payload testing
- Walking tests

### Stop condition

Stop and mark the charter **BLOCKED** if any required requirement loses its:

- Numerical value or explicit control condition
- Named owner
- Verification method

### Next dependency

Day 3 shall analyze this charter for:

- Conflicting requirements
- Missing requirements
- Mass-budget pressure
- Financial-budget pressure
- Verification gaps
- Safety gaps
- Caregiver-feature risks
- Privacy and consent requirements
- Plastic-panel effects on movement and cooling

Any change to the height, mass, walking claim, payload, caregiver-reporting scope, access boundary, or excluded claims must create a new charter revision.

## 13. Revision history

| Revision | Date | Author | Change |
|---|---|---|---|
| v0.1 | 2026-10-21 | Faisal Farouq | Initial project framing and measurable success criteria |
| v1.0 | 2026-10-23 | Faisal Farouq | Added caregiver-support scope, health-data reporting, stationary payload requirements, plastic-panel requirements, named parameters, access boundaries, and provisional-status rules |
