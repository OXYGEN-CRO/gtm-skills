# Live tables: feeds (push and pull)

Use a feed whenever a table should keep filling itself instead of being loaded once. A **live table** is an ordinary workspace table with a bound **feed**. Feeds come in two transports and share everything downstream: one delivery ledger, one auto-run path, one pause control.

| Transport | Rows arrive because | Create it with |
| --- | --- | --- |
| **push** | an external app POSTs JSON at the feed's endpoint | `oxygen tables webhook create <table> ...`, or `oxygen feeds bind [table] --schema-json <schema>` to refuse rows that do not match a declared schema |
| **pull** | a cadence harvests the next page from a provider | `oxygen feeds bind <table> ...` |

Pick **push** when the source system can call you (product signups, form fills, a Zapier or n8n bridge, your own backend). Pick **pull** when the data lives at a provider you must ask. A live TAM or a live signal list starts from its planner, which prices the source first and then binds it: the `oxygen-sourcing` skill (`references/companies.md`) for companies, the `oxygen-signals` skill (`references/signal-feeds.md`) for hiring, funding, tech, news and LinkedIn posts. This page is the mechanics underneath.

`oxygen feeds list|get|pause|resume|deliveries|unbind` operate on **both** transports. `oxygen feeds bind` binds a pull feed, or — with `--schema-json` — a push feed whose rows must match a declared schema; `oxygen tables webhook ...` stays the push-only alias for endpoints without a schema.

## Push: capture the JSON first, add fields later

For a new webhook table, start with one JSON column keyed **`payload`**. The receiver
stores each incoming JSON object there in full, including nested values. No field
schema is required. Add or extract columns after seeing real payloads.

```bash
oxygen tables create "Webhook table" --columns-json '[{"key":"payload","label":"Webhook payload","dataType":"jsonb","kind":"source","definition":{"webhook_payload":true}}]' --json
oxygen tables webhook create <table> --name "Webhook" --auth-mode secret --json
```

Copy `webhookUrl` and the one-time `secret` from creation. Send JSON with
`Content-Type: application/json` and `x-oxygen-table-webhook-secret: <secret>`.
These calls enable receipt only; no paid columns run automatically. In the web app,
**New table → Webhook** creates this payload table and opens the endpoint configuration
on the right. The URL and shared-secret controls remain available under **Webhook settings**.

**Volume.** An endpoint accepts a number of deliveries a minute that grows with the plan size, and one sender IP may use all of it. The `rate_limit` field of every `tables webhook` response gives the endpoint's number, and `oxygen limits show --json` lists every size's number under `plan_bands[].webhooks`. A delivery over the limit gets HTTP 429 with `Retry-After`. Nothing is written for it, so the sender redelivers. To send more rows than that, batch several rows into one delivery with `--items-path` (a delivery may carry an array of rows, up to 1 MB of JSON, and counts once) or move to a larger plan. A refused delivery is not recorded in `tables webhook deliveries`. Compare the sender's peak rate with the endpoint's before you promise a customer a volume.

## Push: inbound JSON into a table, with auto-run

1. Create or inspect the target table and the downstream columns first.

```bash
oxygen tables describe <table> --json
oxygen columns add <table> --key <score_column> --label "Qualification Score" \
  --prompt "Score this inbound lead 0-100 against our ICP using {{company_name}} and {{domain}}. Return score and one-sentence reason." --json
oxygen columns add <table> --kind tool --key <sync_column> --label "CRM Sync" \
  --definition-json '{"version":1,"mode":"native","toolId":"<tool-id from `oxygen tools search`>","inputMapping":{"domain":{"type":"column","columnKey":"domain"}}}' --json
```

2. Create the push feed with auto-run columns. Table webhooks are public by default so most providers can POST directly to the URL. Once auto-run columns are configured, every written row queues those columns automatically.

