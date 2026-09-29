#!/usr/bin/env python3
"""
Builds the Disclosure Commons static site from data/cases.json.

Run from the repo root:
    python3 scripts/build_site.py

Regenerates everything under docs/ except assets/style.css and browse/index.html,
which are hand-maintained. Safe to re-run any time data/cases.json changes.
"""
import json
import re
import shutil
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "cases.json"
DOCS = ROOT / "docs"

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,400;0,500;0,600;1,400'
    '&family=IBM+Plex+Mono:wght@400;500;600&family=Source+Sans+3:wght@400;500;600&display=swap" '
    'rel="stylesheet">'
)

CAT_COLORS = {
    'Vulnerability Disclosure': 'var(--c-vuln)',
    'Informed Consent & Human Subjects': 'var(--c-consent)',
    'Dual-Use Research': 'var(--c-dual)',
    'Legal Boundaries & CFAA Overreach': 'var(--c-legal)',
    'Institutional Suppression': 'var(--c-suppress)',
    'Financial Conflict of Interest': 'var(--c-financial)',
    'Critical Infrastructure & Public Trust': 'var(--c-infra)',
    'Surveillance & Offensive Tools': 'var(--c-surveil)',
}

NAV_ITEMS = [
    ("Home", "/"),
    ("Browse", "/browse/"),
    ("Taxonomy", "/taxonomy/"),
    ("About", "/about/"),
    ("Contribute", "/contribute/"),
    ("Further reading", "/articles/"),
    ("Cite this", "/cite/"),
]


def esc(s):
    """Minimal HTML escaping for text content."""
    if s is None:
        return ""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def nav_html(active_path, depth):
    """depth = number of '../' needed to reach docs/ root from this page."""
    prefix = "../" * depth if depth else "./"
    links = []
    for label, href in NAV_ITEMS:
        target = prefix if href == "/" else prefix + href.strip("/") + "/"
        cls = " active" if href == active_path else ""
        links.append(f'<a class="{cls.strip()}" href="{target}">{label}</a>')
    brand_href = prefix
    return (
        '<nav class="sitenav"><div class="sitenav-inner">'
        f'<a class="sitenav-brand" href="{brand_href}">Disclosure Commons</a>'
        f'<div class="sitenav-links">{"".join(links)}</div>'
        '</div></nav>'
    )


def footer_html(depth):
    prefix = "../" * depth if depth else "./"
    return (
        '<footer class="sitefooter"><div class="sitefooter-inner">'
        '<span>Disclosure Commons &middot; cybersecurity ethics case library</span>'
        f'<span><a href="{prefix}cite/">Cite this dataset</a> &middot; '
        '<a href="https://github.com/disclosure-commons/cybersecurity-ethics-commons" '
        'target="_blank" rel="noopener">GitHub</a> &middot; '
        f'<a href="{prefix}contribute/">Report a correction</a></span>'
        '</div></footer>'
    )


def page_shell(title, description, body_html, active_path="", depth=0, extra_head="", wide=False):
    page_class = "page wide" if wide else "page"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} &middot; Disclosure Commons</title>
<meta name="description" content="{esc(description)}">
{FONT_LINK}
<link rel="stylesheet" href="{'../' * depth if depth else './'}assets/style.css">
{extra_head}
</head>
<body>
{nav_html(active_path, depth)}
<main class="{page_class}">
{body_html}
</main>
{footer_html(depth)}
</body>
</html>
"""


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_home(cases, categories, years_min, years_max):
    counts = Counter(c["category"] for c in cases)
    cards = "".join(f"""
      <div class="home-card" style="border-color:{CAT_COLORS.get(cat['name'],'#999')}">
        <h2>{esc(cat['name'])}</h2>
        <p>{esc(cat['description'])}</p>
        <span class="cat-count">{counts.get(cat['name'],0)} cases</span>
      </div>""" for cat in categories)

    body = f"""
<div class="hero">
  <div class="hero-inner">
    <h1>A working library of cybersecurity research ethics cases.</h1>
    <p class="dek">Disclosure fights, CFAA prosecutions, dual-use dilemmas, and institutional retaliation &mdash; documented, tagged, and sourced for teaching, citation, and reuse.</p>
    <div class="hero-actions">
      <a class="btn primary" href="./browse/">Browse the cases</a>
      <a class="btn secondary" href="./taxonomy/">See the taxonomy</a>
    </div>
    <div class="docket">{len(cases)} cases &middot; {len(categories)} categories &middot; {years_min}&ndash;{years_max}</div>
  </div>
