# BlitzAPI Runbook

Use this runbook when OXYGEN tool discovery returns `blitzapi.*` tools for prospecting, enrichment, or email-related work. Blitz returns verified B2B decision-makers from a 380M+ LinkedIn-based dataset.

## When To Use

- You need managed provider coverage through OXYGEN without configuring the user's own provider key.
- You are sourcing people or companies by ICP, or enriching known people or companies from table rows.
- You need a quick pilot before choosing a broader provider chain.

## Before Running

```bash
oxygen tools search blitz --json
oxygen tools search --provider blitzapi --all --no-access-check --json
oxygen tools get <blitzapi_tool_id> --json
oxygen billing balance --json
```

Inspect the descriptor for input schema, credit posture, output shape, and whether the tool is read-only or writes externally. `blitzapi.key_info` is a free, unbilled preflight: it reports key validity, `records_remaining` with its `next_reset_at`, the per-endpoint `max_requests_per_seconds`, and `allowed_apis` (phone enrichment needs a phone-capable plan).

## Endpoint Routing

Pick exactly one search tool per motion — getting this wrong makes everything downstream wrong:

| You have… | You want… | Tool | Pagination |
|-----------|-----------|------|------------|
| An ICP (industry/size/geo + persona) | People across **many** companies | `blitzapi.people_search` | cursor, read `total_results` |
| An ICP, but companies not people | An **account list** | `blitzapi.company_search` | cursor, read `total_results` |
| One named account | The **best** decision-maker via a priority cascade | `blitzapi.waterfall_person_search` / `waterfall_icp_search` | none — single set |
| One named account | **Every** matching employee, or a head-count | `blitzapi.employee_search` | page, read `total_pages` |
| A hiring ICP | Distinct companies plus matching-job counts | `blitzapi.tam_by_jobs` | cursor, 50k companies |
| A hiring market | Individual job postings | `blitzapi.job_search` | cursor, 5k postings |
| One known account | Its individual job postings | `blitzapi.company_jobs_search` | cursor, 5k postings |

Shortcuts:

- "Build me a prospect list" → `people_search` directly; it takes the same company filters as `company_search` and returns the people in one call — no need to chain.
- "Who is the buyer at <company>" / "break into these 500 accounts" → waterfall, one call per account.
- "Everyone in Sales at <company>" / "how big is X" → `employee_search` (enum-only filters, no job-title keywords; `total_pages` sizes the company).
- Row only has a domain → `blitzapi.domain_to_linkedin` first, then the account-scoped tool.
- "Which companies are hiring X, and how many roles" → `tam_by_jobs`. Each row is `{company: {name, linkedin_url, domain, …}, matched_jobs}`, so map `company.name`, `company.linkedin_url` and `matched_jobs`. It has no posting links; use `job_search` for those.

## Recall-First Filter Strategy

There are two ways a Blitz search underperforms, and only the first is obvious:

1. **Enum typo → hard 0 results.** Enum values are case-sensitive and fail silently (`"SaaS"` ≠ `"Software Development"`). See "Enum-Backed Fields" below — OXYGEN rejects unknown values with `invalid_provider_enum_value` before the provider call, which protects you from typos but not from sparse fields.
2. **Correct-but-sparse field → silent recall collapse.** `industry`, `job_level`, `job_function`, and `type` only match records *tagged* with them. A clean-looking search can quietly return a fraction of the real population — no error, just a plausible-looking smaller number.

Build the backbone from **dense** fields nearly every record has, and treat sparse enums as precision knobs:

| Backbone — dense, high-recall | Precision knobs — sparse, lossy |
|---|---|
| `people.job_title` (full-text; everyone has one) | `people.job_level`, `people.job_function` (tagged only) |
| `company.keywords` (searches the company description) | `company.industry` (tagged only) |
| city filters (keyword-matched), `employee_range` | `company.type`, revenue-style fields |
| `people.min_connections` | |

`people.job_title.include` is full-text search and values OR together — spray synonyms, long and short forms, and multilingual variants (`Head of Sales`, `VP Sales`, `Vice President of Sales`, `CRO`; `HR` / `RH` / `Ressources Humaines` when the geo spans languages). Wrap a value in brackets (`"[VP Sales]"`) only when you want exact matching. Keep `include_linkedin_headline` false except in deliberate low-precision passes. De-noise by sampling results and iterating keywords, not by stacking sparse enum filters.

