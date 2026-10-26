# Exa Runbook

Use this runbook when OXYGEN tool discovery returns `exa.*` tools for web retrieval, company discovery, people/profile discovery, source expansion, content fetching, or cited answers.

## When To Use

- You need auditable web sources before an AI column scores, classifies, or writes outreach context.
- You are looking for niche companies from a natural-language description that structured company databases may miss.
- You have known URLs and need page text, highlights, summaries, subpages, or crawl status.
- You need a one-off cited answer and do not need row-level source records first.

## Before Running

```bash
oxygen tools search exa --json
oxygen tools get exa.search --json
oxygen tools get exa.contents --json
oxygen tools run exa.search --mode dry_run --input-json '{"query":"B2B SaaS companies selling compliance automation","numResults":3,"contents":{"highlights":true}}' --json
```

Inspect descriptor cost posture, required fields, category restrictions, result shape, and fallback tools. Exa runs managed on Oxygen credits (priced per operation in the generated block below). A BYOK override with the org's own Exa key is supported; only then is the connected Exa account charged instead.

For large `exa.contents` table batches, prefer connecting a BYOK Exa key before the live run. Oxygen's managed key is paced for shared-key safety; BYOK uses the workspace's own Exa capacity and gives more predictable throughput for hundreds or thousands of known URLs.

## Recommended Patterns

- For table workflows, run `exa.search` or `exa.company_search`, inspect result rows, then run `exa.contents` on selected URLs.
- For `exa.contents` runs over hundreds of rows, use a one-row pilot, cap `text.maxCharacters`, and recommend BYOK Exa credentials before starting the full batch.
- Use `exa.company_search` when the user describes a company type conceptually. Use structured company providers first when the user has crisp filters like headcount, funding, industry, geography, or revenue.
- Use `exa.people_search` only for profile discovery. Follow with identity validation and contact enrichment providers before email or phone use.
- Use `exa.find_similar` to expand from a known good customer page, portfolio page, article, category page, or competitor URL.
- Use `exa.answer` for one-off synthesis. Prefer retrieval-first tools when the output will feed rows, cells, approvals, or outbound copy.

## Gotchas

- `type` controls search strategy. Use `category` for `company`, `people`, `news`, `personal site`, `financial report`, and `research paper`.
- Exa's `company` and `people` categories reject several general filters, including publish/crawl date filters, text include/exclude filters, and excluded domains.
- Exa's `people` category only accepts LinkedIn domains in `includeDomains`.
- Content options can increase response size and provider cost. Set `text.maxCharacters` or use highlights for pilots.
- Managed `exa.contents` table runs are intentionally paced below Exa's documented `/contents` ceiling so one workspace cannot monopolize the shared Oxygen key. BYOK is the right posture for sustained large-batch web research.
- Exa does not verify emails, find phone numbers, write CRM records, send messages, or enroll outbound campaigns.

## Approval

Before live batch runs, show row scope, selected Exa operation, requested `numResults`, content options, livecrawl/cache posture, expected maximum provider spend if known, and a one-row pilot output. Require explicit approval before broad live runs or any workflow that combines Exa results with external writes.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `exa.answer` | 2.5 cr | pre_authorize | paid_provider | — |
| `exa.company_search` | 3.5 cr (example payload; estimate 3.5–48.5 cr) | pre_authorize | paid_provider | — |
| `exa.contents` | 0.5 cr (example payload; estimate 0.5–5050 cr) | pre_authorize | paid_provider | — |
| `exa.find_similar` | 3.5 cr | pre_authorize | paid_provider | — |
| `exa.people_search` | 3.5 cr (example payload; estimate 3.5–48.5 cr) | pre_authorize | paid_provider | — |
| `exa.search` | 3.5 cr (example payload; estimate 3.5–48.5 cr) | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
