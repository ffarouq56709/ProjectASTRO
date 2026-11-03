"""Build dist/plan.json and the 365-day CSV for Baymax 365 R0.3.

python3 build_plan.py
"""
import csv
import json
from pathlib import Path

import plan_model as pm
import plan_w01_06, plan_w07_12, plan_w13_20, plan_w21_30, plan_w31_42, plan_w43_53  # noqa: F401

ROOT = Path(__file__).resolve().parent
OLD = pm.OLD
base = json.loads((ROOT / "source_baseline.json").read_text())

assert sorted(pm.DAYS) == list(range(1, 366)), [n for n in range(1, 366) if n not in pm.DAYS]

STOP = {
    "Foundation": "Stop if the work needs real patient data, clinical authority, spending or powered motion.",
    "Software": "Stop if a test would use real personal data, send to an unapproved recipient, or give clinical or dosing advice.",
    "Engineering": "Stop before any order or fabrication. Calculations here authorise nothing physical.",
    "Simulation": "Stop a success claim if it relies on a hidden fixed base, unlimited torque, missing logs or tether pulling.",
    "Procurement": "Stop before paying unless G3 and your written spending approval cover the exact line.",
    "Fabrication": "Stop if a drawing is unreleased, a material is substituted or an inspection fails.",
    "Hardware": "Stop at any trip, unexpected motion, person in the fall zone, or missing permit, limits file or stop operator.",
    "Handling": "Stop for any release of the object, interference, limit trip, or walking enable with the payload on.",
    "Enclosure": "Stop for interference, an exposed moving gap, blocked stop or vent, or mass over 55 kg.",
    "Integration": "Stop for privacy or clinical-boundary failures, or anything that could move the robot without a permit.",
    "Closeout": "Stop any release claim with missing evidence or a failed criterion.",
    "Buffer": "A buffer day never replaces a permit, a review or a failed test.",
}
ALT = {
    "Procurement": ["List the unanswered quote fields for this package.", "Update the cost/technical comparison with replies you have.", "Record the missing approval and the next follow-up date. Spend nothing."],
    "Fabrication": ["Mark every unreleased or substituted interface on the drawing.", "Write the reviewer questions and inspection hold points.", "Save a drawing-rework list. Fabricate nothing."],
    "Hardware": ["Open the protocol and existing logs for this stage. Keep power off.", "Compare required signals, calibration, limits and support with what you actually have.", "Write the missing permit, review or equipment items and who can supply each."],
    "Handling": ["Recalculate the 2 kg load case with current reach and tray mass.", "Audit retention, stand and interlock evidence.", "List missing reviews; keep the object off and power off."],
    "Enclosure": ["Check this clearance issue in CAD only.", "Compare panel masses and earlier temperature logs with the accepted configuration.", "Save an annotated rework drawing."],
    "Integration": ["Run the fictional workflow on the laptop instead.", "Check preview, consent and gateway denials for this scenario.", "Save software-only evidence and mark the physical part untested."],
}
ALT_DEFAULT = ["List what is missing for today's task.", "Do only the safe, reversible part with inputs you have.", "Record the blocker, who can unblock it and the follow-up date."]

FILE_RECORDS = {
    1: ("PASS", "Mission accepted; charter differences resolved 2026-10-28", "JacobsBaymax/requirements/day_001_mission_acceptance.md"),
    2: ("PASS", "Folder and archive setup only", "JacobsBaymax/evidence/day_002_folder_setup.json"),
    3: ("PASS", "Checklist coverage only", "JacobsBaymax/evidence/day_003_checklist_review.json"),
    4: ("PASS", "List completeness only; six specialist roles unassigned", "JacobsBaymax/evidence/day_004_responsibility_review.json"),
    5: ("PASS", "Arithmetic and options document only; ceiling undecided", "JacobsBaymax/evidence/day_005_budget_review.json"),
    6: ("PASS", "Configuration document; owner accepted 2026-10-28; G2 not released", "JacobsBaymax/evidence/day_006_configuration_review_R0_3.json"),
    7: ("PASS", "G0 released 2026-10-28 for documentation, software and analysis only", "JacobsBaymax/requirements/day_007_G0_baseline_review.md"),
    8: ("PASS", "Requirement audit: 64 rows, links consistent, 9 wording issues for Day 14", "JacobsBaymax/requirements/day_008_requirement_audit.csv"),
    9: ("PASS", "Fall hazard questions and envelope sketch; no ratings approved", "JacobsBaymax/requirements/day_009_fall_hazard_questions.md"),
}

