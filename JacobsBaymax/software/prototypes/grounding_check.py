"""Grounding check prototype (R0.3, 2026-11-04). Fictional data only.

Every sentence the robot shows or sends must be backed by the records it cites.
The checker rejects a sentence that adds a number, time, unit, medicine name,
quotation or judgment that the cited records do not contain. A rejected draft
is replaced by the template wording; it is never "fixed up" by a model.

python3 grounding_check.py            # runs the SIM-002 test set, writes results CSV
"""
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE.parents[1] / "simulated_patient_data" / "fictional_fixture_SIM-002.json"
STALE_HOURS = 6  # ASSUMPTION: owner/care-team setting, not a clinical value

# Words that judge, diagnose, advise or promise. A summary states records; it never says these.
FORBIDDEN = [
    r"diagnos", r"hypo", r"hyper", r"neuropath", r"low (blood )?sugar", r"high (blood )?sugar",
    r"\bnormal\b", r"\bdanger", r"\bsafe\b", r"\bstable\b", r"\bimprov", r"\bworse", r"\bfine\b",
    r"\benough\b", r"\bshould\b", r"\bdose", r"\bdouble\b", r"on the way", r"is coming",
    r"help has been", r"ambulance", r"administered", r"confirmed taken", r"\bemergency\b",
]
ATTRIB = re.compile(r"\b(said|says|reported|told|answered)\b", re.I)
TIME = re.compile(r"\b\d{1,2}:\d{2}\b")
NUM = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])")
UNITS = re.compile(r"1/min")  # units that contain digits are not values
MED = re.compile(r"Demo Medication [A-Z]")
QUOTE = re.compile(r"[\"“]([^\"”]+)[\"”]")


def _t(s):
    return datetime.fromisoformat(s) if s else None


def _num(v):
    return ("%g" % v) if isinstance(v, (int, float)) else None


def index(fx):
    """record id -> dict(kind, facts, units, rec)."""
    idx = {}

    def add(rid, kind, rec, nums=(), units=(), times=(), names=(), date=None):
        facts = {x for x in nums if x} | {t.strftime("%H:%M") for t in times if t} | set(names)
        if date:
            facts.add(str(date.day))
        idx[rid] = dict(kind=kind, rec=rec, facts=facts, units=dict(units))

    for o in fx["observations"]:
        t = _t(o["observed_at"])
        v = _num(o["value"])
        add(o["id"], "observation", o, [v], [(v, o["unit"])] if v else [], [t], [], t)
    for s in fx["patient_statements"]:
        t = _t(s["said_at"])
        add(s["id"], "statement", s, NUM.findall(s["verbatim"]), [], [t], MED.findall(s["verbatim"]), t)
    for e in fx["interaction_events"]:
        t = _t(e["at"]); r = _t(e.get("response_at"))
        names = [m["name"] for m in fx["medications"] if m["id"] == e["ref"]]
        add(e["id"], "event", e, NUM.findall(str(e.get("response", ""))), [], [t, r], names, t)
    for m in fx["medications"]:
        add(m["id"], "medication", m, [], [], [datetime.strptime(x, "%H:%M") for x in m["schedule"]], [m["name"]])
    for p in fx["profiles"]:
        for r in p["care_team_notify_values"]:
            vals = [_num(r.get("notify_below")), _num(r.get("notify_above"))]
            add(r["id"], "rule", r, vals, [(v, r["unit"]) for v in vals if v])
    for m in fx["messages"]:
        t = _t(m.get("received_at"))
        add(m["id"], "message", m, [], [], [t, _t(m.get("reviewed_at"))], [], t)
    return idx


