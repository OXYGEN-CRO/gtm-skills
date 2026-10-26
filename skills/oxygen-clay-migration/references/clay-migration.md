# Clay migration walkthrough

Move the accessible Clay workspace into native Oxygen objects. Use the hosted connection for source configuration and data, and the existing native tools to reconstruct behavior. Coverage depends on what Clay actually exposes; an inventory or successful transfer alone never establishes complete migration.

## Browser connection and inventory

```bash
oxygen clay migration --action connect --json
oxygen clay migration --action status --migration-id <migration-id> --json
oxygen clay migration --action discover --migration-id <migration-id> --source-workspace-id <workspace-id> --json
oxygen clay migration --action read --migration-id <migration-id> --resource-type table --resource-id <source-id> --json
oxygen clay migration --action read --migration-id <migration-id> --resource-type table --resource-id <source-id> --section row --row-id <source-row-id> --json
oxygen clay migration --action report --migration-id <migration-id> --json
```

In browser chat call `oxygen_clay_migration` with the same action and snake_case arguments. Present the connect response’s verification link/code; after user approval check status, verify the source identity and select the workspace. Follow discovery cursors and record incomplete exports or unsupported resource types. Read configuration and bounded samples, then create the destination typed columns plus `clay_source_cells` (JSON) and `clay_source_row_id` (text). Call `transfer` with `resource_type: table` or `audience`, the source `resource_id`, `target_table`, and `mapping: [{source_column_id, target_column}]` for bulk data; Audience mappings use field keys, and `global-people`, `global-companies` or `global-deals` select the whole discovered store. The background worker follows all transfer pages; read `report` for progress and retry a failed transfer with the same mapping. These preservation columns must already exist, and the target must have no auto-run enabled. Never send all rows through chat. For large configuration, drill into the returned dotted path or JSON pointer with `path`; continue long prompts with `text_offset` from `next_text_offset` until the scalar is complete.

`section: rows` lists bounded rows; `section: row` with `row_id` reads one source row's details, including exposed structured `cells.<column-id>.fields`, displayed `value`, status and error wrappers. A row-detail read takes no `limit` or `cursor`; use `path` and `text_offset` to inspect large fields. Keep displayed values and structured payloads distinct. Missing or inaccessible payloads remain explicit gaps; a successful detail sample does not establish complete rich-cell export or formula parity.

Audience discovery registers default `global-people`, `global-companies`, `global-deals` and separate `global-archived-people`, `global-archived-companies`, `global-archived-deals` resources. Each saved people/company Audience also gets an `archived:<original-id>` membership resource; its metadata, field-schema and record-ID reads resolve the original Audience without replaying its filter. Transfer each scope into its own new target; the discovered identity pins its scope. Direct `read` with `section: record_ids` accepts `archived: true` (CLI `--archived`); other reads and `transfer` refuse that flag. Resource IDs refuse entity or archive selectors that conflict with their saved scope. Follow all identity cursors and reconcile each scope separately; compare the combined union by entity and source record ID rather than adding overlapping counts. Registering scopes proves neither access nor membership extraction, and draft inclusion remains unproven.

Keep the migration ID in the conversation and persist each resource mapping with `checkpoint` using `resource_type`, `resource_id`, `disposition`, optional `target_kind`/`target_id`, and bounded `notes` for accepted replacements, verification and unresolved items. Use dispositions `copied`, `rebuilt`, `needs_decision`, `unsupported`, `inaccessible`, `excluded` or `failed` according to the evidence. On resumption read `report` before creating more objects. Establish all table identities before linking tables; migrate Audience identities through Records using the oxygen-crm skill. Read source functions, Claygents and standalone workflows and recreate their supported behavior through native Functions and draft hosted Workflows. Preserve accessible configuration for anything unsupported. Schedules and feeds stay inactive. Temporary Clay access ends with `disconnect`.

## User-supplied CSV fallback

Only use the following fallback when the user supplies or chooses a file export. CSV carries resolved cell values, not the logic that produced them; explain that this cannot establish whole-workspace migration.

## 1. Export from Clay

Ask the user to export the Clay table as CSV (in Clay: open the table, Export, Download CSV). It contains the current value of every cell: names, companies, domains, the emails, phones and LinkedIn URLs a waterfall already found, and the text a Claygent column already wrote. It does not contain formula definitions, waterfall provider configs, Claygent prompts, HTTP-API column setups, run history, the credit ledger or column settings; those are rebuilt in steps 3 to 6. Clay Enterprise may also offer API access to the rows; never assume it, the CSV is the universal path.

Keep the identity columns you will re-enrich against (`full_name`, `company`, `domain`, `linkedin_url`, any known `email`). Keep the Clay-derived columns you intend to regenerate as `<column>_clay_original` if the user wants a parity check (step 7).

## 2. Import

```bash
oxygen tables import --create "Clay Migration - <table name>" --file ./clay-export.csv --background --json
oxygen tables describe <table> --json
oxygen tables query <table> --limit 3 --json
```

`--create` infers column types; in Claude Desktop call `oxygen_cli_file_import_prepare` on the local path first. **Verify the row count against the Clay export before rebuilding anything**; a short table is a partial import to fix, not to build on. Then add the free cleanups before paying to enrich duplicates or dead domains: the normalize templates and `--preset domain_check` ([import and cleanup](../../oxygen-tables/references/import-and-folders.md), [templates](../../oxygen-tables/references/templates.md)).