HW_PHASES = {"Hardware", "Handling", "Enclosure", "Integration"}

days = []
for n in range(1, 366):
    o = pm.OLD_DAYS[n]
    x = pm.DAYS[n]
    rec = dict(
        id=n, week=o["week"], weekDay=o["weekDay"], title=x["title"], weekTitle=o["weekTitle"],
        phase=o["phase"], kind=x["kind"], mode=pm.KINDS[x["kind"]], minutes=x["minutes"],
        goal=x["goal"], objective=x["goal"], inputs=x["inputs"], steps=x["steps"], stepMinutes=x["stepMinutes"],
        acceptance=x["acceptance"], calculation=x["calculation"], output=x["output"],
        extraOutputs=x["extraOutputs"], help=x["help"], note=x["note"],
        stop=x["stop"] or STOP[o["phase"]], gates=o["gates"], stages=o["stages"],
        requirements=x["requirements"] or o["requirements"],
        alternative=ALT.get(o["phase"], ALT_DEFAULT), alternativeOutput=o["alternativeOutput"],
        dependencyDays=pm.deps(x),
        hardwareRecord=(x["kind"] in ("physical", "powered")),
    )
    if n in FILE_RECORDS:
        r, scope, ev = FILE_RECORDS[n]
        rec["fileRecord"] = dict(result=r, scope=scope, evidence=ev)
    days.append(rec)

for i, d in enumerate(days):
    d["next"] = f"Day {i+2:03d}: {days[i+1]['title']}" if i < 364 else "The next scope you and your reviewers actually approve."

assert len({d["output"] for d in days}) == 365
assert len({d["title"] for d in days}) == 365
assert all(sum(d["stepMinutes"]) == d["minutes"] for d in days)

hours = round(sum(d["minutes"] for d in days) / 60, 1)
meta = dict(OLD["meta"])
meta.update(revision="R0.3", date="2026-10-28", previousRevision="R0.2", ownerHours=hours,
            cashCap=10000, cashScenario=15000, ceilingStatus="Final ceiling undecided (D-01)",
            note="Planned dates, task records and hardware results are kept separately. Progress stays in this browser; export backups.",
            costReferences={"B-01": {"forecast": 3481, "basis": "R0.3 listing screen: 10 x USD 319 + 4 stages x USD 50 (assumed) + USD 91.25 CAN hub. Listings 2026-10-28, not quotes. Low case USD 2,841.", "r01Reference": 8899}},
            appearanceReference="JacobsBaymax/cad_specifications/reference/baymax-rigid-panel-concept-v1.png")

data = dict(OLD)
data.update(meta=meta, days=days)
data["kinds"] = pm.KINDS
(ROOT / "dist/plan.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))

with (ROOT / "dist/resources/Baymax_365_Daily_Plan.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Day", "Week", "Phase", "Work type", "Title", "Goal", "Planned minutes", "Inputs", "Steps",
                "Calculation or measurement", "Output", "Extra outputs", "Completion checks", "Outside help",
                "Gates", "Prior stages", "Depends on days", "Project file record", "Revision"])
    for d in days:
        fr = d.get("fileRecord")
        w.writerow([d["id"], d["week"], d["phase"], d["mode"], d["title"], d["goal"], d["minutes"],
                    "\n".join(d["inputs"]),
                    "\n".join(f"{i+1}. ({m} min) {s}" for i, (m, s) in enumerate(zip(d["stepMinutes"], d["steps"]))),
                    d["calculation"], d["output"], "\n".join(d["extraOutputs"]), "\n".join(d["acceptance"]),
                    d["help"] or "", ",".join(d["gates"]), ",".join(d["stages"]),
                    ",".join(map(str, d["dependencyDays"])), f"{fr['result']}: {fr['scope']}" if fr else "", "R0.3"])

print(json.dumps(dict(days=len(days), owner_hours=hours,
                      steps=sum(len(d["steps"]) for d in days),
                      hardware_record_days=sum(d["hardwareRecord"] for d in days),
                      help_days=sum(bool(d["help"]) for d in days),
                      min_minutes=min(d["minutes"] for d in days), max_minutes=max(d["minutes"] for d in days))))
