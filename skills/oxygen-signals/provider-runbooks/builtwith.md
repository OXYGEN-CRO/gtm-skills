# BuiltWith Runbook

Use `oxygen tools get <tool_id> --json` to discover the exact builtwith inputs, credential requirements and live quote. Preview a bounded request before approving execution; do not infer a managed price from catalog availability.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `builtwith.domain_lookup` | no managed price — use an eligible BYOK connection | pre_authorize | paid_provider | — |
| `builtwith.lists` | no managed price — use an eligible BYOK connection | pre_authorize | paid_provider | — |
| `builtwith.relationships` | no managed price — use an eligible BYOK connection | pre_authorize | paid_provider | — |
| `builtwith.technology_search` | no managed price — use an eligible BYOK connection | pre_authorize | paid_provider | — |
| `builtwith.trends` | free — not billed | no_bill | none | — |
<!-- END GENERATED -->
