# Day 005 - D-01 budget options

Revision: **R0.2**  
Actual date: **2026-10-27**, America/Los_Angeles  
Accountable project owner: **Faisal Farouq**  
Day result: **PASS - budget arithmetic and options document only**  

## The short version

The original workbook allocates **USD 7,000** to non-actuator items and leaves **USD 3,000** for ten actuator assemblies: **USD 300 per assembly**. The R0.1 reference example totals **USD 15,899**, or **USD 5,899 above the original USD 10,000 limit**.

At a **USD 15,000 planning scenario**, the same USD 7,000 non-actuator allowance leaves **USD 800 per assembly**. The same historical example remains **USD 899 above the scenario**. All these prices and allowances are **UNQUOTED**; none is a current vendor quote or selected, qualified bill of materials.

## What the owner decided today

The user first said the budget was flexible to at least USD 15,000, then explicitly selected: **"Keep $15,000 as a scenario; the final ceiling is undecided."**

Record USD 15,000 as a scenario only. The R0.1 workbook's USD 10,000 limit remains preserved in its original context; **no new ceiling has been approved or entered into the workbook, requirements or website by this task**. Funding availability, funding source and prior project spending are unconfirmed. No purchase is authorized by this discussion.

The dated [D-01 scenario record](../revision_history/day_005_D01_scenario_record.json) preserves this decision separately from the unchanged R0.1 register.

## Opened and checked

The working [control workbook](../budget/Project_ASTRO_Control_Workbook_R0_1.xlsx), Budget tab, identifies **R0.1 / Faisal Farouq / 2026-10-23**. The Decisions tab has the same revision/date and still lists D-01 as blocked pending a funding/feasibility decision. The workbook was read only.

I checked the quantities, unit allowances and cached line totals in Budget rows **6-19**, then independently recomputed all 14 products. The non-actuator sum from rows **7-19** agrees with **Budget!E25 = USD 7,000**. Row 6 contains ten assemblies at USD 300 each. Summary values in E21-E30 agree with the arithmetic below. This is a check of saved values and formulas, not a new live Excel recalculation or a technical qualification review.

| Non-actuator allowance | Item | Amount - UNQUOTED |
|---|---|---:|
| B-02 | Structure and qualified fabrication | USD 650.00 |
| B-03 | Feet and contact sensors | USD 180.00 |
| B-04 | Battery charger and power distribution | USD 650.00 |
| B-05 | Independent safety hardware | USD 450.00 |
| B-06 | Compute perception audio and display | USD 500.00 |
| B-07 | Plastic panels and mounts | USD 550.00 |
| B-08 | Supported handling module | USD 350.00 |
| B-09 | Rated robot fall protection and anchorage access | USD 1,000.00 |
| B-10 | Fixtures tools and inspection equipment access | USD 500.00 |
| B-11 | Qualified independent engineering review | USD 600.00 |
| B-12 | Software communication and content licenses | USD 120.00 |
| B-13 | Freight taxes duties and standards access | USD 650.00 |
| B-14 | Spares and uncommitted contingency | USD 800.00 |
| Total | Non-actuator allowances, including the existing contingency | **USD 7,000.00** |

The USD 800 contingency is already included in USD 7,000. It is not an extra reserve outside this total and should not be removed to hide a known shortfall.

## The arithmetic

| Calculation | Original R0.1 limit | USD 15,000 scenario only |
|---|---:|---:|
| Limit / scenario amount | USD 10,000 | USD 15,000 |
| Non-actuator allowances - UNQUOTED | USD 7,000 | USD 7,000 |
| Available actuator pool | USD 3,000 | USD 8,000 |
| Actuator count | 10 assemblies | 10 assemblies |
| Affordable allowance per assembly | **USD 300** | **USD 800** |
| R0.1 reference project total - UNQUOTED | USD 15,899 | USD 15,899 |
| Reference excess | **USD 5,899** | **USD 899** |

```text
(10000 - 7000) / 10 = 300 USD per assembly
10 x 889.90 = 8899 USD for the historical reference actuator set
7000 + 8899 = 15899 USD historical reference project total
15899 - 10000 = 5899 USD original reference excess

(15000 - 7000) / 10 = 800 USD per assembly in the scenario
15899 - 15000 = 899 USD reference excess over that scenario
```

The USD 889.90 number is a starting-price reference recorded in R0.1 on 2026-10-23, not a current quotation. Driver inclusion, exact configuration, suitability, shipping, taxes, delivery and actual support/review costs need evidence. The calculation does not establish a USD 15,899 minimum cost or a viable complete robot at that price.

