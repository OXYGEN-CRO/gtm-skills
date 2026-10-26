# Linkup Runbook

**Own key only.** Linkup runs on the workspace's own key: a call bills that account plus OXYGEN's per-call BYOK platform fee when it applies, which the preview shows. It is available for explicit requests and is absent from the default managed search chain.

## When to use it

- `linkup.search` for sourced answers, citations and schema-shaped output.
- `linkup.fetch` for known HTML or PDF sources.
- `linkup.research_create` for asynchronous research, followed by exact task-id polling.

## Execute and verify

Hydrate the selected operation with `oxygen tools get <tool_id> --json`. Inspect its current inputs, credential requirements, limits and quote, then preview a bounded request. Research depth can materially change charges on the customer's Linkup account; obtain approval for that scope before a live call. Poll only the returned task id, and read the result and citations before using it in a Table.

For managed research, inspect the current `answer_question` or Web Research Agent column route and quote. Keep PDF page budgets explicit and bounded.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `linkup.credits_balance` | free — not billed | no_bill | none | — |
| `linkup.fetch` | 0.5 cr | pre_authorize | paid_provider | — |
| `linkup.research_create` | 125 cr | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `linkup.research_get` | free — not billed | no_bill | none | — |
| `linkup.research_list` | free — not billed | no_bill | none | — |
| `linkup.search` | 3 cr | pre_authorize | paid_provider | — |
| `linkup.tasks_create` | 3 cr | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `linkup.tasks_get` | free — not billed | no_bill | none | — |
| `linkup.tasks_list` | free — not billed | no_bill | none | — |
<!-- END GENERATED -->
