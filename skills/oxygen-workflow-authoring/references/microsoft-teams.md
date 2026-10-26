# Microsoft Teams notifications

Use this for Teams destination discovery and outbound Teams notifications. Teams (`microsoft_teams`) runs on the customer's own Microsoft 365 consent through an OAuth connection, so it bills 0 OXYGEN credits.

Teams is **send-only**: there is no inbound Teams event, no Teams webhook and no Teams workflow trigger. Teams is also not a Messages channel; there is no Teams inbox.

## When To Use

- The user wants a Teams channel or chat notified when something happens in Oxygen.
- A workflow should post a positive reply, a run summary, or an approval prompt into Teams.
- The user needs the raw Microsoft Graph `team_id` and `channel_id` GUIDs a Teams send step requires.

## Destination Discovery

`team_id` and `channel_id` are opaque Graph GUIDs. Resolve them, never ask the user to find them by hand.

```bash
oxygen integrations connect microsoft_teams --json
oxygen integrations destinations microsoft_teams --json
oxygen integrations destinations microsoft_teams --team-id <team_id> --json
oxygen integrations destinations microsoft_teams --kind chats --json
```

`oxygen integrations destinations microsoft_teams` lists teams; adding `--team-id <team_id>` also lists that team's channels. It is a free read-only lookup — no `--approved`, no `--max-credits`. Use `--connection-id <id>` when several Teams connections are active. It answers `microsoft_teams_connection_required` when Teams is not connected; connect first, then re-run.

Two destination shapes: a **channel** needs `team_id` plus `channel_id`; a **chat** (1:1, group, or meeting) needs `chat_id`. With no `--kind` the command lists teams and chats; add `--team-id` for that team's channels, or `--kind teams|channels|chats` to narrow it to one lookup.

Microsoft returns every team in the tenant, not only the ones the connected account has joined, and channels are readable only for joined teams. Expect the team list to be much longer than the usable set, and expect a `Forbidden` on the channel lookup to mean "this account is not a member of that team" rather than a failure. Confirm the destination with the user by team and channel name before sending.

Chats are named by their topic, which meeting and group chats have and one-to-one chats do not — Microsoft keeps the counterpart's name on chat members this lookup does not return. An unnamed chat is therefore labelled by type, like `Direct chat · f9126f7a`. Never guess which person a direct chat belongs to; if the user needs one, have them confirm it or use a named group or channel instead.

## Before Writes

```bash
oxygen integrations actions microsoft_teams --json
oxygen tools search microsoft_teams --json
oxygen tools get composio.microsoft_teams.teams_post_channel_message --json
```

Send actions:

- `MICROSOFT_TEAMS_TEAMS_POST_CHANNEL_MESSAGE` — post into a team channel (`team_id`, `channel_id`, `content`).
- `MICROSOFT_TEAMS_TEAMS_POST_CHAT_MESSAGE` — post into a 1:1, group, or meeting chat (`chat_id`, `content`); resolve the chat with `oxygen integrations destinations microsoft_teams --kind chats`.
- `MICROSOFT_TEAMS_TEAMS_POST_MESSAGE_REPLY` — reply inside an existing thread.

Read actions `MICROSOFT_TEAMS_TEAMS_LIST` and `MICROSOFT_TEAMS_TEAMS_LIST_CHANNELS` are what the destination lookup runs for you.

Ad-hoc sends go through `oxygen integrations run`, which gates every live integration action, reads included, behind `--approved` and a positive `--max-credits` of at least 20. Teams still bills 0 credits; the cap is a ceiling, not a price. That is the asymmetry to remember: `integrations destinations` needs no approval because the server runs a fixed pair of allowlisted read lookups, while `integrations run --live` always does. Dry-run is the default; inspect it, then re-run with `--live`.

```bash
oxygen integrations run microsoft_teams MICROSOFT_TEAMS_TEAMS_POST_CHANNEL_MESSAGE --input '{"team_id":"<team_id>","channel_id":"<channel_id>","content":"Test post from Oxygen"}' --json
oxygen integrations run microsoft_teams MICROSOFT_TEAMS_TEAMS_POST_CHANNEL_MESSAGE --input '{"team_id":"<team_id>","channel_id":"<channel_id>","content":"Test post from Oxygen"}' --live --approved --max-credits 20 --json
```

Destructive Teams actions exist (`MICROSOFT_TEAMS_DELETE_TEAM`, `MICROSOFT_TEAMS_ARCHIVE_TEAM`). Keep them out of recipes and workflows; run them only on an explicit, specific request.

## Notify Pattern

"Notify Teams when X happens" is an ordinary Workflow, not a Teams feature: an Oxygen trigger plus a Teams send step.

1. Pick the trigger from Oxygen's own catalog with `oxygen workflows events list --search "<outcome>" --json`, then `oxygen workflows events get <catalog_id> --json` for the exact trigger object. Sequence and CRM events are the usual sources; Teams never triggers anything.
2. Resolve the destination with `oxygen integrations destinations microsoft_teams --team-id <team_id> --json`.
3. Add a `composio.microsoft_teams.teams_post_channel_message` external-write step with `team_id`, `channel_id`, and `content`; pin `connection_id` when several connections exist.
4. Lint and apply: `oxygen workflows lint --file <path> --json`, then `oxygen workflows apply --file <path> --json`.
5. Inspect deliveries with `oxygen workflows runs --workflow <workflow> --json`.

Normal workflow metering and revision-bound approval still apply even though the Teams call is no-bill, and a provider-declared failure fails the step.

`oxygen sequences workflows configure sequencer-positive-reply-teams` is a legacy compatibility preset kept only for workspaces that already have one configured. Do not create new Teams notifications there; build the workflow above instead.

## Approval Checklist

- Connected Microsoft Teams account, and which connection when several are active.
- Exact `team_id` and `channel_id` resolved from `oxygen integrations destinations`, not typed by hand.
- Message content and the events that will produce it.
- Expected delivery volume — a per-reply notification fires as often as replies arrive.
- Failure and retry behavior for the send step.

## Stop Conditions

- Teams is not connected (`microsoft_teams_connection_required`).
- Destination GUIDs are guessed rather than resolved.
- The user wants inbound Teams — a Teams trigger, a Teams webhook, or a Teams inbox in Messages. None exist; Teams is send-only.
