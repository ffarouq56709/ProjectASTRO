BAYMAX 365 - PLAN R0.3 - 28 OCTOBER 2026
Owner: Faisal Farouq

Open Baymax_365_Offline.html in any modern browser. It works without a server or internet. Keep the resources/ folder next to it for the PDFs, photo, workbook and CSVs.

Your progress stays in the browser where you enter it. Same browser, same file location: your R0.2 notes and outcomes load automatically. Elsewhere: Settings -> Import a backup. Old step ticks are kept aside because the steps changed in R0.3.

Each day shows three separate things: the planned date, your task record (PASS / REWORK / BLOCKED) and, on hands-on days, the hardware result (what the robot actually did).

Planned time: about 672 hours over 365 days (90-140 min a day), inside your 2-3 hour budget. Outside reviews and fabrication are extra.

source/ holds the editable plan (plan_w*.py), build scripts and checks:
  python3 build_plan.py      -> dist/plan.json and the 365-day CSV
  python3 build_offline.py   -> ../Baymax_365_Offline.html
  node verify_site.mjs       -> qa/logic_checks_R0_3.json
archive_R0_2/ keeps the previous offline site, CSV and code unchanged.

Progress file: import Baymax_365_Progress_Days_001-013.json with Settings -> Import -> Merge (keep my records). It extends the saved Days 1-12 records with Day 13 PASS (document audit only), 2 hours. Existing browser records stay in place. The project-file notice and library downloads are updated in the rebuilt site; browser-local task records change only after import.
