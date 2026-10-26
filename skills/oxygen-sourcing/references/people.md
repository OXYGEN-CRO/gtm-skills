# People search

`oxygen people search` is the one people and contact entrypoint: personas, decision makers, a named account's people, people at a list of companies, audience sizing and a single profile lookup. Generic `oxygen search`, `oxygen sourcing plan` and `oxygen lead-sourcing plan` delegate their people step here; lead-sourcing stays the account-first wrapper and hands over the accepted account domains as the `company.domains` filter.

## See the people before you pay

`people search filters` lists every native field; `people search preview --filters-json <filters>` returns up to 50 real people for free; `people search run --source people_search --source-filters-json <the same filters>` fills a table with every person matching exactly those filters, with no prompt, plan or source table. The preview's `next_step` names the size: all matches, up to what one query reaches and a tenth of the spendable credits. Use it whenever the persona can be stated as filters: titles, level, function, location, education, and the companies (up to 50 `company.linkedin_url`). Finding people at specific companies is part of the free preview, scoped through `company.linkedin_url`. Its `company_fit` names what a person row cannot show (company headcount and industry, often seniority) and the filters every person matched; `next_step` prices saving them and finding their work emails.

## Planner flow

Use `people search plan` (typed filters) → `run --mode dry_run` → `run --mode live` for prose-to-route compilation, provider fallbacks, a table fan-out or audience sizing.

```bash
oxygen people search plan --prompt "Heads of Data Governance at US fintechs, 200-2000 employees" \
  --filters-json '{"titles":{"include":["Head of Data Governance"]},"seniorities":{"include":["Director","VP"]},"geo":{"countries":["US"]},"company":{"industries":{"include":["fintech"]},"employee_count":{"min":200,"max":2000}}}' --json
oxygen people search run --plan-json ./people-plan.json --route-id <route_id> --mode dry_run --json
oxygen people search run --plan-json ./people-plan.json --route-id <route_id> --mode live --max-credits <cap> --upsert-key linkedin_url --approved --json
```

The planner takes titles (include, adjacent, exclude), seniorities, departments, job functions, names, keywords, geo (ISO-3166 alpha-2 `countries`, `continents`, `sales_regions`), `min_connections`, contactability (require email or phone, email status) and a nested company scope (domains, names, LinkedIn URLs, industries, `employee_count`, technologies). Titles go out as full-text by default; `--title-match exact` opts into exact matching for one search, a large recall loss. Read in the plan:

- `extracted_filters` (explicit `--filters-json` wins per path), `unparsed_constraint_hints` and the `unsupported_constraints` gate.
- `filter_application[]`: per route, `applied` against `dropped`. Contactability is honored only by the reachability route; other routes report it as dropped.
- `estimated_match_count`: on by default, a single zero-credit count probe when one is connected (a deterministic guess otherwise); `--no-estimate` skips it. Size the persona before any paid pull.
- `recommended_live_route_id`: the preferred ingest route without preflight, missing inputs or dropped account scope. Confirm its `tool_access` entry is `runnable`. Routes whose search returns masked records without a stable `linkedin_url` are preview-only and never queued live.

Live runs auto-paginate toward the target within `--max-credits` (`auto_paged` reports pages), and rows upsert on `linkedin_url`. A plan with no named count targets every match its live route can reach, up to a tenth of the spendable credits, and the run stops when the source runs out (`target_count_default`). The dry run reads the live route's own free count and sizes the run to it; the plan's count probe, counting another provider's database, never sizes the run. A route on the workspace's own provider key keeps one page unless you name a count, because its pages bill that provider account. MCP: `oxygen_people_search_plan` and `oxygen_people_search_run`; the plan widget shows filter chips, per-route coverage, the estimate and the gates.

A search repeated into the same table, such as a daily Workflow step, needs `--continue` (MCP `continue: true`) with `--table`: each run resumes where the last run of that exact search stopped, so it adds new people instead of buying page one again. The dry run's `run_request.continuation` shows each search as `first_page`, `continued` or `exhausted`; once every search is exhausted the run refuses with `people_search_exhausted` and spends nothing, so widen the filters. Changing the filters or the target starts a new search from page one. More than 50 values in one include list (for example every manufacturing industry) run as several searches, each billed per page.

## People at companies you already have

**A company table**: fan out over it, one person search per company, with a real `company` relation column back to each company row.

```bash
oxygen people search plan --from-table accounts --linkedin-url-column company_linkedin_url \
  --job-functions Sales --seniorities VP,Director --countries US --min-connections 200 --json
```

`--prompt` is optional with `--from-table`. `source.companies_planned` is the company count the run spends against: the fan-out is priced per company per page, so a 1,900-company table is about 1,900 page charges. Buy one company first with `--company-limit 1` on the live run, then `--table <the table it created> --company-offset 1 --pages-per-company <n>` for the rest; `--max-pages` means pages per company here. MCP: `oxygen_people_search_plan` with `source={table, linkedin_url_column}`.

**A list of companies**: a plain plan with `company.linkedin_urls` (up to 50) is one priced page across all of them, and each person row carries `company_name`, `company_domain` and `company_linkedin_url` to join on. It samples a persona across accounts cheaply; use the fan-out when you need contacts at EACH account and the relation column.

Account scope survives every fallback: a live cascade never advances to a provider that drops `company.names`, `company.domains` or `company.linkedin_urls`. Prefer qualified domains, and resolve company names to domains before live execution when the route cannot apply names exactly.

## Account-scoped specializations

The planner is the default executor; these cover cases it does not:

- A qualified account row with a `company_linkedin_url`: the employee search for every matching employee, or a priority waterfall (`blitzapi.waterfall_person_search`) for the best contact per account ([Blitz](../provider-runbooks/blitzapi.md)).
- A preview-first search with paid single reveals after approval: Wiza (`wiza.people_search`, then `wiza.person_reveal`).
- A masked people pull sized by its free count first: Dropleads ([runbook](../provider-runbooks/dropleads.md)).
- Apollo people search, Lusha and RocketReach run only on the workspace's own key. Apollo search is never an automatic fallback; use Blitz for managed search.

## Rules

- Live runs need `--approved` and `--max-credits`; never live-run a count or preview route, or a route that needs preflight proof it does not have.
- The dry-run request is the provider contract; never rewrite it from memory or start raw `blitzapi.people_search` instead of the planner.
- Confirm the workspace through the plan's `context_confirmation` before sourcing contacts.
- Keep people in a Contacts table linked to the Accounts table, with source tool, query, run id and raw source per row. Enrich (email, phone) only after the rows have stable `linkedin_url` values and acceptable duplicates: the `oxygen-enrichment` skill.
