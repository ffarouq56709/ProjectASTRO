from plan_model import W, d, O

R = "ProjectASTRO/"
PHOTO = R + "cad_specifications/reference/astro-rigid-panel-concept-v1.png"

# ---------------------------------------------------------------- Week 13
W(13)
d(85, "Choose and configure the CAD tool",
  goal="A CAD setup that keeps units right and exports STEP.",
  inp=[R + "cad_specifications/parameters.json"],
  st=[(30, "Choose FreeCAD 1.x (free, local) or Onshape (free plan makes documents public). Record name and version."),
      (30, "Set units to mm; note 1 m = 1,000 mm conversion at the top of the master file."),
      (40, "Create planes with x forward, y left, z up. Model a 100 mm cube, export STEP, reopen, measure.")],
  calc="Cube edge after round trip must read 100.00 mm.",
  chk=["Tool and version recorded.", "Cube reopens at 100 mm.", "Frame note in the master file."])

d(86, "Draw the height envelope",
  goal="A dimension chain that adds up to 1.829 m with the chosen hip spacing.",
  inp=[R + "cad_specifications/parameters.json", O(6), O(7), PHOTO],
  st=[(30, "Set levels: floor 0, sole top, ankle axis, knee axis (+430 mm), hip axis (+430 mm), pelvis top, shoulder, head top 1,829 mm."),
      (40, "From the photo (≈2.8 mm/px) estimate torso and head heights; write each as 'photo estimate ±20%'."),
      (30, "Place hip-roll axes at the Day 7 choice (0.30 m or 0.24 m apart).")],
  calc="Example chain: ankle 90 + shank 430 + thigh 430 + pelvis-to-shoulder 600 + shoulder-to-head-top 279 = 1,829 mm.",
  chk=["Chain sums to 1,829 mm.", "Every value labelled provisional or photo estimate.", "Hip spacing matches Day 7."])

d(87, "Draw the front body envelope",
  goal="The photo's front silhouette on the master skeleton.",
  inp=[O(86), PHOTO],
  st=[(40, "Trace the photo's front outline over the skeleton: egg head, wide shoulders, rounded torso, wide thighs."),
      (30, "Add pinned-arm detail: shoulder pin hole and removable pin; hands sculpted and fixed."),
      (30, "Mark charcoal gap zones at neck, shoulders, hips, knees, ankles.")],
  calc="Shoulder width from photo ≈ 0.8–1.0 m (perspective); confirm in CAD.",
  chk=["Envelope referenced to skeleton.", "Arm pin and fixed hands shown.", "Panels marked non-structural."])

d(88, "Draw the side body envelope",
  goal="Place heavy parts and access doors in side view.",
  inp=[O(86), O(87)],
  st=[(40, "Place battery, computer and chest camera window. Keep the handling tray clear of the chest window."),
      (30, "Mark vents at thighs and hips (as in the photo) and service doors."),
      (30, "Mark e-stop button reach and tether attachment zone on the upper back.")],
  calc="Note battery height (R0.1 assumed 0.85 m) and computer height (1.35 m).",
  chk=["Cooling, camera view and e-stop access conflicts listed.", "Tether point marked unrated.", "Tray clears chest window."])

d(89, "Set the broad foot envelopes",
  goal="Feet that match the photo and the 0.32 × 0.22 m baseline.",
  inp=[O(86), PHOTO],
  st=[(40, "Model each foot 320 × 220 mm with rounded corners and a dark replaceable sole 15 mm thick."),
      (30, "Set foot centre spacing to match hip spacing (0.30 or 0.24 m) or record the difference."),
      (30, "Mark 4 load-sensor zones per foot (heel left/right, toe left/right).")],
  calc="Sole area 0.32 × 0.22 = 0.0704 m².",
  chk=["Left and right identical.", "Spacing recorded.", "No stability margin claimed."])

d(90, "Map panel removal and access",
  goal="A panel schedule with area and mass for each part of the shell.",
  inp=[O(87), O(88)],
  st=[(40, "Split shell into named panels (head, chest, back, belly, shoulders, upper/lower arms, thighs, shins, feet covers)."),
      (40, "For each: area from CAD, material candidate (ABS/PETG), thickness 1.5 mm, mass = area × 0.0015 × 1,050."),
      (30, "Write fastener direction and removal order.")],
  calc="Total area A (m²) × 1.575 kg/m² + 1.26 kg mounts. Compare with 5.2 kg allocated.",
  chk=["Every panel has area and mass.", "Total vs 5.2 kg stated.", "Removal does not block e-stop or vents."])

