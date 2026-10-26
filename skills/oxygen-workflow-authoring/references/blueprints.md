# Blueprints

A Blueprint is a reusable install: tables, columns, prompts and a disabled hosted Workflow from one manifest. Applying one costs 0 credits and makes no provider call or external write; enabling or calling the workflow is the separate, approved step. `oxygen blueprints list --json` shows the workspace's and OXYGEN's seed Blueprints; plays that install a kit of Blueprint stages are the `oxygen-recipes` skill.

## Describe, preflight, apply

```bash
oxygen blueprints describe dm-outbound-pilot --json
oxygen blueprints preflight dm-outbound-pilot --input-json '<json>' --json
oxygen blueprints apply dm-outbound-pilot --input-json '<json>' --json
```

1. `describe` lists the inputs, what gets created and which columns are gated. Confirm every input with the user before spending: for `dm-outbound-pilot`, titles (exact-match `[CEO]` syntax), country codes, Blitz `industry` and `job_level` enum values (`oxygen tools enums get blitzapi industry --json`), headcount, founded year, keywords, `max_leads` (at most 50) and the destinations (email platform and campaign, LinkedIn platform and campaign, CRM).
2. `preflight` compiles the manifest, validates the inputs and reports missing integrations, current prices and collisions, without spending. A missing required integration stops here.
3. `apply` creates the tables and a **disabled** workflow; it sources, enriches and enrolls nothing. Reuse existing tables with `--table-ref <ref=id>`, or target an installed workflow with `--workflow-id`.

## Run it

Before going live, show the resolved request (filters and `max_leads`), the estimated credits for each paid stage, the destinations and that their columns are gated, the table link and the ceiling, and get approval.

```bash
oxygen workflows enable <workflow> --approved --json
oxygen workflows call <workflow> --mode live --approved --max-credits <cap> --json
oxygen tables query <table> --limit 10 --json
```

Read a sample end to end (for this Blueprint, an icebreaker and its work email) before anything reaches a person. Outbound enrollment and CRM sync columns are created but never run by the workflow: each is its own approved run with its own ceiling, after that review.

```bash
oxygen columns run <table> outbound_email_enrollment --background --approved --max-credits <cap> --json
oxygen columns run <table> crm_sync --background --approved --max-credits <cap> --json
oxygen table-runs items <run_id> --status failed --json
```

Keep that split: chaining enrollment onto sourcing by editing a column definition skips the review the gate exists for.

## Stop

- Preflight reports a missing required integration: connect it first.
- A search returns zero rows: relax the filters (industries, countries, seniority).
- Generated copy reads generic or states facts it cannot support: stop, inspect rows, and tighten the prompt or raise the reasoning level before any enrollment.

## Share

`oxygen blueprints share <slug> --json` returns a public `share_url`; anyone opening it can apply the Blueprint into their own workspace. `--expires-in-days` bounds it, and `--disabled` creates it switched off. `blueprints apply --from-url <url>` applies a shared one.
