# Company search

`oxygen companies search` is the one company-search entrypoint: account lists, TAM pulls, lookalikes, local businesses, hiring and technology account lists, and companies from a known public source. The generic `oxygen search` surface answers a company-shaped request with a typed `use_companies_search` error, and lead-sourcing hands its account step here through a `delegate_to` block.

## See real companies for free

`companies search filters` lists the native fields and `companies search preview --filters-json <filters>` returns up to 50 real companies for free. Its answer leads with the totals, notes and a priced `next_step` that saves every match (`next_step_quote.save_to_table` holds its size, pages and credits); each row is compact (name, domain, LinkedIn, headcount, industry, location, a one-line description), and `--view full` (MCP `view: "full"`) adds the provider record. The preview takes the provider's native names (`hq.country_code`, `industry.include`, `employee_count.min`); `companies search plan` and `run` take the planner shape (`geo.countries`, `industries.include`, `employee_count.min`). A wrong-shape key is refused and names the sibling command's spelling.

## Plan, dry run, live

```bash
oxygen companies search plan --prompt "Series A fintech companies in Germany, 20-200 employees" \
  --filters-json '{"industries":{"include":["fintech"]},"geo":{"countries":["DE"]},"employee_count":{"min":20,"max":200},"funding":{"stages":["series_a"]}}' --estimate --json
oxygen companies search run --plan-json ./plan.json --route-id <route_id> --mode dry_run --json
oxygen companies search run --plan-json ./plan.json --route-id <route_id> --mode live --max-credits <cap> --approved --json
```

The planner takes typed filters next to the prompt: industries, keywords, `employee_count`, `employee_range`, founded year, company types, revenue, geo (ISO-3166 alpha-2 countries plus cities and states), funding stages, amounts and dates, technologies, `lookalike_domains` and a `hiring` block. A prompt alone pre-fills `extracted_filters`; explicit `--filters-json` wins per filter path, and `filters` shows the merge. Read the plan before spending:

- `filter_application[]`: per route, the filters `applied` and `dropped`, with the reason. **A dropped filter is never described as applied.** Constraints that could not be parsed or expressed surface as the `unparsed_constraints`, `dropped_constraints` and `unsupported_constraints` gates; re-pass an important hint through `--filters-json` or pick a route that covers it.
- `estimated_match_count`: `--estimate` runs a free provider count when a free count route exists and resolves provider enums for free (`preflight_resolution`). **Quote a number only when `basis` is `provider_count`, and name the probe.** Otherwise say the provider publishes no free count and the real count appears as rows land. When no managed route can count companies for free, the plan says so in its `no_managed_company_count` gate.
- `routes[]` with `routing_rationale` (why each route ranks where it does), and `recommended_live_route_id`, the route that can go live now. A route listing `required_inputs` needs those values first; a route with `requires_preflight=true` needs server-verified preflight proof before it runs live.
- `provider_availability`: `degraded: true` is a known bench, `availability: "unknown"` means it could not be checked (retry the preview). A live run refuses a known benched managed primary before it creates a table or reserves credits. A snapshot is not a dispatch guarantee.

A live run cascades the route's primary tool and then its fallbacks, and auto-paginates toward the plan's target within `--max-credits`; `auto_paged` reports requested against granted pages. A plan with no named count targets every match its live route can reach, up to a tenth of the spendable credits, and the run stops when the source runs out; `target_count_default` explains the size. The dry run reads the live route's own free count and sizes the run to it. Without `--table` the run creates one; `--project <folder>` chooses where it lands (ignored with `--table`: a run fills a table, it never moves one). The run returns an ingestion, not rows: `oxygen table-ingestions wait <run_id> --json`, then `oxygen tables query <table> --limit 10 --json`.

## Headcount and shapes

`employee_count` is the live count: write it for "51-200 employees". `employee_range` (people search: `company.employee_range`) matches the band a company declares on its own page, which lags the live count for more than half of a sample. A malformed shape (`company.domains: ["acme.com"]` instead of `{"include": ["acme.com"]}`, or `employee_count: "51-200"`) is refused with `invalid_filters` naming the field; nothing is dropped silently.

