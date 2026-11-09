# Day 15 — actuator-bench and care-software boundary

Revision: R0.3  
Actual work date: 2026-11-05  
Accountable owner: Faisal Farouq  
Document status: project planning record; not a controls, security, clinical or safety review  
Owner time recorded: 2.0 hours  
Document result: **PASS — software boundary and laptop inventory only**

## Boundary decision

The actuator bench and fictional caregiver demo are separate processes with separate data, privileges and logs. There is no care-app-to-motion API, import, socket, queue, shared command file or credential. The permitted care-to-bench command count is **zero**.

```text
Fictional caregiver process
  SIM-002 fixture -> templates -> grounding checker -> localhost mock receiver
             |
             X  no imports, motor commands, CAN access or bench credentials
             |
Operator-controlled bench process
  explicit CLI -> current clamp / watchdog -> DryRunBackend
                                      -> TODO reviewed hardware adapter (blocked)
```

## Process and privilege inventory

| Boundary | Actuator bench process | Fictional caregiver process |
|---|---|---|
| Entry point | `software/bench/single_joint_bench.py` invoked explicitly by an operator | Future bounded demo using `caregiver_workflows/05_caregiver_link_and_grounding.md` and the grounding prototype |
| Default behavior | Dry run only; generated telemetry is labelled simulated | Fictional SIM-002 records only; consent false by default; mock receiver only |
| Hardware privilege | Future adapter is deliberately unimplemented; hardware mode requires permit ID, second-person acknowledgement and firmware revision before it reaches the TODO | None; no CAN library, interface, motor command schema or permit credential |
| Network privilege | None required for the current dry run | `http://127.0.0.1:8001` only when the mock receiver is intentionally started; no real recipient |
| Data allowed | Bench command and telemetry fields; no care profile or message records | Fictional readings, verbatim confirmed statements, robot events and mock care-team entries; no bench commands |
| Stop behavior | Software current clamp, telemetry watchdog, signal stop and backend stop/close | Rejected factual sentences use deterministic fallback; no output can enable motion |
| Cross-process interface | **DENY — zero allowed calls or command files** | **DENY — zero allowed calls or command files** |

## Laptop inventory recorded on 2026-11-05

| Item | Recorded value | Status / limitation |
|---|---|---|
| Computer | MacBook Pro, model identifier Mac14,7, Apple M2 | RECORDED from local hardware inventory; serial identifiers intentionally omitted |
| CPU | 8 cores: 4 performance and 4 efficiency | RECORDED |
| Memory | 8 GB | RECORDED; suitability for later local LLM/ASR candidates is UNTESTED |
| Operating system | macOS 26.5.2, build 25F84 | RECORDED |
| Python | CPython 3.13.7 from `python3 --version` | RECORDED for the current command environment |
| Root filesystem | 460 GiB volume; 83 GiB available at inspection | POINT-IN-TIME ONLY; available space will change |
| CAN interface | No CAN-named network or `/dev` interface identified by the local screen | **UNCONFIRMED** — no adapter make/model, USB identity, driver, isolation or compatibility evidence recorded |
| Tools / bench supply | No physical inventory supplied | **UNCONFIRMED** |

No serial number, hardware UUID or private network address is stored in this document.

## Repository ownership and logs

| Asset | Accountable role | Current path | Evidence/log path |
|---|---|---|---|
| Bench controller and analyzer | Owner; controls reviewer still unassigned | `software/bench/` | Future reviewed runs: `tests/bench_runs/<run-id>/`; Day 15 dry run stays in a temporary directory and is not hardware evidence |
| Grounding prototype | Owner; software/security reviewer still unassigned | `software/prototypes/` | `software/prototypes/grounding_check_results_SIM-002.csv` |
| Care workflow and fixtures | Owner; ethics/clinical authority not assigned | `caregiver_workflows/` and `simulated_patient_data/` | Future fictional demo logs: `software/care_demo/logs/<run-id>/` after that component exists |
| Decisions and permissions | Owner | `revision_history/decision_log_R0_3.csv` | Exact permit, reviewer and purchase records in their named requirement/test files |

Proposed future log paths do not assert that the directory, service or test exists today.

## Deny-by-default integration rule

1. Care software must never import the bench controller or a future CAN adapter.
2. Care output must never be interpreted as a position, velocity, current, enable, disable or reset command.
3. Bench software must never read fictional patient records, consent, messages or caregiver replies.
4. No shared secret, permit token, motor socket, command queue or writable command file may bridge the processes.
5. If a later integration needs robot status in the care UI, it starts as one-way, read-only, typed status through a new reviewed interface. Its failure must not affect stop behavior.
6. Any proposed motion authority requires a new decision, requirements, threat review, controls/safety review and test evidence. Silence or an unknown message always denies motion.

## Day 15 dry-run evidence

Command:

```bash
python3 ProjectASTRO/software/bench/single_joint_bench.py \
  --duration-s 1 --rate-hz 40 \
  --output /private/tmp/projectastro_day15_bench.csv
```

Acceptance:

- no hardware mode requested;
- no CAN frame, identifier or register used;
- output must say `DRY RUN ONLY` and watchdog `OK`;
- temporary CSV must contain command, measured position/velocity/current, temperature and UTC timestamp fields; and
- generated torque, backlash and temperature values remain simulated, not robot evidence.

## Completion checks

- PASS: care software has no motor or CAN authority and no permitted care-to-bench call.
- PASS: available laptop facts are recorded; CAN adapter, tools and later local-model suitability remain explicitly unconfirmed or untested.
- PASS: the bench logger defaults to dry run and can execute without hardware.
- LIMIT: no software/security or controls reviewer has approved this boundary.
- LIMIT: Day 14 decisions are accepted; owner outreach remains unsent, so Day 14 remains REWORK.

## Sources

- `software/bench/single_joint_bench.py`
- `software/bench/analyze_bench.py`
- `software/prototypes/grounding_check.py`
- `caregiver_workflows/05_caregiver_link_and_grounding.md`
- `simulated_patient_data/fictional_fixture_SIM-002.json`
- `requirements/day_014_walking_first_reset.md`

