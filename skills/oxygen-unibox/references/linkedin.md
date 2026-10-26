# LinkedIn in the Unibox

## Inbox scope

LinkedIn visibility is set per sender account. New accounts default to `oxygen_initiated`: only chats OXYGEN started are ingested and shown, and inside such a chat only messages from the first successful OXYGEN send onward. Unrelated LinkedIn conversations stay out of OXYGEN. `all` opts into the full LinkedIn inbox and is the account owner's explicit choice; switching back to `all` restores access to retained history. Accounts connected before this setting existed keep `all` until it is changed.

- Read or change it: `oxygen senders inbox-scope get <id> --json`, `senders inbox-scope set <id> --scope oxygen_initiated|all`. The change costs no credits, triggers no provider sync and sends no message.
- Restricted scope relies on the chat id recorded when OXYGEN created the chat, so a chat counts as OXYGEN-started only with that record, however outbound it looks.

## Sync and older history

New LinkedIn messages arrive in real time. `inbox sync` forces a backstop sync for LinkedIn and WhatsApp accounts. `inbox backfill` opts one account (or all) into a slow drip of older history under its own read budget, filling over days; `--cancel` stops it and keeps what arrived. Neither sends anything or costs credits.

## Replies and links

A LinkedIn reply through `inbox send` runs on the automated lane and counts against the account's message cap; a person typing in the web Unibox is the human lane (account safety: `oxygen-sequencer` skill, `references/linkedin.md`). `--attach <url>` adds up to five public URLs.

## Delete a sent LinkedIn message

1. Read `oxygen inbox get <conversation> --channel linkedin --json` and find the exact outbound message. Use its OXYGEN conversation and message UUIDs, not provider ids. Only the connected account's own messages with a known send time in the last 60 minutes qualify.
2. Preview: `oxygen inbox delete-message <conversationId> <messageId> --json` (MCP `oxygen_inbox_delete_message` with `approved: false`). Show the sender, recipient and message, and that removal is permanent for everyone; get approval for that exact message.
3. After approval, repeat with `--approved` (MCP `approved: true`). Deletion costs 0 credits. Provider limits and account pacing can still refuse it, and an expired window means the message stays.
4. `deleted: true` confirms it; `already_deleted: true` means it was gone before. Read the thread back: the message keeps its place as a "Message deleted" tombstone (`isDeleted: true`) without its text or attachments. With `unibox_mirrored: false`, report the confirmed LinkedIn deletion and the pending inbox sync, and keep the conversation link.
