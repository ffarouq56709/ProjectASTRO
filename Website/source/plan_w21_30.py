from plan_model import W, d, O

R = "ProjectASTRO/"
SIMSTOP = "Stop a success claim if it relies on a hidden fixed base, unlimited torque, missing logs or tether pulling."
BACKUP = "Export a website backup (Settings → Export progress JSON) into ProjectASTRO/evidence/backups/."

# ---------------------------------------------------------------- Week 21
W(21)
d(141, "Set up a versioned simulation project",
  goal="A MuJoCo setup anyone can rebuild from the README, with the version pinned.",
  inp=["https://mujoco.readthedocs.io (official docs)", O(15)],
  st=[(30, "Create simulation/ with model/, controllers/, params/, tests/, logs/ and a Python venv. Commit the empty tree."),
      (30, "Run `pip install mujoco`, then `python -c \"import mujoco; print(mujoco.__version__)\"`. Write that exact version into requirements.txt as `mujoco==<version>` and into the README."),
      (40, "Download one official example model (e.g. humanoid.xml from the MuJoCo repo), open it with `python -m mujoco.viewer --mjcf=humanoid.xml`, close the terminal, and repeat from the README alone.")],
  calc="One pinned version string; one example reproduced twice.",
  chk=["The version is pinned in requirements.txt and README.", "A fresh terminal following only the README opens the example.", "The project contains no hardware or motor-bus code."],
  kind="simulation")

d(142, "Build the free base and link tree",
  goal="An MJCF model with a free-floating pelvis and exactly the 10 named leg joints.",
  inp=[O(92), O(96)],
  st=[(50, "Write model/astro.xml: a pelvis body with <freejoint/>, two legs with hinge joints named exactly as in the Day 92 register, axes and offsets from the Day 96 worksheet."),
      (40, "Use capsules and boxes for collision geometry; put the shell in a visual-only group (contype=0 conaffinity=0)."),
      (30, "Write tests/test_tree.py: load the model, assert model.nq == 17 (7 free + 10 hinge) and that the 10 joint names match the register.")],
  calc="nq = 7 + 10 = 17; nv = 6 + 10 = 16.",
  chk=["tests/test_tree.py passes.", "No <weld> or fixed joint ties the pelvis to the world.", "Joint names match the register character for character."],
  kind="simulation", stop=SIMSTOP)

d(143, "Enter estimated masses and inertias",
  goal="The model's mass and centre of mass match the Day 102–103 mass budget.",
  inp=[O(102), O(103)],
  st=[(50, "Enter each link's mass, CoM and inertia. Where CAD inertia is missing, use the box formula and note 'box estimate' in a comment."),
      (40, "Print total mass (`model.body_subtreemass[1]`) and the CoM in the neutral pose; compare with Day 102 for configuration Y1-WALK."),
      (30, "Fix any difference over 0.5 kg or 10 mm, then save params/mass_R0_3.csv with a source per link.")],
  calc="Box inertia: Ixx = m(b² + c²)/12, etc. Acceptance used here: |Δm| ≤ 0.5 kg, |ΔCoM| ≤ 10 mm (analysis choice).",
  chk=["Model mass within 0.5 kg of Y1-WALK.", "CoM within 10 mm of Day 102.", "Every link has a source note."],
  kind="simulation")

d(144, "Add feet ground contact and limits",
  goal="Feet that touch the floor and drives that saturate like the real ones.",
  inp=[O(118), O(110), R + "architecture/day_006_actuator_screen.csv"],
  st=[(40, "Add 0.32 × 0.22 m sole boxes with friction μ = 0.5 (Day 118 middle value)."),
      (50, "Add <motor> actuators with forcerange: ankles and hip pitch ±120 N m, knees ±228 N m (2:1), hip roll ±342 N m (3:1) peak. Put rated values in a comment for thermal checks."),
      (30, "Write tests/test_limits.py: command 1,000 N m at each joint for one step and assert the applied force equals the forcerange limit.")],
  calc="10 joints × 1 clamp test = 10 assertions.",
  chk=["All 10 clamp assertions pass.", "Contact parameters cite Day 118.", "Simulated limits are labelled model values, not approved operating limits."],
  kind="simulation")

d(145, "Add sensor timing and noise",
  goal="Simulated sensors that lag and jitter like the real ones will.",
  inp=[O(115), O(144)],
  st=[(40, "Write controllers/sensors.py producing joint angle (500 Hz, σ = 0.001 rad), IMU (500 Hz, gyro σ = 0.01 rad/s), foot force (200 Hz, σ = 2 N) with a configurable delay."),
      (40, "Run a 5 s standing hold with clean sensors, then with each imperfection switched on alone; save five logs."),
      (20, "Write params/sensors_R0_3.json with every rate, noise and delay and its source or 'assumed'.")],
  calc="5 ms delay = 2.5 samples at 500 Hz. 5 runs.",
  chk=["Each log names its sensor model.", "Clean and imperfect runs both saved.", "All values in a versioned params file."],
  kind="simulation")

d(146, "Add the tether approximation",
  goal="A tether model that shows exactly how much it helps at every moment.",
  inp=[O(135), O(143)],
  st=[(40, "Add a spatial tendon from a ceiling site to an upper-back site with 20 mm slack and a stiffness to confirm with the rigger (start 20 kN/m, assumed)."),
      (40, "Log tendon force every step; run a 5 s stand with and without the tendon."),
      (30, "Plot tether force vs time for both runs and save the plot.")],
  calc="Slack 0.020 m. Tether force should be 0 N while slack.",
  chk=["Tether force is in every log.", "A no-tether run exists for comparison.", "No equality constraint holds the robot up."],
  kind="simulation", stop=SIMSTOP)

