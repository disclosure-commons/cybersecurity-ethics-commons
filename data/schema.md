# Data schema

## Fields (`cases.csv` / `cases.json`)

| Field | Description |
|---|---|
| `id` | Sequential case number, matches the site's "Case No." |
| `institution` | Name of the primary institution or individual actor involved |
| `year` | Year or year range of the case (some are approximate, marked `~`) |
| `summary` | One- to two-sentence factual summary of the case |
| `category` | Primary category — one of the 8 taxonomy categories below |
| `intent` | Actor Intent tag (see below) |
| `actor_type` | Actor Type tag (see below) |
| `disclosure` | How findings were disclosed (e.g. responsible/coordinated, media-first, none/withheld) |
| `outcome` | Legal or institutional outcome of the case |
| `chilling` | `Yes` / `No` — did the case have a documented chilling effect on future research or disclosure? |
| `dilemmas` | Key ethical dilemmas raised, written for classroom discussion |
| `source` | Link to the original reporting or primary source |

## Primary categories

| Category | Description |
|---|---|
| Vulnerability Disclosure | Cases centered on when, how, and to whom to disclose security findings — including responsible disclosure, media-first disclosure, non-responsive vendors, and provocation tactics. |
| Informed Consent & Human Subjects | Research conducted on people or communities without their knowledge or consent — phishing simulations, passive traffic monitoring, Tor de-anonymization, honeypots. |
| Dual-Use Research | Work that produces knowledge, tools, or methods usable for both defense and attack — ransomware simulations, keylogger research, internet-wide scanning, mass vulnerability databases. |
| Legal Boundaries & CFAA Overreach | Cases where good-faith or ambiguous research collided with criminal law, often highlighting disproportionate prosecution or vague statutory language (CFAA, DMCA, CMA). |
| Institutional Suppression | Cases where vendors, governments, or employers used legal, political, or economic power to silence, suppress, or retaliate against researchers exposing flaws or breaches. |
| Financial Conflict of Interest | Cases where research or disclosure was motivated or tainted by profit — short-selling, bug bounty disputes, threat-intelligence monetization, nonprofit commercial data deals. |
| Critical Infrastructure & Public Trust | Research on elections, medical devices, transit, water systems, and power grids where findings carry societal risk beyond the technical, including potential to fuel disinformation. |
| Surveillance & Offensive Tools | Development, sale, or deployment of tools designed to compromise systems at scale — commercial spyware, government malware operations, cyber-mercenary firms. |

## Actor Intent tags

- Good faith (intended public benefit)
- Ambiguous / gray area (mixed or unclear intent)
- Financially motivated (profit, stock, bounty)
- Malicious / reckless (knowingly harmful)
- Institutional action against researcher

## Actor Type tags

- Academic researcher
- Student
- Independent / contractor
- Corporate / private sector
- Journalist / activist / independent
- Government / law enforcement

## Inclusion and sourcing criteria

- Every case must have at least one linked, publicly available source (news reporting, court record, or the subject's own public statement).
- Cases are tagged by a single primary category, chosen for the case's *central* ethical tension, even when multiple categories are arguably relevant. Secondary themes are captured in `dilemmas` rather than as additional category tags.
- No unpublished, leaked, or non-public information is included. See [CONTRIBUTING.md](../CONTRIBUTING.md) for how new cases are vetted before being added.