Through the managed route (`oxygen people search plan/run`, `oxygen_people_search_*`), `filters.titles.include` is sent **unbracketed** — full-text — by default. Opt into exact matching per search with `--title-match exact` (`titles.match_mode: "exact"`); `titles.include_adjacent` always stays full-text. `filters.keywords` maps to `company.keywords`. Bracketing every title is a large recall loss: one security-leadership persona returned a few hundred people bracketed against 28,702 unbracketed.

## Probe Volume Before Pulling

Population size is cheap to read and expensive to pull. Run a 1-result probe and read the count before committing to ingestion:

```bash
oxygen tools run blitzapi.people_search --mode dry_run --input-json '{
  "company": { "keywords": { "include": ["devtools"] }, "hq": { "country_code": ["US"] } },
  "people": { "job_title": { "include": ["VP Engineering", "Head of Engineering"] } },
  "max_results": 1
}' --json
```

Then one live probe (`--mode live`, 1 credit) to read the real `total_results` (`total_pages` for `employee_search`). Add title/keyword variants and adjust geo/headcount, re-probing, until the number stops climbing — saturation or the user's target count is the stop signal. Never bolt on off-ICP keywords just to inflate the number.

## Complete API Surface

Oxygen exposes every current Blitz v2 route except TAM by People (`/v2/company/tam-by-people`), plus the public changelog: 22 operation ids backed by 19 distinct routes, with three compatibility aliases. Use the exact `--provider blitzapi --all` inventory above; a fuzzy `tools search blitz` can also return relevant tools from other providers. Search and hiring use the paginated tools above. The remaining tools are:

- Person and phone: `person_enrich` (a work email from a LinkedIn URL; it returns no phone), `phone_enrich` (a mobile or direct phone from a LinkedIn URL), `email_to_person`, `phone_to_person`.
- Company identity and detail: `company_profile_enrich` for a full profile from LinkedIn; `domain_to_linkedin` plus its compatibility alias `company_enrich`; and `linkedin_to_domain`.
- Company analytics: `company_distribution_by_country`, `company_employment_distribution` (compatibility alias), and `company_distribution_by_department`.
- Utilities: `current_date`, free `key_info`, and free public `changelog`.

Use `oxygen tools get blitzapi.<operation> --json` for the exact current field schema. The aliases share both the provider endpoint and its endpoint-specific rate-limit bucket; do not treat them as extra throughput.

## The ~50k Ceiling and Partitioning

`people_search` and `company_search` top out around **50,000 reachable results per query** (50 per page, ~1,000 pages); `employee_search` around **10,000 per company** (~200 pages). Beyond the ceiling Blitz **silently truncates** — no error. When the probe shows more than the ceiling, split the ICP into MECE segments that each fit, run them all, and dedupe on `linkedin_url`:

OXYGEN's native People Search run uses the full Blitz contract: request a target up to 50,000 (or `max_pages` up to 1,000), inspect the dry-run credit quote, then approve that bounded run. The 50-row provider page stays internal. Cursor fetches remain sequential because page N returns the cursor for page N+1, while the durable ingestion workers overlap prior-page Table writes at bounded concurrency. The run response exposes both facts under `pagination_execution`; do not describe 50 as an Oxygen table or run limit.

1. **`employee_range` buckets** first — already MECE (`1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1001-5000`, `5001-10000`, `10001+`).
2. Still too big → **geography**: `hq.country_code`, then `sales_region`, then city.
3. Still too big → split the **job-title keyword set into clusters** and run each as its own segment.

**Never partition on a sparse enum** (`industry`, `job_level`): each segment would silently leak every untagged record. In OXYGEN, run each segment as its own ingestion into the same table and let row dedupe on the LinkedIn URL key collapse the union.

## Enum-Backed Fields

Blitz search payloads use normalized enum values for `industry`, `employee_range`, `country_code`, `continent`, `sales_region`, `company_type`, `job_level`, and `job_function`. Passing free-form values is rejected with `invalid_provider_enum_value` before any provider call.

1. After `oxygen tools get`, look at `enum_catalogs[]` for the tool. Each entry lists the catalog's `enum_ref`, the affected `fields[]`, the `value_count`, and a ready-to-run `fetch_command`.
2. Fetch the catalog before drafting a payload:

```bash
oxygen tools enums list --provider blitzapi --json
oxygen tools enums get blitzapi industry --query software --json
oxygen tools enums get blitzapi employee_range --json
oxygen tools enums get blitzapi country_code --query United --json
```

