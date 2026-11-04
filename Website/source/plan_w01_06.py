from plan_model import W, d, O

R = "JacobsBaymax/"

# ---------------------------------------------------------------- Week 1
W(1)
d(1, "Define the year one outcome",
  goal="Agree one mission text and settle the five charter differences, so every later file builds on the same scope.",
  inp=[O(1) + " (R0.2 draft, REWORK)",
       "ProjectBayMax/phase_01/week1/day_1/project-charter.md, day_2/project-chart.md, day_3/project_charter.md (older charters)",
       R + "requirements/requirements.csv rows JB-R-001 to 009 and 057 to 064"],
  st=[(25, "Read M01–M06 and DEM-01 to DEM-06 in section 2. Mark each line KEEP or write the exact replacement words."),
      (35, "Open section 9. For each of the five differences (real vs fictional data, ±10 mm height tolerance, USD 6,350/5,000 lower case, 0.5–1.0 m lift, 60 s message timing) write one line: adopt R0.2 wording, adopt charter wording, or new wording."),
      (30, "Recommended default: adopt R0.2 wording for all five. Real data and a 60 s message promise conflict with JB-R-061 and JB-R-060; a 0.5–1.0 m lift has no reviewed load case."),
      (20, "Add a dated 'Owner decision 2026-__-__' block to section 9 with your five choices. Do not edit the older charters; they stay as history."),
      (10, "Enter your real minutes for Day 1 in the website outcome form. Record PASS only when all five rows have a decision.")],
  calc="Trials: 2 × 3 steps = 6 planned steps in two separate trials. Height 1,829 mm = 1.829 m. JB-R-002 band 1.809–1.849 m (±20 mm) vs charter ±10 mm: pick one.",
  chk=["All 12 mission and demonstration lines are marked KEEP or have replacement text.",
       "Section 9 has a dated decision for each of the five differences.",
       "No sentence promises real patient data, diagnosis, emergency response or person support."],
  note="Project files record Day 1 as REWORK: owner acceptance and charter reconciliation are still open.")

d(2, "Create the working folders",
  goal="Make every working file findable in under a minute and keep R0.1 originals untouched.",
  inp=[R + "release_archive/R0_1/ (original package)", O(1)],
  st=[(20, "List the 14 working folders under JacobsBaymax/ and confirm each exists: requirements, architecture, cad_specifications, simulation, software, tests, evidence, budget, procurement, risk_records, caregiver_workflows, simulated_patient_data, revision_history, release_archive."),
      (25, "Run `shasum -a 256` on the five R0.1 files in release_archive/R0_1 and compare with MANIFEST_SHA256.txt. Write any mismatch in the index."),
      (25, "Write a one-line purpose and the main file for each folder in the index."),
      (20, "Timed test: from the folder root, open the mission PDF, requirements.csv, hazards.csv, verification_matrix.csv and the workbook. Record seconds for each.")],
  calc="5 file opens; target under 60 s each. Hash check: 5 files, 0 mismatches expected.",
  chk=["All 14 folders listed with purpose and main file.",
       "R0.1 hashes match the manifest, or each mismatch is recorded.",
       "All five core files opened from the index in under 60 s each."],
  note="Project files record Day 2 as PASS for folder setup only.")

d(3, "Write the measurable success checklist",
  goal="Turn each year-one target into a row with a unit, a measurement method and the evidence that would prove it.",
  inp=[O(1), R + "requirements/requirements.csv", R + "tests/verification_matrix.csv"],
  st=[(30, "Make columns: requirement ID, target, unit, measurement method, instrument, evidence file, current status."),
      (40, "Add rows for height (m), robot mass per configuration (kg), joint count (count), step count per trial (count), trial count (count), speed (m/s over first toe-off to third stable landing), payload (kg), repetitions (count)."),
      (30, "For speed write the formula: v = pelvis displacement (m) / time (s) between the two events, measured from synchronized video and logs."),
      (20, "Set every status to TARGET – NOT MEASURED.")],
  calc="Speed check: 0.45 m in 3.0 s = 0.15 m/s; 0.45 m in 4.5 s = 0.10 m/s.",
  chk=["Every row has a unit or count and a named instrument or method.",
       "Two separate trials of three alternating steps are separate rows from the speed row.",
       "No row shows a measured value."],
  note="Project files record Day 3 as PASS for checklist coverage only.")

