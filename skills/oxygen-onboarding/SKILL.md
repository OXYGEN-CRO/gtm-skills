---
name: oxygen-onboarding
description: "Guide OXYGEN onboarding: company context, first leads, a reviewed sequence, sender and bounded launch; set up daily Oxygent routines when requested. Use for 'get me started' or the first campaign and morning briefing. For a GTM diagnosis or plan, use oxygen-gtm-consultant."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Onboarding

In an Oxygent chat, a guided "Start onboarding" runs agent-led onboarding as the chat's instructions say; a chosen play then follows the steps below.

Other workspaces follow Get started: **first leads → first sequence → a connected account → launch** (`oxygen activation checklist --json`, MCP `oxygen_activation_checklist`). Learn the company and goal; explain one step at a time.

For a named play, run `oxygen recipes show <slug> --json` and use existing workspace resources.

## Speed rules

- Resolve context: `oxygen knowledge resolve --purpose onboarding --json` (MCP `oxygen_context_resolve`, purpose `onboarding`). It may migrate the workspace schema, then returns company research, workspace state (`workspace`) and next reads (`plays`). Run independent reads together.
- When `plays.workspace` is `blank`, skip the warm-lead reads and answer about their company. Never tell the user the workspace is blank or empty.
- Say in one sentence what you are checking, then check. Never make the user wait on research or confirm a dossier first.
- Ask one question only when it changes the next action; offer concrete choices.
- Leftover test tables and drafts are not findings unless they block a step.
- In a coding agent, also read your starting folder (docs, pricing notes, customer lists, CRM or LinkedIn exports); never upload or write a file into OXYGEN without asking.
- End every answer with the next step and what it costs or needs approved, never with "tell me what you want".

## 1. Know the company

New workspaces start with website drafts (`persona-*`, `pain-*`, `filter-*` and more): build on them; set each `active` once confirmed. When the profile's offer or ICP is empty, read the research page (`oxygen knowledge page get company-research --json`): it holds the product, pricing, alternatives and hypotheses. In the first answer, say in two or three lines what the company sells, to whom and why it wins, and draft the ICP in one line as a hypothesis. A claim needs a number or named customer behind it; otherwise call it unproven. Invite corrections without waiting, and save what the user confirms or corrects ([consultation](references/consultation.md)). When research is missing or still running, say so in one line and follow [consultation](references/consultation.md#when-research-is-missing). The full offer and ICP, with their quality bar: [offer and ICP](references/offer-and-icp.md).

## 2. Show real matches, then ask

In the same answer, run the free company preview on the ICP (`oxygen companies search filters --json` lists accepted values) and list the five best matches with why each fits. Close with choices that act on them: save them with their buyers as the First leads (free), tighten the ICP, or use their own list. If the preview fails, don't wait on it: say so in one line and offer two or three first steps from the workspace's lists or a fitting play (`oxygen recipes list`), each with what it gets them. Without research, first ask in one line what they sell.

## 3. First leads

Source the first list from whatever fits their goal. With warm sources connected, work the warmth ladder first: customers and open deals, the user's LinkedIn network and engagers, people showing intent ([warm leads](references/warm-leads.md)). Otherwise use the free company and people previews on the ICP's filters (`oxygen companies search filters --json`, `oxygen people search filters --json`), a CSV they already have, their CRM, or people engaging with posts about the buyer's problem. A free preview shows up to 50 real matches: if the first page does not look like their buyers, tighten once (the buyer role, an exclusion, a narrower size) and preview again. Drop do-not-contact entries and sample records (`_sample: true`).

`network_mining` in First leads: [day-1 loop](references/day-one-loop.md). Save the list with the onboarding read's `plays.save` before you answer: about ten ranked leads with why each fits, and first-message drafts for the top three to five in its `draft_message` cells, each grounded in why that person fits. Drafting needs no approval. This ticks **Source your first leads**. That table is the shortlist; when the user wants the whole market in a table, the preview's `next_step` saves every match, up to a tenth of their credits, after their approval, never a 50-row sample.

## 4. First sequence

Create the first sequence for the channel they chose; a draft counts and nothing sends until launch: `oxygen sequences create` (MCP `oxygen_sequences_create`), or `oxygen sequences draft --channel linkedin` for AI-written LinkedIn steps (`--channel email` for email; generation requires a previewed credit cap). Ground every step in the offer and in why these leads fit; a new LinkedIn account starts with a few invites and messages a day, so a blast is never the plan. This ticks **Create your first sequence**.

## 5. Connect the account

Connect the account the sequence sends from: LinkedIn with `oxygen senders connect` (MCP `oxygen_senders_connect`) or the web Connections page, or a mailbox for email. A connected account has a monthly cost the connect states first. Every sending account connects only on a plan: on a free workspace, tell the user to subscribe to the Oxygen plan and link the plan page the refusal returns (`upgrade_url`), never a credit top-up. This ticks **Connect your first account**.

## 6. Launch

Review the exact selected audience, sender, personalized copy, schedule and positive action ceiling through the native preview (`oxygen sequences preview`, MCP `oxygen_sequences_start` with `approved: false`). For the guided LinkedIn pilot, follow [bounded launch](references/bounded-launch.md) and echo its frozen review. Start under the current explicit or valid auto-approve authority. Launch, first confirmed send and daily readiness are distinct outcomes.

Free and paid steps under 100 credits in Oxygent chats run (state cost in one line); outbound or larger steps need approved caps. After each step, read the checklist, say what is done and what comes next, and link what you built.

## 7. Daily rhythm, when requested

For requested nightly scans or morning briefings, follow [daily Oxygent routines](references/daily-rhythm.md): two explicit schedules, confirmed IANA timezone, exact resources and separate caps. Candidates stay review only; briefings go to Oxygent’s chat (shared for Workspace, creator-only for Personal). Preserve own-agent access and native readiness refusals. Routine readiness is separate from checklist milestones.

## 8. Remember

Save the confirmed offer, ICP, chosen goal and next step so the next session resumes from them ([consultation](references/consultation.md) has the commands). For a diagnosis of what runs or a GTM plan, hand over to the `oxygen-gtm-consultant` skill.

Plays: [day-1-first-win](plays/day-1-first-win.md).
