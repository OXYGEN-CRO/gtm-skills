# Turn replies into booked meetings

## The Play
Every email and LinkedIn reply lands in one list with a suggested answer. You edit it, add your booking link, and it goes out only after your yes; calls booked through Cal.com then log themselves on the person's record in OXYGEN's CRM (its customer list). "Not now" replies go into a slow lane with a date to follow up, instead of being forgotten.

## Before You Start
- **A plan and credits for the connect.** Connecting a mailbox or LinkedIn account needs a paid plan, whatever the credits: on Free tell the founder "the smallest plan is $49 a month and includes 4,900 credits"; `oxygen billing change --to oxygen_49 --json` returns a link only they can confirm. On a plan, `oxygen billing estimate --mailboxes 1 --json` (free) says how the workspace pays for connected accounts: `"sender_billing": "credit_reservations"` means the connect needs `spendable_credits` (`oxygen billing balance --json`) of at least 100 for a mailbox or 3,400 for LinkedIn. Tell the founder: "Connecting your inbox reserves 100 credits a month from your balance."
- **Your mailbox.** Check `oxygen mailboxes list --json` (count 0 means none). Connecting reserves 100 credits a month, reply analysis included. If missing, steps 1-2 connect it.
- **LinkedIn (optional).** Check `oxygen senders list --json` (it lists LinkedIn accounts only). An account reserves 3,400 credits a month on the new pricing; `oxygen billing estimate --mailboxes 1 --linkedin-accounts 1 --json` quotes both for this workspace, free. If missing, tell the founder email works on its own.
- **Booking link.** Any Cal.com, Calendly or Google Calendar link books calls; only Cal.com bookings log themselves. Check `oxygen integrations connections --integration-id cal --json`, and ask the founder for their link.
- **Company context.** Check `oxygen context profile get --json` (company, offering, icp). If empty, suggested answers read generic: run day-1-first-win first.

## Steps
1. Register your mailbox and preview the connection — free. Write `./mailbox.csv` with the lines `email_address,provider,first_name,last_name` and `<your email>,google,<first>,<last>` (use `microsoft` for Outlook or Microsoft 365), then:
   ```bash
   oxygen mailboxes import --file ./mailbox.csv --json
   oxygen mailboxes connect-oauth --vendor composio --provider google --mailboxes <your email> --json
   ```
   Tell the founder: "Connecting your inbox costs 100 credits a month; you approve it on a Google or Microsoft page."
> APPROVAL GATE — inbox-connect: the mailbox, "100 credits a month until you disconnect it", and that its Inbox, Sent and archive history (not spam, trash or drafts) is imported; for LinkedIn too, the account and "3,400 credits a month".
2. Connect it — 100 credits a month.
   ```bash
   oxygen mailboxes connect-oauth --vendor composio --provider google --mailboxes <your email> --approved --json
   oxygen mailboxes sync <your email> --json
   ```
   The founder opens the consent link from the first line; the second shows the import (`sync.state` reaches `ready`). LinkedIn too (3,400 credits a month)? `oxygen senders connect --country <two-letter country> --inbox-scope all --json` returns a login link valid for 10 minutes; `--inbox-scope all` also brings in chats OXYGEN did not start.
   Tell the founder: "Your inbox is connected; replies now land in OXYGEN."
3. List the replies waiting on you — free.
   ```bash
   oxygen inbox list --status interested,neutral --unanswered --since <date 14 days ago> --json
   oxygen inbox get <conversation> --json
   ```
   Analysed conversations carry a suggested answer (`suggestedReply`; it is null until a conversation is analysed, and on threads triage judged need no answer); skip thank-yous and booking confirmations. A brand-new reply reads neutral until `oxygen inbox analyze <conversation> --json` classifies it (at most 1 credit; add `--channel linkedin` for a LinkedIn chat).
   Tell the founder: "These N people are waiting on an answer, newest first."
4. Write the answer and preview it — free. Start from the suggested answer, reply to their point in one or two sentences, and end with "Grab any time that suits you: <booking link>": `oxygen inbox send <conversation> --text "<answer>" --json`.
   Tell the founder: "Here is exactly what <name> will get."
> APPROVAL GATE — reply-send: recipient, channel, the sending mailbox or account, and the exact previewed text; send that text only after a yes.
5. Send it — 0 credits: `oxygen inbox send <conversation> --text "<approved answer>" --approved --json`.
   Tell the founder: "Sent from your own inbox; it shows in the thread."
6. Preview automatic booking logs — free, Cal.com only: `oxygen crm automation set crm-meeting-booked --armed --dry-run --json`. It writes nothing and returns `rule: null`; that is expected, not "no change", and it does not check Cal.com, so the switch-on in step 7 connects Cal.com first.
   Tell the founder: "When someone books through your Cal.com link, OXYGEN can log the meeting on their record and move them to the meeting stage."
> APPROVAL GATE — booking-log-arm: connect Cal.com and keep this on until switched off: every new Cal.com booking logs a meeting and moves that person to the meeting stage, free per booking.
7. Switch it on — free per booking.
   ```bash
   oxygen integrations connect cal --json
   oxygen integrations events enable --source cal --event booking.created --json
   oxygen crm automation set crm-meeting-booked --armed --live --approved --max-credits 1 --json
   ```
   The founder approves the Cal.com link from the first line, then pastes `setup.webhookUrl` and `setup.webhookSecret` from the second into Cal.com → Settings → Developer → Webhooks, trigger Booking Created. After a booking: `oxygen crm activity timeline people <attendee email> --json`. Booked through Calendly or Google Calendar? Mark the thread yourself: `oxygen inbox status <conversation> meeting_booked --json` (free).
   Tell the founder: "Cal.com bookings now log themselves."
