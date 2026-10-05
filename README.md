<!--
  Yash Waghmare · GitHub profile README

  assets/hero.svg   ← scripts/gen_hero.py (committed; CI fails on drift)
  output/snake-*    ← Platane/snk via .github/workflows/profile-assets.yml (daily)

  Every claim on this page was checked against a repository, a merged PR or a
  live deployment. Keep it that way: if it can't be linked or shown in code,
  it doesn't go here.
-->

<p align="center">
  <img width="100%" src="./assets/hero.svg" alt="Yash Waghmare terminal hero — software engineer and full-stack developer from IIT Guwahati." />
</p>

<h1 align="center">I BUILD THINGS THAT FEEL alive.</h1>

<p align="center">
  <b>Full-Stack Developer</b> · IIT Guwahati<br />
  I turn messy ideas into products people can use, trust, and remember.
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/waghmareyash07/"><b>LinkedIn</b></a> &nbsp;·&nbsp;
  <a href="https://yash-waghmare.netlify.app"><b>Portfolio</b></a> &nbsp;·&nbsp;
  <a href="https://github.com/yash07-bit?tab=repositories"><b>GitHub</b></a> &nbsp;·&nbsp;
  <a href="mailto:waghmareyash07@gmail.com"><b>Email</b></a>
</p>

<br />

### `~/now` &nbsp;<sub>what I'm focused on</sub>

