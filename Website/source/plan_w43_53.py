from plan_model import W, d, O

R = "ProjectASTRO/"
PHOTO = R + "cad_specifications/reference/astro-rigid-panel-concept-v1.png"
STOPOP = "A second competent adult as stop operator, briefed on the e-stop and standing outside the fall zone. Get: their name and signature on the run sheet."
PERMIT = "Your named reviewer signs the stage permit. Get: signed permit naming the configuration, limits file hash and people."
BACKUP = "Export a website backup (Settings → Export progress JSON) into ProjectASTRO/evidence/backups/."

# ---------------------------------------------------------------- Week 43 · handling setup
W(43)
d(295, "Freeze the stationary handling configuration",
  goal="One named handling configuration with every mass listed separately.",
  inp=[O(6), O(201), O(103)],
  st=[(40, "Define Y1-HAND: robot secured to its frame, walking disabled, separate floor stand, bought actuator, tray, 2 kg object."),
      (40, "List masses separately: robot (as weighed), stand, actuator, tray, object."),
      (20, "Write the configuration ID into the limits file and the handling software.")],
  calc="Held load: 19.62 N (object) + ≈ 4.9 N (tray) = 24.5 N.",
  chk=["Masses listed separately.", "Walking disabled in this configuration.", "ID used in every file."])

d(296, "Review handling load and retention",
  goal="A reviewer confirms the holding force and stand stability.",
  inp=[O(295), O(187)],
  st=[(50, "Send the actuator datasheet (holding force), stand drawing and tip-over check to the mechanical reviewer."),
      (40, "Ask them to set the required holding ratio (screen used 4: 98 N ÷ 24.5 N) and confirm the tray retention."),
      (20, "Record their answer.")],
  calc="Ratio = datasheet holding force ÷ 24.5 N.",
  chk=["Ratio set by the reviewer.", "Stand stability confirmed.", "Retention confirmed or rework listed."],
  kind="review", help="Mechanical reviewer. Get: signed note with the ratio and drawing revision.")

d(297, "Release the handling trajectory",
  goal="Every motion value approved by the reviewer.",
  inp=[O(296)],
  st=[(50, "Propose: travel 0.10 m, speed 0.02 m/s, dwell 5 s at top and bottom, reach 0.30 m from the stand column."),
      (40, "Write the 10-cycle sequence and get the reviewer to accept or change each value."),
      (20, "Save the accepted values in the limits file.")],
  calc="0.10 m ÷ 0.02 m/s = 5 s each way; 20 s per cycle; 200 s for 10 cycles.",
  chk=["Each value accepted by the reviewer.", "Sequence written.", "Limits file updated."])

d(298, "Inspect the fixture module and catch tray",
  goal="Stand, actuator, tray and catch tray checked before any load.",
  inp=[O(297)],
  st=[(50, "Check stand bolts, actuator mounting, tray lip and pin, catch-tray position under the tray path."),
      (40, "Record serials and the position, current and temperature channels."),
      (20, "Leave the object off.")],
  calc="Items passed / checked.",
  chk=["All items pass.", "Channels identified.", "Unloaded."],
  kind="physical")

d(299, "Verify unloaded handling and interlocks",
  goal="Handling runs unloaded and the interlocks refuse unsafe combinations.",
  inp=[O(298), O(237)],
  st=[(50, "Run 3 unloaded cycles; check end positions and stops."),
      (40, "Set support-present false and try handling enable; set payload-present true and try walking enable."),
      (20, "Log both denials.")],
  calc="2 forbidden combinations → 2 denials.",
  chk=["Both denied.", "Stops work.", "Logs saved."],
  kind="powered", help=STOPOP)

d(300, "Prepare the ten repetition protocol",
  goal="Rules that tell complete, stopped and failed cycles apart.",
  inp=[O(297)],
  st=[(50, "Define one cycle: bottom dwell 5 s → up 0.10 m → top dwell 5 s → down → bottom. Complete = all four events with no trip."),
      (40, "Set limits for current, temperature and position error, and what to do on power loss or tray release."),
      (20, "Write the payload check: weigh before and after.")],
  calc="10 cycles × 4 events = 40 events.",
  chk=["Outcomes unambiguous.", "All limits set.", "Saved."])

d(301, "Review stage fourteen readiness",
  goal="A signed S14 permit for the stationary 2 kg task.",
  inp=[O(296), O(299), O(300)],
  st=[(50, "Send structural, actuator, retention, interlock and protocol evidence to the reviewer."),
      (40, "Record the permit or the list of blockers."),
      (20, "Book the stop operator.")],
  calc="—",
  chk=["Permit covers stationary 2 kg only.", "Signed.", "People booked."],
  kind="review", help=PERMIT)

