# Project ASTRO · R0.3 changes (28 October 2026)

## Description (92 words)
See PROJECT_DESCRIPTION.txt.

## What changed
- **Day 6 rewritten** (requirements/day_006_D03_D04_configuration.md + PDF). Keeps 10 leg joints with no hip yaw. Adds load, gait, drive, cost and mass screens (architecture/day_006_joint_load_screen.py). Recommends hip-roll axes 0.30 m apart under wide thigh shells, a 3:1 stage on hip roll and 2:1 on knee, pinned arms during gait, fixed hands, and a bought guided linear actuator on its own stand for handling. Mass 48.5 kg + 6.5 kg reserve (shell +1.6 kg risk). Actuator line USD 2,841–3,481 from dated listings, not quotes.
- **Reference photo** saved at cad_specifications/reference/astro-rigid-panel-concept-v1.png and used on Days 6, 86–91, 309, 314, 362.
- **All 365 days rewritten**: goal, inputs (with links to earlier days), timed steps, numbers, output file, checks, outside help. Day numbers, weeks, output paths, gates and stages unchanged. Planned time ~669 h (90–135 min/day).
- **Website**: cream/mint/blush notebook style, 16 px body text, separate planned date / task record / hardware result, project-file records shown for Days 1–6, R0.2 progress migrates automatically.
- New working files: revision_history/decision_log_R0_3.csv, evidence/day_006_configuration_review_R0_3.json; CHANGELOG and sources.csv appended.

## Preserved
R0.1 release archive, R0.1 registers, both earlier Day 6 versions (revision_history/day_006_initial_proposal_R0_2.zip, day_006_revised_proposal_R0_2.zip), Day 1–5 records, old charters, R0.2 website (Website/archive_R0_2/) and R0.2 builders (Website/source/archive_R0_2/). CURRENT_PROJECT_READINGS.txt and 01_PROJECT_BRIEF.txt are left as the R0.2 handoff text.

## Verified
22 website logic checks pass; browser checks at 1366 px and 390 px with no errors or sideways scroll; Day 6 numbers reproduced by the screen script; package checksums in FILE_MANIFEST_R0_3.json. No hardware, simulation run, purchase or review took place.

## Owner decisions (2026-10-28)
Accepted: D-03 Option A with 0.30 m hip axes, 3:1 hip roll, 2:1 knee; D-04 handling stand; D-01 USD 10,000 working cap until quotes. Still open: D-02, D-05; D-06 awaiting confirmation.

## Original Day 7 list
1. D-03: accept 10 joints, no yaw, for modelling.
2. Hip spacing: 0.30 m + 3:1 hip roll (keeps the photo's stance) or 0.24 m + 2:1.
3. D-04: bought actuator on its own stand.
4. D-01: working cap until quotes (Day 193 final).
5. D-06: Day 1 charter differences (recommend R0.2 wording for all five).

## Not accessed
Browser-local progress (none exported), the original pasted brief, the latest GitHub copy, ISO standard full texts, vendor quotes.