- **Agents that do real work.** Tool-calling AI that acts across Gmail, Drive, Notion and Calendar, and stops for a human before anything that matters ([InternFlow AI](https://github.com/yash07-bit/InternFlow_AI)).
- **Spirit '26.** Building and running the festival's web platforms as WebOps Head.
- **Going deeper.** Backend architecture, system design and DSA.

<br />

### `~/work` &nbsp;<sub>selected projects</sub>

<table>
<tr>
<td width="50%" valign="top">

#### InternFlow AI &nbsp;<sub>AI agent</sub>
Turns a job posting into a complete application workflow across five apps, and waits for your approval before doing anything consequential.

- 13 risk-tagged tools; the orchestrator, not the prompt, enforces approval gates
- Streams every step over SSE; switches to a deterministic planner if the model fails mid-run
- Strips prompt injection from job pages, blocks SSRF, encrypts OAuth tokens with AES-256-GCM

<code>TypeScript</code> <code>React 19</code> <code>Express 5</code> <code>Claude API</code> <code>Vitest</code>

[**Code**](https://github.com/yash07-bit/InternFlow_AI) &nbsp;·&nbsp; [**Walkthrough**](https://github.com/yash07-bit/InternFlow_AI#walkthrough-video)

</td>
<td width="50%" valign="top">

#### Velora &nbsp;<sub>route optimization · team</sub>
Constraint-aware cab routing for corporate commutes. Built as a team for Kriti '26, IIT Guwahati's inter-hostel tech meet.

- LNS, ALNS and VROOM solve in parallel; a shared feasibility scorer picks the winner
- Long solves run on Celery + Redis so the API never blocks; the client polls for results
- Road distances come from a self-hosted OSRM server, and routes render on a Next.js map

<code>Next.js</code> <code>FastAPI</code> <code>Celery</code> <code>Redis</code> <code>PostgreSQL</code> <code>OSRM</code>

[**Code**](https://github.com/yash07-bit/optimization-main) &nbsp;·&nbsp; [**Live**](https://opti-front-nine.vercel.app)

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### Spirit CA Portal &nbsp;<sub>in production</sub>
The campus-ambassador platform for Spirit, IIT Guwahati's sports festival: tasks, referrals, a tiered leaderboard and an admin panel.

- Built the referral pipeline: an idempotent RabbitMQ worker, with a TTL retry queue, that awards points when referred participants register
- 80+ commits and 50+ merged PRs across the UI, admin dashboard and backend

<code>React</code> <code>Express</code> <code>MySQL</code> <code>RabbitMQ</code>

[**Live**](https://ca.spiritiitg.in) &nbsp;·&nbsp; <sub>source is private to the Spirit org</sub>

</td>
<td width="50%" valign="top">

#### Wanderlust &nbsp;<sub>full-stack</sub>
An Airbnb-style stays platform: list a place, upload photos, search, filter and review.

- Passport auth with sessions persisted in MongoDB; ownership checks on every edit and delete
- Joi validation at the route boundary; deleting a listing cascades to its reviews
- Case-insensitive search across title, location and country, plus category filters

<code>Node.js</code> <code>Express</code> <code>MongoDB</code> <code>EJS</code> <code>Cloudinary</code>

[**Code**](https://github.com/yash07-bit/wanderlust) &nbsp;·&nbsp; [**Live**](https://wanderlust-fuiy.onrender.com) <sub>(free tier, first load is slow)</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### VectorShift Pipeline Builder &nbsp;<sub>workflow editor</sub>
A drag-and-drop canvas for composing data and LLM pipelines.

- Nine node types built on one shared node component
- Text nodes parse `{{ variables }}` as you type and grow matching input handles
- A FastAPI endpoint checks that the graph is acyclic using Kahn's algorithm

<code>React Flow</code> <code>Zustand</code> <code>FastAPI</code> <code>Python</code>

[**Code**](https://github.com/yash07-bit/VectorShift)

</td>
<td width="50%" valign="top">

#### NexaVault &nbsp;<sub>dashboard</sub>
A personal-finance dashboard: import an Excel sheet and see it flow into budgets, insights and reports.

- One shared data context keeps all seven pages in sync
- An admin/viewer role switch gates write actions; amounts display in USD, EUR or GBP
- Recharts for balance trends, category splits and month-over-month comparisons

<code>React</code> <code>Vite</code> <code>Tailwind CSS</code> <code>Recharts</code> <code>SheetJS</code>

[**Code**](https://github.com/yash07-bit/Finance-Dashboard) &nbsp;·&nbsp; [**Live**](https://nexa-vault-three.vercel.app)

</td>
</tr>
</table>

<br />

### `~/principles` &nbsp;<sub>how I build, and where it shows</sub>

| Principle | Where it shows up |
|---|---|
| **Guardrails belong in code, not prompts** | InternFlow's orchestrator decides when to stop for approval, and the agent has no send-email tool, only drafts |
| **Validate at every boundary** | Joi on Wanderlust's routes · Pydantic on the pipeline API · Zod on the config endpoint I added to `get_attendance_hours` |
| **Slow work goes on a queue** | Spirit's referral points are awarded by a RabbitMQ consumer, not by the request that registered the participant |
| **Degrade, don't die** | InternFlow falls back to a local planner when the model fails, and warns and moves on when an app is unreachable |
| **It isn't done until it's deployed** | [ca.spiritiitg.in](https://ca.spiritiitg.in) · Wanderlust on Render · NexaVault on Vercel |

<br />

### `~/experience`

**WebOps Head** · Spirit, IIT Guwahati<br />
I lead web for IITG's annual inter-college sports festival. On the CA Portal I built the referral pipeline and much of the UI and admin tooling, and I also contribute to the main festival platform.

**Senior Web Developer** · Students' Web Committee (SWC), IIT Guwahati<br />
I build institute web platforms, including the Students' Senate portal home page and a feedback endpoint for the events scheduler.

**Data Analytics Virtual Experience** · Deloitte Australia<br />
Analysed transaction data in Excel and built Tableau dashboards for stakeholders.

<br />

### `~/open-source`

Contributions to [`RonStrauss/get_attendance_hours`](https://github.com/RonStrauss/get_attendance_hours), a TypeScript tool that scrapes attendance from HR systems and fills in timesheets automatically.

| PR | Change | Status |
|---|---|---|
| [#55](https://github.com/RonStrauss/get_attendance_hours/pull/55) | Moved UI options behind a backend `/config` endpoint, validated on the client with Zod | **Merged** |
| [#57](https://github.com/RonStrauss/get_attendance_hours/pull/57) | Structured, readable errors when a scrape fails | Open |
| [#58](https://github.com/RonStrauss/get_attendance_hours/pull/58) | Support for mixed-type days, such as half vacation and half work | Open |
| [#59](https://github.com/RonStrauss/get_attendance_hours/pull/59) | Split the scraper and the API into independent run modes | Open |

Also: a merged layout fix in [Ash469/NSS#4](https://github.com/Ash469/NSS/pull/4).

<br />

### `~/stack`

<table>
  <tr><td><b>Languages</b></td><td>TypeScript · JavaScript · Python · C++ · SQL</td></tr>
  <tr><td><b>Frontend</b></td><td>React · Next.js · Tailwind CSS · Vite · React Flow</td></tr>
  <tr><td><b>Backend</b></td><td>Node.js · Express · FastAPI · REST · Server-Sent Events</td></tr>
  <tr><td><b>Data</b></td><td>PostgreSQL · MySQL · MongoDB · Redis · RabbitMQ</td></tr>
  <tr><td><b>AI & infra</b></td><td>Claude API · Docker · GitHub Actions · Render · Vercel</td></tr>
</table>

<br />

### `~/activity`

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/yash07-bit/yash07-bit/output/snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/yash07-bit/yash07-bit/output/snake-light.svg" />
    <img alt="Contribution graph being eaten by a snake" src="https://raw.githubusercontent.com/yash07-bit/yash07-bit/output/snake-light.svg" />
  </picture>
</p>

---

<p align="center">
  <b>Open to software engineering internships.</b><br />
  If you're building something real, I'd like to hear about it.
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/waghmareyash07/">LinkedIn</a> &nbsp;·&nbsp;
  <a href="https://yash-waghmare.netlify.app">Portfolio</a> &nbsp;·&nbsp;
  <a href="mailto:waghmareyash07@gmail.com">waghmareyash07@gmail.com</a>
</p>

<p align="center"><sub><code>build → ship → learn → repeat</code></sub></p>
