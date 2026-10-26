# Wind down mailboxes, domains or a workspace

Every path here previews first and executes only with the fresh preview's `plan_hash` and its exact confirmation.

## Before any approval, tell the customer

- Sending from the selected inboxes stops at once, and OXYGEN's credentials for them are cleared.
- The Google Workspace or Microsoft 365 accounts themselves are never deleted, and conversation, message and delivery history remains.
- The recurring lines that stop are listed in the preview (for example `mailbox_monthly_credits_stopped`); the current period is not refunded.
- Every Sequence that sends from these inboxes, by name: each keeps its status but loses these senders and is not paused automatically, so replace the sender or pause it.

## Delete mailboxes or domains

```bash
oxygen mailboxes delete --mailboxes sender@example.com --json
oxygen mailboxes delete --mailboxes sender@example.com --approved --plan-hash <plan_hash> --confirmation "<confirmation_phrase>" --json
oxygen domains delete send.example.com --json
```

- `mailboxes delete` removes exact inboxes from OXYGEN. An inbox whose own warm-up or monitoring is still connected fails closed with its teardown steps; `--cascade` (on the preview and the approval) disconnects those add-ons in the same delete. A live managed domain subscription covers other inboxes, so it needs the whole domain: `--include-domains` when every inbox on it is selected, or `domains delete`.
- `domains delete` removes domains with every inbox on them: inbox orders are cancelled, a domain bought through OXYGEN on its own stops renewing and stays registered until expiry, and a domain of your own is archived with its DNS and registrar untouched (`domains unarchive` restores it).
- Re-importing a deleted address restores its row but never its OAuth token: complete exact-account OAuth again.
- To stop cold email but stay on OXYGEN, use these deletes. `managed-inboxes exit` is for moving a domain to another provider.

## Managed orders: cancel or move

- `oxygen managed-inboxes cancel <domain> --json` itemizes the teardown (every line that stops billing, when the inboxes go dark, which live Sequences send from them); `--approved --confirm <domain>` cancels. The inboxes send until the paid period ends, and the domain stays registered until its term ends. Original-address recovery depends on provider eligibility; preview it with `oxygen managed-inboxes recover <domain> --json` ([recovery](managed-inboxes.md#recover-canceled-inboxes)).
- `oxygen managed-inboxes exit <domain> --json` is for transferring the domain: it stops OXYGEN's renewals and records a handoff while the domain, inboxes, DNS, warm-up state and data stay as they are. `--approved --confirm <domain>` records it; the receipt says `human_only: true` because a person completes the handoff with support. `--revoke` resumes renewals. If an exit reports a partial renewal update, preview and run it again: the retry repairs only the flags that did not converge.

## Leaving a workspace

`oxygen workspace infrastructure-exit --json` previews every renewing external resource with its release timing and the exact workspace confirmation and `plan_hash`; it is free and changes nothing. `--approved --confirm <workspace> --plan-hash <hash>` stops renewals and begins teardown under the paid terms; check the per-resource status until the exit completes. Records and history remain. The OXYGEN plan itself is separate: preview `oxygen billing cancel`.
