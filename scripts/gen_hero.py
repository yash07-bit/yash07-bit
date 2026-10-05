#!/usr/bin/env python3
"""Generate assets/hero.svg — portfolio-style profile banner.

    python3 scripts/gen_hero.py

The banner is designed to mirror the portfolio's editorial card aesthetic:
paper background, technical grid, crisp black typography, and a warm orange accent.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "hero.svg")

# Portfolio-inspired palette
BG = "#F3F0E8"
GRID = "#D8D4CC"
TEXT = "#111111"
MUTED = "#66615A"
SUB = "#55514B"
WARM = "#FF5A36"
WARM2 = "#FF7A45"
LIGHT = "#F3F0E8"
DARK = "#111111"
SOFT = "#A7A39C"
WHITE = "#FFFFFF"

W, H = 1200, 390


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(d):
    a = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
        "<defs>",
        "  <pattern id=\"grid\" width=\"40\" height=\"40\" patternUnits=\"userSpaceOnUse\">",
        "    <path d=\"M 40 0 L 0 0 0 40\" fill=\"none\" stroke=\"#D8D4CC\" stroke-width=\"1\" opacity=\"0.45\"/>",
        "  </pattern>",
        "  <linearGradient id=\"accent\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"0\">",
        f"    <stop offset=\"0%\" stop-color=\"{WARM}\"/>",
        f"    <stop offset=\"100%\" stop-color=\"{WARM2}\"/>",
        "  </linearGradient>",
        "</defs>",
        f'<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#grid)"/>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="none" stroke="{TEXT}" stroke-width="2"/>',
        f'<text x="42" y="43" font-family="monospace" font-size="13" font-weight="700" letter-spacing="3" fill="{TEXT}">{esc(d["label"])}</text>',
        f'<text x="1158" y="43" text-anchor="end" font-family="monospace" font-size="12" font-weight="700" letter-spacing="2" fill="{MUTED}">{esc(d["status"])}</text>',
        f'<rect x="42" y="72" width="34" height="5" rx="2" fill="url(#accent)"/>',
        f'<text x="42" y="150" font-family="Arial, Helvetica, sans-serif" font-size="72" font-weight="800" letter-spacing="-3" fill="{TEXT}">{esc(d["name"])}</text>',
        f'<text x="45" y="192" font-family="monospace" font-size="17" font-weight="700" letter-spacing="4" fill="{SUB}">{esc(d["role"])}</text>',
        '<rect x="45" y="211" width="180" height="3" fill="#FF5A36"/>',
        '<rect x="42" y="255" width="205" height="49" rx="6" fill="#111111"/>',
        '<text x="60" y="275" font-family="monospace" font-size="10" letter-spacing="2" fill="#A7A39C">EDUCATION</text>',
        f'<text x="60" y="294" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="700" fill="{LIGHT}">{esc(d["education"])}</text>',
        '<rect x="262" y="255" width="285" height="49" rx="6" fill="#FFFFFF" stroke="#111111" stroke-width="1.5"/>',
        '<text x="280" y="275" font-family="monospace" font-size="10" letter-spacing="2" fill="#77716A">CURRENTLY</text>',
        f'<text x="280" y="294" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="700" fill="{TEXT}">{esc(d["currently"])}</text>',
        '<rect x="562" y="255" width="250" height="49" rx="6" fill="#FF5A36"/>',
        '<circle cx="583" cy="279" r="5" fill="#111111"/>',
        '<text x="598" y="284" font-family="monospace" font-size="11" font-weight="700" letter-spacing="1.5" fill="#111111">OPEN TO SWE INTERNSHIPS</text>',
        f'<text x="1125" y="315" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="90" font-weight="900" fill="{TEXT}" opacity="0.07">{esc(d["id"])}</text>',
        '<line x1="42" y1="335" x2="1158" y2="335" stroke="#111111" stroke-width="1"/>',
        f'<text x="42" y="360" font-family="monospace" font-size="12" font-weight="700" letter-spacing="2" fill="{TEXT}">{esc(d["motto"])}</text>',
        f'<text x="1158" y="360" text-anchor="end" font-family="monospace" font-size="11" letter-spacing="1" fill="{MUTED}">{esc(d["location"])}</text>',
        '</svg>',
    ]
    return "\n".join(a) + "\n"


HERO = {
    "label": "YASH #07",
    "status": "STATUS: BUILDING",
    "name": "Yash Waghmare",
    "role": "FULL-STACK / WEB DEVELOPER",
    "education": "IIT GUWAHATI",
    "currently": "WEBOPS HEAD @ SPIRIT",
    "id": "#07",
    "motto": "BUILD → BREAK → ITERATE → SHIP → REPEAT",
    "location": "GUWAHATI / NASHIK",
}


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build(HERO))
    print(f"wrote {OUT}  {os.path.getsize(OUT)} bytes")
