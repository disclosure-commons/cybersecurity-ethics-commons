# Disclosure Commons — Cybersecurity Ethics Case Library

A working library of real cybersecurity research ethics cases — disclosure fights, CFAA prosecutions, dual-use research dilemmas, and institutional suppression — for teaching, citation, and reuse.

**[Browse the case commons →](https://disclosure-commons.github.io/cybersecurity-ethics-commons/)**

## What's here

- **94 tagged cases**, each with its own citable page, plus an interactive filterable browser.
- **An 8-category taxonomy** (see [`data/schema.md`](data/schema.md) and the site's [Taxonomy page](https://disclosure-commons.github.io/cybersecurity-ethics-commons/taxonomy/)).
- **Raw data exports** (`data/cases.csv`, `data/cases.json`) for reuse in your own research, teaching materials, or tools.
- A static-site build script (`scripts/build_site.py`) that regenerates every page from `data/cases.json` — the dataset is always the single source of truth.

## Site pages

| Page | URL |
|---|---|
| Home | `/` |
| Browse (interactive, filterable) | `/browse/` |
| Individual case pages | `/cases/001/` … `/cases/094/` |
| Taxonomy | `/taxonomy/` |
| About / methodology | `/about/` |
| Contribute | `/contribute/` |
| Further reading | `/articles/` |
| Cite this dataset | `/cite/` |

## Repository structure

```
.
├── docs/                       # published via GitHub Pages
│   ├── index.html              # Home (generated)
│   ├── browse/index.html       # Interactive browser (hand-maintained)
│   ├── cases/NNN/index.html    # One static page per case (generated)
│   ├── taxonomy/index.html     # (generated)
│   ├── about/index.html        # (generated)
│   ├── contribute/index.html   # (generated)
│   ├── articles/index.html     # (generated)
│   ├── cite/index.html         # (generated)
│   └── assets/
│       ├── style.css           # shared design tokens (hand-maintained)
│       └── cases.json          # copy of data/cases.json, fetched by browse/
├── data/
│   ├── cases.csv
│   ├── cases.json              # source of truth
│   └── schema.md                # taxonomy + field definitions
├── scripts/
│   └── build_site.py            # regenerates everything under docs/ except
│                                  #   assets/style.css and browse/index.html
├── .github/ISSUE_TEMPLATE/
│   ├── new-case.md
│   └── correction-request.md
├── CONTRIBUTING.md
└── LICENSE
```

## Updating the site

1. Edit `data/cases.csv` (or `cases.json` directly).
2. Keep both files in sync, or regenerate `cases.json` from the CSV.
3. Run:
   ```
   python3 scripts/build_site.py
   ```
4. Commit the regenerated `docs/` output along with the data change.

`docs/assets/style.css` and `docs/browse/index.html` are hand-maintained — the build script does not touch them.

## Citation

See the [Cite this dataset](https://disclosure-commons.github.io/cybersecurity-ethics-commons/cite/) page for the current recommended citation and DOI (once minted via Zenodo).

## Corrections and removal requests

Every case is drawn from previously published reporting, court records, or public statements — sources are linked on each case page. To request a correction, added context, or reconsideration of an entry, open an issue using the templates in `.github/ISSUE_TEMPLATE/`, or visit the [Contribute page](https://disclosure-commons.github.io/cybersecurity-ethics-commons/contribute/).

## License

- **Case data** (`data/`, `docs/cases/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — reuse and adapt with attribution.
- **Site code**: [MIT License](LICENSE).