d(147, "Validate simple model cases",
  goal="Hand calculations and the model agree before any controller tuning.",
  inp=[O(143), O(108)],
  st=[(40, "Hold the model in a static single-support pose with inverse dynamics (`mj_inverse`) and read joint torques."),
      (40, "Compare hip roll and knee torques with Day 108; write the % difference for each."),
      (30, "Save model hash (`sha256sum model/astro.xml`), timestep, seed and the replay command in logs/baseline_R0_3.md.")],
  calc="Difference % = (model − hand) / hand × 100 for hip roll and knee.",
  chk=["Differences over 15% are explained or logged as REWORK.", "Replay command reproduces the numbers.", "Hashes saved."],
  kind="simulation")

# ---------------------------------------------------------------- Week 22
W(22)
d(148, "Define the standing reference case",
  goal="A single file that fully defines the quiet-standing test.",
  inp=[O(147)],
  st=[(40, "Write tests/cases/stand_ref.json: initial angles (knees 0.3 rad, ankles −0.15 rad, hips −0.15 rad), duration 10 s, timestep 0.002 s, tether slack 20 mm."),
      (40, "List outcome metrics: CoM horizontal drift (m), peak and RMS torque per joint (N m), time in saturation (s), mean tether force (N)."),
      (20, "Add analysis-only pass criteria: drift ≤ 0.02 m, saturation 0 s, tether force 0 N.")],
  calc="10 s / 0.002 s = 5,000 steps.",
  chk=["The case runs from the JSON alone.", "All four metrics defined with units.", "Criteria labelled analysis-only."],
  kind="simulation")

d(149, "Implement a bounded standing controller",
  goal="A joint PD controller with gravity compensation that never exceeds the drive limits.",
  inp=[O(148), O(144)],
  st=[(50, "Write controllers/stand.py: τ = Kp(q* − q) − Kd·q̇ + g(q), with g(q) from mj_inverse at the target pose; clip τ to each actuator's range."),
      (40, "Put Kp and Kd per joint in params/stand_gains.json (start Kp = 300 N m/rad, Kd = 15 N m s/rad)."),
      (30, "Log commanded vs applied torque and count clipped samples per joint.")],
  calc="Clipped samples / total samples per joint.",
  chk=["Gains live only in the params file.", "Clipping is counted and logged.", "No torque above the actuator range is applied."],
  kind="simulation")

d(150, "Run the first standing cases",
  goal="Two logged standing runs with honest outcomes.",
  inp=[O(149)],
  st=[(40, "Run stand_ref and a copy with the pelvis 0.02 m forward at the start."),
      (40, "Save joint states, contact forces, CoM, torques and tether force as CSV with run IDs SIM-STAND-01 and -02."),
      (20, "Write one line per run: stood / fell / saturated, and when.")],
  calc="2 runs × 5,000 steps.",
  chk=["Both runs have IDs and full logs.", "A fall or saturation is written down, not re-run away.", "Each run replays identically."],
  kind="simulation")

d(151, "Inspect static load and saturation",
  goal="Explain every difference between simulated and hand-calculated standing torque.",
  inp=[O(150), O(108)],
  st=[(50, "Tabulate RMS torque per joint from SIM-STAND-01 against the Day 108 static screen."),
      (40, "Flag any joint above its rated torque (40 N m direct, 76 at 2:1, 114 at 3:1) for more than 1 s, and any non-zero tether force."),
      (20, "Write the likely cause for each flag (posture, gains, mass error).")],
  calc="RMS = sqrt(mean(τ²)).",
  chk=["Every joint has a model vs hand value.", "Over-rated joints flagged.", "Tether help disclosed."],
  kind="simulation")

d(152, "Sweep mass and COM assumptions",
  goal="Find which mass assumptions decide whether standing works.",
  inp=[O(150), O(12)],
  st=[(50, "Run stand_ref at total mass 50, 55 and 60 kg (scale the torso) and with the torso CoM moved ±30 mm forward and sideways."),
      (40, "Record outcome, hip-roll RMS and knee RMS for each of the 7 cases in sweeps/stand_mass.csv."),
      (20, "Mark each assumption that moves knee or hip-roll RMS by more than 10%.")],
  calc="3 masses + 4 CoM offsets = 7 cases.",
  chk=["7 cases logged.", "Sensitive assumptions named.", "The reference case is untouched."],
  kind="simulation")

d(153, "Check standing numerical convergence",
  goal="Show the standing result does not depend on the timestep.",
  inp=[O(150)],
  st=[(50, "Rerun SIM-STAND-01 at timestep 0.001 s and 0.0005 s."),
      (40, "Compare peak knee torque and CoM drift across the three timesteps."),
      (20, "Accept if the change from 0.002 to 0.001 s is under 5% (analysis choice; record it).")],
  calc="Δ% between timesteps for 2 metrics.",
  chk=["All three timesteps reported.", "Δ% stated against the 5% choice.", "The chosen timestep written into stand_ref.json."],
  kind="simulation")

d(154, "Review standing evidence",
  goal="A replayable standing packet with bounded conclusions.",
  inp=[O(150), O(151), O(152), O(153)],
  st=[(40, "Write the review: model hash, controller version, runs, sweeps, convergence, failures."),
      (40, "State conclusions one line each, e.g. 'stands 10 s at 55 ± 5 kg with knee RMS ≤ X N m in this model'."),
      (20, BACKUP)],
  calc="Runs passing analysis criteria / runs.",
  chk=["The exact model and controller are identified.", "Every claim has a run ID.", "Physical standing remains untested."],
  kind="simulation")

