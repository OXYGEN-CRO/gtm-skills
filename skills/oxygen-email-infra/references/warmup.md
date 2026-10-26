# OXYGEN Warm-up

OXYGEN Warm-up is the managed warm-up service for sending inboxes. Warm-up authority is separate from native-send authorization: importing an inbox adds it to the pool without buying warm-up, authorizing campaign sends or enabling monitoring, and warm-up never authorizes a Sequence send.

## Which inboxes are not sending (start here)

Ask the pool, not each inbox:

```bash
oxygen mailboxes list --stalled                # enrolled, nothing ever sent
oxygen mailboxes list --next-action fix_dns    # blocked on a DNS record the customer owns
oxygen mailboxes list --warmup paused,error    # stopped, whatever stopped them
```

The plain output lists counts first, then every inbox that owes an action with its cause and exact command. `--warmup` takes `warmupTruth.state` values and `--next-action` takes `next_action.code` values; they combine with each other and with `--status` and `--tag`. `--json` adds `summary.warmup` (`enrolled`, `stalled`, `needs_action`, `by_truth_state`, `by_next_action`); MCP `oxygen_mailboxes_list` takes `warmup`, `next_action` and `stalled`. Counts across every state and cause at once: `oxygen mailboxes health --json` (`warmup.byState`, `warmup.byCause`). Filter on the server: a silent inbox billed for weeks is easy to miss in a full JSON dump.

## Keep a warm standby reserve

Standby inboxes keep their existing warm-up running while pending outreach is held. Marking an inbox standby does not enroll, restart or buy warm-up, and does not cancel its connection or warm-up charges. Read current warm-up billing separately before changing a subscription.

```bash
oxygen mailboxes standby pool --json
oxygen mailboxes standby get --mailbox <mailbox-id-or-address> --json
oxygen mailboxes standby set --mailbox <mailbox-id-or-address> --role standby --json
oxygen mailboxes standby set --mailbox <mailbox-id-or-address> --role standby --approved --plan <plan> --json
```

Preview and apply both require mailbox write access (sequence write access for campaign opt-in). These commands use an unapproved call for preview, not the generic `--preview` flag. The unapproved role change previews the exact address and affected campaigns without writing. Review its outreach hold with the user, then echo the returned `plan` with `--approved`. Use `--role outreach` with the same preview/approval flow to return an inbox to outreach. In Accounts → Email, **Keep on standby** and **Use for outreach** are available in an inbox's Settings and the selected-inbox bulk bar.

`standby pool` reports `minimum_days`, `ready_count`, per-inbox `confirmed_days`, readiness blockers and replacement history. Reserve readiness is assessed after an inbox is kept on standby. An outreach inbox without an assessment has `assessment_status: not_assessed` and `confirmed_days: null`; a newly selected standby inbox shows `pending` until its first check. Existing confirmed warm-up days carry over; selecting standby does not restart the count. `assessment_observed_at` dates the evidence; stale assessments may retain historical days without proving current readiness. The default is 14 confirmed warm-up sending days; elapsed calendar days do not count. After the user chooses a different threshold, set it with `oxygen mailboxes standby policy --minimum-days <1-28> --json`. Missing or stale evidence, unverified enrollment, stopped warm-up, failed DNS, missing authorization, a safety pause or a missing sender profile blocks readiness.

Each campaign opts in separately through `oxygen sequences standby set --sequence <sequence-id-or-slug> --enabled --json`, then the same command with its reviewed `--plan <plan> --approved`. Review the reserve's real sender names and signatures: replacements may belong to another person. The email reference in `oxygen-sequencer` owns the contacted-lead and safety behavior. MCP equivalents are `oxygen_mailboxes_standby_pool`, `_get`, `_set`, `_policy` and `oxygen_sequences_standby_get` / `_set`; arguments match these flags (`mailbox`, `sequence`, `role`, `minimum_days`, `enabled`, `plan`, `approved`). Standby reads and configuration consume 0 credits; current subscriptions continue.

## Enroll

A fresh managed-inbox order activates warm-up after provisioning without a second approval only when its approved quote carries `warmup_activation.automatic_after_provisioning=true`, the exact future addresses, the ramp, the recurring price and the credit ceiling. That approval covers those addresses only; no other inbox is swept in.

