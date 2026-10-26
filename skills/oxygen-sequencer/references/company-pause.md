# Pause a company

A company pause holds every lead at one company in your campaigns: nothing is sent to them
until someone resumes the company, and then each lead continues where it stopped. It is
the resumable counterpart of a company do-not-contact entry, which blocks every campaign
permanently. Two leads are the same company when they share a work-email domain (Gmail,
Outlook and other freemail never match) or an explicit company-domain or LinkedIn-company
field.

Work-email domains are detected from enrolled leads automatically; you do not enter a
domain for reply-triggered pauses. New sequences leave company reply pause off until you
enable it. If the replier has no work-email domain, company-domain or LinkedIn-company
field, only that lead stops: no company hold is created. The skipped pause is logged as
`no_company_identity`.

## When someone replies (campaign setting)

A reply always stops that lead. To also pause the replier's colleagues in that campaign:

```bash
oxygen sequences update <sequence> --company-reply-pause default --json
oxygen sequences update <sequence> --company-reply-pause interested,not_now,not_interested --json
oxygen sequences update <sequence> --company-reply-pause off --json
oxygen sequences get <sequence> --json # read the saved settings.company_reply_pause
```

`default` is interested, neutral, not_now and not_interested. Reply categories are your inbox
labels (`oxygen inbox labels list --json`), so custom labels work too. The company is held as
soon as a human reply arrives; when the inbox classifies it, the hold stays if the category is
one you chose and lifts on its own if not. Auto-replies and bounces never pause. Web: the
campaign's Launch step, **Reply handling**. MCP: `company_reply_pause` in
`oxygen_sequences_update`.

## On demand, or from a Workflow

```bash
oxygen sequences pause-company --domain acme.com --dry-run --json   # who would be paused, per campaign
oxygen sequences pause-company --domain acme.com --note "meeting booked" --json
oxygen sequences paused-companies --json
oxygen sequences resume-company --domain acme.com --json
```

Name the company with exactly one of `--domain`, `--email` (a work email), `--linkedin-company`
or `--record` (a CRM company, person or deal record id; a person linked to several companies
pauses all of them, a deal pauses the companies it is linked to). Every non-archived campaign
is paused unless you pass `--sequence` (repeatable). MCP: `oxygen_sequences_company_pause`,
`oxygen_sequences_company_resume`, `oxygen_sequences_company_pauses`. Web: Sequencer → Do not
contact → **Paused companies**.

### Meeting booked in the Oxygen CRM → pause that company

Start from `oxygen workflows init --id <id>`, then set the trigger, nodes and edges below
(this exact shape passes `workflows lint --phase publish`). The trigger is the builtin event
`crm.activity_created.meeting_booked` (`oxygen workflows events get
crm.activity_created.meeting_booked --json`). Its payload's `links` is a list of
`{ "object_slug", "row_id", "role" }`, one per record the activity belongs to; pass a `row_id`
as `record_id`. Any linked person, company or deal record works: a person resolves to its
work-email domain and every linked company, a deal to its companies.

```json
{
  "trigger": { "type": "event", "source": "crm", "event": "activity_created",
    "filters": [{ "path": "activity_type", "op": "eq", "value": "meeting_booked" }] },
  "nodes": [
    { "id": "trigger", "name": "Meeting booked", "kind": "trigger",
      "ui": { "x": 0, "y": 0 } },
    { "id": "pause", "name": "Pause company", "kind": "tool",
      "tool": "oxygen_sequences_company_pause", "effect": "external_write",
      "ui": { "x": 320, "y": 0 },
      "params": {
        "record_id": { "type": "ref", "path": "trigger.input.links[0].row_id" },
        "note": { "type": "literal", "value": "meeting booked" }
      } }
  ],
  "edges": [{ "id": "e1", "source": "trigger", "target": "pause" }]
}
```

Leave the step's `mode` unset: a step pinned to `dry_run` only previews and never pauses.

### Meeting booked anywhere else (HubSpot, Calendly, your app)

