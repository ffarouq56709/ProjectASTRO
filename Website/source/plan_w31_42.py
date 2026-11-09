from plan_model import W, d, O

R = "ProjectASTRO/"
STOPOP = "A second competent adult as stop operator, briefed on the e-stop and standing outside the fall zone. Get: their name and signature on the run sheet."
PERMIT = "The reviewer named on Day 133 signs the stage permit. Get: signed permit naming the configuration, limits file hash and people."
BACKUP = "Export a website backup (Settings → Export progress JSON) into ProjectASTRO/evidence/backups/."


def review_day(n, stage, inputs, goal, extra_step, calc="Runs accepted / runs attempted."):
    d(n, f"Review and disposition stage {stage}", goal=goal, inp=inputs,
      st=[(40, f"Build the {stage} evidence index: one line per run with run ID, file path, result, stops and calibration reference."),
          (40, "Send the index to the reviewer. Record their decision (PASS / REWORK / BLOCKED), name, date and conditions in tests/stage records."),
          (30, extra_step)],
      calc=calc,
      chk=[f"{stage} is recorded only from the reviewer's decision.", "Failed and stopped runs are in the index.", "Conditions for the next stage are written."],
      kind="review", help=PERMIT)


# ---------------------------------------------------------------- Week 31 · S2 sensors
W(31)
d(211, "Review the sensor test permit",
  goal="Start Stage 2 only under a signed low-energy permit.",
  inp=[O(210), O(116), O(132)],
  st=[(40, "Fill the permit: you as operator; bench setup with drives unpowered; sensor logic from a current-limited bench supply (≤ 24 V, ≤ 1 A); procedure; calibrated references."),
      (40, "List every channel to check: 10 joint encoders, 1 IMU, 8 foot load cells, drive current and temperature channels."),
      (20, "Get the reviewer's signature and save the scan in ProjectASTRO/tests/permits/.")],
  calc="Channels: 10 + 1 + 8 + current/temperature.",
  chk=["Permit signed and saved.", "Channel list complete.", "Calibration references listed with dates."],
  kind="review", help=PERMIT)

d(212, "Verify position sensor readings",
  goal="Each joint encoder reads the right angle in the right direction.",
  inp=[O(211)],
  st=[(50, "With drives unpowered, turn each output by hand to −0.5, 0, +0.5 rad against a digital angle gauge (±0.1°)."),
      (40, "Record encoder reading, gauge reading and sign for each point in a CSV."),
      (30, "Power-cycle the logic and confirm each encoder reports the same zero within the permit tolerance.")],
  calc="10 joints × 3 angles = 30 points; error = reading − gauge (rad).",
  chk=["30 points recorded; errors within the permit tolerance or logged as failures.", "Every sign matches the register.", "Zero recovers after power-cycle."],
  kind="physical")

d(213, "Verify IMU and time behavior",
  goal="The IMU frame and timestamps match what the controller expects.",
  inp=[O(211)],
  st=[(50, "Place the IMU on each of its 6 faces on a level surface; record the gravity vector for 10 s each."),
      (40, "Log 60 s continuously and count timestamp gaps over 2 ms."),
      (20, "Reboot the IMU and check the stream resumes with a fresh timestamp.")],
  calc="|g| ≈ 9.81 m/s² on each face; sign matches x forward, y left, z up.",
  chk=["All 6 faces give the expected axis and sign.", "Gap count recorded.", "Reboot behaviour recorded."],
  kind="physical")

d(214, "Verify foot contact sensing",
  goal="Foot load cells are calibrated with known weights.",
  inp=[O(116)],
  st=[(50, "On the restrained foot fixture, zero each cell, then load 5, 10 and 20 kg calibrated weights on it in turn."),
      (40, "Fit a straight line per cell; compute the worst error as % of full scale."),
      (20, "Note any saturation and the room temperature.")],
  calc="References 49.05, 98.1, 196.2 N; acceptance ≤ 2% FS per the Day 116 protocol.",
  chk=["8 cells calibrated or failures logged.", "Fit error recorded per cell.", "Raw data saved."],
  kind="physical")

d(215, "Verify current and temperature logging",
  goal="Current and temperature channels read correctly against references.",
  inp=[O(211)],
  st=[(50, "Pass 1, 2 and 5 A through a power resistor from the bench supply; compare the drive current channel with a clamp meter."),
      (40, "Compare each temperature channel with a reference thermometer at room temperature and after 10 min of current."),
      (20, "Write offsets and units in a CSV.")],
  calc="Offset = channel − reference at 3 currents.",
  chk=["Each channel identified and within tolerance, or REWORK.", "Units recorded.", "Second person present while powered."],
  kind="powered", help=STOPOP)

d(216, "Verify disconnect and stale signal behavior",
  goal="An unplugged sensor shows 'unavailable', never a believable zero.",
  inp=[O(212), O(213), O(214)],
  st=[(50, "With drives unpowered, unplug one encoder, the IMU and one foot cell in turn."),
      (40, "Measure how long the software takes to mark each as unavailable (target ≤ 100 ms, set in the permit)."),
      (20, "Confirm the state machine refuses enable while any channel is unavailable.")],
  calc="3 disconnects × detection time (ms).",
  chk=["Every disconnect detected, or logged as a blocker.", "No fake healthy value shown.", "Enable refused."],
  kind="physical")

review_day(217, "S2", [O(212), O(213), O(214), O(215), O(216)],
  "A real S2 decision on the sensor evidence.",
  "Enter S2 on the website Reviews page with the signed record path.",
  calc="Channels passing / channels checked.")

