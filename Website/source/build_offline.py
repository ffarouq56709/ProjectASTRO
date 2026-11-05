"""Build ../Baymax_365_Offline.html (one file, opens without a server) and sync ../resources."""
import base64, json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parent
dist = ROOT / "dist"
# Keep downloadable working registers and the progress backup in both builds.
project = ROOT.parents[1]
for source, target in [
    ("JacobsBaymax/requirements/day_013_hazard_traceability.csv", "Day_013_Hazard_Traceability.csv"),
    ("JacobsBaymax/risk_records/hazards_R0_3.csv", "Hazards_R0_3.csv"),
    ("JacobsBaymax/requirements/requirements_R0_3.csv", "Requirements_R0_3.csv"),
    ("JacobsBaymax/tests/verification_matrix_R0_3.csv", "Verification_R0_3.csv"),
    ("Website/Baymax_365_Progress_Days_001-013.json", "Baymax_365_Progress_Days_001-013.json"),
]:
    shutil.copy2(project / source, dist / "resources" / target)
html = (dist / "index.html").read_text()
css = (dist / "styles.css").read_text()
js = (dist / "app.js").read_text()
plan = (dist / "plan.json").read_text()
fav = base64.b64encode((dist / "favicon.svg").read_bytes()).decode()
html = html.replace('<link rel="icon" href="favicon.svg" type="image/svg+xml">', f'<link rel="icon" href="data:image/svg+xml;base64,{fav}">')
html = html.replace('<link rel="stylesheet" href="styles.css">', f"<style>{css}</style>")
html = html.replace('<script src="app.js" defer></script>', "")
safe_plan = plan.replace("</", "<\\/")
html = html.replace("</body></html>", f'<script id="embedded-plan" type="application/json">{safe_plan}</script>\n<script>{js}</script>\n</body></html>')
out = ROOT.parent / "Baymax_365_Offline.html"
out.write_text(html)
res = ROOT.parent / "resources"
for f in (dist / "resources").iterdir():
    shutil.copy2(f, res / f.name)
shutil.copy2(dist / "resources" / "Baymax_365_Daily_Plan.csv", ROOT.parent / "Baymax_365_Daily_Plan.csv")
print(out, out.stat().st_size)
