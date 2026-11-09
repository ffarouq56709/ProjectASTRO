# Hazard and ethical risk register

Revision R0.1 | 2026-10-23 | Owner Faisal Farouq

## Task control

**Artifact:** ASTRO-A-09

**Objective:** Identify credible harm, risk controls and evidence required before release.

**Required inputs:** Requirements, architecture, test configuration, qualified risk review and operator procedures.

**Known values and provisional assumptions:** 20 hazard/ethical records; consequence severity 1-4; probability and residual risk unknown.

**Unknowns:** Exposure, actual failure rates, required safety integrity, validated human contact limits and residual acceptance.

**Calculations:** No risk-priority multiplication is used: unknown probability cannot support a numeric residual-risk reduction or a safe claim.

**Output file:** risk_records/09_hazard_and_ethical_risk_register.md

**Implementation steps:** 1. Review hazards by configuration. 2. Add site-specific hazards. 3. Assign named qualified reviewers. 4. Verify controls by linked tests. 5. Record residual risk and release disposition.

**Acceptance test:** Each record has harm, priority, controls, requirement/test links, accountable owner and a reviewer role; residual acceptance stays pending until evidence.

**Stop conditions:** Any P0 release control absent, unknown stop response, unqualified arrest design, real patient data or unsupported clinical claim.

**Result:** REWORK - preliminary register; residual risks not assessed or accepted

**Next dependency:** G2 qualified hazard review and site survey

**Physical authorization and supervision:** All physical activity needs a test permit and qualified supervision; this register is not that permit.

**Budget effect:** Safety controls remain inside the financial model; cost inadequacy blocks release.

**Revision:** R0.1

**Date:** 2026-10-23

**Accountable owner:** Faisal Farouq

## Specification

Severity uses 1 negligible harm, 2 minor reversible injury or inconvenience, 3 serious injury or substantial privacy harm, and 4 fatal/permanent injury or potentially severe care-related misuse. These are conservative consequence categories for screening, not a quantified clinical risk analysis. Likelihood is UNASSESSED for every record. P0 means the relevant release is blocked until the control is verified and reviewed; P1 means resolve before the relevant demonstration stage. Neither category estimates probability.

The complete register is risk_records/hazards.csv and the Hazards workbook tab. Faisal Farouq is accountable for disposition and appointments, not presumed qualified to sign every specialized design. Reviewer fields contain roles marked unassigned; they do not invent professional sign-off. Residual risk remains UNASSESSED and acceptance NOT RECORDED throughout R0.1.

Stop design needs explicit gravity behavior. Removing motor power can cause collapse. The physical safety case must show how the arrest/support retains the robot and object without battery, compute, network or a held torque command. A safety relay, contactor or independent microcontroller alone does not establish the integrity of the whole function. The safety reviewer must define and validate response time, fault detection, reset behavior, limits and retained-load behavior.

ISO 13482 and ISO 13850 official abstracts are design-review references (SRC-03/04). No paid full-standard assessment, compliance claim, certification or regulatory determination is made. Recheck applicable editions and jurisdiction at the architecture gate. Friendly styling increases the need for clear boundaries because spectators may approach or touch the robot. Year 1 physical demonstrations use barriers and scripted adult operators; they are not patient trials. No contact-force number has been borrowed from a different robot standard to imply that this full-size biped is safe for contact.