# ---------------------------------------------------------------- Week 32 · S3 one actuator
W(32)
d(218, "Review the actuator bench release",
  goal="A signed permit before any drive gets power.",
  inp=[O(217), O(200)],
  st=[(40, "Fill the permit: knee drive with its 2:1 stage, clamped to the fixture; bench supply 48 V current-limited to 3 A; e-stop in the supply line."),
      (40, "Record drive model, serial, firmware, limits file hash (±0.5 rad, 0.5 rad/s, 3 A), operator and stop operator."),
      (20, "Get the reviewer's signature.")],
  calc="Supply limit 3 A × 48 V = 144 W.",
  chk=["Permit signed.", "Stop operator named.", "Limits hash recorded."],
  kind="review", help=PERMIT + " " + STOPOP)

d(219, "Inspect module installation deenergized",
  goal="The drive is mounted exactly as drawn.",
  inp=[O(218)],
  st=[(50, "With power isolated, check bolt torques (mark each with paint pen), belt tension, connector seating and cable guards."),
      (40, "Weigh the module with its stage and record."),
      (20, "Photograph the installation for the record.")],
  calc="Measured mass vs 1.42 + 0.35 = 1.77 kg (Day 6 assumption).",
  chk=["All items pass or the module is held.", "Mass recorded.", "Power isolated throughout."],
  kind="physical")

d(220, "Check identity and communications under permit",
  goal="You are talking to the right drive and lost messages stop it.",
  inp=[O(219)],
  st=[(50, "Power logic only; read drive ID, firmware and units over CAN and compare with the register."),
      (40, "Unplug the CAN cable; confirm the software refuses enable within 100 ms."),
      (20, "Save the bus log.")],
  calc="Response age (ms) before and after unplugging.",
  chk=["ID unique and matches register.", "Stale comms block enable.", "Bus log saved."],
  kind="powered", help=STOPOP)

d(221, "Run the approved unloaded motion check",
  goal="Bounded unloaded motion inside the permit limits.",
  inp=[O(220)],
  st=[(50, "Run the permit trajectory: 0 → +0.5 → −0.5 → 0 rad at 0.5 rad/s, three times."),
      (40, "Log position, speed, current and temperature at ≥ 200 Hz."),
      (20, "Compute max tracking error and peak current.")],
  calc="Each pass ≈ 4 s; 3 passes ≈ 12 s.",
  chk=["All samples inside the permit limits.", "Any stop recorded with time and cause.", "Stop operator present."],
  kind="powered", help=STOPOP)

d(222, "Check approved module fault behavior",
  goal="The drive stops when commands vanish or the e-stop is pressed.",
  inp=[O(221)],
  st=[(50, "During slow motion, press the e-stop 5 times and kill the command stream 5 times."),
      (40, "Measure time from trigger to zero speed using the 1 kHz logger."),
      (20, "Check that reset alone does not restart motion.")],
  calc="10 trials; report max stop time vs the permit value.",
  chk=["All 10 within the permit value.", "Reset never restarts motion.", "Times measured, not estimated."],
  kind="powered", help=STOPOP)

d(223, "Assess module duty and temperature evidence",
  goal="Check the knee drive stays cool under one gait cycle's load.",
  inp=[O(110), O(222)],
  st=[(50, "If the permit allows: hang the lever load giving 51.7 N m and run the Day 109 knee profile 3 times."),
      (40, "Log winding or case temperature; compute rise per cycle."),
      (20, "If not permitted, analyse the unloaded logs and write what load test is still needed.")],
  calc="Lever: 51.7 N m at 0.5 m = 103.4 N ≈ 10.5 kg.",
  chk=["The tested load and duration are stated exactly.", "Temperature rise recorded.", "Untested conditions listed."],
  kind="powered", help=STOPOP)

review_day(224, "S3", [O(219), O(220), O(221), O(222), O(223)],
  "A real S3 decision on the single-drive evidence.",
  "Write what S3 does not cover (other joints, full leg, continuous duty).")

# ---------------------------------------------------------------- Week 33 · S4 power
W(33)
d(225, "Review the electrical test release",
  goal="A signed electrical permit before the pack is connected.",
  inp=[O(224), O(126)],
  st=[(40, "Check the pack and charger match the design: 13s, 54.6 V full, BMS model, fuse rating set by the electrical reviewer."),
      (40, "Fill the permit: operator, instruments (multimeter, clamp meter), isolation steps, fault tests allowed."),
      (20, "Get the electrical reviewer's signature.")],
  calc="Voltage margin to drive max: 60 − 54.6 = 5.4 V.",
  chk=["Permit signed.", "Pack matches the design.", "Stop conditions listed."],
  kind="review", help="Electrical reviewer from Day 126. Get: signed electrical test permit.")

d(226, "Inspect distribution deenergized",
  goal="The wiring matches the drawings before power.",
  inp=[O(225)],
  st=[(50, "With the pack disconnected, check fuse ratings, contactor model, polarity, wire gauges and connector types against the drawing."),
      (40, "Measure continuity and insulation between DC+ and chassis with the multimeter."),
      (20, "Tag any non-conforming item.")],
  calc="Items passed / items checked.",
  chk=["Exact revision inspected.", "Faults block energising.", "Results recorded."],
  kind="physical", help="Electrical reviewer or a qualified technician to witness. Get: their initials on the checklist.")

d(227, "Verify approved startup and isolation",
  goal="Power comes up only in the designed order.",
  inp=[O(226)],
  st=[(50, "Connect the pack; close the main switch; watch precharge and then contactor closure with motors inhibited."),
      (40, "Record bus voltage, aux voltages and precharge time."),
      (20, "Open the e-stop; confirm the contactor opens and the bus discharges as designed.")],
  calc="Precharge time (s) vs design.",
  chk=["Startup order matches the design.", "No drive enables.", "Readings logged."],
  kind="powered", help=STOPOP)

