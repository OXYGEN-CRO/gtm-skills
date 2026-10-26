# Journeys: branches, signals, variants and send windows

Step kinds, minimal step shapes and copy syntax are in `oxygen sequences create --help`. This page covers how a journey behaves once it runs.

## Reply-stop keeps follow-ups linear

Reply-stop is automatic and works across channels: an email, LinkedIn or WhatsApp reply ends that lead's enrollment before its next step, and a person takes over in Messages. Write follow-ups as a straight line (`msg1 -> wait -> msg2 -> wait -> msg3`). Branch on connection state, engagement, lead data or external signals. A branch that tests `*_replied` only ever sees people who have not replied, so it always takes its `else` arm.

## Branches

- Connection branches take a string condition and route with `then_id` / `else_id`: `already_connected` (resolved at entry), `connection_accepted` (waits up to `timeout_days` for the invite, then routes; on timeout to `else_id`, or stops when that is omitted) and `open_profile` (Open Profiles, which a free `inmail` step can reach).
- Signal branches take an object condition and route with `then` / `else`: a signal leaf `{ "signal": "company_raised_funds" }`, a data leaf `{ "has_column": "email" }` (true when that lead column is non-empty), `"present": false` to test absence, and `all` / `any` / `not` to combine. A data leaf decides at once, with no waiting.
- To cover leads with different data in one campaign, branch on a contact leaf `{ "has_contact": "email" }` (or `"linkedin"`, `"phone"`). It resolves the contact the way sending does: the mapped email/phone column with the built-in fallbacks, and the LinkedIn profile captured at enrollment. Prefer it to `has_column` for channel routing, and do not split one audience into a campaign per data shape: a lead without LinkedIn still enrolls when its email or phone reaches another step. Mapped CRM tasks also retain a lead with a stable `table_row_id` or `lead_provider_id`, even without email, LinkedIn or phone; CRM identities and properties are validated when planned. Each unavailable channel step is skipped.
- End each arm with a `stop` step, or both arms fall through into the same trailing steps.

## Waiting

- `wait`: `days` and/or `hours` (at least one hour in total); `jitter_hours` spreads a batch enrolled together so it does not fire in one burst. Days are calendar days unless `working_days: true`: then only the sending schedule’s allowed weekdays count, in its timezone, preserving local time across daylight-saving changes. Without a schedule, use Monday–Friday UTC. Hours and jitter still count elapsed time.
- `wait_for_connection`: advances when the invite is accepted; after `timeout_days` (default 14) `on_timeout` stops (default) or continues. Add `withdraw_on_timeout: true` to withdraw an unanswered invitation through the normal durable action path before applying that stop/continue policy. Withdrawal still obeys sender limits and safety gates; set this option while draft, before the first start.
- `wait_for_signal`: holds until a named signal is recorded on the enrollment; after `timeout_days`, `on_timeout` stops (default) or continues.

Engagement signals (`linkedin_connected`, `email_opened`, `email_clicked`, `email_bounced`, `meeting_booked`, call outcomes) arrive on their own. External signals (`company_hiring`, `company_raised_funds`, `job_change`, `new_hire`, `web_visit`, `intent`) arrive from a monitor, a Workflow, an Agent or you:

```bash
oxygen sequences signal <sequence> --signal company_raised_funds --enrollment <enrollment_id> --json
oxygen sequences signal <sequence> --signal new_hire --lead <lead_provider_id> --json
```

Recording a signal costs 0 credits and sends nothing; the next tick re-evaluates gates and branches under the same caps and windows. MCP: `oxygen_sequences_signal`.

## A/B variants, spintax and the auto-winner

- `variants` on a message, InMail, email or WhatsApp step holds up to 25 alternates of that step's copy: the base step is variant `a`, then `b`, `c` in order. Message and WhatsApp variants vary `template`; InMail `subject_template` and `template`; email `subject_template`, `body_template` and `body_html_template`, or only the body on an email without a subject. A field a variant cannot vary is not saved and the response names it under `warnings`. Each lead is assigned one variant deterministically, so a dry run shows the real split and a retry never changes it.
- `oxygen sequences render <sequence> --step <id> --json` shows each variant rendered for leads of the bound table (`--row`, `--sender` to choose), before anyone is enrolled.
- Spintax (`{Hi|Hey}`) varies wording inside one variant and is not tracked as a test.
- The auto-winner is on for every Sequence unless `--no-auto-optimize`: every step with variants is judged on replies, and once each active variant has 100 sends and 5 replies the ones converting below the leader pause. A step's own `auto_optimize` (`{ "metric": "reply" | "click" | "open" }`, optional `min_sends_per_variant` and `min_conversions`) changes that step's metric or thresholds; `click` and `open` need native tracking.
- `oxygen sequences variants <sequence> --json` shows each variant's results and the auto-winner's decisions. `--auto-optimize` runs it now on the whole sequence; `--pause`, `--activate` and `--reset` with `--step <id>` override it, one flag per call. The last active variant of a step cannot be paused. Every decision is reversible.

## Send windows