d(4, "Assign people without inventing qualifications",
  goal="Know exactly which outside help the project needs, when, and what proof of competence to ask for.",
  inp=[O(3), R + "revision_history/gates.csv"],
  st=[(25, "List seven roles: owner, test director, mechanical reviewer, electrical reviewer, controls/safety reviewer, rigging provider, fabricator. Add an eighth: stop operator (a second competent adult for every powered test)."),
      (35, "For each role write the first day it is needed (e.g. mechanical reviewer Day 112, stop operator Day 218, rigging Day 135) and the evidence to collect: CV or licence number, written scope, availability dates, fee."),
      (25, "Mark every role except owner UNASSIGNED unless you have a written yes from a real person."),
      (15, "Write where you could ask for each role (school robotics lab, makerspace, local engineering firm, online quote). Mark these as 'to ask', not 'available'.")],
  calc="8 roles; 1 assigned (owner); 7 unassigned. First outside need: Day 112.",
  chk=["Each role has a first-needed day and a list of evidence to collect.",
       "No person, licence, facility or free service is shown as confirmed without written proof.",
       "Faisal Farouq remains the accountable owner."],
  help="Nobody yet. This list is what you will ask for later.",
  note="Project files record Day 4 as PASS for list completeness only (six specialist roles unassigned).")

d(5, "Expose the budget gap",
  goal="Show exactly how much money each actuator can cost under the cap and under the USD 15,000 scenario.",
  inp=[R + "budget/financial_budget.csv", R + "budget/Jacobs_Baymax_Control_Workbook_R0_1.xlsx (Budget tab)"],
  st=[(30, "Add the 13 non-actuator lines B-02 to B-14 and confirm USD 7,000."),
      (30, "Compute the actuator pool and per-assembly allowance for USD 10,000 and USD 15,000."),
      (30, "Write three D-01 routes: documented reuse or sponsorship, redesign within the cap, extend the schedule. For each, list the proof needed before it counts."),
      (20, "Label every price UNQUOTED and record that the ceiling is undecided.")],
  calc="(10,000 − 7,000) / 10 = USD 300 per assembly. (15,000 − 7,000) / 10 = USD 800. R0.1 reference 7,000 + 10 × 889.90 = 15,899.",
  chk=["The 13 lines sum to USD 7,000.",
       "Both per-assembly allowances and the 15,899 reference are shown with working.",
       "USD 15,000 is labelled a scenario, not a new cap."],
  note="Project files record Day 5 as PASS for arithmetic and options only. Day 6 R0.3 updates the actuator line to USD 2,841–3,481 from dated listings.")

d(6, "Choose the provisional research configuration",
  goal="Decide which leg, head, arm and handling layout to model, backed by load, gait, cost and mass numbers rather than preference.",
  inp=[R + "cad_specifications/parameters.json and candidate_joints.csv (R0.1)",
       R + "budget/mass_budget.csv, financial_budget.csv (R0.1)", O(5),
       R + "cad_specifications/reference/baymax-rigid-panel-concept-v1.png (owner photo)",
       R + "release_archive/R0_1/Jacobs_Baymax_Engineering_Baseline_R0_1.pdf pp. 6–8"],
  st=[(20, "Frontal-plane check. Sketch both legs with feet flat and the pelvis shifted sideways by d. Each leg tilts by φ = asin(d / 0.86 m). Note that hip roll = −φ and ankle roll = +φ are both needed to keep the soles flat. Write why Option C (yaw instead of ankle roll) cannot do this."),
      (30, "Run `python3 JacobsBaymax/architecture/day_006_joint_load_screen.py`. Copy the hip-roll, knee, hip-pitch and ankle rows into the Day 6 load table. Mark the R0.1 hip screen (51.5 N m) as an underestimate and say why: it ignores the swing leg."),
      (25, "Estimate leg spacing from the photo: 1.829 m ≈ 663 px, so ≈ 2.8 mm per px. Record 0.30–0.38 m (±20%). Choose hip-roll axis spacing: 0.30 m under wide thigh shells (recommended) or 0.24 m."),
      (25, "Fill the drive table from dated listings: RobStride 04 (40/120 N m, 1.42 kg, USD 255–319), with 2:1 and 3:1 stage concepts, and CubeMars AK80-64 (48/120 N m, USD 1,150.76). Mark which pass rated ≥ static and peak ≥ 1.5 × static at each joint."),
      (20, "Update cost and mass: actuator line 10 × 255–319 + 4 × 50 + 91.25; M-02 14.0 → 17.3 kg; M-09 3.0 → 0.4 kg (handling moves to its own stand). Add the bulky-shell risk of +1.6 kg."),
      (15, "Write the D-04 handling spec: one bought guided linear actuator, ≥100 mm stroke, datasheet holding force ≥ 98 N, separate floor stand, robot secured. Write four Day 7 decisions and the outside-help table.")],
  calc="Hip roll τ = g(m_upper·s/2 + m_leg·s): 0.30 m → 9.81 × (35 × 0.15 + 10 × 0.30) = 80.9 N m; 0.36 m → 97.1 N m. Knee at 0.7 rad: 49.5 × 9.81 × 0.43 × sin 0.35 = 71.6 N m. Actuator line: 2,550 + 200 + 91.25 = 2,841.25 to 3,190 + 200 + 91.25 = 3,481.25 USD. Mass: 47.8 − 14.0 + 17.3 − 3.0 + 0.4 = 48.5 kg; reserve 6.5 kg.",
  chk=["The proposal names exactly 10 leg joints (5 + 5) with both ankle axes and no hip yaw, or records the conflict.",
       "Every number in the Day 6 tables is reproduced by the screen script or shown arithmetic.",
       "Each price is a dated listing marked UNQUOTED; each assumption is marked as such.",
       "Four owner decisions are written for Day 7."],
  extra=[R + "architecture/day_006_joint_load_screen.py", R + "architecture/day_006_joint_load_screen.csv",
         R + "architecture/day_006_actuator_screen.csv", R + "requirements/day_006_D03_D04_configuration.pdf"],
  help="Not today. Day 112 needs a mechanical or robotics engineer to check the loads that grow from this screen.",
  note="Project files record Day 6 as REWORK: the R0.3 proposal awaits your review on Day 7. R0.2 versions are archived.")

