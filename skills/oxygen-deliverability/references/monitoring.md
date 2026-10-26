# OXYGEN deliverability mailbox monitoring

OXYGEN deliverability monitors connected sending inboxes and runs their placement tests. Connecting an inbox stores its IMAP/SMTP account at OXYGEN deliverability; it sends no email and creates no placement test. Monitoring has a recurring price per inbox and cycle that includes a number of tests; read both from the preview and `placement-test list` (`pricing`). Monitoring connection previews on the customer's own OXYGEN deliverability key quote 0 OXYGEN credits; placement-test calls have the separately quoted OXYGEN platform fee plus any provider-account charge. Included managed tests reset each UTC calendar month and unused tests do not roll over.

## Connect inboxes

```bash
oxygen mailboxes deliverability connect --mailboxes ada@send-acme.com --json
oxygen mailboxes deliverability connect --mailboxes ada@send-acme.com --approved --plan <plan_hash> --max-credits <max_credits> --json
```

- The preview reads only whether the inbox's encrypted credential exists and its revision, plus OXYGEN deliverability capacity; it decrypts nothing and writes nothing. It returns `per_inbox_credits`, `total_monthly_credits` and the `plan_hash`.
- Approval binds the exact inboxes, credential revision, OXYGEN deliverability workspace, account name, price and capacity. A batch that cannot fit every account fails before any credential is sent. Managed credits are reserved before the external write.
- Google Workspace inboxes need a real app password, used only after approval. Microsoft 365 and InboxKit Azure inboxes are `vendor_blocked`: OXYGEN deliverability exposes no Microsoft OAuth or tenant consent, and OXYGEN never falls back to password authentication. Their placement tests still run without a monitored account.
- Warm-up never hands its credential or connection to OXYGEN deliverability; the two connect separately.
- `outcome_unknown` or `billing_pending`: retry the same connect flow so OXYGEN reconciles the original account and credit hold; a second account or hold is never the fix.
- A refusal of the platform authentication mapping is a support case: send the inbox and refusal code, and keep the customer's credentials as they are.

## Standing auto-enrollment

```bash
oxygen mailboxes deliverability auto-enroll --json
oxygen mailboxes deliverability auto-enroll --arm --max-credits <per-cycle-ceiling> --json
oxygen mailboxes deliverability auto-enroll --arm --max-credits <per-cycle-ceiling> --approved --json
oxygen mailboxes deliverability auto-enroll --run --dry-run --json
oxygen mailboxes deliverability auto-enroll --disarm --json
```

- Arming is a standing authorization for a recurring per-inbox charge, so it needs `--approved` and a per-billing-cycle credit ceiling. It is off until armed, and a missing or unusable configuration reads as off.
- Once armed, OXYGEN enrolls new eligible inboxes hourly in batches of ten under that ceiling; `--run` enrolls a batch now and `--run --dry-run` shows what it would enroll and why the rest is skipped. Before each renewal, check that the ceiling still covers the intended inboxes.
- `last_sweep_at` stays `null` until the hourly sweep reaches the workspace; `last_sweep.error` names a run that could not happen.
- Every skipped inbox carries a `reason` (vendor-blocked, out of budget for the cycle, deferred to a later batch), counted in `skip_summary`. An inbox waiting on OXYGEN's own managed capacity appears once under `platform_condition` (`owner: "oxygen"`) instead: OXYGEN is alerted and the sweep enrolls it when capacity returns, with nothing for the customer to do. Only a customer's own OXYGEN deliverability connection can raise its own quota.
- `--disarm` turns it off at once without approval; existing subscriptions continue.

## Disconnect

`oxygen mailboxes deliverability disconnect --mailboxes <address> --json` previews; `--approved --plan <plan_hash>` deletes exactly that OXYGEN deliverability account, confirms it is gone and only then cancels the monitoring line. A lost delete stays `outcome_unknown` with billing active until absence is proven; `billing_pending` after a successful delete means preview the disconnect again rather than deleting anything by hand.