Every other inbox uses the standalone path:

```bash
oxygen mailboxes compatibility --mailboxes ada@send-acme.com --json
oxygen mailboxes warmup enable --mailboxes ada@send-acme.com --json
oxygen mailboxes warmup enable --mailboxes ada@send-acme.com --approved --plan <plan_hash> --max-credits <max_credits> --json
```

The first `warmup enable` is a no-write preview naming the eligible and blocked addresses, the ramp, the recurring price (or `included_in_connection: true` when the inbox's monthly connection covers warm-up), the `plan_hash` and the first-cycle ceiling. Only the matching approved call hands credentials over or starts billing; the user may also continue without warm-up. The ramp completes after 28 days on which the provider confirmed a warm-up send (days with no confirmed send extend it); a paid inbox then keeps warming at up to 10 a day, billed monthly, until you disable it. Dedicated Azure/Entra tenants keep their lower domain-density limit during maintenance (2 per inbox per day at 100 inboxes on one domain). `--ramp-weeks <n>` only spreads the volume climb. `warmup status` shows `ramp.confirmed_sending_days` of `ramp.required_sending_days` and `ramp.phase` (`ramp`, then `maintaining`). One preview covers at most 220 inboxes.

How each inbox gets its credential:

- Google with a compatible app-password import: the encrypted credential from import is used at enrollment, with no second Google login.
- Google connected through OXYGEN’s managed Composio connection: preview `oxygen mailboxes warmup enable --mailboxes <address> --json`. When available, its target shows `handoff: composio_gmail_bridge` and `mailbox_access: standard_mailbox`. Explain that approval permits warm-up to send, read and organize mail through the existing connection; disabling warm-up revokes this access. No second Google consent is needed. If the preview says this path is unavailable, contact OXYGEN support; do not start a different Google authorization.
- Other Google without a source credential: connect the exact inbox to OXYGEN first, then preview `oxygen mailboxes warmup google --mailboxes <address> --json`. Approve its fresh plan with `--approved --plan <plan_hash> --max-credits 0`, let that inbox's owner open the returned Google link, and poll the same command with `--status`. Google shows the warmup provider's application. No native grant or password transfers; setup neither enrolls nor charges warmup. After consent, preview `warmup enable` separately.
- Imported Microsoft: each mailbox owner completes one OXYGEN Warm-up Outlook authorization from `oxygen mailboxes warmup microsoft` (preview, approve with `--max-credits 0`, open each link, poll with `--status`). Passwords are never used, and one mailbox's consent never covers another. `consent_state: consent_stalled` means a requested consent was never completed (link expired, or no confirmation after 48 hours; see `stalled[]`): approve the command again.
- OXYGEN-managed Google, Microsoft or Azure: no password and no warm-up login; OXYGEN hands the inbox over itself.

One inbox warms on one network. A warm-up still running at another provider blocks enrollment: cancel it there (or ask support for a managed inbox), then preview again.

## Read warmupTruth

Every inbox in `mailboxes list --json`, `mailboxes warmup status --json` and `oxygen_mailboxes_list` carries `warmupTruth`, the authoritative reading; the bare `warmupState` is only the stored token and reads `error` for a provider-paused seat.

- `state`: `warming`, `active`, `paused`, `error`, `disabled`, `pending`, `not_enrolled` or `unknown`, with a one-sentence `label`. A `pending` row carrying an older provider token is not enrolled: preview `warmup enable`.
- `last_send`: the later of the last campaign send and the last warm-up send, with its `precision`; `source: none` ("Never sent") means nothing ever left the inbox. Only an exact warm-up timestamp proves a recent successful send.
- `pause.origin`: `breaker` (OXYGEN stopped a runaway dispatch; `code` and `label` explain it), `vendor`, `human` or `none`.
- `dispatch`: `attempted` counts tries and `sent` counts mail that left, so many attempts with few sends is an authentication or runaway problem, never a deliverability rate. Totals may include an earlier ramp: compare against a dated baseline before claiming recovery. `dns_score` must be 80 or more to dispatch, and `dns_failing_records` names what failed.
- The legacy `warmupMetrics.daily[].sent` field counts attempts at OXYGEN Warm-up; use `warmupTruth.dispatch.sent` and an exact warm-up timestamp for successful sending. Neither successful sending nor a vendor inbox-rate counter proves inbox placement.
- `billing.status`: `active`, `past_due`, `cancelled`, `none` (no live subscription), `unavailable` (the ledger read failed) or `not_checked`. `pending` with a `hold` is a first enrollment still holding reserved credits: recover it with the enrollment preview, which separates `total_monthly_credits`, `additional_credits` and the `reserved_credits` being recovered and never charges a second first cycle.
- `warmupRepair.mode: automatic`: OXYGEN is repairing this exact inbox at 0 credits on bounded attempts (`nextAttemptAt` is the next try, not a success). Wait for it before suggesting a manual command.

## Next actions

`next_action` gives a `code` and, when one exists, the exact `command`:

- `resume_warmup`: `oxygen mailboxes warmup resume --mailboxes <address>` after reviewing the pause. It changes state, has no preview, creates no subscription and charges nothing; skip it during a read-only investigation.
- `reconnect_warmup`: `oxygen mailboxes warmup reconnect --mailboxes <address>` pushes a Google credential again at 0 credits (re-import a changed credential first). On a managed InboxKit seat whose sends keep failing it replaces the seat through a fresh native export; the ramp restarts at day 1. If it reports the export unresolved, run it once more after a minute to adopt the new seat.
- `reactivate_warmup`: `oxygen mailboxes warmup reactivate --mailboxes <address>` asks the service to re-check a Microsoft consent seat at 0 credits and restarts a warm-up the service stopped, from its first ramp day. If the tenant blocks sign-in (for example SMTP AUTH switched off), its administrator unblocks it first.
- `enable_warmup`: preview `mailboxes warmup enable` for an inbox that is not enrolled.
- `fix_dns`: correct the named record at its DNS host. OXYGEN re-checks eligible paid seats on a schedule, and the status shows `resume` as the command when a manual re-check is needed. The ramp keeps its position, and a cycle with zero sends is not billed.
- `connect_oauth`, `wait`, `contact_support`, `none`: follow the label; `none` proposes nothing and proves no fresh send. Quote the reason for `wait` rather than predicting a pause from old counters.

## Lifecycle

- OXYGEN refreshes warming and error rows by itself. For read-only diagnosis use `oxygen mailboxes get <address> --json`: `warmup status` persists state and may pause a runaway, and `warmup reconnect` replaces the connection.
- Approval binds the exact inboxes, credential revision, ramp, price and cap; any change returns `plan_stale`, so preview again.
- An unclear answer from the service keeps the credit hold until OXYGEN knows whether enrollment happened; a failed attempt is never charged twice.
- `mailboxes warmup pause|resume|disable` act on the recorded connection. `disable` removes the inbox from warm-up and cancels its recurring line, so repair a seat with `reconnect` or `reactivate` and keep the subscription.
- Enrollment requires the provider's ramp to match the approved settings and the destination's DNS to be ready. A warming status or a rising ramp day proves nothing was sent: check attempts, sends and the last-send time.
- Daily charts refresh a few inboxes at a time; a missing or stale chart is not evidence of zero sends.

## Settings

Standard warm-up starts at 1 email a day, adds 1 a day and levels off at 10, the rate a paid inbox keeps after its ramp; dedicated-tenant profiles stay stricter. This is separate from the campaign ramp (`mailboxes ramp set`). `oxygen mailboxes warmup config <mailbox> --json` reads the effective plan for free. An override sets all four knobs (`--initial-per-day`, `--increase-per-day`, `--max-per-day`, `--reply-rate`); OXYGEN Warm-up applies the three volume knobs and saves the reply rate without applying it. `--reset` restores the defaults, and an active warm-up syncs without re-enrollment.

Mailboxes still on the retired TrulyInbox rail are read with `oxygen mailboxes warmup status --provider trulyinbox --json` and can only be paused, resumed, configured or disabled there, each after the user approves that exact scope; disabling ends that enrollment and its subscription, while pausing alone keeps billing. A customer's own TrulyInbox key gives no authority over managed enrollments.

Mailbox monitoring and placement tests are separate products with their own approval: the `oxygen-deliverability` skill.
