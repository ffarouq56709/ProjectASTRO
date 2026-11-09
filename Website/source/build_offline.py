"""Build ../ASTRO_365_Offline.html (one file, opens without a server) and sync ../resources."""
import base64, json, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parent
dist = ROOT / "dist"
html = (dist / "index.html").read_text()
css = (dist / "styles.css").read_text()
academic_css = (dist / "academic-theme.css").read_text()
js = (dist / "app.js").read_text()
plan = (dist / "plan.json").read_text()
fav = base64.b64encode((dist / "favicon.svg").read_bytes()).decode()
html = html.replace('<link rel="icon" href="favicon.svg" type="image/svg+xml">', f'<link rel="icon" href="data:image/svg+xml;base64,{fav}">')
html = html.replace('<link rel="stylesheet" href="styles.css">', f"<style>{css}</style>")
html = html.replace('<link rel="stylesheet" href="academic-theme.css">', f"<style>{academic_css}</style>")
html = html.replace('<script src="app.js" defer></script>', "")
safe_plan = plan.replace("</", "<\\/")
html = html.replace("</body></html>", f'<script id="embedded-plan" type="application/json">{safe_plan}</script>\n<script>{js}</script>\n</body></html>')
out = ROOT.parent / "ASTRO_365_Offline.html"
out.write_text(html)
res = ROOT.parent / "resources"
for f in (dist / "resources").iterdir():
    shutil.copy2(f, res / f.name)
shutil.copy2(dist / "resources" / "ASTRO_365_Daily_Plan.csv", ROOT.parent / "ASTRO_365_Daily_Plan.csv")
print(out, out.stat().st_size)
