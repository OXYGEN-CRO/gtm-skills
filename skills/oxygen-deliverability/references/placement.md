# Placement tests

A placement test sends one probe from a connected sending inbox to seed inboxes and reports which folder it landed in. It is directional evidence about that sender and that content, not recipient verification.

## Read saved results first

```bash
oxygen deliverability placement-test list --view summary --json
oxygen deliverability placement-test get <test-id> --json
```

Both cost 0 credits and never create or send a test; active tests may refresh. `list` also returns `pricing`: the monitoring price per inbox-month, the tests included per inbox per cycle and the price of an extra test. The allowance resets at the start of each UTC calendar month; unused tests do not roll over. `managed_test_credits` applies without subscription coverage and `managed_extra_test_credits` applies after the included allowance is used: equal values describe the same unit price, not two charges. Own-key tests do not consume this managed allowance. `get` returns the status, seed counts, per-provider results and a web link to that exact result. To confirm whose test it was, match `oxygen mailboxes get <sender-email> --json` against the test's `mailboxIds`.

Filter inventory with `--status incomplete` (also pending_send, sending, awaiting_results, completed or failed), and pass the response's `next_cursor` as `--cursor` with the same filter until null. Changing the filter requires restarting without a cursor. `count` is the returned page size; `total` and `status_counts` cover all matching tests before the cursor. This is a live history, so status changes during traversal can change matches. Omit `--view summary` for full rows, or use `get` for one test's seeds. MCP uses `oxygen_placement_tests_list` with the same `status`, `cursor`, `limit` and `view` fields.

In compact history, `seed_count` counts allocated seed addresses, not received messages. A saved report can contain observations without an allocated-address list. `creditsUsed` retains the recorded original cost; `results.refund` (summary: `refund`) records restoration, not an additional charge. The refund follows the attributable captured ledger charge, which can differ from the recorded cost. Use the receipt for the amount restored; test rows alone do not establish net wallet spend. Current pricing does not reprice older tests.

## Run a test: OXYGEN deliverability (default)

OXYGEN deliverability is the default provider for every sending inbox. Creating a test and sending its probe are two separate approvals, and a zero-credit preview authorizes neither. Respect the test limit the preview states.

```bash
oxygen deliverability placement-test run ada@send-acme.com --json
oxygen deliverability placement-test run ada@send-acme.com --approved --plan <plan_hash> --max-credits <credits_required> --json
oxygen deliverability placement-test send <id> --json
oxygen deliverability placement-test send <id> --approved --plan <plan_hash> --json
oxygen deliverability placement-test get <id> --json
```

1. `run` without `--approved` is a cost preview (`credits_required`; 0 while the managed cycle's included tests last; own-key tests pay the quoted OXYGEN platform fee separately from provider-account charges).
2. `run --approved` creates and charges the test and returns its seeds and filter phrase. No email has left yet.
3. `send <id>` previews the exact sender, every recipient and the phrase-bearing content with a fresh `plan_hash`.
4. `send --approved` sends that one message through the inbox's own transport, at 0 additional credits.
5. Poll `get`. A test in `pending_send` needs step 3 and 4; polling alone produces nothing.

A send that fails after delivery began is ambiguous: OXYGEN records `outcome_unknown` and never retries it. Reconcile the inbox's sent folder and the test before any new probe.

Use realistic prospect outreach: supply actual campaign `--subject` and `--body` at creation. New tests without copy preview a realistic business email; do not claim it represents a different campaign. Put `{{placement_test_phrase}}` where the mandatory matching identifier belongs, for example `Reference: {{placement_test_phrase}}` after the signature. New tests add that neutral reference when absent; send preview resolves it without a test-labelled footer. Historical tests retain frozen rendering. Review the exact copy before approval.

## Diagnose a paused inbox

Preserve campaign pauses. With explicit approval for one diagnostic, add `--allow-paused-probe` to all four OXYGEN deliverability create/send preview and approval commands above. Both hashes bind that permission; a test created without it cannot gain it at send time. Preview names exact recipients/content; the paid creation still needs its quoted credit ceiling. This queues one probe without changing status, pause evidence or caps. Disabled or unauthorized inboxes remain blocked, ordinary sends remain blocked, and a placement score never authorizes resume. This flag is available only for the two-stage native diagnostic.

## Run a test: Zapmail (Zapmail-hosted inboxes)

Zapmail tests only inboxes hosted on the connected Zapmail account. It is used when OXYGEN deliverability is not connected for the workspace, or with `--provider zapmail`.

- `placement-test run <inbox> --provider zapmail --json` previews; `--approved --plan <hash> --max-credits 0` lets Zapmail compose and send the probe itself in one step. On the customer's own Zapmail account it costs 0 OXYGEN credits and draws on their Zapmail plan.
- Results arrive in 2 to 24 hours; `awaiting_results` is pending, not evidence. Poll the saved test, minutes apart, and keep to one test per question: one Zapmail key has a small shared request budget.
- `zapmail_wallet_insufficient` (402) means no test started: pass the returned checkout link to the account owner and wait until the wallet is topped up. `zapmail_mailbox_not_eligible` means the inbox is not on that Zapmail account: use OXYGEN deliverability.

## OXYGEN placement evaluation (limited pilot)

The `--provider oxygen_placement` option is available only for the eligible connected sender enabled for this pilot. It is never selected automatically and permits one 0-credit test. Supply `--subject` and `--body` when previewing `placement-test run`; approval requires the preview's `plan_hash` and `--max-credits 0`. Approval creates and sends the probe in one step, with no separate `send` approval. Poll `get` for the result. Summary values with unverified units are shown as recorded, without conversion; per-seed counts are labelled separately.

## Read results

- Counts describe only the tested seeds and content. A vendor health score is not an inbox percentage.
- A low, isolated score is a reason to look closer, not to pause: corroborate with repeated tests, domain authentication and blocklist evidence, and the bounce and reply trend.
- Keep OXYGEN Warm-up telemetry separate from a content-specific placement test; their windows and calculations differ.
- No health provider connected: `mailboxes health` and `placement-test run` return 409 with a readiness hint. A managed-provider refusal belongs to OXYGEN support; stop before creating a test.

## Partial and incomplete reports

Read the existing test before buying another. Active seed observations can change in the final report. `seed_progress.pending` lists addresses without observed delivery, including on terminal reports; the test status describes report completion. Verified per-seed observations appear while a report is pending; a seed with no observation is unknown, not proof of a bounce or spam placement. OXYGEN deliverability tests close as incomplete two hours after confirmed seed send unless a final read yields a valid complete report. Incomplete reports keep available observations but have no overall score. The worker refunds the captured managed test charge exactly once, or restores an included allowance; own-key tests receive no OXYGEN test-credit refund. Read the test's refund receipt before claiming credits were restored. Other placement providers keep their own completion windows. Never resend or buy a replacement automatically, and never omit allocated seeds.
