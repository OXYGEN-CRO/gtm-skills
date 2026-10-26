# Day 30: review, scale, or kill

## The Play

Once a month, the founder sees what the workspace's GTM work cost and what it brought back, then gives each campaign or automation that is still running one verdict: scale it (do more of it), change one thing, or stop it. Run it once something has been running for a few weeks; on day 1 there is nothing to review yet. Every read is free; the only paid step is an optional learnings summary at 1.5 credits.

## Before You Start

- **Something ran in the last 30 days:** `oxygen sequences list --json` (a campaign whose `startedAt` is set) and `oxygen runs list --limit 1 --json` (the newest run; something ran if its `createdAt` falls in the last 30 days; the full list is about 2 KB a run), both free. If neither, stop and tell the founder: "Nothing has run yet, so there is nothing to review. Start with the day-1-first-win or outbound-pilot-50 play and come back once a campaign has sent for a week."
- **About 2 credits for the optional summary:** `oxygen billing balance --json`, free; `spendable_credits`, after the list of plans, must cover 1.5. If it does not, skip step 4 and tell the founder the review still works without it.

## Steps

1. See what the month cost — free.
   `oxygen billing audit --days 30 --group-by category --json`, then the same with `--group-by category,provider` to name the provider inside each cost
   `totals.managed_credits_spent` is the month's spend. A `groups` row with `category` `admin` is a grant or an adjustment (`managed_credits_spent` 0), not spending; `oxygen billing usage --category admin --days 30 --json` names each one. In the `category` read, `groups` come biggest first, so the first two are the two biggest costs; `totals.fixed_credits_spent` is monthly charges for connected accounts, mailboxes and warm-up, and `totals.flexible_credits_spent` is enrichment, AI and automation. If anything is connected, `oxygen billing commitments --json` lists what each account reserves every month, used or not (LinkedIn 3,400 credits, an own mailbox 100).
   Tell the founder: "Last month cost N credits; most of it went to X and Y."
2. See what the campaigns brought back — free.
   `oxygen sequences analytics --range 30d --json`: messages sent, replies and positive replies, in total (`analytics.totals.funnels`) and per campaign (each row of `analytics.sequences`: `name`, `status`, `stats.sentByKind`, `stats.funnels.<channel>.replied` and `.positiveReplied`, `operational.failureAnalytics.terminalFailed`). The reply is long: add `--projection value --path /analytics/sequences` to read only the campaign rows, and read every row, paused ones included.
   `oxygen signals list --since 30 --json`: people who visited the site, viewed a profile, reacted to a post or followed.
   Tell the founder: "Campaign A sent 120 messages and got 6 replies, 2 of them interested."
3. Find what failed — free.
   `oxygen observability runs --status failed --limit 100 --json` lists the failed runs across tables and automations (the ones Home counts as "runs failed"). Its `counts` cover only the runs it scanned: if a `sources[]` row says `capped: true`, older failures exist beyond the window, so tell the founder how many Home counts and how many you could name; do not call either number wrong. Its message is generic, so read each cause one level down, with the id in the item's `decide_hint`: `oxygen table-ingestions items <ingestion_run_id> --json`: read `lastError.code` and optional `lastError.next_step`; `lastError.message` is fixed customer copy. For table-action items, use `oxygen table-runs items <action_run_id> --status failed --json` (`lastError.error.code` and `message`). Do not run the `retry-failed` hint during the review: a `table_ingestion_effect_unknown` request may already have completed (`retryable: false`), so retrying is the founder's separate decision. `oxygen runs get` shows no cause for these runs. Failed automations: `oxygen workflows runs --status failed --json`. Failed sends inside a campaign are its `operational.failureAnalytics.terminalFailed` from step 2; `oxygen sequences enrollments <sequence> --status failed --json` lists each failed lead with its latest error.
   Tell the founder: "2 runs failed because …; fixing them is a separate step."
> APPROVAL GATE — synthesis-run: one AI call for 1.5 credits; propose it only when step 2 shows sent messages or replies (with no enrolled leads, replies or recorded outcomes at all it returns `insufficient_evidence` and charges 0). The preview saves nothing; saving the reviewed text afterwards is free and writes an editable learnings page in the workspace notes.
4. Optional: summarize what the month taught — 1.5 credits, then free to save.
   ```bash
   oxygen knowledge synthesize --kind campaign_learnings --json
   oxygen knowledge synthesize --kind campaign_learnings --approved --body '<the previewed markdown>' --json
   ```
   Tell the founder: "Here is what worked and what didn't, saved to your workspace notes."
5. Decide one verdict for each running campaign and automation, and for each paused campaign that brought interested replies (resume it or leave it paused), and pick next month's play — free. Running automations are the `oxygen workflows list --json` rows whose `status` is `active`; the ones with a `cron` trigger run on their own.
   Scale when it brought interested replies or meetings at a cost the founder accepts: rerun its play with a bigger cap, under that play's own approval. Change one thing when it sent but few replied: the list, the message or the timing, one only. Stop when it cost credits or a monthly account fee and brought nothing. A campaign row's `creditsUsed` counts only its own sends (0 for LinkedIn and WhatsApp), and no read splits the month's spend by campaign, so judge cost by the step 1 fees of the accounts it sends from.
   ```bash
   oxygen knowledge log append --event decision --summary "<SCALE|CHANGE|STOP> <name>: <the number that decided it>; next: <action>" --json
   oxygen recipes list "<next month's goal>" --view summary --limit 6 --json
   ```
   Tell the founder: one line per verdict with its number, plus the one or two plays for next month.
> APPROVAL GATE — apply-verdicts: list each campaign to pause and each automation to switch off, with its name, the reason from step 5 and that it can be turned back on; run only the ones the founder approves.
6. Apply the stops the founder approved — free.
   ```bash
   oxygen sequences pause <sequence> --json
   oxygen workflows disable <workflow> --reason "<the review's reason>" --json
   ```
   `oxygen sequences resume <sequence> --json` undoes a pause. A monthly account fee from step 1's `billing commitments` keeps running after its campaigns are paused: name each connected account that brought nothing, with its monthly fee. Disconnecting it (LinkedIn: `oxygen senders disconnect <id> --json`) and deleting anything are the founder's separate decisions, outside this review.
   Tell the founder: "Paused X and switched off Y; nothing was deleted."

## If It Goes Wrong

- Every number is 0 and the only campaign is a draft → it is too early; stop as Before You Start says.
- `oxygen table-runs list` stops with `missing_required_option` → it reads one table at a time; use `oxygen runs list --json` for the whole workspace.
- Home shows "runs failed" without naming them → `oxygen observability runs --status failed --limit 100 --json`, then the item read from step 3 for each one; `oxygen runs get` shows no cause for table runs.
- `crm_object_not_found` from `oxygen signals list` → the workspace has no CRM yet, so no signals were recorded; report none and go on.
- `insufficient_evidence` from `oxygen knowledge synthesize` → there is nothing to learn from yet and 0 credits were charged; skip step 4.
- Charged twice for the summary → `--approved` without `--body` runs the AI again; save the previewed text with `--approved --body`.
- `oxygen billing usage` shows 50 events and `has_more: true` → that is the raw ledger; the totals are in the `oxygen billing audit` read from step 1 (pass `--days 30`; it defaults to a year).
- `cli_update_required` → run `oxygen update`, then rerun the command.
