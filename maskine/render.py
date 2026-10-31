"""Gør en ugefil (content/uge-XX.json) til færdige Instagram-karruseller (1080x1350 PNG).

Brug:  python3 render.py content/uge-01.json
Output: out/<uge>/<opslag>/NN.png  +  out/<uge>/oversigt.png
"""
import json
import sys
from pathlib import Path

import subprocess

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
M = 96  # sidemargen

C = {
    "bg": "#F5F0E8",
    "ink": "#1E2B2F",
    "muted": "#66706C",
    "green": "#2E5E4E",
    "green_soft": "#DCE7E1",
    "mustard": "#F2B544",
    "mustard_soft": "#FBEBC6",
    "red": "#B8503A",
    "red_soft": "#F4DCD5",
    "grey_soft": "#E6E1D8",
    "white": "#FFFFFF",
    "cream": "#F5F0E8",
}

THEMES = {
    "green":      {"bg": "#2E5E4E", "circle": "#376B5A", "title": "#FFFFFF", "sub": "#D6E4DD", "kbg": "#F2B544", "kfg": "#1E2B2F", "foot": "#F5F0E8", "line": "#4F7A6B", "mark": "#F2B544"},
    "navy":       {"bg": "#263A5E", "circle": "#2F4670", "title": "#FFFFFF", "sub": "#D3DCEB", "kbg": "#F2B544", "kfg": "#1E2B2F", "foot": "#E9EEF6", "line": "#46597D", "mark": "#F2B544"},
    "mustard":    {"bg": "#F2B544", "circle": "#F5C466", "title": "#1E2B2F", "sub": "#4A3B12", "kbg": "#1E2B2F", "kfg": "#FFFFFF", "foot": "#4A3B12", "line": "#D79E33", "mark": "#1E2B2F"},
    "terracotta": {"bg": "#C8643F", "circle": "#D27652", "title": "#FFFFFF", "sub": "#F7DED3", "kbg": "#F5F0E8", "kfg": "#9E4426", "foot": "#FBEAE2", "line": "#DA8866", "mark": "#F2B544"},
}

ILL_DIR = Path(__file__).parent / "illustrations"
_ill_cache = {}


def illustration(name, width):
    """Renderer en SVG-illustration til PNG med gennemsigtig baggrund."""
    key = (name, width)
    if key not in _ill_cache:
        out = Path("out") / "_ill" / f"{name}-{width}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["rsvg-convert", "-w", str(width), "-o", str(out), str(ILL_DIR / f"{name}.svg")], check=True)
        _ill_cache[key] = Image.open(out).convert("RGBA")
    return _ill_cache[key]


FD = "/usr/share/fonts/opentype/inter/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


def F_title(s):
    return font("InterDisplay-ExtraBold.otf", s)


def F_head(s):
    return font("InterDisplay-Bold.otf", s)


def F_body(s):
    return font("Inter-Regular.otf", s)


def F_med(s):
    return font("Inter-Medium.otf", s)


def F_semi(s):
    return font("Inter-SemiBold.otf", s)


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            test = (cur + " " + w).strip()
            if draw.textlength(test, font=fnt) <= width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, lh=1.3, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    step = int(fnt.size * lh)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


def fit_title(draw, text, width, start, minimum, max_lines, maker=F_title):
    s = start
    while s > minimum:
        f = maker(s)
        if len(wrap(draw, text, f, width)) <= max_lines:
            return f
        s -= 4
    return maker(minimum)


