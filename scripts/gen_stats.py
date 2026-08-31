#!/usr/bin/env python3
"""
Generate an aurora-themed GitHub stats card as a self-hosted SVG.

Replaces github-readme-stats (whose public instance is DEPLOYMENT_PAUSED).
Run by .github/workflows/profile-assets.yml; output lands on the `output`
branch, which the README's Activity section points at.

Needs GITHUB_TOKEN in the environment for the GraphQL call. Without one it
renders from REST-only data and leaves GraphQL-derived tiles at zero, so a
token outage degrades the card instead of failing the build.
"""
import json, os, sys, urllib.request, urllib.error, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import (BG, CYAN, SKY, INDIGO, VIOLET, FUCHSIA, TEXT, MUTED, DIM,
                   MONO, SANS, esc, cut_rect, corner_bracket, defs_aurora,
                   defs_grid, layer_grid)

USER = os.environ.get("STATS_USER", "yash07-bit")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("STATS_OUT", "dist/stats.svg")

QUERY = """
query($login:String!) {
  user(login:$login) {
    followers { totalCount }
    pullRequests { totalCount }
    repositories(first:100, ownerAffiliations:OWNER, isFork:false) {
      totalCount
      nodes {
        stargazerCount
        languages(first:8, orderBy:{field:SIZE, direction:DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def graphql():
    if not TOKEN:
        print("WARN: no GITHUB_TOKEN, skipping GraphQL", file=sys.stderr)
        return None
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": "bearer " + TOKEN,
                 "Content-Type": "application/json",
                 "User-Agent": "stats-card"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=30))
    except urllib.error.HTTPError as e:
        print("WARN: GraphQL HTTP", e.code, e.read()[:200], file=sys.stderr)
        return None
    if "errors" in r:
        print("WARN: GraphQL errors:", r["errors"][:1], file=sys.stderr)
        return None
    return r["data"]["user"]


def streaks(weeks):
    days = [d for w in weeks for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    today = datetime.date.today().isoformat()
    days = [d for d in days if d["date"] <= today]
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    cur = 0
    for d in reversed(days):
        if d["contributionCount"] > 0:
            cur += 1
        elif d["date"] != today:      # today not yet committed doesn't break it
            break
    return cur, longest


LANG_FALLBACK_COLOR = "#818CF8"
LANG_COLORS = {
    "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Python": "#3572A5",
    "EJS": "#a91e50", "HTML": "#e34c26", "CSS": "#563d7c", "SCSS": "#c6538c",
    "Java": "#b07219", "C": "#555555", "C++": "#f34b7d", "Shell": "#89e051",
    "Jupyter Notebook": "#DA5B0B", "Vue": "#41b883", "Go": "#00ADD8",
    "Ruby": "#701516", "PHP": "#4F5D95", "Dart": "#00B4AB", "Rust": "#dea584",
}


def rest(path):
    h = {"User-Agent": "stats-card", "Accept": "application/vnd.github+json"}
    if TOKEN:
        h["Authorization"] = "bearer " + TOKEN
    req = urllib.request.Request("https://api.github.com" + path, headers=h)
    return json.load(urllib.request.urlopen(req, timeout=30))


def rest_fallback(d):
    """Fill what REST can when GraphQL is unavailable.

    Contributions, commit totals and streaks only exist in GraphQL, so those
    stay at whatever GraphQL managed to set. Everything else is recoverable.
    """
    try:
        prof = rest("/users/%s" % USER)
        d["followers"] = prof["followers"]
    except Exception as e:
        print("WARN: REST profile failed:", e, file=sys.stderr)
    try:
        repos = [r for r in rest("/users/%s/repos?per_page=100" % USER) if not r["fork"]]
        d["repos"] = len(repos)
        d["stars"] = sum(r["stargazers_count"] for r in repos)
        totals = {}
        for r in repos:
            try:
                for k, v in rest("/repos/%s/languages" % r["full_name"]).items():
                    totals[k] = totals.get(k, 0) + v
            except Exception:
                continue
        tot = sum(totals.values()) or 1
        top = sorted(totals.items(), key=lambda kv: -kv[1])[:6]
        d["langs"] = [(n, v * 100.0 / tot, LANG_COLORS.get(n, LANG_FALLBACK_COLOR))
                      for n, v in top]
    except Exception as e:
        print("WARN: REST repos failed:", e, file=sys.stderr)
    try:
        q = "/search/issues?q=author:%s+type:pr&per_page=1" % USER
        d["prs"] = rest(q)["total_count"]
    except Exception as e:
        print("WARN: REST pr search failed:", e, file=sys.stderr)
    return d


def collect():
    d = {"contributions": 0, "commits": 0, "prs": 0, "stars": 0,
         "repos": 0, "followers": 0, "cur": 0, "long": 0, "langs": []}
    try:
        u = graphql()
    except Exception as e:
        print("WARN: GraphQL call raised:", e, file=sys.stderr)
        u = None

    if u:
        try:
            cc = u["contributionsCollection"]
            cal = cc["contributionCalendar"]
            d["contributions"] = cal["totalContributions"]
            d["commits"] = cc["totalCommitContributions"] + cc["restrictedContributionsCount"]
            d["prs"] = u["pullRequests"]["totalCount"]
            d["repos"] = u["repositories"]["totalCount"]
            d["followers"] = u["followers"]["totalCount"]
            d["cur"], d["long"] = streaks(cal["weeks"])
            totals, colors = {}, {}
            for repo in (u["repositories"]["nodes"] or []):
                d["stars"] += repo.get("stargazerCount") or 0
                # languages is null for repos linguist cannot classify
                edges = (repo.get("languages") or {}).get("edges") or []
                for e in edges:
                    node = e.get("node") or {}
                    n = node.get("name")
                    if not n:
                        continue
                    totals[n] = totals.get(n, 0) + (e.get("size") or 0)
                    colors[n] = node.get("color") or LANG_COLORS.get(n, LANG_FALLBACK_COLOR)
            tot = sum(totals.values()) or 1
            top = sorted(totals.items(), key=lambda kv: -kv[1])[:6]
            d["langs"] = [(n, v * 100.0 / tot, colors[n]) for n, v in top]
        except Exception as e:
            print("WARN: GraphQL parse failed, falling back to REST:", e, file=sys.stderr)
            u = None

    if not u:
        rest_fallback(d)
    return d


def render(d):
    """Draw the card in the same visual language as hero.svg and stack.svg:
    dark ground, blueprint grid, HUD brackets, cut-corner panels."""
    W, H, uid = 1200, 320, "t"
    a = []
    a.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
             f'height="{H}" fill="none" role="img" '
             f'aria-label="GitHub activity statistics for {USER}">')

    a.append("<defs>")
    a.append(defs_aurora(uid))
    a.append(defs_grid(uid, W, H, cell=40, fade_to=0.92))
    a.append(f'<clipPath id="cl{uid}"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    a.append(f'<linearGradient id="num{uid}" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="#F1F5F9"/><stop offset="1" stop-color="{MUTED}"/>'
             f'</linearGradient>')
    a.append("</defs>")

    a.append(f'<g clip-path="url(#cl{uid})">')
    a.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    a.append(f'<g filter="url(#bl{uid})" opacity="0.5">'
             f'<ellipse cx="90" cy="0" rx="250" ry="130" fill="url(#au3{uid})"/>'
             f'<ellipse cx="1120" cy="{H}" rx="250" ry="130" fill="url(#au2{uid})"/></g>')
    a.append(layer_grid(uid, W, H, opacity=0.05))
    for cx, cy, sx, sy in ((14, 14, 1, 1), (W - 14, 14, -1, 1),
                           (14, H - 14, 1, -1), (W - 14, H - 14, -1, -1)):
        a.append(corner_bracket(cx, cy, 18, sx, sy, CYAN, 0.45))

    a.append(f'<text x="44" y="52" font-family="{MONO}" font-size="12.5" fill="{DIM}" '
             f'letter-spacing="2.4">\u25c8 ACTIVITY</text>')
    a.append(f'<text x="{W-44}" y="52" font-family="{MONO}" font-size="12.5" fill="{CYAN}" '
             f'text-anchor="end" letter-spacing="1.4">@{USER}</text>')
    a.append(f'<line x1="44" y1="68" x2="{W-44}" y2="68" stroke="#FFFFFF" stroke-opacity="0.08"/>')

    # ── six stat panels ──
    tiles = [("contributions", d["contributions"]), ("total commits", d["commits"]),
             ("pull requests", d["prs"]),           ("current streak", d["cur"]),
             ("longest streak", d["long"]),         ("repositories", d["repos"])]
    accents = [CYAN, SKY, INDIGO, "#A78BFA", VIOLET, FUCHSIA]
    TW, TH, GAP, X0, Y0 = 200, 88, 12, 44, 92
    for i, (label, val) in enumerate(tiles):
        col, row = i % 3, i // 3
        x = X0 + col * (TW + GAP)
        y = Y0 + row * (TH + GAP)
        c = accents[i]
        a.append(f'<path d="{cut_rect(x, y, TW, TH, 8)}" fill="#FFFFFF" fill-opacity="0.022" '
                 f'stroke="{c}" stroke-opacity="0.20" stroke-width="1">'
                 f'<animate attributeName="stroke-opacity" values="0.20;0.50;0.20" dur="5s" '
                 f'begin="{i * 0.6:.1f}s" repeatCount="indefinite"/></path>')
        a.append(f'<text x="{x+18}" y="{y+46}" font-family="{SANS}" font-size="36" '
                 f'font-weight="700" fill="url(#num{uid})">{val}</text>')
        a.append(f'<rect x="{x+18}" y="{y+56}" width="24" height="2.5" rx="1.25" fill="{c}"/>')
        a.append(f'<text x="{x+18}" y="{y+74}" font-family="{MONO}" font-size="11" fill="{DIM}" '
                 f'letter-spacing="1.2">{label}</text>')

    # ── top languages ──
    LX = X0 + 3 * (TW + GAP) + 28
    LW = W - 44 - LX
    a.append(f'<line x1="{LX-24}" y1="88" x2="{LX-24}" y2="{H-40}" stroke="#FFFFFF" '
             f'stroke-opacity="0.08"/>')
    a.append(f'<text x="{LX}" y="106" font-family="{MONO}" font-size="11" fill="{DIM}" '
             f'letter-spacing="1.2">top languages</text>')

    langs = d["langs"] or [("No data", 100.0, "#30363D")]
    a.append(f'<clipPath id="bar{uid}"><rect x="{LX}" y="122" width="{LW}" height="14" rx="7"/></clipPath>')
    a.append(f'<g clip-path="url(#bar{uid})">')
    x = LX
    for _, pct, color in langs:
        w = max(LW * pct / 100.0, 2)
        a.append(f'<rect x="{x:.1f}" y="122" width="{w:.1f}" height="14" fill="{color}"/>')
        x += w
    a.append(f'<rect x="{x:.1f}" y="122" width="{LW}" height="14" fill="#30363D"/>')
    a.append("</g>")

    for i, (name, pct, color) in enumerate(langs):
        col, row = i % 2, i // 2
        lx = LX + col * (LW / 2 + 4)
        ly = 178 + row * 30
        a.append(f'<circle cx="{lx+5}" cy="{ly-4}" r="5" fill="{color}"/>')
        a.append(f'<text x="{lx+20}" y="{ly}" font-family="{SANS}" font-size="13.5" '
                 f'fill="#CBD5E1">{esc(name)}</text>')
        a.append(f'<text x="{lx + LW/2 - 20:.0f}" y="{ly}" font-family="{MONO}" font-size="12.5" '
                 f'fill="{DIM}" text-anchor="end">{pct:.1f}%</text>')

    a.append("</g>")
    a.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" '
             f'stroke="#FFFFFF" stroke-opacity="0.10"/>')
    a.append("</svg>")
    return "".join(a)


if __name__ == "__main__":
    import traceback
    try:
        data = collect()
    except Exception:
        traceback.print_exc()
        print("ERROR: collect() failed; emitting an empty card so the publish "
              "step still runs and the snake stays live.", file=sys.stderr)
        data = {"contributions": 0, "commits": 0, "prs": 0, "stars": 0,
                "repos": 0, "followers": 0, "cur": 0, "long": 0, "langs": []}
    print("data:", {k: v for k, v in data.items() if k != "langs"})
    print("langs:", [(n, round(p, 1)) for n, p, _ in data["langs"]])
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(render(data))
    print("wrote", OUT, os.path.getsize(OUT), "bytes")