8. "Not now" replies → a slow lane with a revisit date — free. Use it once `oxygen inbox list --status not_now --json` returns people. There is no one-step move from the inbox into a table yet, so add each person once by hand:
   ```bash
   oxygen tables create "Not now" --columns-json '[{"key":"email","label":"Email","dataType":"text"},{"key":"first_name","label":"First name","dataType":"text"},{"key":"company","label":"Company","dataType":"text"},{"key":"revisit_date","label":"Revisit on","dataType":"timestamptz"},{"key":"status","label":"Status","dataType":"text"}]' --json
   oxygen tables upsert not-now --key email --rows-json '[{"email":"<email>","first_name":"<name>","company":"<company>","revisit_date":"<YYYY-MM-DD>","status":"waiting"}]' --json
   ```
   Use the table slug the create reply returns. Date from their words: "next quarter" → the first day of next quarter; anything vague → 90 days out. Their campaign already stopped when they replied, and "stop emailing me" replies join the do-not-contact list on their own. Each week, list who is due and answer them as in step 4: `oxygen tables query not-now --filter-tree-json '{"type":"group","conjunction":"and","children":[{"type":"leaf","columnKey":"revisit_date","operator":"on_or_before","value":"<today as YYYY-MM-DD>"},{"type":"leaf","columnKey":"status","operator":"is","value":"waiting"}]}' --json`.
   Tell the founder: "These N people said not now; each has a date and comes back to you on it."
9. Optional: prepare a light email every 90 days for the lane — free. Write `./not-now-steps.json`:
   ```json
   {"steps":[{"id":"w1","kind":"wait","days":90},{"id":"t1","channel":"email","kind":"email_send","subject_template":"Something useful for {{company|your team}}","body_template":"Hi {{first_name|there}}, no ask, just <one useful fact or resource>. {{sender_first_name}}"},{"id":"w2","kind":"wait","days":90},{"id":"t2","channel":"email","kind":"email_send","subject_template":"Still worth revisiting?","body_template":"Hi {{first_name|there}}, has the timing changed? Either answer is fine. {{sender_first_name}}"}]}
   ```
   ```bash
   oxygen sequences create --name "Not now - quarterly touch" --slug not-now-touch --steps-file ./not-now-steps.json --channels email --table not-now --enroll --schedule-timezone <IANA time zone, e.g. Europe/Berlin> --schedule-days mon-fri --schedule-hours-start 09:00 --schedule-hours-end 17:00 --max-live-sends 100 --json
   oxygen sequences start not-now-touch --json
   ```
   Creating and enrolling send nothing; `sequences start` with no flags is the free launch check (who, what, when).
   Tell the founder: "Each person would get two short emails, 90 and 180 days after joining the lane."
> APPROVAL GATE — nurture-live: how many people, both emails as previewed, the sending mailbox, at most 100 sends, 0 credits per send; it keeps running until paused, and a first live start also switches on the free reply → CRM update for the workspace.
10. Start it — 0 credits per send: `oxygen sequences start not-now-touch --approved --max-live-sends 100 --json`. Later "not now" people: add their row, then `oxygen sequences enroll not-now-touch --from-table --json`.
    Tell the founder: "The quarterly touch is running."

## If It Goes Wrong
- `upgrade_required` on a connect → this workspace does not yet pay for sending in credits; see the credits bullet above. `sending_seat_required` or `insufficient_credits` on the LinkedIn connect → the message names the price or the shortfall; buying is the founder's call (`oxygen billing seats --json`).
- The connect preview skips your address with `mailbox_not_found` → it is not registered yet; run the `mailboxes import` line first.
- The list is empty while other reads in the same session fail (for example `tenant_migration_failed`) → the inbox could not be read; tell the founder that, not "no replies", and retry later.
- The list stays empty → the consent link is not approved yet or the import is still running (`oxygen mailboxes sync <your email> --json`); for LinkedIn chats run `oxygen inbox sync --json`.
- `oxygen crm automation rules --json`: `rules` lists only automations that were switched on at some point (some may be off again); `templates` lists every standing automation with its armed state, `crm-meeting-booked` included. Arm it by name as in step 7. `workflow_standing_authorization_required` → arming live needs `--approved --max-credits 1`.
- A Cal.com booking did not log → `oxygen integrations events deliveries --source cal --json`; no `webhook_event_dispatched` entry means Cal.com never sent it, so re-run the `events enable` line and paste the new URL and secret into Cal.com.
- `crm_object_not_found` on the timeline read → this workspace has no CRM yet: open https://oxygen-agent.com/crm once, then retry.
- `sequences enroll` skips someone as do-not-contact → anyone who replied on LinkedIn is on that list by default; follow up by hand as in step 4 on their date.
- A live start is refused for a missing send cap → add `--max-live-sends`; `--max-credits` is optional. The launch check is `sequences start <sequence>` with no flags; `--dry-run` switches the sequence on in test mode.