d(7, "Review the five owner decisions",
  goal="Make or defer each open decision in writing, so Weeks 2–12 run on a known scope.",
  inp=[O(6), R + "revision_history/decision_log_R0_3.csv", O(1), O(4), O(5)],
  st=[(20, "D-03: accept Option A (10 joints, no yaw) for modelling, or write the change."),
      (20, "Hip spacing and drives: choose (a) 0.30 m axes, 3:1 hip roll, 2:1 knee, or (b) 0.24 m, 2:1 on both."),
      (15, "D-04: accept the bought guided actuator on its own stand, or write the change."),
      (20, "D-01: choose the working cap until quotes arrive (keep USD 10,000, adopt 15,000, or another figure). Write the final-decision day (recommended Day 193)."),
      (15, "D-02 and D-05: write 'open' with the first day each is needed (D-02 Day 112, D-05 Day 57)."),
      (20, "Fill the G0 packet: mission (Day 1), exclusions, budget (Day 5), roles (Day 4), decisions (this file). Record G0 as BLOCKED if Day 1 is still REWORK.")],
  calc="G0 needs Days 1–6 PASS or an accepted restriction. Current file records: Day 1 REWORK, Day 6 REWORK.",
  chk=["Each of D-01 to D-06 shows accept, change or open with a date.",
       "Day 6 result is updated to PASS only if D-03 and D-04 are accepted or changed in writing.",
       "G0 is recorded as released only with this signed packet; otherwise BLOCKED with the missing items."])

# ---------------------------------------------------------------- Week 2
W(2)
d(8, "Audit all requirement IDs",
  goal="Prove the 64 requirements are unique, phased and linked to a test before anyone designs against them.",
  inp=[R + "requirements/requirements.csv", R + "tests/verification_matrix.csv"],
  st=[(30, "Load requirements.csv in a spreadsheet. Count rows (expect 64), unique IDs (expect 64), and phases: Year 1, Later, Excluded."),
      (30, "Check every Verification ID exists in verification_matrix.csv (JB-V-01 to 26). List any missing."),
      (40, "Add columns 'Day 6/7 effect' and 'Wording issue'. Note JB-R-002 band vs Day 1 choice, JB-R-003 mass with off-robot handling stand, JB-R-005 joint count."),
      (20, "Save as a new CSV; leave requirements.csv unchanged.")],
  calc="Expected phase counts from R0.1: Year 1 = 50, Later = 6, Excluded = 8; total 64.",
  chk=["64 rows, 64 unique IDs, phase counts recorded.",
       "Every row maps to an existing JB-V ID or the gap is listed.",
       "Original requirements.csv is unchanged (same SHA-256)."])

d(9, "Describe the robot fall hazards",
  goal="Write the questions a rigging provider must answer before any standing test, without guessing ratings.",
  inp=[R + "risk_records/hazards.csv (JB-H-01, 14, 17, 20)", R + "cad_specifications/parameters.json"],
  st=[(30, "Sketch the robot in side and front view at 1.829 m. Draw the fall circle: radius = height, so 1.83 m around each foot. Mark it as a sketch, not a safe distance."),
      (30, "List the arrest path: robot attachment point → tether → connector → overhead beam or frame → building anchor. For each, write the question: rating, inspection date, who signs it."),
      (30, "Write the site checklist: floor area, ceiling height, beam or frame, power outlets, barrier, spectator line, where the stop operator stands."),
      (20, "Note the difference between an arrest system (catches a fall) and balance control (stops it happening).")],
  calc="Static weight 55 × 9.81 = 539.55 N. This does not size arrest equipment; dynamic arrest loads are larger and need the rigging provider.",
  chk=["The fall envelope is labelled a sketch.",
       "Every arrest component has a rating question and a named role (unassigned is fine).",
       "No anchor capacity or safe distance is presented as approved."])