d(228, "Verify protected auxiliary loads",
  goal="Computer and sensors run steadily from the pack.",
  inp=[O(227)],
  st=[(50, "Run the computer and all sensors from the pack for 30 min; log current, voltage and DC-DC temperature every 10 s."),
      (40, "Compare average power with the Day 121 estimate."),
      (20, "Note any droop below the converter's minimum input.")],
  calc="Measured W vs modelled W.",
  chk=["30 min log saved.", "Within limits.", "Differences explained."],
  kind="powered", help=STOPOP)

d(229, "Review regen and protection behavior",
  goal="Evidence that braking energy and faults are handled.",
  inp=[O(227)],
  st=[(50, "With the reviewer, back-drive one restrained drive and watch bus voltage; confirm the bleeder or BMS limits it below 60 V."),
      (40, "For short-circuit and over-current protection, use vendor test data instead of testing."),
      (20, "Record which cases were tested and which rely on vendor data.")],
  calc="Peak bus voltage during regen (V).",
  chk=["Each protection case evidenced or a blocker.", "No short-circuit test performed.", "Sources recorded."],
  kind="powered", help="Electrical reviewer present.")

d(230, "Check charging and service controls",
  goal="Charging follows the pack manual.",
  inp=[O(125)],
  st=[(50, "Charge on a non-flammable surface per the manual; log time, voltage and temperature."),
      (40, "Practise the service isolation steps: switch off, remove pack plug, wait the stated time, measure bus = 0 V."),
      (20, "Fill the Day 125 procedure with the real values.")],
  calc="Charge time vs manual.",
  chk=["Manual followed.", "Isolation verified with a meter.", "Procedure completed."],
  kind="physical")

review_day(231, "S4", [O(226), O(227), O(228), O(229), O(230)],
  "A real S4 decision on the power system.",
  "Update the power model and hazards ASTRO-H-04 and ASTRO-H-17 with measured values.")

# ---------------------------------------------------------------- Week 34 · S5 safety
W(34)
d(232, "Review the safety test permit",
  goal="Stop-time limits are set before any safety test.",
  inp=[O(231), O(132)],
  st=[(40, "Confirm the reviewer's numbers: max stop time, retained-load method, fault list, logger at ≥ 1 kHz, reset procedure."),
      (40, "Trace the wiring once more to confirm the computer and network are not in the stop path."),
      (20, "Get the safety reviewer's signature.")],
  calc="Logger 1 kHz → 1 ms resolution.",
  chk=["Permit signed.", "Independence traced.", "Criteria present."],
  kind="review", help="Safety reviewer from Day 129.")

d(233, "Test local and operator emergency stops",
  goal="Each e-stop removes drive power within the limit.",
  inp=[O(232)],
  st=[(50, "On the restrained rig, run a joint slowly and press the robot e-stop 5 times, then the hand-held e-stop 5 times."),
      (40, "Measure trigger-to-contactor-open and trigger-to-zero-speed from the logger."),
      (20, "Check the gravity load stays held by the fixture after each stop.")],
  calc="2 stops × 5 = 10 trials; report max times.",
  chk=["All 10 within the limit.", "Times measured.", "Gravity load held."],
  kind="powered", help=STOPOP)

d(234, "Test watchdog and communication loss",
  goal="Losing the computer stops motion through the independent path.",
  inp=[O(232)],
  st=[(50, "During slow motion: kill the controller process, unplug CAN, stop the conversation service — one at a time."),
      (40, "Record what removed drive power and how fast."),
      (20, "Confirm the conversation service stopping changes nothing in motion safety.")],
  calc="3 faults × stop time.",
  chk=["No unbounded motion.", "Independent path acted.", "Logs saved."],
  kind="powered", help=STOPOP)

d(235, "Test restart and power loss behavior",
  goal="Nothing restarts by itself.",
  inp=[O(232)],
  st=[(50, "Run: reset after e-stop, controller reboot, pack disconnect during motion."),
      (40, "After each, confirm motion needs a separate enable and start."),
      (20, "Confirm the fixture holds every load with power gone.")],
  calc="3 cases; unexpected restarts expected = 0.",
  chk=["No automatic restart.", "Loads retained.", "Logs saved."],
  kind="powered", help=STOPOP)

d(236, "Test invalid limits and forbidden requests",
  goal="Bad limits and bypass requests are refused.",
  inp=[O(131)],
  st=[(50, "Try enable with: no limits file, a limits file with a wrong hash, a step request outside the skill list."),
      (40, "Ask the conversation service to 'move the leg now'; confirm the gateway refuses."),
      (20, "Save each denial message.")],
  calc="4 attempts → 4 denials.",
  chk=["All denied.", "Denials saved.", "No motion occurred."],
  kind="powered", help=STOPOP)

d(237, "Test handling and payload interlocks",
  goal="Handling needs a secured robot; walking is refused with a payload.",
  inp=[O(127)],
  st=[(50, "Use switches or dummy signals for support-present and payload-present."),
      (40, "Try all 4 combinations for walking enable and handling enable; fill the 2 × 2 table."),
      (20, "Use an inert dummy weight, never a person or body part.")],
  calc="2 × 2 = 4 combinations; allowed: handling only with support present; walking only with no payload.",
  chk=["Forbidden combinations denied.", "Table saved.", "Sensing limits documented."],
  kind="powered", help=STOPOP)

review_day(238, "S5", [O(233), O(234), O(235), O(236), O(237)],
  "A real S5 decision on the stop and interlock functions.",
  "Record the approved limits file hash that later stages must use.")

