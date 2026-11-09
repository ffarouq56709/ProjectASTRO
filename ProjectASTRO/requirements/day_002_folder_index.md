# Day 002 - Working folder index

Revision: **R0.2**  
Actual date: **2026-10-25**, America/Los_Angeles  
Accountable project owner: **Faisal Farouq**  
  
Owner participation: user-reported **1.5 hours (90 minutes)**; this is a self-report, not an independently measured duration.  
Result: **PASS - folder setup, source preservation and direct-path checks evidenced**.

## Objective and inputs

Create the 14 working folders, preserve the R0.1 release, seed working registers and make the five required documents reachable by exact navigation paths. This is reversible documentation work; no engineering gate or physical-stage release is required to organize files.

Inputs reviewed: R0.1 mission PDF (1 page), R0.1 engineering baseline (21 pages, front-page revision/status), and the R0.1 workbook Decisions tab, all dated 2026-10-23; the existing R0.2 Day 001 draft and its unresolved items; the R0.2 website Day 002 instructions; the original R0.1 ZIP and its embedded SHA-256 list.

Existing project folder: `ProjectASTRO/`.

## Start here - exact navigation, without search

From `Project ASTRO`, open `ProjectASTRO`, then follow these paths. The links go to the working copies.

| Required item | Exact path from ProjectASTRO | Direct link |
|---|---|---|
| Mission | `requirements/Project_ASTRO_Mission_R0_1.pdf` | [Open mission](Project_ASTRO_Mission_R0_1.pdf) |
| Requirements register | `requirements/requirements.csv` | [Open requirements](requirements.csv) |
| Hazard register | `risk_records/hazards.csv` | [Open hazards](../risk_records/hazards.csv) |
| Verification register | `tests/verification_matrix.csv` | [Open verification](../tests/verification_matrix.csv) |
| Budget workbook | `budget/Project_ASTRO_Control_Workbook_R0_1.xlsx` | [Open workbook](../budget/Project_ASTRO_Control_Workbook_R0_1.xlsx) - Budget and Mass tabs |

Your [current Day 001 mission draft](day_001_mission_acceptance.md) is retained separately. Its owner-review/time state is not changed by Day 2.

## Folder map

| Folder | What belongs here |
|---|---|
| `requirements/` | Mission drafts, requirements.csv, feature_backlog.csv and sources.csv |
| `architecture/` | Architecture, access_authorization.csv and system diagram |
| `cad_specifications/` | Candidate joint table, parameters and CAD guidance; no fabrication release |
| `simulation/` | Simulation guidance; no simulation result claimed |
| `software/` | Software guidance; no implemented robot software claimed |
| `tests/` | verification_matrix.csv and planned demonstration/verification documents |
| `evidence/` | Evidence template, evidence-status note and the actual Day 2 file-check record |
| `budget/` | Budget workbook, financial_budget.csv, mass_budget.csv and budget notes |
| `procurement/` | make_vs_buy.csv and sourcing guidance; no order authorization |
| `risk_records/` | hazards.csv, assumptions.csv and scope/risk notes |
| `caregiver_workflows/` | Fictional caregiver workflow specification |
| `simulated_patient_data/` | Clearly fictional demonstration fixture; no real patient records |
| `revision_history/` | decisions.csv, gates.csv, roadmap and original baseline changelog |
| `release_archive/` | Unpacked R0.1 source release and an unchanged copy of its ZIP |

The pre-existing `reference_baseline/` folder is also retained. The full release now has one explicit preservation location: [release_archive/R0_1](../release_archive/R0_1/START_HERE.md). Existing earlier `phase_01` charters remain at the Project ASTRO root.

## Working copies and preserved originals

- R0.1 extracted files are under `release_archive/R0_1/`; their original directory structure is retained after removing the ZIP's single `Project_ASTRO_R0_1` wrapper directory.
- An unchanged ZIP copy is at `release_archive/Project_ASTRO_Complete_Package_R0_1.zip`.
- Active register seeds and supporting baseline documents were copied into the matching working folders. Their original R0.1 revision/status fields remain unchanged; copying is not a new engineering revision or review.
- Edit working copies in future tasks. Treat `release_archive/R0_1` as the preserved source and verify its original [checksum list](../release_archive/R0_1/MANIFEST_SHA256.txt) after any suspected alteration.
- Historical document-render QA stays inside the archived release. It is not robot test evidence.
- New records include this R0.2 index, the root [START_HERE guide](../START_HERE.md) and [Day 2 file-check evidence](../evidence/day_002_folder_setup.json).