# ---------------------------------------------------------------- Week 44 · S14
W(44)
d(302, "Verify the payload and preflight",
  goal="The object is weighed and the setup is secured.",
  inp=[O(301)],
  st=[(50, "Weigh the object on a calibrated scale; it must read 2.00 kg within the permit tolerance."),
      (40, "Secure the robot to its frame, place the catch tray, confirm walking is disabled."),
      (20, "Start logging; assign run ID S14-RUN-01.")],
  calc="Measured mass vs 2.00 kg.",
  chk=["Mass recorded.", "Preflight signed by both people.", "Logging live."],
  kind="physical", help=STOPOP)

d(303, "Execute only the approved handling check",
  goal="One loaded cycle within limits.",
  inp=[O(302)],
  st=[(50, "Place the object, pin it, and run one cycle."),
      (40, "Log position, current, temperature and any force reading."),
      (20, "Compare peak current with the limit and decide with the reviewer whether to run 10.")],
  calc="Peak current vs limit.",
  chk=["Meets criteria, or the 10-cycle run is blocked.", "Logs saved.", "Stop operator present."],
  kind="powered", help=STOPOP)

d(304, "Run the ten repetition sequence",
  goal="Ten complete cycles, every one recorded.",
  inp=[O(303), O(300)],
  st=[(50, "Run 10 cycles back to back."),
      (40, "Label each cycle complete, stopped or failed using the Day 300 rules."),
      (20, "Weigh the object again afterwards.")],
  calc="≈ 200 s run time.",
  chk=["10 complete cycles, or the actual count stated.", "Robot stayed secured; walking disabled.", "Raw logs saved."],
  kind="powered", help=STOPOP)

d(305, "Analyze handling duty and stop evidence",
  goal="Per-cycle numbers for all ten handling cycles.",
  inp=[O(304)],
  st=[(50, "Tabulate per cycle: time, peak current, temperature, end-position error."),
      (40, "Find the worst cycle and any trend (e.g. temperature climbing)."),
      (20, "Any limit excursion makes that cycle not complete until the reviewer decides.")],
  calc="Temperature rise over 10 cycles (°C).",
  chk=["Each cycle traceable.", "Worst case stated.", "Saved."])

d(306, "Inspect and review after load testing",
  goal="No hidden damage after the load test.",
  inp=[O(305)],
  st=[(50, "Isolate power; inspect mounts, tray lip and pin, actuator rod and cables."),
      (40, "Quarantine anything damaged."),
      (20, "Send any partial-run questions to the reviewer.")],
  calc="—",
  chk=["No unresolved defect.", "Recorded.", "Questions sent."],
  kind="physical")

d(307, "Retest only the reviewed handling scope",
  goal="Retest if needed; otherwise audit the data.",
  inp=[O(306)],
  st=[(50, "If the reviewer asks for a retest, run it with run ID S14-RUN-02 after the agreed fix."),
      (40, "Otherwise audit the S14-RUN-01 logs for missing samples."),
      (20, "Keep all earlier failures in the index.")],
  calc="—",
  chk=["The claim matches the accepted task.", "Failures kept.", "Mass stays 2 kg."],
  kind="powered", help=STOPOP)

d(308, "Review and disposition stage fourteen",
  goal="A real reviewer decision on the 2 kg handling stage.",
  inp=[O(302), O(304), O(305), O(306), O(307)],
  st=[(40, "Build the S14 index: payload weights, cycles, stops, inspections."),
      (40, "Record the reviewer's decision, name, date and conditions."),
      (20, "Enter S14 on the Reviews page.")],
  calc="Complete cycles / 10.",
  chk=["Recorded from the real review.", "No person lifting implied.", "Conditions written."],
  kind="review", help=PERMIT)

# ---------------------------------------------------------------- Week 45 · shell
W(45)
d(309, "Update panels from the as built skeleton",
  goal="Panels fit the real robot and still look like the photo.",
  inp=[O(90), O(255), PHOTO],
  st=[(50, "Adjust panel CAD to measured joint centres, vents, e-stop, camera window and tether point."),
      (40, "Update each panel's area and mass."),
      (20, "Mark any panel that would cover an unguarded moving gap.")],
  calc="Panel total vs 5.2 kg (risk +1.6 kg).",
  chk=["Uses as-built measurements.", "Access kept.", "Masses updated."])

