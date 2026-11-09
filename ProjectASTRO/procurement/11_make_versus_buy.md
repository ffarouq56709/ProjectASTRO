# Make versus buy and procurement plan

Revision R0.1 | 2026-10-23 | Owner Faisal Farouq

## Task control

**Artifact:** ASTRO-A-11

**Objective:** Prepare sourcing and fabrication decisions without buying from nominal or peak torque alone.

**Required inputs:** Frozen interfaces, load/duty models, quotes, safety requirements, budget and named fabricator.

**Known values and provisional assumptions:** Ten sourcing packages defined; no supplier selected or order placed; commercial actuator is a reference only.

**Unknowns:** Vendor curves, thermal conditions, delivery/returns, braking, mounting loads, complete quotes and service access.

**Calculations:** Commercial reference mass=10*0.85=8.5 kg before secondary transmission/mounts; 14 kg allocation leaves 5.5 kg for those parts, but gives no suitability proof.

**Output file:** procurement/11_make_versus_buy.md

**Implementation steps:** 1. Issue information/quote checklist. 2. Compare technical compliance. 3. Reconcile full BOM. 4. Complete independent G3 review. 5. Sign exact purchase lines. 6. Inspect delivered revision before use.

**Acceptance test:** Every major item has data, interface drawing, duty suitability, landed cost, inspection method and named release authority.

**Stop conditions:** Peak-torque-only selection, absent driver configuration, missing thermal data, cap overrun, unreviewed structural drawings or unnamed fabricator.

**Result:** BLOCKED - quote packages defined; design and procurement prerequisites absent

**Next dependency:** G2 architecture freeze then G3 procurement release

**Physical authorization and supervision:** Only an explicitly named authorized qualified fabricator may perform released structural work.

**Budget effect:** No expenditure approved; current reference route exceeds cap.

**Revision:** R0.1

**Date:** 2026-10-23

**Accountable owner:** Faisal Farouq

## Specification

The ten sourcing decisions are in procurement/make_vs_buy.csv and the Make Buy workbook tab. Buy protected commercial energy equipment, sensors and suitable safety components. Use qualified fabrication for structural load paths and fixtures. Make the deterministic record, consent, audit, summary and communication services. Reuse compute only after availability, ownership and suitability are documented.

Actuator request for information: exact model/hardware/firmware and driver option; output continuous torque versus speed; peak torque duration and recovery; allowable duty cycle versus ambient and cooling; motor and gear thermal limits; efficiency map; rotor/output inertia; backlash/compliance; encoder behavior on reboot; power-off/backdrive and brake behavior; radial/axial/moment bearing loads; mechanical life; absolute and full-charge voltage range; bus/phase current definitions; regen handling; fault/enable interface and safety claims; CAN protocol; dimensional STEP and 2D toleranced interfaces; service lead time; complete landed quote and warranty/returns. Without these, an impressive peak torque does not qualify a joint.

Every purchase request includes accepted requirement IDs, intended joints/configuration, drawing revision, vendor evidence, planned incoming inspection, cost impact, unresolved deviations and independent reviewer disposition. G3 release covers specific items and amounts. A prototype actuator order is still a purchase and needs separate owner authorization plus a safe bench-test plan; this baseline places none.

Incoming inspection records part/revision/serial number, physical condition, dimensions, weight, electrical ratings, connector/polarity and documentation. Qualified personnel execute energized checks on a restrained fixture after power/safety acceptance. Nonconforming material is quarantined and excluded from motion configurations. Fabrication drawings must include material, finish, critical tolerances, fastener specifications, load cases, inspection and revision. The master CAD envelope is not a released fabrication drawing.