d(91, "Review the geometry conflicts",
  goal="One list of conflicts to fix before structural work.",
  inp=[O(86), O(87), O(88), O(89), O(90)],
  st=[(40, "Compare envelopes with mass allocation, joint ranges, feet, access and the photo."),
      (40, "Save annotated views; list each conflict with owner decision."),
      (20, "Update the shell-mass risk with the real CAD area."),
      (10, "Export a website backup (Settings → Export progress JSON) into ProjectASTRO/evidence/backups/.")],
  calc="Shell mass from CAD vs 5.2 kg; difference added to the risk line.",
  chk=["Conflict list has decisions or owners.", "Shell risk updated.", "Nothing labelled fabrication-ready."])

# ---------------------------------------------------------------- Week 14
W(14)
d(92, "Create the joint name register",
  goal="One master table for the 10 joints used by CAD, simulation and code.",
  inp=[R + "cad_specifications/candidate_joints.csv", O(7)],
  st=[(40, "List l_/r_ hip_roll, hip_pitch, knee_pitch, ankle_pitch, ankle_roll."),
      (40, "Add parent, child, axis, zero pose, CAD range, drive class, stage ratio (3:1 hip roll, 2:1 knee, 1:1 others per Day 7)."),
      (30, "Mark operating limits NOT SET.")],
  calc="10 joints; 4 with external stages.",
  chk=["Exactly 10 unique names.", "Frame convention x fwd, y left, z up.", "Limits NOT SET."])

d(93, "Model the two hip axes",
  goal="Hip roll and pitch axes placed with explicit offsets.",
  inp=[O(86), O(92)],
  st=[(40, "Place hip roll axes at ±0.15 m (or ±0.12 m) and hip pitch below them; record offsets in mm."),
      (40, "Fit a box for the 3:1 hip-roll stage and drive; check it fits inside the wide thigh shell."),
      (30, "Rotate through CAD ranges; note torso and cable conflicts.")],
  calc="Hip-roll stage envelope ≈ module Ø + belt length; record mm.",
  chk=["Offsets numeric.", "Stage fits shell or conflict recorded.", "No implicit frames."])

d(94, "Model knees and link lengths",
  goal="Knee axes and 430 mm links with a 2:1 stage envelope.",
  inp=[O(93)],
  st=[(40, "Add knee axes; thigh 430 mm, shank 430 mm; zero = straight leg."),
      (40, "Fit the 2:1 knee stage envelope; check knee pad clearance from the photo."),
      (30, "Check bent poses 0.3, 0.5, 0.7 rad.")],
  calc="Knee offset from hip-ankle line at 0.7 rad: 430 × sin 0.35 = 147 mm.",
  chk=["Chains reconcile with height.", "Knee stage fits or conflict listed.", "Ranges not treated as stops."])

d(95, "Model both ankle axes",
  goal="Ankle pitch and roll with sole origin and rotation signs explicit.",
  inp=[O(94), O(89)],
  st=[(40, "Add ankle pitch then roll; ankle axis 120 mm from heel, 200 mm from toe."),
      (40, "Sweep foot ±0.35 rad pitch, ±0.2 rad roll with both legs; note collisions."),
      (30, "Write transform order in the register.")],
  calc="Ankle to toe 200 mm, to heel 120 mm (Day 6 assumption A6-05).",
  chk=["Axes and signs explicit.", "Collisions listed.", "Transform order written."])

d(96, "Build the forward kinematics worksheet",
  goal="A script that predicts foot positions and agrees with CAD.",
  inp=[O(92), O(93), O(94), O(95)],
  st=[(50, "Write a small Python script with 4×4 transforms for one leg."),
      (40, "Compute neutral, knee 0.5 rad, ankle-roll 0.1 rad poses."),
      (30, "Compare to CAD measurements; choose tolerance 1 mm.")],
  calc="3 poses × 3 coordinates = 9 comparisons; tolerance 1 mm.",
  chk=["9 comparisons within 1 mm or explained.", "Units on every value.", "Script saved."])

d(97, "Review range and clearance conflicts",
  goal="Find every collision and pinch gap in stepping poses.",
  inp=[O(96), O(10)],
  st=[(40, "Sweep each joint alone, then combined low-step poses."),
      (40, "Record collisions, cable bends, shell pinch gaps at knee pads and ankles."),
      (30, "Assign each a fix and owner.")],
  calc="Conflicts count by joint.",
  chk=["Every conflict has a drawing reference.", "Guards not reduced for looks.", "Owners assigned."])