d(310, "Review material thickness and process",
  goal="Choose the shell material and process with evidence.",
  inp=[O(309)],
  st=[(50, "Compare ABS, PETG and ASA at 1.5 mm: mass per m², heat resistance, cleaning, finish, cost."),
      (40, "Get quotes for two processes (e.g. 3D-print service, vacuum forming)."),
      (20, "Ask the reviewer to accept the choice.")],
  calc="Mass per m² = 0.0015 × density (e.g. 1,050 kg/m³ → 1.58 kg/m²).",
  chk=["Choice traceable.", "Quotes saved.", "Reviewer accepted."])

d(311, "Release removable panel fabrication",
  goal="Panels ordered from released files.",
  inp=[O(310)],
  st=[(50, "Send geometry, fasteners, finish, seams and vents to the supplier."),
      (40, "Record any substitution they propose and get it reviewed."),
      (20, "Record the cost on the Budget page.")],
  calc="Quote vs B-07 USD 550.",
  chk=["Released files only.", "Substitutions logged.", "Cost recorded."],
  kind="procurement")

d(312, "Inspect and weigh produced panels",
  goal="Every panel has an ID and a mass.",
  inp=[O(311)],
  st=[(50, "Inspect edges, vents and fastener holes against the drawings."),
      (40, "Weigh each panel; enter M-11 on the Budget & mass page."),
      (20, "Tag defects.")],
  calc="Σ panel mass vs 5.2 kg.",
  chk=["IDs and masses recorded.", "Defects tagged.", "M-11 updated."],
  kind="physical")

d(313, "Fit panels with energy isolated",
  goal="Panels on, with stops, vents and sensors clear.",
  inp=[O(312)],
  st=[(50, "Isolate power and secure the robot in its support; fit panels in the planned order."),
      (40, "Check e-stop reach, privacy light, vents, camera window and tether point."),
      (20, "Write any conflict for rework.")],
  calc="Panels fitted / total.",
  chk=["Fitted with power off.", "Access clear.", "Conflicts recorded."],
  kind="physical")

d(314, "Inspect appearance and service removal",
  goal="It looks like the photo and can still be serviced.",
  inp=[O(313), PHOTO],
  st=[(50, "Photograph the robot from the photo's angles; list differences (head, shoulders, knee pads, feet, teal light, fixed hands)."),
      (40, "Remove and refit two panels; time it."),
      (20, "Record which differences you accept.")],
  calc="Panel removal time (min).",
  chk=["Differences listed.", "Service works.", "No inflatable or combat styling."],
  kind="physical")

d(315, "Review enclosure test readiness",
  goal="Ready for S15, or blocked.",
  inp=[O(312), O(313), O(314)],
  st=[(50, "Project full Y1-WALK mass with panels; apply the 55 / 65 kg rules."),
      (40, "Draft the S15 permit: clearance poses and thermal duty."),
      (20, "List blockers.")],
  calc="Full mass projection (kg).",
  chk=["Mass rules applied.", "Permit drafted.", "Blockers listed."])

# ---------------------------------------------------------------- Week 46 · S15
W(46)
d(316, "Review the S15 test permit",
  goal="Clearance and thermal limits set before testing.",
  inp=[O(315)],
  st=[(50, "Define the poses to inspect, the bounded motions, the thermal duty (e.g. 10 min of the gait profile on the support) and temperature limits."),
      (40, "Keep walking and handling configurations separate."),
      (20, "Get the signature.")],
  calc="Thermal duty duration (min).",
  chk=["Numeric criteria.", "Signed.", "Separate configurations."],
  kind="review", help=PERMIT)

d(317, "Check the isolated clearance envelope",
  goal="Measure panel gaps at the required poses.",
  inp=[O(316)],
  st=[(50, "With power off, move the legs by hand (or support) to each pose and measure gaps with feeler gauges or calipers."),
      (40, "Record the minimum gap per joint."),
      (20, "Stop on any rubbing or pinch.")],
  calc="Minimum gap (mm) per joint vs permit.",
  chk=["Within criteria or rework.", "Recorded.", "Power off."],
  kind="physical")

d(318, "Run approved supported clearance motion",
  goal="Panels don't bind during powered motion.",
  inp=[O(317)],
  st=[(50, "Run the permitted unloaded motions on the support."),
      (40, "Watch and listen for rubbing; log current spikes and stops."),
      (20, "Inspect panels afterwards.")],
  calc="Current spikes compared with S8 baseline.",
  chk=["No binding.", "Stops reachable.", "Logs saved."],
  kind="powered", help=STOPOP)