# ---------------------------------------------------------------- Week 35 · S6 one joint
W(35)
d(239, "Review the one joint configuration",
  goal="Every part of the one-joint test is named before it starts.",
  inp=[O(238)],
  st=[(40, "Fill the permit for the knee with its 2:1 stage on the leg fixture: drive serial, stage, fixture drawing, limits hash, load plan (up to 51.7 N m)."),
      (40, "Confirm the fixture holds the lever and weights with power off."),
      (20, "Get the reviewer's signature and book the stop operator.")],
  calc="Max planned test torque 51.7 N m.",
  chk=["Permit names all parts.", "Fixture holds loads unpowered.", "People booked."],
  kind="review", help=PERMIT)

d(240, "Inspect the joint and load path",
  goal="The joint is built as drawn.",
  inp=[O(239)],
  st=[(50, "With power isolated, check bearing preload, belt tension, fastener torque marks and alignment."),
      (40, "Record results; any adjustment goes through the reviewer."),
      (20, "Photograph the installed joint.")],
  calc="Belt tension vs vendor value.",
  chk=["Matches the drawing.", "Nonconformances closed or held.", "Photos saved."],
  kind="physical")

d(241, "Verify bounded tracking",
  goal="The joint follows commands with the right sign.",
  inp=[O(240)],
  st=[(50, "Run the unloaded reference: 0 → 0.7 rad knee bend → 0 at 0.5 rad/s, three times."),
      (40, "Log command vs position; compute RMS tracking error."),
      (20, "Check the soft limits stop motion before the hard stops.")],
  calc="RMS tracking error (rad).",
  chk=["Error within the permit value.", "No wrong-direction motion.", "Logs saved."],
  kind="powered", help=STOPOP)

d(242, "Run the approved representative duty",
  goal="The knee carries its gait load on the fixture.",
  inp=[O(241), O(110)],
  st=[(50, "Hang 10.5 kg at 0.5 m (51.7 N m) and run the Day 109 knee profile 3 times."),
      (40, "Log current, speed and temperature."),
      (20, "Compute temperature rise per cycle and extrapolate to 2 trials.")],
  calc="51.7 N m = 10.5 kg × 9.81 × 0.5 m.",
  chk=["Only the tested duty is claimed.", "Temperatures logged.", "Uncertainty stated."],
  kind="powered", help=STOPOP)

d(243, "Check fault response under the joint setup",
  goal="Stops still work with the joint loaded.",
  inp=[O(242)],
  st=[(50, "With the load hung, repeat 3 e-stop and 3 watchdog stops."),
      (40, "Compare stop times with S5."),
      (20, "Note any coast or drop of the load.")],
  calc="Stop time loaded vs S5.",
  chk=["Within the limit.", "No load drop.", "Logs saved."],
  kind="powered", help=STOPOP)

d(244, "Inspect after the duty run",
  goal="No damage is carried into the leg stage.",
  inp=[O(243)],
  st=[(50, "Isolate power and inspect for wear dust, loosened fasteners, belt damage and heat marks."),
      (40, "Recheck torque marks and belt tension; weigh the joint."),
      (20, "Quarantine anything changed.")],
  calc="Torque marks moved: target 0.",
  chk=["No unresolved damage.", "Mass updated.", "Findings recorded."],
  kind="physical")

review_day(245, "S6", [O(241), O(242), O(243), O(244)],
  "A real S6 decision on the single-joint evidence.",
  "Write the limits the one-leg stage may use, based on what S6 showed.")

# ---------------------------------------------------------------- Week 36 · S7 one leg
W(36)
d(246, "Review the one leg permit",
  goal="A permit for five powered joints on the fixture.",
  inp=[O(245)],
  st=[(40, "Fill the permit: left leg, 5 drives (hip roll 3:1, knee 2:1, others direct), fixture, limits hash, cases."),
      (40, "Review collision and cable-strain risks from Day 97 with the reviewer."),
      (20, "Get the signature; book the stop operator.")],
  calc="5 joints; max test torques from Day 110.",
  chk=["Permit complete and signed.", "Collision risks reviewed.", "People booked."],
  kind="review", help=PERMIT)

d(247, "Assemble and inspect through the qualified team",
  goal="The leg is assembled from released parts with hold points checked.",
  inp=[O(246)],
  st=[(60, "Assemble the leg on the fixture following the drawings; stop at each hold point for the reviewer's check."),
      (40, "Record serials, fastener torques and any deviation."),
      (20, "Weigh the leg.")],
  calc="Leg mass vs 10 kg assumption (A6-02).",
  chk=["Hold points signed.", "Deviations recorded.", "Mass recorded."],
  kind="physical", help="Mechanical reviewer for hold-point checks. Get: initials at each hold point.")

d(248, "Verify joint identity and directions",
  goal="Five channels map to the five right joints.",
  inp=[O(247)],
  st=[(50, "Move one joint at a time by +0.1 rad and confirm the expected link moves in the expected direction."),
      (40, "Record name, address, sign and zero for each."),
      (20, "Fix any mismatch before any coupled motion.")],
  calc="5 joints × 1 check.",
  chk=["All names and signs match.", "Mismatches fixed and rechecked.", "Logs saved."],
  kind="powered", help=STOPOP)

d(249, "Run approved coupled leg motion",
  goal="The leg moves through a swing shape safely.",
  inp=[O(248), O(163)],
  st=[(50, "Run the Day 163 swing trajectory slowed to 50% speed, then 100%."),
      (40, "Watch for self-collision and cable strain; log all joints."),
      (20, "Compare peak joint speeds with simulation.")],
  calc="Peak joint speed measured vs simulated.",
  chk=["Inside the permit envelope.", "No collision.", "Logs synchronised."],
  kind="powered", help=STOPOP)