d(98, "Review the candidate topology",
  goal="Agree the kinematic tree is good enough to simulate.",
  inp=[O(92), O(96), O(97)],
  st=[(40, "Check CAD, register and planned simulation names match exactly."),
      (40, "Decide: accept for modelling, or rework. Turning stays out of year one."),
      (30, "Optionally send the tree and conflicts to a robotics engineer for comments.")],
  calc="Name mismatches: target 0.",
  chk=["Names identical across files.", "Decision recorded.", "Missing review stays REWORK."],
  help="Optional: a controls or robotics engineer for 30 minutes of comments on the joint tree.")

# ---------------------------------------------------------------- Week 15
W(15)
d(99, "Inventory every onboard component",
  goal="Every part on the robot appears once in the mass list.",
  inp=[R + "budget/mass_budget.csv", O(6)],
  st=[(50, "Expand M-01 to M-13 into parts: 10 drives, 4 stages, mounts, battery, BMS, shell panels, pins, sensors."),
      (30, "Record mass, source (datasheet/CAD/assumption) and confidence."),
      (30, "List off-robot items separately: handling stand, actuator, tray, 2 kg object, tether, fixtures.")],
  calc="Start from Day 6: 48.5 kg components.",
  chk=["Each part in exactly one line.", "Unknown masses marked unknown.", "Off-robot list separate."])

d(100, "Calculate structural concept masses",
  goal="Structure mass from CAD volumes with stated densities.",
  inp=[O(94), O(99)],
  st=[(40, "Assign densities: aluminium 6061 2,700 kg/m³, steel 7,850, PETG 1,270 (cite source)."),
      (40, "Export volumes per link; compute mass."),
      (30, "Hand-check one bracket: volume × density.")],
  calc="m = V (m³) × ρ (kg/m³).",
  chk=["Every density cited.", "Hand check within 5%.", "Units consistent."])

d(101, "Calculate exterior panel mass",
  goal="Replace the 2.5 m² guess with CAD area.",
  inp=[O(90)],
  st=[(40, "Sum panel areas from Day 90."),
      (30, "Compute at 1.5 mm and 3.0 mm with ρ = 1,050 kg/m³, plus 1.2625 kg mounts."),
      (30, "Compare with 5.2 kg and the R0.1 reference.")],
  calc="R0.1: 2.5 × 0.0015 × 1,050 = 3.94 + 1.26 = 5.2 kg; at 3 mm 9.14 kg. Photo-based 3.5 m²: 6.77 kg.",
  chk=["Real area used.", "Both thicknesses shown.", "Overrun stated in kg."])

d(102, "Calculate the component center of mass",
  goal="An estimated CoM for neutral and bent-knee poses.",
  inp=[O(99), O(100), O(101)],
  st=[(50, "Assign x, y, z to each part; compute Σ(m·r)/Σm."),
      (40, "Repeat with knees at 0.5 rad."),
      (20, "Exclude the reserve and say why.")],
  calc="CoM height target for gait model ≈ 1.0 m (Day 6 assumption A6-12). Record the computed value.",
  chk=["CoM reproducible from the table.", "Two poses computed.", "Reserve excluded."])

d(103, "Allocate mass growth and configuration IDs",
  goal="Name each configuration and its exact mass list.",
  inp=[O(102)],
  st=[(40, "IDs: Y1-WALK (no handling, no payload), Y1-STAND (supported standing), Y1-HAND (robot secured + stand + 2 kg)."),
      (40, "List mass per configuration; allocate the reserve to the most uncertain items."),
      (20, "State walking config has no payload.")],
  calc="Y1-WALK mass = components − handling stand items.",
  chk=["3 configurations with complete lists.", "Reserve not counted twice.", "Walking has no payload."])

d(104, "Run the mass conflict screens",
  goal="Know how much growth the design can take.",
  inp=[O(103)],
  st=[(40, "Compute 20% and 40% growth on the current components total."),
      (40, "Write what you would cut or change for each case."),
      (20, "Compare with 55 kg and 65 kg.")],
  calc="R0.1: 47.8 × 1.2 = 57.36 kg (+2.36); 47.8 × 1.4 = 66.92 kg (+1.92 over 65). Repeat with the Day 103 total.",
  chk=["Both cases computed.", "Rework options named.", "Overruns not hidden."])