def check(sentence, cites, idx, report_time):
    """Return a list of rule failures for one sentence. Empty list = grounded."""
    text = sentence
    fails = []
    low = text.lower()
    for pat in FORBIDDEN:
        if re.search(pat, low):
            fails.append(f"R4 judgment/advice/promise word: /{pat}/")
    recs = [idx.get(c) for c in cites]
    if any(r is None for r in recs):
        fails.append("R1 cites a record that does not exist")
        recs = [r for r in recs if r]
    times = TIME.findall(text)
    nums = NUM.findall(UNITS.sub(" ", TIME.sub(" ", text)))
    meds = MED.findall(text)
    if not recs and (times or nums or meds or ATTRIB.search(text)):
        return fails + ["R1 states a fact with no citation"]
    facts = set().union(*[r["facts"] for r in recs]) if recs else set()
    units = {}
    for r in recs:
        units.update(r["units"])
    # derived numbers allowed: age in hours of cited observations
    for r in recs:
        if r["kind"] == "observation":
            age = (report_time - _t(r["rec"]["observed_at"])).total_seconds() / 3600
            facts.add(str(int(age)))
    for t in times:
        if t.zfill(5) not in facts:
            fails.append(f"R2 time {t} not in cited records")
    for n in nums:
        if n not in facts:
            fails.append(f"R2 number {n} not in cited records")
        elif n in units and not re.search(re.escape(n) + r"\s*" + re.escape(units[n]), text):
            fails.append(f"R2 number {n} missing or wrong unit (record unit {units[n]})")
    for m in meds:
        if m not in facts:
            fails.append(f"R3 medicine name '{m}' not in cited records")
    for r in recs:
        rec = r["rec"]
        if r["kind"] == "statement":
            if not ATTRIB.search(text):
                fails.append(f"R5 patient statement {rec['id']} written as fact (no 'said/reported')")
            for q in QUOTE.findall(text):
                if q.strip().lower().rstrip(".") not in rec["verbatim"].lower():
                    fails.append(f"R5 quote not verbatim from {rec['id']}")
            if not rec.get("confirmed"):
                fails.append(f"R5 statement {rec['id']} not read back and confirmed")
        if r["kind"] == "observation":
            obs_t = _t(rec["observed_at"])
            if obs_t.strftime("%H:%M") not in times:
                fails.append(f"R6 reading {rec['id']} shown without its observed time")
            if (report_time - obs_t).total_seconds() / 3600 > STALE_HOURS and " old" not in low:
                fails.append(f"R6 reading {rec['id']} older than {STALE_HOURS} h but not marked old")
            if rec["value"] is None:
                if "no reading" not in low:
                    fails.append(f"R7 missing reading {rec['id']} not stated as 'no reading'")
                if [n for n in nums if n in units] or re.search(r"mg/dl|1/min|degc", low):
                    fails.append(f"R7 value given for missing reading {rec['id']}")
        if r["kind"] == "event" and re.search(r"\btaken\b|\btook\b", low):
            if rec.get("response") != "taken" or not ATTRIB.search(text):
                fails.append(f"R8 'taken' claimed but event {rec['id']} response is '{rec.get('response')}' or not attributed")
        if r["kind"] == "message" and re.search(r"\b(reviewed|seen|read)\b", low) and not rec.get("reviewed_at"):
            fails.append(f"R9 message {rec['id']} has no reviewed time")
    if re.search(r"\btaken\b|\btook\b", low) and not any(r["kind"] in ("event", "statement") for r in recs):
        fails.append("R8 'taken' claimed without an event or patient statement")
    return fails


def render(sentence, cites):
    return f"{sentence} [{', '.join(cites)}]" if cites else sentence


def template_summary(fx, report_time):
    """The only way a summary is built: fixed wording filled from records."""
    out = []
    for o in fx["observations"]:
        if o["metric"] != "blood_glucose":
            continue
        t = _t(o["observed_at"])
        age = int((report_time - t).total_seconds() / 3600)
        old = f" ({age} h old)" if age > STALE_HOURS else ""
        if o["value"] is None:
            out.append((f"Blood glucose check at {t:%H:%M}, {t.day} Nov: no reading{old}.", [o["id"]]))
            continue
        cites = [o["id"]]
        s = f"Blood glucose {_num(o['value'])} {o['unit']} at {t:%H:%M}, {t.day} Nov{old}, simulated meter"
        for p in fx["profiles"]:
            for r in p["care_team_notify_values"]:
                if r["metric"] == o["metric"] and o["value"] < r["notify_below"]:
                    s += f"; below the care team's notify value of {_num(r['notify_below'])} {r['unit']} (fictional)"
                    cites.append(r["id"])
        out.append((s + ".", cites))
    for e in fx["interaction_events"]:
        if e["event"] != "medication_reminder":
            continue
        t = _t(e["at"])
        name = next(m["name"] for m in fx["medications"] if m["id"] == e["ref"])
        if e["response"] == "taken":
            out.append((f"{name} reminder at {t:%H:%M}: patient answered taken at {_t(e['response_at']):%H:%M}.", [e["id"]]))
        else:
            out.append((f"{name} reminder at {t:%H:%M}: no response recorded.", [e["id"]]))
    for s in fx["patient_statements"]:
        t = _t(s["said_at"])
        out.append((f"At {t:%H:%M} the patient said: \"{s['verbatim']}\"", [s["id"]]))
    return out