d(319, "Run the approved enclosure thermal duty",
  goal="Measure drive temperatures with the shell on.",
  inp=[O(318)],
  st=[(50, "Run the permitted duty with panels fitted; log ambient and drive temperatures."),
      (40, "Repeat with panels off (or use S7 data) and compare."),
      (20, "Stop at the permit limit.")],
  calc="ΔT shell-on − shell-off (°C) per hot joint.",
  chk=["Measured or marked unverified.", "No touch-safety claim.", "Logs saved."],
  kind="powered", help=STOPOP)

d(320, "Check cleaning and maintenance compatibility",
  goal="Cleaning instructions match the real materials.",
  inp=[O(310)],
  st=[(50, "Wipe a spare panel sample with the planned cleaner 20 times."),
      (40, "Record any damage, residue or blocked vents."),
      (20, "Write the cleaning instruction for the handover notes.")],
  calc="20 wipes.",
  chk=["Result recorded.", "Instruction written.", "No infection-control claim."],
  kind="physical")

d(321, "Resolve panel thermal or mass defects",
  goal="Fix and retest enclosure problems.",
  inp=[O(317), O(318), O(319), O(320)],
  st=[(50, "Send issues to the reviewer; apply released changes (vents, gaps, thinner panels)."),
      (40, "Retest only the affected poses or duty."),
      (20, "Update mass and BOM.")],
  calc="Issues closed / open.",
  chk=["No untested change accepted.", "Retested.", "Mass and BOM updated."],
  kind="powered", help=STOPOP)

d(322, "Review S15 and the G7 release",
  goal="Real S15 and G7 decisions.",
  inp=[O(308), O(321)],
  st=[(40, "Build the S14–S15 index."),
      (40, "Record the reviewers' decisions on S15 and G7 with limits."),
      (30, "Enter them on the Reviews page; " + BACKUP[0].lower() + BACKUP[1:])],
  calc="—",
  chk=["From the real review.", "Use limited to controlled research.", "Recorded."],
  kind="review", help=PERMIT)

# ---------------------------------------------------------------- Week 47 · integration
W(47)
d(323, "Install the accepted companion release",
  goal="The reviewed app runs on the robot computer.",
  inp=[O(84)],
  st=[(50, "Install the tagged software release on the robot computer; record OS, Python and package versions."),
      (40, "Compare file hashes with the Day 84 archive."),
      (20, "Confirm the app has no CAN or motor credentials.")],
  calc="Hash matches / files.",
  chk=["Matches the release.", "Drives inhibited during install.", "No motor access."],
  kind="software")

d(324, "Verify the software motion boundary",
  goal="The app can only request named, bounded skills.",
  inp=[O(323), O(65)],
  st=[(50, "With drives inhibited, send each allowed skill request and check the gateway logs it."),
      (40, "Try a raw joint command, a limits change and a model 'bypass' prompt; save each denial."),
      (20, "Record results.")],
  calc="Bypass attempts → denials.",
  chk=["Authority not expanded.", "Denials saved.", "Drives inhibited."],
  kind="software")

d(325, "Run companionship on the stationary setup",
  goal="Games and stories on the robot while it is secured.",
  inp=[O(323)],
  st=[(50, "Run one game, one story, an unclear request and a 'get a person' request in each of the 5 modes."),
      (40, "Check speaker volume, captions, board and stop-button visibility."),
      (20, "Keep everyone outside the motion zone.")],
  calc="5 modes × 4 tasks = 20 cases.",
  chk=["Works or hands off clearly.", "No motion.", "Logged."],
  kind="software")

d(326, "Run records and medication on the robot interface",
  goal="Same results on the robot as on the laptop.",
  inp=[O(323), O(42)],
  st=[(50, "Enter observations, correct one, and log a medication response."),
      (40, "Compare results with the laptop baseline."),
      (20, "Check the instruction string hash matches.")],
  calc="Instruction hash equality.",
  chk=["No silent change.", "Provenance kept.", "Logged."],
  kind="software")

d(327, "Run communication with explicit consent",
  goal="An approved send to the approved recipient only.",
  inp=[O(57), O(63)],
  st=[(50, "Preview, confirm and send a fictional summary to the approved recipient or mock."),
      (40, "Show receipt and, separately, human review; show the manual call option."),
      (20, "Check the SIMULATED label on every screen and message.")],
  calc="Unapproved sends: 0.",
  chk=["Approved content and recipient only.", "Truthful status.", "Logged."],
  kind="software")

