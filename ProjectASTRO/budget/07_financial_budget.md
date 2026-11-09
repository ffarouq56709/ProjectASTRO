# Financial budget and feasibility

Revision R0.1 | 2026-10-23 | Owner Faisal Farouq

## Task control

**Artifact:** ASTRO-A-07

**Objective:** Preserve the funding cap while exposing unquoted allowances and commercial actuator cost conflict.

**Required inputs:** USD 10000 cap, budget allowances, official manufacturer price reference and later landed quotes.

**Known values and provisional assumptions:** USD 10000 ceiling allocation; USD 7000 non-actuation total; USD 3000 left for ten actuator assemblies.

**Unknowns:** Landed prices, safety equipment rental, tax/duty, review hours, reused equipment ownership and paid labor.

**Calculations:** Affordable actuator allowance=(10000-7000)/10=USD 300. Example reference=10*889.90=8899; total=7000+8899=15899; over cap=5899 or 58.99 percent.

**Output file:** budget/07_financial_budget.md

**Implementation steps:** 1. Confirm accounting scope. 2. Request quotes without purchasing. 3. Replace allowances and reconcile reserve. 4. Seek compliant design/reuse/sponsorship decisions. 5. Release exact BOM only at G3.

**Acceptance test:** All required cash costs including safety, freight/taxes and reserve covered within cap with written quotes; no unsupported free-resource assumptions.

**Stop conditions:** Total forecast >10000 USD, quote/configuration mismatch, omitted safety cost, or donor equipment/access not documented.

**Result:** BLOCKED - major procurement is not financially reconciled

**Next dependency:** D-01 then G3 landed BOM and feasible actuation route

**Physical authorization and supervision:** No procurement, fabrication or load testing authorized.

**Budget effect:** Cap stays USD 10000; reference estimate exceeds it by USD 5899; no increase approved.

**Revision:** R0.1

**Date:** 2026-10-23

**Accountable owner:** Faisal Farouq

## Specification

The ceiling budget deliberately totals USD 10000. The actuator line is an affordability constraint, not evidence that appropriate ten-joint actuation is available for USD 3000. All remaining lines are unquoted allowances. B-09 includes rated robot arrest and anchor access; B-11 includes limited independent review; B-13 includes freight, tax, duties and standards access; B-14 includes spares and contingency. Reducing safety or omitting review to make the total fit is not a viable budget solution.

The manufacturer's page displayed USD 889.90 as a starting price when checked for this baseline (SRC-02). A driver option is present, so the exact with-driver variant, lead time, warranty, compatible bus and landed price must be confirmed in writing. Ten modules at that displayed minimum cost USD 8899, consuming 88.99 percent of the USD 10000 cap and leaving USD 1101 for the remaining USD 7000 allowance. The illustrative total is USD 15899. This is a feasibility reference with optimistic non-actuator allowances, not a selected BOM, purchase recommendation, firm quote or demonstrated minimum project cost. Actuator suitability remains unproven by the torque and thermal screens.

At the USD 5000 lower funding case, the current USD 7000 non-actuator allowance alone exceeds funding by USD 2000. There is no credible full first-year build plan at USD 5000 on current evidence. Software-first demonstration and engineering/quotation work can proceed as no-spend tasks using equipment only after its availability is confirmed. Completion of software alone must be recorded as a partial project outcome.

Accounting assumption A-07 excludes paid owner/development labor, major facility construction and clinical/regulatory deployment. It includes allowances for qualified fabrication, fixture/tool access and independent reviews, whose sufficiency is unknown. If the funding limit must include paid engineering labor or unavailable facilities, add those costs and reopen feasibility. Record donated/reused equipment with condition, replacement value, ownership and associated cash costs; a donation does not waive safety qualification.

Budget revision rule: the owner accepts every baseline change through a decision record showing previous total, new total, difference, cause, phase impact and funding source. No such increase is approved in R0.1. Existing committed spend is recorded as USD 0 in this package because no purchases were made by this work; prior project spending, if any, is unknown and must be supplied before financial release.
