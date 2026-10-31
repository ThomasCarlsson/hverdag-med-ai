"""Lægger en færdig uge i køen.

Brug: python3 scripts/enqueue.py <uge.json> <out/uge-NN-mappe> <mandagsdato YYYY-MM-DD>

Laver en mappe pr. opslag i queue/ med JPEG-billeder og opslag.json.
Tidspunkter: hverdage og weekend efter config.json (standard 19:00 og 10:00, dansk tid).
"""
import json
import sys
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
TZ = ZoneInfo(CONFIG.get("tidszone", "Europe/Copenhagen"))
DAYS = {"mandag": 0, "tirsdag": 1, "onsdag": 2, "torsdag": 3, "fredag": 4, "lørdag": 5, "søndag": 6}


def main(content_path, week_dir, monday):
    data = json.loads(Path(content_path).read_text(encoding="utf-8"))
    week_dir = Path(week_dir)
    monday = date.fromisoformat(monday)
    hverdag = time.fromisoformat(CONFIG.get("tid_hverdag", "19:00"))
    weekend = time.fromisoformat(CONFIG.get("tid_weekend", "10:00"))
    for post in data["posts"]:
        offset = DAYS[post["day"].lower()]
        d = monday + timedelta(days=offset)
        t = weekend if offset >= 5 else hverdag
        when = datetime.combine(d, t, tzinfo=TZ)
        name = f"{d.isoformat()}-{t.strftime('%H%M')}-{post['slug'].split('-', 1)[-1]}"
        dest = ROOT / "queue" / name
        dest.mkdir(parents=True, exist_ok=True)
        src = week_dir / post["slug"]
        images = []
        for png in sorted(src.glob("*.png")):
            jpg = dest / (png.stem + ".jpg")
            Image.open(png).convert("RGB").save(jpg, "JPEG", quality=92, optimize=True)
            images.append(jpg.name)
        caption = post["caption"] + "\n\n" + " ".join(post["hashtags"])
        opslag = {
            "tidspunkt": when.isoformat(),
            "status": "klar",
            "type": "billede" if len(images) == 1 else "karrusel",
            "titel": post["cover"]["title"] if "cover" in post else post.get("tip", ""),
            "billeder": images,
            "billedtekst": caption,
            "note": "",
        }
        (dest / "opslag.json").write_text(json.dumps(opslag, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{name}: {len(images)} billede(r), {when:%a %d.%m kl. %H:%M}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