## 3. Rebuild waterfalls

Map each Clay enrichment to its OXYGEN waterfall and run the free preview first: it returns the lane order, `estimated_credits_per_row` and `recommended_max_credits`, the honest Clay-against-OXYGEN credit comparison, before a single credit is spent.

| Clay enrichment | OXYGEN equivalent | Free preview |
| --- | --- | --- |
| Find work email | work-email waterfall | `oxygen enrich-column preview <table> --capability work_email --json` |
| Find phone or mobile | phone waterfall | `oxygen enrich-column preview <table> --capability mobile_phone --json` |
| Find or enrich LinkedIn URL | LinkedIn URL waterfall | `oxygen enrich-column preview <table> --capability linkedin_url --json` |
| Enrich company | company enrichment | `oxygen companies enrich preview <table> --json` |

For each: show the preview, get approval, pilot one row with the preview's ceiling, inspect it, then run the bounded batch. Each waterfall's flags and QA rules are in the `oxygen-enrichment` skill (`references/email.md`, `phone.md`, `linkedin-url.md`, `company.md`). Provider order and credit logic do not import from Clay; OXYGEN's waterfalls are cost-ordered by default, and `--provider-order` is for a deliberate reason.

## 4. Rebuild Claygent columns

A Claygent research, scoring or classification column becomes an OXYGEN column ([AI and formula columns](../../oxygen-tables/references/ai-columns.md), [research columns](../../oxygen-tables/references/research-columns.md)):

- A question Clay answered with one of its company-research templates (founders, parent company, funding, cloud provider, is SaaS, offers demos, industry, NAICS, HQ, a LinkedIn, Crunchbase or Glassdoor page) maps to an OXYGEN template: `oxygen columns catalog --category company --search <word> --json`, then `columns add <table> --prompt-key <key> --input domain=<column>`.
- A web question becomes a research column (`--kind research`); reasoning over the row's own data becomes an AI column with `--prompt` (text or a file) and `--output-schema-json` when the answer has fields. `--label` is only the display name.
- OXYGEN prepends the workspace's pinned voice, brand and positioning pages to AI message columns, so company context is not re-pasted into every prompt the way a Claygent column needs.
- **Recover the original prompt when you can.** Recover it from the hosted configuration read first. A CSV never carries it, but the user can copy it from the Clay column. A recovered original goes into `--prompt` with Clay's placeholders changed to OXYGEN's `{{column_key}}` tokens and the note `# ported from recovered Clay prompt`; a prompt rebuilt from the column's name and output says `# approximated — original Claygent prompt not recovered`. A migrated prompt never claims more fidelity than it has.

```bash
oxygen columns run <table> <column_key> --limit 1 --dry-run --json
```

## 5. Rebuild HTTP-API columns

Clay's HTTP-API column has two OXYGEN equivalents, chosen by where the credential lives: a reusable custom integration (credential stored in OXYGEN, a `custom_http.<slug>.<operation>` tool) or an inline HTTP column. In the browser migration, use workspace-managed connections; leave missing credentials as a setup task rather than asking the user to run terminal commands. A non-GET call is an external write that needs `--approved`. Both, with the manifest shape: [tool and HTTP columns](../../oxygen-tables/references/tool-columns.md).

## 6. What does not map

- **Clay formulas**: rewrite each as a formula column; Clay's syntax does not import. Check it on real rows with `oxygen formulas validate <table> --expression '<expr>' --json`.
- **Clay webhooks**: recreate the inactive receiving configuration, then ask before repointing any external sender. Create the endpoint with `oxygen tables webhook create <table>` (optionally `--auto-run-columns`) and point the sender at the new URL and secret ([feeds](../../oxygen-tables/references/feeds.md)).
- **A Clay provider OXYGEN does not carry**: check with `oxygen tools search <provider> --json` before promising parity; route the intent through a waterfall that covers it, wire it as a custom integration, or, with the user's consent, request it through the `oxygen-feedback` skill.
- **Scheduled or auto-updating Clay tables**: a hosted Workflow on a cron or trigger over the same columns, or a feed that keeps the table filling (the `oxygen-workflow-authoring` skill).

## 7. Verify

- **Row counts match** the Clay export (`tables query` totals or `oxygen db query`).
- **Paid pilot, only with separate approval**: run one column with `--limit 1`, then `oxygen cells inspect <table> <row-id> <column> --json` and `oxygen table-runs get <run_id> --json` for the value and its provider and credit attribution.
- **The receipt matches**: `oxygen billing usage --limit 20 --json` against the pilot's expected cost, compared with what Clay charged.
- **Parity, when originals were kept**: `oxygen tables query <table> --fields <column_key>,<column_key>_clay_original --limit 500 --json`, then report a match rate per column type (exact for formulas, label agreement for classification, found-rate for emails, non-failure rate for free text) and inspect a handful of mismatched rows before concluding anything. Keep the `_clay_original` columns until the user agrees they can go.

For a workspace migration, reconcile every discovered source resource in the migration report, including unsupported behavior, inaccessible resources, extraction limits and unresolved decisions. Imported outputs are historical Clay data, not Oxygen execution receipts. Validate deterministic formulas on sample rows; do not claim AI/provider equivalence without an authorized pilot.

Register each migrated table as a deliverable: `oxygen session output --table <table> --label "Migrated from Clay" --json`.
