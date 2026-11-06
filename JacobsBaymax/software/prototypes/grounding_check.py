#!/usr/bin/env python3
"""Grounding checker v2 for fictional SIM-002 records.

Rules R1-R9 are deterministic guardrails, not a clinical or language-model
evaluation. Each factual sentence is checked separately. A rejected sentence
is replaced by fixed fallback text rather than rewritten by a model.

The checker distinguishes the judgment "safe" from the harmless adverb in
"safely stored". It also rejects paraphrases such as "concerning" and
"worrying". Standard library only.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

HERE = Path(__file__).resolve().parent
FIXTURE = HERE.parents[1] / "simulated_patient_data" / "fictional_fixture_SIM-002.json"
STALE_HOURS = 6  # ASSUMPTION: demo setting, not a clinical value
DEFAULT_REPORT_TIME = datetime.fromisoformat("2026-11-04T21:30:00-08:00")
DEFAULT_FALLBACK = "I could not verify that sentence from the fictional records."

FORBIDDEN = [
    r"\bdiagnos(?:e|ed|es|is|tic)?\b", r"\bhypo(?:glycemi[ac])?\b",
    r"\bhyper(?:glycemi[ac])?\b", r"\bneuropath(?:y|ic)?\b",
    r"\blow (?:blood )?sugar\b", r"\bhigh (?:blood )?sugar\b",
    r"\bnormal\b", r"\bdanger(?:ous)?\b", r"\bsafe\b", r"\bstable\b",
    r"\bimprov(?:e|ed|ing|ement)?\b", r"\bwors(?:e|ened|ening)\b",
    r"\bfine\b", r"\benough\b", r"\bconcerning\b", r"\bworrying\b",
    r"\balarming\b", r"\bserious\b", r"\bshould\b",
    r"\brecommend(?:ed|ation)?\b", r"\bdose\b", r"\bdouble\b",
    r"\bon the way\b", r"\bis coming\b", r"\bhelp has been\b",
    r"\bambulance\b", r"\badministered\b", r"\bconfirmed taken\b",
    r"\bemergency\b",
]

# Interface or limitation statements that do not assert a SIM-002 record fact.
NEUTRAL_PATTERNS = [
    r"^please choose a fictional profile\.?$", r"^please choose an option\.?$",
    r"^would you like me to repeat that\??$", r"^would you like to request a human\??$",
    r"^would you like to contact your approved caregiver\??$", r"^you can decline\.?$",
    r"^you can stop at any time\.?$", r"^nothing was sent\.?$",
    r"^i did not save that\.?$", r"^i cannot determine what it means\.?$",
    r"^i cannot diagnose conditions\.?$", r"^i cannot give dosing advice\.?$",
    r"^i cannot give food advice\.?$", r"^i cannot lift or transfer a person\.?$",
    r"^i can show the fictional records\.?$", r"^i can read the stored text aloud\.?$",
    r"^the microphone is off\.?$", r"^the camera is off\.?$",
    r"^this is a simulated-data demonstration\.?$", r"^this uses fictional data only\.?$",
    r"^delivery is unconfirmed\.?$", r"^please review the exact text before sending\.?$",
    r"^choose cancel or continue\.?$", r"^no value is available\.?$",
    r"^request cancelled\.?$", r"^i could not verify that sentence from the fictional records\.?$",
]

ATTRIB = re.compile(r"\b(said|says|reported|told|answered)\b", re.I)
TIME = re.compile(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\b")
NUM = re.compile(r"(?<![\w.])[-+]?\d+(?:\.\d+)?(?![\w.])")
MED = re.compile(r"Demo Medication [A-Z]")
QUOTE = re.compile(r"[\"“]([^\"”]+)[\"”]")
CITATIONS = re.compile(r"\[([A-Z][A-Z0-9-]*(?:\s*,\s*[A-Z][A-Z0-9-]*)*)\]")
UNIT = re.compile(r"(?<!\w)(mg/dL|mmol/L|1/min|degC|°C)(?!\w)", re.I)


def _t(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


def _num(value: object) -> str | None:
    return f"{value:g}" if isinstance(value, (int, float)) else None


def load_fixture(path: Path = FIXTURE) -> dict:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    if fixture.get("simulated") is not True or not all(p.get("simulated") is True for p in fixture.get("profiles", [])):
        raise ValueError("fixture must be marked simulated")
    return fixture


def index(fixture: dict) -> dict[str, dict]:
    """Create an index containing only literal facts used by R1-R9."""
    records: dict[str, dict] = {}

    def add(record_id: str, kind: str, record: dict,
            numbers: Iterable[str | None] = (), units: Iterable[tuple[str, str]] = (),
            times: Iterable[datetime | None] = (), names: Iterable[str] = ()) -> None:
        time_values = [value for value in times if value is not None]
        facts = {value for value in numbers if value is not None}
        facts.update(value.strftime("%H:%M") for value in time_values)
        facts.update(str(value.day) for value in time_values)
        facts.update(names)
        records[record_id] = {"kind": kind, "record": record, "facts": facts, "units": dict(units)}

    for observation in fixture["observations"]:
        observed = _t(observation["observed_at"])
        number = _num(observation["value"])
        add(observation["id"], "observation", observation, [number],
            [(number, observation["unit"])] if number is not None else [], [observed])
    for statement in fixture["patient_statements"]:
        add(statement["id"], "statement", statement, NUM.findall(statement["verbatim"]), [],
            [_t(statement["said_at"])], MED.findall(statement["verbatim"]))
    for event in fixture["interaction_events"]:
        names = [m["name"] for m in fixture["medications"] if m["id"] == event["ref"]]
        add(event["id"], "event", event, NUM.findall(str(event.get("response", ""))), [],
            [_t(event["at"]), _t(event.get("response_at"))], names)
    for medication in fixture["medications"]:
        add(medication["id"], "medication", medication, [], [],
            [datetime.strptime(value, "%H:%M") for value in medication["schedule"]], [medication["name"]])
    for profile in fixture["profiles"]:
        for rule in profile["care_team_notify_values"]:
            values = [_num(rule.get("notify_below")), _num(rule.get("notify_above"))]
            add(rule["id"], "rule", rule, values,
                [(value, rule["unit"]) for value in values if value is not None])
    for message in fixture["messages"]:
        add(message["id"], "message", message, [], [],
            [_t(message.get("received_at")), _t(message.get("reviewed_at"))])
    return records


def is_neutral(sentence: str) -> bool:
    text = re.sub(r"\s+", " ", sentence.strip()).lower()
    return any(re.fullmatch(pattern, text, re.I) for pattern in NEUTRAL_PATTERNS)


def check(sentence: str, cites: list[str], records: dict[str, dict], report_time: datetime) -> list[str]:
    """Return R1-R9 failures for one citation-free sentence body."""
    text = sentence.strip()
    lower = text.lower()
    failures: list[str] = []
    if not cites and is_neutral(text):
        return failures
    for pattern in FORBIDDEN:
        if re.search(pattern, lower, re.I):
            failures.append(f"R4 judgment/advice/promise word: /{pattern}/")

    cited = [records.get(citation) for citation in cites]
    if any(record is None for record in cited):
        failures.append("R1 cites a record that does not exist")
        cited = [record for record in cited if record is not None]
    if not cited:
        failures.append("R1 factual sentence has no valid citation")
        return failures

    facts = set().union(*(record["facts"] for record in cited))
    units: dict[str, str] = {}
    for record in cited:
        units.update(record["units"])
        if record["kind"] == "observation":
            age = (report_time - _t(record["record"]["observed_at"])).total_seconds() / 3600
            facts.add(str(int(age)))

    times = TIME.findall(text)
    numbers = NUM.findall(TIME.sub(" ", text))
    medicines = MED.findall(text)
    shown_units = [value.lower() for value in UNIT.findall(text)]
    for value in times:
        if value.zfill(5) not in facts:
            failures.append(f"R2 time {value} not in cited records")
    for number in numbers:
        if number not in facts:
            failures.append(f"R2 number {number} not in cited records")
        elif number in units and not re.search(re.escape(number) + r"\s*" + re.escape(units[number]), text, re.I):
            failures.append(f"R2 number {number} missing or wrong unit (record unit {units[number]})")
    expected_units = {value.lower() for value in units.values()}
    for unit in shown_units:
        if unit not in expected_units:
            failures.append(f"R2 unit {unit} not in cited records")
    for medicine in medicines:
        if medicine not in facts:
            failures.append(f"R3 medicine name '{medicine}' not in cited records")

    for record in cited:
        raw = record["record"]
        if record["kind"] == "statement":
            if not ATTRIB.search(text):
                failures.append(f"R5 patient statement {raw['id']} written as fact")
            quotes = QUOTE.findall(text)
            if not quotes:
                failures.append(f"R5 patient statement {raw['id']} not quoted verbatim")
            for quote in quotes:
                if quote.strip().lower().rstrip(".") != raw["verbatim"].strip().lower().rstrip("."):
                    failures.append(f"R5 quote not verbatim from {raw['id']}")
            if not raw.get("confirmed"):
                failures.append(f"R5 statement {raw['id']} not read back and confirmed")
        elif record["kind"] == "observation":
            observed = _t(raw["observed_at"])
            if observed.strftime("%H:%M") not in times:
                failures.append(f"R6 reading {raw['id']} shown without observed time")
            age_hours = (report_time - observed).total_seconds() / 3600
            if age_hours > STALE_HOURS and not re.search(r"\b(?:old|stale)\b", lower):
                failures.append(f"R6 reading {raw['id']} older than {STALE_HOURS} h but not marked old")
            if raw["value"] is None:
                if "no reading" not in lower:
                    failures.append(f"R7 missing reading {raw['id']} not stated as 'no reading'")
                if any(number not in facts for number in numbers) or shown_units:
                    failures.append(f"R7 value or unit supplied for missing reading {raw['id']}")
        elif record["kind"] == "event" and re.search(r"\b(?:taken|took)\b", lower):
            if raw.get("response") != "taken" or not ATTRIB.search(text):
                failures.append(f"R8 'taken' unsupported by event {raw['id']}")
        elif record["kind"] == "message" and re.search(r"\b(?:reviewed|seen|read)\b", lower):
            if not raw.get("reviewed_at"):
                failures.append(f"R9 message {raw['id']} has no review time")
    if re.search(r"\b(?:taken|took)\b", lower) and not any(record["kind"] in ("event", "statement") for record in cited):
        failures.append("R8 'taken' claimed without an event or patient statement")
    return list(dict.fromkeys(failures))


def split_sentences(output: str) -> list[str]:
    normalized = re.sub(r"([.!?])\s*(\[[A-Z][A-Z0-9,\- ]*\])", r" \2\1", output.strip())
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9I\"“\[])", normalized) if part.strip()]


def extract_sentence(sentence: str) -> tuple[str, list[str]]:
    citations: list[str] = []
    for match in CITATIONS.finditer(sentence):
        citations.extend(value.strip() for value in match.group(1).split(","))
    body = CITATIONS.sub("", sentence)
    body = re.sub(r"\s+([.!?])", r"\1", re.sub(r"\s+", " ", body)).strip()
    return body, citations


@dataclass(frozen=True)
class SentenceDecision:
    original: str
    body: str
    citations: tuple[str, ...]
    failures: tuple[str, ...]
    output: str

    @property
    def accepted(self) -> bool:
        return not self.failures


@dataclass(frozen=True)
class OutputDecision:
    rendered_text: str
    sentences: tuple[SentenceDecision, ...]

    @property
    def accepted(self) -> bool:
        return all(sentence.accepted for sentence in self.sentences)


def check_output(output: str, records: dict[str, dict], report_time: datetime = DEFAULT_REPORT_TIME,
                 fallback: str = DEFAULT_FALLBACK) -> OutputDecision:
    """Check model output sentence-by-sentence and replace rejected sentences."""
    decisions = []
    for original in split_sentences(output):
        body, citations = extract_sentence(original)
        failures = check(body, citations, records, report_time)
        decisions.append(SentenceDecision(original, body, tuple(citations), tuple(failures),
                                          original if not failures else fallback))
    return OutputDecision(" ".join(item.output for item in decisions), tuple(decisions))


def render(sentence: str, citations: list[str]) -> str:
    return f"{sentence.rstrip('.')} [{', '.join(citations)}]." if citations else sentence


def template_summary(fixture: dict, report_time: datetime = DEFAULT_REPORT_TIME) -> list[tuple[str, list[str]]]:
    output: list[tuple[str, list[str]]] = []
    for observation in fixture["observations"]:
        if observation["metric"] != "blood_glucose":
            continue
        observed = _t(observation["observed_at"])
        age = int((report_time - observed).total_seconds() / 3600)
        age_text = f" ({age} h old)" if age > STALE_HOURS else ""
        if observation["value"] is None:
            sentence = f"Blood glucose check at {observed:%H:%M}, {observed.day} Nov: no reading{age_text}."
        else:
            sentence = f"Blood glucose {_num(observation['value'])} {observation['unit']} at {observed:%H:%M}, {observed.day} Nov{age_text}."
        output.append((sentence, [observation["id"]]))
    for event in fixture["interaction_events"]:
        if event["event"] != "medication_reminder":
            continue
        at = _t(event["at"])
        name = next(m["name"] for m in fixture["medications"] if m["id"] == event["ref"])
        if event["response"] == "taken":
            sentence = f"{name} reminder at {at:%H:%M}: patient answered taken at {_t(event['response_at']):%H:%M}."
        else:
            sentence = f"{name} reminder at {at:%H:%M}: no response recorded."
        output.append((sentence, [event["id"]]))
    for statement in fixture["patient_statements"]:
        said = _t(statement["said_at"])
        output.append((f"At {said:%H:%M} the patient said: \"{statement['verbatim']}\".", [statement["id"]]))
    return output


REGRESSION_CASES = [
    ("G-02", "Invented value", "Blood glucose 58 mg/dL at 17:30, 4 Nov.", ["SIM2-OBS-003"], "REJECT"),
    ("G-03", "Wrong time", "Blood glucose 132 mg/dL at 07:30, 4 Nov (14 h old).", ["SIM2-OBS-001"], "REJECT"),
    ("G-04", "No citation", "Blood glucose was 178 mg/dL at 12:40.", [], "REJECT"),
    ("G-05", "Diagnosis", "Low blood sugar episode: 64 mg/dL at 17:30, 4 Nov.", ["SIM2-OBS-003"], "REJECT"),
    ("G-06", "Statement as fact", "Left foot is numb.", ["SIM2-STM-003"], "REJECT"),
    ("G-07", "Judgment", "The patient said they drank enough water today.", ["SIM2-STM-002"], "REJECT"),
    ("G-08", "False taken", "Demo Medication B taken at 18:00.", ["SIM2-EVT-006"], "REJECT"),
    ("G-09", "Filled missing", "Blood glucose at 21:00 was 132 mg/dL.", ["SIM2-OBS-004"], "REJECT"),
    ("G-10", "Stale current", "Heart rate 76 1/min at 07:12, 4 Nov.", ["SIM2-OBS-005"], "REJECT"),
    ("G-11", "Promise", "Your care team has reviewed it and help is on the way.", ["SIM2-MSG-001"], "REJECT"),
    ("G-12", "Wrong unit", "Blood glucose 64 mmol/L at 17:30, 4 Nov.", ["SIM2-OBS-003"], "REJECT"),
    ("G-13", "Paraphrased quote", "At 14:20 the patient said: \"my foot is numb\".", ["SIM2-STM-003"], "REJECT"),
    ("G-14", "Unknown medicine", "Demo Medication D reminder at 21:30: no response recorded.", ["SIM2-MED-C"], "REJECT"),
    ("G-15", "Grounded", "Blood glucose 64 mg/dL at 17:30, 4 Nov.", ["SIM2-OBS-003"], "ACCEPT"),
    ("G-16", "Reviewed", "Message received at 17:33 and marked reviewed at 17:41.", ["SIM2-MSG-001"], "ACCEPT"),
    ("G-17", "Missing record", "Blood glucose 64 mg/dL at 17:30, 4 Nov.", ["SIM2-OBS-099"], "REJECT"),
]


def main() -> int:
    fixture = load_fixture()
    records = index(fixture)
    rows = []
    summary_text = " ".join(render(sentence, citations) for sentence, citations in template_summary(fixture))
    summary_decision = check_output(summary_text, records)
    rows.append(("G-01", "Template summary", summary_text, "ACCEPT",
                 "ACCEPT" if summary_decision.accepted else "REJECT",
                 " | ".join(f for d in summary_decision.sentences for f in d.failures)))
    for case_id, description, sentence, citations, expected in REGRESSION_CASES:
        failures = check(sentence, citations, records, DEFAULT_REPORT_TIME)
        result = "REJECT" if failures else "ACCEPT"
        rows.append((case_id, description, render(sentence, citations), expected, result, "; ".join(failures)))
    output = HERE / "grounding_check_results_SIM-002.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["Case", "What it tests", "Text checked [citations]", "Expected", "Result", "Rule failures"])
        writer.writerows(rows)
    for row in rows:
        print(f"{row[0]}  {'PASS' if row[3] == row[4] else 'FAIL'}  expected {row[3]:6} got {row[4]:6}  {row[1]}")
    passed = sum(row[3] == row[4] for row in rows)
    print(f"\n{passed}/{len(rows)} cases as expected -> {output.name}")
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
