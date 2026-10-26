# Read Sequence results

Every command here is a free read.

- `oxygen sequences stats <sequence> --json`: launch status kept apart from operational state, lifetime sent, failed and deferred counts, the funnel, today's budget and why work waits.
- `oxygen sequences analytics --range 30d --json`: every campaign in the window, with native email attribution under `analytics.emailAttribution` (`byMailbox`, `byDomain`, `unattributed`). `--sequence <sequence>` adds `senderPerformance` (results by sending person) and `messagePerformance` (each copy-bearing step variant). `--sender <key>` (repeatable) keeps chosen senders; keys come from the output's `senders` list. A per-day send series is `--sequence` with a `--range`.
- `oxygen sequences variants <sequence> --json`: the per-step action and variant rollup plus native email `by_mailbox` and `by_domain`, reply types and auto-winner state. It counts actions, so a base row can be a visit or an invite rather than copy.
- `oxygen sequences events <sequence> --json`: the per-lead activity ledger, newest first (`--kind sent,replied,bounced`, `--enrollment <id>`, `--before <iso>` to page). Email events carry `mailboxEmail` and `sendingDomain` when the evidence preserved them.
- `oxygen sequences contacts <sequence> --contact-state replied,positive_reply --json`: contacts by state (`not_contacted`, `contacted`, `connected`, `replied`, `positive_reply`), with `--exclude-contact-state`.
- `--opportunity-value <usd>` on create or update makes stats report pipeline value for positive replies; it never gates a send.

A fact without a preserved sender stays `unattributed`: report it as unknown rather than assigning it to a mailbox from the pool. Older replies without step or variant provenance stay in campaign totals, outside any message row.

Omit `--projection` to read all analytics sections in one call. For native value windows, `--path /analytics` selects the complete analytics object; `value_json` is escaped JSON text and `value_cursor` continues it losslessly. A cursor refuses changed live data. Restart the selection, or scope to one sequence; a fresh summary provides current single-item paths.

`oxygen dashboards summary` reads a windowed funnel alongside current inbox triage. `unreadReplies` counts current unread conversations across channels; `positiveRepliesWaiting` counts current interested email conversations. Neither triage count is restricted to the selected range. Domain `volume.outbound_30d` counts outbound messages from the synced inbox ledger, including mail outside Sequences; campaign attribution comes from Sequence analytics.

## Compact progress reads

For progress reviews, `oxygen sequences enrollments <sequence> --json` uses compact rows with invite state, failures and next-message timing. Follow `next_offset` for complete coverage; use `--full` for stored enrollment details. Discover a command with `oxygen commands search <goal> --json` and hydrate its exact name instead of loading broad help.

The enrollment response's `timezone` and `next_due.at_local` use the campaign's `settings.schedule.timezone`, falling back to UTC when no valid timezone is set. This labels the read's displayed times; channel sending windows and LinkedIn account working hours still govern dispatch.