HubSpot meetings do **not** automatically become Oxygen timeline activities: the native
HubSpot event ingress currently supports contact creation, and imported HubSpot history fires
no event. The CRM **Meeting booked** event above fires when a person, the API, CLI or MCP logs
a `meeting_booked` activity in Oxygen (`oxygen crm activity log people <row_id> --type
meeting_booked --live`), not when a meeting is only saved in HubSpot. Activities written by a
Workflow never fire workflow events, so a meeting logged by the Cal.com meeting router or a
Sequence does not start this workflow. For Cal.com, trigger the pause from the Cal.com
**booking created** integration event instead.

For HubSpot, use a contact-based HubSpot workflow whose enrollment means a new meeting was
booked. Its **Send a webhook** action can call an Oxygen webhook workflow directly; no CRM
record creation or permanent suppression is needed. Confirm your HubSpot subscription exposes
that action before configuring it. [HubSpot's setup guide](https://knowledge.hubspot.com/workflows/how-do-i-use-webhooks-with-hubspot-workflows)
explains the action's availability, custom body and API-key authentication.

Start from the same Oxygen graph above, replacing the trigger and input schema with:

```json
{
  "trigger": { "type": "webhook", "trigger_id": "hubspot-meeting-company-pause",
    "secret_required": true, "idempotency_key_path": "event_id" },
  "input_schema": { "type": "object",
    "properties": { "email": { "type": "string" }, "event_id": { "type": "string" } },
    "required": ["email", "event_id"], "additionalProperties": false }
}
```

In the pause node replace `record_id` with
`"email": { "type": "ref", "path": "trigger.input.email" }`. Keep its `effect` and leave
`mode` unset. Omit `sequence_ids` to hold the company across all non-archived campaigns;
this uses the same durable hold and dispatch protection as `company_reply_pause`.

Configure HubSpot's action as follows:

1. POST to the **workflow-specific** `webhook_url` returned when Oxygen publishes the graph.
2. Choose **API key** authentication in the request **header**, named
   `x-oxygen-workflow-secret`, with the one-time `webhookSecret` returned on publish.
   Keep that secret in HubSpot's secret store; Oxygen's HubSpot app-signature endpoint is a
   different ingress. Rotate through Oxygen if the secret has been lost.
3. Customize the JSON body to exactly `{ "email": "<booker's work email>",
   "event_id": "<stable unique booking identifier>" }`. Map actual HubSpot properties;
   placeholders are not literal values. The booking identifier must stay the same on retries
   and change for each new booking; contact id alone would discard later meetings. A stored
   booking timestamp plus contact id is an alternative when composed in the source workflow.
4. Lint and publish the Oxygen graph, inspect its call preview, and dry-run with that exact
   body. After approval, enable it with an explicit positive per-delivery credit ceiling.
   Enable the HubSpot workflow only after both the recipient mapping and scope are reviewed.
5. Send a controlled test booking and read the Oxygen workflow run and
   `oxygen sequences paused-companies --json`. A webhook HTTP 202 means queued; check the
   completed pause step and its `total_enrollments` before claiming the company stopped.

This direct webhook pauses outreach; it does not itself add a CRM meeting timeline entry.
An absent email, freemail address, or unresolved company must be corrected at the source;
never substitute the contact's name as a company identity. Repeated deliveries of one booking
reuse its run via `event_id`. Resuming is explicit with `oxygen sequences resume-company`;
a separate new booking can pause the company again. Calendly or your own app can send the
same authenticated payload.

Emails already handed to a bound Instantly campaign keep sending from Instantly; a pause that
reaches such a campaign says so under `warnings` (`instantly_email_not_paused`).

Lint, apply and enable as usual (`oxygen-workflow-authoring`). Like every write step, the pause
step is enabled with approval and a credit ceiling, and a run bills its step at the usual
workflow rate; the pause itself costs nothing and sends nothing. A resume restarts sending, so
it asks for approval in the Copilot.