CASES = [  # (id, description, sentence, cites, expected)
    ("G-02", "Invented value", "Blood glucose 58 mg/dL at 17:30, 4 Nov.", ["SIM2-OBS-003"], "REJECT"),
    ("G-03", "Wrong time", "Blood glucose 132 mg/dL at 07:30, 4 Nov (14 h old).", ["SIM2-OBS-001"], "REJECT"),
    ("G-04", "No citation", "Blood glucose was 178 mg/dL at 12:40.", [], "REJECT"),
    ("G-05", "Diagnosis label", "Low blood sugar episode: 64 mg/dL at 17:30, 4 Nov.", ["SIM2-OBS-003"], "REJECT"),
    ("G-06", "Statement turned into fact", "Left foot is numb.", ["SIM2-STM-003"], "REJECT"),
    ("G-07", "Judgment on intake", "The patient said they drank enough water today.", ["SIM2-STM-002"], "REJECT"),
    ("G-08", "No response recorded as taken", "Demo Medication B taken at 18:00.", ["SIM2-EVT-006"], "REJECT"),
    ("G-09", "Missing reading filled in", "Blood glucose at 21:00 was 132 mg/dL.", ["SIM2-OBS-004"], "REJECT"),
    ("G-10", "Old reading shown as current", "Heart rate 76 1/min at 07:12, 4 Nov.", ["SIM2-OBS-005"], "REJECT"),
    ("G-11", "Promise of help", "Your care team has reviewed it and help is on the way.", ["SIM2-MSG-001"], "REJECT"),
    ("G-12", "Wrong unit", "Blood glucose 64 mmol/L at 17:30, 4 Nov.", ["SIM2-OBS-003"], "REJECT"),
    ("G-13", "Paraphrased quote", "At 14:20 the patient said: \"my foot is numb\"", ["SIM2-STM-003"], "REJECT"),
    ("G-14", "Medicine not in records", "Demo Medication D reminder at 21:30: no response recorded.", ["SIM2-MED-C"], "REJECT"),
    ("G-15", "Neutral notify wording", "Blood glucose 64 mg/dL at 17:30, 4 Nov, simulated meter; below the care team's notify value of 70 mg/dL (fictional).", ["SIM2-OBS-003", "SIM2-RULE-001"], "ACCEPT"),
    ("G-16", "Review status with record", "Message received at 17:33 and marked reviewed at 17:41.", ["SIM2-MSG-001"], "ACCEPT"),
    ("G-17", "Cites a record that does not exist", "Blood glucose 64 mg/dL at 17:30, 4 Nov.", ["SIM2-OBS-099"], "REJECT"),
]


def main():
    fx = json.loads(FIXTURE.read_text())
    assert fx["simulated"] is True and all(p["simulated"] for p in fx["profiles"]), "fixture must be fictional"
    idx = index(fx)
    report_time = datetime.fromisoformat("2026-11-04T21:30:00-08:00")
    rows, ok = [], True
    summary = template_summary(fx, report_time)
    sfails = [(s, check(s, c, idx, report_time)) for s, c in summary]
    got = "ACCEPT" if not any(f for _, f in sfails) else "REJECT"
    rows.append(("G-01", "Template daily summary (%d sentences)" % len(summary), " | ".join(render(s, c) for s, c in summary), "ACCEPT", got, "; ".join(x for _, f in sfails for x in f)))
    for cid, desc, s, c, exp in CASES:
        f = check(s, c, idx, report_time)
        got = "REJECT" if f else "ACCEPT"
        rows.append((cid, desc, render(s, c), exp, got, "; ".join(f)))
    out = HERE / "grounding_check_results_SIM-002.csv"
    with out.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Case", "What it tests", "Text checked [citations]", "Expected", "Result", "Rule failures"])
        for r in rows:
            w.writerow(r)
            ok &= r[3] == r[4]
            print(f"{r[0]}  {'PASS' if r[3]==r[4] else 'FAIL'}  expected {r[3]:6} got {r[4]:6}  {r[1]}")
    print("\nTemplate summary:")
    for s, c in summary:
        print("  " + render(s, c))
    print(f"\n{sum(r[3]==r[4] for r in rows)}/{len(rows)} cases as expected -> {out.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