d(105, "Review mass evidence and missing inputs",
  goal="A mass budget everyone can trust for actuator sizing.",
  inp=[O(99), O(100), O(101), O(102), O(103), O(104)],
  st=[(40, "Reconcile CAD, datasheet and allowance values."),
      (30, "List the five biggest unknowns by kg."),
      (30, "Update the workbook copy and assumptions."),
      (10, "Export a website backup (Settings → Export progress JSON) into ProjectASTRO/evidence/backups/.")],
  calc="If projection > 65 kg: stop and hold a major review.",
  chk=["Mass and cost use the same configuration.", "Top 5 unknowns listed.", "No as-built claim."])

# ---------------------------------------------------------------- Week 16
W(16)
d(106, "Define structural and actuator load cases",
  goal="A load-case list so no joint is sized from one pose.",
  inp=[O(6), O(103)],
  st=[(40, "Cases: double support, single support, bent knee 0.5/0.7 rad, weight shift, step landing, stop, power loss, handling (robot secured)."),
      (40, "For each: posture, contacts, masses, load path."),
      (30, "Mark fault cases separately.")],
  calc="≈ 9 cases × 10 joints.",
  chk=["All cases listed.", "Fault cases separate.", "No peak-only sizing."])

d(107, "Calculate the static ankle screens",
  goal="Ankle torque from the ZMP plan and the sole-edge bound.",
  inp=[O(6), O(102)],
  st=[(40, "Planned ZMP 0.06 m sagittal, 0.04 m lateral from ankle."),
      (40, "Compute with the Day 102 mass; compare with the sole-edge bounds."),
      (30, "Keep the 1.5 multiplier separate.")],
  calc="55 × 9.81 × 0.06 = 32.4 N m pitch; × 0.04 = 21.6 N m roll; ×1.5 = 48.6 / 32.4. Bounds 107.9 / 59.4 N m.",
  chk=["Planned and bound values separate.", "Multiplier labelled.", "Uses current mass."])

d(108, "Calculate hip and knee screens",
  goal="Hip-roll and knee torque from the real CAD mass distribution.",
  inp=[O(6), O(102), R + "architecture/day_006_joint_load_screen.py"],
  st=[(40, "Replace A6-02 leg mass and upper-body mass with Day 102 values; rerun the screen."),
      (40, "Record hip roll at the chosen spacing and knee at 0.5/0.7 rad."),
      (30, "Compare with Day 6 numbers and explain differences.")],
  calc="Day 6: hip roll 80.9 N m (0.30 m); knee 51.7 / 71.6 N m.",
  chk=["Script rerun with new inputs.", "Differences explained.", "R0.1 51.5 N m marked superseded."])

d(109, "Define the joint duty trajectory",
  goal="Time histories for stand, shift and three steps.",
  inp=[O(108)],
  st=[(50, "Write angle, speed, acceleration per joint for: stand 10 s, shift 2 s, 3 steps at 1.2 s each, settle 3 s."),
      (40, "Use rad, rad/s, rad/s²; include holding periods."),
      (20, "Note that walking speed ≠ joint speed.")],
  calc="Total cycle ≈ 10 + 2 + 3.6 + 3 = 18.6 s.",
  chk=["Every phase has duration.", "Units explicit.", "Holding periods included."])

d(110, "Calculate the load duty summary",
  goal="Peak and RMS torque per joint over the test cycle.",
  inp=[O(109)],
  st=[(50, "Estimate torque vs time per joint from the quasi-static model."),
      (40, "Compute RMS: sqrt(Σ τ²·dt / Σ dt)."),
      (30, "Compare RMS with rated (40 N m direct, 76 at 2:1, 114 at 3:1) and peak with 120/228/342.")],
  calc="τ_RMS = sqrt(Σ τᵢ² Δtᵢ / Σ Δtᵢ).",
  chk=["10 joints with peak, RMS, duration.", "Thermal unknowns listed.", "Margins shown."])

d(111, "Compare actuator classes without selecting one",
  goal="A dated comparison of real modules against the duty summary.",
  inp=[O(110), R + "architecture/day_006_actuator_screen.csv"],
  st=[(40, "Recheck listings (RobStride 04/03, AK80-64, one MyActuator RMD-X) and record date, price, rated/peak, mass, voltage, interface."),
      (40, "Fill pass/fail per joint for rated vs RMS and peak vs peak."),
      (30, "Write the vendor questions: continuous rating without heat sink, driver inclusion, CAN protocol, lead time.")],
  calc="Set of 10 cost and mass per class.",
  chk=["Every value dated and sourced.", "Peak-only matches marked unqualified.", "Vendor questions written."])

