# LinkedIn outreach volume, ramp and kill lines

The numbers a LinkedIn campaign is planned with. Disclosure, quota mechanics, caution levels, weekend caps and health: [LinkedIn steps and account safety](linkedin.md). Quote the account's live values from `oxygen senders limits get <id> --json`; an owner may have changed them.

## Daily budget

| Limit | Default per account |
| --- | --- |
| Invites | 20 a day, 100 a week |
| Messages | 40 a day |
| Profile views | 50 a day |
| Profile lookups | 80 a day |
| Pending-invite withdrawals | 10 a day |

Budget profile reads, not invites: they run out first, and LinkedIn allows only about 100 profile retrievals a day. A lead known only by profile URL costs a lookup before its first send, and each `already_connected` branch reads the profile. Enroll by member id (`lead_provider_id`, the `ACo…` value) whenever the table holds it.

## Ramp for a new account

| Days since connect | Invites a day | Messages a day |
| --- | --- | --- |
| 0–2 | 5 | 5 |
| 3–6 | 10 | 15 |
| 7–13 | 15 | 30 |
| 14 on | account caps | account caps |

This is the `standard` preset; other presets and `--established`: [linkedin.md](linkedin.md), Warm-up.

## Connection notes

Send invites without a note on every signal play and put the words in the message after acceptance. Preview refuses a note over 200 characters (`linkedin_invite_note_too_long`): LinkedIn refuses longer notes from accounts without Premium, and OXYGEN cannot see the tier.

## Kill lines

- **Campaign:** 14 days after the 50th invite, read `oxygen sequences stats <sequence> --json`. `stats.acceptanceRate` is a fraction of `stats.connectionRequestsSent` that counts pending invites, so it reads low while invites are young. Below 0.30, `oxygen sequences pause <sequence>` and re-check the audience and its qualification before resuming.
- **Account, automatic:** over 30 days, under 15% acceptance after 30+ invites, or under 2% replies after 50+ messages, or a checkpoint in the last 14 days, halves the send caps; two restrictions in 30 days pause the account once OXYGEN has sent 20+ invites and messages from it. `oxygen senders health <id> --json` shows the tier.

## Follow-ups

- Signal plays: at most one nudge, 5–7 days after the message (a `wait` step, then a `message` step), then stop. A reply ends the enrollment first.
- Existing network: no automated follow-up; follow up by hand in the thread (`oxygen-unibox` skill).

## Pending invites

Every active sender withdraws its pending invites once they are 21 days old, at most 10 a day, with no setup. A `wait_for_connection` step with `withdraw_on_timeout: true` withdraws when its `timeout_days` end. To clear invites now, `oxygen linkedin invitations withdraw --older-than <days> --account <ref> --json` previews the list and `--approved` withdraws it. A withdrawn person then sits out the re-invite cooldown ([linkedin.md](linkedin.md), Limits).
