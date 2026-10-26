# ContactOut Runbook

> **The people planners use its free count route.** Its registered people search is available through
> the named tool; the Reachable people journey remains coming soon under D51. It is outside the default
> email, phone and LinkedIn URL chains. Select `--provider-order contactout` on an enrichment column
> when that explicit provider is needed.

Use ContactOut when the row has a person LinkedIn URL, email, or strong name plus company identity and the workflow needs work email, phone, or LinkedIn-profile repair.

## Best Fits

- `contactout.people_enrich` with work email included for known LinkedIn profiles.
- `contactout.people_enrich` with phone included for approved phone enrichment.
- `contactout.phone_status` as a free coverage probe before paying for a phone lookup.
- `contactout.email_verify` when ContactOut is already the selected email provider.
- `contactout.people_enrich` for personal email or phone only by explicit `--provider-order`: it is not in the `personal_email` or `mobile_phone` default chains (`oxygen enrichment catalog --intent find_personal_email` shows the default).

## Operating Pattern

1. Inspect the descriptor and access state.

```bash
oxygen tools search contactout --json
oxygen tools get contactout.people_enrich --json
```

2. Prefer column waterfalls for row-by-row phone or email work so provider preflight, credits, source, and run status stay visible.

```bash
oxygen enrich-column preview <contacts_table> --capability mobile_phone --source-column linkedin_url --provider-order contactout --json
```

3. For live runs, present row scope, selected include fields, estimated credits, and max credits before approval.

## Cost And Safety

- Enrichment waterfalls require usable contact data for a hit. Direct tools use their quoted operation billing; inspect the dry-run estimate before dispatch.
- Phone enrichment should be run only after qualification or a user-approved pilot.
- Provider sample responses must not be treated as real data; Oxygen extractors drop known sample envelopes.

## Fallbacks

- Phone: LeadMagic, BetterContact, Apollo, or the native phone waterfall; Findymail and Crustdata only on the workspace's own key.
- Work email: Blitz API, Prospeo, LeadMagic, Hunter, BetterContact, AI Ark, or the native email waterfall.
- Verification: use dedicated validators when outbound deliverability or phone validity changes the decision.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `contactout.api_usage_stats` | free — not billed | no_bill | none | — |
| `contactout.company_search` | 16.5 cr per result (example payload: 25 results = 412.5 cr) | pre_authorize | paid_provider | — |
| `contactout.contact_info_linkedin` | 16.5 cr | pre_authorize | paid_provider | — |
| `contactout.contact_info_linkedin_batch` | 16.5 cr | pre_authorize | paid_provider | — |
| `contactout.contact_info_linkedin_batch_create` | 16.5 cr | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `contactout.contact_info_linkedin_batch_get` | free — not billed | no_bill | none | async — returns a job handle; poll for completion |
| `contactout.decision_makers` | 16.5 cr per result (example payload: 25 results = 412.5 cr) | pre_authorize | paid_provider | — |
| `contactout.domain_enrich` | 16.5 cr | pre_authorize | paid_provider | — |
| `contactout.email_profile_enrich` | 16.5 cr | pre_authorize | paid_provider | — |
| `contactout.email_to_linkedin` | 16.5 cr | pre_authorize | paid_provider | — |
| `contactout.email_verify` | 16.5 cr | pre_authorize | paid_provider | — |
| `contactout.email_verify_batch_create` | 16.5 cr | pre_authorize | paid_provider | async — returns a job handle; poll for completion |
| `contactout.email_verify_batch_get` | free — not billed | no_bill | none | async — returns a job handle; poll for completion |
| `contactout.linkedin_profile_enrich` | 16.5 cr | pre_authorize | paid_provider | — |
| `contactout.people_count` | free — not billed | no_bill | none | — |
| `contactout.people_enrich` | 16.5 cr (example payload; estimate 0–20 cr) | pre_authorize | paid_provider | — |
| `contactout.people_search` | 16.5 cr per result (example payload: 25 results = 412.5 cr) | pre_authorize | paid_provider | — |
| `contactout.personal_email_status` | free — not billed | no_bill | none | — |
| `contactout.phone_status` | free — not billed | no_bill | none | — |
| `contactout.work_email_status` | free — not billed | no_bill | none | — |
<!-- END GENERATED -->
