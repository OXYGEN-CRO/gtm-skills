# Email in the Unibox

Email replies are polled automatically, so new replies reach `inbox list` without a sync command. An email reply goes out from the thread's own mailbox, threaded.

## Attachments

```bash
oxygen inbox send <conversation> --channel email --text "..." --attach ./proposal.pdf --json
```

- `--attach` is repeatable: local PDF, DOCX, XLSX, PPTX, TXT or CSV files, up to five and 10 MiB in total.
- Without `--approved` the command uploads the files and returns a preview that names them; rerun it with `--approved` to queue the email, then read its delivery status with `inbox get`. An upload unused for 24 hours expires for new sends.
- MCP: call `oxygen_inbox_attachment_upload` with the email conversation, filename and base64 bytes, then pass each returned `file.id` in `attachment_ids` to `oxygen_inbox_send`: first with `approved: false` to inspect the named attachments, then `approved: true` after the user approves.
- Files travel only on email from a native Gmail or Microsoft mailbox. A mailbox sending through Zapbox refuses attachments (`attachments_unsupported_transport`), and WhatsApp takes none. LinkedIn takes public URLs ([LinkedIn](linkedin.md)).

## One direct email

`oxygen email send --to <address> --subject "..." --body-file ./body.txt --json` previews the exact mailbox and transport; `--approved` sends one email. `--from <mailbox>` pins the mailbox, otherwise the pool rotation picks one. A cadence, several recipients or reply-stop is a Sequence (`oxygen-sequencer`).

## Connected mailbox history

A customer's own Gmail or Microsoft 365 inbox can import its history and business activity into the Unibox and CRM. Connecting it, its price and its controls belong to the `oxygen-email-infra` skill (`references/connect-mailbox.md`). Progress is a free read: `oxygen mailboxes sync <address> --json` (MCP `oxygen_mailboxes_sync_status`); linked accounts: `oxygen unibox metadata --json`.