d(250, "Assess leg duty and thermal behavior",
  goal="Check hip roll (3:1) and knee (2:1) heat under load.",
  inp=[O(249)],
  st=[(50, "Hang the hip-roll test load (16.5 kg at 0.5 m = 80.9 N m) and run the hip-roll profile 3 times."),
      (40, "Repeat for the knee at 51.7 N m; log temperatures."),
      (20, "Compare rises with the Day 124 estimate.")],
  calc="80.9 N m = 16.5 kg × 9.81 × 0.5 m.",
  chk=["Temperature rise per joint recorded.", "Compared with the model.", "No walking claim."],
  kind="powered", help=STOPOP)

d(251, "Test stage specific stops and inspect",
  goal="Stops still work with the whole leg; no damage carried forward.",
  inp=[O(250)],
  st=[(50, "Run 3 e-stops and 3 watchdog stops during coupled motion."),
      (40, "Isolate and inspect all 5 joints, cables and sensors."),
      (20, "Quarantine anything changed.")],
  calc="6 stops; stop times vs S5.",
  chk=["Stop times within the limit.", "Inspection complete.", "Defects quarantined."],
  kind="powered", help=STOPOP)

d(252, "Review stage seven and G5",
  goal="Real S7 and G5 decisions.",
  inp=[O(217), O(224), O(231), O(238), O(245), O(251)],
  st=[(40, "Build one index for S2–S7 with every run, stop and inspection."),
      (40, "Ask the mechanical, electrical and safety reviewers to decide S7 and G5; record names, dates and conditions."),
      (30, "Enter S7 and G5 on the Reviews page; " + BACKUP[0].lower() + BACKUP[1:])],
  calc="Stages accepted / 6.",
  chk=["G5 recorded from the real review.", "Blockers kept visible.", "Backup saved."],
  kind="review", help="Mechanical, electrical and safety reviewers.")

# ---------------------------------------------------------------- Week 37 · S8 lower body
W(37)
d(253, "Review the lower body assembly permit",
  goal="A permit limited to assembly and static checks.",
  inp=[O(252)],
  st=[(40, "Fill the permit: both legs, pelvis, feet, overhead support attached at all times."),
      (40, "Write the excluded activities: standing on the floor, weight shift, stepping."),
      (20, "Get the signature.")],
  calc="Lower body mass ≈ 2 × 10 + pelvis ≈ 25 kg (estimate).",
  chk=["Scope limited.", "Support required at all times.", "Signed."],
  kind="review", help=PERMIT)

d(254, "Assemble accepted lower body parts",
  goal="Both legs, pelvis and feet assembled while hanging from the support.",
  inp=[O(253)],
  st=[(60, "Assemble with the pelvis hung from the overhead support; follow the drawings and hold points."),
      (40, "Record serials and any substitution."),
      (20, "Leave drives inhibited.")],
  calc="Parts installed / BOM lines.",
  chk=["Only released parts used.", "Substitutions recorded.", "Supported throughout."],
  kind="physical", help="A helper to lift: the lower body weighs about 25 kg.")

d(255, "Inspect bilateral geometry and clearances",
  goal="As-built geometry matches the CAD.",
  inp=[O(254)],
  st=[(50, "Measure hip-roll axis spacing, foot centre spacing, leg lengths and foot squareness with tape and calipers."),
      (40, "Compare with CAD (e.g. hip axes 0.30 m apart)."),
      (20, "Hold any deviation beyond the drawing tolerance.")],
  calc="Δ = measured − CAD (mm) per dimension.",
  chk=["Within tolerance or held.", "Measurements recorded.", "No powered sweep beyond the permit."],
  kind="physical")

d(256, "Weigh the actual lower body configuration",
  goal="Real mass replaces estimates for the lower body.",
  inp=[O(254)],
  st=[(50, "Weigh the lower body on a calibrated scale (or with a calibrated hanging scale on the support)."),
      (40, "Add remaining estimated upper-body items to project full Y1-WALK mass."),
      (20, "Apply the 55 / 65 kg rules and record the reserve.")],
  calc="Projection = measured lower body + remaining estimates.",
  chk=["Measured and estimated parts labelled.", "Overruns exposed.", "Scale calibration recorded."],
  kind="physical")

d(257, "Check data channels with motion inhibited",
  goal="All ten joint channels and sensors report together.",
  inp=[O(254)],
  st=[(50, "Confirm 10 joint names, 8 foot channels, IMU and time sync in one log."),
      (40, "Confirm the limits hash matches S5 and the interlocks still refuse enable when a channel is missing."),
      (20, "Save the channel audit.")],
  calc="10 + 8 + 1 channels.",
  chk=["Exactly 10 joint channels.", "Interlocks hold.", "Audit saved."],
  kind="powered", help=STOPOP)

d(258, "Review supports and post assembly safety",
  goal="The overhead support is inspected before any standing.",
  inp=[O(135), O(254)],
  st=[(50, "Ask the rigging provider to inspect the attachment, tether, anchor and slack setting with the real robot."),
      (40, "Compare the setup with the Day 136 floor plan."),
      (20, "Record their findings and any changes.")],
  calc="Slack setting (mm) as set by the rigger.",
  chk=["Signed rigging inspection.", "Floor plan matches.", "No one holds the robot."],
  kind="review", help="The rigging provider from Day 135. Get: signed inspection record.")

review_day(259, "S8", [O(255), O(256), O(257), O(258)],
  "A real S8 decision on the assembled lower body.",
  "Write the conditions for a separate supported-standing permit.")

