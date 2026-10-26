# Apollo Runbook

Use Apollo for reviewed people or account enrichment when the table already has strong identity, such as an email, Apollo id, LinkedIn URL, full name, and company domain.

Apollo company and people searches are BYOK only. Use Blitz for managed company and people search; Apollo enrichment and CRM tools retain their existing credential modes.

## Credential And Plan

- **Search is BYOK only.** Company and people searches require your own Apollo key. Enrichment and CRM operations support Oxygen’s managed Apollo account. BYOK is supported: connect an Apollo key and select `credential_mode: user_api_key` to run on your own account and your own Apollo credits.
- **Enrichment can spend Apollo lead credits.** Enrichment, organization details and news searches use `pre_authorize`. Company and people searches require BYOK. Oxygen applies its usual BYOK platform fee, and Apollo may charge the connected account. Preview searches first, then enrich only the rows you kept. CRM read operations remain `no_bill`.
- **Advanced filters are plan-gated.** Apollo refuses filters its plan does not include (funding, technology, job-posting ranges) with an entitlement error, not a validation error: Oxygen returns `provider_plan_limit` naming the exact refused filters and the plan. Drop those filters and re-run, or route that query to another provider (Blitz API, or Crustdata or SignalBase on the workspace's own key) — re-tuning the query will not help.
- **A refused Apollo call is a failure, not an empty result.** Apollo answers some bulk endpoints with HTTP 200 carrying `status` / `error_code` / `error_message`; Oxygen surfaces that as a failed run rather than writing it into the cell. An unmatched row inside a successful response (`missing_records`) is a genuine no-match.

## Best Fits

- `apollo.people_search`: explicit BYOK people search using the workspace’s own Apollo key. Use Blitz for managed search.
- `apollo.people_enrich`: enrich a known person and optionally request phone waterfall or phone reveal.
- `apollo.people_bulk_enrich`: enrich a small reviewed batch when row identity is stable.
- `apollo.organization_enrich`: fill account fields from trusted organization identity.

## Operating Pattern

1. Discover exact descriptors before building a column.

```bash
oxygen tools search apollo --json
oxygen tools get apollo.people_enrich --json
```

2. For phone enrichment, preview the table column first instead of running the direct tool across many rows.

```bash
oxygen enrich-column preview <contacts_table> --capability mobile_phone --source-column linkedin_url --provider-order apollo --json
```

3. Use a one-row live pilot only after the user approves row scope and max credits.

## Cost And Safety

- Apollo people enrichment is a paid provider action when it enriches a record or requests contact-channel reveal.
- A person costs several times more when the request reveals a phone (`reveal_phone_number`, `run_waterfall_phone`), reveals personal emails (`reveal_personal_emails`) or runs the email waterfall (`run_waterfall_email`); `oxygen tools get apollo.people_enrich --json` quotes both prices. Leave those flags off when the work email is enough, and use them only for qualified contacts.
- `apollo.people_bulk_enrich` is priced per person in `details`.
- Use the native phone column for phones rather than Apollo's webhook-based asynchronous phone paths.

## Fallbacks

- For phone lookup, prefer the native Oxygen phone waterfall unless the user specifically wants Apollo-only coverage.
- For account discovery, compare Apollo with LeadMagic based on the fields needed, and with Crustdata or SignalBase only where the workspace has connected its own key.
- For work email, use the email waterfall recipe instead of forcing Apollo into every row.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `apollo.account_bulk_create` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.account_bulk_update` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.account_create` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.account_get` | free — not billed | no_bill | none | — |
| `apollo.account_search` | free — not billed | no_bill | none | — |
| `apollo.account_stages_list` | free — not billed | no_bill | none | — |
| `apollo.account_update` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.account_update_owners` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.analytics_report` | free — not billed | no_bill | none | — |
| `apollo.api_usage_stats` | free — not billed | no_bill | none | — |
| `apollo.call_create` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.call_search` | free — not billed | no_bill | none | — |
| `apollo.call_update` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.contact_bulk_create` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.contact_bulk_update` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.contact_create` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.contact_deals_list` | free — not billed | no_bill | none | — |
| `apollo.contact_get` | free — not billed | no_bill | none | — |
| `apollo.contact_search` | free — not billed | no_bill | none | — |
| `apollo.contact_stages_list` | free — not billed | no_bill | none | — |
| `apollo.contact_update` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.contact_update_owners` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.contact_update_stages` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.deal_create` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.deal_get` | free — not billed | no_bill | none | — |
| `apollo.deal_search` | free — not billed | no_bill | none | — |
| `apollo.deal_stages_list` | free — not billed | no_bill | none | — |
| `apollo.deal_update` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.email_accounts_list` | free — not billed | no_bill | none | — |
| `apollo.email_message_activities` | free — not billed | no_bill | none | — |
| `apollo.email_messages_search` | free — not billed | no_bill | none | — |
| `apollo.field_create` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.fields_list` | free — not billed | no_bill | none | — |
| `apollo.labels_list` | free — not billed | no_bill | none | — |
| `apollo.news_articles_search` | 12.5 cr (example payload; estimate 2–20 cr) | pre_authorize | paid_provider | — |
| `apollo.notes_list` | free — not billed | no_bill | none | — |
| `apollo.organization_bulk_enrich` | 12.5 cr (example payload; estimate 2–20 cr) | pre_authorize | paid_provider | — |
| `apollo.organization_enrich` | 12.5 cr (example payload; estimate 2–20 cr) | pre_authorize | paid_provider | — |
| `apollo.organization_get` | 12.5 cr (example payload; estimate 2–20 cr) | pre_authorize | paid_provider | — |
| `apollo.organization_job_postings` | 12.5 cr (example payload; estimate 2–20 cr) | pre_authorize | paid_provider | — |
| `apollo.organization_search` | free — not billed | no_bill | paid_provider | BYOK — runs on the org's connected `apollo` API key; provider-side charges may apply |
| `apollo.people_bulk_enrich` | 12.5 cr (example payload; estimate 12.5–1000 cr) | pre_authorize | paid_provider | — |
| `apollo.people_enrich` | 12.5 cr (example payload; estimate 12.5–100 cr) | pre_authorize | paid_provider | — |
| `apollo.people_search` | free — not billed | no_bill | none | BYOK — runs on the org's connected `apollo` API key; provider-side charges may apply |
| `apollo.sequence_abort` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits) |
| `apollo.sequence_add_contacts` | free — not billed | no_bill | campaign_enroll | external write — live gate (approved + max_credits) |
| `apollo.sequence_approve` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits) |
| `apollo.sequence_archive` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits) |
| `apollo.sequence_search` | free — not billed | no_bill | none | — |
| `apollo.sequence_update_contact_status` | free — not billed | no_bill | campaign_enroll | external write — live gate (approved + max_credits) |
| `apollo.task_bulk_create` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.task_create` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits) |
| `apollo.task_search` | free — not billed | no_bill | none | — |
| `apollo.typed_custom_fields_list` | free — not billed | no_bill | none | — |
| `apollo.users_search` | free — not billed | no_bill | none | — |
<!-- END GENERATED -->