## D-01 options - no route selected yet

| Route | What to do before crediting it in the budget | What it changes |
|---|---|---|
| **Documented reuse or sponsorship** | Record exact item/provider, quantity, ownership or written commitment, condition, technical compatibility, inspection needs, availability and the remaining cash costs such as adapters, transport, repair or access fees. Verify the actual saved cash rather than subtracting a catalogue value. | May reduce actual cash costs or add documented funding. No donated equipment or free access is assumed today. |
| **Redesign within the chosen ceiling** | Rework the component/architecture proposal using the actual duty, mass, interface and thermal models. Compare a complete quoted parts-and-services list. Record any proposed outcome change for owner review. | May reduce cost after technical review. Keep safety/support/review costs explicit; changing requirements is a separate recorded decision. |
| **Extend the schedule** | Identify the affected milestones, funding timing, quote validity, provider availability and delivery dates, then explicitly review the year-one completion goal. | Changes timing. It does not itself reduce the example cost, erase either gap or approve a larger ceiling. |

The USD 15,000 scenario is available for comparison across these routes. It has not been selected as an approved limit or as proof that a particular route works.

## Open items and limitations

- Decide the final total cash ceiling and confirm actual available funding/source and earlier commitments. The latest owner statement leaves the ceiling undecided.
- Replace allowances with current, configuration-specific landed quotes. Procurement remains blocked until the actual whole-system cost and technical suitability are reconciled.
- Day 004 identifies six specialist roles as UNASSIGNED. The USD 600 review allowance and access/rigging allowances are not evidence that those services are available or sufficient.
- D-02 facility/people, D-03 topology, D-04 handling and D-05 fictional workflow/recipient remain open. No equipment, simulation, physical test, fabrication release or specialist approval is established today.
- The original accounting assumption excludes paid owner/development labor, major facility construction and clinical/regulatory deployment. If actual project accounting includes those costs, add them before assessing feasibility. Record reused/donated resources and associated cash costs explicitly.
- Source prices are historical and UNQUOTED. This task performed no live price check or vendor contact and made no order or commitment.

## Completion record

Actual observations: all 14 saved line totals agree with independently recomputed quantity x unit allowance; the 13 non-actuator lines sum to USD 7,000; the original unit allowance is USD 300; the R0.1 excess is USD 5,899; the USD 15,000 scenario yields USD 800 per assembly and an illustrative USD 899 gap. All three requested options and the owner's scenario-only decision are documented.

**Result: PASS** for the Day 005 budget-gap document. **D-01 remains OPEN and major procurement remains BLOCKED** pending a final ceiling, funding and complete technically suitable quotes. A documentation PASS does not release a gate, approve spending, certify safety or prove the robot works.

- Actual evidence: this document and [day_005_budget_review.json](../evidence/day_005_budget_review.json).
- Daily log details are retained in the evidence record.
- New spending/commitments from this work: **USD 0**. Prior spending is unknown.
- Stop conditions: no real patient data, clinical authority, unapproved spending or powered motion is introduced by this task; preserve original records and label unquoted inputs.
- Next: **Day 006 - choose the provisional research configuration**, carrying D-01 and the other open decisions forward.

## Sources and preservation

1. [Working control workbook](../budget/Project_ASTRO_Control_Workbook_R0_1.xlsx), R0.1, 2026-10-23: Budget C6:E19, E21:E30 and Decisions tab D-01. Its file fingerprint matches the archived R0.1 workbook.
2. [Financial budget register](../budget/financial_budget.csv) and [financial feasibility note](../budget/07_financial_budget.md), R0.1, 2026-10-23.
3. [Original decision register](../revision_history/decisions.csv), D-01; unchanged source context.
4. [Mission PDF](Project_ASTRO_Mission_R0_1.pdf) and [engineering baseline](../release_archive/R0_1/Project_ASTRO_Engineering_Baseline_R0_1.pdf), R0.1, 2026-10-23.
5. [Day 004 responsibility matrix](day_004_responsibility_matrix.csv) and its [review record](../evidence/day_004_responsibility_review.json), R0.2, 2026-10-27; role appointments remain unassigned.
6. Owner's current budget statements and confirmed scenario-only choice in this chat, 2026-10-27. Exact Day 005 website instructions and source fingerprints are retained in the evidence JSON.

Revision history: R0.2 Day 005 record created 2026-10-27. The workbook, active source registers, earlier daily records and archived releases were preserved. No original funding limit was silently rewritten.
