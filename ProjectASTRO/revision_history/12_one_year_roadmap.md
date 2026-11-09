# One year roadmap and release gates

Revision R0.1 | 2026-10-23 | Owner Faisal Farouq

## Task control

**Artifact:** ASTRO-A-12

**Objective:** Sequence six workstreams through explicit procurement fabrication and test gates while preserving a software-first result.

**Required inputs:** Accepted baseline, staffing capacity, facility, quotes, CAD/simulation evidence and safety reviews.

**Known values and provisional assumptions:** Months 1-12 are relative to G0 acceptance; indicative dates 2026-11-02 to 2027-11-01 are provisional.

**Unknowns:** Staff hours, skills, fabrication lead time, facility access, budget feasibility and actuator lead times.

**Calculations:** No schedule confidence percentage is calculated without resource/lead-time data. A missed gate shifts dependent work; calendar dates never waive prerequisites.

**Output file:** revision_history/12_one_year_roadmap.md

**Implementation steps:** 1. Accept G0 and name roles. 2. Run the six workstreams below. 3. Review gate evidence, cost and mass monthly. 4. Release only next authorized stage. 5. Archive final evidence and limitations at G8.

**Acceptance test:** G0-G8 have named authority, deliverables and release restrictions; all 16 integration stages stay in order.

**Stop conditions:** Over-cap BOM, unstaffed specialist role, unapproved gate, missing support or attempted schedule bypass.

**Result:** REWORK - dependency roadmap defined; dates and resources unconfirmed

**Next dependency:** D-01 to D-05, then G0 baseline acceptance

**Physical authorization and supervision:** Procurement and physical work require gate-specific written authorization; none supplied here.

**Budget effect:** Cap unchanged; no committed spend; schedule/resource changes require a revised estimate.

**Revision:** R0.1

**Date:** 2026-10-23

**Accountable owner:** Faisal Farouq

## Specification

Workstream A maintains requirements, safety/ethical risks, assumptions, decisions, access matrix, verification and excluded claims throughout the year. Faisal Farouq chairs owner decisions; independently qualified people review specialized engineering. A document status PASS is not a physical release.

Workstream B builds the companion and caregiver laptop experience in months 1-3, then tests and refines it through month 12. Complete fictional-data, medication, consent, summary, audit and communication failure tests before connection to any robot. This work can progress while mechanical feasibility remains open, using confirmed available equipment and no unapproved spending.

Workstream C develops the master CAD skeleton, five-joint-per-leg candidate, feet, load cases, mass/COM/inertias, protected power, safety stop behavior and panel schedule in months 2-4. Workstream D develops the pinned-version MuJoCo model concurrently using the same names/axes/limits and documented mass/inertia estimates. Standing, weight-shift and three-step sweeps include friction, delay, backlash, thermal/duty constraints and failure injection. The simulator includes a calibrated tether approximation; its assistance is logged. Nothing here claims those models or simulations have been executed.

Workstream E prepares quotes and interface/inspection packages in months 3-5, with expensive orders blocked until G3. If no credible whole-system route fits USD 10000, the owner must retain the cap and revise resources, design or schedule through a recorded decision. The walking commitment is not silently removed, and a budget increase is not implied. Fabrication starts only at G4 with a named qualified shop and released drawings.

Workstream F follows the exact staged order: 1 software-only caregiver demonstration; 2 sensors; 3 individual actuator module; 4 power system; 5 safety controller and stops; 6 one joint; 7 one leg on fixture; 8 lower-body structure without walking; 9 supported standing; 10 weight shifting; 11 one tethered step; 12 three consecutive tethered steps; 13 repeated three-step sequence; 14 stationary supported handling; 15 shell clearance/thermal testing; 16 full caregiver-support demonstration. Each stage has separate evidence and a release for the next. Simulation evidence before purchasing is distinct from physical powered-actuator acceptance after receipt.

Indicative timing: G0 month 1; G1 months 1-3; G2 months 2-4; G3 months 4-5; G4 months 5-6; G5 months 6-8; G6 months 8-10; G7 months 10-11; G8 month 12. Relative timing starts only when G0 is accepted. Staffing and lead times are unknown, so this is a dependency plan, not a promise of a completed full-size biped in one year.

At G8 archive the accepted requirements, as-built BOM/drawings, actual spend, configuration hashes, calibrated logs, approved protocols, raw failures, verified outcomes and limitations. A software-only fallback may be shown when motion gates are blocked, labeled as partial completion. No public demonstration is the first test of two hazardous subsystems together.
