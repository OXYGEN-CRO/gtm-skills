---
name: oxygen-sequencer
description: "Run OXYGEN Sequences: net-new LinkedIn outreach, even one message, and multistep email, LinkedIn, WhatsApp, call and CRM-task cadences. Covers the launch ladder, send ceilings, enrollment, do-not-contact, reply-stop and recovery. Existing-thread replies and direct email use Messages."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Sequencer

Sequences own outreach initiation and cadence: sender binding, pacing, suppression, reply-stop, retries and provenance. Step kinds and copy syntax (interpolation, fallbacks, spintax, conditionals, sender variables) live in `oxygen sequences create --help`; this skill carries the gates.

## Boundary

- New LinkedIn conversation, even one person/one message: Sequence (one-step gateway: `sequences send` / `oxygen_sequences_send`).
- Multi-recipient or multistep email, LinkedIn, WhatsApp, call or CRM-task outreach: Sequence.
- Reply in an existing email, LinkedIn or WhatsApp thread: Messages (`oxygen-unibox`).
- New direct email with no cadence: Messages via `email send`.
- Deterministic automation around a campaign: a Workflow outside, the Sequence inside. A Workflow enrolls leads and the Sequence sends; a draft or paused Sequence holds them until start.
- Rows for a campaign already running in Smartlead, Instantly, lemlist or HeyReach: `sequences push-external` ([external campaigns](references/external-campaigns.md)).

Channel rules: [email](references/email.md), [LinkedIn](references/linkedin.md) (also LinkedIn account safety), [WhatsApp](references/whatsapp.md), [calls and CRM tasks](references/calls-and-crm-tasks.md). Branching, signals, variants and send windows: [journeys](references/journeys.md).
For cold outbound open its play: [whole market](plays/whole-tam-email.md), [signals](plays/signal-outbound.md), [email + LinkedIn](plays/multichannel-top-tier.md); [copy](references/cold-copy.md).

## Launch ladder

1. Readiness: `oxygen sequences get <sequence> --readiness --json` lists blockers (a missing send cap, the WhatsApp opt-in, sender gaps) and the mailbox pool, and changes nothing.
2. Draft: `sequences create`, then `sequences update` while draft. `--sender-profiles` gives each lead one person across channels; `sequences get` lists every sending account under `sender_pool`, and `--senders ""` removes accounts attached directly.
3. Preview: `oxygen sequences preview <sequence> --json` is the free launch check (MCP: `oxygen_capabilities_read` on `oxygen_sequences_start` with `approved: false`): `sender_journey` (who sends each step), per-kind scope, capacity, suppressions, CRM readiness and rendered LinkedIn/WhatsApp copy samples. `oxygen sequences render <sequence> --json` (MCP `oxygen_sequences_render`) renders every step and A/B variant, email included, for leads of the bound table, even on a draft. Unsubscribe settings are in `sequences get` (off when unset).
4. Ceilings: state the send ceiling; a credit ceiling only on request.
5. Approval: explicit approval for the external write and the ceilings.
6. Enroll, then start: `sequences enroll`, then `sequences start <sequence> --approved` with the approved ceilings. Name every `unresolved_linkedin_lead_details` row (not enrolled) and every `linkedin_unavailable_lead_details` row (LinkedIn skipped), not only the counts. Return the Sequence and run deep-links.
7. Monitor: `sequences stats` (operational reasons, today's budget), `oxygen sequences events <sequence> --kind skipped,sent --json` (including `no_whatsapp_account` skips), `sequences enrollments <sequence> --status failed`, sender health. Results: [analytics and compact reads](references/analytics.md#compact-progress-reads).

`sequences start --dry-run` is a separate action: it activates a simulated run with no sends and no credits, and a later live start restarts those leads from the first step.

## Send ceilings

- `--max-live-sends <n>` is the hard ceiling on real sends and CRM writes across channels. Email, WhatsApp and CRM-task journeys require it for a live start, because those actions cost 0 credits and a credit cap cannot bound them; without it the start returns `send_cap_required`. LinkedIn-only journeys may add it.
- `--max-credits <n>` is an optional credit ceiling, off unless set; sends cost 0 credits. AI-written comments bill outside it, so 0 refuses them. Omitted at start, a saved ceiling applies.
- After the first start, change ceilings through `sequences start`.

## Enrollment

- `sequences enroll <sequence> --from-table` admits unenrolled bound rows, max 500/call, with no qualification filter. Repeat while `from_table.has_more`; on zero progress read `skipped_by_reason`. Subset: `--leads-file` with `table_row_id`s. Missing table (`sequence_no_source_table`): `sequences update <sequence> --source-table <table>` while draft or paused.
- `--max-new-enrollments-per-day` paces first touches; it never shrinks what enrollment admitted.
- WhatsApp-only campaigns enroll each normalized number once, including `--from-table`. Mixed campaigns keep other channels and skip duplicate WhatsApp actions. [Duplicate scope](references/whatsapp.md) defaults to this campaign.
- `--exclude-contacted` skips people another active Sequence is talking to. A `bound_to_other_sender` skip means another LinkedIn account owns that person: add that sender to the pool or accept the skip ([LinkedIn](references/linkedin.md)).
- A deleted source row leaves its lead enrolled and contacted: `sequences contacts-remove <sequence> --missing-source-rows` previews them and `--approved` removes them.
- Recurring HubSpot-list enrollment: `sequences hubspot-list-import configure` previews; live needs the reviewed fingerprint with `--live --approved`.

## Do not contact

The list always blocks, at enrollment, at planning and before every send. Policy decides who is added: read `suppressions policy show`, change one rule with `suppressions policy set --rule <key> --effect <off|stop_only|suppress>`. Seven events default to `suppress`: `email_hard_bounce`, `email_unsubscribe_click`, `email_optout_phrase`, `linkedin_reply`, `whatsapp_reply`, `call_do_not_call`, `call_wrong_number`.

- `linkedin_reply` and `whatsapp_reply` fire on any inbound message, so by default a positive replier is blocked from every future campaign. `stop_only` ends only the current enrollment; settle this before the first live start.
- `email_hard_bounce` and `email_unsubscribe_click` are compliance rules: lowering them keeps mailing bounced addresses or ignores unsubscribes. Keep them at `suppress` unless the user decides otherwise with that consequence stated.
- Add entries with `suppressions add` or `suppressions import`; a bare domain blocks email to the whole domain and needs `--reason`.
- Every entry gets a CRM person record; `suppressions crm-backfill` covers older entries and previews until `--live`.

Company pause holds every lead at one company and resumes later, unlike do-not-contact: `sequences update <sequence> --company-reply-pause default` pauses a replier's colleagues, and `sequences pause-company --domain <domain>` (`--dry-run` previews) pauses a company on demand or from a Workflow. Details: [company pause](references/company-pause.md).

## Recovery

Every recovery path previews first, applies only to a paused Sequence, and keeps window, spacing, quota, suppression and cap checks.

- Ambiguous LinkedIn invite or message: pause, then `sequences reconcile <sequence> --action <id>`; `--approved` records an exact provider match and never resends. Send again only after reconciliation proves the provider refused it.
- Stale deferrals: `sequences retry-deferred` previews, `--approved` re-readies them; resume afterwards.
- Provider-capacity denials: `sequences recover-capacity` previews; apply that exact scope with `--approval-token <token> --approved`.
- `pause` and `resume` are reversible. To retire a paused Sequence, `sequences delete` previews and `--approved` deletes; nothing archives.
