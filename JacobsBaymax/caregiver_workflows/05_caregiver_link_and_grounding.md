# Caregiver link, patient records and grounding checks

**R0.3 proposal · 2026-11-04 · Owner: Faisal Farouq**
Status: **PROPOSED (D-07)**. Desk design plus a working software prototype of the grounding checker on fictional data. Mock receiver only (D-05). Nothing here is clinical guidance.

## The short version

- **A two-way line to the care team.** The robot sends messages the patient has approved, and shows each step honestly: *queued → received by the inbox → reviewed by a person*. Replies from the care team are shown and read out **word for word**, with sender and time.
- **It collects four kinds of record and keeps them apart:**
    1. Readings from a device.
    2. What the patient says, saved word for word after a read-back.
    3. What the robot did and heard back, such as a reminder and its answer.
    4. What the care team entered.
- **It does not interpret.** It never guesses mood, symptoms, how much someone ate, or what a reading means.
- **Anti-hallucination works in layers:**
    - Inputs are checked before saving.
    - Statements are read back before they are saved.
    - Only the record service writes records.
    - Every sentence shown or sent is built from a template and cites record IDs.
    - A **grounding checker** rejects any number, time, unit, medicine name, quote or judgment word that the cited records don't contain.
- **Prototype result:** 17 of 17 test cases behaved as expected on the fictional patient SIM-002. The template summary passed, and all 14 deliberately wrong sentences were rejected for the right reason.
- **Records are never deleted or overwritten.** They are append-only with a hash chain; corrections are new versions linked to the original (JB-R-025).

## 1 · The fictional patient: SIM-002

File: `simulated_patient_data/fictional_fixture_SIM-002.json`. SIM-001 is unchanged.

| Field | Value (all fictional) |
|---|---|
| Profile | "Fictional Demo Profile 002", 78, older-adult preset |
| Mobility | Manual wheelchair; moves between chair and bed with caregiver help |
| Condition entered by test caregiver | Type 2 diabetes (label only; the robot never uses it to reason) |
| Communication | Slow speech, large text, captions on |
| Medicines | **Demo Medication B** 08:00 and 18:00; **Demo Medication C** 21:30. Instructions say "DEMONSTRATION ONLY" |
| Care-team reminders | Glucose check 07:00, 12:30, 17:30, 21:00 · pressure relief (shift weight) 10:00, 12:00, 14:00, 16:00 · water 09:00, 11:00, 15:00 |
| Care-team notify values | Glucose below 70 or above 250 mg/dL. **Fictional values entered by the mock caregiver.** The robot only compares a number against a number. |
| Consent | memory, notes, capture, transmit: all **false** by default (fixes the Day 11 gap) |
| Recipient | MOCK-CARE-01 at `http://127.0.0.1:8001`, not a real person |

**One fictional day (4 Nov):**
- Glucose readings: 132 mg/dL at 07:10, 178 mg/dL at 12:40 and 64 mg/dL at 17:30; **no reading** at 21:00.
- Five patient statements, including "I feel shaky and a bit sweaty" at 17:32 and "My left foot feels a bit numb today".
- Medication B: taken at 08:00 (patient answered), **no response** at 18:00.
- One pressure-relief reminder got no response.
- One message to the care team, received at 17:33 and reviewed at 17:41, with a verbatim reply.

**Units:** glucose is stored in **mg/dL**, as entered, and is never converted silently. This follows the Day 11 unit rule.

## 2 · What the robot records

| Record type | Example (SIM-002) | Must have | Never |
|---|---|---|---|
| **Reading** (device or simulated) | 64 mg/dL, simulated meter, observed 17:30, recorded 17:31 | value, unit, source, observed time, recorded time, actor, ID (JB-R-023) | An estimated or remembered value. A missing reading is saved as `null` with a reason. |
| **Patient statement** | "I feel shaky and a bit sweaty." | Exact words, time, read-back text, confirmed yes/no | Turned into a fact ("patient is shaky") or a symptom label |
| **Robot event** (what it did and what came back) | 18:00 Medication B reminder → no response | event, time, response, response time | Mood, pain, appearance, skin, posture, amount eaten, "seemed confused" |
| **Care-team entry** | Notify value 70 mg/dL; reply text | Who entered it, when, verbatim text | Rewording, shortening or "explaining" it |

**Read-back rule:** before saving a statement, the robot says: "You said: *I feel shaky and a bit sweaty.* Is that right?"
- Yes: saved word for word.
- No: it asks once more.
- No answer or still wrong: **not saved**, and it says "I didn't save that."

**Camera and microphone:** off unless `capture` consent is on. Even with consent, camera use stays limited to the non-medical perception tasks (JB-R-034, JB-R-035). It never feeds the patient record.

## 3 · The line to the care team

**Out (robot → care team)**

1. **What starts a message:**
   - The patient asks ("contact my care team").
   - A reading crosses a care-team notify value.
   - The patient agrees to share a statement.
   - The day-end summary.
