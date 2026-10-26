# Connect a customer's own Gmail or Microsoft 365 inbox

This connects a person's existing work inbox so its mail history appears in the Unibox and its business activity reaches the CRM. It is separate from buying or importing sending inboxes.

## Connect

```bash
oxygen mailboxes connect-oauth --vendor composio --provider google --mailboxes <address> --json
```

- `--provider microsoft` covers Microsoft 365, Exchange Online and Outlook. MCP: `oxygen_mailboxes_connect_oauth` with `dry_run: true`.
- Each owner consents individually; one run covers up to 10 registered addresses. Import an address first if it is not in the pool yet.
- The preview costs nothing and returns the recurring monthly price; quote it, or any mailbox count with `oxygen billing estimate --mailboxes <n> --json` (MCP `oxygen_billing_estimate`). Approve with `--approved` (MCP `approved: true`) only after the user accepts that recurring charge; each owner then opens their consent link and grants Composio's managed app access in Google or Microsoft.
- Warm-up is included in the mailbox's monthly connection once the mailbox is connected for sending; the warm-up preview confirms it per mailbox with `included_in_connection`.
- An unavailable managed Gmail connection is a support case. An unavailable managed Microsoft connection names `details.alternative`: OXYGEN's own sign-in, sending only, without history or CRM. Offer it and run `--vendor oxygen --authorization-mode individual` only if the user chooses it. A mailbox connected through the native `--vendor oxygen` path keeps its existing polling; full history and CRM analysis need this managed connection.

## Watch progress

`oxygen mailboxes sync <address> --json` (MCP `oxygen_mailboxes_sync_status`) is a free read: `sync.state` (`importing`, `ready`, `paused`, `disconnected`, `reconnect_required`), `messages_processed`, `pages_imported`, `history_completed_at`, `last_synced_at`, `crm_progress.messages_analyzed` and `messages_needing_review`. The mail itself: `oxygen inbox list --channel email --include-archived --json`; linked accounts: `oxygen unibox metadata --json`.

## What imports

Inbox, Sent and archive import in bounded pages; spam, trash and drafts stay out, and coverage already paid for is reused. Business mail creates contacts, companies and email activities, with summaries and intent in the Unibox; personal and automated mail stays in the Unibox only. Manual CRM values and company links are preserved, and ambiguous matches and deal or stage suggestions wait for review. History never triggers campaign reply actions.

## Control

`oxygen mailboxes sync <address> --action start|pause|resume|disconnect --json` (MCP `oxygen_mailboxes_sync`) previews; apply with `--approved` after review. Pause stops import and analysis. Disconnect also stops sends from that mailbox and future renewals of its commitment, with no refund for the current period; mail and CRM records remain, and paid seats or add-ons keep their own contracts.
