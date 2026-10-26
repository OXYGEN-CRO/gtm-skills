# Tool, HTTP and sync columns

A tool column runs one provider operation per row. Prefer a column for repeated row work and `oxygen tools run` only for one-off checks and descriptor probes. Contact and company data have maintained presets and waterfalls (the `oxygen-enrichment` skill); reach for a hand-built tool column when no preset fits.

## Add and run a tool column

Inspect the descriptor before writing the mapping:

```bash
oxygen tools get blitzapi.person_enrich --json
oxygen columns add leads --label "Person Enrichment" --kind tool \
  --definition-json '{"toolId":"blitzapi.person_enrich","inputMapping":{"person_linkedin_url":{"type":"column","columnKey":"linkedin_url"}}}' --json
oxygen columns run leads person_enrichment --limit 1 --dry-run --json
```

`--kind tool` stores the whole provider answer in a jsonb cell; pass `--data-type text` only together with an `outputPath` that lifts one scalar out. Copy fields into ordinary columns for free with `oxygen columns materialize <table> <column> --mappings-json '[{"source_path":"response.raw.organic.0.link","target_column":"top_link"}]'`; it makes no provider call. Use `--connection-id <id>` when the tool needs one of several workspace connections.

## Bounded runs

```bash
oxygen columns run leads person_enrichment --background --limit 500 --approved --max-credits <n> --json
oxygen table-runs wait <run_id> --json
oxygen table-runs items <run_id> --status failed --json
```

- `--limit N` selects the next N rows whose cell is still empty; `--force` re-runs filled cells. Repeat capped runs until the run reports `row_count: 0` instead of one all-rows run.
- `oxygen table-runs create <table> --column <key> --limit <n> --approved --max-credits <n>` queues a durable run over the newest n rows (`columns run --limit` takes the next empty cells instead); `table-runs wait` blocks until it settles, so no shell loop is needed.
- After a run, read failures and spend before widening scope: `table-runs items <run_id> --status completed --limit 5`, `oxygen billing usage --limit 20 --json`. A row can bill 0 when the same lookup ran recently and was reused.
- Stuck, failed or surprising runs: the `oxygen-diagnostics` skill.

## One-off tool calls

```bash
oxygen tools get blitzapi.email_to_person --json
oxygen tools run blitzapi.email_to_person --input-json '{"email":"founder@example.com"}' --mode dry_run --json
oxygen tools run hubspot.contacts_create --input-json '{"properties":{"email":"a@example.com"}}' --mode dry_run --connection-id <conn_id> --json
```

A dry run validates and prices the request without a provider call. A live write tool needs the user's approval of the exact scope and runs with `--mode live --approved --max-credits <n>`.

## HTTP API columns and custom integrations

Two native ways to call your own REST endpoint per row; both run on OXYGEN in the background with billing and provenance:

**A. Custom integration (reusable, credential stored in OXYGEN).** Write a `version: 1` manifest with `slug`, `name`, `description`, `baseUrl`, an `auth` block (`{"type":"none"}`, `bearer`, `{"type":"api_key_header","header":"X-API-Key"}`, `{"type":"api_key_query","param":"key"}` or `{"type":"basic","username":"..."}`) and `operations[]`, each with `operation`, `displayName`, `method`, `path`, `effect` (`read` or `write`), `sideEffectClass` and typed `fields[]`. Each operation becomes the tool `custom_http.<slug>.<operation>`:

```bash
oxygen custom-integrations apply --manifest ./integration.json --json
oxygen custom-integrations connect <slug> --secrets-file ./secret.env --json
oxygen tools get custom_http.<slug>.<operation> --json
oxygen columns add <table> --kind tool --definition-json '{"toolId":"custom_http.<slug>.<operation>","inputMapping":{"domain":{"type":"column","columnKey":"domain"}}}' --json
```

**B. Inline HTTP column (one endpoint, one column).** A `--kind tool` column whose definition uses `mode: "custom_http"` with a `request` block (`method`, `url`, optional `headers`, `body`, and `secrets` named by reference).

- `{{<column>}}` and `{{secrets.<NAME>}}` template the request. A `{"env": "NAME"}` secret resolves on the server from the workspace's registered custom integration `NAME`; an unregistered reference fails the row with `custom_http_secret_unavailable` instead of sending a blank credential. `columns run --local` runs the column in the CLI process and reads your own machine's env var, so the key never leaves it.
- `columns run --dry-run` previews one row's request with secrets masked. Redirects and private hosts are blocked, the response size is capped and secret values are redacted from stored output. OXYGEN charges 0 credits for the call.
- **A `GET` is a read; any other method is an external write and needs `--approved`.**

## External sync columns

Write to a CRM or outbound tool only from the table, and mirror every live write back to the row:

```bash
oxygen columns add contacts --label "HubSpot Contact ID" --key hubspot_contact_id --data-type text --json
oxygen columns add contacts --label "HubSpot Sync Status" --key hubspot_sync_status --data-type text --json
oxygen columns add contacts --label "HubSpot Sync Error" --key hubspot_sync_error --data-type text --json
oxygen columns add contacts --label "HubSpot Synced At" --key hubspot_synced_at --data-type timestamptz --json
```

Provider ids, status, errors and timestamps stay in OXYGEN rows or runs, never only in stdout, a CSV or the provider's UI; batch status changes with `oxygen tables upsert`. Do not re-run successful rows without an idempotency key or a provider-id check. Approval for a sync names the rows and filter, the provider and account, the exact write, duplicate handling, estimated cost and the retry plan. CRM-specific sync (bidirectional HubSpot and Attio, imports, do-not-contact): the `oxygen-crm` skill; pushing rows into a Smartlead, Instantly, lemlist or HeyReach campaign: `oxygen-sequencer`.