</div>
<div class="home-grid">{cards}</div>
"""
    return body


def build_case_page(case, all_cases, idx):
    cid = case["id"]
    color = CAT_COLORS.get(case["category"], "#999")
    chilling_stamp = '<div class="stamp">Chilling effect</div>' if case.get("chilling") == "Yes" else ""
    source = case.get("source") or ""
    source_html = (
        f'<h3>Source</h3><p><a href="{esc(source)}" target="_blank" rel="noopener">{esc(source)}</a></p>'
        if source else ""
    )

    prev_case = all_cases[idx - 1] if idx > 0 else None
    next_case = all_cases[idx + 1] if idx < len(all_cases) - 1 else None
    prev_link = f'<a href="../{prev_case["id"]:03d}/">&larr; No.{prev_case["id"]:03d}</a>' if prev_case else "<span></span>"
    next_link = f'<a href="../{next_case["id"]:03d}/">No.{next_case["id"]:03d} &rarr;</a>' if next_case else "<span></span>"

    body = f"""
<div class="case-num">Case No.{cid:03d}</div>
<h1>{esc(case['institution'])}</h1>
<div class="case-cat" style="color:{color}">{esc(case['category'])} &middot; {esc(case['year'])}</div>
{chilling_stamp}
<p>{esc(case['summary'])}</p>
<div class="meta-grid">
  <div class="meta-field"><label>Actor type</label><div>{esc(case['actor_type']) or '&mdash;'}</div></div>
  <div class="meta-field"><label>Actor intent</label><div>{esc(case['intent']) or '&mdash;'}</div></div>
  <div class="meta-field"><label>Disclosure method</label><div>{esc(case['disclosure']) or '&mdash;'}</div></div>
  <div class="meta-field"><label>Legal outcome</label><div>{esc(case['outcome']) or '&mdash;'}</div></div>
</div>
<h3>Key ethical dilemmas</h3>
<p>{esc(case['dilemmas']) or '&mdash;'}</p>
{source_html}
<div class="case-nav">{prev_link}{next_link}</div>
"""
    title = f"{case['institution']} (Case No.{cid:03d})"
    desc = case["summary"][:155]
    return page_shell(title, desc, body, active_path="/browse/", depth=2)


def build_taxonomy(cases, categories, tags_by_dim):
    counts = Counter(c["category"] for c in cases)
    entries = ""
    for cat in categories:
        color = CAT_COLORS.get(cat["name"], "#999")
        entries += f"""
<div class="cat-entry" style="--cat-color:{color}">
  <h3>{esc(cat['name'])}</h3>
  <p>{esc(cat['description'])}</p>
  <span class="cat-count">{counts.get(cat['name'],0)} cases</span>
</div>"""

    tag_rows = ""
    for dim, values in tags_by_dim.items():
        for val, desc in values:
            tag_rows += f"<tr><td>{esc(dim)}</td><td>{esc(val)}</td><td>{esc(desc)}</td></tr>"

    body = f"""
<h1>Taxonomy</h1>
<p class="dek">The categories and tags used to classify every case in the commons &mdash; the codebook behind the dataset.</p>

<h2>Primary categories</h2>
<p>Every case is assigned exactly one primary category, chosen for its central ethical tension even when other themes are present.</p>
{entries}

<h2>Tag dimensions</h2>
<p>Beyond the primary category, each case is tagged along several independent dimensions:</p>
<table class="tag-table">
<tr><th>Dimension</th><th>Value</th><th>Description</th></tr>
{tag_rows}
</table>
"""
    return page_shell(
        "Taxonomy",
        "The category and tag taxonomy used to classify cybersecurity ethics cases.",
        body, active_path="/taxonomy/", depth=1,
    )


def build_about():
    body = """
<h1>About this project</h1>
<p class="dek">What this is, how cases are selected, and who's behind it.</p>

