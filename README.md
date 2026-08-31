<!--
  ─────────────────────────────────────────────────────────────────────
  Yash Waghmare · GitHub Profile README
  Palette: #22D3EE cyan → #818CF8 indigo → #E879F9 fuchsia

  The four cards on this page — hero, stack, activity, snake — are all
  generated and self-hosted:

    assets/hero.svg   ┐ scripts/gen_cards.py   (committed; CI checks drift)
    assets/stack.svg  ┘
    output/stats.svg    scripts/gen_stats.py   (rebuilt daily in CI)
    output/snake-*.svg  Platane/snk            (rebuilt daily in CI)

  Nothing above the fold depends on a third-party image service that can
  rate-limit or 404 — which is exactly how the old activity section broke.
  All four share scripts/theme.py, so the palette and geometry stay in sync.

  To change the hero copy or the stack list: edit the DATA block at the
  bottom of scripts/gen_cards.py, run `python3 scripts/gen_cards.py`, and
  commit the regenerated SVGs. CI fails if they drift.

  The cards are single dark panels rather than dark/light pairs on purpose:
  the aurora needs a dark ground to read, and one file per graphic means no
  prefers-color-scheme path that can break on its own.
  ─────────────────────────────────────────────────────────────────────
-->

<p align="center">
  <img width="100%" src="./assets/hero.svg" alt="Yash Waghmare — Frontend Developer · Full-Stack Builder · IIT Guwahati · Open to SWE Internships" />
</p>

<p align="center">
  <a href="https://yash-waghmare.netlify.app"><img src="https://img.shields.io/badge/PORTFOLIO-22D3EE?style=for-the-badge&logo=firefoxbrowser&logoColor=070A10&labelColor=070A10" alt="Portfolio" /></a>
  <a href="https://linkedin.com/in/waghmareyash07"><img src="https://img.shields.io/badge/LINKEDIN-818CF8?style=for-the-badge&logo=linkedin&logoColor=070A10&labelColor=070A10" alt="LinkedIn" /></a>
  <a href="mailto:w.prakash@iitg.ac.in"><img src="https://img.shields.io/badge/EMAIL-E879F9?style=for-the-badge&logo=gmail&logoColor=070A10&labelColor=070A10" alt="Email" /></a>
  <img src="https://komarev.com/ghpvc/?username=yash07-bit&label=VISITORS&color=22D3EE&style=for-the-badge" alt="Profile views" />
</p>

<br />

## &nbsp;◈&nbsp; whoami

```ts
const yash: Developer = {
  education : "B.Tech, Mechanical Engineering @ IIT Guwahati",
  role      : "WebOps Head @ Spirit — IITG's sports festival",
  building  : ["Wanderlust  · MERN travel platform",
               "NexaVault   · React 19 finance dashboard",
               "VectorShift · React + FastAPI pipeline builder"],
  learning  : ["DSA", "System Design", "Motion & UI/UX"],
  askMeAbout: ["React", "Node / Express", "MongoDB", "UI/UX"],
  goal      : "Ship products people actually enjoy using ✨",
};
```

<br />

## &nbsp;◈&nbsp; Stack Manifest

<p align="center">
  <img width="100%" src="./assets/stack.svg" alt="Tech stack — Languages: JavaScript, Python, C++, C, SQL, HTML5, CSS3 · Frontend: React, Tailwind CSS, Vite, Framer Motion, EJS, Bootstrap · Backend: Node.js, Express, FastAPI, MongoDB, MySQL, REST APIs · Tooling: Git, GitHub, VS Code, Postman, Vercel, Netlify, Figma" />
</p>

<br />

## &nbsp;◈&nbsp; Featured Work

<table>
<tr>
<td width="50%" valign="top">

### ▸ &nbsp;Wanderlust

Full-stack **MERN** travel platform — publish, browse and review stays.

- Session-based auth with route-level guards
- RESTful Express APIs + server-side validation
- Mongo schemas for listings, reviews, users
- Fully responsive UI

<code>Node</code> <code>Express</code> <code>MongoDB</code> <code>EJS</code>

