# WhatsApp in the Unibox

WhatsApp runs on an unofficial linked-device connection, so every message acts on the person's own account.

## Start a chat

`oxygen inbox start-whatsapp --sender <account> --phone <+E.164> --text "..." --json` (or `--person-row-id <id>` for a CRM person) previews the exact recipient and first message; `--approved` sends it. A cold first message can increase the account's restriction risk: say so before approval. Many recipients or a cadence is a WhatsApp Sequence (`oxygen-sequencer`).

One message into a chat that already exists: `inbox send <conversation> --text "..."` (preview, then `--approved`), or `whatsapp warm-send`.

## History

The first history import can take a while: older, archived and group chats arrive after the provider syncs. `inbox list --channel whatsapp --include-archived` includes archived chats. `oxygen whatsapp history <chat>` backfills one conversation's full history (poll until `SYNC_DONE`); `whatsapp sync` refreshes account status only. Opening a thread with `inbox get` may fetch provider history and costs no credits.

## One conversation per person

A phone-number chat and a contact-id chat merge only when the provider confirms they are the same person on the same sender account. Merging happens during inbox sync and may also happen when a thread opens, so older duplicates can show until then. Sent and received messages share the merged conversation, old conversation links still resolve to it, and its `conversation.id` is the one to use.

## Forget a chat from OXYGEN

`oxygen inbox forget-whatsapp-chat <conversationId> --sender <senderAccountId> --before <ISO timestamp> --json` previews permanent removal of that chat, its messages and its reply drafts from OXYGEN. It needs a disconnected sender whose provider account has ended. Review the sender, recipient, date and counts, repeat with `--approved`, and read the Unibox back.

This removes data only from OXYGEN (`provider_deleted: false`); say exactly that. A copy in a connected WhatsApp account is a separate provider action: find `whatsapp.chats_delete` with `oxygen tools search` (MCP `oxygen_tools_search`), dry-run it with `oxygen tools run whatsapp.chats_delete --mode dry-run --connection-id <connectedId> --input-json '{"chat_id":"<providerChatId>"}'` (MCP `oxygen_tools_run_dry`), then run the approved live action (MCP `oxygen_tools_run_live`) and verify its result. A disconnected account cannot delete.
