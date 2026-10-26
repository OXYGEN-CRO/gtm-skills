# Attio Runbook

Use this runbook for Attio CRM reads, record writes, list membership, and webhook-triggered reconciliation.

## When To Use

- The user wants to mirror approved leads, accounts, or lifecycle fields into Attio.
- A workflow needs to inspect Attio people, companies, records, lists, or tasks.
- An Attio webhook should reconcile provider state back into Oxygen tables.

## Before Writes

```bash
oxygen tools search attio --json
oxygen tools get attio.assert_a_record --json
oxygen integrations list --json
```

Run a dry-run or one-row preview first. Never write live CRM records without explicit approval, row scope, and a retry/idempotency plan.

## Sync Pattern

- Use `attio.records_query` or `attio.search_records` to inspect existing state before writes.
- Use `attio.assert_a_record` when the intent is create-or-update by a stable identifier.
- Store Attio record IDs, list entry IDs, operation status, error, and timestamp in the Oxygen table.
- Use Attio object/list identifiers from the connected workspace, not display labels, when building durable mappings.

## Approval

A live write follows the sync-column approval: the `oxygen-tables` skill, `references/tool-columns.md` (External sync columns). Name the Attio list as well when the write adds list entries.

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `attio.assert_a_list_entry_by_parent` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.assert_a_record` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.companies_query` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.create_a_comment` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_a_folder` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_a_list` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_a_note` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_a_record` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_a_select_option` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_a_status` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_a_task` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_a_webhook` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_an_attribute` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_an_entry` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_an_object` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.create_call_recording` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.delete_a_comment` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.delete_a_file` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.delete_a_list_entry` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.delete_a_note` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.delete_a_record` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.delete_a_task` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.delete_a_webhook` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.delete_call_recording` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.download_a_file` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.find_or_create_a_meeting` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.get_a_comment` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_a_file` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_a_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_a_list_entry` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_a_meeting` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_a_note` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_a_task` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_a_thread` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_a_webhook` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_a_workspace_member` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_an_attribute` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_an_object` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_call_recording` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.get_call_transcript` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.identify` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_all_lists` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_attribute_values_for_a_list_entry` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_attributes` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_call_recordings` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_entries` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_files` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_meetings` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_notes` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_record_attribute_values` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_record_entries` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_select_options` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_statuses` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_tasks` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_threads` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_views_for_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_views_for_object` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_webhooks` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.list_workspace_members` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.objects_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.patch_lists_list_entries_entry_id` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.patch_objects_object_records_record_id` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.people_query` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.query_records` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.records_get` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.records_query` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.search_records` | free — not billed | no_bill | none | OAuth — runs on the org's connected `attio` account |
| `attio.update_a_list` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.update_a_list_entry` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.update_a_record` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.update_a_select_option` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.update_a_status` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.update_a_task` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.update_a_webhook` | free — not billed | no_bill | external_send | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.update_an_attribute` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.update_an_object` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
| `attio.upload_a_file` | free — not billed | no_bill | crm_write | external write — live gate (approved + max_credits); OAuth — runs on the org's connected `attio` account |
<!-- END GENERATED -->