# ---------------------------------------------------------------- Week 23
W(23)
d(155, "Define the weight shift trajectory",
  goal="A timed side-to-side shift that keeps both soles flat.",
  inp=[O(154), O(6)],
  st=[(40, "Write tests/cases/shift_ref.json: pelvis moves 0.10 m toward the left foot over 2.0 s (cosine profile), holds 1.0 s, returns over 2.0 s."),
      (40, "Compute the expected stance-foot load at full shift and write it in the case file."),
      (20, "Set tether slack 20 mm; any tether force will be reported as assistance.")],
  calc="Left-foot load at full shift ≈ 539.55 × (0.17 + 0.10)/0.34 ≈ 428 N (static estimate).",
  chk=["Trajectory fully timed.", "Expected load stated with working.", "Within joint envelopes."],
  kind="simulation")

d(156, "Implement bounded weight shift tracking",
  goal="Track the shift with inverse kinematics that keep the feet flat.",
  inp=[O(155), O(149)],
  st=[(50, "Add IK to controllers/shift.py: for lateral shift y, hip roll = −asin(y/L) and ankle roll = +asin(y/L) per leg, L = hip-to-ankle length."),
      (40, "Reuse the standing PD + gravity terms and the same clipping."),
      (20, "Log foot roll relative to the floor; it should stay within ±0.01 rad.")],
  calc="y = 0.10 m, L ≈ 0.84 m → φ = asin(0.119) = 0.119 rad.",
  chk=["Foot roll within ±0.01 rad.", "Same clipping as standing.", "Run replays identically."],
  kind="simulation")

d(157, "Run left and right shifts",
  goal="Mirror runs that expose sign errors.",
  inp=[O(156)],
  st=[(40, "Run SIM-SHIFT-L and SIM-SHIFT-R with identical settings."),
      (40, "Compare peak hip-roll and ankle-roll torques and stance-foot load."),
      (30, "Investigate any left/right difference over 5% by checking axis signs in the register.")],
  calc="Asymmetry % = |L − R| / mean.",
  chk=["Both runs logged.", "Asymmetry ≤ 5% or explained.", "Axis signs confirmed."],
  kind="simulation")

d(158, "Inspect contact and sole behavior",
  goal="Make sure soft contact or friction is not faking success.",
  inp=[O(157)],
  st=[(50, "Plot stance-foot CoP during the shift and measure its closest distance to the sole edge."),
      (40, "Check for corner lift-off (contact force < 5 N) and slip (> 2 mm)."),
      (20, "Write the contact settings used next to the results.")],
  calc="Lateral edge margin = 0.11 m − |CoP_y|.",
  chk=["Edge margin reported.", "Lift-off and slip checked.", "Contact settings cited."],
  kind="simulation")

d(159, "Sweep friction and sensor delay",
  goal="See how the shift behaves with worse floors and slower sensors.",
  inp=[O(157), O(118)],
  st=[(50, "Run the left shift at μ = 0.3, 0.5, 0.7 and with sensor delay 0, 10, 20 ms, one change at a time."),
      (40, "Record success, slip, saturation and tether force in sweeps/shift.csv."),
      (20, "Record peak stance-foot yaw moment and compare with the 28.2 N m Day 6 friction screen.")],
  calc="6 cases; yaw margin = 28.2 − peak yaw (N m) at μ = 0.5.",
  chk=["Each case has its exact values.", "Yaw margin recorded.", "Reference run untouched."],
  kind="simulation")

d(160, "Inject a blocked transition",
  goal="See what the controller does when a foot sensor drops out mid-shift.",
  inp=[O(157), O(128)],
  st=[(50, "At t = 1.0 s mark the left foot-force signal stale. The controller should enter STOP_LATCHED."),
      (40, "Log detection time and what the model robot and tether do over the next 3 s."),
      (20, "Link the result to its hazard ID.")],
  calc="Detection time = t_detect − 1.0 s.",
  chk=["Detection time logged, or the failure recorded.", "Post-stop behaviour described.", "Hazard linked."],
  kind="simulation")

d(161, "Review weight shifting readiness",
  goal="Decide whether the shift is good enough to build steps on.",
  inp=[O(155), O(156), O(157), O(158), O(159), O(160)],
  st=[(50, "Write the passing parameter region (μ, delay, mass) and the failures."),
      (40, "Optionally send the packet to a controls reviewer for 30 minutes of comments."),
      (20, BACKUP)],
  calc="Passing region as μ and delay ranges.",
  chk=["Every claim has a run ID.", "Failures listed.", "Decision written: proceed or rework."],
  kind="simulation", help="Optional: a controls engineer. Get: written notes with name and date.")

# ---------------------------------------------------------------- Week 24
W(24)
d(162, "Define step and speed measurements",
  goal="Rules that count steps and compute speed the same way in simulation and on hardware.",
  inp=[O(3)],
  st=[(40, "Define events: toe-off = foot force < 5% body weight; landing = first contact; stable contact = foot force ≥ 80% of expected for 0.2 s."),
      (40, "Define speed: pelvis x displacement between first toe-off and third stable landing, divided by that time."),
      (20, "Report start-up before the first toe-off and settling after the third landing separately.")],
  calc="0.45 m / 3.0 s = 0.15 m/s; 0.45 m / 4.5 s = 0.10 m/s.",
  chk=["Each event has a numeric threshold.", "The speed formula is fixed.", "The same file is used for hardware Days 281–291."],
  kind="simulation")