d(112, "Review the sizing conflicts",
  goal="An outside check of the loads before any money moves.",
  inp=[O(106), O(107), O(108), O(110), O(111)],
  st=[(40, "Write a 2-page summary: load cases, duty table, candidate classes, open questions."),
      (40, "Send it to a mechanical or robotics engineer; ask for written comments."),
      (30, "Update D-01 interim: actuator line estimate vs USD 3,000 pool.")],
  calc="Actuator line Day 6: USD 2,841–3,481.",
  chk=["Review request recorded with reply or no-reply.", "D-01 interim updated.", "No purchase."],
  help="A mechanical or robotics engineer (paid if needed, from B-11). Get: name, background, date, written comments on the load cases.")

# ---------------------------------------------------------------- Week 17
W(17)
d(113, "Define the foot load path",
  goal="Show how ankle load reaches the floor through a replaceable sole.",
  inp=[O(89), O(95)],
  st=[(40, "Draw ankle bracket → foot plate → load sensors → sole."),
      (40, "Mark cosmetic cover vs structural plate vs sole."),
      (30, "List bending and fastener questions for review.")],
  calc="Ankle pitch bound 107.9 N m acts on the foot plate.",
  chk=["Three layers distinguished.", "Questions listed.", "Broad flat foot kept."])

d(114, "Calculate contact geometry screens",
  goal="Pressure and margin numbers for the sole.",
  inp=[O(89)],
  st=[(40, "Area 0.0704 m²; mean pressure 539.55 / 0.0704."),
      (40, "Half-width 0.11 m; with 0.025 m edge allowance, 0.085 m."),
      (20, "Label uniform-pressure assumption.")],
  calc="539.55 / 0.0704 = 7,664 Pa.",
  chk=["Numbers shown with working.", "Assumption labelled.", "No stability claim."])

d(115, "Choose contact sensing requirements",
  goal="Specify what the foot sensors must report.",
  inp=[O(114)],
  st=[(40, "Requirements: 4 channels per foot, range ≥ 600 N per channel, rate ≥ 200 Hz, fault on disconnect."),
      (40, "Compare 2–3 load cell types (strain-gauge button cells, FSR) on range, drift, wiring."),
      (30, "Write saturation and disconnect behaviour.")],
  calc="Full weight on one cell worst case 539.55 N → choose ≥ 600 N range.",
  chk=["Zero, expected, saturation and disconnect cases covered.", "Candidates compared.", "No safety-function claim."])

d(116, "Design the sensor calibration method",
  goal="A calibration procedure for the foot sensors.",
  inp=[O(115)],
  st=[(40, "Write zero and known-load steps using calibrated weights (e.g. 5, 10, 20 kg)."),
      (40, "Data columns: reference N, output, time, temperature."),
      (20, "Rejection rule: linear fit error > 2% full scale (to confirm with reviewer).")],
  calc="5, 10, 20 kg → 49.05, 98.1, 196.2 N.",
  chk=["Procedure complete.", "Rejection rule written.", "No loads applied today."])

d(117, "Plan sole friction testing",
  goal="A simple friction test before any walking.",
  inp=[O(89)],
  st=[(40, "Inclined-plane method: put a weighted sole sample on a board, tilt until it slides; μ = tan θ."),
      (40, "Conditions: dry, dusty, worn. Floors: the planned test floor."),
      (20, "Repeat each condition 5 times and report mean and range of μ.")],
  calc="μ = tan θ; θ = 26.6° → μ = 0.5 (Day 6 assumption).",
  chk=["Method and repeats defined.", "Conditions listed.", "Cannot release walking by itself."])

d(118, "Update the contact simulation inputs",
  goal="A contact parameter table ready for MuJoCo.",
  inp=[O(114), O(117)],
  st=[(40, "Enter sole box size, contact points, μ range 0.3–0.7, stiffness/damping placeholders."),
      (40, "Tag each value measured / vendor / assumed."),
      (20, "Add loss-of-contact and saturation cases.")],
  calc="μ sweep 0.3, 0.5, 0.7.",
  chk=["Each value tagged.", "Sweep defined.", "File versioned."])

