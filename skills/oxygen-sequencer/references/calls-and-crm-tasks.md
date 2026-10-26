# Call tasks and CRM tasks

Two step kinds hand work to people or to the CRM instead of messaging the lead.

## Call tasks (`call_task`)

```json
{ "id": "call", "kind": "call_task", "note": "Ask about {{company}}'s rollout", "priority": 10, "timeout_days": 3, "on_timeout": "continue" }
```

- Planning the step queues one call for a person and parks the enrollment until the call is dispositioned. Every disposition resumes it and records `call_connected` (a conversation happened, whatever the answer), `call_voicemail` or `call_no_answer`, which a later `branch` can route on. `on_timeout` decides what happens when nobody calls within `timeout_days` (default 3): `continue` (the default) advances, `stop` ends the enrollment.
- `note` is talking points shown on the dial screen and is never sent. Higher `priority` dials first.
- A person dials in the web softphone. The `voice tasks` commands and `oxygen_voice_*` tools manage the queue (list, claim, complete, skip, override) and never dial.
- `voice tasks list` reports `dialable` and `block_reason` per lead: outside the lead's 09:00-20:00 local window, an unknown timezone (fails closed), the number's daily cap, do-not-call, or an unreachable destination. `voice tasks override` waives the first three for one lead; do-not-call and destination blocks stay.
- A `do_not_call` or `wrong_number` disposition adds the number to do-not-contact by default (`SKILL.md`, Do not contact).
- Numbers: `voice numbers search`, then `voice numbers buy` previews a recurring monthly charge; buy only with `--approved`.
- Outside the US and Canada, `voice verification list` says which countries a workspace can buy in. Where business verification is offered, GB, DE, AT, CH and FR unlock after `voice verification submit` (read the form from `voice numbers requirements --country <iso>`; it previews until `--approved`, and Twilio reviews it in about three business days). NL, ES, IT and PL have no local numbers.

## CRM tasks (`crm_task`)

A CRM task step creates one task in the connected HubSpot account and advances once HubSpot confirms it. It is an external write: a live start needs `--max-live-sends`, and the launch preview's `crm_track` names a missing connection or missing CRM scopes.

```json
{
  "id": "hubspot_call",
  "kind": "crm_task",
  "provider": "hubspot",
  "property_mappings": {
    "hs_timestamp": { "source": "relative_time", "offset_minutes": 1440 },
    "hs_task_subject": { "source": "template", "template": "Call {{first_name}}" },
    "hs_task_type": { "source": "literal", "value": "CALL" },
    "custom_segment": { "source": "row", "key": "segment" }
  },
  "record_mappings": {
    "account": {
      "object_type": "companies",
      "identities": [{ "kind": "domain", "property": "domain", "value": { "source": "row", "key": "company_domain" } }],
      "property_mappings": { "name": { "source": "template", "template": "{{company}}" } },
      "on_missing": "create",
      "on_match": "update"
    },
    "person": {
      "object_type": "contacts",
      "identities": [
        { "kind": "email", "property": "email", "value": { "source": "row", "key": "email" } },
        { "kind": "linkedin_url", "property": "linkedin_url", "value": { "source": "row", "key": "linkedin_url" } }
      ],
      "property_mappings": {},
      "on_missing": "create",
      "on_match": "reuse"
    }
  },
  "record_links": [{ "from_record": "person", "to_record": "account" }],
  "associations": [{ "record_ref": "person" }]
}
```

- `property_mappings` are HubSpot property internal names, custom properties included. Each value is `literal`, `row` (a lead column), `template` (copy syntax) or `relative_time` (minutes after the step runs). `hs_timestamp`, the due date, is required.
- `record_mappings` resolve named records before the task exists. Identities are exact: `provider_id`, `email`, `domain`, `linkedin_url` or `exact`, each with its destination `property` (omitted only for `provider_id`). Matching by name alone is unsupported. `on_missing` defaults to `fail` and `on_match` to `reuse`; creating or updating HubSpot records takes an explicit `create` or `update`.
- `record_links` associate two named records; `associations` attach the task to a named record (`record_ref`) or to an existing id (`object_type` plus `object_id`). Optional `association_type_id` and `association_category` choose a custom association.
- Replay safety: every value (relative times, templates, row values, identities) is frozen into the action before the first HubSpot call, so a retry writes exactly the same request; an exact identity match is reused and conflicting identities fail closed.
- Limits: 100 task properties, 10 named records, 20 links and 20 associations per step. `connection_id` pins a HubSpot connection; otherwise the workspace's active one is used.
- CRM-task leads in a single or mixed journey need a stable `table_row_id` or `lead_provider_id` besides their mapped row values. They remain eligible without email, LinkedIn or phone; unavailable channel steps skip, and CRM identity/property mappings are validated when the task is planned. A HubSpot id in `associations` names the destination record, not the enrollment.
