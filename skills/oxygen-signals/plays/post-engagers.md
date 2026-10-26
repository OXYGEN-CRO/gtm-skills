# Play: start conversations with the buyers who engage with your posts

## When

The user posts on LinkedIn and asks to reach the people who react or comment. Commenters who asked for a lead-magnet resource are owed the resource, not outreach: leave them out of this play.

## Numbers

- Enroll only people with high company fit and high person fit ([qualification](../references/qualification.md)): in OXYGEN's own campaign most engagers who replied were not buyers.
- First-degree engagers get a message; everyone else a blank invite, up to 14 days for acceptance, then the message. Volume, notes, follow-ups and kill lines: `oxygen-sequencer` skill, [LinkedIn volume](../../oxygen-sequencer/references/linkedin-volume.md).

## Steps

1. **Capture.** Your own posts through the connected account, free and metered: `oxygen posts get --post <post-url> --account <ref> --json` for the `social_id`, then `oxygen engagement harvest --post <social_id> --source unipile --recurring --json` ([LinkedIn captures](../references/linkedin.md)). A daily watcher of 1–10 public profiles is paid per cycle ([public research](../references/public-research.md)).
2. **Qualify.** The harvest table holds only name, headline and engagement type: enrich person and company first (`oxygen-enrichment` skill), then add the `qualification` column ([qualification](../references/qualification.md)).
3. **Exclude** lead-magnet commenters, then everyone [qualification](../references/qualification.md) § 7 lists.
4. **Draft the Sequence** with manual enrollment, so launching cannot enroll the whole engager table:

   ```bash
   oxygen sequences create --name "Post engagers" --slug post-engagers --steps-file steps.json \
     --table <table> --senders <sender> --no-auto-enroll-table-rows --exclude-contacted --json
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

   For the one nudge, add a `wait` and a second `message` step to each arm (LinkedIn volume, Follow-ups).
5. **Write the opener** into an `opener` column, one per person, by hand or with an AI column (`oxygen-tables` skill), following the first-message rules in the `oxygen-unibox` skill (`oxygen skills get oxygen-unibox --file references/dm-conversion.md`). A commenter's opener uses their actual comment (read it with `oxygen posts comments --post <social_id> --json`); a reaction alone gives no personal hook to invent.
6. **Launch** through the Sequence ladder: `sequences preview` and `sequences render` show every rendered opener, then `sequences enroll <sequence> --leads-file <file>` with only the qualified `table_row_id`s, carrying `lead_provider_id` from `provider_id`, and `sequences start <sequence> --approved` with the approved ceilings (`oxygen-sequencer` skill, Launch ladder).
7. **Repeat daily** for newly qualified rows, or arm the router from step 6 of the qualification reference.
8. **Replies:** answer buyers the same day, as the `oxygen-unibox` DM conversion reference routes them.

## Kill and scale

- Acceptance under the campaign kill line: pause and re-check the rubric before the copy.
- Replies arriving mostly from non-buyers: tighten the rubric, not the opener.
- Scale by posting more or watching more relevant public profiles, never by loosening the fit gate.
