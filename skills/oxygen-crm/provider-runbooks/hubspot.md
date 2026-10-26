# HubSpot Runbook

Use this runbook for HubSpot reads, contact/company writes, webhook events, or workflow-triggered sync.

## When To Use

- The user wants CRM records created or updated from an OXYGEN table.
- A HubSpot saved contact list should feed an OXYGEN Table (`tables hubspot import`), the suppression ledger (`suppressions hubspot sync`), or a Sequence (`sequences hubspot-list-import`).
- A HubSpot event should trigger an OXYGEN workflow.
- OXYGEN needs to mirror CRM IDs or lifecycle status back into table rows.

## Before Writes

```bash
oxygen tools search hubspot --json
oxygen tools get <hubspot_tool_id> --json
oxygen integrations events list --source hubspot --json
```

Run dry-run or one-row preview first. Never write live CRM records without explicit approval.

## Sync Pattern

- Use a tool/sync column for the write.
- Store HubSpot object IDs, operation, status, error, and timestamp in the table.
- Use provider IDs or idempotency fields to avoid duplicate records.
- Use workflow events for inbound webhook-triggered reconciliation.

## List To A Table + DNC

The user wants one saved HubSpot list as **rows they can work**, and no Sequence
yet. This is the create-table lane, not `crm sync import` (which pulls a whole
object and has no segment filter) and not the Sequence path below (which needs a
Sequence to bind to).

```bash
oxygen tables hubspot lists --json                      # saved lists; 0 credits, definitions only
oxygen tables hubspot import --list <lead_list_id> \
  --dnc-list <dnc_list_id> --name "Q3 leads" --json     # free preview -> fingerprint
oxygen tables hubspot import --list <lead_list_id> --dnc-list <dnc_list_id> \
  --live --approved --reviewed-fingerprint <hash> --json
```

- Rows land in a **new Table**, keyed on `hubspot_contact_id`, and nothing is
  enrolled or sent.
- `--refresh once` imports a single time; the default re-snapshots on a bounded
  cron.
- Do-not-contact first, `--no-dnc` and list-only suppression: [import](../references/import.md).

## List To Sequence + DNC

Use HubSpot's saved contact segment/list as the source of truth: an **Active** segment recalculates membership in HubSpot, while a **Static** segment changes only when someone edits its membership. In the web app, open the Sequence's **Leads** stage and choose **Import leads → HubSpot list**. The equivalent agent-first discovery path is:

```bash
oxygen sequences hubspot-list-import lists <sequence> \
  --query "<saved-segment-name>" --json
```

Preview the exact lead list, DNC list, cadence, Table binding, and caps without reading list members or changing workspace state:

```bash
oxygen sequences hubspot-list-import configure <sequence> \
  --lead-list <lead-list-id> \
  --dnc-list <dnc-list-id> \
  --max-records-per-list 5000 \
  --max-credits <n> \
  --json
```

After showing that preview to the operator, repeat it with `--live --approved --reviewed-fingerprint <fingerprint>`. The live request creates and binds a leads Table only when the Sequence has none, arms one deterministic `hubspot-list-sequence-sync` Workflow revision for that Sequence, and queues the first durable cycle immediately. An active Sequence with no Table must be paused before that binding change.

- Connect HubSpot with `crm.lists.read` and `crm.objects.contacts.read` granted.
- The DNC snapshot is read and imported first. Imports are additive: removal from HubSpot never removes an OXYGEN suppression.
- Each HubSpot **contact** lands as one merged do-not-contact person (subject `hubspot:contacts:<record_id>`) holding its email, LinkedIn URL, and primary phone together; a second phone keeps its own typed row under that same subject. **Company**-list rows stay company subjects (`hubspot:companies:<record_id>`) and block the domain / LinkedIn page across every channel. In the run receipt `people_imported` counts contacts only, while `subjects_imported` counts person and company subjects together. Contact/company DNC sync without a Sequence is `oxygen suppressions hubspot lists|sync`, where either list id may be omitted.
- To un-suppress a whole merged person, remove the **subject**, not one identifier: `oxygen suppressions remove --subject-id hubspot:contacts:<record_id>` (MCP: `oxygen_suppressions_remove` with `subject_id`) clears that subject's email, phone, LinkedIn, and company rows in one transaction and reports per-ledger counts. Read the id as `metadata.dnc_subject_id` in `oxygen suppressions list` — which lists LinkedIn rows only, so a HubSpot contact with no LinkedIn URL appears instead in `oxygen suppressions addresses|phones|companies --json`. `manual:<uuid>` subjects are returned in the `subjects[]` receipt of `oxygen suppressions import-person`. Removing one identifier (`--lead`, `remove-address`, `remove-phone`, `remove-company`) still leaves the person suppressed on every other channel, and a later sync re-imports the subject.
- The lead snapshot is upserted by HubSpot contact id, then only current members with canonical Table row ids and usable emails are offered to the bound draft, active, or paused Sequence. Draft/paused enrollments remain pending until launch/resume; active recipients use the Sequence's existing pacing and ceilings.
- Re-running the sync is safe: the same Sequence will not enroll the same Table row twice, and `exclude_contacted` controls cross-Sequence duplicate exclusion.
- Paging, count, hydration, suppression-import, Table-binding, or row-provenance mismatches fail closed before enrollment.
- Leaving the HubSpot lead segment does not stop a recipient who is already running: membership governs new enrollment on each successful snapshot, and a newly added DNC suppression still blocks further sends through the Sequence's suppression checks.
- Add enrichment as ordinary Table columns before enrollment when a motion needs it.

## Approval

A live write follows the sync-column approval: the `oxygen-tables` skill, `references/tool-columns.md` (External sync columns).

<!-- BEGIN GENERATED: prices -->
## Credit prices (generated)

Prices describe the example payload; request shape (limits, formats, waterfall options) changes the billed amount. Live runs of any operation not classed `none`/`no_bill` require `approved=true` plus `max_credits` (server-enforced). Hydrate the selected operation with `oxygen tools get <tool_id> --json` for its current quote and exact inputs.

| Operation | Customer price | Billing | Side effects | Notes |
| --- | --- | --- | --- | --- |
| `hubspot.api_request` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.companies_archive` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.companies_create` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.companies_get` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.companies_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.companies_search` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.companies_update` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.contacts_archive` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.contacts_create` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.contacts_get` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.contacts_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.contacts_search` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.contacts_update` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_association_labels_archive` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_association_labels_create` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_association_labels_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_associations_archive` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_associations_create_default` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_associations_create_labeled` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_associations_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_objects_archive` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_objects_batch_archive` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_objects_batch_create` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_objects_batch_read` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_objects_batch_update` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_objects_create` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_objects_get` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_objects_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_objects_search` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_objects_update` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_owners_get` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_owners_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_pipeline_stages_archive` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_pipeline_stages_create` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_pipeline_stages_get` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_pipeline_stages_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_pipeline_stages_update` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_pipelines_archive` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_pipelines_create` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_pipelines_get` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_pipelines_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_pipelines_update` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_properties_archive` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_properties_create` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_properties_get` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_properties_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_properties_update` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_schemas_archive` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_schemas_create` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_schemas_get` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_schemas_list` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.crm_schemas_update` | free — not billed | no_bill | paid_provider | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.list_memberships` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.lists_get` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
| `hubspot.lists_search` | free — not billed | no_bill | none | OAuth — runs on the org's connected `hubspot` account |
<!-- END GENERATED -->
