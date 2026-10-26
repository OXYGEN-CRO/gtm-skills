---
name: oxygen-quickstart
description: "Run a safe first OXYGEN CLI session: verify identity and workspace, search capabilities and exact commands, create a small hosted Table, inspect it, and discover provider operations without executing paid calls or external writes."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Quickstart

Use `oxygen` in the authenticated environment; never switch environments or workspaces on your own.

For onboarding or a first improvement, load `oxygen-onboarding` with `oxygen skills get oxygen-onboarding --json` before asking company questions; for a diagnosis of what already runs, load `oxygen-gtm-consultant`. Reserve the Table demonstration below for an explicit product walkthrough.

For an explicit safe CLI walkthrough:

1. Verify identity and workspace with `oxygen whoami --json`; resolve org selection. On `entitled: false` follow its `billing_owner_candidates` before proposing a plan. Each app connected with OAuth (ChatGPT, Claude…) keeps its own default workspace: `oxygen connectors list`, then `oxygen connectors set`. What OXYGEN sends an app (its event subscriptions and deliveries): `oxygen connectors events get <app>`; `oxygen connectors events revoke <app> --subscription <id|all>` stops them. While an app holds event subscriptions its paid calls are capped by its daily credit ceiling: `oxygen connectors get <app>` shows it and what it spent; `oxygen connectors set <app> --credit-ceiling <credits>` changes it. Your own sidebar pages (Settings → Customise): `oxygen settings pages list`, then `oxygen settings pages set --hide <pages>`; only yours changes, nothing is deleted.
2. Route an outcome with `oxygen capabilities search "build a small prospect table" --json`.
3. Hydrate one recommendation with `oxygen commands get "tables create" --json`.
4. Create a tiny hosted Table and insert a few manual rows using the exact returned grammar.
5. Describe and inspect the bounded rows; surface the table `web_url`.
6. Demonstrate the second catalog with `oxygen tools search "public LinkedIn profile" --json`. Do not call `tools run-live` or run a paid column. `oxygen tools search --for-table <table-id> --json` on the table from step 4 answers "what can I add here, and what will each row cost" without spending.
7. Find a narrower skill with `oxygen skills search "<next goal>" --json`, then hydrate it with `oxygen skills get <name> --json` or install it.
8. For the next improvement, use `oxygen-onboarding`; `oxygen recipes list --json` and `oxygen blueprints list --json` supply optional depth.

The CLI keeps itself current; `oxygen update --status --json` shows the installed and newest version and whether automatic updates are on (turn them off on a build server with `oxygen update --disable-auto` or `OXYGEN_NO_AUTO_UPDATE=1`).

Stop before any credit-consuming provider call, AI/tool/waterfall column run, purchase, CRM write, or outbound action — including every step inside a selected play. The first session should prove hosted state and discovery, not spend.