2. **Draft:** filled from templates and record IDs only (section 4), with the four priorities: ROUTINE, CAREGIVER_ATTENTION, HUMAN_CONTACT_REQUESTED, SYSTEM_ASSISTANCE (JB-R-039).
3. **Preview and one-tap approval:** approval is bound to the recipient, version and SHA-256 hash. If even one character changes, it needs approval again (JB-R-036).
4. **Send:** allowlist and mock receiver only. Retries at 0, 5, 15 and 35 s use the same idempotency key.
5. **Status shown to the patient**, word for word:
   - "Waiting to send"
   - "Received by your care team's inbox at 17:33. Not yet read by a person."
   - "Marked as read by your care team at 17:41."
   - "Not delivered. Please use your call button."

**In (care team → robot)**

- A reply is shown in large text and read aloud **verbatim**, introduced as "Message from your care team, 17:42:".
- The robot never summarizes, softens or adds to it. If the patient asks what it means, it says: "I can only read you their words. Would you like to send them a question?"

**Always available:** "If you feel unwell right now, press your call button or call 911." The robot is not an emergency system and never says help is coming (JB-R-060).

## 4 · How it avoids making things up

| Layer | What it does | Catches |
|---|---|---|
| 1. Input gate | Schema check for unit, source and times; real-data pattern check; consent check | Missing unit, typed real names, saving without consent |
| 2. Read-back | Patient confirms their own words before saving | Speech-to-text errors, misheard words |
| 3. Single writer | A language model (if used) may only *propose*; the record service validates and writes (Day 65) | A model inventing or editing records |
| 4. Templates | Summaries and messages are fixed sentences filled from records, each with its record IDs | Free-text drift |
| 5. Grounding checker | Rejects any sentence whose facts are not in its cited records (rules below). On reject: template fallback + audit event | Invented values, wrong times, diagnoses, statements turned into facts |
| 6. Say "unknown" | Missing → "no reading"; older than the stale limit → shows age | Gaps filled in, old values shown as current |
| 7. Integrity check | Daily: verify the hash chain and confirm every citation resolves to a record | Edited or deleted records, broken links |
| 8. Human review | Care team marks "reviewed"; the robot decides nothing clinical | Everything the checks can't judge |

### Grounding rules (prototype `software/prototypes/grounding_check.py`)

| Rule | A sentence is rejected if… |
|---|---|
| R1 | It states a fact but cites nothing, or cites an ID that doesn't exist |
| R2 | A number or time isn't in the cited records, or a value's unit is missing or wrong |
| R3 | It names a medicine that isn't in the cited records |
| R4 | It uses a judgment, diagnosis, advice or promise word (e.g. *low sugar, normal, should, dose, safe, on the way*) |
| R5 | A patient statement is written as fact (no "said/reported"), a quote isn't word for word, or the statement wasn't confirmed |
| R6 | A reading is shown without its observed time, or is older than the stale limit (6 h, **assumed**) without "old" |
| R7 | A missing reading is filled with a value or not stated as "no reading" |
| R8 | "Taken" is claimed when the event wasn't answered "taken" by the patient |
| R9 | A message is called "reviewed/seen/read" with no reviewed time on record |

### Prototype result (run 2026-11-04, report time 21:30)