```bash
oxygen tables webhook create <table> --name "Inbound events" --mode upsert --upsert-key event_id --event-id-path event_id --event-type-path type --occurred-at-path occurred_at --auto-run-columns <score_column>,<sync_column> --auto-run-max-credits 50 --auto-run-max-concurrency 5 --json
```

If the source provider can send an Oxygen secret header and the user wants a signed endpoint, opt in explicitly:

```bash
oxygen tables webhook create <table> --name "Signed inbound events" --auth-mode secret --mode upsert --upsert-key event_id --event-id-path event_id --event-type-path type --occurred-at-path occurred_at --json
```

3. Send a smoke payload from the source system, then inspect the delivery.

```bash
oxygen feeds deliveries --table <table> --limit 5 --json
oxygen table-runs get <action_run_id> --json
oxygen tables preview <table> --limit 5 --include-system-fields --json
```

4. Update the auto-run column set when the table flow changes.

```bash
oxygen tables webhook update <endpoint_id> --auto-run-columns <new_column_keys> --json
oxygen tables webhook get <endpoint_id> --json
```

## Push: product signups

Your application emits signup events; the table owns storage, deduplication, enrichment and downstream runs.

1. Keep stable `event_id`, `event_type`, `occurred_at`, email, name and company fields plus a JSON `payload` column for the source evidence, then create the endpoint: `oxygen tables webhook create <table> --name "Signup events" --mode upsert --upsert-key event_id --event-id-path event_id --event-type-path type --occurred-at-path occurred_at --json`.
2. Store the URL and the one-time secret in the application's secret manager, never in chat, wiki pages or exported rows. Reuse each event's stable id on retries.
3. Deliver one test event and read it back with `oxygen tables webhook deliveries <endpoint_id> --json` and `tables describe`.
4. Add enrichment, scoring or CRM-sync columns only as needed, preview a small scope, and get approval for the exact auto-run columns, the per-delivery ceiling and the recurring posture before arming auto-run.
5. Backfill through the same emitter in bounded batches with the original event ids, reading delivery status, row counts and run effects after each batch. An accepted delivery is not proof that every enrichment or CRM write completed.

Promote a person to Records only at the chosen signup or qualification gate (the `oxygen-crm` skill); outreach is a Sequence with its own approval.

## Push with a declared row schema (typed or rejected)

Use this when the sender is outside your control and a malformed row must never land half-written — the answer to "can I create a custom signal?": signals are typed or rejected, so an outside event stream comes in as a push feed with a schema.

```bash
cat > signup.schema.json <<'JSON'
{"type":"object","properties":{"email":{"type":"string"},"plan":{"enum":["free","starter","pro"]},"seats":{"type":["integer","null"]}},"required":["email","plan"],"additionalProperties":false}
JSON
oxygen feeds bind --create "Product signups" --schema-json signup.schema.json --upsert-key email --json   # new table, columns derived from the schema
oxygen feeds bind <table> --schema-json signup.schema.json --items-path '$.rows' --json                   # existing table; every property must match a column
```

- The response carries `webhookUrl` and the `secret` (shown once; send it as `x-oxygen-table-webhook-secret`). Binding is free and inbound rows cost nothing.
- Allowed keywords: `type`, `properties`, `required`, `additionalProperties`, `items`, `enum`, `const`, `anyOf`. `format`, `pattern`, min/max and `oneOf`/`allOf`/`$ref` are refused at bind time with the exact paths, because ingest could not enforce them.
- A delivery with any non-matching row answers **422** with `error.details.issues` (path + message) and appears in `oxygen feeds deliveries --status rejected`; nothing is written. Fix the payload and resend — the same event id still lands.
- Add auto-run columns afterwards with `oxygen tables webhook update <endpoint_id> --auto-run-columns <keys> --auto-run-max-credits <n>`. To change the schema, bind a new feed (new endpoint) and `oxygen feeds unbind` the old one.