3. Use the exact returned strings (including casing and punctuation). For example, the industry catalog includes both `"Software Development"` and `"Computer Software"` — they're not interchangeable.
   Job functions follow Blitz's taxonomy, not the title: software engineers, engineering managers and other software, data and IT roles are `"Information Technology"`, while `"Engineering"` holds non-software engineering, so a software-team search under `Engineering` can return 0 where `Information Technology` returns the real population. `oxygen tools enums get blitzapi job_function --query software --json` shows the labels.
   Job levels are tags too: `Manager` includes team leads, and a function tag can cover adjacent roles (an `Information Technology` + `Manager` search can return team leads from revenue or support). Check titles in the results.
4. `company.keywords.include` / `company.keywords.exclude` stay free-form — and per the strategy above, they're usually the better lever than `industry` anyway.

## Waterfall Semantics

The cascade is a **priority ranking, not a seniority ladder**: tier 1 is the perfect contact; lower tiers are looser matches or an alternative persona you'd accept. The engine fills `max_results` slots top-tier first and backfills (5 C-levels if it can, else Directors top up the rest). Each result carries `icp` (which tier matched, 1 = top) and `ranking` (relevance within the company) — `icp` is a ready-made persona signal for tailoring outreach copy per tier. Spray full-text title variants within each tier; turn `include_headline_search` on only in lower fallback tiers; use `["WORLD"]` for a global location tier. One result set per call — never paginate or partition a waterfall.

## Enrich Last

Enrichment (`person_enrich`, `phone_enrich`) is one paid call per row. Order the table pipeline as:

> search → dedupe on `linkedin_url` → post-hoc ICP cleanup → enrich the survivors.

Never enrich duplicates or rows you're about to discard. Email coverage is broad; **phone is US-only** — gate the phone column on `country_code == "US"` and only add it when the user actually asked for phones. Misses come back as `found: false`, not errors — store the empty result, don't retry. A miss on a direct `blitzapi.*` tool column still bills that column's price; the opinionated work-email, mobile-phone, person-profile and company-enrichment columns bill the Blitz lane only on a hit.

## Table Pattern

- Store the raw result in a JSONB tool column.
- Materialize only stable fields such as work email, phone, company domain, or profile URL into companion columns.
- Preserve provider confidence, `icp`/`ranking` tier metadata, and error codes in the raw result.
- Preserve `source_tool`, `source_query`, provider run id, page or cursor, raw response, and selected title tier in table provenance before any email, phone, CRM, or outbound step.

## Gotchas

- A hard **0** from a correct-looking search means a wrong enum value or over-tight AND filters; a **suspiciously small non-zero** count is usually the sparse-enum trap — drop the sparse enum and lean on the keyword backbone.
- Do not assume all BlitzAPI tools share the same result envelope: `people_search`/`employee_search` return flat person fields in `results[]`, the waterfall nests under `results[].person`. Inspect each descriptor.
- `employee_search` has **no job-title keyword filter** — enum-only. For "who do I contact at this account," switch to the waterfall instead of over-filtering employee pages.
- Treat email/phone discovery as paid unless a dry-run response proves otherwise.
- Prefer a one-row pilot with `oxygen columns run --limit 1` before a background run.

## Approval

For batch enrichment or any partitioned multi-segment pull, show the probe-based volume estimate, estimated credits, row cap, selected tool ID, partition plan if any, and the pilot output before running live.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `blitzapi.changelog` | free — not billed | no_bill | none | — |
| `blitzapi.company_distribution_by_country` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.company_distribution_by_department` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.company_employment_distribution` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.company_enrich` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.company_jobs_search` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.company_profile_enrich` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.company_search` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.current_date` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.domain_to_linkedin` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.email_to_person` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.employee_search` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.job_search` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.key_info` | free — not billed | no_bill | none | — |
| `blitzapi.linkedin_to_domain` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.people_search` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.person_enrich` | 1.5 cr | pre_authorize | paid_provider | — |
| `blitzapi.person_profile_enrich` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.phone_enrich` | 10 cr | pre_authorize | paid_provider | — |
| `blitzapi.phone_to_person` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.tam_by_jobs` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.waterfall_icp_search` | 1 cr | pre_authorize | paid_provider | — |
| `blitzapi.waterfall_person_search` | 1 cr | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
