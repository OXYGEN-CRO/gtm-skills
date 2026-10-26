# Crustdata Runbook

> **Runs only on the workspace's own Crustdata key**, and is in no default chain. Connect it with
> `oxygen integrations connect crustdata --api-key <key>`, then select it with `--tool-id` or `--route-id` on a search run, or
> `--provider-order` on an enrichment column.
> A call on your key spends your Crustdata credits; OXYGEN's per-call BYOK platform fee, when it applies, shows in the preview and in
> `oxygen billing usage --meter byok_calls --json`. The generated table lists OXYGEN's
> rates for reference.

Use this runbook when OXYGEN tool discovery returns `crustdata.*` tools for account sourcing, people sourcing, company or person enrichment, hiring-signal analysis, web research, legacy migration support, or watcher-backed signal monitoring.

## When To Use

- You need account lists from structured company filters such as domain, industry, geography, funding, headcount, growth, or hiring signals.
- You need people discovery by role, company, location, skills, education, or related structured filters.
- You have reviewed company or person identifiers and need selected enrichment fields.
- You need person phone fields for a qualified row and can keep requested fields narrow.
- You need indexed job listings or job-count aggregations as a hiring signal.
- You need web search or page fetches for current public research sources.
- You need a watched Crustdata signal to feed an Oxygen workflow through a reviewed webhook endpoint.

Do not use Crustdata to send messages, enroll campaigns, write CRM records, or run generic outbound execution. Use outbound or CRM providers for those steps.

## Before Running

Discover the exact tool and cost posture:

```bash
oxygen tools search crustdata --json
oxygen tools get crustdata.company_search --json
oxygen tools get crustdata.person_search --json
oxygen tools get crustdata.company_enrich --json
```

Dry-run representative calls before live runs:

```bash
oxygen tools run crustdata.company_identify --mode dry_run --input-json '{"domains":["example.com"]}' --json
oxygen tools run crustdata.person_search --mode dry_run --input-json '{"filters":{"field":"experience.employment_details.current.title","type":"=","value":"CEO"},"limit":1}' --json
oxygen tools run crustdata.job_search --mode dry_run --input-json '{"filters":{"field":"company.basic_info.primary_domain","type":"=","value":"example.com"},"limit":5}' --json
```

Inspect required fields, output shape, side-effect class, rate limit, fallback tools, and managed/BYOK auth requirements.

## Recommended Patterns

- Run autocomplete before paid search when filter values come from user text, scraped labels, or ambiguous categories.
- Check remaining provider headroom with the free `crustdata.account_credits` read before a table-scale run.
- Use company/person search for discovery, then enrich only reviewed rows.
- Use company identify before company enrich when the row has mixed or low-confidence names, domains, or profile URLs.
- Request only the company or person fields the workflow will inspect or materialize.
- For phone enrichment, request `contact.phone_numbers` only when the row has a trusted LinkedIn URL or business email and the user approved phone lookup.
- Store the raw provider envelope in a JSONB tool column and materialize stable values into companion columns such as domain, company id, title, profile URL, business email, job count, and status.
- Read rows from each search endpoint's own key — `company_search` returns `companies[]`, `person_search` returns `profiles[]`, `job_search` returns `job_listings[]` — and paginate with `next_cursor` (null on the last page), not `cursor`.
- Pass `filters` as a single condition object (`{"field": "<dot.path>", "type": "=", "value": ...}`) or an `and`/`or` group; an array of `{field, operator, value}` is rejected before the call.
- Use job search with `limit: 0` plus aggregations when the workflow only needs counts.
- Use web search to find URLs, then fetch only selected URLs with `web_enrich_live`.
- Treat legacy `/screener` operations as migration support. Prefer current Company, Person, Job, and Web endpoints for new workflows.

## Watcher Pattern

- Create watches only after the event scope, webhook endpoint, frequency, expiration date, and downstream workflow owner are explicit.
- Use `watcher_watches_list` and `watcher_watches_get` before update or cancel.
- Prefer `watcher_watches_update` with `status: "paused"` when the user wants reversible behavior.
- Store watch id, status, event slug, endpoint, expiration, notification cap, and last event provenance in Oxygen table or workflow state.
- Remember that creating or managing a watch can be free while later watch processing can consume provider credits.

## Approval

Before live paid runs, show row scope, selected tool IDs, requested fields, expected maximum provider credits, rate-limit posture, fallback order, and a one-row pilot output. Live company/person search, live person enrich, web fetch batches, legacy realtime searches, legacy social-post engagement fields, and watcher create/update/cancel require explicit operator approval.

Stop if identifier type is mixed, filter values are unverified, row scope is broad, webhook ownership is unclear, or the user expects Crustdata to perform outbound/CRM writes.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `crustdata.account_credits` | free — not billed | no_bill | none | — |
| `crustdata.company_enrich` | 50 cr (example payload; estimate 4–100 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.company_identify` | free — not billed | no_bill | none | — |
| `crustdata.company_professional_network_search_live` | 250 cr (example payload; estimate 4–4000 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.company_search` | 3.75 cr (example payload; estimate 0.06–60 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.company_search_autocomplete` | free — not billed | no_bill | none | — |
| `crustdata.job_search` | 3.75 cr (example payload; estimate 0.06–60 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.legacy_company_enrich` | 25 cr (example payload; estimate 2–250 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.legacy_company_identify` | free — not billed | no_bill | none | — |
| `crustdata.legacy_company_linkedin_posts` | 125 cr (example payload; estimate 2–2000 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.legacy_company_search` | 625 cr (example payload; estimate 2–50 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.legacy_companydb_autocomplete` | free — not billed | no_bill | none | — |
| `crustdata.legacy_companydb_search` | 25 cr (example payload; estimate 2–20 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.legacy_filters_autocomplete` | free — not billed | no_bill | none | — |
| `crustdata.legacy_linkedin_filter_autocomplete` | free — not billed | no_bill | none | — |
| `crustdata.legacy_linkedin_posts_keyword_search` | 125 cr (example payload; estimate 2–10000 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.legacy_people_linkedin_posts` | 125 cr (example payload; estimate 2–2000 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.legacy_person_enrich` | 75 cr (example payload; estimate 0–450 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.legacy_person_search` | 125 cr (example payload; estimate 10–20000 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.legacy_persondb_autocomplete` | free — not billed | no_bill | none | — |
| `crustdata.legacy_persondb_search` | 75 cr (example payload; estimate 0–60 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.person_enrich` | 25 cr (example payload; estimate 2–350 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.person_professional_network_enrich_live` | 175 cr (example payload; estimate 14–350 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.person_professional_network_search_live` | 250 cr (example payload; estimate 4–4000 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.person_search` | 3.75 cr (example payload; estimate 0.06–60 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.person_search_autocomplete` | free — not billed | no_bill | none | — |
| `crustdata.watcher_watches_cancel` | free — not billed | no_bill | external_send | async — returns a job handle; poll for completion; external write — live gate (approved + max_credits) |
| `crustdata.watcher_watches_create` | free — not billed | no_bill | external_send | async — returns a job handle; poll for completion; external write — live gate (approved + max_credits) |
| `crustdata.watcher_watches_get` | free — not billed | no_bill | none | — |
| `crustdata.watcher_watches_list` | free — not billed | no_bill | none | — |
| `crustdata.watcher_watches_update` | free — not billed | no_bill | external_send | async — returns a job handle; poll for completion; external write — live gate (approved + max_credits) |
| `crustdata.web_enrich_live` | 25 cr (example payload; estimate 2–20 cr) — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `crustdata.web_search_live` | 25 cr — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
