---
name: oxygen-recipes
description: "Search, read and install OXYGEN plays: proven GTM motions with prerequisites, credit posture, approval gates and an optional kit of native stages. Use when the user names a play or wants a proven motion to borrow from; to design a motion for their company, use oxygen-gtm-consultant."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Recipes

The play catalog is OXYGEN's library of proven GTM motions. Every play has the same schema: business case, outcome, leading metric with labelled benchmark ranges, prerequisites with check commands, credit posture, approval gates and, optionally, a kit of native stages. A play is inspiration: adapt it to the company the way `oxygen-gtm-consultant` teaches, and keep its gates. Its steps call ordinary native primitives with ordinary previews, approvals, caps and observability.

## Commands

- Search by goal or constraint: `oxygen recipes list "<goal>" --view summary --limit 6 --json` (MCP `oxygen_recipes_list` with `query`, `view: "summary"` and `limit`). Results are ranked, best first; narrow with `--category`, `--stage` or `--audience`.
- Read one play: `oxygen recipes show <slug> --json` (MCP `oxygen_recipes_get`). It reports which kit stages this workspace already has before the body. Every body has four sections, The Play, Before You Start, Steps and If It Goes Wrong; `--section "Steps"` reads one. An old play name opens the play it folded into and says so first.
- Forecast a kit: `oxygen recipes apply <slug> --dry-run --json` preflights every stage in one read.
- Install a kit: `oxygen recipes apply <slug> --json` installs the stages in order under one approval: 0 credits, no provider calls, every Workflow disabled, and an already-active stage skipped rather than replaced.
- Keep a durable copy: `oxygen recipes install <slug> --json` saves the play as a playbook page in the workspace wiki.

A play the user already selected wins over any default. Installing grants nothing further: running, enabling, enrolling, sending and spending each keep their own preview, cap and approval.

## Which skill does the work

- "What should I do first?" or "who should I contact?": `oxygen-onboarding`.
- "Why is pipeline flat?", "what should we change?" or "plan our GTM": `oxygen-gtm-consultant`, which searches plays by the binding constraint and designs the motion.
- Running a stage: the feature skill that owns it, such as `oxygen-sequencer`, `oxygen-workflow-authoring` or `oxygen-signals`, whose audience campaign guide covers plays built on post engagers and followers.

Search, then read the one or two plays you need, and use live command discovery for exact flags, provider readiness and cost. Present a play in plain words: what it gets them, its steps, what the workspace still lacks, what it costs and what each approval asks; then ask whether to set it up. Return deep links for every native object and run you create.