d(163, "Create one swing foot trajectory",
  goal="A low, smooth swing the legs can follow.",
  inp=[O(155), O(97)],
  st=[(40, "Define swing: step length 0.144 m, peak lift 0.03 m, duration 0.6 s, quintic profile (zero speed and acceleration at both ends)."),
      (40, "Solve leg IK along the swing; record peak joint speed and acceleration for all 5 joints."),
      (20, "Check sole clearance stays > 0.01 m mid-swing and no Day 97 collision is hit.")],
  calc="Step period 1.2 s → 0.144 / 1.2 = 0.12 m/s.",
  chk=["Peak joint speeds tabulated.", "Clearance > 0.01 m.", "No known collision."],
  kind="simulation")

d(164, "Run one simulated step",
  goal="One logged step driven by a ZMP plan, not by the tether.",
  inp=[O(163), O(156)],
  st=[(50, "Implement ZMP preview control (Kajita et al., 2003) with the cart-table model at CoM height 1.0 m; generate the CoM path for one step."),
      (40, "Run stand → shift → swing → land; save contacts, pelvis x, joint torques and tether force as SIM-STEP-01."),
      (30, "Check tether force during swing against the analysis target of 27 N (5% of weight).")],
  calc="ω = sqrt(9.81 / 1.0) = 3.13 rad/s.",
  chk=["The step is visible in contact logs.", "Tether force reported.", "Failed attempts kept."],
  kind="simulation")

d(165, "Chain three alternating steps",
  goal="L-R-L stepping with explicit hand-overs.",
  inp=[O(164)],
  st=[(50, "Extend the ZMP plan to three steps; hand over only when the landing foot reaches stable contact (Day 162 rule)."),
      (40, "Log each transition time and any limit or fault event."),
      (20, "Define the reset pose and settle time between trials.")],
  calc="3 swings + 3 landings = 6 events per trial.",
  chk=["Six events logged.", "Transitions follow the Day 162 rule.", "Reset defined."],
  kind="simulation")

d(166, "Run two separate simulated trials",
  goal="Two independent three-step trials with speed measured by the fixed rule.",
  inp=[O(165), O(162)],
  st=[(50, "Run SIM-3STEP-T1 and -T2 from the reset pose."),
      (40, "Compute speed per trial and peak and RMS torque per joint."),
      (20, "Write each trial's result separately: steps completed, speed, max tether force.")],
  calc="Target 0.10–0.15 m/s per trial.",
  chk=["Each trial reported on its own.", "Model, controller and case hashes saved.", "Slower or failed trials reported as such."],
  kind="simulation")

d(167, "Inspect gait feasibility conflicts",
  goal="Find joints that need more torque or cooling than the chosen drives give.",
  inp=[O(166), O(111)],
  st=[(50, "Compare each joint's RMS and peak with the drive's rated and peak (direct, 2:1 or 3:1)."),
      (40, "For any joint over rated RMS, rerun with a 1.5 s step period and note the change."),
      (20, "List remaining conflicts with a proposed fix (ratio, posture, hip spacing).")],
  calc="Margin = rated − RMS (N m) per joint.",
  chk=["All 10 joints have margins.", "Slower-step effect measured.", "Conflicts have proposed fixes."],
  kind="simulation")

d(168, "Review simulated gait evidence",
  goal="A gait packet ready for outside comments.",
  inp=[O(162), O(166), O(167)],
  st=[(40, "Package trials, event counts, speeds, torque margins and tether forces."),
      (40, "Send it to a controls or robotics engineer with three questions: is the ZMP plan sound, are the margins enough, what would you change?"),
      (20, BACKUP)],
  calc="Trials meeting 0.10–0.15 m/s / 2.",
  chk=["Assumptions and tether help disclosed.", "Review request recorded.", "No claim that the robot walked."],
  kind="simulation", help="A controls or robotics engineer. Get: written answers to the three questions, with name and date.")

# ---------------------------------------------------------------- Week 25
W(25)
d(169, "Create the bounded sweep matrix",
  goal="Plan every uncertainty case before running any.",
  inp=[O(12), O(166)],
  st=[(50, "Write sweeps/manifest.csv: mass ±10%, CoM ±30 mm, μ 0.3/0.7, delay 10/20 ms, backlash 0.25/0.5°, torque limit 80%."),
      (40, "Give each case an ID and seed; change one parameter at a time from the reference."),
      (20, "Define the outcome: three steps without tether force > 27 N and without saturation > 0.2 s.")],
  calc="12 off-reference cases + 1 reference.",
  chk=["Every case reproducible from the manifest.", "Outcome rule written before running.", "Range sources cited."],
  kind="simulation")

d(170, "Run mass and inertia sensitivity",
  goal="Find the worst credible mass case for the drives.",
  inp=[O(169)],
  st=[(60, "Run the mass and CoM cases from the manifest."),
      (40, "Record outcome, hip-roll RMS and knee RMS per case in sweeps/mass_results.csv."),
      (20, "Highlight the worst case and its margin to rated torque.")],
  calc="Worst hip-roll RMS vs 114 N m (3:1).",
  chk=["All planned cases run or marked not run.", "Worst case identified.", "Failures kept."],
  kind="simulation")

d(171, "Run contact sensitivity",
  goal="Robustness across friction and backlash.",
  inp=[O(169)],
  st=[(60, "Run the μ and backlash cases."),
      (40, "Where the outcome flips, rerun at half timestep to check it is physical, not numerical."),
      (20, "Record peak yaw moment for each μ against μ × 539.55 × 0.104 N m.")],
  calc="Yaw capacity at μ = 0.3: 16.8 N m; at 0.7: 39.4 N m.",
  chk=["Each claim backed by a run.", "Timestep check done where results flip.", "Yaw recorded."],
  kind="simulation")

