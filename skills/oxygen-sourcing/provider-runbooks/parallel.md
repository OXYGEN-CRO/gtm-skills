# Parallel Runbook

**Own key only.** Parallel runs on the workspace's own key: a call bills that account plus OXYGEN's per-call BYOK platform fee when it applies, which the preview shows. It is available for explicit requests and is absent from the default managed search chain.

## When to use it

- `parallel.search` for objective-targeted research with excerpts and native include/exclude domain filters.
- `parallel.extract` for known-URL extraction with the workspace's own key.

## Execute and verify

Hydrate the selected operation with `oxygen tools get <tool_id> --json`, inspect its exact schema and credential requirements, then preview a bounded input. A live call can incur charges on the customer's Parallel account; obtain approval for that scope and inspect the returned result before using it in a Table.

For managed web grounding, inspect the AI research column's live route and quote. Use its eligible managed providers when the workspace has no Parallel key.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `parallel.extract` | no resolvable price — unknown until run | pre_authorize | paid_provider | — |
| `parallel.search` | 0.5 cr | pre_authorize | paid_provider | — |
<!-- END GENERATED -->