## Pull: a provider harvest on a cadence

A pull feed replays one frozen provider request every cycle, advancing a cursor or a date window so it asks only for what is new. It writes a delivery row exactly like an inbound POST does, so everything below the ingest point is identical.

1. Bind the feed. Everything about *what* to ask the provider is frozen at bind time from `--tool-id` plus `--request-json`; everything about *how often and how much* is the `--every` / `--max-credits` pair. A paid cadence requires `--approved` — that flag is the founder agreeing to recurring spend, not to one call.

```bash
oxygen feeds bind <table> --kind company_search --tool-id <tool_id> --request-json ./request.json --rows-path <rows_path> --row-mapping-json ./mapping.json --upsert-key domain --every daily@9 --max-credits <n> --max-rows 500 --approved --json
```

Cadence vocabulary is the shared one: `hourly`, `every_6h`, `daily@<hour>`, `weekly@<day><hour>` (hours are 0–23 UTC).

2. Price the next cycle before it fires. `--mode dry_run` is free and renders the exact request the next cycle will send, with the cursor or date window already injected.

```bash
oxygen feeds run <feed> --mode dry_run --json
```

3. Run one cycle now, if the user wants proof before the first cron tick.

```bash
oxygen feeds run <feed> --mode live --approved --max-credits <n> --json
```

4. Watch it fill.

```bash
oxygen feeds get <feed> --include-cursor --json
oxygen feeds deliveries --table <table> --limit 5 --json
oxygen tables preview <table> --limit 5 --include-system-fields --json
```

## Both transports: pause, resume, retire

```bash
oxygen feeds list --table <table> --json
oxygen feeds pause <feed> --json
oxygen feeds resume <feed> --json
oxygen feeds unbind <feed> --json
```

Pause is the single revocation. A paused push feed rejects the POST with `table_webhook_disabled` instead of silently accepting and dropping it — tell the source system, because those deliveries are refused, not queued, and leave no ledger row to recover from. A paused pull feed's cron still fires but the cycle refuses before it claims anything, so it spends nothing. Resume also clears a stopped machine state: a feed that exhausted itself on empty cycles or errored on a budget refusal is deliberately unclaimable until someone says continue.

To disable automation on a push feed without giving up the endpoint URL, clear the auto-run config instead of pausing:

```bash
oxygen tables webhook update <endpoint_id> --clear-auto-run --json
```

## Rules

- Keep the emitting app or provider as a source only; GTM logic belongs in table columns.
- A bound feed is a standing permission to **receive rows**, never a standing permission to **spend**. Auto-run columns spend under the auto-run config's `--auto-run-max-credits`; a pull cycle spends under the feed's `--max-credits`. Set both explicitly rather than relying on a default ceiling.
- Do not ask for per-delivery approval. Do ask again when the user changes the cadence or raises the per-cycle ceiling — both enlarge the standing grant, and the API will refuse without `--approved`.
- Not every provider tool can be armed. A tool that publishes no resumption point (a cursor, a row timestamp to watermark on, or a recency filter) is one-shot only, because every cycle would re-read and re-bill the same window. `oxygen feeds bind --every ...` refuses those with `feed_not_incremental`; run them once instead and re-run when the user asks.
- Default to public push endpoints. Use `--auth-mode secret` only when the source can send `Authorization` or `x-oxygen-*-secret` headers. Pull feeds have no inbound URL at all.
- Always dry-run a pull feed before arming it, and read the rendered request back to the user — it is the only place the frozen provider query is visible in full.
- Use hosted workflows instead when the flow needs branching, multi-table orchestration, or manual approval steps. A feed supplies rows; it does not orchestrate.
- Inspect `oxygen feeds deliveries` and `oxygen tables preview` row provenance before assuming enrichment or sync columns ran.
- `oxygen feeds unbind` deletes the binding and, for a push feed, its endpoint URL. Pause first when the user only wants it to stop.
