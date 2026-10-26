---
name: oxygen-unibox
description: "Use OXYGEN Messages and the Unibox to find, read, classify, tag, archive, draft and reply in existing email, LinkedIn and WhatsApp conversations, send one direct email, start one WhatsApp chat or delete a sent LinkedIn message. Net-new LinkedIn outreach uses Sequences."
allowed-tools: Bash(oxygen *)
---

# OXYGEN Unibox

The Unibox shows Messages across email, LinkedIn and WhatsApp with participants, delivery state and reply provenance. Every sent fact stays in Messages.

## Routing boundary

- Existing email, LinkedIn or WhatsApp thread: read and reply through the Unibox.
- New direct email without a cadence: Messages via the email-send gateway (`email send`).
- New one-to-one WhatsApp chat: `inbox start-whatsapp` ([WhatsApp](references/whatsapp.md)).
- New LinkedIn conversation, even one recipient/one step: Sequence (`oxygen-sequencer`).
- Cold, multistep, multi-recipient, sender-rotated, suppressed or reply-stop outreach: Sequence.

A reply in an existing thread stays a Messages reply sent through `inbox send`; turning it into a Sequence would restart outreach and bypass reply-stop.

Confirm with `oxygen capabilities search "<message goal>" --json`, then hydrate the exact `inbox`, `messages`, `email`, `reviews` or `agent` command.

Channel details: [email](references/email.md) (attachments, direct email, connected mailbox history), [LinkedIn](references/linkedin.md) (inbox scope, history backfill, deleting a sent message), [WhatsApp](references/whatsapp.md) (new chats, history, merged chats, forgetting a chat).

Before drafting a LinkedIn reply to outreach, or a Sequence's first message: [DM conversion](references/dm-conversion.md) (routes, the buyer's second message, anti-patterns).

## Triage loop

1. Query a bounded slice: `oxygen inbox list --channel <channel> --status <keys> --since <iso> --json`. The default list is the merged email, LinkedIn and WhatsApp stream. `--search` is fuzzy across every non-warmup conversation, archived and sent-only threads included.
2. Read the thread (`inbox get <conversation>`) and the relevant CRM and Knowledge context before classifying or drafting. `messages query` reads stored messages without refreshing anything from the provider.
3. Classify, tag or archive. `inbox bulk --action <action> --ids <ids>` previews the matched and changed counts; `--yes` applies them. Tags use the shared workspace Tags vocabulary.
4. Draft the reply and show the exact channel, account, thread, recipients and content.
5. Send only after explicit approval: `inbox send <conversation> --text "..."` previews, `--approved` sends. Return the message and conversation deep-links.

Read the filters for what they are:

- `--unanswered` means the last message is theirs. It also keeps thank-yous and automated mail, so it is not a needs-a-reply queue; add `--sequence-id` for replies to your outreach.
- Statuses come from AI reply triage and mean sales intent, so "who showed interest" and "who said no" are filters, never a script over `--json`: `inbox list --status interested`, `--status not_interested`; `inbox labels list` gives the keys. `interested` includes thank-yous and booking confirmations, and `neutral` can hold real questions. A reply that just arrived reads `neutral` until analyzed: `inbox analyze <conversation>` classifies it now. Each mailbox's scope (`mailboxes update <mailbox> --classify replies|all`) decides which email triage classifies, at credits each: `replies` covers Sequence threads and threads you wrote in, so newsletters stay unclassified. `--segment primary` leaves out the negative tier (`not_now`, `not_interested`, `lost`, `bounced`); `--segment all` keeps every ordinary conversation. `--sequence-id` scopes to one email campaign and leaves out DMs.
- In `--json`, `count` is the rows on this page; email's `total_conversations` and `sidebar_counts` are mailbox-wide and ignore your filters.
- `--sender-profile-id <ids>` keeps one person's conversations: their own inboxes and LinkedIn/WhatsApp accounts (`unibox metadata` lists each sender profile and its id). `inbox mark-all-read` takes it too.

## Saved views

A sales team saves the filters it works in as named Unibox views, shared with the whole workspace: `inbox views list`, then `inbox views create --name "Anna" --filters "sender_profile_id=<id>&channels=linkedin"` (a Unibox URL or `inbox list` params; without `segment` a view opens on the Primary tab, `segment=all` on every conversation). Each member's `--default` is their own and is what their Unibox opens on; `inbox views update <view> --no-default` returns them to every conversation. Deleting a view removes it for everyone, so confirm with the user first.

## Drafts and agents

Stored drafts: `inbox drafts list` (email and LinkedIn) and `whatsapp drafts list`; MCP reads them through `oxygen_capabilities_read`, and personal composer drafts stay private. The reply agent (`inbox reply-agent get|set`) writes drafts a person approves and sends; each draft it writes costs credits once it is enabled. The AI Inbox Tagger (`inbox auto-tagger get|set`) applies tags from an allowlist you set. A generated draft is a reviewable fact; sending it is the same approved `inbox send`, with `--draft-id` to mark it sent.

## Guardrails

- Messages owns every reply in its threads: send through `inbox send` or `email send`, never through raw provider actions.
- Bulk actions show their count and scope before they apply.
- When a send outcome is ambiguous, inspect the message and run provenance (`inbox get`) before any retry.

When replies are not turning into meetings, or "not now" leads need bringing back, open the [reply-to-meeting](plays/reply-to-meeting.md) play first.
