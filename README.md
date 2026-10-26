# GTM Engineering Skills for OXYGEN

Give your AI agent the skills to source accounts, research buyers, qualify leads and prepare outreach in your OXYGEN workspace.

**25 OXYGEN skills, with their playbooks and supporting references.** Use them directly in OXYGEN, or install them in Claude Code or Codex and connect your OXYGEN account. Both routes use OXYGEN for data and execution.

You need an [OXYGEN account](https://oxygen-agent.com). The skill download has no separate fee. Data, enrichment, sending and other execution use your workspace's plan, credits and connected accounts. [See pricing](https://oxygen-agent.com/pricing).

## Choose where to work

### 1. Work directly in OXYGEN

Open your workspace at [oxygen-agent.com](https://oxygen-agent.com), start a chat and paste a prompt from [Start with a useful job](docs/start-here.md). The OXYGEN route uses its hosted skill library; you do not need to install this repository inside the app. Product access and account connections still apply.

### 2. Work in Claude Code or Codex

You need Node.js 22.22 or later, npm 10.9 or later and a terminal-capable AI agent.

Install the OXYGEN CLI and sign in through your browser:

```sh
npm install -g @oxygen-agent/cli
oxygen login
oxygen whoami --json
```

Confirm that `whoami` shows the workspace you intend to use. Keep tokens out of prompts, repositories and messages.

From the project where you want to use the skills, install the kit for your agent:

```sh
# Claude Code
npx skills add OXYGEN-CRO/gtm-skills --agent claude-code --skill '*' --yes

# Codex
npx skills add OXYGEN-CRO/gtm-skills --agent codex --skill '*' --yes
```

These commands install into the current project. Choose the line for your agent, then start a fresh agent session in that project so it discovers the skills. The installer may create its own skill directories and lockfile.

Login can also install OXYGEN skills automatically. This repository gives you an inspectable release snapshot and setup guide. If you already use the hosted skill installer, you can keep that route instead:

```sh
oxygen skills install --agents codex --skill '*' --project --copy --json
```

Prefer the hosted installer when you want the current account-appropriate catalog. This repository contains a selected customer release snapshot; the hosted catalog may change independently.

For MCP-first clients, use the [official OXYGEN plugin and connection guide](https://github.com/OXYGEN-CRO/agent-plugins). This kit's full skill files are written for terminal-capable agents; installing Markdown alone does not connect an MCP server or authenticate OXYGEN.

## Try a first task

Paste this into OXYGEN, Claude Code or Codex after connecting:

> Use OXYGEN to verify which workspace is active. Read the company and ICP context already available, then show me the best next GTM action based on existing data. Explain the evidence and what remains unknown. Use free reads only. Do not spend credits, upload local files or send anything. Ask me the one question that would change your recommendation most.

Then choose one of the [6 starting prompts](docs/start-here.md):

| Job | Start with |
| --- | --- |
| Decide what to fix first | `oxygen-gtm-consultant` |
| Build a target-account list | `oxygen-sourcing` |
| Find buyers at those accounts | `oxygen-sourcing`, `oxygen-enrichment` |
| Research and qualify accounts | `oxygen-tables`, `oxygen-enrichment` |
| Prioritize warm opportunities | `oxygen-signals`, `oxygen-crm`, `oxygen-unibox` |
| Prepare an outreach pilot | `oxygen-sequencer`, `oxygen-deliverability` |

## What is included

The [skill catalog](docs/catalog.md) links every skill and describes when to use it. The package includes onboarding and GTM consulting, sourcing and enrichment, Tables and CRM, signals, email infrastructure, sequences, replies, content, publishing, workflows, knowledge, collaboration and diagnostics.

The method starts with your company context and a concrete goal. It checks what already exists, finds the bottleneck, proposes a motion and starts with a bounded pilot. An account list or signal is useful only when you can explain why it fits.

Review the exact audience, copy, schedule and cost before approving live work. A skill is an instruction file, not a running campaign or a standing job. Use OXYGEN's live previews and command discovery for current limits and approvals.

## Update the kit

The files are a release snapshot. To refresh a GitHub installation, use the [skills installer](https://github.com/vercel-labs/skills):

```sh
npx skills check
npx skills update
```

For current hosted skills, use `oxygen skills install` after signing in. If a saved command is no longer recognized, ask the agent to discover the current command with `oxygen commands get` or `oxygen capabilities search` before acting.

## Source and license

The skill files are copied without edits from a pinned OXYGEN product release. [SOURCE.json](SOURCE.json) records the source revision and SHA-256 hashes. The OXYGEN product repository owns the skill content; this repository owns the distribution guide. Maintainers can reproduce the export with [the sync script](scripts/sync_from_product.py).

This package uses the [OXYGEN Proprietary License](LICENSE). It permits unmodified use with an authorized OXYGEN account. It is publicly available, with no separate skill fee. Redistribution, resale or reuse in another product requires OXYGEN's written permission. Earlier lawful license grants are preserved by the license's own terms.

OXYGEN's [terms](https://oxygen-agent.com/terms) and [privacy policy](https://oxygen-agent.com/privacy) govern the service.