d(172, "Inject sensing and communication faults",
  goal="Map each sensor or comms fault to a hazard and a detection time.",
  inp=[O(169), O(127)],
  st=[(60, "Inject one per run: encoder freeze, IMU 50 ms delay, foot-sensor dropout, controller comms loss for 100 ms."),
      (40, "Record detection time, the state entered and the tether load afterwards."),
      (20, "Link each to its hazard ID and Day 132 fault case.")],
  calc="4 faults × detection time (ms).",
  chk=["Each fault mapped to a hazard.", "Detection or non-detection recorded.", "Tether load recorded."],
  kind="simulation")

d(173, "Inject saturation and restart faults",
  goal="Show restarts never resume motion and missing limits block motion.",
  inp=[O(128), O(131)],
  st=[(60, "Run: torque limit cut to 80%, limits file missing, limits hash wrong, controller restart mid-step, stale step request."),
      (40, "Check the state machine ends in DISABLED or STOP_LATCHED for each."),
      (20, "Save logs with case IDs.")],
  calc="5 cases; motions after restart expected = 0.",
  chk=["No case resumes motion by itself.", "Missing or bad limits block enable.", "Logs saved."],
  kind="simulation")

d(174, "Reconcile simulation and sizing",
  goal="Give every joint a clear technical status for procurement.",
  inp=[O(170), O(171), O(110), O(111)],
  st=[(60, "For each joint put hand screen, simulated worst RMS and peak, and the drive's rated and peak side by side."),
      (40, "Mark each joint OK / marginal (< 15% margin) / fails, with the fix for marginal and failing joints."),
      (20, "Update the D-03 notes in revision_history/decision_log_R0_3.csv.")],
  calc="Margin % = (rated − worst RMS) / rated.",
  chk=["All 10 joints have a status.", "Fixes named for marginal joints.", "Decision log updated."],
  kind="simulation")

d(175, "Review the simulation evidence release",
  goal="Close the simulation phase with conclusions you can defend.",
  inp=[O(169), O(170), O(171), O(172), O(173), O(174)],
  st=[(40, "Write the summary: model version, convergence, cases run vs planned, failures, open gaps."),
      (40, "Add simulation evidence references to ASTRO-V-04 and ASTRO-V-05 in the working verification matrix, labelled analysis only."),
      (20, BACKUP)],
  calc="Cases run / cases planned.",
  chk=["Every conclusion has a run ID.", "Matrix updated with analysis-only labels.", "Physical walking tests still 0."],
  kind="simulation")

# ---------------------------------------------------------------- Week 26
W(26)
d(176, "Audit mechanical interfaces",
  goal="One consistent set of mechanical interfaces across CAD and tables.",
  inp=[O(92), O(97), O(113)],
  st=[(50, "List every interface: drive-to-bracket, stage-to-link, ankle-to-foot, pelvis-to-torso, shell mounts, tether point."),
      (40, "For each, check the CAD dimension equals the register value; assign an interface ID and drawing number."),
      (20, "Write every mismatch with the chosen value and why.")],
  calc="Interfaces checked / listed.",
  chk=["Every interface has an ID.", "No silent choice between conflicting values.", "Mismatches recorded."])

d(177, "Audit electrical and control interfaces",
  goal="Every signal has a producer, consumer, unit and failure behaviour.",
  inp=[O(120), O(128)],
  st=[(50, "List power rails, connectors, CAN buses (ID per drive), enable lines, fault lines and the limits file path."),
      (40, "For each signal write producer, consumer, unit, rate and what happens if it is lost."),
      (20, "Trace the e-stop path and confirm the computer is not in it.")],
  calc="Signals listed; components in the e-stop path.",
  chk=["Every signal row complete.", "Computer not in the e-stop path.", "Vendor gaps listed."])

d(178, "Reconcile mass cost and simulation",
  goal="One configuration, one set of numbers for G2.",
  inp=[O(103), O(110), O(174)],
  st=[(50, "For Y1-WALK put mass, CoM, worst joint demand, drive choice and actuator cost in one table."),
      (40, "Compare with Day 6 (48.5 kg; actuator line USD 2,841–3,481) and explain each change."),
      (20, "Update D-01, D-03 and D-04 in the decision log.")],
  calc="Δ mass and Δ cost vs Day 6.",
  chk=["Same configuration everywhere.", "Changes explained.", "Decision log updated."])

d(179, "Prepare the independent G2 review",
  goal="A packet a reviewer can work through in two hours.",
  inp=[O(176), O(177), O(178), O(175), O(140)],
  st=[(50, "Assemble requirements, hazards, interface audits, mass, duty, power, simulation summary and facility status."),
      (40, "List the decisions you need, each with its evidence path (e.g. 'accept 3:1 hip roll — see day_174')."),
      (20, "Agree a date and fee with the reviewers in writing.")],
  calc="Reviewer hours × rate vs B-11 USD 600.",
  chk=["Every decision has evidence.", "Reviewers and date confirmed or pending.", "Cost compared with B-11."],
  help="Mechanical, electrical and controls reviewers (one person may cover two). Get: written scope, date and fee.")

d(180, "Conduct the architecture review",
  goal="Record actual G2 decisions from real reviewers.",
  inp=[O(179)],
  st=[(60, "Walk the reviewers through the packet; write their comments as they speak."),
      (40, "For each issue record accepted / rework / blocked, the owner and the evidence needed."),
      (20, "Enter G2 on the website Reviews page only from this record.")],
  calc="Issues by status.",
  chk=["Only people present are listed.", "G2 recorded from the real decision.", "Every issue has an owner."],
  kind="review", help="Same reviewers as Day 179.")

