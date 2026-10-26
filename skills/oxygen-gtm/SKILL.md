---
name: oxygen-gtm
description: "Route an OXYGEN GTM outcome to its native primitive and the feature skill that teaches it: Knowledge, Records, Tables, Messages, Posts, Signals, Dashboards, Ads, Tags, Sequences, Publishing, Workflows, Agents, Observability. Use as the fallback when no narrower skill matches."
allowed-tools: Bash(oxygen *)
---

# OXYGEN GTM

Use the narrower skill the map names. For onboarding, load `oxygen skills get oxygen-onboarding --json` before company questions; for a GTM diagnosis or plan, load `oxygen skills get oxygen-gtm-consultant --json`.

## Discover, then hydrate

Start from the outcome, not a product noun:

```bash
oxygen capabilities search "<goal>" --json
oxygen commands get "<recommended command>" --json
```

MCP: `oxygen_capabilities_search` → selected `oxygen_capabilities_schema` → `oxygen_capabilities_read` (read-only) or `oxygen_capabilities_call` (writes/spend), with `{tool, arguments}`. Providers: `oxygen tools search "<intent>" --json` → `oxygen tools get <tool_id> --json`. Inspect inputs, cost and gates before calling.

Hydrate a skill with `oxygen skills get <name> --json` (MCP `oxygen_skills_get` with `{name}`); read one supporting file with `--file <manifest-relative-path>` (MCP `{name, file}`). Instruction reads need an authenticated, entitled workspace.

## Ownership map

| Intent | Native owner | Skill | Boundary |
|---|---|---|---|
| company context, ICP, positioning, voice, durable findings | Knowledge Graph | `oxygen-knowledge` | not local chat memory |
| proven plays to borrow from | Recipes | `oxygen-recipes` | advisory; not an execution runtime |
| canonical companies, people, deals, custom objects | Records | `oxygen-crm` | working lists stay in Tables until promoted |
| row work: AI, research, formula, tool columns, Functions, feeds, imports | Tables | `oxygen-tables` | never rebuild execution in a local spreadsheet/script |
| contact and company data, waterfalls, verification | Tables | `oxygen-enrichment` | name the data, not the provider |
| new companies and people, TAM, personas | Tables via planners | `oxygen-sourcing` | plan and preview before paid pulls |
| direct email or reply in an existing thread | Messages | `oxygen-unibox` | net-new LinkedIn initiation belongs to Sequences |
| post drafts, comments, reactions, performance | Posts | `oxygen-publishing` | a draft is saved as a Post, not left in chat; Publishing owns delivery |
| durable events: visits, views, engagement, hiring, funding, posts | Signals | `oxygen-signals` | a reported visit is a Signal on the person's record, not a note or row; acting on one is Sequences or Workflows |
| funnel, spend and needs-action reporting; saved dashboards | Dashboards | this skill | not a second analytics store |
| competitor ad intelligence | Ads | `oxygen-signals` | owned-audience activation is not implied |
| cross-primitive labels and campaign handles | Tags | this skill | not a separate campaign entity |
| cadence, enrollment, suppression, reply-stop, net-new LinkedIn | Sequences | `oxygen-sequencer` | not generic automation |
| scheduled, approval-gated broadcast delivery | Publishing | `oxygen-publishing` | not one-to-one outreach |
| deterministic triggers, branches, retries, approvals | Workflows | `oxygen-workflow-authoring` | hosted Workflow, not a local loop; local files only author definitions |
| adaptive governed goals, threads, checkpoints | Agents | this skill | deterministic graphs belong to Workflows |
| runs, costs, failures, approvals, provenance | Observability | `oxygen-diagnostics` | read/control lens, not another executor |

Public or third-party LinkedIn research uses the native cookieless `scraper.*` catalog by default and consumes no connected-account quota; connected `linkedin.*` operations are for the workspace account's own network, inbox and writes. Never silently fall back from the native scraper to a more expensive provider.

**Dashboards, Tags and Agents** have no feature skill; hydrate each command before use. `oxygen dashboards summary --range 30d --json` reads the curated funnel, and `dashboards create` with `dashboards widgets kinds|add` builds a saved one. `oxygen tags list --json` reads the vocabulary, `tags attach` replaces an item's tags, and `tags rename` previews until `--apply`. Tags preserve entered case and match case-insensitively; case-only renames update spelling everywhere, including archived carriers (for example, `oxygen tags rename "trust valley days 2026" "Trust Valley Days 2026" --json` previews the change). `oxygen agent list --json` lists Agents, `agent create` builds one (at most five skills including dependencies), and `agent run` needs `--approved` and its own `--max-credits`: tool authority never implies spend authority.

## Operating loop

1. Confirm the active workspace and resolve relevant Knowledge context.
2. Search the capability catalog and accept the native owner unless the user chooses otherwise.
3. Hydrate one command/tool schema and inspect readiness.
4. Preview the smallest representative scope. For Tables, start with a few rows.
5. Before credits or external writes, show scope, estimated credits, and side effects; require explicit approval and a hard ceiling. Stop with `AWAIT_APPROVAL` until that approval arrives. In an Oxygent chat, a paid step whose `max_credits` is under 100 credits needs no approval: run it and state its cost in one plain line.
6. Execute on OXYGEN's hosted primitive. Long work becomes a durable run.
7. Return the `web_url`, cost/provenance, and any retryable failures.

Spend arithmetic, stop-after-pilot rules and honest reporting: [guides/cost-precheck.md](guides/cost-precheck.md). Recipes and Blueprints add execution depth; a recommendation does not start a motion. The live search, get and schema surfaces are the source of exact grammar.