## Intents

- **Lookalikes**: up to five seed `lookalike_domains` (or `--source-intent lookalike`) fan out as one provider call per seed into one table, deduped on domain; the dry run reports `fan_out.calls`, and the quote is per seed.
- **Who is hiring, as postings**: `companies search filters --source hiring` lists the job fields (`job.title.include`, `job.date_posted.last_days` and the `company.*` block). `companies search preview --source hiring --filters-json <filters>` shows matching postings free (one row per role, recruitment agencies excluded, the last 45 days unless set). `companies search run --source hiring --source-filters-json <filters>` imports them, deduped on the posting URL. Without `--target-count` a run imports every posting up to 5,000, bounded by a tenth of the spendable credits (the preview's `next_step` names that size); a run that stopped at its target says `stopped_by: row_target`.
- **Who is hiring, as accounts**: `companies search plan --source-intent hiring` with the `hiring` block returns one deduplicated company row with `matched_jobs` and firmographics, with no link to each posting. Always bound recency, or the list is a job board rather than a signal.
- **Local businesses**: `companies search preview --source google_maps --filters-json '{"q":"<category> in <place>"}'` shows up to 20 businesses for 0 Oxygen credits, but still calls the supplier. `companies search run --source google_maps --source-filters-json '<same>' --target-count <n> --mode dry_run` returns a free quote and the exact `output_columns` and `run_request`; inspect them before the approved live call with the quoted ceiling. Maps takes the area inside `q` (no country filter).
  The import saves `name`, `website`, `phone`, `google_maps_url`, `place_id` and `cid`, plus the listing details and returned place record in `raw_source`. `google_maps_url` is built from `cid`; `place_id` preserves the provider's `placeId`. The native import upserts on `cid`: an overlapping listing updates its existing row, while separate offices sharing a website stay separate. It handles the provider cursor across pages and stops at the row target, page or credit ceiling, or when results end. `total_results: null` means the source publishes no total; the target is a ceiling, not a match count.
- **Company names to websites**: `companies search plan --prompt "Find the websites for these companies: <names>" --source-intent url_recovery`, then validate identity before writing a canonical domain or LinkedIn URL. Resolve domains before any people search at those companies.
- **Technology users**: the technology route (technographic filters) and a technology label lookup when the label is uncertain.
- **Concepts the filters cannot express**: semantic company search (Exa) and web discovery; **a known public source**: scrape the URL you have (Firecrawl), searching for candidate URLs first when there is none.

Rows land in a table with source tool, source query, run id and provider request metadata. Move to contacts, enrichment or outreach only after the accounts have stable domains, acceptable duplicates and visible provenance.

## Live TAM

To keep a TAM refilling, bind the route you ran as a pull feed. Copy `request`, `rows_path` and `row_mapping` from the chosen route in the plan; the feed replays that exact request:

```bash
oxygen feeds bind <table> --kind company_search --tool-id <route_tool_id> --request-json ./request.json --rows-path <rows_path> --row-mapping-json ./mapping.json --upsert-key domain --every daily@9 --max-credits <n> --approved --json
oxygen feeds run <feed> --mode dry_run --json
```

A company search plan carries no `schedulable` flag: bind, and treat a `feed_not_incremental` refusal (no resumption point) as the answer. Blitz company search pages by cursor and can be armed; Apollo cannot. **The cadence is a second, separate approval**: the first run is one purchase, the feed a standing one, and raising its ceiling or changing `--every` asks again. Feed mechanics: the `oxygen-tables` skill (`references/feeds.md`).

## Rules

- Direct Apollo company search requires the workspace's own Apollo key. Automatic company search uses Blitz and specialized providers; Apollo is never an automatic fallback.
- Live runs need `--approved` and `--max-credits`; quote the ceiling in the same sentence as the action and send exactly that number.
- The dry-run request is the provider contract; never rewrite a payload from memory. Never live-run a count route, a placeholder actor id or a route still missing `required_inputs`.
- The browser equivalent is the new-table wizard at `/tables/new`; its plan, priced button and cadence step call the same routes.