def pill(draw, xy, text, bg, fg, size=30):
    f = F_semi(size)
    x, y = xy
    tw = draw.textlength(text, font=f)
    h = int(size * 1.9)
    draw.rounded_rectangle([x, y, x + tw + size * 1.4, y + h], radius=h // 2, fill=bg)
    draw.text((x + size * 0.7, y + h / 2), text, font=f, fill=fg, anchor="lm")
    return y + h


def footer(draw, account, idx, total, col, line):
    y = H - 118
    draw.line([M, y, W - M, y], fill=line, width=2)
    f = F_med(28)
    draw.text((M, y + 46), account, font=f, fill=col, anchor="lm")
    right = f"{idx}/{total}   Swipe  →" if idx < total else f"{idx}/{total}"
    draw.text((W - M, y + 46), right, font=f, fill=col, anchor="rm")


def brand_mark(draw, x, y, col="#F2B544"):
    """Lille fast kendetegn: tre prikker i stigende størrelse."""
    for i, r in enumerate((7, 10, 13)):
        cx = x + i * 34
        draw.ellipse([cx - r, y - r, cx + r, y + r], fill=col)


def cover(post, account, total):
    t = THEMES[post.get("theme", "green")]
    img = Image.new("RGB", (W, H), t["bg"])
    d = ImageDraw.Draw(img)
    d.ellipse([W - 330, -230, W + 230, 330], fill=t["circle"])
    brand_mark(d, M + 13, 120, t["mark"])
    y = 190
    y = pill(d, (M, y), post["cover"]["kicker"], t["kbg"], t["kfg"], 30) + 44
    tf = fit_title(d, post["cover"]["title"], W - 2 * M, 100, 68, 3)
    y = text_block(d, (M, y), post["cover"]["title"], tf, t["title"], W - 2 * M, lh=1.06) + 28
    text_block(d, (M, y), post["cover"]["subtitle"], F_body(38), t["sub"], W - 2 * M, lh=1.35, max_lines=2)
    if post.get("illustration"):
        ill = illustration(post["illustration"], 820)
        img.paste(ill, ((W - ill.width) // 2, H - 140 - ill.height), ill)
        d = ImageDraw.Draw(img)
    footer(d, account, 1, total, t["foot"], t["line"])
    return img


STYLE = {
    "step": ("green_soft", "green"),
    "compare": ("grey_soft", "ink"),
    "tip": ("mustard_soft", "ink"),
    "mistake": ("red_soft", "red"),
    "prompt": ("mustard", "ink"),
}


def content_slide(s, account, idx, total, theme):
    t = THEMES[theme]
    img = Image.new("RGB", (W, H), C["bg"])
    d = ImageDraw.Draw(img)
    d.ellipse([W - 150, -150, W + 150, 150], fill=t["bg"])
    kind = s["type"]
    pill_bg, pill_fg = STYLE.get(kind, ("green_soft", "green"))
    if kind == "compare" and s["label"].lower() == "nu":
        pill_bg, pill_fg = "green", "white"
    pill_fg_col = C[pill_fg] if pill_fg in C else pill_fg

    def draw_all(d, y):
        return _content_body(d, s, kind, pill_bg, pill_fg_col, y)

    probe = ImageDraw.Draw(Image.new("RGB", (W, H)))
    height = draw_all(probe, 0)
    top, bottom = 150, H - 118 - 60
    y0 = max(top, int(top + (bottom - top - height) / 2 - 40))
    draw_all(d, y0)
    footer(d, account, idx, total, C["muted"], "#D8D1C4")
    return img


def _content_body(d, s, kind, pill_bg, pill_fg_col, y):
    y = pill(d, (M, y), s["label"].upper(), C[pill_bg], pill_fg_col, 28) + 54
    tf = fit_title(d, s["title"], W - 2 * M, 80, 56, 3, maker=F_head)
    y = text_block(d, (M, y), s["title"], tf, C["ink"], W - 2 * M, lh=1.12) + 48

    if kind == "prompt":
        bf = F_med(38)
        inner = W - 2 * M - 2 * 56
        lines = wrap(d, s["body"], bf, inner)
        box_h = len(lines) * int(38 * 1.42) + 2 * 56 + 30
        d.rounded_rectangle([M, y, W - M, y + box_h], radius=28, fill=C["white"])
        d.rectangle([M, y + 28, M + 10, y + box_h - 28], fill=C["mustard"])
        d.text((M + 56, y + 50), "KOPIÉR", font=F_semi(24), fill=C["muted"])
        text_block(d, (M + 56, y + 100), s["body"], bf, C["ink"], inner, lh=1.42)
        return y + box_h
    else:
        if kind == "compare":
            # stor kontrasttekst for før/efter
            accent = C["green"] if s["label"].lower() == "nu" else C["muted"]
            d.rectangle([M, y, M + 120, y + 8], fill=accent)
            y += 50
        return text_block(d, (M, y), s["body"], F_body(46), "#3A4744", W - 2 * M, lh=1.45)


def bookmark_icon(d, x, y, s, col):
    d.polygon([(x, y), (x + s, y), (x + s, y + s * 1.3), (x + s / 2, y + s * 0.95), (x, y + s * 1.3)], fill=col)


def cta_slide(s, account, idx, total, theme, ill_name=None):
    t = THEMES[theme]
    img = Image.new("RGB", (W, H), t["bg"])
    d = ImageDraw.Draw(img)
    d.ellipse([-200, -200, 300, 300], fill=t["circle"])
    bookmark_icon(d, M, 220, 64, t["kbg"] if theme != "mustard" else "#1E2B2F")
    y = 360
    tf = fit_title(d, s["title"], W - 2 * M, 92, 64, 3)
    y = text_block(d, (M, y), s["title"], tf, t["title"], W - 2 * M, lh=1.08) + 36
    text_block(d, (M, y), s["body"], F_body(40), t["sub"], W - 2 * M, lh=1.4, max_lines=3)
    if ill_name:
        ill = illustration(ill_name, 560)
        img.paste(ill, (W - ill.width - 40, H - 150 - ill.height), ill)
        d = ImageDraw.Draw(img)
    footer(d, account, idx, total, t["foot"], t["line"])
    return img


def image_post(post, account):
    """Enkelt billedopslag: tegnet scene i fuld størrelse med tippet i et kort nederst."""
    img = Image.new("RGB", (W, H), C["bg"])
    scene = illustration(post["scene"], W)
    img.paste(scene, (0, 0), scene)
    d = ImageDraw.Draw(img)
    t = THEMES[post.get("theme", "green")]
    pad, inner = 56, W - 2 * 60 - 2 * 56
    tf = fit_title(d, post["tip"], inner, 54, 40, 3, maker=F_head)
    lines = wrap(d, post["tip"], tf, inner)
    card_h = 57 + 34 + len(lines) * int(tf.size * 1.15) + 40 + 40 + pad
    top = H - 60 - card_h
    d.rounded_rectangle([60, top, W - 60, H - 60], radius=36, fill=C["bg"])
    y = pill(d, (60 + pad, top + pad), post["tip_label"].upper(), t["bg"], "#FFFFFF" if post.get("theme") != "mustard" else C["ink"], 28) + 34
    y = text_block(d, (60 + pad, y), post["tip"], tf, C["ink"], inner, lh=1.15) + 22
    d.text((60 + pad, y + 18), account, font=F_med(26), fill=C["muted"], anchor="lm")
    brand_mark(d, W - 60 - pad - 81, y + 18, t["bg"])
    return img


def render_week(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    week_dir = Path("out") / Path(path).stem
    week_dir.mkdir(parents=True, exist_ok=True)
    account = data["account"]
    rows = []
    for post in data["posts"]:
        total = 1 + len(post.get("slides", []))
        pdir = week_dir / post["slug"]
        pdir.mkdir(exist_ok=True)
        theme = post.get("theme", "green")
        ill = post.get("illustration")
        if post.get("type") == "image":
            imgs = [image_post(post, account)]
            pdir.mkdir(exist_ok=True)
            imgs[0].save(pdir / "01.png", optimize=True)
            (pdir / "billedtekst.txt").write_text(post["caption"] + "\n\n" + " ".join(post["hashtags"]) + "\n", encoding="utf-8")
            rows.append((post, imgs))
            print(f"{post['slug']}: 1 billede")
            continue
        imgs = [cover(post, account, total)]
        for i, s in enumerate(post["slides"], start=2):
            if s["type"] == "cta":
                imgs.append(cta_slide(s, account, i, total, theme, ill))
            else:
                imgs.append(content_slide(s, account, i, total, theme))
        for i, im in enumerate(imgs, start=1):
            im.save(pdir / f"{i:02d}.png", optimize=True)
        tags = " ".join(post["hashtags"])
        (pdir / "billedtekst.txt").write_text(post["caption"] + "\n\n" + tags + "\n", encoding="utf-8")
        rows.append((post, imgs))
        print(f"{post['slug']}: {len(imgs)} billeder")
    contact_sheet(rows, data, week_dir / "oversigt.png")


def contact_sheet(rows, data, out):
    tw, th, gap, left, top = 216, 270, 16, 300, 120
    maxn = max(len(r[1]) for r in rows)
    sw = left + maxn * (tw + gap) + 40
    sh = top + len(rows) * (th + 60) + 20
    sheet = Image.new("RGB", (sw, sh), "#FFFFFF")
    d = ImageDraw.Draw(sheet)
    d.text((40, 50), f"{data['account']}  ·  {data['week']}", font=F_head(40), fill=C["ink"])
    y = top
    for post, imgs in rows:
        d.text((40, y + 20), post["day"], font=F_head(30), fill=C["ink"])
        d.text((40, y + 62), post["pillar"], font=F_body(24), fill=C["muted"])
        text_block(d, (40, y + 104), post["cover"]["title"] if "cover" in post else post["tip"], F_body(20), C["muted"], 230, lh=1.3, max_lines=6)
        x = left
        for im in imgs:
            sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
            x += tw + gap
        y += th + 60
    sheet.save(out, optimize=True)


if __name__ == "__main__":
    render_week(sys.argv[1] if len(sys.argv) > 1 else "content/uge-01.json")
