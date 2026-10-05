#!/usr/bin/env python3
"""Generate assets/hero.svg — the terminal-window header of the profile README.

    python3 scripts/gen_hero.py

Edit the DATA block at the bottom, re-run, commit the SVG. CI fails if the
committed file drifts from this script's output.

Design constraints worth knowing before editing:
  * GitHub serves this through <img>, so no web fonts and no scripts — only
    system font stacks, and CSS animations (which honour reduced-motion).
  * Monospace runs use <tspan> flow instead of hand-placed x positions, so a
    narrower mono face (Consolas) can't make words collide.
  * The card scales down on phones; everything in it is repeated as real
    text in the README, so nothing here is the only copy of a fact.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "hero.svg")

# GitHub dark palette, so the card sits naturally next to code blocks.
BG, BAR, BORDER = "#0A0A0B", "#111315", "#2A2A2D"
TEXT, MUTED, DIM = "#F5F1E8", "#B9B0A2", "#7C746A"
BLUE, GREEN, PURPLE = "#8AB4F8", "#B9D97A", "#CDB8FF"
ORANGE, RED, YELLOW = "#F0B35A", "#F26D6D", "#E6C76C"

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

W, H = 1000, 300
BAR_H, STATUS_H = 38, 30
LEFT, SPLIT, RIGHT = 44, 592, 626


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def prompt(y, command=""):
    """`~ $ command` as one flowing text run."""
    return (f'<text x="{LEFT}" y="{y}" font-family="{MONO}" font-size="14">'
            f'<tspan fill="{BLUE}">~</tspan><tspan fill="{DIM}"> $ </tspan>'
            f'<tspan fill="{TEXT}">{esc(command)}</tspan></text>')


def build(d):
    a = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
         f'height="{H}" fill="none" role="img" aria-label="{esc(d["aria"])}">']

    n = len(d["loop"])
    step = 100 / n
    a.append(
        "<style>"
        ".cur{animation:blink 1.1s steps(1,end) infinite}"
        f"@keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}"
        f".w{{fill:{DIM};animation:lit {n * 2}s steps(1,end) infinite}}"
        + "".join(f".w{i}{{animation-delay:{i * 2}s}}" for i in range(1, n))
        + f"@keyframes lit{{0%{{fill:{GREEN}}}{step:g}%,100%{{fill:{DIM}}}}}"
        "@media (prefers-reduced-motion:reduce){.cur,.w{animation:none}}"
        "</style>")

    a.append(f'<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>')
    a.append('<g clip-path="url(#c)">')
    a.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    # ── title bar ──
    a.append(f'<rect width="{W}" height="{BAR_H}" fill="{BAR}"/>')
    a.append(f'<rect y="{BAR_H - 1}" width="{W}" height="1" fill="{BORDER}"/>')
    for i, c in enumerate((RED, YELLOW, GREEN)):
        a.append(f'<circle cx="{24 + i * 20}" cy="{BAR_H / 2}" r="6" fill="{c}" opacity="0.85"/>')
    a.append(f'<text x="{W / 2}" y="{BAR_H / 2 + 4.5}" font-family="{MONO}" font-size="12.5" '
             f'fill="{MUTED}" text-anchor="middle">{esc(d["title"])}</text>')

    # ── left: who ──
    a.append(prompt(92, "whoami"))
    a.append(f'<text x="{LEFT - 3}" y="152" font-family="{SANS}" font-size="52" '
             f'font-weight="700" letter-spacing="-1.5" fill="#F0F6FC">{esc(d["name"])}</text>')
    roles = f'<tspan fill="{DIM}"> · </tspan>'.join(
        f'<tspan fill="{GREEN if i == len(d["roles"]) - 1 else TEXT}">{esc(r)}</tspan>'
        for i, r in enumerate(d["roles"]))
    a.append(f'<text x="{LEFT}" y="188" font-family="{SANS}" font-size="16.5">{roles}</text>')

    a.append(prompt(238))
    cursor_x = LEFT + len("~ $ ") * 14 * 0.6
    a.append(f'<rect class="cur" x="{cursor_x:.1f}" y="226" width="8.5" height="16" fill="{TEXT}"/>')

    # ── divider ──
    a.append(f'<rect x="{SPLIT}" y="{BAR_H + 30}" width="1" height="{H - BAR_H - STATUS_H - 60}" '
             f'fill="{BORDER}"/>')

    # ── right: neofetch-style facts ──
    a.append(f'<text x="{RIGHT}" y="82" font-family="{MONO}" font-size="14" font-weight="700">'
             f'<tspan fill="{GREEN}">{esc(d["user"])}</tspan><tspan fill="{DIM}">@</tspan>'
             f'<tspan fill="{GREEN}">{esc(d["host"])}</tspan></text>')
    a.append(f'<text x="{RIGHT}" y="98" font-family="{MONO}" font-size="14" fill="{DIM}">'
             f'{"─" * (len(d["user"]) + len(d["host"]) + 1)}</text>')
    for i, (k, v) in enumerate(d["facts"]):
        y = 124 + i * 24
        a.append(f'<text x="{RIGHT}" y="{y}" font-family="{MONO}" font-size="13" fill="{BLUE}">{esc(k)}</text>')
        a.append(f'<text x="{RIGHT + 60}" y="{y}" font-family="{MONO}" font-size="13" fill="{TEXT}">{esc(v)}</text>')
    for i, c in enumerate((RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, TEXT, DIM)):
        a.append(f'<rect x="{RIGHT + i * 22}" y="{124 + len(d["facts"]) * 24 - 6}" '
                 f'width="18" height="10" rx="2" fill="{c}"/>')

    # ── status bar: the loop ──
    sy = H - STATUS_H
    a.append(f'<rect y="{sy}" width="{W}" height="{STATUS_H}" fill="{BAR}"/>')
    a.append(f'<rect y="{sy}" width="{W}" height="1" fill="{BORDER}"/>')
    a.append(f'<rect x="0" y="{sy}" width="64" height="{STATUS_H}" fill="{GREEN}"/>')
    a.append(f'<text x="32" y="{sy + 19.5}" font-family="{MONO}" font-size="11.5" font-weight="700" '
             f'fill="{BG}" text-anchor="middle" letter-spacing="1">LOOP</text>')
    words = f'<tspan fill="{DIM}">  →  </tspan>'.join(
        f'<tspan class="w w{i}">{esc(w)}</tspan>' for i, w in enumerate(d["loop"]))
    a.append(f'<text x="80" y="{sy + 19.5}" font-family="{MONO}" font-size="12.5" '
             f'xml:space="preserve">{words}</text>')
    a.append(f'<text x="{W - 20}" y="{sy + 19.5}" font-family="{MONO}" font-size="12.5" '
             f'fill="{MUTED}" text-anchor="end">{esc(d["status_right"])}</text>')

    a.append("</g>")
    a.append(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" '
             f'stroke="{BORDER}"/>')
    a.append("</svg>")
    return "".join(a) + "\n"


# ══════════════════════════════════════════════════════════════════════════
# DATA — edit here, then re-run
# ══════════════════════════════════════════════════════════════════════════
HERO = {
    "aria": "Yash Waghmare — Software Engineer, Full-Stack Developer, Builder. "
            "WebOps Head at Spirit IIT Guwahati; Senior Web Developer at SWC IIT Guwahati.",
    "title": "yash@portfolio: ~",
    "name": "Yash Waghmare",
    "roles": ["Full-Stack Developer", "Web Engineer", "Builder"],
    "user": "yash",
    "host": "portfolio",
    "facts": [
        ("role", "WebOps Head · Spirit IITG"),
        ("also", "Sr. Web Dev · SWC IITG"),
        ("edu", "B.Tech · IIT Guwahati"),
        ("stack", "TypeScript · Node · React · Python"),
        ("focus", "backend · AI agents · design"),
    ],
    "loop": ["build", "ship", "learn", "repeat"],
    "status_right": "portfolio / github",
}


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build(HERO))
    print(f"wrote {OUT}  {os.path.getsize(OUT)} bytes")
