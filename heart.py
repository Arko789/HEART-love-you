"""
heart.py - text geometry for the Love Heart page.

Computes where every phrase sits inside the heart (rows, spans, sizes,
colours, spawn order) and writes it to layout.js.
index.html loads layout.js + music.mp3 and plays the animation.

Run:  python heart.py
"""
import json
import math as m
import random

SC = 21          # heart scale
OY = 20          # vertical offset
GAP = 7
SIZES_PT = (9, 10, 11, 12)
FONT = "Arial"

PHRASES = [
    "I love you", "Seni seviyorum", "Te amo", "Je t'aime",
    "Ich liebe dich", "Ti amo", "Eu te amo", "Я тебя люблю",
    "사랑해", "愛してる", "我爱你", "मैं तुमसे प्यार करता हूँ",
    "Σ' αγαπώ", "Ik hou van jou", "Jag älskar dig", "Kocham cię",
    "ฉันรักเธอ", "Anh yêu em", "Aku cinta kamu", "Я тебе кохаю",
]

# ---- text measuring: real Tk fonts if available, else an estimate ----
_tk = None
try:
    import tkinter as tk
    import tkinter.font as tkf
    _tk = tk.Tk()
    _tk.withdraw()
except Exception:
    _tk = None

_fonts = {}


def _font(px):
    if px not in _fonts:
        _fonts[px] = tkf.Font(root=_tk, family=FONT, size=-int(round(px)), weight="bold")
    return _fonts[px]


def measure(text, px):
    if _tk:
        return _font(px).measure(text)
    w = 0
    for ch in text:
        o = ord(ch)
        w += px * (1.0 if o >= 0x2E80 else 0.62 if 0x0900 <= o < 0x0E80 or 0x0E00 <= o < 0x0E80 else 0.58)
    return w


def linespace(px):
    return _font(px).metrics("linespace") if _tk else px * 1.2


# ---- heart geometry ----
def heart(a):
    x = 16 * (m.sin(a) ** 3)
    y = 13 * m.cos(a) - 5 * m.cos(2 * a) - 2 * m.cos(3 * a) - m.cos(4 * a)
    return x * SC, y * SC + OY


POLY = [heart(2 * m.pi * i / 720) for i in range(720)]
EDGES = list(zip(POLY, POLY[1:] + POLY[:1]))
YMAX = max(p[1] for p in POLY)
YMIN = min(p[1] for p in POLY)
CY = (YMAX + YMIN) / 2


def spans(y):
    xs = []
    for (x1, y1), (x2, y2) in EDGES:
        if (y1 <= y < y2) or (y2 <= y < y1):
            xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
    xs.sort()
    return list(zip(xs[0::2], xs[1::2]))


def intersect(A, B):
    out = []
    for a in A:
        for b in B:
            lo, hi = max(a[0], b[0]), min(a[1], b[1])
            if hi - lo > 14:
                out.append((lo, hi))
    return out


def mix(a, b, k):
    return tuple(p + (q - p) * k for p, q in zip(a, b))


def rad_of(x, y):
    return m.hypot(x / (16 * SC), (y - CY) / (14.5 * SC))


def make_layout(font_scale, seed=11):
    rng = random.Random(seed)
    sizes = [round(s * 4 / 3 * font_scale, 1) for s in SIZES_PT]
    gap = GAP * font_scale

    def cycle():
        while True:
            order = PHRASES[:]
            rng.shuffle(order)
            yield from order

    nxt = cycle()
    row_h = max(linespace(z) for z in sizes) + 4 * font_scale
    half = row_h / 2
    placed = []

    y = YMAX - half
    while y > YMIN + half:
        for lo, hi in intersect(spans(y + half), spans(y - half)):
            lo += 4
            hi -= 4
            cur = lo + rng.uniform(0, 8)
            line = []
            while True:
                fit = None
                for _ in range(10):
                    text = next(nxt)
                    size = rng.choice(sizes)
                    w = measure(text, size)
                    if cur + w <= hi:
                        fit = (text, size, w)
                        break
                if not fit:
                    break
                text, size, w = fit
                line.append([cur + w / 2, text, size, w])
                cur += w + gap
            if not line:
                continue
            if len(line) > 1:
                left = hi - (line[-1][0] + line[-1][3] / 2)
                for i, it in enumerate(line):
                    it[0] += left * i / (len(line) - 1)
            else:
                line[0][0] = (lo + hi) / 2
            for i, (x, text, size, w) in enumerate(line):
                placed.append(dict(x=x, y=y, text=text, size=size,
                                   edge=(i == 0 or i == len(line) - 1)))
        y -= row_h

    wine, crimson, blood = (0.58, 0.0, 0.09), (0.90, 0.05, 0.14), (0.98, 0.10, 0.16)
    for p in placed:
        rad = min(1.0, rad_of(p["x"], p["y"]))
        base = mix(wine, crimson, 0.25 + 0.75 * rad)
        base = mix(base, blood, rng.uniform(0, 0.35) + (0.3 if p["edge"] else 0))
        p["color"] = [round(min(1, v), 3) for v in base]
        p["rad"] = rad
        p["dx"] = round(rng.uniform(-10, 10), 1)

    edges = [p for p in placed if p["edge"]]
    inner = [p for p in placed if not p["edge"]]
    edges.sort(key=lambda p: m.atan2(p["x"], p["y"] - CY) % (2 * m.pi))
    inner.sort(key=lambda p: -p["rad"] + rng.uniform(0, 0.08))

    return [dict(x=round(p["x"], 1), y=round(p["y"], 1), t=p["text"],
                 s=p["size"], c=p["color"], dx=p["dx"]) for p in edges + inner]


if __name__ == "__main__":
    data = {
        "cy": round(CY, 1),
        "wide": make_layout(1.0),      # desktop / landscape
        "narrow": make_layout(1.4),    # phones / portrait (bigger text)
    }
    with open("layout.js", "w", encoding="utf-8") as f:
        f.write("const LAYOUTS = " + json.dumps(data, ensure_ascii=False) + ";\n")
    print("layout.js written:", len(data["wide"]), "words (wide),",
          len(data["narrow"]), "words (narrow)",
          "| measured with", "Tk" if _tk else "estimate")
