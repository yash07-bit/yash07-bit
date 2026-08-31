"""Shared palette, type metrics and SVG primitives for the profile cards.

Every card in ./assets is generated — hero.svg and stack.svg by gen_cards.py,
stats.svg by gen_stats.py in CI. They share this module so the four of them
stay one visual system: same ground, same grid, same corner-cut geometry.
"""

BG      = "#070A10"
CYAN    = "#22D3EE"
SKY     = "#38BDF8"
INDIGO  = "#818CF8"
VIOLET  = "#A855F7"
FUCHSIA = "#E879F9"
GREEN   = "#4ADE80"

TEXT  = "#E2E8F0"
MUTED = "#94A3B8"
DIM   = "#64748B"

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Ubuntu,'Helvetica Neue',Arial,sans-serif"


# ── type metrics ──────────────────────────────────────────────────────────
# Advance widths in em for a Helvetica-class face. Only accurate enough to
# size a chip around a label; nothing here is laid out to the pixel.
_NARROW = "iljI.,'|!:;()[]/\\-"
_WIDE   = "mMW"

def _adv(ch):
    if ch in _NARROW:  return 0.30
    if ch in _WIDE:    return 0.86
    if ch == " ":      return 0.28
    if ch in "ft":     return 0.36
    if ch.isdigit():   return 0.56
    if ch.isupper():   return 0.69
    if ch in "cvxyzks": return 0.50
    return 0.55

def text_w(s, size, mono=False, tracking=0.0):
    """Rendered width of `s`, including inter-letter tracking."""
    if mono:
        base = len(s) * size * 0.60
    else:
        base = sum(_adv(c) for c in s) * size
    return base + max(len(s) - 1, 0) * tracking


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ── geometry ──────────────────────────────────────────────────────────────
def cut_rect(x, y, w, h, c=7):
    """Octagonal 'cut corner' panel path — the house shape for chips and tiles."""
    return (f"M{x+c} {y}H{x+w-c}L{x+w} {y+c}V{y+h-c}L{x+w-c} {y+h}"
            f"H{x+c}L{x} {y+h-c}V{y+c}Z")


def corner_bracket(x, y, arm, sx, sy, color, opacity=0.5, w=1.4):
    """An L-shaped HUD bracket. sx/sy are +1/-1 for which way the arms point."""
    return (f'<path d="M{x} {y + sy*arm}V{y}H{x + sx*arm}" fill="none" '
            f'stroke="{color}" stroke-opacity="{opacity}" stroke-width="{w}" '
            f'stroke-linecap="square"/>')


# ── reusable layers ───────────────────────────────────────────────────────
def defs_aurora(uid):
    """Four soft colour fields plus the blur that turns them into aurora."""
    return (
        f'<filter id="bl{uid}" x="-70%" y="-70%" width="240%" height="240%">'
        f'<feGaussianBlur stdDeviation="80"/></filter>'
        f'<radialGradient id="au1{uid}"><stop offset="0" stop-color="{SKY}"/>'
        f'<stop offset="1" stop-color="{SKY}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="au2{uid}"><stop offset="0" stop-color="{VIOLET}"/>'
        f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="au3{uid}"><stop offset="0" stop-color="{CYAN}"/>'
        f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="au4{uid}"><stop offset="0" stop-color="{FUCHSIA}"/>'
        f'<stop offset="1" stop-color="{FUCHSIA}" stop-opacity="0"/></radialGradient>')


def defs_grid(uid, w, h, cell=40, fade_to=1.0):
    """A blueprint grid, masked so it dissolves toward the bottom of the card.

    fade_to is the fraction of the height at which the grid has fully faded;
    cards with a horizon pass the horizon's position so the two meet cleanly.
    """
    return (
        f'<pattern id="gr{uid}" width="{cell}" height="{cell}" patternUnits="userSpaceOnUse">'
        f'<path d="M{cell} 0H0V{cell}" fill="none" stroke="#FFFFFF" stroke-width="1"/></pattern>'
        f'<linearGradient id="gm{uid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.55"/>'
        f'<stop offset="{fade_to:.3f}" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
        f'<mask id="gk{uid}"><rect width="{w}" height="{h}" fill="url(#gm{uid})"/></mask>')


def layer_grid(uid, w, h, opacity=0.05):
    return (f'<g mask="url(#gk{uid})" opacity="{opacity}">'
            f'<rect width="{w}" height="{h}" fill="url(#gr{uid})"/></g>')


def layer_stars(uid, w, h, n=44, seed=7, y0=0, y1=None):
    """Deterministic starfield — a fixed seed keeps regenerated cards diffable."""
    import random
    rng = random.Random(seed)
    y1 = h if y1 is None else y1
    out = ['<g fill="#FFFFFF">']
    for i in range(n):
        x  = rng.randint(20, w - 20)
        y  = rng.randint(y0, y1)
        r  = round(rng.uniform(0.5, 1.3), 2)
        o  = round(rng.uniform(0.12, 0.45), 2)
        d  = rng.randint(3, 8)
        b  = round(i * 0.17, 2)
        hi = round(min(o * 2.6, 0.85), 3)
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" opacity="{o}">'
                   f'<animate attributeName="opacity" values="{o};{hi};{o}" '
                   f'dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>')
    out.append('</g>')
    return "".join(out)