- One schedule for every channel: `sequences update <sequence> --schedule-timezone <tz> --schedule-days mon-fri --schedule-hours-start 09:00 --schedule-hours-end 17:00` (MCP `sending_schedule`). Without one, email sends weekdays 09:00-17:00 UTC.
- Separate LinkedIn invitations from messages/InMail per Sequence: `sequences update <sequence> --linkedin-invite-schedule '<window JSON>' --linkedin-message-schedule '<window JSON>'` (MCP: `linkedin_invite_schedule`, `linkedin_message_schedule`). Each window has timezone, ISO days, start and end; it replaces the general window for its action kinds. `null` restores inheritance. Web: Launch → Sending schedule → Advanced sending schedule. Account hours still apply; see [LinkedIn](linkedin.md).
- Email alone: `--send-window-file` with `{ timezone, days?, start, end, timezone_mode?, recipient_timezone_column? }`. `timezone_mode: "recipient"` sends in each lead's local time from that column, falling back to `timezone`. An `email_send` step's own `send_window` overrides it for that step.
- LinkedIn and WhatsApp alone: `--linkedin-timezone`, `--linkedin-days`, `--linkedin-hours-start`, `--linkedin-hours-end`. For LinkedIn this narrows each account's working hours; WhatsApp has no other hours limit.

## Reply-to-stop email footer

Set `oxygen sequences update <sequence> --reply-to-stop-text "Not the right person? Just reply and I won't follow up."` (MCP `reply_to_stop_text`) for an optional footer of at most 500 characters on first-touch emails only. An empty string clears it. In-thread follow-ups do not receive this footer. It is independent of the one-click headers and the automatic reply-stop above. With the visible unsubscribe on, plain-text emails show this line in place of the link, or a default opt-out line when it is empty.

## Changing a running Sequence

Journey structure, channels and the email binding are editable only in draft, so changed scope gets a fresh launch approval. A started Sequence, including one paused after launch, may change `days`, `hours`, `jitter_hours` and `working_days` on its existing `wait` steps (`sequences update --steps-file` with the same step IDs, kinds and order, MCP `definition`). Calendar-to-working-day changes are timing edits. Zero a delay instead of deleting its step, because enrollments track their position by index. Connection-wait fields (`timeout_days`, `on_timeout`, `withdraw_on_timeout`) remain draft-only after start; pausing does not unlock them. To change more, `sequences duplicate` (MCP `oxygen_sequences_duplicate`) makes a draft copy with the same settings and senders.

## Correcting variables after enrollment

Each enrollment keeps the campaign values captured at enrollment (`rowValues` in a full
enrollment read). The source Table and an enrolled lead can therefore show different values.

1. Read `oxygen sequences get <sequence> --json` for `status` and `sourceTableId`, then
   `oxygen sequences enrollments <sequence> --view full --limit 100 --json` for the exact
   `id`, `tableRowId` and `rowValues`. Follow `next_offset` with `--offset` when needed.
2. Compare that exact source row and only the fields you intend to change. Preserve deliberate
   enrollment overrides and fallback copy; an empty source cell is not evidence to erase one.
3. Before launch, while the Sequence is **draft**, edit the source row through the grid or
   `oxygen tables update <table> <row_id> --values-json '{"notes":"Reviewed notes"}' --json`.
   This shared row-edit path also updates the changed fields in pending enrollments that have
   no actions yet. Other fields remain intact. This is not a bulk import or column-run refresh.
4. Read the same enrollment back and use
   `oxygen sequences render <sequence> --row <row_id> --json` to inspect the result before launch.

After a Sequence starts, including while paused, source edits do **not** rewrite its saved
campaign values or queued messages. There is currently no supported customer command to
refresh those existing enrollment snapshots. Re-running `sequences enroll --from-table`
only adds unenrolled rows; it does not refresh existing leads. Do not remove/re-enroll a lead,
resume sending, or blanket-copy a Table row as a refresh workaround. For a launched campaign,
provide support with the Sequence ID, enrollment ID, source row ID, exact fields and reviewed
old/new values so a scoped correction can preserve journey progress, approved copy and history.

## Example: connect, then message, or InMail

```json
{
  "steps": [
    { "id": "invite", "kind": "invite", "note_template": "Hi {{first_name|there}}, {{opener}}" },
    { "id": "wait_accept", "kind": "wait_for_connection", "timeout_days": 7, "on_timeout": "continue", "withdraw_on_timeout": true },
    { "id": "connected", "kind": "branch", "condition": "already_connected", "then_id": "thread", "else_id": "open" },
    { "id": "thread", "kind": "message", "template": "{{message_1}}" },
    { "id": "pause", "kind": "wait", "days": 4, "working_days": true },
    { "id": "follow_up", "kind": "message", "template": "{{message_2}}" },
    { "id": "stop_thread", "kind": "stop" },
    { "id": "open", "kind": "branch", "condition": "open_profile", "then_id": "inmail", "else_id": "stop_rest" },
    { "id": "inmail", "kind": "inmail", "subject_template": "{{inmail_subject}}", "template": "{{message_1}}" },
    { "id": "stop_rest", "kind": "stop" }
  ]
}
```
