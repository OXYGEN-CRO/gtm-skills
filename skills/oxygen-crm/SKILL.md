---
name: oxygen-crm
description: "Operate OXYGEN Records, the native CRM: objects, fields, identities and relationships, notes, tasks and files, imports from HubSpot, Attio and Pipedrive, list imports with do-not-contact first, bidirectional sync, and binding and promoting table rows onto records."
allowed-tools: Bash(oxygen *)
---

# OXYGEN CRM (Records)

Records hold canonical truth: companies, people, deals and any object the workspace adds (partners, renewals, projects), with identities, relationships, activities, notes, tasks and files. Tables hold disposable work (`oxygen-tables`); a row becomes a record only at a deliberate gate, by binding and promoting it.

## Pick the path

| Need | Start with | Read |
| --- | --- | --- |
| See or shape the model: objects, fields, identities, relationships | `oxygen crm objects --projection compact --json`, `oxygen crm describe <object> --json` | [data model](references/data-model.md) |
| Count or list stored records | `oxygen crm objects --projection compact --json`, then `oxygen tables preview <backing-table> --fields <field-key> --summary-only --json` for an exact total, or omit `--summary-only` for rows | [data model](references/data-model.md) |
| Empty CRM enrichment fields, or Open Deal / Account Stage meaning and repair | `oxygen crm enrichment list --object <object> --json`; `oxygen crm rollup --dry-run --json` | [data model](references/data-model.md) |
| Notes, tasks and files on a record; every open task | `crm notes add`, `crm tasks add`, `crm files attach`; `oxygen crm tasks list --json` | [data model](references/data-model.md) |
| Find a record from a fragment, or open it | `oxygen crm search "<fragment>" --suggest --json`, `crm get <object> <record_id>` | [bind and promote](references/promote.md) |
| One HubSpot list or Pipedrive filter as a working table, do-not-contact first | `tables hubspot import`, `tables pipedrive import` | [import](references/import.md) |
| A whole CRM object into Records | `crm sync import <provider> --object <object>` | [import](references/import.md) |
| HubSpot or Attio and Records converged on a schedule | `crm sync configure`, `crm sync run --dry-run` for prices, then `crm sync enable` | [sync](references/sync.md) |
| Table rows as native contacts | a bind column, then `tables promote` | [bind and promote](references/promote.md) |
| Who to contact first today | `oxygen signals leads-today --json` (the `oxygen-signals` skill) | — |

Provider specifics: [HubSpot](provider-runbooks/hubspot.md) (lists, do-not-contact subjects, list-to-Sequence), [Attio](provider-runbooks/attio.md). Salesforce has no integration.

## Gates

- **Check the connection first.** `oxygen integrations list --json`; a `needs_reconnect` or `health.status: error` connection stops the work and goes to Connections. Never route around it through another tool.
- **Preview, then approve.** Every import, sync, object change and promotion previews or dry-runs first; the live call needs `--approved` (object and field changes take `--live`). Review the current quote and an explicit `--max-credits` spend ceiling before going live.
- **Stored records and external CRM calls have different costs.** Native OXYGEN record reads cost 0 credits. Calls using your own CRM API key cost 0.05 credits each after repricing takes effect, including read, discovery and pagination calls. OAuth calls follow their current tool quote. Live Workflow steps cost 0.05 credits each after repricing takes effect and count toward the spend ceiling then; provider billing and API quota are separate. Read the current unit-price quote: the complete run estimate is unknown (null), independent of the explicit spend ceiling. A stored manifest quote is a captured snapshot; refresh the preview for current prices and cap coverage.
- **Do-not-contact syncs first.** A list or filter import syncs its do-not-contact list before any row lands, and no row lands unless that sync succeeds. Suppression is additive; skipping it needs an explicit `--no-dnc`, which changes the preview fingerprint. Un-suppress a whole person by subject (`suppressions remove --subject-id <id>`), never by one identifier.
- **Imports are last-write-wins** on the fields the CRM supplies. Edits made in the CRM do not flow in by themselves: re-run the import, or use the bidirectional sync.
- **Bound both rows and credits.** `--max-rows` limits sync volume; `--max-credits` limits OXYGEN spend. Neither replaces the other or the CRM's API quota. A broken connection switches the cron off; deletes are never synced.
- **Write shapes fail quietly when guessed.** Unknown column keys are rejected, a dropdown carries its options at create, and an object without an identity duplicates on every re-import. Read the data model before creating an object or a field.
- **Bound record reads.** MCP record reads default to compact data and name any `omitted_row_fields`; inspect those values through `oxygen_table_row_inspect` using the returned `detail` reference. CLI: `oxygen crm get <object> <record> --projection compact --max-chars 10000 --json`. Select an existing column key from the object description for Table previews (Companies: `name`; People: `full_name`). Table totals include samples. `_sample` is metadata, not a selectable Table column; request existing fields and inspect the returned marker rather than selecting `_sample`.
- **Samples are not the workspace's records.** A new workspace starts with sample companies, CEOs and deals: reads mark them `_sample: true` (`sample: true` on `crm pipeline` deals and suggestions) and pipeline, funnel and chart totals leave them out. Only seeded records carry the true marker; an absent marker on a native CRM record read means it is not a seeded sample. Never count, work or recommend them. Only the user decides one is real: `oxygen crm keep <object> <record>` (MCP `oxygen_crm_record_keep`).
- **Binding and promoting are truth writes.** `--bind-create` and `tables promote` preview free, then need `--approved`; identity fields are never overwritten from a table.
- **Hosted runs only.** An import runs as a durable hosted Workflow run. On an executor mismatch, fail closed with the run link and error; do not tell the customer to change an environment variable or move execution local.

Return the record, run and table links with every change.

Plays: [website-visitor-outreach](plays/website-visitor-outreach.md).
