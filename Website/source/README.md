# ASTRO 365 · plan R0.3

Static planner for Project ASTRO. Owner: Faisal Farouq. 28 October 2026.

- Day content: `plan_w01_06.py` … `plan_w43_53.py` (one `d()` call per day: goal, inputs, timed steps, numbers, output, checks, outside help).
- `plan_model.py` reads `source_r02_plan.json` so day numbers, weeks, gates and stages stay aligned with R0.2. Rewritten days may use clearer, unique output paths.
- `python3 build_plan.py` writes `dist/plan.json` and `dist/resources/ASTRO_365_Daily_Plan.csv`.
- `python3 build_offline.py` writes `../ASTRO_365_Offline.html` and syncs `../resources/`.
- `node verify_site.mjs` runs 22 logic checks (no browser, no robot).
- Serve `dist/` over HTTP for the multi-file version: `python3 -m http.server 4173 --directory dist`.

Browser storage key is unchanged (`jacobs-astro-365-r02`), so existing progress loads. R0.2 builders are in `archive_R0_2/`.
