# LinkedIn steps and account safety

This is the one LinkedIn account-safety reference: Signals captures, Publishing and Messages follow the same rules. The numbers a campaign plans with (default caps, ramp, notes, kill lines, follow-ups, pending invites) are in [outreach defaults](linkedin-volume.md).

## Tell the customer first

LinkedIn's User Agreement restricts automated activity, and LinkedIn can warn, limit, restrict or close an account at its discretion. OXYGEN is not affiliated with LinkedIn. Everything a connected account does (invites, messages, likes, comments, team amplification, network capture) acts on that person's account through a third-party connectivity provider; caps, spacing, working hours and warm-up reduce the risk of a restriction without removing it. Say this plainly before arming any of it, and describe LinkedIn automation as lower-risk, never as safe, risk-free or zero-risk.

Data from the managed scraper does not use the customer's account: a named supplier listed at https://oxygen-agent.com/subprocessors collects it, and the customer controls how they use that personal data. The sentence to relay: "This does not use your LinkedIn account; the data is collected by our named supplier, and you decide how to use it lawfully."

## Choose the surface by whose data it is

| Data | Surface | Cost | Account used |
| --- | --- | --- | --- |
| A third party's profile, posts, company, engagers, people search | Cookieless `scraper.*` operations and harvests (`oxygen-signals` skill) | Credits, quoted live | None |
| Your own network, followers, viewers, own-post engagers, inbox | Connected-account captures and reads | Free | Metered read budgets |
| Mutual connections with one profile | Non-notifying `linkedin.users_get` (`notify:false`); `unavailable` is not zero | Free | One metered read |
| Invites, messages, InMails, posts, comments, reactions | Sequences, Publishing, engagement commands | Free sends | Metered send budgets, approval-gated |

Connected accounts read what they own plus narrow relationship context only their session can expose. Third-party research is bought cookieless with credits: routing it through a connected account to save credits is the pattern that gets accounts restricted.

## Connect an account

```bash
oxygen senders connect --country DE --json
oxygen senders connect --country DE --count 5 --owner-consent --json
```

- `--country` is required for a new account: the owner's normal LinkedIn login country, not the campaign target or the client's headquarters. Only the 56 countries OXYGEN has LinkedIn proxies in are accepted; any other is refused with `linkedin_country_unsupported` and the supported list, so pick the closest one. OXYGEN pins the account's automatic proxy to that country and verifies it after connect; owners in different countries need separate commands.
- Each link connects one account, is valid for 10 minutes and is free to re-mint. Send it to the person who owns the LinkedIn account: they sign in themselves (2FA goes to them, no password sharing) and the account lands in this workspace's `senders list`; no OXYGEN login is needed. The account also gets its sender profile automatically: the person who already owns another connection of the same LinkedIn member, else the active profile with the same name and no live LinkedIn account, else a new profile named and pictured from LinkedIn (`senders profiles list`); a reconnect keeps its current profile. Treat every link as sensitive and keep its owner association. `--count` above 1 (up to 25 per call) or `--share-link` needs `--owner-consent`, because each owner connects their own account. Web: Connections, Get shareable link.
- `--sales-nav` requests Sales Navigator too, only for an account with an active subscription. `--cookie-auth` adds cookie login and `--custom-proxy` lets the owner enter their own proxy in the hosted wizard; OXYGEN receives neither the cookies nor the proxy credentials. `--established` skips the warm-up ramp for a real, aged profile.
- A new account shows only chats OXYGEN started (`--inbox-scope all` opts into the whole inbox): the `oxygen-unibox` skill, `references/linkedin.md`.
- `connection.safety` reads `verified` or `warning` (proxy missing or mismatched, a proxy outside the requested country, verification unavailable, a requested product not running); review a warning before using the sender. A missing proxy, a country the provider never accepted, or a proxy parked in another country because none was free at home pauses the sender and its Sequences (`auto_pause.reason: proxy_safety` in `senders health`). Each connect and `senders sync` asks the provider for the home country again; `oxygen senders proxy-country <id> --country <cc>` (web: account menu, Proxy country) moves the proxy without a reconnect, and a clean check lifts the pause.

## Metered, fail-closed quota

Every LinkedIn call from any surface (CLI, MCP, table columns, Workflows, inbox sync, background drips) claims the account's daily quota before it runs. Reads have their own budgets apart from sends, and background drips draw on separate, slower ingest budgets, so a big import spreads over days; one inbox sync spends about 30 message reads. A refused call returns `linkedin_rate_limited` with the exhausted limit and `resets_at`: wait for that time or raise that one limit, and leave retry loops out. A table run that hits the limit defers its rows and resumes after the reset instead of failing.

