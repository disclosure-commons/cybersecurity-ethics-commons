# Contributing

## Proposing a new case

1. Open an issue using the "New case" template.
2. Include at minimum: institution/actor name, year, a factual summary, and at least one link to public reporting or a primary source.
3. Suggest a primary category from [`data/schema.md`](data/schema.md), but the final tagging call is made during review.
4. Cases involving unpublished, leaked, or non-public information will not be accepted, regardless of how it was obtained.

## Requesting a correction or reconsideration

Use the "Correction request" issue template. Common reasons:
- A factual error (wrong date, outcome, or attribution)
- A legal outcome has changed since the entry was written (e.g. a conviction was later expunged or overturned)
- You are a subject of the case and want added context or a request reviewed

Corrections are handled case by case. We don't auto-remove entries on request, since the accountability and teaching value of many cases depends on them staying in the record — but we do take reconsideration requests seriously, particularly where a legal outcome has since changed in the subject's favor.

## Editorial review for new cases

New case submissions are checked for:
- Verifiable sourcing (a working link to reporting, a court record, or a public statement)
- Whether it adds a genuinely distinct ethical scenario, not a near-duplicate of an existing case
- Whether the primary category and tags fit the existing taxonomy, or whether the taxonomy itself needs to be extended

## Releasing a version

When a meaningful batch of changes (new cases, corrections, taxonomy updates) has accumulated:

1. Update `data/cases.csv` and `data/cases.json` together — they must stay in sync.
2. Tag a GitHub release (e.g. `v1.1`).
3. Archive that release on [Zenodo](https://zenodo.org) to mint or update the dataset's DOI.
4. Update the citation block in `README.md` if this is the first release.

Small typo fixes don't need a full version bump; batch them into the next scheduled release instead.