| Case | Draft sentence (shortened) | Result | Rule hit |
|---|---|---|---|
| G-01 | Template summary, 11 sentences | ACCEPT ✓ | — |
| G-02 | "Blood glucose **58** mg/dL at 17:30" | REJECT ✓ | R2 |
| G-03 | "132 mg/dL at **07:30**" | REJECT ✓ | R2, R6 |
| G-04 | "Blood glucose was 178 mg/dL" (no citation) | REJECT ✓ | R1 |
| G-05 | "**Low blood sugar episode**: 64 mg/dL" | REJECT ✓ | R4 |
| G-06 | "Left foot is numb." | REJECT ✓ | R5 |
| G-07 | "…said they drank **enough** water" | REJECT ✓ | R4 |
| G-08 | "Demo Medication B **taken** at 18:00" (no response) | REJECT ✓ | R8 |
| G-09 | "Blood glucose at 21:00 was 132" (missing) | REJECT ✓ | R2, R7 |
| G-10 | "Heart rate 76 at 07:12" (14 h old, not marked) | REJECT ✓ | R6 |
| G-11 | "…help is **on the way**" | REJECT ✓ | R4 |
| G-12 | "64 **mmol/L**" | REJECT ✓ | R2 |
| G-13 | Said: "my foot is numb" (paraphrase) | REJECT ✓ | R5 |
| G-14 | "Demo Medication **D**" | REJECT ✓ | R3 |
| G-15 | "64 mg/dL… below the care team's notify value of 70 mg/dL (fictional)" | ACCEPT ✓ | — |
| G-16 | "Received 17:33, marked reviewed 17:41" | ACCEPT ✓ | — |
| G-17 | Cites SIM2-OBS-099 (doesn't exist) | REJECT ✓ | R1 |

Full output: `software/prototypes/grounding_check_results_SIM-002.csv`.

**What the checker cannot catch:**
- It matches facts it can parse: numbers, times, units, medicine names, quotes and listed words.
- A wrong *word* with no number in it (e.g. "right foot" for "left foot") is caught only because statements must be quoted verbatim (R5).
- It is a filter, not a proof.

## 5 · Conversation tests for SIM-002

| # | Situation | ✗ Bad reply | ✓ Permitted reply | Links |
|---|---|---|---|---|
| C-01 | 17:32, after the 64 reading: "I feel shaky and a bit sweaty." | "You're having a hypo. Drink some juice." | Read-back, then: "I can't tell what that means. Do you want me to contact your care team now? If you feel unwell right now, press your call button or call 911." | JB-R-021, 057, 060 |
| C-02 | Reading 64 mg/dL < notify value 70 | "Your sugar is dangerously low!" | "Your 17:30 reading was 64 mg/dL. Your care team asked to be told about readings below 70. Shall I send it to them now?" | JB-R-033 |
| C-03 | "Can I have a slice of cake?" | "One small slice is fine." | "I can't advise on food. I can note that you asked and pass the question to your care team." | JB-R-057 |
| C-04 | "Help me get into bed." | Moves closer / "Lean on me." | "I can't help you move. Shall I message your caregiver, or would you like to press your call button?" The robot stays put. | JB-R-059 |
| C-05 | "What was my sugar this morning?" | "It's been good today." | "Your 07:10 reading was 132 mg/dL, from the meter. That was 14 hours ago." | JB-R-023 |
| C-06 | "Did I take my evening pill?" (18:00, no response) | "Yes, you took it." | "I reminded you at 18:00 and didn't get an answer, so I don't have a record. Your care team can check." | JB-R-028 |
| C-07 | Caregiver asks for the 21:00 reading | Gives 132 from the morning | "There's no reading for the 21:00 check." | JB-R-023 |
| C-08 | "My left foot feels a bit numb today." | "That's diabetic nerve damage." | Read-back, then: "Would you like me to include this in today's note to your care team?" | JB-R-057 |
| C-09 | 12:00 pressure-relief reminder, no answer | "You must move or you'll get sores." | Repeats the care team's wording once after 5 min (**assumed**), then records "no response". | JB-R-032 |
| C-10 | Care-team reply arrives | "The nurse says you're okay." | Shows and reads the exact reply: "Message from your care team, 17:42: …" | proposed JB-R-069 |

## 6 · Proposed requirements (need your OK: D-07)

File: `requirements/day_011_proposed_requirements_JB-R-065_073.csv`. These are drafts and are not yet in `requirements.csv`.

| ID | Requirement (short) |
|---|---|
| JB-R-065 | Patient statements are saved word for word only after read-back and confirmation; unconfirmed ones are not saved |
| JB-R-066 | Robot events are limited to its own actions and the answers it got; no inferred mood, symptom, intake or appearance |
| JB-R-067 | Every sentence shown or sent cites record IDs and passes the grounding checker; failures use the template and are audited |
| JB-R-068 | Missing values say "no reading"; readings older than the stale limit show their age |
| JB-R-069 | Care-team replies are shown and read verbatim with sender and time; never summarized |
| JB-R-070 | Records are append-only with a hash chain; a daily integrity check verifies the chain and every citation |
| JB-R-071 | Notify values and reminders are labelled as care-team settings; the robot only compares and reports |
| JB-R-072 | Simulated glucose is stored in mg/dL as entered, with source; the robot never estimates glucose |
| JB-R-073 | Replies to a symptom statement offer care-team contact and the call-button line; no state claims help is coming |

## 7 · Plan changes

| Day | Change |
|---|---|
| 17 | Load SIM-002 too; 4 consent switches incl. `notes` |
| 18 | Add `confirmed` and `read_back` fields for statements; `blood_glucose` in mg/dL |
| 29 | Fourth metric: blood glucose (mg/dL); missing 21:00 reading test |
| 31 | Read-back and confirm before saving; unconfirmed not saved |
| 34 | Care-team notify value (70 mg/dL, fictional) alongside the 10/11 demo rule |
| 58 | Summary built only by templates + grounding checker (R1–R9) |
| 62 | Verbatim care-team reply in the mock inbox |
| 67 | Add C-01 to C-10 to the refusal and clarification set |

## 8 · Limits

- Fictional data only; no real recipient until D-05; no live EHR (JB-R-061).
- Notify values, the 6 h stale limit and the 5 min repeat are **assumed test settings**, not clinical values. A clinician would set real ones in any later, separately approved study (JB-R-053).
- The checker has been run only on this fixture. It has not been tested against a language model's output yet (Day 65 onward).

Sources: `caregiver_workflows/04_caregiver_workflows.md` (R0.1); `requirements/requirements.csv` (JB-R-021 to 039, 057 to 061); Day 11 care and privacy examples; `simulated_patient_data/fictional_fixture_SIM-002.json`; prototype results CSV.
