# CRM data model: objects, fields, identities

The workspace is not limited to Companies, People and Deals. Anything it needs to track as records of its own — partners, projects, renewals, properties — is a CRM **object**, with its own fields and its own records, and it appears beside the standard three everywhere: the sidebar, `crm objects`, search, assert.

- **See the model:** `oxygen crm objects` lists every object with its field count and what makes two of its records the same. `oxygen crm describe <slug>` is one object in full; `--field <key>` narrows it to one field. In the app it is **Settings → CRM Data Model** (`/settings/data-model`).
- **Create one:** `/settings/data-model/new`, or `oxygen crm objects create --slug partners --display-name Partners --columns-json '[…]' --live`. Defaults to dry-run.
- **Add a field to one that exists — standard objects included:** `oxygen crm objects add-attr <object> --column-json '{…}' --live`, or **Add field** on the object's data-model page. A field you add belongs to the workspace and survives later `crm setup` runs.
- **Change a field:** `oxygen crm objects update-attr <object> <field-key> --name "Contract renewal" --live` renames it; `--required` / `--no-required` flips the flag; `--options-json '[{"value":"negotiation","label":"Negotiation"}, …]'` replaces a select/status field's whole choice list (keep an existing `value` to keep the records that hold it). In the app, click the field's row on the object's data-model page: it opens in the same column editor the Tables grid uses, where a field you added can also change its data type through the previewed retype flow. The field's **key never changes**, so prompts, formulas and integrations that read it keep working. Use `crm objects update-attr` to edit CRM field metadata directly. The shared Table column editor and `oxygen columns update <object-table> <field-key> --label "…"` also synchronize a bound CRM field's display name; read `crm describe` → `attributes[].displayName` to verify it.
- **Remove a field you added:** `oxygen crm objects remove-attr <object> <field-key> --live`, or **Remove field** in the same dialog. The column is archived (no value destroyed), the object stops listing it, and the key is free again at once — add a field with the same name and it just works. Changed your mind? `oxygen columns restore <object-table> <field-key>` brings the column back **as the same CRM field**. `columns archive` on the same column hides it from the grid but leaves the CRM still advertising the field — use `remove-attr`.
- **Read one field:** `oxygen crm describe <object> --field <field-key>` returns just that field (name, type, choices, flags, identity) instead of the whole object — the check to run after any of the above.
- **What Oxygen owns on a standard object:** a template field on Companies, People or Deals keeps its key, type and required flag (`cannot_edit_standard_attribute` on `--required`) and cannot be removed (`cannot_remove_standard_attribute`) — but its **name** and its **choices** are the workspace's: `update-attr companies domain --name Website` renames it and survives later `crm setup` runs; `update-attr deals pipeline_stage --options-json …` is how a pipeline or lead-stage list changes. The title field, identity fields and relation fields stay on every object.

Three things about the write shape, because guessing them wrong fails quietly rather than loudly:

- A column needs `key`, `label`, `data_type` (`text`, `numeric`, `boolean`, `jsonb`, `timestamptz`) and `semantic_type`. **Unknown keys are rejected**, so a typo or a copied-in field is an error rather than a column that silently lacks what you meant to give it.
- **A dropdown carries its choices at create time**, in the column's own `options` array plus `option_model_type` (`status`, `single_select`, `multi_select`). `metadata.option_set` is what `crm describe` REPORTS BACK — it is not what create accepts, and passing it is refused.
- **An identity is what makes two records the same one**, and without one a re-import creates duplicates. It names a column plus how the value is compared: `email_v1`, `domain_v1`, `linkedin_url_v1`, `exact_text_v1`, `uuid_v1` — the versioned names, not the short `email`/`domain` spellings that `--lookup-normalize` takes on a Table column. At most one identity per object is primary.

```sh
oxygen crm objects create --slug partners --display-name Partners --live \
  --columns-json '[{"key":"name","label":"Name","data_type":"text","semantic_type":"text","is_record_label":true},
                   {"key":"status","label":"Status","data_type":"text","semantic_type":"status","option_model_type":"status",
                    "options":[{"value":"prospect","label":"Prospect"},{"value":"active","label":"Active"}]},
                   {"key":"domain","label":"Website domain","data_type":"text","semantic_type":"text"}]' \
  --identities-json '[{"column_key":"domain","normalization":"domain_v1","is_primary":true}]'
```

Relationships between objects are defined after the object exists: `oxygen crm relationships define <object> <slug> --target-object <object> --cardinality one_to_many --live`. `one_to_many` reads source→target: one source record links many target records.

## Empty enrichment fields on existing records

CRM enrichment presets and backfill support Companies and People. A blank field
alone does not prove enrichment never ran. Inspect its configured presets with `oxygen crm enrichment list --object <object> --json`, and inspect
the backing Table's column and run when a fault or missing input needs diagnosis.
Arming automatic enrichment covers later record writes; records that predate it
may need a separate backfill.

Preview one bounded batch with
`oxygen crm enrichment backfill --object <object> --limit 50 --json`.
The preview costs 0 credits and reports pending records, the batch quote and the
estimated cost to finish. Inspect the exact target and quote, then obtain approval
before repeating that scope with `--live --approved --max-credits <n>`.
Each batch is capped at 5,000 records; later batches select what remains missing.
Keep existing values: `columns run --force` is not a backfill substitute.

MCP: hydrate `oxygen_crm_enrichment` with `oxygen_capabilities_schema`, then use
`oxygen_capabilities_call` with `{"tool":"oxygen_crm_enrichment","arguments":{"action":"backfill","object":"<object>","limit":50}}`.
This mixed read/write tool uses the call gateway even for its free preview.
Only after approval repeat the same scope with `live: true`, `approved: true`
and `max_credits` matching the approved ceiling. Return the run link and read its
outcome before starting another batch.

## Open Deal and Account Stage

**Open Deal** (`deal_stage`) is the most advanced currently open deal stage on a
company, also copied to its people. It is blank when no open deal remains,
including when all deals are won or lost. **Account Stage** (`lifecycle_stage`)
is the company's lifecycle derived from its people and deals, with a separate
human override; it is not the stage of one deal.

For stale projections after an import or relationship change, preview
`oxygen crm rollup --dry-run --json`; add `--include-lifecycle` only to include
Account Stage. Review the proposed scope and obtain approval before `--live`.
The repair costs 0 credits and makes no provider call. MCP uses
`oxygen_crm_rollup` through the call gateway, defaulting to dry-run;
`include_lifecycle: true` adds Account Stage and `live: true` applies the reviewed
repair. Read the records back and preserve manual lifecycle choices.

## Notes, tasks and files on a record

A record carries its own **notes, tasks (reminders) and files**, beside the timeline. `oxygen crm notes add <object> <record> "…"` writes a note (markdown, pinnable, editable; it lands on the timeline too); `oxygen crm tasks add <object> <record> "Send the deck" --due 2026-09-25 --priority high --assignee <email>` files a reminder on the record; `oxygen crm files attach <object> <record> <path>` attaches what the customer sent. **The open work across the whole workspace is one read**: `oxygen crm tasks list` (no record) lists every open task with the record it is about, its owner, deadline and priority — `--assignee me` for yours, `--status completed` for the done ones — and `oxygen crm tasks complete <task_id>` closes one. In the app that list is **CRM → Tasks** (`/crm/tasks`); a record's own live in its **Notes** / **Tasks** / **Files** tabs. All free and internal: no preview, no approval, no credits.