# ---------------------------------------------------------------- Week 38 · S9 standing
W(38)
d(260, "Review the supported standing release",
  goal="A permit for supported standing.",
  inp=[O(259), O(154)],
  st=[(40, "Fill the permit: stand 10 s, three times; slack per the rigger; limits hash; tether load cell logging."),
      (40, "Name who directs the test (the reviewer, or you under their written permit) and the stop operator."),
      (20, "Get the signature.")],
  calc="3 × 10 s stands.",
  chk=["Permit signed.", "Tether logging planned.", "People named."],
  kind="review", help=PERMIT)

d(261, "Inspect the pre standing configuration",
  goal="Preflight complete and signed.",
  inp=[O(260)],
  st=[(50, "Run the preflight: assembly, calibration dates, charge ≥ 80%, support and slack, both e-stops, barrier, no payload."),
      (40, "Record each value and sign; the stop operator countersigns."),
      (20, "Assign run ID S9-RUN-01.")],
  calc="Charge % recorded.",
  chk=["Every item evidenced.", "Area controlled.", "Signed by both people."],
  kind="physical", help=STOPOP)

d(262, "Run the first approved supported stand",
  goal="Stand for the permitted time with support active.",
  inp=[O(261)],
  st=[(50, "Lower the robot until the feet carry load and the tether goes slack; run the standing controller for 10 s."),
      (40, "Log joints, foot loads, temperatures and tether force."),
      (20, "Repeat up to 3 times; stop at any trip.")],
  calc="Mean tether force vs 539.55 N weight (should be near 0 N if standing).",
  chk=["Each run meets criteria or is kept as a failed run.", "Tether force reported.", "Logs saved."],
  kind="powered", help=STOPOP)

d(263, "Compare standing with the model",
  goal="Measure how far reality is from the simulation.",
  inp=[O(262), O(150)],
  st=[(50, "Compare RMS torque per joint, foot load split and CoM drift with SIM-STAND-01."),
      (40, "Quantify differences and the tether's share of support."),
      (20, "List likely causes before changing anything.")],
  calc="% difference per joint.",
  chk=["Same units compared.", "Tether help shown.", "Causes listed."])

d(264, "Apply only reviewed standing corrections",
  goal="Fix standing defects through review.",
  inp=[O(263)],
  st=[(50, "Send the defect list to the reviewer; implement only released changes (gains, calibration, posture)."),
      (40, "Retest the affected case as S9-RUN-02 under a new configuration ID."),
      (20, "Keep the original failed run in the index.")],
  calc="Changes released / proposed.",
  chk=["Every change has a review reference.", "Retest logged.", "Original failure kept."],
  kind="powered", help=STOPOP)

d(265, "Repeat the accepted standing case",
  goal="Show supported standing repeats.",
  inp=[O(264)],
  st=[(50, "Repeat the accepted 10 s stand three times."),
      (40, "Compare the three runs: drift, torque, temperature."),
      (20, "Inspect feet, soles and cables afterwards.")],
  calc="3 runs; spread of CoM drift.",
  chk=["All three meet the protocol, or REWORK.", "Inspection recorded.", "Logs saved."],
  kind="powered", help=STOPOP)

review_day(266, "S9", [O(262), O(263), O(264), O(265)],
  "A real S9 decision on supported standing.",
  "Write the support conditions any weight-shift test must keep.")

# ---------------------------------------------------------------- Week 39 · S10 weight shift
W(39)
d(267, "Review the physical shift protocol",
  goal="Shift amplitudes and limits come from the protocol, not the calendar.",
  inp=[O(266), O(161)],
  st=[(40, "Set the progression: 0.03, 0.06, then 0.10 m lateral shift, 2 s each way, each step only after the previous is accepted."),
      (40, "Copy stop criteria: foot slip > 2 mm, CoP within 0.02 m of the sole edge, any saturation."),
      (20, "Get the signature.")],
  calc="0.03 m = 30% of the 0.10 m simulated sway.",
  chk=["Progression written.", "Stop criteria numeric.", "Signed."],
  kind="review", help=PERMIT)

d(268, "Perform the shift preflight",
  goal="Preflight complete for the shift runs.",
  inp=[O(267)],
  st=[(50, "Run the preflight checklist from Day 261 again."),
      (40, "Confirm nothing changed since S9 (hashes and part list); if anything did, get the reviewer's OK."),
      (20, "Assign run IDs S10-L-01 and S10-R-01.")],
  calc="Hash comparison: S9 vs today.",
  chk=["No stale approval reused.", "Signed.", "Run IDs assigned."],
  kind="physical", help=STOPOP)

d(269, "Run the first left shift case",
  goal="One left shift at the first amplitude, within limits.",
  inp=[O(268)],
  st=[(50, "Run the 0.03 m left shift twice."),
      (40, "Log joints, foot loads, CoP and tether force."),
      (20, "Compute the left-foot load share at full shift.")],
  calc="Expected share at 0.03 m ≈ (0.17 + 0.03) / 0.34 = 59%.",
  chk=["Meets criteria or stopped and recorded.", "Logs saved.", "Stop operator present."],
  kind="powered", help=STOPOP)

d(270, "Run the mirrored right shift case",
  goal="The right shift matches the left.",
  inp=[O(269)],
  st=[(50, "Run the 0.03 m right shift twice."),
      (40, "Compare load share, torques and CoP with the left runs and simulation."),
      (20, "Investigate any asymmetry over 10%.")],
  calc="Asymmetry % = |L − R| / mean.",
  chk=["Asymmetry explained.", "Logs saved.", "Stops recorded."],
  kind="powered", help=STOPOP)