d(10, "Describe joint and payload hazards",
  goal="Link each motion and payload hazard to a control idea and a test.",
  inp=[R + "risk_records/hazards.csv", O(6), O(9)],
  st=[(35, "List pinch points from the photo: knee pads, ankle gaps, hip, shoulder pins, shell seams. Give each a joint name from the 10-joint list."),
      (30, "For the handling stand: list drop, pinch between tray and chest window, stand tip-over, power loss."),
      (35, "Write one control idea per hazard (guard, gap ≥ finger size to be set by reviewer, holding brake, interlock) and the JB-V test that checks it."),
      (20, "Leave severity and residual risk blank for the reviewer.")],
  calc="2 kg object weight 19.62 N; with ≈0.5 kg tray 24.5 N held by the handling actuator.",
  chk=["Each hazard has a control idea, a JB-V link and a reviewer role.",
       "No gap size, force limit or residual risk is invented.",
       "Person lifting and cargo walking are listed as excluded uses."])

d(11, "Describe care and privacy risks",
  goal="Write one bad and one good response for each care risk, so the software tests have exact targets.",
  inp=[R + "caregiver_workflows/04_caregiver_workflows.md", R + "simulated_patient_data/fictional_fixture.json"],
  st=[(30, "List six risks: medication advice, false ingestion record, wrong unit, missing timestamp, unauthorized recipient, misleading delivery status."),
      (50, "For each, write a bad robot reply and a permitted reply using SIM-001 and Fictional Demo Medication A."),
      (20, "Tag each pair with the requirement (e.g. JB-R-028, 036, 038) and the test day that will check it (Days 38, 57, 62).")],
  calc="6 risks × 2 examples = 12 scripted lines.",
  chk=["12 lines written with fictional data only.",
       "Permitted replies contain no diagnosis, dosing or emergency promise.",
       "Each pair names a requirement and a test day."])

d(12, "Build the assumption register",
  goal="Make every assumption visible with a route to evidence and a deadline.",
  inp=[R + "risk_records/assumptions.csv (A-01 to A-12)", O(6) + " (A6-01 to A6-16)"],
  st=[(30, "Copy A-01 to A-12 and add the 16 Day 6 assumptions (leg mass 10 kg, μ = 0.5, stage masses, listing prices...)."),
      (40, "Add columns: evidence needed, who provides it, decide-by day, status."),
      (30, "Flag as assumptions: facility access, volunteer help, laptop ownership, the 55 kg allocation, shell area 2.5 vs 3.5 m².")],
  calc="12 + 16 = 28 assumptions.",
  chk=["28 rows, each with a decide-by day.",
       "No assumed free resource is marked confirmed.",
       "Day 6 assumptions keep their A6- IDs."])

d(13, "Link hazards to tests",
  goal="Check every hazard and test link in both directions and block releases on open P0 hazards.",
  inp=[R + "risk_records/hazards.csv", R + "tests/verification_matrix.csv", O(10)],
  st=[(40, "For each of 20 hazards, check its requirement and JB-V links exist. Then check each JB-V points back."),
      (30, "Add the Day 10 hazards with new IDs JB-H-21 onward."),
      (30, "Add a column 'blocks gate' and fill it for each P0 hazard (e.g. JB-H-01 blocks G5/G6).")],
  calc="Links checked = hazards × 2 directions.",
  chk=["All linked IDs exist.",
       "Every P0 hazard names the gate it blocks.",
       "Likelihood and residual risk remain UNASSESSED."])

d(14, "Hold the first evidence review",
  goal="Close Week 2 with a clean R0.3 register set and a short change list.",
  inp=[O(8), O(9), O(10), O(11), O(12), O(13)],
  st=[(30, "List every change made this week by file and ID."),
      (30, "Split them: documentation fixes vs owner decisions. Make the owner decisions now or mark them open."),
      (30, "Save working registers with R0.3 headers; keep R0.1 copies untouched."),
      (10, "Export a website backup (Settings → Export progress JSON).")],
  calc="Executed robot tests to date: 0 of 26 JB-V protocols.",
  chk=["Change list names file, ID and reason.",
       "R0.1 originals unchanged.",
       "Backup file saved with today's date."])

