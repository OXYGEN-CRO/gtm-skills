# PredictLeads Runbook

Use this runbook when OXYGEN tool discovery returns `predictleads.*` tools. PredictLeads is the default provider for **funding, news and technology signals** (and a secondary for hiring): company-level watch-list reads, market-wide discovery, technology detections, connections, products, GitHub repositories, and startup-platform posts.

Do not use PredictLeads to find or verify contact data, send messages, or write CRM records — use the people-search, email-verification, sequencing, and CRM providers for those.

## Credentials

PredictLeads needs **two** secrets, not one: an API key (`X-API-KEY`) and an organization API token (`X-API-TOKEN`).

- **Managed (default).** OXYGEN's own PredictLeads account; the run is billed in OXYGEN credits.
- **BYOK.** Connect the workspace's own key **and** token. Exactly one half is a misconfiguration and fails closed with `missing_integration_secret` — it never falls through to the managed key.
- `follow_company`, `unfollow_company` and `followed_companies` are **BYOK-only** by design: follow state belongs to the connected account and is never shared through OXYGEN's managed one.

## Vendor error semantics

Read the status before deciding a credential is dead — PredictLeads uses four failure codes with different meanings, each returned as `{"error":{"type","message"}}`:

| Status | `error.type` | What it means | What OXYGEN does |
| --- | --- | --- | --- |
| 401 | `unauthorized` | The key/token pair is rejected. | Real credential failure — reconnect or rotate. |
| 402 | `payment_required` | The account's **monthly request quota** is spent. | Account credit refusal; the plan or the month is the fix, not the key. |
| 403 | `forbidden` | **Request rate over limit** (sustained pacing), not a permission problem. | Retried like a 429, then raised as `rate_limit_exceeded`; lower the pacing. |
| 429 | `too_many_requests` | Short burst over the limit. | Retried with backoff. |

A 403 whose message actually states a permission denial is still treated as a credential/permission failure.

## Cost model

Two different meters, and the difference dominates the bill:

- **Per request** — one provider credit per call, whatever the page returns. Every company-scoped read (`company_*`), every single-record read, and the ordinary discovery endpoints.
- **Per returned record** — one provider credit per company returned, capped by `limit` (1–1,000): `companies`, `company_similar_companies`, `discover_connection_investors`. A careless `limit` here is the difference between one credit and a thousand.

Watch-list monitoring is a **poll**: re-reading 1,000 followed companies each pass costs 1,000 provider credits per pass, so pass frequency, not row count, is the lever. Prefer market-wide `discover/*` reads with date filters (`first_seen_at_from`, `found_at_from`) over re-polling every company when the question is "what happened since X".

## Before running

```bash
oxygen tools search predictleads --json
oxygen tools get predictleads.company_financing_events --json
oxygen tools run predictleads.company_news_events --mode dry_run --input-json '{"company_id_or_domain":"openai.com","page":1,"limit":10}' --json
oxygen tools run predictleads.companies --mode dry_run --input-json '{"location":"California","sizes":["11-50"],"page":1,"limit":25}' --json
```

`discover_job_openings` rejects a pagination-only request: pass `onet_codes` and/or `location`.

## Approval

Live runs need row scope, an explicit `limit` on the result-priced operations, and a credit cap. `follow_company` / `unfollow_company` mutate the connected PredictLeads account and need explicit operator approval on a reviewed company scope.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `predictleads.api_subscription` | free — not billed | no_bill | none | — |
| `predictleads.companies` | 500 cr (example payload; estimate 5–5000 cr) | pre_authorize | paid_provider | — |
| `predictleads.company` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.company_connections` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.company_financing_events` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.company_github_repositories` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.company_job_openings` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.company_news_events` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.company_products` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.company_similar_companies` | 500 cr (example payload; estimate 5–5000 cr) | pre_authorize | paid_provider | — |
| `predictleads.company_technology_detections` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.company_website_evolution` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.discover_connection_investors` | 500 cr (example payload; estimate 5–5000 cr) | pre_authorize | paid_provider | — |
| `predictleads.discover_job_openings` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.discover_products` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.discover_technology_technology_detections` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.extended_technology_detection` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.financing_events` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.follow_company` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `predictleads` API key; provider-side charges may apply |
| `predictleads.followed_companies` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `predictleads` API key; provider-side charges may apply |
| `predictleads.job_opening` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.news_event` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.news_events` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.product` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.startup_platform_posts` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.technologies` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.technology` | 5 cr | pre_authorize | paid_provider | — |
| `predictleads.unfollow_company` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); BYOK — runs on the org's connected `predictleads` API key; provider-side charges may apply |
<!-- END GENERATED -->
