# Prospeo Runbook

> **Runs only on the workspace's own Prospeo key**, and is in no default chain. Connect it with
> `oxygen integrations connect prospeo --api-key <key>`, then select it with `--provider-order` on an
> enrichment column. A call on your key spends your Prospeo credits plus OXYGEN's per-call BYOK platform fee when it applies.

Use Prospeo for person enrichment when a row has a trusted LinkedIn profile or full name plus company identity and the workflow needs verified work email or direct mobile coverage.

## Best Fits

- `prospeo.enrich_person` for verified work email on a known person.
- `prospeo.enrich_person` with mobile enabled for approved phone enrichment.
- Prospeo after lower-cost first passes when direct mobile coverage matters for a qualified row.

## Operating Pattern

1. Inspect the descriptor.

```bash
oxygen tools search prospeo --json
oxygen tools get prospeo.enrich_person --json
```

2. Use the native email or phone waterfall column instead of direct batch tool runs when enriching a table.

```bash
oxygen enrich-column preview <contacts_table> --capability mobile_phone --source-column linkedin_url --provider-order prospeo --json
```

3. Run one row, inspect raw provider payload, normalized output, provider source, and credits before approving a wider batch.

## Cost And Safety

- Mobile enrichment is materially more expensive than work-email lookup.
- Treat `NO_MATCH` and invalid datapoint responses as no-result, not as fatal workflow errors.
- Do not use personal contact enrichment as a first-pass step for unqualified rows.

## Fallbacks

- Work email: Blitz API, LeadMagic, Hunter, ContactOut, BetterContact, AI Ark, or the native email waterfall.
- Phone: LeadMagic, ContactOut, BetterContact, AI Ark, Apollo, or the native phone waterfall; Findymail and Crustdata only on the workspace's own key.
- Verification: pair final phones with ClearoutPhone when the workflow needs validity evidence.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `prospeo.account_information` | free — not billed | no_bill | none | BYOK — runs on the org's connected `prospeo` API key; provider-side charges may apply |
| `prospeo.bulk_enrich_company` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `prospeo` API key; provider-side charges may apply |
| `prospeo.bulk_enrich_person` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `prospeo` API key; provider-side charges may apply |
| `prospeo.enrich_company` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `prospeo` API key; provider-side charges may apply |
| `prospeo.enrich_person` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `prospeo` API key; provider-side charges may apply |
| `prospeo.search_company` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `prospeo` API key; provider-side charges may apply |
| `prospeo.search_person` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `prospeo` API key; provider-side charges may apply |
| `prospeo.search_suggestions` | free — not billed | no_bill | none | BYOK — runs on the org's connected `prospeo` API key; provider-side charges may apply |
<!-- END GENERATED -->
