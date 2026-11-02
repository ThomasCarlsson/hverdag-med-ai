"""Bygger prompt-siden (prompts/index.html) ud fra alle uger i maskine/content/.

Siden linkes fra Instagram-bioen, så følgere kan kopiere prompts med én knap.
Kør: python3 scripts/build_prompts.py   (fra repoets rod)
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "maskine" / "content"
OUT = ROOT / "prompts" / "index.html"


def week_no(p):
    m = re.search(r"uge-(\d+)", p.stem)
    return int(m.group(1)) if m else 0


def posted_titles():
    """Titel -> tidspunkt for opslag, der er postet (fra queue/*/opslag.json)."""
    out = {}
    for f in (ROOT / "queue").glob("*/opslag.json"):
        q = json.loads(f.read_text(encoding="utf-8"))
        if q.get("status") == "postet":
            out[q.get("titel", "")] = q.get("postet") or q.get("tidspunkt", "")
    return out


def collect():
    posted = posted_titles()
    groups = []
    for f in CONTENT.glob("uge-*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        for post in data.get("posts", []):
            prompts = [s for s in post.get("slides", []) if s.get("type") == "prompt"]
            title = post.get("cover", {}).get("title", "")
            if not prompts or title not in posted:
                continue
            groups.append({
                "id": f"{f.stem}-{post['slug']}",
                "title": title,
                "week": data.get("week", f.stem),
                "prompts": prompts,
                "postet": posted[title],
            })
    groups.sort(key=lambda g: g["postet"], reverse=True)
    return groups


def render(groups):
    cards = []
    n = 0
    for g in groups:
        items = []
        for s in g["prompts"]:
            n += 1
            label = s.get("label", "")
            if label.lower().startswith(("kopiér", "kopier", "prøv")):
                label = s.get("title", "")
            items.append(f"""
      <div class="prompt">
        <p class="label">{html.escape(label)}</p>
        <p class="text" id="p{n}">{html.escape(s['body'])}</p>
        <button type="button" class="copy" data-target="p{n}">Kopiér prompt</button>
      </div>""")
        cards.append(f"""
    <section class="post" id="{g['id']}">
      <h2>{html.escape(g['title'])}</h2>
      <p class="week">{html.escape(g['week'])}</p>{''.join(items)}
    </section>""")

    return f"""<!doctype html>
<html lang="da">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Prompts fra @hverdag.med.ai</title>
<meta name="description" content="Kopiér prompts fra opslagene på @hverdag.med.ai med ét tryk.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap">
<style>
:root {{ --bg:#F5F0E8; --card:#FFFFFF; --ink:#1E2B2F; --muted:#5F6B66; --green:#2E5E4E; --mustard:#F2B544; --line:#E6DFD2; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font-family:Inter, system-ui, -apple-system, "Segoe UI", sans-serif; line-height:1.5;
  padding:24px max(16px, env(safe-area-inset-right)) 48px max(16px, env(safe-area-inset-left)); }}
main {{ max-width:640px; margin:0 auto; display:grid; gap:20px; }}
header {{ background:var(--green); color:#fff; border-radius:24px; padding:24px; }}
.dots {{ display:flex; gap:7px; align-items:center; margin-bottom:12px; }}
.dots i {{ display:block; border-radius:50%; background:var(--mustard); }}
h1 {{ font-size:28px; font-weight:800; line-height:1.15; margin:0 0 8px; }}
header p {{ margin:0; opacity:.9; }}
.post {{ display:grid; gap:12px; }}
h2 {{ font-size:20px; font-weight:800; margin:8px 0 0; line-height:1.25; }}
.week {{ margin:-8px 0 0; color:var(--muted); font-size:14px; }}
.prompt {{ background:var(--card); border-radius:18px; padding:18px; display:grid; gap:10px; border-left:6px solid var(--mustard); }}
.label {{ margin:0; font-size:13px; font-weight:600; letter-spacing:.04em; text-transform:uppercase; color:var(--muted); }}
.text {{ margin:0; font-size:17px; white-space:pre-wrap; user-select:text; -webkit-user-select:text; }}
.copy {{ justify-self:start; font:inherit; font-weight:600; font-size:16px; border:0; border-radius:999px; padding:12px 20px; background:var(--green); color:#fff; cursor:pointer; }}
.copy.done {{ background:var(--mustard); color:var(--ink); }}
.copy:focus-visible {{ outline:3px solid var(--mustard); outline-offset:2px; }}
.empty {{ background:var(--card); border-radius:18px; padding:18px; margin:0; }}
footer {{ text-align:center; color:var(--muted); font-size:14px; }}
footer a {{ color:var(--green); }}
</style>
</head>
<body>
<main>
  <header>
    <div class="dots" aria-hidden="true"><i style="width:9px;height:9px"></i><i style="width:12px;height:12px"></i><i style="width:15px;height:15px"></i></div>
    <h1>Prompts fra @hverdag.med.ai</h1>
    <p>Tryk på knappen for at kopiere en prompt. Sæt den ind i din AI-assistent, og udskift teksten i [klammer] med dine egne detaljer.</p>
  </header>
{''.join(cards) if cards else '<p class="empty">De første prompts kommer snart. Kig forbi igen, når der er nye opslag på profilen.</p>'}
  <footer>Nye prompts hver uge på <a href="https://www.instagram.com/hverdag.med.ai/">@hverdag.med.ai</a></footer>
</main>
<script>
function fallbackCopy(text) {{
  var ta = document.createElement('textarea');
  ta.value = text; ta.setAttribute('readonly', '');
  ta.style.position = 'absolute'; ta.style.left = '-9999px';
  document.body.appendChild(ta); ta.select(); ta.setSelectionRange(0, text.length);
  var ok = false; try {{ ok = document.execCommand('copy'); }} catch (e) {{}}
  document.body.removeChild(ta); return ok;
}}
function selectText(el) {{
  var r = document.createRange(); r.selectNodeContents(el);
  var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
}}
document.querySelectorAll('.copy').forEach(function (btn) {{
  btn.addEventListener('click', function () {{
    var el = document.getElementById(btn.dataset.target);
    var text = el.textContent;
    function done(ok) {{
      if (ok) {{ btn.textContent = 'Kopieret ✓'; btn.classList.add('done'); }}
      else {{ selectText(el); btn.textContent = 'Markeret – tryk Kopiér'; }}
      setTimeout(function () {{ btn.textContent = 'Kopiér prompt'; btn.classList.remove('done'); }}, 2500);
    }}
    if (navigator.clipboard && window.isSecureContext) {{
      navigator.clipboard.writeText(text).then(function () {{ done(true); }}, function () {{ done(fallbackCopy(text)); }});
    }} else {{ done(fallbackCopy(text)); }}
  }});
}});
</script>
</body>
</html>
"""


if __name__ == "__main__":
    groups = collect()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(groups), encoding="utf-8")
    print(f"Prompt-side bygget: {sum(len(g['prompts']) for g in groups)} prompts fra {len(groups)} opslag → {OUT.relative_to(ROOT)}")
