# System architecture and boundaries

Revision R0.1 | 2026-10-23 | Owner Faisal Farouq

## Task control

**Artifact:** ASTRO-A-02

**Objective:** Define modular interfaces that prevent AI failures from becoming unrestricted motion or silent care-data changes.

**Required inputs:** Mission, requirements, hazard log, candidate joint topology, data policy and selected safety components later.

**Known values and provisional assumptions:** 15 modules from the brief; local-first fictional care service; independent safety chain; topology A-02 remains provisional.

**Unknowns:** Safety integrity requirement, braking strategy, final bus/voltage, model provider and stop-time budget.

**Calculations:** Stop-envelope screening: d = v*t + v^2/(2*a). For v=0.15 m/s, t=0.10 s and a=0.50 m/s2, d=0.0375 m. This translation-only example excludes limb sweep, fall, latency variation and arrest dynamics; it sets no separation distance.

**Output file:** architecture/02_system_architecture.md

**Implementation steps:** 1. Assign interfaces below. 2. Separate credentials and motor networks. 3. Define signed limits and fail states. 4. Freeze topology at G2. 5. Test denied paths before hardware integration.

**Acceptance test:** ASTRO-V-04, 08, 09, 16 and 19 demonstrate interface consistency and denied unauthorized paths; none is executed yet.

**Stop conditions:** AI direct bus access, AI writable safety limits, uncontrolled gravity on stopping, or record mutation without authorization.

**Result:** REWORK - conceptual interfaces defined, hardware and safety response unresolved

**Next dependency:** G2 safety requirements and architecture freeze

**Physical authorization and supervision:** Qualified controls/electrical/rigging review before any powered implementation.

**Budget effect:** No commitments; interfaces may change component costs at G3.

**Revision:** R0.1

**Date:** 2026-10-23

**Accountable owner:** Faisal Farouq

## Specification

The mechanical load path runs from the removable exterior and upper structures through the pelvis, lower-body joints and feet to the floor. Exterior panels are non-structural unless later drawings explicitly qualify them. The object-handling module has a separate support path and enable condition. Robot arrest and handling fixtures stay effective without controller or battery power.

The companion model receives only consented fictional context. It proposes typed actions to a deterministic interaction gateway. That gateway can request a curated game, draft a note, request a report preview or request a named bounded motion skill. It cannot open a motor bus, write a database, choose a recipient, change limits or write original medication instructions. Human confirmations bind to the actual proposed revision or transmission. AI-generated text is untrusted until schema and authorization checks pass.

The care-record and medication-log services own validated transactions. The record service appends corrections with superseded-version links. Audit events record create, view, change, deny and transmit actions. A deterministic summary builder cites source IDs. The model may rephrase a draft only where the final facts are checked against those IDs. Medication instructions remain an immutable original string per human-authorized version.

The communication service receives an approved immutable report snapshot, recipient ID and approval token bound to its hash. A local outbox owns idempotency and retry states. A mock receiver returns endpoint receipt. Human review is a separate explicit authenticated action. Telepresence requires capture consent and a visible call state. External EHR routes and credentials are absent from the Year 1 deployment.

The main motion controller owns standing, weight-shift and gait skills. A separate safety controller supervises independently available enable, stop, watchdog and relevant fault signals. E-stop hardware inhibits hazardous drive enable through a reviewed independent path. A diagnostic controller does not become safety-rated by being independent. Required integrity, channels, monitored contacts, brake behavior and fault coverage need qualified review. Torque-off alone does not hold up a biped. Mechanical support and arrest remain mandatory. Reset clears a latch only after fault resolution and never resumes motion automatically.

Modules M01 structure, M02 lower actuation, M03 feet/contact, M04 protected power, M05 safety, M06 main compute, M07 perception, M08 companion, M09 records, M10 medication, M11 communication, M12 handling, M13 body, M14 evidence and M15 simulation have distinct ownership of state. Evidence subscribes read-only to timestamped events. Simulation emits a distinctly labeled simulation channel and has no hardware credentials. Safety event logging must survive AI or network failure.

The candidate joint tree has l_hip_roll, l_hip_pitch, l_knee_pitch, l_ankle_pitch, l_ankle_roll and the corresponding r_ names. With x forward, y left and z up, roll axes are x and pitch axes are y. There is no hip yaw. This supports investigation of straight-line tethered stepping; turning is excluded. Candidate limits and dimensions live in the CAD and simulation specifications and are not operational safety limits.
