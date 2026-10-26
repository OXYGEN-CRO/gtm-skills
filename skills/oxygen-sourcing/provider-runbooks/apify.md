# Apify Runbook

Use `oxygen tools get <tool_id> --json` to discover the exact apify inputs, credential requirements and live quote. Preview a bounded request before approving execution; do not infer a managed price from catalog availability.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `apify.actor_run_abort` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits) |
| `apify.actor_run_status` | free — not billed | no_bill | none | — |
| `apify.dataset_items` | free — not billed | no_bill | none | — |
| `apify.run_actor_async` | no managed price — use an eligible BYOK connection | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `apify.run_actor_sync` | no managed price — use an eligible BYOK connection | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