**[↗ Live](https://wanderlust-fuiy.onrender.com)** &nbsp;·&nbsp; **[↗ Code](https://github.com/yash07-bit/wanderlust)**

</td>
<td width="50%" valign="top">

### ▸ &nbsp;NexaVault

Personal finance dashboard on **React 19**, with real data flowing through it.

- Excel (XLSX) import for transactions
- Bidirectional sync across every page
- Budgets, insights, reports, monthly trends
- Multi-currency (USD / EUR / GBP)

<code>React 19</code> <code>Tailwind</code> <code>Vite</code>

**[↗ Live](https://nexa-vault-three.vercel.app)** &nbsp;·&nbsp; **[↗ Code](https://github.com/yash07-bit/Finance-Dashboard)**

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ▸ &nbsp;VectorShift

Visual **drag-and-drop** builder for data-processing pipelines.

- Node canvas — LLM, API, Math, Filter, Delay types
- Auto variable detection from `{{ template }}` syntax
- Dynamic handles with automatic edge cleanup
- DAG validation on submit

<code>React</code> <code>FastAPI</code> <code>Python</code>

**[↗ Code](https://github.com/yash07-bit/VectorShift)**

</td>
<td width="50%" valign="top">

### ▸ &nbsp;Smart Waste Classifier

Type a waste item, get its category and disposal guidance instantly.

- Rule-based classifier — wet / dry / e-waste
- Framer Motion transitions throughout
- Example chips + educational category section
- Animated, responsive landing

<code>React</code> <code>Vite</code> <code>Tailwind</code>

**[↗ Code](https://github.com/yash07-bit/waste_type_detector)**

</td>
</tr>
</table>

<br />

## &nbsp;◈&nbsp; Experience

<details open>
<summary><b>&nbsp;▸ &nbsp;WebOps Head — Spirit, IIT Guwahati</b> &nbsp;·&nbsp; <i>present</i></summary>
<br />

- Leading web operations for one of IIT Guwahati's flagship festivals
- Designing and shipping the festival's digital experience end to end
- Shipping features to <code>spiritiitg/CA_PORTAL</code> through reviewed pull requests
  <!-- de-linked: github.com/spiritiitg 404s for anonymous visitors (the whole org,
       not just the repo), so the link was dead for everyone reading the profile.
       Restore the <a href="..."> wrapper if the org becomes public. -->
- Coordinating across design, content and dev to keep releases predictable

</details>

<details>
<summary><b>&nbsp;▸ &nbsp;Data Analytics Virtual Internship — Deloitte Australia</b></summary>
<br />

- Analysed transaction datasets in **Excel** to surface anomalies
- Built interactive **Tableau** dashboards for business stakeholders
- Translated raw data into decision-ready insights

</details>

<br />

## &nbsp;◈&nbsp; Activity

<!--
  Generated by scripts/gen_stats.py and published to the `output` branch by
  .github/workflows/profile-assets.yml — NOT by github-readme-stats, whose
  public instance is DEPLOYMENT_PAUSED (503). Self-hosting means this section
  cannot go dark because someone else ran out of quota.

  No width="100%" here, or on the snake below: both SVGs are already about
  GitHub's content width, so a failed load shows a small box rather than a
  giant empty one.
-->
<p align="center">
  <img src="https://raw.githubusercontent.com/yash07-bit/yash07-bit/output/stats.svg" alt="GitHub activity — contributions, commits, pull requests, streaks, repositories and top languages" />
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/yash07-bit/yash07-bit/output/snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/yash07-bit/yash07-bit/output/snake-light.svg" />
    <img alt="Snake eating my contribution graph" src="https://raw.githubusercontent.com/yash07-bit/yash07-bit/output/snake-light.svg" />
  </picture>
</p>

<br />

## &nbsp;◈&nbsp; Let's Build Something

<p align="center">
  <i>Open to Software Engineering internships and interesting frontend problems.</i>
</p>

<p align="center">
  <a href="mailto:w.prakash@iitg.ac.in"><img src="https://img.shields.io/badge/SAY_HELLO-E879F9?style=for-the-badge&logo=gmail&logoColor=070A10&labelColor=070A10" alt="Email" /></a>
  <a href="https://linkedin.com/in/waghmareyash07"><img src="https://img.shields.io/badge/CONNECT-818CF8?style=for-the-badge&logo=linkedin&logoColor=070A10&labelColor=070A10" alt="LinkedIn" /></a>
  <a href="https://yash-waghmare.netlify.app"><img src="https://img.shields.io/badge/SEE_MY_WORK-22D3EE?style=for-the-badge&logo=firefoxbrowser&logoColor=070A10&labelColor=070A10" alt="Portfolio" /></a>
</p>

<p align="center"><sub>Always learning, building, improving.</sub></p>