d(328, "Inject application outages while supported",
  goal="App failures cannot move the robot or fake success.",
  inp=[O(327)],
  st=[(50, "Stop the conversation service, the mock endpoint and the app process in turn."),
      (40, "Check records, privacy state and stop authority after each."),
      (20, "Confirm no motion was requested.")],
  calc="3 outages.",
  chk=["No unrestricted motion.", "No fake receipt.", "Logged."],
  kind="software")

d(329, "Review stationary integration evidence",
  goal="An integration packet with critical defects closed.",
  inp=[O(324), O(325), O(326), O(327), O(328)],
  st=[(50, "Index all integration runs and defects."),
      (40, "Fix and retest critical defects."),
      (20, BACKUP)],
  calc="Critical defects open: target 0.",
  chk=["Mapped to cases.", "Critical defects closed.", "Gait and handling claims kept separate."],
  kind="software")

# ---------------------------------------------------------------- Week 48 · demo prep
W(48)
d(330, "Audit year one demonstration coverage",
  goal="Know exactly what can be shown live.",
  inp=[O(3), O(294), O(308), O(329)],
  st=[(50, "Map each Year 1 requirement to its accepted evidence."),
      (40, "Mark each demo item: live, recorded evidence, or simulation only."),
      (20, "List gaps by requirement ID.")],
  calc="Requirements with accepted evidence / 50 Year 1.",
  chk=["Each requirement marked.", "Gaps listed.", "Saved."])

d(331, "Write the controlled demonstration run sheet",
  goal="Software, walking and handling as separate segments.",
  inp=[O(330), R + "tests/05_demonstration_script.md"],
  st=[(50, "Write segments A (companion), B (records/medication/communication), C (gait, no payload), D (handling, robot secured)."),
      (40, "For each: configuration ID, people, evidence channels, words you will say."),
      (20, "List transitions and who checks each.")],
  calc="4 segments.",
  chk=["Each segment has its configuration.", "Prerequisites met.", "Saved."])

d(332, "Reconfirm facility and qualified personnel",
  goal="People and place confirmed in writing.",
  inp=[O(331)],
  st=[(50, "Confirm the reviewer, stop operator, rigging inspection date, barriers and test recipient in writing."),
      (40, "Record what changed since the last trials."),
      (20, "Cancel any hazardous segment whose conditions changed.")],
  calc="Confirmations received / needed.",
  chk=["Written confirmations.", "Changes recorded.", "No public operation."],
  help="Everyone named on the run sheet. Get: written confirmation of date and role.")

d(333, "Review exact spoken claims and displays",
  goal="Every sentence in the demo is true.",
  inp=[O(331)],
  st=[(50, "Write the opening: 'This is a research prototype. The care data is fictional. The tether is part of the test.'"),
      (40, "Write the measured results you will state, each with its evidence ID."),
      (20, "Remove any medical, emergency or guarantee wording from screens and script.")],
  calc="Claims with evidence / claims.",
  chk=["Every claim cites evidence.", "Simulated labels visible.", "No prohibited wording."])

d(334, "Rehearse software and transitions without hazardous motion",
  goal="A smooth rehearsal with motion disabled.",
  inp=[O(331)],
  st=[(50, "Run segments A and B and walk through C and D transitions with the robot disabled."),
      (40, "Practise resets and how to explain a cancelled segment."),
      (20, "Time each segment.")],
  calc="Rehearsal time vs run sheet.",
  chk=["No energised combination used.", "Resets work.", "Times logged."],
  kind="software")

d(335, "Review the final test permit",
  goal="A signed permit for the exact demo.",
  inp=[O(331), O(332)],
  st=[(50, "Send the run sheet, evidence and setup to the reviewer."),
      (40, "Record the permitted scope; cancel anything outside it."),
      (20, "Get the signature.")],
  calc="—",
  chk=["Permit matches the run sheet.", "Signed.", "Cancelled items noted."],
  kind="review", help=PERMIT)

d(336, "Close readiness gaps or record partial scope",
  goal="The run sheet matches reality.",
  inp=[O(335)],
  st=[(50, "Fix the top readiness issue with the person responsible."),
      (40, "If it can't be fixed, rewrite the run sheet as a partial demo."),
      (20, "Keep unmet goals listed as unmet.")],
  calc="—",
  chk=["Run sheet truthful.", "No conditional claim.", "Recorded."])

