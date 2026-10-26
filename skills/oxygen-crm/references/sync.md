# CRM sync (outbound and bidirectional)

Mirror OXYGEN Records or table rows into HubSpot or Attio, or keep both sides converged. Pushing rows into an outbound campaign (Smartlead, Instantly, lemlist, HeyReach) is `sequences push-external`: the `oxygen-sequencer` skill.

## Readiness first

A `needs_reconnect` or `health.status: error` connection is the most common cause of a failed sync. Check it before building anything, and surface it rather than route around it (never fall back to a standalone provider tool or MCP):

```bash
oxygen integrations list --json
```

If the provider is missing or unhealthy, stop and send the user to `https://oxygen-agent.com/connections` to reconnect.

## Continuous bidirectional sync (HubSpot and Attio)

A scheduled sync keeps an OXYGEN object and a CRM object converged in both directions. It is driven from the CLI and MCP; Connections manages only authentication, account selection and health.

```bash
oxygen crm sync configure --provider hubspot --object contacts --direction bidirectional --dry-run --json
oxygen crm sync run --provider hubspot --object contacts --direction bidirectional --dry-run --json
oxygen crm sync enable --provider hubspot --object contacts --approved --max-credits <n> --max-rows <n> --json
oxygen crm sync status --provider hubspot --object contacts --json
oxygen crm sync disable --provider hubspot --object contacts --json
```

- `configure --dry-run` returns real planned counts and writes nothing; `enable` arms the cron and the standing write permission; `disable` stops both.
- Read `sync run --dry-run` before enabling: it makes no provider calls and costs 0 credits on this request. In the JSON response, `data.preview.credits.quote` gives current unit prices, Workflow-step cap coverage and the unknown (`estimated_credits: null`) complete-run estimate. The configure counts preview does not contain this price quote.
- **Supported pairs only:** `hubspot/contacts`, `hubspot/companies`, `attio/people`, `attio/companies`.
- **Conflicts:** field-level most-recent-edit-wins. The newer of the provider field's edit time and the OXYGEN cell's edit time wins; within a small skew the provider wins and the value is not pushed back in the same cycle.
- **Bound both volume and spend.** Always set the per-cycle `--max-rows` row cap and the `--max-credits` OXYGEN spend ceiling. OAuth provider calls follow their current tool quote; an own-API-key call costs 0.05 credits after repricing takes effect. Live Workflow steps cost 0.05 credits each after repricing takes effect and count toward the spend ceiling then. Provider billing and the CRM's API quota are separate. The complete-run estimate is unknown (null), independent of the explicit ceiling. A stored manifest quote is a captured snapshot; refresh the preview for current prices and cap coverage. A zero provider quote does not make a Workflow cycle free.
- **A broken connection disables the cron.** When a cycle fails because the connection lost its write scope or its OAuth grant, that pair's cron switches off and `status` shows it. Reconnect with write access, then `crm sync enable` again.
- **Deletes are out of scope:** a cycle creates and updates, never deletes, a provider record or an OXYGEN row. A mapping archived because its CRM record was deleted is never re-created; clear the mapping to re-create on purpose.
- **Attio syncs outbound only.** Attio records carry no last-modified time, so a scheduled sync cannot tell which Attio records changed; `configure`, `run` and `enable` refuse `inbound` and `bidirectional` for Attio with `crm_sync_direction_unsupported` and need an explicit `--direction outbound`. Bring Attio records into OXYGEN with [import](import.md), or read exactly the ones you want with `attio.query_records` (`filter_view_id` for a saved Attio view, or a `record_id` `$in` filter).

## Column-based sync from a table

For a one-off push, write from a table with a provider write tool column (`oxygen tools search <provider> --json`, then `oxygen tools get <tool_id> --json`). The column pattern, its preview and approval, and the provider id, status and error columns every live write mirrors back: the `oxygen-tables` skill (`references/tool-columns.md`, External sync columns). Retry failed items through the run's retry (`oxygen table-runs retry-failed <run_id>`).