d(271, "Inspect shift loads and temperatures",
  goal="Loads and temperatures stay within the envelopes.",
  inp=[O(269), O(270)],
  st=[(50, "Compute peak and RMS torque per joint, CoP margin and temperature rise for all shift runs."),
      (40, "Compare hip-roll RMS with 114 N m (3:1 rated) and knee with 76 N m (2:1 rated)."),
      (20, "Decide with the reviewer whether to try 0.06 m next.")],
  calc="Margins per joint.",
  chk=["No over-limit run accepted.", "Margins computed.", "Next amplitude decided by the reviewer."])

d(272, "Repeat or rework the bounded shifts",
  goal="Move up to the next amplitude only when evidence allows.",
  inp=[O(271)],
  st=[(50, "If approved, run 0.06 m left and right; otherwise repeat 0.03 m after the agreed fix."),
      (40, "Inspect soles, cables and fasteners afterwards."),
      (20, "Record the configuration if anything changed.")],
  calc="Amplitude run vs approved.",
  chk=["Only the approved amplitude run.", "Inspection recorded.", "Logs saved."],
  kind="powered", help=STOPOP)

review_day(273, "S10", [O(269), O(270), O(271), O(272)],
  "A real S10 decision on weight shifting.",
  "Write the largest accepted shift amplitude; the step permit must stay inside it.")

# ---------------------------------------------------------------- Week 40 · S11 one step
W(40)
d(274, "Review the single step release",
  goal="A signed permit for one step.",
  inp=[O(273), O(164)],
  st=[(40, "Set the first step: length 0.08 m, lift 0.02 m, swing 0.8 s; then 0.12 m if accepted."),
      (40, "Confirm the arrest system was inspected this week and the area is clear."),
      (20, "Get the signature.")],
  calc="0.08 m ≈ 55% of the 0.144 m simulated step.",
  chk=["Permit complete.", "Arrest inspected.", "Signed."],
  kind="review", help=PERMIT)

d(275, "Verify the step evidence setup",
  goal="The logs can reconstruct a step exactly.",
  inp=[O(162)],
  st=[(50, "Set two cameras (side and front) at fixed marks with a 1 m scale bar in view; check focus and frame rate (≥ 60 fps)."),
      (40, "With motion disabled, tap each foot sensor and flash an LED to check video-to-log sync."),
      (20, "Make sure no one who hasn't agreed is in frame.")],
  calc="Sync error between video and log (ms).",
  chk=["Events reconstructable.", "Sync error measured.", "Privacy respected."],
  kind="physical")

d(276, "Execute one released tethered step",
  goal="One real step, honestly recorded.",
  inp=[O(275)],
  st=[(50, "Run the 0.08 m step from the reset pose."),
      (40, "Stop on a tether catch, slip or limit trip; keep the full recording either way."),
      (20, "Assign run ID S11-RUN-01 and note the outcome immediately.")],
  calc="1 swing + 1 landing event expected.",
  chk=["Swing and landing seen in logs, or failure recorded.", "Within limits.", "Recording kept."],
  kind="powered", help=STOPOP)

d(277, "Analyze the actual step and support load",
  goal="Describe exactly what the hardware did.",
  inp=[O(276), O(164)],
  st=[(50, "Apply the Day 162 event rules; measure step length and pelvis displacement from video and logs."),
      (40, "Compute mean tether force during swing and compare with 27 N."),
      (20, "Compare with SIM-STEP-01.")],
  calc="Mean tether force during swing (N).",
  chk=["Result stated exactly.", "Assistance disclosed.", "Simulation comparison saved."])

d(278, "Review and correct step defects",
  goal="Fix step problems through review.",
  inp=[O(277)],
  st=[(50, "Send the analysis to the reviewer and list proposed fixes."),
      (40, "Apply only released changes and update the configuration ID."),
      (20, "Schedule the repeat.")],
  calc="Fixes released / proposed.",
  chk=["No unreviewed change.", "Configuration updated.", "Repeat scheduled."],
  kind="powered", help=STOPOP)

d(279, "Repeat the accepted single step",
  goal="Show the step repeats, then try 0.12 m if allowed.",
  inp=[O(278)],
  st=[(50, "Repeat the 0.08 m step twice; if both pass and the reviewer agrees, run one 0.12 m step."),
      (40, "Inspect soles, cables and fasteners afterwards."),
      (20, "Log all attempts.")],
  calc="Attempts passing / attempted.",
  chk=["Meets criteria or REWORK.", "Inspection recorded.", "All attempts logged."],
  kind="powered", help=STOPOP)

review_day(280, "S11", [O(276), O(277), O(278), O(279)],
  "A real S11 decision on single stepping.",
  "Write the step length and timing the three-step protocol may use.")

# ---------------------------------------------------------------- Week 41 · S12 three steps
W(41)
d(281, "Write the three step physical protocol",
  goal="Exact rules for the first three-step trial.",
  inp=[O(162), O(280)],
  st=[(50, "Write: reset pose, L-R-L sequence, step length (from S11), timing 1.2 s per step, Day 162 event rules."),
      (40, "Fix the acceptable tether assistance before testing (e.g. mean ≤ 27 N during swing, no catch) with the reviewer."),
      (20, "List stop conditions.")],
  calc="Speed = pelvis Δx / Δt from first toe-off to third stable landing.",
  chk=["Step completion separate from speed.", "Assistance limit set in advance.", "Stops listed."])

d(282, "Obtain the three step permit",
  goal="A signed three-step permit.",
  inp=[O(281)],
  st=[(50, "Send S11 evidence, simulation, configuration and protocol to the reviewer."),
      (40, "Record their decision and conditions."),
      (20, "Book the stop operator and the rigging check.")],
  calc="—",
  chk=["Permit signed.", "Conditions recorded.", "People booked."],
  kind="review", help=PERMIT)