# ---------------------------------------------------------------- Week 49 · S16
W(49)
d(337, "Confirm the final configuration and preflight",
  goal="Everything matches the signed run sheet.",
  inp=[O(335)],
  st=[(50, "Record hardware, software, model, limits and calibration references against the run sheet."),
      (40, "Run the stop, support, area, charge, temperature and privacy checks."),
      (20, "Cancel any segment that fails.")],
  calc="Checks passed / required.",
  chk=["Preflight passes or segment cancelled.", "Signed.", "Recorded."],
  kind="physical", help=STOPOP)

d(338, "Demonstrate companion and care records",
  goal="The software segment, exactly as scripted.",
  inp=[O(337)],
  st=[(50, "Run a game, a check-in, trends, a correction and a medication log."),
      (40, "Capture screens and logs."),
      (20, "Note any deviation as it happens.")],
  calc="Script steps completed / total.",
  chk=["Matches the script.", "Fictional data only.", "Logged."],
  kind="software")

d(339, "Demonstrate approved communication",
  goal="An approved send, shown honestly.",
  inp=[O(337)],
  st=[(50, "Preview, confirm and send the fictional summary."),
      (40, "Show receipt, review and the timeout behaviour."),
      (20, "Save the audit trail.")],
  calc="—",
  chk=["Backed by audit.", "Truthful states.", "Logged."],
  kind="software")

d(340, "Demonstrate only released tethered locomotion",
  goal="Show only the walking that was accepted.",
  inp=[O(294), O(337)],
  st=[(50, "If the permit includes live walking, run the accepted no-payload three-step sequence."),
      (40, "If not, play the accepted trial recordings and say they are recordings."),
      (20, "Log everything.")],
  calc="—",
  chk=["Accurately labelled.", "No new gait for show.", "Logged."],
  kind="powered", help=STOPOP)

d(341, "Demonstrate only released supported handling",
  goal="Show only the handling that was accepted.",
  inp=[O(308), O(337)],
  st=[(50, "With the robot secured, run the accepted 2 kg cycles or play the recording."),
      (40, "Confirm walking is disabled on screen."),
      (20, "Log everything.")],
  calc="—",
  chk=["Matches accepted evidence.", "No person assistance.", "Logged."],
  kind="powered", help=STOPOP)

d(342, "Export and reconcile demonstration evidence",
  goal="All demo evidence indexed.",
  inp=[O(338), O(339), O(340), O(341)],
  st=[(50, "Secure the robot; collect logs, messages, video and stop records."),
      (40, "Compare each segment with the run sheet."),
      (20, "List anything omitted or interrupted.")],
  calc="Segments completed / planned.",
  chk=["Every pass has a reference.", "Nothing missing silently.", "Indexed."])

d(343, "Review and disposition stage sixteen",
  goal="A real reviewer decision on the complete demonstration.",
  inp=[O(342)],
  st=[(50, "Send the evidence index to the independent reviewer."),
      (40, "Record their decision and limits."),
      (20, "Enter S16 on the Reviews page.")],
  calc="—",
  chk=["No substitute claimed.", "Recorded.", "Limits stated."],
  kind="review", help="An independent evidence reviewer. Get: signed disposition.")

# ---------------------------------------------------------------- Week 50 · closeout records
W(50)
d(344, "Audit every requirement evidence link",
  goal="Every PASS points to real evidence.",
  inp=[O(330), R + "requirements/requirements.csv"],
  st=[(60, "Check all 64 rows: evidence path, failures, missing runs."),
      (40, "Recompute SHA-256 for each evidence file and compare with the index."),
      (20, "Change any unsupported PASS to REWORK or BLOCKED.")],
  calc="64 rows.",
  chk=["Every PASS backed.", "Hashes valid.", "Changes logged."])

d(345, "Audit prohibited capability boundaries",
  goal="Show the excluded functions are absent.",
  inp=[O(344)],
  st=[(60, "Check UI, tools, motion interfaces, endpoints and wording for each of ASTRO-R-057 to 064."),
      (40, "Attach a denial test or inspection for each."),
      (20, "Fix any wording that slipped in.")],
  calc="8 excluded requirements.",
  chk=["Each has evidence.", "Wording clean.", "Saved."])

d(346, "Audit residual risk dispositions",
  goal="Risks reviewed by people with authority.",
  inp=[R + "risk_records/hazards.csv"],
  st=[(60, "Go through each hazard with the reviewers who signed permits."),
      (40, "Record verified controls and any residual risk they accept within their authority."),
      (20, "Leave unknown risks marked unknown.")],
  calc="Hazards reviewed / total.",
  chk=["No invented numbers.", "Authority recorded.", "Saved."],
  kind="review", help="The reviewers who signed stage permits.")