# ---------------------------------------------------------------- Week 3
W(3)
d(15, "Choose a simple local software stack",
  goal="Pick tools you can actually run and learn, and fix where each piece of state lives.",
  inp=[R + "caregiver_workflows/04_caregiver_workflows.md", R + "architecture/access_authorization.csv"],
  st=[(20, "Record laptop model, OS version, free disk, Python version (`python3 --version`) and your coding experience in one line each."),
      (30, "Default stack unless you know a better one: Python 3.12, FastAPI, SQLite, plain HTML/JS front end, pytest. All free and local."),
      (40, "Draw seven modules: UI, consent, records, medication, summary, outbox, audit. For each write: what it stores, which table, who may change it."),
      (20, "Write two rules: the conversation part can only propose actions; no module talks to motors.")],
  calc="7 modules; 1 database file; 0 paid services.",
  chk=["Every module has a store and a single writer.",
       "No paid service or cloud account is required.",
       "Motor control is outside this app."])

d(16, "Create and start the empty app",
  goal="Get a page saying SIMULATED DATA running locally from a written README.",
  inp=[O(15)],
  st=[(30, "Create software/care_app/ with frontend/, services/, fixtures/, tests/. Write README with exact commands: `python3 -m venv .venv`, `pip install fastapi uvicorn pytest`, `uvicorn services.main:app --port 8000`."),
      (40, "Serve a page showing 'Jacobs Baymax · Research caregiver support · SIMULATED DATA'."),
      (20, "Close the terminal, open a new one and follow the README exactly. Save the startup log."),
      (10, "Commit to git with message 'Day 16 empty app'.")],
  calc="Pinned versions: record `pip freeze` output in README.",
  chk=["A fresh terminal following the README shows the banner.",
       "`pip freeze` is saved.",
       "No paid service is used."])

d(17, "Define the fictional profile schema",
  goal="Make it impossible to load a profile that is not marked simulated.",
  inp=[O(16), R + "simulated_patient_data/fictional_fixture.json", R + "simulated_patient_data/fictional_fixture_SIM-002.json"],
  st=[(40, "Write a JSON schema: id, simulated (must be true), display_name, interaction_mode (5 values), preferences, mobility text, condition labels (text only, never used for logic), care_team list, consent {preference_memory, notes, capture, transmit} all default false."),
      (30, "Load SIM-001 'Fictional Demo Profile 001' and SIM-002 'Fictional Demo Profile 002' (78, wheelchair, type 2 diabetes label)."),
      (40, "Write 4 pytest cases: SIM-001 and SIM-002 load; simulated=false rejected; missing consent block defaults to all false; a condition label cannot trigger any rule.")],
  calc="4 tests; expected 4 pass.",
  chk=["simulated=false is rejected by the parser.",
       "All four consents default to false.",
       "Fixture contains no real name or identifier."])

d(18, "Define the observation schema",
  goal="Every reading carries value, unit, source and two timestamps, or it is rejected.",
  inp=[O(17), "HL7 FHIR R4 Observation (structure reference only)", R + "caregiver_workflows/05_caregiver_link_and_grounding.md"],
  st=[(40, "Fields: record_id, profile_id, metric, value (typed), unit, source_id, actor_id, observed_at, recorded_at, version, supersedes_id, statement_type (simulated_fact, patient_statement, robot_observation, unknown). Statements also carry verbatim, read_back, confirmed."),
      (30, "Allow value null only with missing_reason. Add metric blood_glucose with unit mg/dL only."),
      (40, "Write 5 tests: valid record; missing unit rejected; missing source rejected; bad timestamp rejected; patient_statement with confirmed=false rejected.")],
  calc="5 tests; 12 fields + 3 statement fields + 1 conditional.",
  chk=["4 tests pass.", "Error messages name the bad field.", "No clinical normal range is stored."])

d(19, "Create the transactional record store",
  goal="Records are written only through service functions and never silently overwritten.",
  inp=[O(17), O(18)],
  st=[(40, "Create SQLite tables profiles and observations. Write create_observation() and get_observation() in services/records.py."),
      (30, "Use a unique record_id and reject a duplicate with an error."),
      (30, "Test: create 3 records, restart the app, read them back; create a duplicate ID and confirm rejection.")],
  calc="3 records written, 3 read after restart, 1 duplicate rejected.",
  chk=["Records survive restart unchanged.", "Duplicate ID cannot overwrite.", "UI code has no direct SQL."])

d(20, "Create the append only audit service",
  goal="Every create, read, change, deny and send leaves an attributable event.",
  inp=[O(19)],
  st=[(40, "Table audit_events: id, time, actor, action, target_id, target_version, result."),
      (30, "Call audit from every service function, including reads."),
      (30, "Test: 1 create + 2 reads = 3 events. Confirm no delete route exists. Note in README that app-level append-only is not tamper-proof.")],
  calc="1 + 2 = 3 events expected.",
  chk=["3 events recorded with actor and target.", "No delete endpoint for audit.", "Limitation written in README."])

