# Company data

## Presets: one command per bundle

Standard person and company enrichment is one command, not a hand-built column. Name the input column with `--input <slot>=<column>` (any column works whatever it is called; without `--input` the preset guesses from column names):

```bash
oxygen columns add <table> --preset person_enrich --input url=<linkedin_column> --json
oxygen columns add <table> --preset company_enrich --input domain=<domain_column> --json
oxygen columns run <table> company_enrich --limit 1 --dry-run --json
```

- `person_enrich`: one LinkedIn profile lookup, billed only when it finds the person, plus free name, current company, job title, start date, school, headline, bio, location and follower columns filled in the same write. The follower count fills only when the fallback lane answers: the first lane publishes none, so most rows leave it empty.
- `company_enrich`: one company lookup from a domain or company LinkedIn URL (a domain-only row looks up its LinkedIn URL first at no charge; a miss costs nothing), keeping the whole profile in its JSON column plus free name, domain, LinkedIn URL, headcount, industry, description, founded year and HQ country columns. It binds its LinkedIn slot to `current_company_linkedin_url` when the table has one, so `person_enrich` then `company_enrich` enriches each person's company from the URL the person lookup found. When `tools search --for-table` offers company LinkedIn pages for person lookups, bind the company bundle's input explicitly (`--input linkedin_url=<column>`).
- `company_funding` (total raised, latest round, rounds, investors), `company_revenue` (an annual estimate, a figure or a range), `company_hiring` (up to ten open roles with a count) and `company_tech_stack`: each one paid lookup column that fills its own columns from data providers. Prefer them to a research column for the same facts. The quoted figure is the ceiling if every lane is tried.

Presets ship maintained extraction formulas, so nobody parses a provider's raw response. Quote the cost with the dry run, confirm real values on one row (`--limit 1 --approved --max-credits <estimate>`), then run the table. Read values back with `oxygen tables query <table> --fields <keys>`; a run's cost is in `oxygen table-runs get <run_id>` (`creditsUsed`) and each row's in `table-runs items`. A row can bill 0 when the same lookup ran recently and was reused. Web: Add column, Person enrichment, Company enrichment, Tech stack, Funding, Revenue (estimate), Hiring signals; MCP: `oxygen_columns_add` with `preset`.

## Missing fields on existing rows

`companies enrich` fills only empty fields on an Accounts table, from the same 33-field catalog `oxygen find company --list-fields` prints:

```bash
oxygen companies enrich preview accounts --missing-fields domain,linkedin_url,headcount,industry,funding_stage,technologies --limit 25 --json
oxygen companies enrich run accounts --missing-fields domain,linkedin_url,headcount,industry,funding_stage,technologies --limit 25 --approved --max-credits <estimated_credits.max> --json
oxygen table-runs provider-summary <run_id> --json
```

- The preview calls no provider; read `eligible_row_estimate`, `estimated_credits.max` (the ceiling to approve), `would_attempt` (each field's lanes in run order with `credits` per attempt, `billed` saying whether a miss is free (`on_hit`) or every attempt bills (`per_attempt`), and `pre_skip` naming why a lane will not run) and the table link. These are the waterfall's own rules; the `company_enrich` preset above is a different path, whose LinkedIn look-up is never billed. With no eligible rows in the sample, query the table before going live.
- Derived fields (description, founded year, HQ, logo, company type, funding stage, latest round, round count, investors, parent and subsidiaries, job openings, a technology check) are read out of a payload the run already holds and cost nothing extra; their `provider_lanes` is empty by design. Funding stage and rounds are free only when the company's LinkedIn page lists funding; `total_funding` always comes from a funding provider.
- Scope rows with `--limit`, `--row-ids`, `--filter-json` or `--all`. Non-empty values are not overwritten unless you pass `--force`.
- `--providers` narrows the lanes; a provider that runs only on the workspace's own key is used once that key is connected (its runbook says so). Read current prices from the preview, never from a copied number.
- For TAM discovery rather than existing rows, use the `oxygen-sourcing` skill.

## One company, no table

```bash
oxygen find company --list-fields --json
oxygen find company --domain acme.com --fields headcount,industry,funding_stage,competitors,technologies --json
oxygen find company --domain acme.com --fields funding_stage,total_funding,parent_company --mode live --max-credits <estimate.recommended_max_credits> --json
oxygen find company --domain acme.com --fields technology_check --check-technologies hubspot,salesforce --json
```

Defaults are the identity plus what one profile lookup answers for free (`domain,linkedin_url,headcount,industry,description,founded_year,hq_country`). Derived fields show in `attempts` as `oxygen.derive` legs with 0 credits; `competitors`, `corporate_structure`, `acquisitions`, `news`, `technologies` and the profile URL fields each add a priced lane. An unknown field key is refused with the supported list.

## LinkedIn company profile from a domain

The managed public LinkedIn lookup needs no connected account or provider key: `oxygen tools get scraper.linkedin_company --json`, then `oxygen tools run scraper.linkedin_company --input-json '{"domain":"microsoft.com"}' --credential-mode managed --mode dry_run --json`. Inputs each mode accepts: [runbook](../provider-runbooks/scraper.md).
