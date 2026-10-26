---
name: oxygen-workflow-authoring
description: "Build, run, or debug deterministic OXYGEN Workflows: schemas, triggers, branches, retries, approvals, durable runs, Blueprints, Teams notifications and MCP tools. Local files only author hosted definitions; adaptive goals use Agents and outreach cadence uses Sequences."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Workflow Authoring

A local file is only an authoring input; OXYGEN runs graphs durably as hosted workflows.

## Boundary

- Workflows own deterministic triggers/control flow; Agents own adaptive goals
  and tool choice; Sequences own outreach cadence; Tables own row dependencies.
- Use hosted runs, never local cron or shell loops.
- Start from a Blueprint when one fits: [Blueprints](references/blueprints.md).

## Authoring loop

1. Write the spec as data: goal, trigger (API, webhook, cron or event), input
   schema, steps with aliases, exact tool ids (`tools search --workflow-eligible`,
   then `tools get`), expected outputs, failure behavior and idempotency key,
   and credit expectations.
2. Search definitions and templates and inspect the schema. Author explicit
   resource ids; lint and apply an immutable version. A node id may not
   contain `#` (reserved for loop iteration step ids). Graph schema
   `examples[0]` lints clean (webhook, set, `oxygen_table_rows_insert`).
3. Before go-live or sign-off, `workflows call <ref> --preview`: what leaves
   OXYGEN, which accounts, the credit floor; it runs nothing and takes no
   `--mode`. Then smoke-test, dry-run, get approval for the exact live scope,
   and watch with `workflows tail`.

```bash
oxygen workflows events list --search "<outcome>" --kind builtin --json
oxygen workflows init --id my-workflow
oxygen workflows schema --subject graph --json
oxygen workflows lint --file my-workflow.workflow.json --phase draft --json
oxygen workflows apply --file my-workflow.workflow.json --draft --json
oxygen workflows lint --file my-workflow.workflow.json --phase publish --json
```

Events: `workflows events list --search <outcome>` (also `--source`, `--kind`)
covers Sequencer outcomes, CRM timeline activity, CRM signals and this
workspace's integration events; `workflows events get <catalog-id>` returns the
exact trigger object. Select its `source`, `event` and `filters` together. A
provider event dispatches only once enabled for the workspace:
`oxygen integrations events enable --source hubspot --event contact.created --json`.
Setup-required events stay draftable but block publish and enable; custom
events need no provider setup. MCP: hydrate `oxygen_workflows_*` through
`oxygen_capabilities_schema`.

Lint returns the same org-aware `canSaveDraft` / `canPublish` report everywhere.
Draft phase permits safe incomplete work; publish phase (the default) checks
readiness. Candidate approval or cap flags never grant authority.

For existing definitions, `oxygen workflows list --search "<name>" --limit 20 --json`
bounds the inventory; `oxygen workflows get <slug> --json` checks an exact ref.

## Run readback

CLI calls without `--preview` create a run; previews return `data.preview` only.
Use the Workflow run's `id` (`data.run.id` in CLI JSON, `run.id` on MCP)
for `tail` and stored reads. `run.runId` is a separate provenance id.
Canonical graph output is `run.output.steps.<node_id>`; inspect the step
that ran and its receipt before signing off. Read bounded native values with:

```bash
oxygen workflows runs --run-id <run_id> --projection value --path /runs/0/output --json
```

The observed cost receipt is returned by `oxygen workflows run <run_id> --json`
and `tail`. For a long response, save its JSON inside your working directory
and read the file with offset/limit controls.

If a value spans windows, pass `next_value_cursor` as `--value-cursor` with
the same selection and path. Append each `value_json` fragment in offset
order until `next_value_cursor` is null, then parse the combined JSON.
MCP: `oxygen_workflows_runs` uses `run_id`,
`projection: "value"`, `path` and `value_cursor`.

## Modes and spend

Draft apply is inert: 0 credits, no node calls, no run, no publish. After
publish lint passes, apply without `--draft`; `call` and `enable` authorize
execution separately.

- `smoke-test` and `dry-run` both accept your `--input-json` (MCP: `input`),
  defaulting to `{}`. They spend 0 credits and make no paid
  provider call or external write; internal reads use current data and
  `oxygen.http_json_request` may GET.
- **A live call needs `--approved` and a positive `--max-credits`**; without
  them the server refuses with `approval_required` or `spend_cap_required`:
  `oxygen workflows call <ref> --input-json '<input>' --mode live --approved --max-credits <n> --json`.
- Quote an unsaved v2 draft with `oxygen billing estimate --workflow-manifest '<JSON>' --workflow-cron '* * * * *' --json`
  (MCP: `oxygen_billing_estimate`, `workflow_manifest` and optional `workflow_cron`).
  This reads prices and the stored spendable balance without financial maintenance.
  It returns a step-cost floor; provider charges, retries and loops can add costs,
  so its upper bound stays unknown. Lint the draft separately before publishing.
- In v2 graphs, ordinary tool nodes bill automation steps; trigger, set and code
  nodes do not. Loops and embedded durable recipes can add billable executions.
- Live runs bill each executed step (`usage.credits_per_step` in `workflows get`);
  writing rows is free. Monthly cost = runs x steps/run x that price. A step on
  the workspace's own provider key also pays the BYOK platform fee when one applies
  (`oxygen billing usage --meter byok_calls`), inside the run's `max_credits`.
- External writes need approval unless the user granted a scoped standing
  permission in product configuration; enabling a cron, event or webhook
  workflow is that standing grant, with its per-delivery ceiling.

For budget refusal, armed-cron pause/resumption or nullable action allowances,
read [Budget state](references/budget-state.md).

Your plan sets the fastest cron schedule (`limits show` →
`workflow_limits.cron_min_interval_minutes`); a faster one is refused with
`cron_interval_below_plan_minimum` and a `details.suggested_cron`. A webhook
trigger's `rate_limit` (in `workflows get`/`apply`) is the deliveries a minute
its URL accepts before HTTP 429. A Code node may declare `timeout_ms` up to
30000; one run attempt gets 30 minutes, then resumes from its checkpoints.

Test ONE step with `workflows call --node <id>` (`test_node_id` on MCP):
OXYGEN runs the target plus only the predecessors it needs from the exact saved
version. Non-live, canonical graph workflows only. JavaScript Code gets only
declared inputs and needs a closed output schema; `run_source`/`ctx` is legacy.

## Composition rules

- Keep row work in Tables; use native actions, not hidden local data. Build the
  smallest child workflow first; add events, fan-out or schedules after it works.
- Outbound uses `oxygen.sequence_enroll` on an active bounded Sequence, never a
  raw provider message.
- Branch on documented outputs and pin exact provider operations.
- Preview/cap paid or external writes; Workflow approval never bypasses safety.
- Notify a Teams channel or chat from a workflow: [Microsoft Teams](references/microsoft-teams.md).

## Lifecycle

Delete is permanent and preview-first: run `workflows delete <ref> --json`, then
repeat with `--yes`. Run history stays read-only.

Rotate webhook secrets preview-first with `workflows webhooks rotate <ref>
--json`, then `--approved`. The old secret stops immediately; copy the one-time
replacement. Rotation never publishes, enables, or runs.

Replay only verified `outcome=ran` webhook deliveries with `workflows webhooks
replay <delivery-id> --request-key <stable-key> --json`. It creates an
inspectable, idempotent `dry_run` of the original revision and payload without
changing ingress/history, spending credits, or writing externally.