d(21, "Rebuild the fixture from scratch",
  goal="Prove the database can be rebuilt from fixtures and that the first tests pass from clean.",
  inp=[O(16), O(17), O(18), O(19), O(20)],
  st=[(20, "Delete only the test database file. Run the fixture loader for SIM-001 and three observations."),
      (40, "Run `pytest -q` and save the output with the git commit hash."),
      (30, "List defects found this week with severity: privacy, data integrity, convenience."),
      (10, "Export a website backup (Settings → Export progress JSON) into JacobsBaymax/evidence/backups/.")],
  calc="Tests so far: 3 + 4 + 2 + 1 = 10 expected.",
  chk=["Database rebuilds from fixtures alone.", "pytest output saved with commit hash.", "Defects listed, none hidden."])

# ---------------------------------------------------------------- Week 4
W(4)
d(22, "Build the fictional profile selector",
  goal="Choose a fictional profile and one of five interaction modes without changing permissions.",
  inp=[O(17), O(21)],
  st=[(40, "Profile screen showing SIM ID and a permanent SIMULATED banner. No field to type a real name."),
      (40, "Mode selector: child, adult, older adult, rehabilitation, limited speech or mobility. Store it on the profile."),
      (30, "Test: switch through all 5 modes; confirm consent values and role are unchanged after each.")],
  calc="5 mode switches × 4 consent fields = 20 assertions.",
  chk=["Banner on every profile screen.", "20 assertions pass.", "No real identifier can be entered."])

d(23, "Build the consent dashboard",
  goal="Four independent consent switches that start off and log who changed them.",
  inp=[O(17), O(20)],
  st=[(40, "Four toggles: preference memory, notes, camera/microphone capture, report sending. Plain-language state next to each."),
      (40, "Store actor, time, scope and version for each change and write an audit event."),
      (30, "Test: turn on notes only; check the other three stay off and one audit event exists.")],
  calc="4 scopes; 1 change → 1 event.",
  chk=["All four start off.", "One toggle never changes another.", "Each change is audited."])

d(24, "Implement consent withdrawal",
  goal="Withdrawing consent stops the behaviour at once and cancels pending sends.",
  inp=[O(23)],
  st=[(40, "Withdraw action per scope. On transmit withdrawal, mark pending report approvals invalid."),
      (30, "Show what happens to fictional stored data before confirming."),
      (40, "Test: prepare a report, withdraw transmit consent, try to send; expect denial and an audit event.")],
  calc="1 prepared report → 0 sent after withdrawal.",
  chk=["Withdrawn send is denied.", "Pending approval invalidated.", "Audit shows withdrawal and denial."])

d(25, "Build the observation entry form",
  goal="Enter a simulated reading with errors caught before saving.",
  inp=[O(18), O(19)],
  st=[(40, "Form: metric, value, unit, source, observed time, actor. SIMULATED badge beside Save."),
      (30, "Preview screen before save. Observed time and recorded time shown separately."),
      (40, "Test: blank unit and malformed time; confirm database row count unchanged and the error names the field.")],
  calc="Row count before = row count after for 2 bad submissions.",
  chk=["Bad input leaves the database unchanged.", "Error names the field.", "Preview shown before save."])

d(26, "Build notes and correction screens",
  goal="Corrections create version 2 and keep version 1 visible.",
  inp=[O(19), O(20)],
  st=[(40, "Separate patient-statement and caregiver notes, both fictional, with preview and confirm."),
      (40, "Correction form: reason required; creates new version with supersedes_id; old version kept."),
      (30, "Test: correct one note; check v1 and v2 both readable side by side, with actor and reason.")],
  calc="1 correction → 2 versions, 1 audit 'change' event.",
  chk=["v1 remains readable.", "Reason and actor stored.", "Audit records the change."])

d(27, "Add basic accessibility controls",
  goal="Every core screen works by keyboard, without sound and with large text.",
  inp=[O(22), O(25), O(26)],
  st=[(40, "Add large text (≥ 20 px), high contrast, captions, speech-rate slider and 44 px touch targets."),
      (30, "Add a communication board: yes, no, repeat, stop, request a human."),
      (40, "Test each core screen with keyboard only and sound off. Record any action you could not complete.")],
  calc="Core screens: profile, consent, observation, notes, board = 5.",
  chk=["All 5 screens usable by keyboard.", "No information only in sound or colour.", "Failures listed."])

d(28, "Review consent and interface behavior",
  goal="Run the week's scenarios end to end and fix the consent policy text.",
  inp=[O(22), O(23), O(24), O(25), O(26), O(27)],
  st=[(40, "Run create, decline, withdraw and correct scenarios yourself in role. Record who took part (only you, unless someone else really did)."),
      (30, "Search logs and database for anything that looks like real personal data."),
      (30, "Save defects and a revised consent policy paragraph."),
      (10, "Export a website backup (Settings → Export progress JSON) into JacobsBaymax/evidence/backups/.")],
  calc="4 scenarios; expected 0 real-data hits.",
  chk=["JB-V-11 and 12 cases reproducible from the steps.", "No participant or study is invented.", "Defects recorded."])