## Actual checks and observations

**Completion-check scope:** explicit path opens, without filename search, Spotlight, recursive discovery or text search during the five-item completion check. Preparation inventories and preservation fingerprints are separate activities.

| Check | Actual observation after installation |
|---|---|
| All 14 named folders exist | PASS - 14/14 directories present at the actual project path. |
| Archived release matches the source package | PASS - all 45 extracted files match the source bytes; original ZIP copy also matches its SHA-256. |
| Original archive manifest matches its covered files | PASS - all 44 listed files match the original SHA-256 list. |
| Working seeds match the corresponding archived files | PASS - 38 working copies match their archived sources. |
| Mission opens directly | PASS - exact path opened; 1-page PDF, R0.1 and named owner identified. |
| Requirements CSV opens directly | PASS - exact path opened; 64 rows and Requirement ID column read. |
| Hazard CSV opens directly | PASS - exact path opened; 20 rows and Hazard ID column read. |
| Verification CSV opens directly | PASS - exact path opened; 26 rows and Verification ID column read. |
| Budget workbook opens directly | PASS - exact path opened; 13 worksheets; Budget, Mass and Decisions accessed; R0.1 header read. |
| Pre-existing Day 1 record, references and local charters preserved | PASS - all 12 pre-existing document fingerprints unchanged. |

Preparation found 64 requirement rows, 20 hazard rows and 26 verification rows. No robot-function result was upgraded. Final observations and file fingerprints are recorded in the evidence JSON from checks against the installed files. All index links also resolved successfully.

## Open decisions, assumptions and limitations

- Day 001 still records pending owner confirmation/time and scope differences with older local charters. These are carried forward; folder creation does not resolve them. They do not prevent reversible file organization.
- D-01 funding/feasibility, D-02 facility/qualified people, D-03 joint topology, D-04 handling arrangement and D-05 fictional workflow/recipient remain open at their existing statuses.
- Confirmed: source files, their revisions, the project path and the user's 1.5-hour self-report. Hardware, equipment access, approvals, measurements and system-test results are not established by this task.
- The worksheet copies were opened for identification and tab access. No spreadsheet formulas, values or engineering status fields were edited or independently validated today.
- Copying the baseline fixture does not authorize real patient data. The active fixture remains fictional.
- The human navigation exercise is available through the five exact paths above. Automated direct-path opening by the assistant is the recorded completion evidence; it does not assert that the user personally opened every file.

## Day outcome and tracker entry

Suggested tracker result: **PASS** for the Day 002 documentation task.  
Actual evidence reference: `ProjectASTRO/requirements/day_002_folder_index.md`, supported by `ProjectASTRO/evidence/day_002_folder_setup.json`.  
Actual user-reported time: **1.5 hours / 90 minutes**. The website's planned 150 minutes is not recorded as elapsed work.  
Actual role: **Faisal Farouq - project owner. File organization and path checks are recorded as documentation work.**  
Qualified reviewer / test permit: **not applicable to this desk task; none issued**.  
Budget effect: **USD 0 new commitments by this work**; earlier project spending remains unconfirmed.  
Physical work: **none**.  
Stop conditions: pause if the task introduces real patient data, clinical authority, unapproved spending or powered motion; do not overwrite divergent existing files or alter preserved release evidence.  
Next dependency: **Day 003 - write the measurable success checklist**, using these working copies and carrying unresolved scope decisions forward.

The result for this day covers file setup and verified navigation only. It does not release a gate, certify safety, authorize an order or prove any robot function.

## Source references and history

- [Archived mission](../release_archive/R0_1/Project_ASTRO_Mission_R0_1.pdf), R0.1, 2026-10-23.
- [Archived engineering baseline](../release_archive/R0_1/Project_ASTRO_Engineering_Baseline_R0_1.pdf), R0.1, 2026-10-23.
- [Archived workbook](../release_archive/R0_1/Project_ASTRO_Control_Workbook_R0_1.xlsx), R0.1; Decisions, Budget and Mass tabs.
- [Active decisions register](../revision_history/decisions.csv), copied without changing its R0.1 fields.
- [Day 001 output](day_001_mission_acceptance.md), R0.2, prepared 2026-10-24; previous evidence preserved.
- Original ZIP SHA-256: `1d1bc2b53f0be81888a858ca373776adbae6911928fbc8779ad3f35c30e80a85`.
- Exact Day 002 website instructions and source-plan fingerprint: retained in `evidence/day_002_folder_setup.json`.
- Time source: user reply "1.5 hrs" during the Day 2 session on 2026-10-25.