<h2>What this is</h2>
<p>Disclosure Commons is a public, structured library of real cybersecurity research ethics cases &mdash;
vulnerability disclosure disputes, CFAA prosecutions, dual-use research dilemmas, and institutional
retaliation against researchers. It's built for classroom use, citation in research, and general reference.</p>

<h2>Inclusion criteria</h2>
<ul>
  <li>Every case must have at least one linked, publicly available source (news reporting, a court record,
  or the subject's own public statement).</li>
  <li>No unpublished, leaked, or non-public information is included, regardless of how it was obtained.</li>
  <li>Cases are tagged with a single primary category, chosen for the case's central ethical tension.</li>
</ul>

<h2>On naming individuals</h2>
<p>Every case here is drawn from previously published reporting or public record. We take seriously that
aggregation itself &mdash; not just disclosure of new facts &mdash; can affect how findable and permanent
a case becomes for the people named in it. See <a href="../contribute/">Contribute</a> for how to request
a correction or reconsideration of an entry.</p>

<h2>Maintenance</h2>
<p>This is a living document. Cases are reviewed periodically for outdated outcomes (e.g. a conviction
later expunged or overturned). See the project's
<a href="https://github.com/disclosure-commons/cybersecurity-ethics-commons" target="_blank" rel="noopener">GitHub repository</a>
for full version history.</p>
"""
    return page_shell(
        "About",
        "How Disclosure Commons selects, sources, and maintains its case library.",
        body, active_path="/about/", depth=1,
    )


def build_contribute():
    body = """
<h1>Contribute</h1>
<p class="dek">Propose a new case, or request a correction to an existing one.</p>

<h2>Propose a new case</h2>
<p>Open a
<a href="https://github.com/disclosure-commons/cybersecurity-ethics-commons/issues/new?template=new-case.md" target="_blank" rel="noopener">New case issue</a>
on GitHub. Include the institution/actor, year, a factual summary, and at least one source link.</p>

<h2>Request a correction</h2>
<p>If you're a subject of one of these cases, or you've spotted a factual error or an outdated legal
outcome, open a
<a href="https://github.com/disclosure-commons/cybersecurity-ethics-commons/issues/new?template=correction-request.md" target="_blank" rel="noopener">Correction request issue</a>.
These are reviewed individually, not auto-approved or auto-denied.</p>

<h2>Full contribution guide</h2>
<p>See
<a href="https://github.com/disclosure-commons/cybersecurity-ethics-commons/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener">CONTRIBUTING.md</a>
for the full editorial review process and release/versioning workflow.</p>
"""
    return page_shell(
        "Contribute",
        "How to propose a new case or request a correction.",
        body, active_path="/contribute/", depth=1,
    )


def build_articles(articles):
    items = "".join(
        f'<li><a href="{esc(url)}" target="_blank" rel="noopener">{esc(title or url)}</a>'
        f'<span class="src">{esc(url)}</span></li>'
        for url, title in articles
    )
    body = f"""
<h1>Further reading</h1>
<p class="dek">A curated set of articles and essays on cybersecurity research ethics, disclosure norms, and legal overreach.</p>
<ul class="article-list">{items}</ul>
"""
    return page_shell(
        "Further reading",
        "Curated articles on cybersecurity research ethics and disclosure norms.",
        body, active_path="/articles/", depth=1,
    )


def build_cite(case_count):
    body = f"""
<h1>Cite this dataset</h1>
<p class="dek">If you use this dataset in published or classroom work, please cite it as follows.</p>

<h2>Recommended citation</h2>
<div class="cite-block">[Author name(s)]. (2026). Disclosure Commons: Cybersecurity Ethics Case Library (Version 1.0) [Data set]. Zenodo. https://doi.org/XX.XXXX/zenodo.XXXXXXX</div>
<p>A permanent DOI will be added here once the first release is archived on Zenodo. Until then, cite the
GitHub repository directly and note the access date.</p>

<h2>License</h2>
<p>Case data ({case_count} cases as of this build) is released under
<a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>
&mdash; reuse and adapt with attribution. Site code is released under the MIT License.</p>

<h2>Individual case citation</h2>
<p>Each case page has a stable URL (e.g. <code>/cases/014/</code>) suitable for citing a single case directly,
in addition to citing the dataset as a whole.</p>
"""
    return page_shell(
        "Cite this dataset",
        "How to cite the Disclosure Commons dataset and individual cases.",
        body, active_path="/cite/", depth=1,
    )


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    cases = data["cases"]
    categories = data["categories"]

    years = []
    for c in cases:
        years.extend(int(n) for n in re.findall(r"\d{4}", c.get("year", "")))
    years_min, years_max = (min(years), max(years)) if years else ("", "")

    tags_by_dim = {
        "Actor Intent": [
            ("Good faith (intended public benefit)", "Researcher genuinely aimed to improve security or protect the public, regardless of legal outcome."),
            ("Ambiguous / gray area (mixed or unclear intent)", "Intent is unclear, mixed, or disputed."),
            ("Financially motivated (profit, stock, bounty)", "Disclosure or research was significantly shaped by financial gain."),
            ("Malicious / reckless (knowingly harmful)", "Actor knowingly caused harm or acted with reckless disregard."),
            ("Institutional action against researcher", "A government, corporation, or institution took action against a researcher."),
        ],
        "Actor Type": [
            ("Academic researcher", "Faculty, PhD student, or postdoc affiliated with a university."),
            ("Student", "Undergraduate or graduate student at a university."),
            ("Independent / contractor", "Freelance security researcher, pen-tester, or consultant."),
            ("Corporate / private sector", "Employee of a company, security firm, or private organization."),
            ("Journalist / activist / independent", "Reporting or advocacy-driven disclosure."),
            ("Government / law enforcement", "Acting in an official government or law-enforcement capacity."),
        ],
    }

    articles = [
        ("https://www.eff.org/issues/coders", "Coders' Rights Project"),
        ("https://www.eff.org/effector/32/12", "Security research is not a crime"),
        ("https://www.theregister.com/security/2005/08/23/legal-disassembly/1099308", "Legal disassembly"),
        ("https://www.wired.com/2015/04/twitter-plane-chris-roberts-security-reasearch-cold-war/", "Hacker's Tweet Reignites Ugly Battle Over Security Holes"),
        ("https://www.wired.com/2016/10/hacking-car-pacemaker-toaster-just-became-legal/", "It's Finally Legal To Hack Your Own Devices (Even Your Car)"),
        ("https://medium.com/@ptcrews/to-disclose-or-not-disclose-the-ethics-of-vulnerability-disclosure-aaf09c1ab4b0", "To Disclose or not Disclose: The Ethics of Vulnerability Disclosure"),
        ("https://www.securityweek.com/drone-maker-dji-researcher-quarrel-over-bug-bounty-program/", "Drone Maker DJI, Researcher Quarrel Over Bug Bounty Program"),
        ("https://arxiv.org/abs/2112.01635", "arXiv:2112.01635"),
    ]

    # --- Home ---
    home_hero_grid = build_home(cases, categories, years_min, years_max)
    home_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Disclosure Commons &middot; Cybersecurity Ethics Case Library</title>
<meta name="description" content="A public library of {len(cases)} cybersecurity research ethics cases &mdash; disclosure fights, CFAA prosecutions, dual-use dilemmas, and institutional retaliation.">
{FONT_LINK}
<link rel="stylesheet" href="./assets/style.css">
</head>
<body>
{nav_html("/", 0)}
{home_hero_grid}
{footer_html(0)}
</body>
</html>
"""
    write(DOCS / "index.html", home_html)

    # --- Case pages ---
    for i, case in enumerate(cases):
        html = build_case_page(case, cases, i)
        write(DOCS / "cases" / f"{case['id']:03d}" / "index.html", html)

    # --- Taxonomy ---
    write(DOCS / "taxonomy" / "index.html", build_taxonomy(cases, categories, tags_by_dim))

    # --- About ---
    write(DOCS / "about" / "index.html", build_about())

    # --- Contribute ---
    write(DOCS / "contribute" / "index.html", build_contribute())

    # --- Articles ---
    write(DOCS / "articles" / "index.html", build_articles(articles))

    # --- Cite ---
    write(DOCS / "cite" / "index.html", build_cite(len(cases)))

    # --- Copy data for the browse app to fetch client-side ---
    write(DOCS / "assets" / "cases.json", json.dumps(data, indent=0))

    print(f"Built {len(cases)} case pages + 6 section pages + home.")


if __name__ == "__main__":
    main()