# ---------------------------------------------------------------- Week 5
W(5)
d(29, "Add the simulated vitals and glucose readings",
  goal="Heart rate, oxygen saturation, temperature and blood glucose as clearly simulated values with units.",
  inp=[O(18), O(25), R + "simulated_patient_data/fictional_fixture_SIM-002.json"],
  st=[(40, "Add metrics heart_rate (1/min), spo2 (%), temperature (°C), blood_glucose (mg/dL) with allowed fixture values only."),
      (30, "Display value, unit, observed time, recorded time, source, actor and SIMULATED. No interpretation text."),
      (20, "Load SIM2-OBS-004 (21:00, value null): the screen must say 'no reading' with the reason."),
      (40, "Test export to JSON and re-import; compare all fields.")],
  calc="4 metrics × 7 displayed fields = 28 checks + 1 missing-reading check.",
  chk=["Round trip keeps units, times and simulated flag.", "No 'normal', 'low' or 'high' wording.", "Missing glucose shows 'no reading', never a number.", "29 checks pass."])

d(30, "Add activity and rest logs",
  goal="Zero and missing are never confused.",
  inp=[O(29)],
  st=[(40, "Steps as integer count; activity and rest as durations in minutes with source and entry type."),
      (30, "Add one fixture with 0 steps and one with steps missing (reason 'not recorded')."),
      (40, "Test the display shows '0' and 'unknown – not recorded' respectively.")],
  calc="2 fixtures; 2 distinct displays.",
  chk=["Zero shows as 0.", "Missing shows as unknown with reason.", "Duration unit shown."])

d(31, "Add patient reported check ins",
  goal="Record words exactly and treat a decline as a decline.",
  inp=[O(18), O(26)],
  st=[(40, "Five check-ins: pain, mood, fatigue, appetite, sleep. Store question version, response text, time."),
      (30, "Read-back before saving: 'You said: <words>. Is that right?' Yes saves; no asks once more; still no or silence saves nothing and says 'I didn't save that.'"),
      (20, "Add a 'prefer not to say' option stored as declined."),
      (40, "Test with SIM2-STM-003 and STM-004: confirmed saves verbatim; rejected read-back saves nothing; declined pain is not shown as 'no pain'.")],
  calc="5 check-ins; 2 read-back cases; 1 decline case.",
  chk=["Actor's words stored verbatim only after confirmation.", "Decline stored separately.", "No score, symptom label or diagnosis derived."])

d(32, "Draw descriptive trend graphs",
  goal="Plot values truthfully: separate units, visible gaps, sorted by observed time.",
  inp=[O(29), O(30)],
  st=[(40, "One graph per unit. Each point links to its record ID."),
      (30, "Add a 6-hour missing interval and an out-of-order fixture."),
      (40, "Check the gap is drawn as a gap and points sort by observed_at.")],
  calc="Fixtures: ≥ 8 points per metric including 1 gap and 1 out-of-order.",
  chk=["Every point traces to a record.", "Gap stays visible.", "Units never mixed on one axis."])

d(33, "Add correction aware trends",
  goal="Graphs use the latest version but the original stays recoverable.",
  inp=[O(26), O(32)],
  st=[(40, "Correct one fictional reading through the correction flow."),
      (30, "Graph uses v2; marker shows 'corrected'; history shows v1."),
      (40, "Compare graph value and report value for that point.")],
  calc="1 corrected point; graph = report = v2.",
  chk=["Graph and report agree.", "v1 recoverable.", "Observed time unchanged."])

d(34, "Add the artificial review rule",
  goal="A non-clinical demo rule that triggers exactly above 10 and never sounds medical.",
  inp=[O(32), R + "caregiver_workflows/04_caregiver_workflows.md"],
  st=[(40, "Add metric synthetic_review_counter (count). Rule: value > 10 shows the prompt."),
      (30, "Prompt text: 'This simulated reading crossed the demonstration review rule. I cannot determine what it means. Would you like to contact your approved caregiver?'"),
      (30, "Add care-team notify values from SIM-002 (glucose below 70 / above 250 mg/dL, labelled fictional and 'set by your care team'). Prompt: 'Your <time> reading was <value> mg/dL. Your care team asked to be told about readings below 70. Shall I send it to them now?'"),
      (40, "Test counter 10 and 11; glucose 70 and 69, 250 and 251; SIM2-OBS-003 (64).")],
  calc="Counter 10 → none, 11 → prompt; glucose 70 → none, 69 → prompt, 250 → none, 251 → prompt.",
  chk=["Every boundary behaves exactly.", "Prompt shows value, unit, time and that the care team set the value.", "No diagnosis, 'low sugar' or emergency wording."])