d(347, "Reconcile as built mass and COM evidence",
  goal="Final measured mass with its configuration.",
  inp=[O(256), O(312)],
  st=[(60, "Weigh the full Y1-WALK configuration on a calibrated scale."),
      (40, "Separate measured from estimated items."),
      (20, "Apply the 55 / 65 kg rules.")],
  calc="Measured total vs 55 kg.",
  chk=["Configuration named.", "Measured vs estimated labelled.", "Rules applied."],
  kind="physical")

d(348, "Reconcile actual cash spending",
  goal="Every dollar accounted for.",
  inp=[O(190), O(193)],
  st=[(60, "Match receipts to BOM lines including shipping, tax and services."),
      (40, "Separate cash spent, commitments and donated items."),
      (20, "Compare with the D-01 ceiling.")],
  calc="Σ actual vs ceiling.",
  chk=["Reconciled.", "Nothing hidden.", "Changes authorised."])

d(349, "Audit reproducibility and evidence retention",
  goal="Someone else can find the evidence without you.",
  inp=[O(342)],
  st=[(60, "Ask a reviewer to find one software, simulation, gait and handling record from the index."),
      (40, "Check each has setup, revision, calibration and raw data."),
      (20, "List gaps they hit.")],
  calc="4 lookups; time each.",
  chk=["Found without help.", "Gaps listed.", "Recorded."],
  help="Any earlier reviewer for 30 minutes.")

d(350, "Prepare the G8 release review packet",
  goal="A packet for a controlled research release only.",
  inp=[O(344), O(345), O(346), O(347), O(348), O(349)],
  st=[(60, "Assemble requirements, risks, verification, as-built, spend and evidence."),
      (40, "Put unmet goals on the first page."),
      (20, "State the scope: controlled research use only.")],
  calc="—",
  chk=["Scope stated.", "Gaps up front.", "Indexed."])

# ---------------------------------------------------------------- Week 51 · buffer
W(51)
d(351, "Select one evidence based priority",
  goal="Pick the single most important open gap.",
  inp=[O(350)],
  st=[(50, "Rank open items by safety, data integrity, then year-one goal impact."),
      (40, "Pick one; write the deliverable, who helps, the release needed and the test."),
      (20, "Schedule it in Days 352–355.")],
  calc="—",
  chk=["A real gap chosen.", "Deliverable defined.", "Scheduled."])

d(352, "Resolve a documentation or software gap",
  goal="Close one no-power defect.",
  inp=[O(351)],
  st=[(60, "Fix the chosen software or documentation defect."),
      (40, "Rerun its test and save the new evidence."),
      (20, "Keep the old failure in the index.")],
  calc="—",
  chk=["Closed only if the test passes.", "Evidence saved.", "Old failure kept."],
  kind="software")

d(353, "Resolve a model or calculation gap",
  goal="Reconcile one engineering discrepancy.",
  inp=[O(351)],
  st=[(60, "Fix one mass, load, thermal or simulation discrepancy with traced inputs."),
      (40, "Ask the reviewer if it affects safety."),
      (20, "Label it analysis, not a hardware result.")],
  calc="—",
  chk=["Traced inputs.", "Review asked if needed.", "Labelled."])

d(354, "Coordinate a qualified dependency",
  goal="Get one missing review, reply or decision.",
  inp=[O(351)],
  st=[(60, "Contact the person or vendor who owns the missing item."),
      (40, "Record their reply or 'no reply' with the date."),
      (20, "Write the schedule or cost effect.")],
  calc="—",
  chk=["Unavailable stays unavailable.", "Recorded.", "Effect noted."],
  help="Whoever owns the missing item.")

d(355, "Retest only an already released scope",
  goal="Run a real permitted retest, or review its protocol.",
  inp=[O(351)],
  st=[(60, "If a retest is permitted and booked, run exactly that scope."),
      (40, "If not, review the protocol at your desk and list what is missing."),
      (20, "Record the outcome.")],
  calc="—",
  chk=["Current permit evidenced if run.", "Logged.", "No permit bypass."],
  kind="powered", help=STOPOP)

d(356, "Assess the honest year end outcome",
  goal="Achieved, partial or unmet for each goal.",
  inp=[O(330), O(350)],
  st=[(60, "Classify the six demonstrations: achieved / partial / unmet, each with evidence."),
      (40, "Estimate the remaining work in hours and cost."),
      (20, "Write it in plain words.")],
  calc="Goals achieved / 6.",
  chk=["Each goal classified.", "Reasons given.", "No effort-based claims."])

