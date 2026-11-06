"""R0.3 day model. Content modules call W() and d(); build_plan.py assembles them.

Old R0.2 data supplies week titles, phases, gates, stages and requirement links.
Rewritten days may set a new unique output path. O(n) resolves the already
defined rewritten output so dependencies remain accurate.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD = json.loads((ROOT / "source_r02_plan.json").read_text())
OLD_DAYS = {d["id"]: d for d in OLD["days"]}

DAYS = {}
_week = {"n": None}

KINDS = {
    "desk": "Desk work",
    "software": "Software on your laptop",
    "simulation": "Simulation only",
    "procurement": "Quotes and orders",
    "physical": "Hands-on, no power",
    "powered": "Powered test (permit + second person)",
    "review": "Review with outside help",
}


def O(n):
    """Output path of an earlier day, including a rewritten output."""
    return DAYS[n]["output"] if n in DAYS else OLD_DAYS[n]["output"]


def W(n):
    _week["n"] = n


def d(n, title, goal, inp, st, chk, calc="", kind="desk", help=None, out=None,
      req=None, extra=None, stop=None, note=None):
    assert n not in DAYS, n
    assert _week["n"] == OLD_DAYS[n]["week"], (n, _week["n"])
    assert 2 <= len(st) <= 8, (n, len(st))
    assert 2 <= len(chk) <= 4, (n, len(chk))
    assert kind in KINDS, (n, kind)
    for m, s in st:
        assert isinstance(m, int) and m > 0 and len(s) > 3, (n, s)
    DAYS[n] = dict(
        id=n, title=title, goal=goal, inputs=list(inp), steps=[s for _, s in st],
        stepMinutes=[m for m, _ in st], minutes=sum(m for m, _ in st),
        acceptance=list(chk), calculation=calc, kind=kind, help=help,
        output=out or O(n), extraOutputs=list(extra or []), stop=stop,
        requirements=req, note=note,
    )


DAYREF = re.compile(r"day_(\d{3})_")


def deps(day):
    found = set()
    for text in day["inputs"]:
        for m in DAYREF.finditer(text):
            k = int(m.group(1))
            if k < day["id"]:
                found.add(k)
    if day["id"] > 1:
        found.add(day["id"] - 1)
    return sorted(found)
