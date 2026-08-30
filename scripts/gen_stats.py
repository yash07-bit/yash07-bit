#!/usr/bin/env python3
"""
Generate an aurora-themed GitHub stats card as a self-hosted SVG.

Replaces github-readme-stats (whose public instance is DEPLOYMENT_PAUSED).
Run by .github/workflows/snake.yml; output lands on the `output` branch.

Needs GITHUB_TOKEN in the environment for the GraphQL call. Without one it
renders from REST-only data and leaves GraphQL-derived tiles at zero, so a
token outage degrades the card instead of failing the build.
"""
import json, os, sys, urllib.request, urllib.error, datetime

USER = os.environ.get("STATS_USER", "yash07-bit")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("STATS_OUT", "dist/stats.svg")

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Ubuntu,'Helvetica Neue',Arial,sans-serif"
BG = "#080B12"

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


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;")


def render(d):
    W, H = 1200, 300
    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
      f'fill="none" role="img" aria-label="GitHub activity statistics for {USER}">')
    a('<defs>'
      '<filter id="bl" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="80"/></filter>'
      '<radialGradient id="g1"><stop offset="0" stop-color="#22D3EE"/><stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></radialGradient>'
      '<radialGradient id="g2"><stop offset="0" stop-color="#A855F7"/><stop offset="1" stop-color="#A855F7" stop-opacity="0"/></radialGradient>'
      '<linearGradient id="num" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset="0" stop-color="#E2E8F0"/><stop offset="1" stop-color="#94A3B8"/></linearGradient>'
      f'<clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>')
    a('<g clip-path="url(#c)">')
    a(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    a('<g filter="url(#bl)" opacity="0.45">'
      f'<ellipse cx="90" cy="0" rx="240" ry="130" fill="url(#g1)"/>'
      f'<ellipse cx="1120" cy="{H}" rx="240" ry="130" fill="url(#g2)"/></g>')

    a(f'<text x="40" y="46" font-family="{MONO}" font-size="13" fill="#64748B" letter-spacing="2">activity</text>')
    a(f'<text x="{W-40}" y="46" font-family="{MONO}" font-size="13" fill="#22D3EE" text-anchor="end">@{USER}</text>')
    a(f'<line x1="40" y1="62" x2="{W-40}" y2="62" stroke="#FFFFFF" stroke-opacity="0.08"/>')

    tiles = [("contributions", d["contributions"]), ("total commits", d["commits"]),
             ("pull requests", d["prs"]),           ("current streak", d["cur"]),
             ("longest streak", d["long"]),         ("repositories", d["repos"])]
    accents = ["#22D3EE", "#38BDF8", "#818CF8", "#A78BFA", "#C084FC", "#E879F9"]
    for i, (label, val) in enumerate(tiles):
        col, row = i % 3, i // 3
        x = 40 + col * 210
        y = 122 + row * 92
        a(f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="40" font-weight="700" '
          f'fill="url(#num)">{val}</text>')
        a(f'<rect x="{x}" y="{y+12}" width="26" height="2.5" rx="1.25" fill="{accents[i]}"/>')
        a(f'<text x="{x}" y="{y+34}" font-family="{MONO}" font-size="11.5" fill="#64748B" '
          f'letter-spacing="1.2">{label}</text>')

    LX, LW = 720, 440
    a(f'<line x1="{LX-40}" y1="86" x2="{LX-40}" y2="{H-40}" stroke="#FFFFFF" stroke-opacity="0.08"/>')
    a(f'<text x="{LX}" y="104" font-family="{MONO}" font-size="11.5" fill="#64748B" '
      f'letter-spacing="1.2">top languages</text>')

    langs = d["langs"] or [("No data", 100.0, "#30363D")]
    a(f'<clipPath id="bar"><rect x="{LX}" y="120" width="{LW}" height="14" rx="7"/></clipPath>')
    a('<g clip-path="url(#bar)">')
    x = LX
    for _, pct, color in langs:
        w = max(LW * pct / 100.0, 2)
        a(f'<rect x="{x:.1f}" y="120" width="{w:.1f}" height="14" fill="{color}"/>')
        x += w
    a(f'<rect x="{x:.1f}" y="120" width="{LW}" height="14" fill="#30363D"/>')
    a('</g>')

    for i, (name, pct, color) in enumerate(langs):
        col, row = i % 2, i // 2
        lx = LX + col * 224
        ly = 176 + row * 30
        a(f'<circle cx="{lx+5}" cy="{ly-4}" r="5" fill="{color}"/>')
        a(f'<text x="{lx+20}" y="{ly}" font-family="{SANS}" font-size="13.5" fill="#CBD5E1">{esc(name)}</text>')
        a(f'<text x="{lx+200}" y="{ly}" font-family="{MONO}" font-size="12.5" fill="#64748B" '
          f'text-anchor="end">{pct:.1f}%</text>')

    a('</g>')
    a(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="#FFFFFF" stroke-opacity="0.09"/>')
    a('</svg>')
    return "".join(p)


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