d(181, "Apply the accepted architecture changes",
  goal="Files match what the review accepted.",
  inp=[O(180)],
  st=[(50, "Update the register, CAD and MJCF model for each accepted change; keep old versions with a suffix."),
      (40, "Rerun only the affected checks (tests/test_tree.py, the load screen, sweeps touching that joint)."),
      (20, "List changed files with old and new hashes.")],
  calc="Files changed; checks rerun.",
  chk=["No stale drawing is marked current.", "Affected checks rerun and passing or logged.", "Old versions kept."])

d(182, "Freeze the quotation baseline",
  goal="A frozen, hashed revision to send for quotes, or a rework list.",
  inp=[O(181)],
  st=[(40, "Copy the accepted interface set to architecture/quotation_baseline_R0_3/ and hash every file."),
      (40, "If G2 is blocked, write the rework list in priority order instead and pause procurement prep."),
      (20, BACKUP)],
  calc="Files hashed.",
  chk=["Baseline hashed.", "G2 status stated.", "No purchase implied."])

# ---------------------------------------------------------------- Week 27
W(27)
d(183, "Create the actuator RFQ template",
  goal="A request vendors can answer with numbers.",
  inp=[O(182), O(110), O(111)],
  st=[(50, "Fields: continuous torque at 40 rpm without heat sink, peak torque and allowed duration, thermal resistance, mass, voltage range, regen behaviour, CAN protocol and baud, driver included, lead time, price for 10 and 12."),
      (40, "Attach the joint duty table and the 2:1 knee / 3:1 hip-roll plan as context."),
      (20, "Mark which fields are mandatory for G3.")],
  calc="Quantity 10 + 2 spares = 12.",
  chk=["Every field has a unit.", "Mandatory fields marked.", "No order language."],
  kind="procurement")

d(184, "Prepare the structural fabrication RFQ",
  goal="Quote request for brackets, links and stage plates.",
  inp=[O(182)],
  st=[(50, "Package STEP and PDF drawings, material (e.g. 6061-T6), tolerances and quantity."),
      (40, "Prepare uploads for two online CNC or sheet-metal quote services and one local shop; ask for part price, setup, inspection and shipping separately."),
      (20, "Label the package 'for quotation only'.")],
  calc="Parts × quantity.",
  chk=["Drawings marked quotation-only.", "Costs requested separately.", "Three sources identified."],
  kind="procurement")

d(185, "Prepare the support and rigging RFQ",
  goal="A quote for the robot support from a qualified provider.",
  inp=[O(135)],
  st=[(50, "Send robot mass 55 kg (plus the rigger's margin), height 1.83 m, attachment drawing and the Day 134 site details."),
      (40, "Ask for design, equipment, installation, inspection, rental period and price as separate lines."),
      (20, "Record who you asked and when.")],
  calc="Quote vs B-09 USD 1,000.",
  chk=["Provider and request date recorded.", "Lines requested separately.", "No assumed rating used."],
  kind="procurement")

d(186, "Prepare power and safety sourcing questions",
  goal="Quotes for the pack, charger and safety parts with the data reviewers need.",
  inp=[O(120), O(129)],
  st=[(50, "Request a complete 48 V (13s) pack with BMS and matched charger; ask for datasheet, continuous and peak discharge, and certifications."),
      (40, "Request the safety relay, contactor and e-stops chosen on Day 129, with datasheets."),
      (20, "List vendor exclusions (e.g. 'not for mobile robots').")],
  calc="Quotes vs B-04 USD 650 + B-05 USD 450.",
  chk=["Datasheets requested.", "Reviewer's chosen parts used.", "Exclusions noted."],
  kind="procurement")

d(187, "Prepare feet sensors and handling questions",
  goal="Quotes for foot sensors and the handling actuator and stand.",
  inp=[O(115), O(6)],
  st=[(50, "Request 8 load cells (≥ 600 N each) with amplifiers, plus sole material samples."),
      (40, "Request a guided linear actuator, stroke ≥ 100 mm, datasheet static holding force ≥ 98 N, with limit switches; plus stand parts and a tray."),
      (20, "Attach the 2 kg stationary task description.")],
  calc="Sensors vs B-03 USD 180; handling vs B-08 USD 350.",
  chk=["Holding force requested.", "Every item tied to a requirement.", "Quantities stated."],
  kind="procurement")

d(188, "Request and organize actual quotations",
  goal="Real dated quotes in one register.",
  inp=[O(183), O(184), O(185), O(186), O(187)],
  st=[(40, "Send the five requests yourself by email or vendor form."),
      (40, "Create the register: vendor, item, quantity, unit price, currency, shipping, tax/duty, validity date, mandatory-field answers."),
      (30, "Fill rows as replies arrive; keep 'no reply' rows with the date asked.")],
  calc="Replies received / requests sent.",
  chk=["Every price has a vendor and date.", "Quotes kept separate from allowances.", "No payment made."],
  kind="procurement")

d(189, "Review quotation completeness",
  goal="Know which quotes are usable for G3.",
  inp=[O(188)],
  st=[(50, "Mark each mandatory field compliant / non-compliant / unanswered."),
      (40, "Send follow-ups for the three most important missing fields."),
      (20, "Keep at least one alternative per critical item.")],
  calc="Complete quotes / total.",
  chk=["No drive marked qualified without continuous and thermal data.", "Follow-ups sent.", "Alternatives kept."],
  kind="procurement")