d(119, "Review foot feasibility",
  goal="Close foot design questions before sourcing.",
  inp=[O(113), O(114), O(115), O(116), O(117), O(118)],
  st=[(40, "Reconcile foot mass, clearance, sensing and floor."),
      (30, "List questions for the reviewer (ankle moments, sole swap, trip risk)."),
      (20, "Change drawings if needed."),
      (10, "Export a website backup (Settings → Export progress JSON) into ProjectASTRO/evidence/backups/.")],
  calc="Foot mass vs M-03 2.5 kg.",
  chk=["Questions listed.", "Drawings updated.", "No stability claim from appearance."])

# ---------------------------------------------------------------- Week 18
W(18)
d(120, "Draw the protected power blocks",
  goal="A block diagram an electrical reviewer can mark up.",
  inp=[O(110)],
  st=[(40, "Blocks: commercial 48 V pack with BMS → main switch → fuse → precharge → contactor (e-stop) → drives; DC-DC for computer/sensors; charger."),
      (40, "Note regen path (a braking resistor/bleeder may be needed)."),
      (30, "List questions: fuse rating, wire gauge, contactor, regen.")],
  calc="10 drives on one 48 V bus.",
  chk=["Every load has protection.", "Isolation shown.", "No build wiring released."])

d(121, "Build the energy worksheet",
  goal="A rough runtime estimate with honest limits.",
  inp=[O(110), O(120)],
  st=[(40, "Average and peak power per block."),
      (40, "Reproduce the R0.1 screen, then redo with Day 110 RMS torques."),
      (20, "Label the result 'idealised screen – not a tested runtime'.")],
  calc="R0.1: P = 10 × 40 × 0.5 / 0.6 + 60 = 393.3 W; 384 Wh × 0.8 / 393.3 W = 0.78 h ≈ 2,812 s.",
  chk=["Both versions shown.", "Holding losses noted.", "Not a tested runtime."])

d(122, "Check voltage compatibility",
  goal="Every part runs across the pack's real voltage range.",
  inp=[O(111), O(120)],
  st=[(40, "Pack: nominal, min, full-charge (e.g. 13s Li-ion: 39–54.6 V)."),
      (40, "Compare with drive range (RobStride 04: 15–60 V) and DC-DC inputs."),
      (20, "Flag regen overshoot risk near 60 V.")],
  calc="13 × 4.2 = 54.6 V full; margin to 60 V = 5.4 V.",
  chk=["All ranges listed.", "Regen risk flagged.", "No pack chosen from nominal voltage alone."])

d(123, "Create the current and regen questions",
  goal="Questions the electrical reviewer must answer, with numbers.",
  inp=[O(121), O(122)],
  st=[(40, "Estimate average and peak bus current."),
      (40, "List worst transients and regen cases."),
      (20, "Write questions for fuse, wire, contactor, bleeder.")],
  calc="I_avg = 393.3 / 48 = 8.2 A (R0.1 example).",
  chk=["Average not used for fuse sizing.", "Questions written.", "Ratings unset."])

d(124, "Build the thermal model structure",
  goal="Know which joints could overheat in a 3-step trial.",
  inp=[O(110), O(111)],
  st=[(40, "List per drive: torque constant, winding resistance, thermal resistance (ask vendor if missing)."),
      (40, "Estimate copper loss I²R for RMS torque at hip roll and knee."),
      (30, "Note cooling: thigh/hip vents from the photo; no 345 mm heat sink inside a leg.")],
  calc="P_loss = I²R; I = τ_motor / k_t.",
  chk=["Missing thermal data marked as procurement blockers.", "Hip roll and knee estimated.", "Vent use noted."])

d(125, "Plan battery charging and service",
  goal="Charging rules from the actual pack's manual, not improvised.",
  inp=[O(120)],
  st=[(40, "Decide: buy a complete commercial pack with BMS and matched charger; do not build packs from cells."),
      (40, "Draft charge, storage, inspection and cool-down steps to be filled from the chosen pack manual."),
      (20, "Add service isolation steps.")],
  calc="Charge rate placeholder = manual value.",
  chk=["No cell-level pack work.", "Every limit cites a manual or is pending.", "Isolation first."])

