# Email steps

Native email sends through the workspace's connected Google and Microsoft mailboxes (Gmail API, Microsoft Graph or Microsoft SMTP transport). Mailboxes, domains, DNS, warm-up and sending authorization belong to the `oxygen-email-infra` skill; this page covers how a Sequence uses them.

## Who sends

- Every inbox belongs to a sender profile, one person's name and photo across their inboxes and LinkedIn and WhatsApp accounts. `--sender-profiles <ids>` gives each lead one of those people, and that person's inboxes send the lead's emails.
- Per step: `email_send.sender_profile_id` sends from any inbox of one person; `sender_mailbox_id` pins one inbox. An email whose From changes, including a return to the lead's original inbox, needs its own `subject_template`.
- `--mailboxes <ids>` limits a Sequence to an allowlist of inboxes instead of the whole pool.
- `oxygen sequences preview <sequence> --json` (a read; the same preview as `sequences start` without `--approved`) shows `sender_journey`: each step's From and how a lead's inbox is picked.

## Threading

`subject_template` decides threading: a step with its own subject starts a new email; a step without one replies in the lead's previous thread as `Re: <previous subject>`. The first email step needs a subject.

## Capacity and pacing

Daily capacity is each inbox's cap times the sendable inboxes, inside the sending window. Defaults: 25 per inbox per day, at least 12 minutes apart, weekdays 09:00-17:00 UTC until a sending schedule is set; a new inbox ramps 5, 10, then 20 a day over its first sending days.

- Per inbox: `mailboxes cap set`, `mailboxes ramp set` (custom ramp, `--off`, or `--clear` for the standard one). `mailboxes get <mailbox>` reads today's `effective_cap` and the ramp schedule. Provider warm-up traffic is separate (`oxygen-email-infra`).
- Per Sequence: `--max-emails-per-mailbox-per-day`, `--max-emails-per-day` (Sequence-wide, counting every channel's sends; `none` removes it), `--max-new-enrollments-per-day` (first touches; `none` removes it), `--email-min-gap-minutes`, and `--sequence-prioritization followups|new_leads` for a tight budget. MCP takes `null` to remove a cap.
- Spacing is the window divided by the cap, never closer than the minimum gap. A step due outside the window waits for the next opening.
- `sequences stats` shows today's sends, reservations, remaining capacity and why work waits (`outside_send_window`, `mailbox_spacing`, `daily_send_cap_reached`).

Schedules, including each recipient's own timezone: [journeys](journeys.md).

## Provider routing

`--esp-matching prefer` (default) favors an inbox on the recipient's own provider and falls back to any; `off` rotates freely; `strict` defers when no same-provider inbox exists. `--esp-routing-file` replaces the whole policy, e.g. `{"routes":{"google":{"microsoft":100}}}` sends to Google-hosted recipients from Microsoft inboxes. Routing applies to the first touch. `sequences esp <sequence>` estimates routing against active workspace mailboxes (DNS lookups only, 0 credits). A narrow `--mailboxes` allowlist plus `strict` can starve sends. The enroll response's `esp` block labels this inventory with `pool_scope: workspace_active_mailboxes`: `matchable` counts leads on Google, Microsoft or neither, and `strict_deferred_leads` estimates deferrals against that inventory. These estimates omit sequence mailbox/sender-profile restrictions, readiness and daily limits; zero deferrals does not guarantee readiness. Review `sequences preview` for the selected senders before launch.

## Bounce protection

A hard bounce stops that lead (`--no-stop-on-bounce` keeps it running) and adds the address to do-not-contact under the `email_hard_bounce` rule. Each Sequence pauses itself when hard bounces exceed 3% of accepted sends over a rolling 7 days once it has at least 20 sends, and warns above 2%; tune with `--bounce-protection '{"pause_rate":0.03}'`. This pauses the Sequence, not the fleet; inbox-level bounce protection is separate. Resume only after cleaning the list; the pause is protecting the inboxes.

## Automatically replace paused inboxes

Automatic replacement is off by default for each campaign. It uses the workspace's shared warm standby reserve when **mailbox-level bounce protection** pauses an inbox; a campaign-wide safety pause remains in force.

```bash
oxygen sequences standby get --sequence <sequence-id-or-slug> --json
oxygen sequences standby set --sequence <sequence-id-or-slug> --enabled --json
oxygen sequences standby set --sequence <sequence-id-or-slug> --enabled --approved --plan <plan> --json
```

Review the preview's reserve, actual sender names and signatures with the user before applying its returned `plan`. A replacement can belong to another person and uses its own identity for uncontacted leads. Contacts already emailed stay pinned to their original inbox, their follow-ups wait while it is paused, and incoming replies remain collected. A step pinned to an exact inbox stays held for review; an uncertain prior send is never replayed as a replacement.

`standby get` shows ready reserve capacity and waiting or completed replacements. With no ready reserve, sending waits; Oxygen does not buy an inbox or start paid warm-up. Replacement preserves sending caps, ramps, schedules and suppression. The paused inbox stays paused until manually repaired. Disable future replacement through the same preview flow with `--no-enabled`; existing replacements then stop serving this campaign until it is enabled again.

MCP: `oxygen_sequences_standby_get` and `oxygen_sequences_standby_set`, with `sequence`, `enabled`, `approved` and `plan`. Configuration and reads cost 0 credits and change no subscriptions. For standby roles, readiness thresholds and warm-up costs, read the `oxygen-email-infra` warm-up reference. In the app, use **Automatically replace paused mailboxes** in the campaign's sending settings.

## Tracking

Open and click tracking are off by default. `--tracking-opens` and `--tracking-clicks` opt in and need a verified tracking domain (`oxygen-email-infra`, domains). An open pixel adds spam-filter surface, and the reply metric works without tracking.

## Unsubscribe

Off by default. `--include-unsubscribe` adds a visible opt-out and one-click headers to first-touch cold emails; follow-ups in a thread carry neither, and Zapbox inboxes carry the link only. HTML emails show a short Unsubscribe link. Plain-text emails never show the signed URL: they end with the `--reply-to-stop-text` line, else "Not interested? Just reply and I won't follow up." Any reply stops the lead in that Sequence, and opt-out wording such as "not interested" adds them to do-not-contact by default (`email_optout_phrase`). On `sequences update`, `--include-unsubscribe-link` and `--include-unsubscribe-headers` switch each half alone. `--reply-to-stop-text` sets the per-sequence first-touch line; an empty string clears it. An unsubscribe click adds the person to do-not-contact (`email_unsubscribe_click`).

## External campaigns

Rows for a campaign already running in Smartlead, Instantly, lemlist or HeyReach, and a native email track bound to an Instantly campaign: [external campaigns](external-campaigns.md).
