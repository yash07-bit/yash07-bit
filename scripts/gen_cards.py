#!/usr/bin/env python3
"""Generate assets/hero.svg and assets/stack.svg.

Both cards are self-hosted on purpose: nothing above the fold on the profile
should depend on a third-party image service that can rate-limit or 404.

    python3 scripts/gen_cards.py

Edit the DATA block at the bottom, re-run, commit the SVGs.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (BG, CYAN, SKY, INDIGO, VIOLET, FUCHSIA, GREEN, TEXT, MUTED,
                   DIM, MONO, SANS, text_w, esc, cut_rect, corner_bracket,
                   defs_aurora, defs_grid, layer_grid, layer_stars)

OUTDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")


# ── shared pieces ─────────────────────────────────────────────────────────
def hud_frame(w, h, color=CYAN, arm=18, inset=14, opacity=0.45, bottom=True):
    out = [corner_bracket(inset, inset, arm, +1, +1, color, opacity),
           corner_bracket(w - inset, inset, arm, -1, +1, color, opacity)]
    if bottom:
        out += [corner_bracket(inset, h - inset, arm, +1, -1, color, opacity),
                corner_bracket(w - inset, h - inset, arm, -1, -1, color, opacity)]
    return "".join(out)


def scanline(w, h, uid, dur=7, opacity=0.5):
    """A CRT sweep travelling down the card."""
    return (f'<rect x="0" y="0" width="{w}" height="2" fill="url(#scan{uid})" opacity="{opacity}">'
            f'<animate attributeName="y" values="-4;{h}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;{opacity};{opacity};0" '
            f'dur="{dur}s" repeatCount="indefinite"/></rect>')


def defs_scan(uid):
    return (f'<linearGradient id="scan{uid}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>'
            f'<stop offset="0.5" stop-color="{CYAN}" stop-opacity="0.85"/>'
            f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>')


def chip(x, y, w, h, label, color, *, mono=True, size=12.5, tracking=1.0,
         fill_op=0.09, stroke_op=0.40, cut=7, pulse=None, dot=False,
         text_color=None):
    """A cut-corner tag. `pulse` staggers a breathing border for wave effects."""
    out = [f'<path d="{cut_rect(x, y, w, h, cut)}" fill="{color}" fill-opacity="{fill_op}" '
           f'stroke="{color}" stroke-opacity="{stroke_op}" stroke-width="1">']
    if pulse is not None:
        out.append(f'<animate attributeName="stroke-opacity" '
                   f'values="{stroke_op};{min(stroke_op + 0.45, 1):.2f};{stroke_op}" '
                   f'dur="5s" begin="{pulse:.2f}s" repeatCount="indefinite"/>')
    out.append("</path>")
    tx = x + w / 2
    if dot:
        cx = x + 15
        cy = y + h / 2
        out.append(f'<circle cx="{cx}" cy="{cy}" r="3.6" fill="{GREEN}">'
                   f'<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="3.6" fill="{GREEN}" opacity="0.55">'
                   f'<animate attributeName="r" values="3.6;10;3.6" dur="2s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="0.5;0;0.5" dur="2s" repeatCount="indefinite"/></circle>')
        tx += 9
    fam = MONO if mono else SANS
    out.append(f'<text x="{tx:.1f}" y="{y + h/2 + size*0.36:.1f}" font-family="{fam}" '
               f'font-size="{size}" fill="{text_color or color}" text-anchor="middle" '
               f'letter-spacing="{tracking}">{esc(label)}</text>')
    return "".join(out)


def chip_w(label, size=12.5, tracking=1.0, mono=True, pad=17, dot=False):
    return round(text_w(label, size, mono=mono, tracking=tracking) + 2 * pad + (18 if dot else 0))


# ══════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════
def perspective_floor(w, y_h, y_b, uid, lines=7, spokes=8, dur=3.6):
    """Synthwave grid: spokes to a vanishing point, plus rungs that scroll.

    Each rung animates from its own position to the next one's, so the set
    reads as one continuously receding surface rather than N blinking lines.
    """
    depth = y_b - y_h
    ys = [y_h + depth * ((k / lines) ** 1.7) for k in range(lines + 1)]
    ops = [min(0.03 + 0.34 * (k / lines) ** 1.5, 0.38) for k in range(lines + 1)]

    out = [f'<g stroke="{CYAN}" fill="none" stroke-width="1">']
    # spokes converging on the vanishing point
    for i in range(-spokes, spokes + 1):
        xb = w / 2 + i * 185
        o = max(0.24 * (1 - abs(i) / (spokes + 2)), 0.035)
        out.append(f'<line x1="{w/2}" y1="{y_h}" x2="{xb:.0f}" y2="{y_b}" stroke-opacity="{o:.3f}"/>')
    # rungs, each stepping into the next rung's slot on every cycle
    for k in range(lines):
        y0, y1 = ys[k], ys[k + 1]
        o0, o1 = ops[k], ops[k + 1]
        out.append(
            f'<line x1="0" y1="{y0:.1f}" x2="{w}" y2="{y0:.1f}" stroke-opacity="{o0:.3f}">'
            f'<animate attributeName="y1" values="{y0:.1f};{y1:.1f}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y2" values="{y0:.1f};{y1:.1f}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values="{o0:.3f};{o1:.3f}" dur="{dur}s" repeatCount="indefinite"/>'
            f'</line>')
    out.append("</g>")
    # a small pulse sitting on the vanishing point, to give the floor a focus
    out.append(f'<circle cx="{w/2}" cy="{y_h}" r="2.2" fill="{CYAN}" opacity="0.9"/>'
               f'<circle cx="{w/2}" cy="{y_h}" r="2.2" fill="{CYAN}" opacity="0.5">'
               f'<animate attributeName="r" values="2.2;16;2.2" dur="4s" repeatCount="indefinite"/>'
               f'<animate attributeName="opacity" values="0.45;0;0.45" dur="4s" repeatCount="indefinite"/>'
               f'</circle>')
    return "".join(out)


def typewriter(phrases, cx, y, uid, size=15.5, tracking=4.5,
               type_s=1.3, hold_s=2.7, wipe_s=0.5):
    """Cycling type-on subtitle, done with an animated clip per phrase.

    No third-party typing service: the whole cycle is one discrete keyframe
    list per phrase, so it survives being embedded as a plain <img>.

    Every list is padded to span keyTimes 0..1 — SMIL drops an animation whose
    keyTimes do not start at 0 and end at 1, which silently blanks any phrase
    whose slot begins later in the cycle.
    """
    slot = type_s + hold_s + wipe_s
    total = slot * len(phrases)
    out, defs = [], []

    for p, raw in enumerate(phrases):
        s_up = raw.upper()
        n = len(s_up)
        full = text_w(s_up, size, mono=True, tracking=tracking)
        x0 = cx - full / 2
        t0 = p * slot

        # (keyTime, clip width) — collapsed before the slot, typed, held, wiped
        frames = [(0.0, 0.0)]
        for i in range(n + 1):
            frames.append(((t0 + type_s * i / n) / total, full * i / n))
        frames.append(((t0 + type_s + hold_s) / total, full))
        for i in range(n, -1, -1):
            frames.append(((t0 + type_s + hold_s + wipe_s * (n - i) / n) / total,
                           full * i / n))
        frames.append((1.0, 0.0))
        frames = [(min(max(k, 0.0), 1.0), v) for k, v in frames]
        frames.sort(key=lambda f: f[0])

        ks = ";".join(f"{k:.5f}" for k, _ in frames)
        vs = ";".join(f"{v:.1f}" for _, v in frames)
        cs = ";".join(f"{x0 + v:.1f}" for _, v in frames)

        defs.append(
            f'<clipPath id="tc{uid}{p}"><rect x="{x0:.1f}" y="{y - size:.1f}" '
            f'width="0" height="{size * 1.6:.1f}">'
            f'<animate attributeName="width" values="{vs}" keyTimes="{ks}" '
            f'calcMode="discrete" dur="{total}s" repeatCount="indefinite"/></rect></clipPath>')

        out.append(f'<g clip-path="url(#tc{uid}{p})">'
                   f'<text x="{cx}" y="{y}" font-family="{MONO}" font-size="{size}" '
                   f'fill="{MUTED}" text-anchor="middle" letter-spacing="{tracking}">'
                   f'{esc(s_up)}</text></g>')

        # the caret rides the same frames, and only shows inside this phrase's slot
        # discrete: value i spans [keyTimes[i], keyTimes[i+1]), so the segment
        # after the slot must already be 0 or the caret never goes away
        vis = "0;1;0;0"
        vis_k = (f"0.00000;{max(t0 / total, 0.0):.5f};"
                 f"{min((t0 + slot) / total, 1.0):.5f};1.00000")
        out.append(
            f'<rect x="{x0:.1f}" y="{y - size + 1:.1f}" width="2" height="{size:.1f}" '
            f'fill="{CYAN}" opacity="0">'
            f'<animate attributeName="x" values="{cs}" keyTimes="{ks}" calcMode="discrete" '
            f'dur="{total}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{vis}" keyTimes="{vis_k}" '
            f'calcMode="discrete" dur="{total}s" repeatCount="indefinite"/>'
            f'<animate attributeName="fill-opacity" values="1;1;0.1;0.1" keyTimes="0;0.5;0.5;1" '
            f'calcMode="discrete" dur="1s" repeatCount="indefinite"/>'
            f'</rect>')

    return "".join(defs), "".join(out)


def build_hero(d):
    W, H = 1200, 400
    Y_HORIZON, uid = 302, "h"
    a = []

    a.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
             f'height="{H}" fill="none" role="img" aria-label="{esc(d["aria"])}">')

    tdefs, tbody = typewriter(d["phrases"], W / 2, 206, uid)
    a.append("<defs>")
    a.append(defs_aurora(uid))
    a.append(defs_grid(uid, W, H, cell=40, fade_to=Y_HORIZON / H))
    a.append(defs_scan(uid))
    a.append(f'<clipPath id="cl{uid}"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    a.append(f'<linearGradient id="wm{uid}" x1="0" y1="0" x2="1" y2="0.35">'
             f'<stop offset="0" stop-color="{CYAN}"/><stop offset="0.45" stop-color="{INDIGO}"/>'
             f'<stop offset="1" stop-color="{FUCHSIA}"/>'
             f'<animate attributeName="x2" values="1;1.55;1" dur="9s" repeatCount="indefinite"/></linearGradient>')
    a.append(f'<linearGradient id="hz{uid}" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>'
             f'<stop offset="0.5" stop-color="{CYAN}" stop-opacity="0.9"/>'
             f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>')
    a.append(f'<linearGradient id="rl{uid}" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{SKY}" stop-opacity="0"/>'
             f'<stop offset="0.5" stop-color="{INDIGO}"/>'
             f'<stop offset="1" stop-color="{FUCHSIA}" stop-opacity="0"/></linearGradient>')
    a.append(f'<filter id="gl{uid}" x="-30%" y="-60%" width="160%" height="260%">'
             f'<feGaussianBlur stdDeviation="20"/></filter>')
    a.append(f'<filter id="hb{uid}" x="-20%" y="-400%" width="140%" height="900%">'
             f'<feGaussianBlur stdDeviation="14"/></filter>')
    a.append(tdefs)
    a.append("</defs>")

    a.append(f'<g clip-path="url(#cl{uid})">')
    a.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    # aurora
    a.append(f'<g filter="url(#bl{uid})" opacity="0.75">'
             f'<ellipse cx="230" cy="70" rx="250" ry="150" fill="url(#au1{uid})">'
             f'<animate attributeName="cx" values="230;400;230" dur="16s" repeatCount="indefinite"/>'
             f'<animate attributeName="cy" values="70;140;70" dur="23s" repeatCount="indefinite"/></ellipse>'
             f'<ellipse cx="930" cy="250" rx="270" ry="160" fill="url(#au2{uid})">'
             f'<animate attributeName="cy" values="250;150;250" dur="19s" repeatCount="indefinite"/>'
             f'<animate attributeName="cx" values="930;780;930" dur="27s" repeatCount="indefinite"/></ellipse>'
             f'<ellipse cx="600" cy="10" rx="230" ry="130" fill="url(#au3{uid})">'
             f'<animate attributeName="cx" values="600;800;600" dur="21s" repeatCount="indefinite"/></ellipse>'
             f'<ellipse cx="1130" cy="60" rx="200" ry="130" fill="url(#au4{uid})" opacity="0.7">'
             f'<animate attributeName="cy" values="60;150;60" dur="25s" repeatCount="indefinite"/></ellipse></g>')

    a.append(layer_grid(uid, W, H, opacity=0.055))
    a.append(layer_stars(uid, W, Y_HORIZON - 30, n=46, seed=11, y0=24))

    # ── the floor ──
    a.append(perspective_floor(W, Y_HORIZON, H + 6, uid))
    a.append(f'<ellipse cx="{W/2}" cy="{Y_HORIZON}" rx="430" ry="8" fill="{CYAN}" '
             f'opacity="0.22" filter="url(#hb{uid})"/>')
    a.append(f'<rect x="0" y="{Y_HORIZON}" width="{W}" height="1.2" fill="url(#hz{uid})" opacity="0.6"/>')

    # ── HUD chrome ──
    a.append(hud_frame(W, H, bottom=False))
    a.append(f'<text x="44" y="44" font-family="{MONO}" font-size="11" fill="{DIM}" '
             f'letter-spacing="2.4">{esc(d["tag_left"])}</text>')
    a.append(f'<circle cx="{W-150}" cy="40" r="3.2" fill="{GREEN}">'
             f'<animate attributeName="opacity" values="1;0.25;1" dur="2s" repeatCount="indefinite"/></circle>')
    a.append(f'<text x="{W-44}" y="44" font-family="{MONO}" font-size="11" fill="{DIM}" '
             f'text-anchor="end" letter-spacing="2.4">{esc(d["tag_right"])}</text>')

    # ── wordmark: glow, chroma split, then the solid gradient on top ──
    name = esc(d["name"])
    wm = (f'font-family="{SANS}" font-size="84" font-weight="800" text-anchor="middle" '
          f'letter-spacing="-3"')
    a.append(f'<text x="{W/2}" y="160" {wm} fill="url(#wm{uid})" filter="url(#gl{uid})" '
             f'opacity="0.5">{name}</text>')
    for color, shift, seed in ((CYAN, -3, "0 0;-3 1;0 0;0 0;2 -1;0 0;0 0;0 0"),
                               (FUCHSIA, 3, "0 0;3 -1;0 0;0 0;-2 1;0 0;0 0;0 0")):
        a.append(f'<g opacity="0.55"><animateTransform attributeName="transform" type="translate" '
                 f'values="{seed}" dur="7s" calcMode="discrete" repeatCount="indefinite"/>'
                 f'<text x="{W/2 + shift}" y="160" {wm} fill="{color}" opacity="0.35">{name}</text></g>')
    a.append(f'<text x="{W/2}" y="160" {wm} fill="url(#wm{uid})">{name}</text>')

    # ── typed subtitle + rule ──
    a.append(tbody)
    a.append(f'<rect x="{W/2 - 160}" y="228" width="320" height="2" fill="url(#rl{uid})" opacity="0.85"/>')

    # ── status chips ──
    chips, gap, ch = d["chips"], 14, 38
    widths = [chip_w(c["label"], dot=c.get("dot", False)) for c in chips]
    x = (W - (sum(widths) + gap * (len(chips) - 1))) / 2
    for c, w in zip(chips, widths):
        a.append(chip(x, 246, w, ch, c["label"], c["color"], dot=c.get("dot", False),
                      text_color="#CBD5E1", fill_op=0.07, stroke_op=0.30))
        x += w + gap

    a.append(scanline(W, H, uid))
    a.append("</g>")
    a.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" '
             f'stroke="#FFFFFF" stroke-opacity="0.10"/>')
    a.append("</svg>")
    return "".join(a)


# ══════════════════════════════════════════════════════════════════════════
# STACK
# ══════════════════════════════════════════════════════════════════════════
def build_stack(d):
    W, uid = 1200, "s"
    LABEL_X, CHIP_X, RIGHT = 178, 206, 1122
    ROW_TOP, LINE_H, ROW_GAP, CH = 96, 44, 18, 34
    gap = 11

    # lay out first so the card can be exactly as tall as its contents
    rows, y = [], ROW_TOP
    for cat in d["categories"]:
        lines, cur, cx = [], [], CHIP_X
        for item in cat["items"]:
            w = chip_w(item, size=13, tracking=0.3, mono=False, pad=15)
            if cur and cx + w > RIGHT:
                lines.append(cur); cur, cx = [], CHIP_X
            cur.append((cx, w, item)); cx += w + gap
        if cur:
            lines.append(cur)
        rows.append({"cat": cat, "lines": lines, "y": y})
        y += len(lines) * LINE_H + ROW_GAP
    H = y + 18

    a = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
         f'height="{H}" fill="none" role="img" aria-label="{esc(d["aria"])}">']
    a.append("<defs>")
    a.append(defs_aurora(uid))
    a.append(defs_grid(uid, W, H, cell=40, fade_to=0.9))
    a.append(defs_scan(uid))
    a.append(f'<clipPath id="cl{uid}"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    a.append(f'<linearGradient id="rail{uid}" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{CYAN}" stop-opacity="0.55"/>'
             f'<stop offset="1" stop-color="{FUCHSIA}" stop-opacity="0.55"/></linearGradient>')
    a.append("</defs>")

    a.append(f'<g clip-path="url(#cl{uid})">')
    a.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    a.append(f'<g filter="url(#bl{uid})" opacity="0.5">'
             f'<ellipse cx="110" cy="{H}" rx="250" ry="130" fill="url(#au3{uid})"/>'
             f'<ellipse cx="1090" cy="0" rx="250" ry="130" fill="url(#au2{uid})"/></g>')
    a.append(layer_grid(uid, W, H, opacity=0.05))
    a.append(hud_frame(W, H))

    total = sum(len(c["items"]) for c in d["categories"])
    a.append(f'<text x="44" y="52" font-family="{MONO}" font-size="12.5" fill="{DIM}" '
             f'letter-spacing="2.4">{esc(d["title"])}</text>')
    a.append(f'<text x="{W-44}" y="52" font-family="{MONO}" font-size="12.5" fill="{CYAN}" '
             f'text-anchor="end" letter-spacing="1.4">{total} MODULES · ONLINE</text>')
    a.append(f'<line x1="44" y1="68" x2="{W-44}" y2="68" stroke="#FFFFFF" stroke-opacity="0.08"/>')

    # left rail threading the category nodes together
    first_y = rows[0]["y"] + CH / 2 + 5
    last_y = rows[-1]["y"] + CH / 2 + 5
    a.append(f'<line x1="192" y1="{first_y}" x2="192" y2="{last_y}" stroke="url(#rail{uid})" '
             f'stroke-width="1"/>')

    n = 0
    for r in rows:
        cat, ry = r["cat"], r["y"]
        color = cat["color"]
        cy = ry + CH / 2 + 5
        a.append(f'<circle cx="192" cy="{cy}" r="3.4" fill="{color}"/>')
        a.append(f'<circle cx="192" cy="{cy}" r="3.4" fill="{color}" opacity="0.5">'
                 f'<animate attributeName="r" values="3.4;9;3.4" dur="3.4s" '
                 f'begin="{rows.index(r) * 0.55:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0.45;0;0.45" dur="3.4s" '
                 f'begin="{rows.index(r) * 0.55:.2f}s" repeatCount="indefinite"/></circle>')
        a.append(f'<text x="{LABEL_X}" y="{cy + 4.5}" font-family="{MONO}" font-size="12.5" '
                 f'fill="{DIM}" text-anchor="end" letter-spacing="1.2">{esc(cat["name"])}</text>')
        a.append(f'<text x="{W-44}" y="{cy + 4}" font-family="{MONO}" font-size="11" '
                 f'fill="{color}" fill-opacity="0.45" text-anchor="end" letter-spacing="1.4">'
                 f'{len(cat["items"]):02d}</text>')
        for li, line in enumerate(r["lines"]):
            ly = ry + li * LINE_H
            for cx, cw, item in line:
                a.append(chip(cx, ly + 5, cw, CH, item, color, mono=False, size=13,
                              tracking=0.3, cut=6, pulse=(n % 9) * 0.55, fill_op=0.10,
                              stroke_op=0.36))
                n += 1

    a.append(scanline(W, H, uid, dur=9, opacity=0.35))
    a.append("</g>")
    a.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" '
             f'stroke="#FFFFFF" stroke-opacity="0.10"/>')
    a.append("</svg>")
    return "".join(a)


# ══════════════════════════════════════════════════════════════════════════
# DATA — edit here, then re-run
# ══════════════════════════════════════════════════════════════════════════
HERO = {
    "name": "Yash Waghmare",
    "aria": "Yash Waghmare — Frontend Developer, Full-Stack Builder, IIT Guwahati, "
            "open to SWE internships",
    "tag_left": "SYS://YASH.WAGHMARE",
    "tag_right": "STATUS: BUILDING",
    "phrases": ["Frontend Developer", "Full-Stack Builder", "React · Node · Python"],
    "chips": [
        {"label": "IIT GUWAHATI", "color": CYAN},
        {"label": "WEBOPS HEAD @ SPIRIT", "color": INDIGO},
        {"label": "OPEN TO SWE INTERNSHIPS", "color": FUCHSIA, "dot": True},
    ],
}

STACK = {
    "title": "◈ STACK MANIFEST",
    "aria": "Tech stack — Languages: JavaScript, TypeScript, Python, C++, C, SQL · "
            "Frontend: React, Tailwind CSS, Vite, Framer Motion, Next.js, EJS, Bootstrap · "
            "Backend: Node.js, Express, FastAPI, MongoDB, MySQL, REST APIs · "
            "Tooling: Git, GitHub, VS Code, Postman, Vercel, Netlify, Figma",
    "categories": [
        {"name": "languages", "color": CYAN,
         "items": ["JavaScript", "Python", "C++", "C", "SQL", "HTML5", "CSS3"]},
        {"name": "frontend", "color": SKY,
         "items": ["React", "Tailwind CSS", "Vite", "Framer Motion", "EJS", "Bootstrap"]},
        {"name": "backend", "color": VIOLET,
         "items": ["Node.js", "Express", "FastAPI", "MongoDB", "MySQL", "REST APIs"]},
        {"name": "tooling", "color": FUCHSIA,
         "items": ["Git", "GitHub", "VS Code", "Postman", "Vercel", "Netlify", "Figma"]},
    ],
}


if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    for fname, svg in (("hero.svg", build_hero(HERO)), ("stack.svg", build_stack(STACK))):
        path = os.path.join(OUTDIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {path}  {os.path.getsize(path)} bytes")