d(126, "Review power and thermal feasibility",
  goal="Close Week 18 with a reviewed or clearly pending power plan.",
  inp=[O(120), O(121), O(122), O(123), O(124), O(125)],
  st=[(40, "Reconcile pack mass, energy, voltage, duty, cooling, cost."),
      (40, "Send the block diagram and questions to an electrical reviewer."),
      (20, "Update hazards ASTRO-H-04, 17."),
      (10, "Export a website backup (Settings → Export progress JSON) into ProjectASTRO/evidence/backups/.")],
  calc="Pack mass vs M-04 3.5 kg.",
  chk=["Reviewer request recorded.", "Missing data blocks G3.", "Hazards updated."],
  help="An electrical engineer or experienced EV/robotics technician. Get: marked-up block diagram with name and date.")

# ---------------------------------------------------------------- Week 19
W(19)
d(127, "Write safety function requirements",
  goal="List every way motion must stop, independent of the conversation software.",
  inp=[R + "risk_records/hazards.csv", O(120)],
  st=[(40, "Functions: e-stop, enable, watchdog, joint limits, fault latch, restart prevention, payload interlock, support-present interlock."),
      (40, "For each: trigger, independent input, output removed, what happens to gravity loads, test."),
      (30, "Note: ISO 13850 for e-stop function; ISO 13849-1 for the reviewer.")],
  calc="8 functions.",
  chk=["Model/network failure cannot block stopping.", "Each has a test.", "Gravity behaviour stated."])

d(128, "Define motion states and transitions",
  goal="A state machine with no shortcut to motion.",
  inp=[O(127)],
  st=[(40, "States: DISABLED, READY, ENABLED, RUNNING, STOP_LATCHED, FAULT."),
      (40, "Reset → READY only; ENABLED needs a separate enable; missing limits keep DISABLED."),
      (20, "Draw the state diagram and save it as architecture/day_128_safety_state_machine.md with a PNG.")],
  calc="Transitions to RUNNING: only from ENABLED by a human start.",
  chk=["No reset → running path.", "No model → enable path.", "Diagram saved."])

d(129, "Define the independent stop concept",
  goal="Ask a qualified person to pick the stop architecture.",
  inp=[O(127), O(128)],
  st=[(40, "Draft concept: e-stop opens the drive-power contactor through a safety relay; drives also get a stop command."),
      (40, "Write why a hobby relay alone may not meet the needed performance level."),
      (30, "Send to a controls/safety reviewer.")],
  calc="Response time budget: set by reviewer.",
  chk=["Concept sent for review.", "Limitations written.", "Hardware not selected yet."],
  help="A controls or machine-safety engineer familiar with ISO 13849-1. Get: written choice of architecture and required performance level.")

d(130, "Define the power loss retained load case",
  goal="Show what holds the robot and the tray when all power goes.",
  inp=[O(127)],
  st=[(40, "Robot: overhead tether/arrest holds it; drives are not trusted to hold."),
      (40, "Handling: actuator datasheet holding force or brake holds the tray (≥ 98 N screen)."),
      (20, "List any load path that relies on motor torque.")],
  calc="Tray held load 24.5 N; screen 98 N.",
  chk=["No motor-held gravity load in a test.", "Retention named.", "List complete."])

d(131, "Define the signed operating limit set",
  goal="A limits file the software must have before any enable.",
  inp=[O(92), O(128)],
  st=[(40, "JSON schema: per joint position, speed, current, temperature, configuration, reviewer, hash."),
      (40, "Add a check: missing or bad hash → stay DISABLED."),
      (20, "Test in software only.")],
  calc="10 joints × 4 limits = 40 fields.",
  chk=["Missing limits block enable in test.", "Values left empty.", "Schema saved."])

d(132, "Write safety fault injection procedures",
  goal="Test cases for every stop function, on a restrained rig.",
  inp=[O(127), O(131)],
  st=[(40, "Cases: each e-stop, broken wire, stale watchdog, app crash, network loss, reboot."),
      (40, "For each: setup, measurement (e.g. scope on contactor), pass criterion (from reviewer)."),
      (20, "List the measuring equipment each case needs (logger rate, scope, camera) and where it comes from.")],
  calc="≈ 8 cases.",
  chk=["Each case has a criterion or blocker.", "Equipment listed.", "Restrained, unloaded only."])

d(133, "Review safety architecture and authority",
  goal="Record what the safety reviewer decided and who can authorise powered tests.",
  inp=[O(127), O(128), O(129), O(130), O(131), O(132)],
  st=[(40, "Collect reviewer comments; update documents."),
      (40, "Write who signs each future stage permit (named reviewer or pending)."),
      (20, "Keep G2/G3 blockers."),
      (10, "Export a website backup (Settings → Export progress JSON) into ProjectASTRO/evidence/backups/.")],
  calc="Open safety decisions count.",
  chk=["No certification claimed.", "Permit authority recorded or pending.", "Blockers kept."],
  help="Same reviewer as Day 129.")