## Limits

`oxygen senders limits get <id> --json` reads the account's current limits, working hours, defaults, hard maximums and caution levels; `senders limits set --help` lists every limit flag with its default and maximum (values above a maximum are clamped). `senders health <id> --json` shows today's usage, effective caps, warm-up day and quota reset.

- Above a caution level the restriction risk rises. Raise a cap past it only for replies people asked for (a post whose commenters all want the same resource), with the user's go-ahead and that risk stated first, together with lower `--min-spacing-seconds` and `--spacing-jitter-seconds`. Cold outreach stays at or below the caution levels.
- Working hours default to 07:00-22:00 every day in the account's timezone; work due outside them is deferred, not failed. A Sequence schedule can narrow them, never widen them.
- Saturday and Sunday halve the daily send caps in the account's timezone (posts, reads and human Unibox sends keep theirs); `senders limits set <id> --weekend-full-volume` opts out.
- A withdrawn invitation blocks re-inviting that person from the same account for 21 days: the invite is refused with `linkedin_reinvite_cooldown` and `resets_at`, and a Sequence defers that lead, keeping its sender.
- `--randomize-caps` varies the daily caps between 80% and 100% so volume is not identical every day.
- Each kind of action is spread across the working hours with its own clock, and any two automated actions keep the minimum spacing. Direct tool runs, table columns and Workflow tool calls get that spacing but no daily spread.

## Two lanes

Everything above governs the automated lane: Sequences, CLI and MCP calls, table columns, Workflows and Agents, all authenticated by token. A person typing in the web Unibox is the human lane: exempt from working hours and the daily message cap, bounded by its own hourly ceiling (`--interactive-sends-per-hour`). An agent's reply through `inbox send` is always automated. When spacing refuses it, the slot in `resets_at` is held for replies until `slot_held_until`, so send it again inside that window rather than in a loop.

## Warm-up

A newly connected account ramps its invite and message caps over about two weeks unless it is connected as established (`senders connect --established`, or the web "Established account" box); mark real, aged profiles established. While an account warms, the ramp caps those two limits whatever you set. `senders limits set` controls it: `--warmup-preset conservative|standard|fast`, `--warmup-restart`, `--warmup-disable`, `--warmup-start-date <iso>` to credit earlier warming. Network capture has its own read ramp (`--read-warmup-disable`). A reconnect never restarts the ramp.

## One person, one sender

- The first real send to a person (invite, message or InMail) binds that person to that account for the whole workspace; every later enrollment routes them back to it. Profile visits never bind.
- An unbound lead goes to the attached sender with the fewest active enrollments.
- A lead bound to a sender outside the Sequence's pool is skipped as `bound_to_other_sender`. Add that sender to `--senders`, or accept the skip. `--ignore-sender-bindings` is for the case where the user explicitly accepts that the person may hear from a second account.
- `--sender-failover rebind` moves untouched enrollments to a healthy sender after a confirmed outage; the default `wait` resumes on recovery.

## LinkedIn steps