d(283, "Complete the three step preflight",
  goal="Preflight complete for trial 1.",
  inp=[O(282)],
  st=[(50, "Run the full preflight: area, arrest, configuration, calibration, temperatures, charge, interlocks, cameras."),
      (40, "Check the sequence file and limits hashes match the permit."),
      (20, "Assign run ID S12-T1.")],
  calc="Hashes match: yes/no.",
  chk=["All references match.", "All channels live.", "Signed by both people."],
  kind="physical", help=STOPOP)

d(284, "Run the released three step sequence",
  goal="Run trial 1 of the two required three-step trials.",
  inp=[O(283)],
  st=[(50, "Run the L-R-L sequence once."),
      (40, "Keep the full recording; stop at any catch or trip and do not retry inside this run."),
      (20, "Note the outcome immediately.")],
  calc="3 swings + 3 landings expected.",
  chk=["Three steps without catch, push or hand support, or the failure recorded.", "Logs saved.", "Stop operator present."],
  kind="powered", help=STOPOP)

d(285, "Analyze count speed and limits",
  goal="Turn the trial 1 logs into counted steps and a measured speed.",
  inp=[O(284)],
  st=[(50, "Count events by the Day 162 rules; compute speed."),
      (40, "Compute peak and RMS torque, temperatures and mean tether force."),
      (20, "State whether 0.10–0.15 m/s was reached.")],
  calc="v = Δx / Δt.",
  chk=["Speed from measurement.", "Limits compared.", "Saved."])

d(286, "Resolve three step defects",
  goal="Fix trial 1 problems through review.",
  inp=[O(285)],
  st=[(50, "Review stops and discrepancies with the reviewer."),
      (40, "Apply released changes; update the configuration ID."),
      (20, "If changed, rerun trial 1 under a new run ID.")],
  calc="—",
  chk=["Each change reviewed.", "Retest planned or run.", "Failures kept."],
  kind="powered", help=STOPOP)

review_day(287, "S12", [O(284), O(285), O(286)],
  "A real S12 decision on the first three-step trial.",
  "Draft the trial 2 protocol with its own reset, preflight and run ID.")

# ---------------------------------------------------------------- Week 42 · S13 repeat
W(42)
d(288, "Review the repeated trial protocol",
  goal="Rules for trial 2, separate from trial 1.",
  inp=[O(287)],
  st=[(50, "Write trial 2: reset, inspection, cool-down to within 5 °C of trial 1's start temperature, same configuration."),
      (40, "If anything changed since trial 1, write whether trial 1 must be repeated."),
      (20, "Get the reviewer's OK.")],
  calc="Cool-down target: T_start2 − T_start1 ≤ 5 °C.",
  chk=["Eligibility explicit.", "Configuration fixed.", "Reviewer OK recorded."])

d(289, "Inspect and reset for the second trial",
  goal="Robot inspected and reset for trial 2.",
  inp=[O(288)],
  st=[(50, "Inspect robot, support, soles, cables and channels."),
      (40, "Record reset pose, temperatures, charge and hashes."),
      (20, "Assign run ID S13-T2.")],
  calc="—",
  chk=["No defect ignored.", "Hashes unchanged.", "Signed."],
  kind="physical", help=STOPOP)

d(290, "Run the second released three step trial",
  goal="Run trial 2 of the two required three-step trials.",
  inp=[O(289)],
  st=[(50, "Run the same L-R-L sequence."),
      (40, "Keep the full recording; a caught or stopped trial counts as an attempt only."),
      (20, "Note the outcome immediately.")],
  calc="3 + 3 events expected.",
  chk=["Three accepted steps, or failure recorded.", "Logs saved.", "Stop operator present."],
  kind="powered", help=STOPOP)

d(291, "Compare both physical trials",
  goal="One table that shows both trials honestly.",
  inp=[O(284), O(290)],
  st=[(50, "Table: steps, speed, peak and RMS torque per joint, temperatures, stops, mean tether force — one column per trial."),
      (40, "Mark which criteria each trial met."),
      (20, "Do not average across trials.")],
  calc="Per-trial values only.",
  chk=["Both trials reconstructable from raw data.", "Criteria per trial.", "Saved."])

d(292, "Investigate any inconsistent result",
  goal="Explain differences, or record the goal as unmet.",
  inp=[O(291)],
  st=[(50, "Compare initial state, floor, tether, temperatures and calibration between trials."),
      (40, "If either trial failed, write 'gait goal unmet' and the retest the reviewer would accept."),
      (20, "Record the conclusion.")],
  calc="—",
  chk=["A two-trial claim exists only if both are accepted.", "Retest scoped if needed.", "Recorded."])

d(293, "Complete the locomotion evidence packet",
  goal="S8–S13 in one packet.",
  inp=[O(259), O(266), O(273), O(280), O(287), O(291)],
  st=[(50, "Collect stage records, masses, permits, logs and comparisons in tests/locomotion_packet/."),
      (40, "Write the limitations: tether, controlled area, straight line, no payload."),
      (20, "Index the packet.")],
  calc="Documents indexed.",
  chk=["Failures included.", "Claims precise.", "Indexed."])

d(294, "Review stage thirteen and G6",
  goal="Real S13 and G6 decisions.",
  inp=[O(293)],
  st=[(40, "Ask the reviewers to decide S13 and G6; record names, dates and conditions."),
      (40, "Write unmet goals plainly (e.g. 'speed 0.08 m/s, below target')."),
      (30, "Enter S13 and G6 on the Reviews page; " + BACKUP[0].lower() + BACKUP[1:])],
  calc="—",
  chk=["From the real review.", "Unmet goals explicit.", "Handling stays a separate permit."],
  kind="review", help=PERMIT)