# ---------------------------------------------------------------- Week 20
W(20)
d(134, "Survey a candidate controlled test area",
  goal="Measure a real space, or write what a space must have.",
  inp=[O(9)],
  st=[(50, "If you have a space: measure floor (target ≥ 4 × 4 m), ceiling height, beam/frame, outlets, door, floor type."),
      (40, "If not: write the requirement list and 3 places you will ask (school lab, makerspace, rented workshop)."),
      (30, "Record answers or 'asked, no reply'.")],
  calc="Fall radius 1.83 m + walkway 0.45 m → area ≥ 4 m long.",
  chk=["Measurements or requirement list saved.", "No access claimed without writing.", "Asks recorded."],
  help="The owner or manager of a candidate space. Get: written permission, hours, cost and rules.")

d(135, "Define the robot arrest load path",
  goal="Get a rigging professional to design the overhead support.",
  inp=[O(9), O(134)],
  st=[(40, "Send mass (55 kg + margin), height, attachment point and site details."),
      (40, "Ask for: anchor, tether, connector, slack, drop distance and dynamic load."),
      (30, "Save the reply, or 'no reply' with the date you asked.")],
  calc="Static 539.55 N; dynamic load from the rigger.",
  chk=["Each component has a rating owner.", "No casual multiplier.", "Reply recorded."],
  help="A qualified rigger or structural engineer. Get: written design or rental spec with load rating and inspection.")

d(136, "Confirm support and exclusion geometry",
  goal="A marked floor plan keeping people out of the fall zone.",
  inp=[O(134), O(135)],
  st=[(40, "Mark fall envelope, tether path, barrier, operator and stop-operator spots."),
      (40, "Keep e-stop reachable from outside the envelope."),
      (20, "Dimensions pending review.")],
  calc="Envelope from rigger; sketch value 1.83 m radius.",
  chk=["People outside envelope.", "Stop reachable.", "Pending review stated."])

d(137, "Check equipment documentation",
  goal="Documents for every support item before it is trusted.",
  inp=[O(135)],
  st=[(40, "Collect specs, ratings, inspection records for candidate support equipment."),
      (40, "Record gaps, quotes, lead times."),
      (20, "Note: a person harness is not a robot arrest system.")],
  calc="Items with documents / total items.",
  chk=["No undocumented item accepted.", "Quotes dated.", "Gaps listed."])

d(138, "Plan fixture and instrument access",
  goal="Know where each measuring tool will come from.",
  inp=[O(116), O(132)],
  st=[(40, "List: calibrated scale (≥ 100 kg), weights, multimeter, current clamp, thermocouple logger, camera ×2, tape, oscilloscope."),
      (40, "For each: own / borrow / rent / buy, cost, calibration status."),
      (20, "Mark unconfirmed items.")],
  calc="Total instrument cost vs B-10 USD 500.",
  chk=["Every measurement has a tool route.", "Costs listed.", "Unconfirmed marked."])

d(139, "Prepare the local response and service plan",
  goal="Who does what when a test stops.",
  inp=[O(136)],
  st=[(40, "Write stop authority, entry rules, how to secure the robot, post-stop inspection."),
      (30, "Battery incident steps from the pack manual and facility rules."),
      (30, "Name real people or leave roles pending.")],
  calc="Roles: owner/operator, stop operator, reviewer.",
  chk=["Roles real or pending.", "Battery steps cite manual.", "No emergency promise."])

d(140, "Review facility readiness and cost",
  goal="Decide D-02 for now: site, support and people.",
  inp=[O(134), O(135), O(136), O(137), O(138), O(139)],
  st=[(40, "Add up access, rigging, instruments, review and freight vs B-09 to B-13."),
      (40, "Record D-02: site confirmed / candidate / none."),
      (20, "Physical tests remain blocked until site and ratings are real."),
      (10, "Export a website backup (Settings → Export progress JSON) into ProjectASTRO/evidence/backups/.")],
  calc="B-09 + B-10 + B-11 + B-13 = 1,000 + 500 + 600 + 650 = USD 2,750 allowance.",
  chk=["D-02 updated with evidence.", "Costs compared.", "No physical release."])
