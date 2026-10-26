# Play: invite the buyers who view your profile or follow you

## When

The user wants outreach to named profile viewers or to people who follow them without being connected. One play covers both; viewers go first.

## Numbers

- Rank viewers before followers: in OXYGEN's own run, viewers passed the fit gate about three times as often as follow-only followers.
- Followers carry no follow date, so a follower's recency is unknown.
- At most 10 new people a day (`--max-new-enrollments-per-day 10`) beside the account's own caps (`oxygen-sequencer` skill, [LinkedIn volume](../../oxygen-sequencer/references/linkedin-volume.md)).

## Steps

1. **Capture**, free and metered on the account ([LinkedIn captures](../references/linkedin.md)):
   - Viewers: `oxygen viewers import --account <ref> --json`.
   - Followers: `oxygen linkedin network setup --json`, then the follow-only rows of the LinkedIn Network table:

     ```bash
     oxygen tables query <network-table> --fields provider_id,full_name,title,company,location,profile_url \
       --filter-tree-json '{"type":"group","conjunction":"and","children":[{"type":"leaf","columnKey":"is_follower","operator":"is_true"},{"type":"leaf","columnKey":"is_connection","operator":"is_empty"}]}' --json
     ```

2. **Exclude before paying for anything** everyone [qualification](../references/qualification.md) § 7 lists, and followers whose `location` lies outside the ICP's regions. Viewers carry only `headline`; gate their region after enrichment.
3. **One scoring table.** Put the remaining viewers and followers in one table with a `signal` column (`viewer` or `follower`) and the `provider_id`: `oxygen tables import --create "Viewers and followers" --file <rows.json> --format json --json`. Enrich the person and company evidence the rubric needs (`oxygen-enrichment` skill), then add and calibrate the `qualification` column ([qualification](../references/qualification.md)).
4. **Draft the Sequence:**

   ```bash
   oxygen sequences create --name "Viewers and followers" --slug viewers-followers --steps-file steps.json \
     --table <scoring-table> --senders <sender> --no-auto-enroll-table-rows --exclude-contacted \
     --max-new-enrollments-per-day 10 --json
   ```

   ```json
   { "steps": [
     { "id": "connected", "kind": "branch", "condition": "already_connected", "then_id": "dm", "else_id": "invite" },
     { "id": "dm", "kind": "message", "template": "{{opener}}" },
     { "id": "end_dm", "kind": "stop" },
     { "id": "invite", "kind": "invite" },
     { "id": "accept", "kind": "wait_for_connection", "timeout_days": 14, "on_timeout": "stop" },
     { "id": "dm_after_accept", "kind": "message", "template": "{{opener}}" }
   ] }
   ```

5. **Opener:** the first-message rules in the `oxygen-unibox` skill (`oxygen skills get oxygen-unibox --file references/dm-conversion.md`).
6. **Launch:** preview and render, then enroll the qualified viewers' row ids before the followers' (`sequences enroll <sequence> --leads-file <file>`, carrying `lead_provider_id` from `provider_id`), and start with approval (`oxygen-sequencer` skill, Launch ladder).

## Kill and scale

- The campaign acceptance kill line applies (LinkedIn volume). Below it, check whether followers drag the rate down and stop enrolling them first.
- A new batch of viewers arrives with every capture walk; re-score new rows only, never the whole table again.
