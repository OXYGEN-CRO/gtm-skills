# Play: message the buyers among your new connections

## When

The user wants to follow up with people who connected recently. They are already first-degree, so this play sends messages only and never an invite; invites stay free for the plays that need them.

## Numbers

- In OXYGEN's own pilot, about a quarter of qualified new connections already had a thread with the sender: check every one.
- At most 10 new people a day (`--max-new-enrollments-per-day 10`). Volume, follow-ups and kill lines: `oxygen-sequencer` skill, [LinkedIn volume](../../oxygen-sequencer/references/linkedin-volume.md).

## Steps

1. **Capture** the network, free and metered: `oxygen linkedin network setup --json`. Until `oxygen linkedin network status --json` shows the drips in `delta`, the first walk is still filling the table ([LinkedIn captures](../references/linkedin.md)).
2. **Select recent connections:**

   ```bash
   oxygen tables query <network-table> --fields provider_id,full_name,title,company,location,profile_url,connected_at \
     --filter-tree-json '{"type":"group","conjunction":"and","children":[{"type":"leaf","columnKey":"is_connection","operator":"is_true"},{"type":"leaf","columnKey":"connected_at","operator":"on_or_after","value":"<iso-date>"}]}' --json
   ```

3. **Exclude** lead-magnet recipients, people outside the ICP's regions, and everyone [qualification](../references/qualification.md) § 7 lists.
4. **Score** in their own table: `oxygen tables import --create "New connections" --file <rows.json> --format json --json`, enrich the evidence the rubric needs (`oxygen-enrichment` skill), then calibrate and run the `qualification` column ([qualification](../references/qualification.md)).
5. **Draft the Sequence** with manual enrollment:

   ```bash
   oxygen sequences create --name "New connections" --slug new-connections --steps-file steps.json \
     --table <scoring-table> --senders <sender> --no-auto-enroll-table-rows --exclude-contacted \
     --max-new-enrollments-per-day 10 --json
   ```

   ```json
   { "steps": [
     { "id": "connected", "kind": "branch", "condition": "already_connected", "then_id": "dm", "else_id": "end" },
     { "id": "dm", "kind": "message", "template": "{{opener}}" },
     { "id": "end", "kind": "stop" }
   ] }
   ```

   The connection check reads the profile once per person; it stops anyone who removed the connection.
6. **Opener:** the first-message rules in the `oxygen-unibox` skill (`oxygen skills get oxygen-unibox --file references/dm-conversion.md`).
7. **Launch:** preview and render, enroll only the qualified row ids with their `provider_id` as `lead_provider_id`, then start with approval (`oxygen-sequencer` skill, Launch ladder).

## Kill and scale

- Read the first replies before making this a daily flow. If they come mostly from non-buyers, tighten the rubric.
- As a daily flow, select connections since the last run (step 2 with the last run's date) and enroll the newly qualified rows into the same Sequence.
