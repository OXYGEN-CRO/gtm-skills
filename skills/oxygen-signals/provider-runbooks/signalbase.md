# Signalbase Runbook

> **Runs only on the workspace's own SignalBase key**, and is in no default chain. Connect it with
> `oxygen integrations connect signalbase --api-key <key>`, then select it with `--tool-id` or `--route-id` on a search run, or
> `--provider` on a signal search.
> A call on your key spends your SignalBase credits; OXYGEN's per-call BYOK platform fee, when it applies, shows in the preview and in
> `oxygen billing usage --meter byok_calls --json`. The generated table lists OXYGEN's
> rates for reference.

Use this runbook when sourcing or enriching account signals such as company metadata, categories, hiring, funding, website content, or ICP evidence.

## When To Use

- You need account-level signals before finding people.
- You are building or auditing a TAM/account table.
- You need signal columns for scoring, segmentation, or workflow routing.

## Before Running

```bash
oxygen tools search signalbase --json
oxygen tools get <signalbase_tool_id> --json
```

Use company-first sourcing. Keep account and contact tables separate.

## Table Pattern

Recommended account columns:

- `company_name`
- `domain`
- `company_linkedin_url`
- `source`
- `signals`
- `icp_notes`
- `signal_updated_at`

Store raw signal payloads in JSONB. Add formula/AI columns for fit labels after the raw signal column exists.

## Gotchas

- Signal names and filters should come from tool descriptors, not guessed strings.
- Broad company searches should be count- or pilot-first.
- Do not enrich contacts until the account table passes an ICP audit.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `signalbase.acquisition_signals` | 250 cr — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `signalbase.companies` | 100 cr — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `signalbase.funding_signals` | 250 cr — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `signalbase.hiring_signals` | 250 cr — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `signalbase.investors` | 100 cr — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
| `signalbase.job_change_signals` | 250 cr — indicative price — confirm the live quote | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