- `--senders` takes LinkedIn account ids attached directly, besides the `--sender-profiles` people's own accounts; a journey with LinkedIn steps needs one to enroll or start. It replaces the directly attached set, `--senders ""` removes it, and `sequences get` names every account under `sender_pool`. A Sequence made with the web's New sequence starts with no senders (2026-10-12), so `sequences enroll` refuses with `sequence_no_senders` until one is attached. The web keeps leads imported before then in the Sequence's table and enrolls them when its Senders stage adds a sender with a LinkedIn account; after attaching senders from the CLI, run `sequences enroll <sequence> --from-table`.
- Leads need a LinkedIn URL in the bound table (`--linkedin-url-column-key`, or `linkedin_url`, `profile_url` and similar). A bare public handle with a hyphen or digit works and is echoed in `linkedin_handles_canonicalized`; every unusable row is named in `unresolved_linkedin_lead_details`. In a LinkedIn + email journey a row with no profile but an email still enrolls for the email steps and is named in `linkedin_unavailable_lead_details`; tell the customer its LinkedIn steps will be skipped, a connection wait passes at once and a connection branch takes its not-connected path. The profile URL is snapshotted from the row at enrollment without a LinkedIn provider lookup, so adding a URL to the row later does not add those steps; the URL has to be in the row before the lead is enrolled. Live dispatch resolves that URL against LinkedIn; a dry run makes no LinkedIn provider calls. The reverse also holds: a lead with a profile but no recipient email skips each `email_send` step (`skipped_reason: no_recipient_email`).
- A `--leads-file` lead with a `lead_profile_url` and no `table_row_id` is filed into the Sequence's leads table, the one bound or a new one, onto the person's existing row, also under another spelling of the same URL (only its empty cells are filled), so the campaign's Contacts view lists it; a person the Sequence already holds keeps that enrollment; like any table-row lead it cannot re-enroll in that Sequence once its enrollment ends. With no table where every new table needs a client signoff the enroll is refused (`sequence_leads_table_needs_signoff`): put those people in a signed-off table and enroll them with `--from-table`. `leads_without_table_row` counts leads given only a `lead_provider_id` and people the Sequence already holds without a row.
- Per-step senders: invite, message, InMail and withdraw steps share one `sender_profile_id` or none, because one account owns each conversation; visits, follows, likes and comments may each name anyone selected.
- `comment_post` with `ai_prompt` generates the comment at send time, a paid AI call; keep a `text_template` as the fallback.
- Network Mining workspaces (dev): `invite` and `message` also take an `ai_prompt`, drafted at send time in the sender's voice (paid). Each draft must pass an automatic check (no placeholder, no sender named in the third person, LinkedIn length) or the `note_template`/`template` fallback goes out; with no fallback the step is skipped (`ai_draft_check_failed`). Preview the drafts before launch with `oxygen sequences standing-approval <seq> --draft-samples --max-credits <n>`. To like, comment on and DM focus leads when they post, see [Engage](network-mining-engage.md).
- `open_profile` routes Open Profiles to a free `inmail` step.

## Health is a precondition

Check `oxygen senders list --json` and `senders health <id> --json` before any motion. A sender in `credentials_required`, `restricted` or `disconnected` refuses metered calls (`linkedin_account_unavailable`) and silently stalls Sequences and drips: sends to a sender that is not `active` defer, and table runs fail fast without burning retries. `oxygen senders sync --json` refreshes status and profile and lists per-account `results` and `warnings` (every account failing is `linkedin_accounts_sync_failed`). Repair the account with `senders connect --reconnect <id>` or `senders checkpoint solve <id> <code>`.

## Seats and disconnects

A connected account carries a monthly charge on its billing owner. Connecting one needs the billing owner's paid plan; on Free the connect returns `upgrade_required` with `upgrade_url`. `oxygen billing estimate --json` names how a plan pays for it: `credit_reservations` uses the owner's credits; legacy `sending_seats` uses purchased or grandfathered dollar seats. A linked client uses its owner's model and funds. `oxygen billing seats --json` shows held seats and next-connection eligibility (paying-seat coverage may be unknown); `oxygen billing commitments --json` shows account reservations. A connect the balance cannot cover fails with `insufficient_credits` and a `details.next_step` top-up. Sends themselves cost 0 credits.

OXYGEN hands the provider seat back, keeping every conversation, message and run, when the account is disconnected (`senders disconnect`), the workspace ends or, on legacy `sending_seats`, its paid plan ends, the provider reports it stopped or failed to create, it stays unhealthy for 7 days, or the same profile is connected again. On `credit_reservations`, losing a paid plan alone does not disconnect an account funded by its reservation. A seat is never released while another workspace still has that account connected and active. Connecting a profile that is already connected makes the new connection the account: the older one shows `disconnected` with `superseded_by`, and its Sequences and open enrollments move across without pausing. Coming back after a release is one `senders connect`; `--reconnect <id>` on a released account mints a fresh link.

Ambiguous invites and messages: reconcile before any resend (`SKILL.md`, Recovery).


## Separate invite and message schedules

In each Sequence, Launch → Sending schedule → Advanced sending schedule sets independent invite and message/InMail windows. Each replaces the general Sequence window for its action kinds; account working hours, safety caps and pacing still apply. Other LinkedIn actions, email and WhatsApp keep their existing windows. Existing Sequences inherit the general window.

CLI: `oxygen sequences update <sequence> --linkedin-invite-schedule '{"timezone":"Europe/Berlin","days":[1,2,3,4,5,6,7],"start":"09:00","end":"17:00"}' --linkedin-message-schedule '{"timezone":"Europe/Berlin","days":[1,2,3,4,5],"start":"10:00","end":"16:00"}'`. Pass `null` to either flag to restore that action's general window. MCP `oxygen_sequences_update` takes the same nullable objects as `linkedin_invite_schedule` and `linkedin_message_schedule`. Read back `sequences get` → `sending_schedule.linkedin_invites` and `linkedin_messages`; these include effective windows and their stored source. These settings do not launch or send anything.
