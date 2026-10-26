# Play: hand-written first messages to buyers already in your network

## When

The user asks to "work my network" or "reactivate my connections". This play writes one message per person by hand and never bulk-enrolls connections into a templated Sequence: in OXYGEN's own outreach, 9 of 76 replied threads were apologies for an automated message to someone the sender already knew.

## Numbers

- Expect a small list after the fit gate; say so before the capture finishes.
- Keep a company when it fits the ICP and shows it by a countable fact (for a sales-tool ICP, for example, 3+ current seller titles and 5–500 staff). Companies above the ICP's size band go on a separate account-based list.
- Keep a person on the buying committee who has never been contacted and is not at a customer. In this play, one message per company: to the buyer, or to the person who engages with the sender's posts.
- Recommended default, not a product rule: the user approves each text for its recipient before it is sent. On Auto-approve, say this play recommends per-message review and follow the user's choice.
- Draft about 5 for a new sender or language, then batches of 10.
- No automated follow-up (`oxygen-sequencer` skill, [LinkedIn volume](../../oxygen-sequencer/references/linkedin-volume.md)).

## Steps

1. **Capture:** `oxygen linkedin network setup --json`, then wait for the first walk (`linkedin network status`). The capture may hold names without titles: enrich the candidates (`oxygen-enrichment` skill) or import the user's own LinkedIn connections export as a Table.
2. **Count the ICP fact** per company: `oxygen tools search "count current employees by job title at a company" --json`, `oxygen tools get <tool_id> --json`, then quote with `oxygen tools run <tool_id> --mode dry-run --input-json '<input>' --json` before any live run.
3. **Qualify** with the `qualification` column ([qualification](../references/qualification.md)) and give the user a review table with a Go / Skip select.
4. **Exclude** everyone [qualification](../references/qualification.md) § 7 lists. Read any thread hit with `oxygen inbox get <conversation> --json` and show the user old one-sided cold messages: the new message lands under them.
5. **Research each Go company** for one dated current fact (a hire, a launch, a round, the person's own recent post) with a research column (`oxygen-tables` skill), quoted first with `--dry-run`.
6. **Draft by hand**, one message per company, following the first-message rules in the `oxygen-unibox` skill (`oxygen skills get oxygen-unibox --file references/dm-conversion.md`). Show each draft with the fact behind it; leave out sensitive facts such as layoffs.
7. **Check each approved recipient**, free and silent:

   ```bash
   oxygen tools run linkedin.users_get --mode live --max-credits 0 \
     --input-json '{"identifier":"<public id>","account_id":"<account id>","notify":false}' --json
   ```

   Send only when `response.network_distance` is `FIRST_DEGREE` and `response.display_name` matches. Each check spends a profile lookup, so check about 20 people on a send day, or the day before. A second-degree person needs a separate invite Sequence (blank invite, the text after acceptance), approved on its own.
8. **Send through one Sequence** for every approved text, not one per message. Steps: `{ "steps": [ { "id": "dm", "kind": "message", "template": "{{dm_text}}" } ] }`.

   ```bash
   oxygen sequences create --name "Network DMs" --slug network-dms --steps-file steps.json --senders <sender> --json
   ```

   Enroll each person with `sequences enroll <sequence> --leads-file <file>` as `{"lead_provider_id":"<ACo… member id>","lead_name":"<name>","row_values":{"dm_text":"<the approved text, exactly>"}}`; a member id spends no lookup, and rows without one take it from step 7's `response.id`. Preview and render, then `sequences start <sequence> --approved --max-live-sends <number approved>`.
9. **Read back** with `oxygen sequences enrollments <sequence> --json` and tell the user when held sends are due.

## Kill and scale

- Answer replies by hand the same day (`oxygen-unibox` skill).
- Scale by batch, never by switching to a template.
