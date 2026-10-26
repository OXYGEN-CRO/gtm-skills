# External campaigns: Smartlead, Instantly, lemlist, HeyReach

A campaign the customer already runs in Smartlead, Instantly, lemlist or HeyReach stays there; OXYGEN pushes reviewed rows into it and mirrors what happened. It is not a Sequence: cadence, reply-stop and sending belong to that platform. All four run on the workspace's own key: connect it with `oxygen integrations connect <provider> --api-key <key>`.

## Push rows into a campaign

```bash
oxygen sequences push-external --provider smartlead --campaign "<name or id>" --from-table <table> --json
oxygen sequences push-external --provider smartlead --campaign "<name or id>" --from-table <table> --mode live --approved --json
```

The first call is a dry run: it shows the field mapping, sample leads, row counts and any platform fee. Show it, get approval, then push for real. Scope rows with `--rows`, `--excluded-rows` or `--filter-json`; `--field-mapping-json` overrides the mapping. When the preview says `live_executable: false`, use the platform's own importer or a native Sequence (`sequences create --from-table <table> --enroll`). A jsonb email cell needs a scalar email column first (a free formula, the `oxygen-tables` skill).

A native Sequence can also bind its email track to an Instantly campaign (`--email-provider instantly`): emails handed to Instantly keep sending from Instantly, and a company pause reaching such a campaign warns `instantly_email_not_paused`.

## Direct platform operations

When `push-external` does not cover the job (stats, webhooks, lead lists, campaign setup), use the platform's tool operations:

```bash
oxygen tools search instantly --json
oxygen tools get <tool_id> --json
oxygen tools run <tool_id> --mode dry_run --input-json '{...}' --json
```

- Resolve destination ids (campaigns, lists, sender accounts) with reads before any mutation; never guess one.
- Keep qualification, copy and approval state in OXYGEN columns, push only a reviewed pilot segment first, and store the provider lead id, campaign id, sync status, error and timestamp on each row (a sync column, `oxygen-tables`). Failed rows must be retryable without re-enrolling successful ones.
- Approval names the connected account, the campaign or list, the row filter and count, the exact write, duplicate handling, the cost on the platform and the retry plan. A live operation runs with `--mode live --approved --max-credits <n>`.
- Prices are per operation and current: `oxygen tools get <tool_id> --json`.

## Instantly

- **Create the API key with all scopes** (`all:all`). A partially scoped key connects but fails single operations with `provider_scope_denied`; the connection shows `degraded` with reason `missing_scope` and stays usable for everything else. Recreate the key with all scopes in Instantly's API settings and reconnect, or run `oxygen integrations test instantly` after fixing the key in place.
- Write path for table rows: `instantly.list_campaign` to resolve ids, `instantly.list_leads` to check existing membership, `instantly.create_email_verification` and `instantly.check_verification_status` when email quality is unknown, `instantly.bulk_add_leads` with `campaign_id` or `list_id` (never both), then `instantly.get_campaign_sending_status` and analytics after a pilot batch.
- Background job ids (moves, warm-up, verification) are durable state to poll later.
- Webhooks: `instantly.list_webhook_event_types` first; `instantly.create_webhook` only when the receiving OXYGEN trigger already exists; `instantly.test_webhook` sends an external request and needs approval.

## Smartlead

Add a jsonb sync result column, run one row first, and run a bounded batch only after approval. Check that the final email and personalization columns are non-empty and that the row filter selects only approved leads.

## lemlist

Enrichment, database, sending and account operations can consume lemlist credits or trigger messages. Confirm email, LinkedIn URL and personalization fields before campaign writes, and settle duplicate handling and the unsubscribe strategy before a live import.

## HeyReach

- Prefer `heyreach.campaigns_add_leads_v2` and `heyreach.lists_add_leads_v2`: they return added, updated and failed counts. Batch at most 100 leads per request.
- `heyreach.campaigns_create` creates a draft; activate a campaign in HeyReach itself.
- `campaigns_update_sequence` replaces the whole sequence tree and `campaigns_update_accounts` the whole account set: use them only when that replacement is intended. Read the campaign and its sequence first.
- Read the inbox before any `heyreach.inbox_send_message`, and send only reviewed copy to a reviewed conversation.
- Organization operations need a HeyReach organization master key; user invites, workspace creation and API-key creation need explicit approval, and returned keys never go into chat or table cells.

## Stop

Stop when the destination, sender account or client workspace is unclear, the email is missing or unverified, the copy is generic or unsupported by evidence, the platform reports a sending problem, or live enrollment is not approved.
