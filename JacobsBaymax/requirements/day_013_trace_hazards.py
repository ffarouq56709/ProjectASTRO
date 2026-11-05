"""Rebuild the Day 13 document audit; --check verifies saved outputs without writes.

Run from any directory with Python 3. No robot, simulator or verification
protocol is executed. R0.1 inputs and the Day 10 source remain unchanged.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-04"
OWNER = "Faisal Farouq"
INPUTS = ["risk_records/hazards.csv", "tests/verification_matrix.csv",
          "requirements/requirements.csv", "requirements/day_010_motion_payload_hazards.csv",
          "revision_history/gates.csv"]

# Planning holds against the existing gate definitions, not reviewer acceptance.
GATES = {
    1: "G2 G3 G4 G5 G6 G7 G8", 2: "G2 G3 G4 G5 G6 G7 G8",
    3: "G2 G3 G4 G5 G6 G7 G8", 4: "G2 G3 G4 G5 G6 G7 G8",
    5: "G2 G3 G4 G7 G8", 6: "G1 G8", 7: "G1 G8", 8: "G1 G8",
    9: "G1 G8", 10: "G1 G8", 11: "G2 G6 G7 G8",
    12: "G1 G2 G5 G6 G7 G8", 13: "G7 G8",
    14: "G2 G3 G4 G5 G6 G7 G8", 15: "G1 G2 G3 G4 G5 G6 G7 G8",
    16: "G1 G8", 17: "G2 G3 G4 G5 G6 G7 G8",
    18: "G2 G3 G4 G5 G6 G7 G8", 19: "G5 G6 G7 G8",
    20: "G2 G5 G6 G7 G8",
}
NEW_GATES = [
    "G2 G4 G5 G6 G7 G8", "G2 G4 G5 G6 G7 G8", "G2 G4 G5 G6 G7 G8",
    "G2 G5 G6 G7 G8", "G2 G5 G6 G7 G8", "G2 G3 G4 G5 G6 G7 G8",
    "G2 G4 G5 G6 G7 G8", "G2 G4 G5 G6 G7 G8", "G2 G4 G5 G6 G7 G8",
    "G2 G3 G4 G7 G8", "G2 G3 G4 G7 G8", "G2 G3 G4 G7 G8",
    "G2 G3 G4 G7 G8", "G2 G5 G6 G7 G8", "G2 G5 G6 G7 G8",
]
SUPPLEMENT = {
    "JB-V-06": "Include foot landing and swing strike exclusion, spectator barriers, and the supported/walking configurations identified on Day 10.",
    "JB-V-07": "Include knee/ankle/hip and shell sweeps, shoulder-pin retention and arm-drop inspection, and full-range cable routing. Guard/gap and retention acceptance require a qualified reviewer; Day 10 numbers are unverified screens.",
    "JB-V-08": "Include cable/sensor disconnect or stale input and power-off handling load retention on the approved restrained fixture. Fault timing and retained-load criteria require reviewer approval.",
    "JB-V-09": "Include direct and reduced-drive speed limits and handling travel/force limits; missing or invalid limits inhibit enable. No Day 10 screen becomes an approved limit.",
    "JB-V-22": "Include separate-stand overturning and anchoring review, tray capture/catch coverage, pinch protection, and power-off brake/holding verification before the loaded repetitions. Reviewer must set load cases and margins.",
    "JB-V-23": "Include payload-present, docked-to-stand and support-present cases; reject gait while loaded or docked and reject handling without secured support. Use inert fixtures/command simulation for person-support refusals.",
    "JB-V-25": "Include no-contact briefing, captive shoulder-pin preflight, barrier and stop-operator checks before each relevant motion stage.",
}


def read(name):
    with (ROOT / name).open(newline="") as f:
        return list(csv.DictReader(f))


def ids(value):
    return set(filter(None, value.split(";")))


def joined(values):
    return ";".join(sorted(values))


def csv_text(rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def build():
    original_h, original_v, original_r, motion, gates = map(read, INPUTS)
    assert len(original_h) == 20 and len(original_v) == 26 and len(original_r) == 64
    assert [m["ID"] for m in motion] == [f"MP-{i:02}" for i in range(1, 16)]
    hazards = {r["Hazard ID"]: dict(r) for r in original_h}
    tests = {r["Verification ID"]: dict(r) for r in original_v}
    reqs = {r["Requirement ID"]: dict(r) for r in original_r}
    assert len(hazards) == 20 and len(tests) == 26 and len(reqs) == 64
    known_gates = {g["Gate"] for g in gates}
    changes = []

    for i, m in enumerate(motion, 21):
        hid = f"JB-H-{i:02}"
        hazards[hid] = {
            "Hazard ID": hid, "Hazard or ethical issue": m["Hazard"],
            "Credible harm": "Injury from " + m["Hazard"].lower(),
            "Severity 1-4": "UNASSESSED", "Release priority": "P0",
            "Context": m["Where / joint"] + ": " + m["How it happens"],
            "Controls": m["Control idea"], "Requirement IDs": m["Requirements"],
            "Verification IDs": m["Verification"],
            "Specialist reviewer": m["Reviewer role"] + " reviewer unassigned",
            "Likelihood": "UNASSESSED", "Residual risk": "UNASSESSED",
            "Acceptance": "NOT RECORDED", "Accountable owner": OWNER,
            "Revision": "R0.3", "Date": DATE,
        }

    # Preserve every declared edge and reconcile its inverse. Existence is
    # checked before closure, so a typo cannot be silently repaired away.
    hr, hv, rv = set(), set(), set()
    for h, row in hazards.items():
        for r in ids(row["Requirement IDs"]):
            assert r in reqs, (h, r)
            hr.add((h, r))
        for v in ids(row["Verification IDs"]):
            assert v in tests, (h, v)
            hv.add((h, v))
    for r, row in reqs.items():
        for h in ids(row["Hazard IDs"]):
            assert h in hazards, (r, h)
            hr.add((h, r))
        for v in ids(row["Verification ID"]):
            assert v in tests, (r, v)
            rv.add((r, v))
    for v, row in tests.items():
        for r in ids(row["Requirement IDs"]):
            assert r in reqs, (v, r)
            rv.add((r, v))

    direct_hv = set(hv)
    # Include the tests assigned to each linked requirement as supporting
    # evidence. This is a traceability relation, not a claim of full coverage.
    hv.update((h, v) for h, r in hr for rr, v in rv if r == rr)
    for h, row in hazards.items():
        n = int(h.rsplit("-", 1)[1])
        row["Requirement IDs"] = joined(r for hh, r in hr if hh == h)
        row["Verification IDs"] = joined(v for hh, v in hv if hh == h)
        row["Revision"], row["Date"] = "R0.3", DATE
        row["Source scenario"] = f"MP-{n - 20:02}" if n > 20 else "R0.1 " + h
        row["Parent hazard IDs"] = motion[n - 21]["Existing hazard"] if n > 20 else ""
        row["blocks gate"] = ";".join((NEW_GATES[n - 21] if n > 20 else GATES[n]).split())
        assert ids(row["blocks gate"]) <= known_gates and "G0" not in ids(row["blocks gate"])
        row["Gate hold basis"] = "Open hazard: applicable evidence/disposition required before the listed release; does not close an already accepted G0 documentation gate."
        row["Priority basis"] = "Conservative P0 planning hold; severity/risk assessment pending" if n > 20 else "Inherited R0.1 release priority; risk assessment pending"
        row["Screen status"] = "Day 10 controls and numbers unverified; reviewer must approve criteria" if n > 20 else "Controls unverified; no acceptance recorded"
    for r, row in reqs.items():
        row["Hazard IDs"] = joined(h for h, rr in hr if rr == r)
        row["Verification ID"] = joined(v for rr, v in rv if rr == r)
        row["Revision"], row["Date"] = "R0.3", DATE
    for v, row in tests.items():
        row["Requirement IDs"] = joined(r for r, vv in rv if vv == v)
        row["Hazard IDs"] = joined(h for h, vv in hv if vv == v)
        row["Day 13 coverage to implement"] = SUPPLEMENT.get(v, "Existing method retained; no execution or acceptance recorded.")
        row["Revision"], row["Date"] = "R0.3", DATE

    for kind, originals, working, key, fields in [
        ("hazard", original_h, hazards, "Hazard ID", ["Requirement IDs", "Verification IDs"]),
        ("requirement", original_r, reqs, "Requirement ID", ["Hazard IDs", "Verification ID"]),
        ("verification", original_v, tests, "Verification ID", ["Requirement IDs"]),
    ]:
        for old in originals:
            for field in fields:
                new = working[old[key]][field]
                if ids(old[field]) != ids(new):
                    changes.append({"Register": kind, "ID": old[key], "Field": field,
                                    "Before": old[field], "After": new,
                                    "Reason": "Preserve declared links and add missing reverse/supporting links"})

    trace = []
    for h, row in hazards.items():
        assert row["Likelihood"] == row["Residual risk"] == "UNASSESSED"
        assert row["Release priority"] != "P0" or row["blocks gate"]
        assert all(h in ids(reqs[r]["Hazard IDs"]) for r in ids(row["Requirement IDs"]))
        assert all(h in ids(tests[v]["Hazard IDs"]) for v in ids(row["Verification IDs"]))
        trace.append({"Hazard ID": h, "Hazard": row["Hazard or ethical issue"],
                      "Source scenario": row["Source scenario"], "Parent hazard IDs": row["Parent hazard IDs"],
                      "Release priority": row["Release priority"], "Requirement IDs": row["Requirement IDs"],
                      "Verification IDs": row["Verification IDs"],
                      "Direct scenario/baseline verification IDs": joined(v for hh, v in direct_hv if hh == h),
                      "blocks gate": row["blocks gate"], "ID existence check": "PASS",
                      "Requirement reverse-link check": "PASS", "Verification reverse-link check": "PASS",
                      "Likelihood": "UNASSESSED", "Residual risk": "UNASSESSED",
                      "Engineering acceptance": "NOT RECORDED - all linked protocols unexecuted",
                      "Audit result": "PASS - document links only"})
    for r, row in reqs.items():
        assert all(r in ids(hazards[h]["Requirement IDs"]) for h in ids(row["Hazard IDs"]))
        assert all(r in ids(tests[v]["Requirement IDs"]) for v in ids(row["Verification ID"]))
    for v, row in tests.items():
        assert row["Result"] == "BLOCKED" and row["Evidence"] == "NONE - NOT EXECUTED"
        assert all(v in ids(hazards[h]["Verification IDs"]) for h in ids(row["Hazard IDs"]))
        assert all(v in ids(reqs[r]["Verification ID"]) for r in ids(row["Requirement IDs"]))

    outputs = {
        "risk_records/hazards_R0_3.csv": csv_text(list(hazards.values())),
        "tests/verification_matrix_R0_3.csv": csv_text(list(tests.values())),
        "requirements/requirements_R0_3.csv": csv_text(list(reqs.values())),
        "requirements/day_013_hazard_traceability.csv": csv_text(trace),
        "requirements/day_013_link_changes.csv": csv_text(changes),
    }
    evidence = {
        "day": 13, "date": DATE, "owner": OWNER,
        "result": "PASS (desk work: hazard-to-test traceability only)",
        "counts": {"baseline_hazards": 20, "day_10_scenarios": 15, "working_hazards": len(hazards),
                   "requirements": len(reqs), "verification_protocols": len(tests),
                   "hazard_requirement_pairs": len(hr), "hazard_verification_pairs": len(hv),
                   "requirement_verification_pairs": len(rv),
                   "direct_hazard_verification_pairs": len(direct_hv),
                   "directed_hazard_links_checked": 2 * (len(hr) + len(hv)),
                   "changed_baseline_link_fields": len(changes),
                   "P0_hazards_with_gate_holds": sum(r["Release priority"] == "P0" for r in hazards.values()),
                   "missing_IDs": 0, "missing_reverse_links": 0},
        "permanent_ID_mapping": {m["ID"]: f"JB-H-{i:02}" for i, m in enumerate(motion, 21)},
        "checks": {"all_linked_IDs_exist": "PASS", "bidirectional_hazard_links": "PASS",
                   "bidirectional_requirement_test_links": "PASS", "every_P0_names_blocked_gates": "PASS",
                   "likelihood_and_residual_risk_unassessed": "PASS", "all_26_protocols_remain_unexecuted": "PASS"},
        "limitations": [
            "New scenarios have conservative P0 planning priority; severity, likelihood and residual risk are UNASSESSED.",
            "Reverse/supporting links establish traceability, not adequacy or successful execution of a protocol.",
            "Day 10 numeric screens and control ideas are retained as unverified source text, not approved design criteria.",
            "Coverage additions identify work for qualified reviewers; no specialist review or gate release is claimed.",
            "Day 14 must reconcile the USD 10,000 wording in baseline requirements/tests/gates and Day 12 assumptions with decided D-01 USD 15,000; D-07 and D-10 remain proposed.",
        ],
        "robot_tests_executed": 0, "simulation_runs_executed": 0,
        "verification_protocols_executed": 0, "purchases_authorized": 0, "gates_released": [],
        "owner_hours": 2, "hours_basis": "Explicit owner instruction: Do day 13, log 2 hours",
        "preparer_role": "Codex - AI documentation assistant; not an independent engineering or safety reviewer",
        "inputs_sha256": {name: digest((ROOT / name).read_bytes()) for name in INPUTS},
        "audit_script_sha256": digest(Path(__file__).read_bytes()),
        "outputs_sha256": {name: digest(content.encode()) for name, content in outputs.items()},
        "progress_backup": "../Website/Baymax_365_Progress_Days_001-013.json",
        "progress_backup_sha256": digest((ROOT.parent / "Website/Baymax_365_Progress_Days_001-013.json").read_bytes()),
        "summary_sha256": digest((ROOT / "requirements/day_013_hazard_traceability.md").read_bytes()),
    }
    outputs["evidence/day_013_hazard_traceability_review.json"] = json.dumps(evidence, indent=2) + "\n"
    return outputs, evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs, evidence = build()
    for name, content in outputs.items():
        path = ROOT / name
        if args.check:
            assert path.read_bytes() == content.encode(), f"Stale or missing output: {name}"
        else:
            path.write_text(content)
    print(json.dumps({"mode": "check" if args.check else "build", "result": evidence["result"],
                      "counts": evidence["counts"]}, indent=2))


if __name__ == "__main__":
    main()