d(35, "Review observation integrity",
  goal="Run every observation fixture and match screen, graph and export to source.",
  inp=[O(29), O(30), O(31), O(32), O(33), O(34)],
  st=[(50, "Run the full fixture set including missing sources, stale times, corrections and declines."),
      (40, "Compare displayed values, graphs and exported JSON with record IDs."),
      (20, "Mark JB-V-15 cases executed / not executed."),
      (10, "Export a website backup (Settings → Export progress JSON) into JacobsBaymax/evidence/backups/.")],
  calc="Coverage = executed cases with evidence / planned cases.",
  chk=["Every difference is a logged defect.", "Coverage figure stated.", "No medical-accuracy claim."])

# ---------------------------------------------------------------- Week 6
W(6)
d(36, "Store original fictional instructions",
  goal="Medication instructions are stored and shown character for character.",
  inp=[R + "simulated_patient_data/fictional_fixture.json (Demo Medication A)", O(19)],
  st=[(40, "Table medications: original_instruction, schedule_label, source, actor, simulated, instruction_version."),
      (30, "Load the exact demo string from the fixture."),
      (40, "Test: SHA-256 of stored string = SHA-256 of displayed string.")],
  calc="1 instruction; hash equality check.",
  chk=["Hashes match.", "No code path rewrites the text.", "Simulated flag shown."])

d(37, "Display the simulated schedule",
  goal="Reminders run on a test clock and never change the schedule.",
  inp=[O(36)],
  st=[(40, "Add a controllable test clock (env var or settings) and a schedule view."),
      (30, "Event states: scheduled, responded, no response; show instruction version."),
      (40, "Advance clock 2 h; confirm reminder state changes and the schedule record is unchanged.")],
  calc="Schedule hash before = after clock change.",
  chk=["Test clock drives state.", "Schedule unchanged.", "Version shown."])

d(38, "Log the four allowed responses",
  goal="Taken, skipped, postponed, no response, recorded as statements.",
  inp=[O(37)],
  st=[(40, "Buttons for 4 responses; store actor, time, event ID, type."),
      (30, "Display 'reported taken', never 'administered'."),
      (40, "Test all four and one correction.")],
  calc="4 responses + 1 correction = 5 records.",
  chk=["All four round-trip.", "Wording says reported.", "Correction keeps original."])

d(39, "Implement human confirmed record changes",
  goal="Only a caregiver role can change instructions, after preview.",
  inp=[O(36), O(20)],
  st=[(40, "Edit flow: caregiver role, preview old vs new, confirm."),
      (30, "Keep old version; invalidate stale confirmations."),
      (40, "Test: patient role and a model proposal both denied and audited.")],
  calc="2 denied attempts, 1 allowed change.",
  chk=["Denials audited.", "Old version kept.", "Stale confirmation rejected."])

d(40, "Create the missed dose draft",
  goal="A skipped dose creates a draft that never sends itself.",
  inp=[O(38)],
  st=[(40, "On skipped: create draft with event ID, instruction version, response, time."),
      (30, "Show full preview; no recipient = cannot send."),
      (40, "Watch the outbox table: 0 rows sent.")],
  calc="1 skip → 1 draft → 0 sends.",
  chk=["Draft created.", "Nothing transmitted.", "Preview complete."])

d(41, "Test prohibited medication requests",
  goal="Prove the app refuses dosing, catch-up and selection requests in every tested phrasing.",
  inp=[O(11), O(38)],
  st=[(40, "Write 15 prompts: double dose, catch-up timing, choose a medicine, calculate a dose, dispense — 3 phrasings each."),
      (50, "Run each; save exact input and output."),
      (30, "Mark each PASS/FAIL; FAIL means REWORK before any demo.")],
  calc="5 topics × 3 phrasings = 15 cases.",
  chk=["15 cases saved verbatim.", "Every FAIL is listed.", "No dosing advice in any PASS."])

d(42, "Review the full medication flow",
  goal="Run the whole medication story once and link it to JB-V-18/19.",
  inp=[O(36), O(37), O(38), O(39), O(40), O(41)],
  st=[(50, "One session: reminder, response, correction, missed-dose draft, declined send, unauthorized edit."),
      (40, "Export transcript and audit events; link to JB-V-18 and 19."),
      (20, "List anything not implemented."),
      (10, "Export a website backup (Settings → Export progress JSON) into JacobsBaymax/evidence/backups/.")],
  calc="6 scenario steps; audit events counted.",
  chk=["Instructions unchanged end to end.", "Human confirmation required for changes.", "Gaps listed."])