d(357, "Review buffer use with Faisal",
  goal="Freeze the closeout scope.",
  inp=[O(351), O(356)],
  st=[(50, "Review what closed and what remains blocked."),
      (40, "Decide on any funding or schedule change."),
      (30, "Confirm later-scope items stay later; " + BACKUP[0].lower() + BACKUP[1:])],
  calc="—",
  chk=["Scope frozen.", "Decisions recorded.", "No new features added."])

# ---------------------------------------------------------------- Week 52 · archive
W(52)
d(358, "Freeze the candidate release inventory",
  goal="List everything that goes in the archive.",
  inp=[O(350)],
  st=[(60, "List requirements, CAD, software, model, BOM, procedures, permits, calibration and logs with paths."),
      (40, "Mark missing items."),
      (20, "Name the revision being archived.")],
  calc="Items listed / expected.",
  chk=["Every item has a path or 'missing'.", "Revision named.", "Saved."])

d(359, "Create the immutable planning and evidence snapshot",
  goal="A hashed archive with failures included.",
  inp=[O(358)],
  st=[(60, "Copy the release into release_archive/R1_0/ and run `shasum -a 256` on every file into a manifest."),
      (40, "Check nothing contains passwords, API keys or real personal data."),
      (20, "Keep working copies separate.")],
  calc="File count = manifest lines.",
  chk=["Hashes reconcile.", "No secrets.", "Failures included."])

d(360, "Conduct the G8 independent release review",
  goal="A real G8 decision, or a pending status.",
  inp=[O(359)],
  st=[(60, "Present the evidence and unmet goals to the independent reviewer."),
      (40, "Record their scope, date and decision."),
      (20, "If no review happens, record G8 pending.")],
  calc="—",
  chk=["Not called certification.", "Recorded.", "Truthful."],
  kind="review", help="An independent evidence reviewer. Get: signed G8 decision.")

d(361, "Write operation maintenance and storage notes",
  goal="Instructions that match the real robot.",
  inp=[O(360)],
  st=[(60, "Write isolation, support, charging, cleaning, inspection and storage steps."),
      (40, "If the robot was not accepted, write a 'do not operate' notice instead."),
      (20, "Get the reviewer's approval.")],
  calc="—",
  chk=["Matches the configuration.", "No unsupervised use.", "Approved."])

d(362, "Write the future phase comparison",
  goal="Compare next-phase options with their costs and reviews.",
  inp=[O(356), PHOTO],
  st=[(60, "Compare: articulated hands (as in the photo), powered arms, hip yaw for turning (12 joints), a cart, a cargo drawer, 5 kg handling."),
      (40, "For each, list reviews needed and a rough cost."),
      (20, "Mark them as options, not plans.")],
  calc="Options × (cost, reviews).",
  chk=["Prerequisites explicit.", "Costs estimated.", "Current release not expanded."])

d(363, "Rehearse recovery from the archive",
  goal="Prove the archive works.",
  inp=[O(359)],
  st=[(60, "In a clean folder, restore the software and replay one simulation case from the archive."),
      (40, "Check tools and versions are documented."),
      (20, "Record gaps.")],
  calc="—",
  chk=["Usable by another person.", "Gaps recorded.", "Logged."],
  kind="software")

d(364, "Prepare the owner year end decision",
  goal="A summary ready for the Day 365 decision.",
  inp=[O(356), O(347), O(348), O(360)],
  st=[(60, "Summarise achieved and unmet goals, mass, spend and risks on one page."),
      (40, "Lay out options: keep scope, extend for named blockers, or start a reviewed next phase."),
      (20, "Leave the decision itself for Day 365.")],
  calc="—",
  chk=["Evidence-based.", "Options clear.", "Ready."])

# ---------------------------------------------------------------- Week 53
W(53)
d(365, "Close the year with an honest owner decision",
  goal="Record the real year-one outcome and the next step.",
  inp=[O(364), O(360) + " or explicit pending status"],
  st=[(30, "Open the requirement matrix, final budget and mass report. List each Year 1 outcome as accepted, partial or unmet, with evidence."),
      (35, "State whether both three-step trials, the speed target, the 2 kg ten-repetition task and the fictional caregiver demo were accepted."),
      (30, "Decide: keep scope, extend for named blockers, or start a separately reviewed next phase."),
      (15, "Save release_archive/day_365_owner_closeout.md and export a website backup and the final archive.")],
  calc="Owner hours = sum of recorded daily hours.",
  chk=["Every outcome backed by evidence or marked unmet.", "Decision recorded only if it happened.", "Archive recoverable."])
