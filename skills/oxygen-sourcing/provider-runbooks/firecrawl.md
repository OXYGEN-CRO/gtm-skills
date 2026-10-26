# Firecrawl Runbook

Use Firecrawl when the GTM question starts from public web content: account websites, competitor pages, pricing pages, docs, help centers, blog posts, or web search results. Do not use it for verified emails, phone numbers, CRM writes, outbound enrollment, or LinkedIn actions.

## Account Website Research

Goal: populate a workspace table with website facts that help qualify accounts or compare competitors.

1. Check `firecrawl.credit_usage` and `firecrawl.queue_status` before paid work.
2. For one known page, run `firecrawl.scrape` with a narrow `formats` list such as `["markdown", "links"]`.
3. For unknown page URLs on a known domain, run `firecrawl.map` with a low `limit` and a focused `search` phrase such as pricing, docs, integrations, security, or customers.
4. For selected URLs, run `firecrawl.batch_scrape_start` only after the operator approves the exact URL count and credit cap, then poll `firecrawl.batch_scrape_status` and inspect `firecrawl.batch_scrape_errors`.
5. For broad website traversal, run `firecrawl.crawl_params_preview` first, require an explicit `limit`, then start `firecrawl.crawl_start` only after the operator approves the scope and credit cap.
6. Write markdown, metadata, source URL, status, credits used, and job ids back into table cells or run provenance.

## Cost Controls

- Always set `limit` for crawls and searches.
- Prefer `map` before `crawl_start` when users need to inspect URL scope.
- Prefer `batch_scrape_start` over `crawl_start` when URLs are already selected.
- Treat JSON extraction, enhanced proxy modes, PDF parsing, and zero data retention as credit multipliers.
- Cancel active crawl or batch jobs only after checking the matching status endpoint.

## Useful Fallbacks

- Known URL: `firecrawl.scrape`.
- Many known URLs: `firecrawl.batch_scrape_start`.
- Known domain but unknown pages: `firecrawl.map`.
- Broad site traversal: `firecrawl.crawl_params_preview`, then `firecrawl.crawl_start`.
- Recent job id recovery: `firecrawl.activity`.
- Failures: `firecrawl.crawl_errors` or `firecrawl.batch_scrape_errors`, then retry selected URLs.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `firecrawl.active_crawls` | free — not billed | no_bill | none | — |
| `firecrawl.activity` | free — not billed | no_bill | none | — |
| `firecrawl.batch_scrape_cancel` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits) |
| `firecrawl.batch_scrape_errors` | free — not billed | no_bill | none | — |
| `firecrawl.batch_scrape_start` | 3.2 cr (example payload; estimate 1.6–160 cr) | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `firecrawl.batch_scrape_status` | free — not billed | no_bill | none | — |
| `firecrawl.crawl_cancel` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits) |
| `firecrawl.crawl_errors` | free — not billed | no_bill | none | — |
| `firecrawl.crawl_params_preview` | free — not billed | no_bill | none | — |
| `firecrawl.crawl_start` | 16 cr (example payload; estimate 1.6–160 cr) | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `firecrawl.crawl_status` | free — not billed | no_bill | none | — |
| `firecrawl.credit_usage` | free — not billed | no_bill | none | — |
| `firecrawl.map` | 1.6 cr | pre_authorize | paid_provider | — |
| `firecrawl.queue_status` | free — not billed | no_bill | none | — |
| `firecrawl.scrape` | 1.6 cr (example payload; estimate 1.6–8 cr) | pre_authorize | paid_provider | — |
| `firecrawl.search` | 3.2 cr (example payload; estimate 3.2–32 cr) | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