# ---------------------------------------------------------------- Week 28
W(28)
d(190, "Build the landed cost BOM",
  goal="Every year-one cash cost in one table.",
  inp=[O(188), O(189)],
  st=[(50, "Enter each line: part, quantity, unit price, shipping, tax/duty, validity, quote reference."),
      (40, "Add support, fixtures, instruments, reviews, fabrication, panels, software and contingency."),
      (20, "Mark unquoted lines; never enter 0 for unknown.")],
  calc="Σ landed cost; Σ unquoted allowances shown separately.",
  chk=["All cost categories present.", "Unknowns not zero.", "Quote references on quoted lines."],
  kind="procurement")

d(191, "Compare technical compliance by joint",
  goal="Ten joint rows backed by quoted data.",
  inp=[O(190), O(174)],
  st=[(50, "For each joint compare simulated worst RMS and peak with quoted continuous and peak (including stage ratio)."),
      (40, "Add thermal, bearing load, interface and protocol notes."),
      (20, "Write any deviation for the reviewer.")],
  calc="10 rows; margin % each.",
  chk=["No peak-only match accepted.", "Evidence linked per row.", "Deviations listed."],
  kind="procurement")

d(192, "Reconcile the revised mass estimate",
  goal="Mass using quoted parts.",
  inp=[O(190), O(103)],
  st=[(50, "Replace allowances with vendor and CAD masses for every BOM part."),
      (40, "Compute Y1-WALK and Y1-HAND masses and compare with 55 and 65 kg."),
      (20, "Show the remaining reserve.")],
  calc="Reserve = 55 − Y1-WALK mass.",
  chk=["Every costed part also in the mass list.", "Reserve stated.", "Thresholds applied."],
  kind="procurement")

d(193, "Resolve the budget route with Faisal",
  goal="Set the final cash ceiling (D-01) from real quotes.",
  inp=[O(190), O(192), O(5), O(6)],
  st=[(50, "Compare the landed total with the USD 15,000 working cap (owner, 2026-11-04) and the uncommitted reserve."),
      (40, "Choose and write: fund the gap (from where?), documented sponsorship, redesign (what?), or extend the schedule. Record the final ceiling."),
      (20, "If unfunded, mark procurement BLOCKED and write the rework package.")],
  calc="Gap = landed total − chosen ceiling.",
  chk=["Ceiling and funding source recorded.", "No safety or review line cut to fit.", "Rework defined if needed."],
  kind="procurement")

d(194, "Assemble the G3 procurement packet",
  goal="Exact order lines ready for an independent check.",
  inp=[O(190), O(191), O(192), O(193)],
  st=[(50, "Collect requirements, architecture, mass, duty, simulation summary, vendor data, budget and inspection plan."),
      (40, "List exact order lines: vendor, part number, quantity, amount."),
      (20, "Name the reviewer and fabricator.")],
  calc="Σ order lines vs ceiling.",
  chk=["Each G3 prerequisite present or a blocker.", "Order lines exact.", "Reviewer named."],
  kind="procurement")

d(195, "Hold the independent procurement review",
  goal="A real G3 decision on the exact order lines.",
  inp=[O(194)],
  st=[(60, "Go through the packet with the reviewer."),
      (40, "Record the decision for each order line and any conditions."),
      (20, "Enter G3 on the website from this record.")],
  calc="Lines approved / proposed.",
  chk=["Decision tied to the exact revision.", "Conditions recorded.", "Gate entered from the real record."],
  kind="review", help="An independent engineering reviewer. Get: signed decision on the exact BOM revision.")

d(196, "Place only specifically authorized orders",
  goal="Order exactly what G3 approved.",
  inp=[O(195)],
  st=[(40, "Place the approved orders; save confirmations and promised dates."),
      (40, "Enter actual spend per line on the website Budget page."),
      (20, "If G3 is blocked, update the alternatives list instead.")],
  calc="Committed spend vs approved amount.",
  chk=["Each order matches an approved line.", "Actuals entered.", "No other spend."],
  kind="procurement")

# ---------------------------------------------------------------- Week 29
W(29)
d(197, "Update the skeleton to selected components",
  goal="CAD uses the real vendor parts.",
  inp=[O(196)],
  st=[(50, "Import vendor STEP files for drives, sensors and the handling actuator; replace placeholders."),
      (40, "Recheck joint axes, fastener access and cable routes at full range."),
      (20, "Search the assembly for any part still named 'placeholder'.")],
  calc="Placeholders remaining: target 0.",
  chk=["Vendor geometry in place.", "Clearances rechecked.", "No placeholder left."])

d(198, "Prepare load bearing part drawings",
  goal="Drawings ready for structural review, stage brackets included.",
  inp=[O(197), O(106)],
  st=[(50, "Dimension each load-bearing part: material, finish, datums, tolerances, revision."),
      (40, "Link each part to its worst Day 106 load case and the simulated loads."),
      (20, "Mark parts that still need a calculation.")],
  calc="Drawings; parts needing calcs.",
  chk=["Each part traceable to a load case.", "Stage brackets included.", "Pending calcs marked."])

d(199, "Review structural calculations",
  goal="A real structural check of the load-bearing parts.",
  inp=[O(198)],
  st=[(50, "Send drawings and load cases; agree scope and fee."),
      (40, "Record the reviewer's calculations, margins and required changes."),
      (20, "Update the drawings for required changes.")],
  calc="Margin per part from the reviewer.",
  chk=["Reviewer names exact revisions.", "Margins recorded.", "Changes applied."],
  kind="review", help="A mechanical or structural engineer (licensed PE where available). Get: signed calculation check or marked-up drawings.")

d(200, "Produce the one leg fixture drawings",
  goal="A fixture that holds a leg and takes its loads without anyone holding it.",
  inp=[O(198)],
  st=[(50, "Design a frame bolted to a bench or floor that clamps the pelvis plate, with a lever arm and weight hanger for load tests."),
      (40, "Size the frame for the largest test torque (hip roll 80.9 N m static) with the reviewer's margin."),
      (20, "Add inspection notes: bolt torques and joint checks.")],
  calc="80.9 N m at 0.5 m = 161.8 N ≈ 16.5 kg on the hanger.",
  chk=["No hand-held step.", "Lever and loads defined.", "Inspection notes on the drawing."])

d(201, "Produce supported handling fixture drawings",
  goal="Drawings for the handling stand, tray and robot-secure frame.",
  inp=[O(6), O(187)],
  st=[(50, "Draw the floor stand with the bought actuator, a tray with a retaining lip and pin, and a catch tray below."),
      (40, "Check tip-over: base half-width must exceed overturning moment / stand weight."),
      (20, "Draw the frame that secures the robot during handling.")],
  calc="Overturning ≈ 24.5 N × 0.30 m = 7.35 N m; a 10 kg stand needs half-width > 7.35 / 98.1 = 0.075 m before margin.",
  chk=["Tip-over check on the drawing.", "Retention shown.", "Robot-secure frame drawn."])

d(202, "Build fabrication and incoming inspection plans",
  goal="What to check before any part is used.",
  inp=[O(198), O(201)],
  st=[(50, "Per part: material certificate, 3 critical dimensions, fit check, mass."),
      (40, "List tools (calipers, scale, thread gauges) and which you own."),
      (20, "Write the quarantine rule: tagged, bagged, logged.")],
  calc="Inspection points per part.",
  chk=["Every part has checks.", "Tools available or listed.", "Quarantine defined."])

d(203, "Review fabrication readiness",
  goal="Drawings, reviews, parts and shop agree.",
  inp=[O(198), O(199), O(200), O(201), O(202)],
  st=[(50, "Cross-check drawing revisions against the reviewer's sign-off and the quotes."),
      (40, "Send the package to the chosen shop for manufacturability comments."),
      (20, BACKUP)],
  calc="Open items count.",
  chk=["Only reviewed revisions in the package.", "Shop comments logged.", "G4 still pending."])

# ---------------------------------------------------------------- Week 30
W(30)
d(204, "Assemble the G4 release packet",
  goal="Everything a fabrication release needs, in one place.",
  inp=[O(203)],
  st=[(50, "List drawing revisions, materials, shop, processes and inspection hold points."),
      (40, "Attach the owner's cost approval and the structural sign-off."),
      (20, "List anything missing as a blocker.")],
  calc="Packet items present / required.",
  chk=["Every prerequisite evidenced or BLOCKED.", "Hold points listed.", "Cost approval attached."])

d(205, "Conduct the fabrication release review",
  goal="A real G4 decision for specific parts.",
  inp=[O(204)],
  st=[(60, "Review the packet with the structural reviewer and the shop."),
      (40, "Record which parts are released and any conditions."),
      (20, "Enter G4 on the website from that record.")],
  calc="Parts released / proposed.",
  chk=["Release names parts and revisions.", "Conditions recorded.", "Gate entered from the record."],
  kind="review", help="Reviewer from Day 199 and the chosen shop.")

d(206, "Coordinate the released fabrication work",
  goal="The shop builds exactly the released revision.",
  inp=[O(205)],
  st=[(50, "Send the controlled package and get written acknowledgment of revision and quantities."),
      (40, "Answer shop questions in writing and log every change request."),
      (20, "Refuse substitutions that have not been re-reviewed.")],
  calc="Parts ordered = parts released.",
  chk=["Acknowledgment saved.", "Changes logged.", "No unreviewed substitution."],
  kind="procurement")

d(207, "Track vendor and shop delivery",
  goal="Know what is late and which stage it delays.",
  inp=[O(196), O(206)],
  st=[(50, "Update promised and actual dates for every order."),
      (40, "For each late item, write which stage (S2–S16) it delays and by how many days."),
      (20, "Plan desk or software work for the waiting time.")],
  calc="Days late per item; stage delay.",
  chk=["Every order has a status.", "Stage impact written.", "Waiting time planned."],
  kind="procurement")

d(208, "Inspect received commercial components",
  goal="Accept only correct, undamaged commercial parts.",
  inp=[O(202)],
  st=[(50, "For each drive, sensor and pack check part number, serial, visible damage and connector type; weigh it."),
      (40, "Photograph labels; tag and bag anything that does not match."),
      (20, "Reconcile against the packing list and order.")],
  calc="Measured vs datasheet mass (e.g. 1.42 kg per RobStride 04).",
  chk=["Mismatches quarantined.", "Masses recorded.", "Nothing powered."],
  kind="physical")

d(209, "Inspect fabricated parts and fixtures",
  goal="Fabricated parts match the drawings.",
  inp=[O(202)],
  st=[(50, "Check material certificates and 3 critical dimensions per part with calipers."),
      (40, "Fit-check mating parts and weigh each."),
      (20, "Quarantine any non-conforming part.")],
  calc="Dimensions in tolerance / checked.",
  chk=["Each accepted part has an inspection record.", "Defects quarantined.", "Masses updated."],
  kind="physical", help="If a critical dimension is out, ask the Day 199 reviewer whether it can be used. Get: written yes or no.")

d(210, "Review physical readiness for sensors",
  goal="Ready for Stage 2, or clearly blocked.",
  inp=[O(208), O(209), O(84)],
  st=[(50, "Check S1 accepted, G4 released, sensor parts accepted, bench space and calibration references available."),
      (40, "Draft the Stage 2 permit with the reviewer named on Day 133."),
      (20, BACKUP)],
  calc="Missing items count.",
  chk=["S1 and G4 records exist.", "Permit drafted.", "Missing items listed as blockers."])
